"""Generated from mgga_x_mbeefvdw.mpl."""

import jax
import jax.lax as lax
import jax.numpy as jnp
from jax.numpy import array as array
from jax.numpy import int32 as int32
from jax.numpy import nan as nan
from typing import Callable, Optional
from .utils import *


def pol(p, r, s=(None, None, None), l=(None, None), tau=(None, None)):
  params = p.params
  (r0, r1), (s0, s1, s2), (l0, l1), (tau0, tau1) = r, s, l, tau
  t2 = jnp.cbrt(3)
  t3 = jnp.cbrt(jnp.pi)
  t5 = t2 / t3
  t6 = r0 + r1
  t7 = 0.1e1 / t6
  t10 = 0.2e1 * r0 * t7 <= p.zeta_threshold
  t11 = p.zeta_threshold - 0.1e1
  t14 = 0.2e1 * r1 * t7 <= p.zeta_threshold
  t15 = -t11
  t17 = (r0 - r1) * t7
  t18 = lax_cond(t14, t15, t17)
  t19 = lax_cond(t10, t11, t18)
  t20 = t19 + 0.1e1
  t22 = jnp.cbrt(p.zeta_threshold)
  t23 = t22 * p.zeta_threshold
  t24 = jnp.cbrt(t20)
  t26 = lax_cond(t20 <= p.zeta_threshold, t23, t24 * t20)
  t27 = jnp.cbrt(t6)
  t29 = jnp.cbrt(r0)
  t30 = t29 ** 2
  t34 = r0 ** 2
  t37 = s0 / t30 / t34
  t40 = jnp.cbrt(6)
  t42 = jnp.pi ** 2
  t43 = jnp.cbrt(t42)
  t44 = t43 ** 2
  t45 = 0.1e1 / t44
  t47 = 0.5e1 / 0.9e1 * (tau0 / t30 / r0 - t37 / 0.8e1) * t40 * t45
  t49 = 0.1e5 < t47
  t50 = lax_cond(t49, t47, 0.1e5)
  t51 = t50 ** 2
  t56 = t51 ** 2
  t60 = lax_cond(t49, 0.1e5, t47)
  t61 = t60 ** 2
  t62 = 0.1e1 - t61
  t63 = t62 ** 2
  t65 = t61 * t60
  t71 = lax_cond(0.1e5 <= t47, 0.1e1 - 0.3e1 / t51 - 0.1e1 / t51 / t50 + 0.3e1 / t56, -t63 * t62 / (0.1e1 + t65 * (0.1e1 + t65)))
  t72 = t71 ** 2
  t73 = t72 * t71
  t77 = t72 ** 2
  t79 = t40 * t45
  t85 = t79 * t37 / (0.65124e1 + t79 * t37 / 0.24e2)
  t87 = t85 / 0.12e2 - 0.1e1
  t88 = t87 ** 2
  t90 = t88 ** 2
  t92 = t88 * t87
  t96 = -0.1e1 / 0.2e1 + 0.3e1 / 0.2e1 * t88
  t98 = -0.1e1 / 0.2e1 + 0.3e1 / 0.2e1 * t72
  t103 = 0.5e1 / 0.2e1 * t73 - 0.3e1 / 0.2e1 * t71
  t108 = 0.3e1 / 0.8e1 + 0.35e2 / 0.8e1 * t77 - 0.15e2 / 0.4e1 * t72
  t113 = 0.5e1 / 0.2e1 * t92 - t85 / 0.8e1 + 0.3e1 / 0.2e1
  t116 = 0.351985355e-2 * t73 + 0.217681859775e-1 * t72 - 0.6972770593e-1 * t71 + 0.61919587625e-3 * t77 - 0.851282539125e-1 * t88 + 0.618699843125e-2 * t90 - 0.50282912e-1 * t92 + 0.1214700985e-1 * t85 - 0.521818079e-2 * t96 * t98 - 0.657949254e-6 * t96 * t103 + 0.201895739e-6 * t96 * t108 + 0.192374554e-1 * t113 * t71
  t125 = 0.3e1 / 0.8e1 + 0.35e2 / 0.8e1 * t90 - 0.15e2 / 0.4e1 * t88
  t144 = 0.10451438955835e1 + 0.133707403e-6 * t113 * t98 - 0.549909413e-7 * t113 * t103 + 0.397324768e-8 * t113 * t108 + 0.919317034e-6 * t125 * t71 - 0.500749348e-6 * t125 * t98 + 0.574317889e-7 * t125 * t103 - 0.340722258e-8 * t125 * t108 + 0.453837246e-1 * t87 * t71 + 0.318024096e-1 * t87 * t98 - 0.608338264e-2 * t87 * t103 - 0.100478906e-6 * t87 * t108 - 0.222650139e-1 * t96 * t71
  t149 = lax_cond(r0 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t26 * t27 * (t116 + t144))
  t151 = lax_cond(t10, t15, -t17)
  t152 = lax_cond(t14, t11, t151)
  t153 = t152 + 0.1e1
  t155 = jnp.cbrt(t153)
  t157 = lax_cond(t153 <= p.zeta_threshold, t23, t155 * t153)
  t159 = r1 ** 2
  t160 = jnp.cbrt(r1)
  t161 = t160 ** 2
  t164 = s2 / t161 / t159
  t170 = t79 * t164 / (0.65124e1 + t79 * t164 / 0.24e2)
  t172 = t170 / 0.12e2 - 0.1e1
  t173 = t172 ** 2
  t174 = t173 * t172
  t183 = 0.5e1 / 0.9e1 * (tau1 / t161 / r1 - t164 / 0.8e1) * t40 * t45
  t185 = 0.1e5 < t183
  t186 = lax_cond(t185, t183, 0.1e5)
  t187 = t186 ** 2
  t192 = t187 ** 2
  t196 = lax_cond(t185, 0.1e5, t183)
  t197 = t196 ** 2
  t198 = 0.1e1 - t197
  t199 = t198 ** 2
  t201 = t197 * t196
  t207 = lax_cond(0.1e5 <= t183, 0.1e1 - 0.3e1 / t187 - 0.1e1 / t187 / t186 + 0.3e1 / t192, -t199 * t198 / (0.1e1 + t201 * (0.1e1 + t201)))
  t208 = t207 ** 2
  t209 = t208 * t207
  t213 = t208 ** 2
  t216 = t173 ** 2
  t220 = -0.1e1 / 0.2e1 + 0.3e1 / 0.2e1 * t173
  t223 = 0.5e1 / 0.2e1 * t209 - 0.3e1 / 0.2e1 * t207
  t228 = 0.3e1 / 0.8e1 + 0.35e2 / 0.8e1 * t213 - 0.15e2 / 0.4e1 * t208
  t232 = -0.1e1 / 0.2e1 + 0.3e1 / 0.2e1 * t208
  t237 = -0.50282912e-1 * t174 + 0.351985355e-2 * t209 - 0.6972770593e-1 * t207 + 0.217681859775e-1 * t208 + 0.61919587625e-3 * t213 - 0.851282539125e-1 * t173 + 0.618699843125e-2 * t216 + 0.1214700985e-1 * t170 - 0.657949254e-6 * t220 * t223 + 0.201895739e-6 * t220 * t228 - 0.521818079e-2 * t220 * t232 - 0.222650139e-1 * t220 * t207
  t248 = 0.3e1 / 0.8e1 + 0.35e2 / 0.8e1 * t216 - 0.15e2 / 0.4e1 * t173
  t259 = 0.5e1 / 0.2e1 * t174 - t170 / 0.8e1 + 0.3e1 / 0.2e1
  t268 = 0.10451438955835e1 - 0.608338264e-2 * t172 * t223 - 0.100478906e-6 * t172 * t228 + 0.318024096e-1 * t172 * t232 + 0.453837246e-1 * t172 * t207 - 0.340722258e-8 * t248 * t228 + 0.574317889e-7 * t248 * t223 - 0.500749348e-6 * t248 * t232 + 0.919317034e-6 * t248 * t207 + 0.397324768e-8 * t259 * t228 - 0.549909413e-7 * t259 * t223 + 0.133707403e-6 * t259 * t232 + 0.192374554e-1 * t259 * t207
  t273 = lax_cond(r1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t157 * t27 * (t237 + t268))
  res = t149 + t273
  return res


