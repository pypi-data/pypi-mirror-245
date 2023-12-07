# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Flax layer for AQT injection."""

import enum
import functools
from . import q_dot_general
from . import calibration
from . import config
from . import int_numerics
import flax.linen as nn
import jax.numpy as jnp
from typing import Optional, Union


class Freezer(nn.Module, config.Preprocess):
    """Identity function that can freeze its input.

    On default, it is an identity function that saves the input in a variable.
    In 'use_frozen=True' mode, ignores the input and returns the frozen value. It
    is usefult to implement 'constant folding' and put quantized weights and
    scales in the checkpoint for serving.
    """

    # If you want use 'params' make sure that there is another mechanism to hide
    # these variables from the optimizer.
    var_collection: str = 'q'

    # If you set it to True, instead of returning the current input
    # will return last input it got.
    use_frozen: bool = False

    @nn.compact
    def __call__(self, inputs):
        # return inputs or the frozen value
        collection = self.var_collection
        frozen = self.variable(collection, 'frozen', jnp.zeros, inputs.shape)
        if not self.use_frozen:
            frozen.value = inputs
        return frozen.value


class QDotGeneral(nn.Module):
    """A layer that can be injected into flax.nn.Dense, etc."""

    cfg: Optional[Union[config.DotGeneral, None]] = None
    prng_name: Optional[Union[str, None]] = 'params'

    @nn.compact
    def __call__(
            self,
            lhs,
            rhs,
            dimension_numbers,
            precision,
            preferred_element_type=None,
    ):
        key = self.make_rng(self.prng_name) if self.prng_name is not None else None
        context = q_dot_general.Context(key=key, train_step=None)
        q_dg = q_dot_general.make_dot_general(self.cfg)
        q_dg = functools.partial(q_dg, context=context)
        return q_dg(
            lhs,
            rhs,
            dimension_numbers,
            precision,
            preferred_element_type=preferred_element_type,
        )


class QEinsum(nn.Module):
    """Quantized Einsum class for model injection."""

    cfg: Optional[Union[config.DotGeneral, None]] = None
    prng_name: Optional[Union[str, None]] = 'params'

    @nn.compact
    def __call__(self, eqn, lhs, rhs):
        key = self.make_rng(self.prng_name) if self.prng_name is not None else None
        context = q_dot_general.Context(key=key, train_step=None)
        q_dg = q_dot_general.make_dot_general(self.cfg)
        q_dg = functools.partial(q_dg, context=context)
        return jnp.einsum(eqn, lhs, rhs, _dot_general=q_dg)


class QuantMode(enum.Enum):
    DYNAMIC = 1
    FREEZE = 2
    SERVE_FROZEN = 3


def mk_freezer(name: str, freeze_collection: str, mode: QuantMode):
    """
    The mk_freezer function is a helper function that returns a Freezer object.

    :param name: str: Name the freezer object
    :param freeze_collection: str: Specify the collection of variables to be frozen
    :param mode: QuantMode: Determine whether to use the frozen graph or not
    :return: A freezer object
    
    """
    assert mode in QuantMode
    if mode == QuantMode.DYNAMIC:
        return None
    use_frozen = mode == QuantMode.SERVE_FROZEN
    return functools.partial(
        Freezer,
        name=name,
        use_frozen=use_frozen,
        var_collection=freeze_collection,
    )


def set_rhs_quant_mode(
        cfg: config.DotGeneral, mode: QuantMode, collection='q'
):
    cfg.fwd.rhs.preprocess_quant_cls = mk_freezer('rhs', collection, mode)
    cfg.fwd.rhs.preprocess_scale_cls = mk_freezer('rhs_scale', collection, mode)


def set_lhs_quant_mode(
        cfg: config.DotGeneral, mode: QuantMode, collection='q'
):
    cfg.fwd.lhs.preprocess_quant_cls = mk_freezer('lhs', collection, mode)
    cfg.fwd.lhs.preprocess_scale_cls = mk_freezer('lhs_scale', collection, mode)