def unpol(p, r, s=None, l=None, tau=None):
  params = p.params
  r0, s0, l0, tau0 = r, s, l, tau
  t3 = jnp.cbrt(3)
  t4 = jnp.cbrt(jnp.pi)
  t7 = 0.1e1 <= p.zeta_threshold
  t8 = p.zeta_threshold - 0.1e1
  t10 = lax_cond(t7, -t8, 0)
  t11 = lax_cond(t7, t8, t10)
  t12 = t11 + 0.1e1
  t14 = jnp.cbrt(p.zeta_threshold)
  t16 = jnp.cbrt(t12)
  t18 = lax_cond(t12 <= p.zeta_threshold, t14 * p.zeta_threshold, t16 * t12)
  t19 = jnp.cbrt(r0)
  t21 = jnp.cbrt(2)
  t22 = t21 ** 2
  t24 = t19 ** 2
  t29 = r0 ** 2
  t31 = 0.1e1 / t24 / t29
  t32 = s0 * t22 * t31
  t35 = jnp.cbrt(6)
  t37 = jnp.pi ** 2
  t38 = jnp.cbrt(t37)
  t39 = t38 ** 2
  t40 = 0.1e1 / t39
  t42 = 0.5e1 / 0.9e1 * (tau0 * t22 / t24 / r0 - t32 / 0.8e1) * t35 * t40
  t44 = 0.1e5 < t42
  t45 = lax_cond(t44, t42, 0.1e5)
  t46 = t45 ** 2
  t51 = t46 ** 2
  t55 = lax_cond(t44, 0.1e5, t42)
  t56 = t55 ** 2
  t57 = 0.1e1 - t56
  t58 = t57 ** 2
  t60 = t56 * t55
  t66 = lax_cond(0.1e5 <= t42, 0.1e1 - 0.3e1 / t46 - 0.1e1 / t46 / t45 + 0.3e1 / t51, -t58 * t57 / (0.1e1 + t60 * (0.1e1 + t60)))
  t67 = t66 ** 2
  t68 = t67 ** 2
  t70 = t67 * t66
  t74 = t35 * t40
  t82 = t74 * s0 * t22 * t31 / (0.65124e1 + t74 * t32 / 0.24e2)
  t84 = t82 / 0.12e2 - 0.1e1
  t85 = t84 ** 2
  t86 = t85 * t84
  t89 = t85 ** 2
  t93 = 0.3e1 / 0.8e1 + 0.35e2 / 0.8e1 * t89 - 0.15e2 / 0.4e1 * t85
  t95 = -0.1e1 / 0.2e1 + 0.3e1 / 0.2e1 * t67
  t100 = 0.5e1 / 0.2e1 * t70 - 0.3e1 / 0.2e1 * t66
  t105 = 0.3e1 / 0.8e1 + 0.35e2 / 0.8e1 * t68 - 0.15e2 / 0.4e1 * t67
  t112 = 0.61919587625e-3 * t68 + 0.351985355e-2 * t70 + 0.217681859775e-1 * t67 - 0.6972770593e-1 * t66 - 0.50282912e-1 * t86 - 0.851282539125e-1 * t85 + 0.618699843125e-2 * t89 - 0.500749348e-6 * t93 * t95 + 0.574317889e-7 * t93 * t100 - 0.340722258e-8 * t93 * t105 + 0.453837246e-1 * t84 * t66 + 0.318024096e-1 * t84 * t95
  t118 = -0.1e1 / 0.2e1 + 0.3e1 / 0.2e1 * t85
  t129 = 0.5e1 / 0.2e1 * t86 - t82 / 0.8e1 + 0.3e1 / 0.2e1
  t141 = 0.10451438955835e1 - 0.608338264e-2 * t84 * t100 - 0.100478906e-6 * t84 * t105 - 0.222650139e-1 * t118 * t66 - 0.521818079e-2 * t118 * t95 - 0.657949254e-6 * t118 * t100 + 0.201895739e-6 * t118 * t105 + 0.192374554e-1 * t129 * t66 + 0.133707403e-6 * t129 * t95 - 0.549909413e-7 * t129 * t100 + 0.397324768e-8 * t129 * t105 + 0.919317034e-6 * t93 * t66 + 0.1214700985e-1 * t82
  t146 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t3 / t4 * t18 * t19 * (t112 + t141))
  res = 0.2e1 * t146
  return res


def invoke(
  p: NamedTuple, rho: Callable, r: jnp.ndarray, mo: Optional[Callable] = None,
  deorbitalize: Optional[float] = None,
):
  args = rho_to_arguments(p, rho, r, mo, deorbitalize)
  code = pol if p.nspin == 2 else unpol
  dens = args[0] if p.nspin == 1 else sum(args[0])
  ret = lax.cond((dens < p.dens_threshold), lambda *_: 0.,
                 lambda *_: code(p, *args), None)
  return ret