def config_v4(
        *,
        fwd_bits: Union[int, None],
        dlhs_bits: Union[int, None],
        drhs_bits: Union[int, None],
        # The dummy static bound flag is for performance benchmarking.
        use_dummy_static_bound: bool = False,
        rng_type: str = 'jax.uniform',  # 'custom-1'
        dlhs_local_q: Union[config.LocalQ, None] = None,
        drhs_local_q: Union[config.LocalQ, None] = None,
        fwd_accumulator_dtype: ... = jnp.int32,
        dlhs_accumulator_dtype: ... = jnp.int32,
        drhs_accumulator_dtype: ... = jnp.int32,
        lhs_quant_mode: QuantMode = QuantMode.DYNAMIC,
        rhs_quant_mode: QuantMode = QuantMode.DYNAMIC,
        freeze_collection: str = 'q',
) -> config.DotGeneral:
    """
    The config_v4 function is a helper function that creates the configuration
    for quantization. It takes in several arguments and returns a config object.
    The config object contains three DotGeneralRaw objects, one for each of the forward pass, left hand side gradient,
    and right hand side gradient. Each DotGeneralRaw object has two Tensor objects: one for the left hand side
    tensor and another for the right hand side tensor. The Tensor class contains information about how to quantize
     each of these tensors (e.g., number of bits). The following are some examples on how to use this function:

    :param *: Pass in a dictionary of parameters
    :param fwd_bits: Union[int,None]: Set the number of bits for the forward pass
    :param dlhs_bits: Union[int,None]: Set the number of bits for the left hand side of a matrix multiplication
    :param drhs_bits: Union[int,None]: Determine the number of bits for quantization
    :param # The dummy static bound flag is for performance benchmarking.
            use_dummy_static_bound: bool: Set the static bound to 1
    :param rng_type: str: Set the random number generator type
    :param # 'custom-1'
            dlhs_local_q: Union[config.LocalQ,None]: Set the random number generator type
    :param drhs_local_q: Union[config.LocalQ,None]: Set the quantization parameters for the right hand side of a matrix multiplication
    :param fwd_accumulator_dtype: ...: Set the accumulator dtype for forward pass
    :param dlhs_accumulator_dtype: ...: Set the accumulator dtype for the left hand side of a matrix multiplication
    :param drhs_accumulator_dtype: ...: Set the accumulator dtype for the right hand side of a matrix multiplication
    :param lhs_quant_mode: QuantMode: Determine whether the left hand side of the matrix multiplication is quantized or not
    :param rhs_quant_mode: QuantMode: Determine whether the right hand side of the matrix multiplication is quantized or not
    :param freeze_collection: str: Freeze the quantization parameters
    :param : Determine which side of the matmul is frozen
    :return: A config
    
    """

    def tensor_config(bits: Union[int, None]) -> config.Tensor:
        assert bits is None or bits >= 2, 'Need at least 2 bits.'
        if bits is None:
            numerics = config.NoNumerics()
        else:
            numerics = int_numerics.IntNumerics(
                bits=bits,
                preserve_zero=True,
                preserve_max_val=False,
                clip=True,
                round=True,
                noise_fn=None,
                clip_gradient=False,  # Can be False when using abs-max scaling.
            )

        return config.Tensor(
            numerics=numerics,
            calib_shared_axes=None,
            scale_stop_grad=True,
            calibration=calibration.AbsMaxCalibration(),
            po2_scale=False,
            use_fake_quant=False,
            # dtype_x=dtype,
            use_fwd_quant=None,
            preprocess_quant_cls=None,
            preprocess_scale_cls=None,
        )

    def dg_raw_config(lhs_bits, rhs_bits, local_q=None) -> config.DotGeneralRaw:
        lhs_cfg = tensor_config(lhs_bits)
        rhs_cfg = tensor_config(rhs_bits)
        if (
                True  # Just to format lines below
                and lhs_bits is not None
                and rhs_bits is not None
                and lhs_bits <= 8
                and rhs_bits <= 8
        ):
            dg_in_dtype = jnp.int8
            dg_accumulator_dtype = jnp.int32
        else:
            # None determines the dtype on the fly in q_dot_general
            dg_in_dtype = None
            dg_accumulator_dtype = None

        return config.DotGeneralRaw(
            lhs=lhs_cfg,
            rhs=rhs_cfg,
            dg_in_dtype=dg_in_dtype,
            dg_accumulator_dtype=dg_accumulator_dtype,
            local_q=local_q,
        )

    cfg = config.DotGeneral(
        fwd=dg_raw_config(fwd_bits, fwd_bits),
        dlhs=dg_raw_config(dlhs_bits, dlhs_bits, local_q=dlhs_local_q),
        drhs=dg_raw_config(drhs_bits, drhs_bits, local_q=drhs_local_q),
    )

    cfg.dlhs.rhs.use_fwd_quant = False
    cfg.drhs.rhs.use_fwd_quant = False

    # Typically we have (but I don't know if it is guraranteed):
    # - vjp_lhs_stochastic_rounding is referring to the gradient and
    # - vjp_rhs_stochastic_rounding is referring to the activations/weights.
    config.set_stochastic_rounding(
        cfg,
        vjp_lhs_stochastic_rounding=True,
        vjp_rhs_stochastic_rounding=False,
        implementation=rng_type,
    )

    if use_dummy_static_bound:
        config.set_static_bound(cfg, 1.0)

    config.set_accumulator_dtype(
        cfg,
        fwd_dtype=fwd_accumulator_dtype,
        dlhs_dtype=dlhs_accumulator_dtype,
        drhs_dtype=drhs_accumulator_dtype,
    )

    assert (
            lhs_quant_mode == QuantMode.DYNAMIC or rhs_quant_mode == QuantMode.DYNAMIC
    ), (
        'It seems unlikely that both sides of the matmul should be frozen.'
        ' E.g. both sides of the matmul be weights. '
    )

    set_rhs_quant_mode(cfg, rhs_quant_mode, freeze_collection)
    set_lhs_quant_mode(cfg, lhs_quant_mode, freeze_collection)

    return cfg
