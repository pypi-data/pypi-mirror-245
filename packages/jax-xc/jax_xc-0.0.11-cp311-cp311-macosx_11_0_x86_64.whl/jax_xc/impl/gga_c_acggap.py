"""Generated from gga_c_acggap.mpl."""

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
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t4 = t1 * t3
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t7 = r0 + r1
  t8 = jnp.cbrt(t7)
  t10 = t6 / t8
  t11 = t4 * t10
  t14 = jnp.sqrt(t11)
  t17 = t11 ** 0.15e1
  t19 = t1 ** 2
  t20 = t3 ** 2
  t22 = t8 ** 2
  t25 = t19 * t20 * t5 / t22
  t31 = jnp.log(0.1e1 + 0.16081979498692535067e2 / (0.379785e1 * t14 + 0.8969 * t11 + 0.204775 * t17 + 0.123235 * t25))
  t33 = 0.621814e-1 * (0.1e1 + 0.53425e-1 * t11) * t31
  t34 = r0 - r1
  t35 = t34 ** 2
  t36 = t35 ** 2
  t37 = t7 ** 2
  t38 = t37 ** 2
  t42 = t34 / t7
  t43 = 0.1e1 + t42
  t44 = t43 <= p.zeta_threshold
  t45 = jnp.cbrt(p.zeta_threshold)
  t46 = t45 * p.zeta_threshold
  t47 = jnp.cbrt(t43)
  t49 = lax_cond(t44, t46, t47 * t43)
  t50 = 0.1e1 - t42
  t51 = t50 <= p.zeta_threshold
  t52 = jnp.cbrt(t50)
  t54 = lax_cond(t51, t46, t52 * t50)
  t56 = jnp.cbrt(2)
  t60 = (t49 + t54 - 0.2e1) / (0.2e1 * t56 - 0.2e1)
  t71 = jnp.log(0.1e1 + 0.32163958997385070134e2 / (0.705945e1 * t14 + 0.1549425e1 * t11 + 0.420775 * t17 + 0.1562925 * t25))
  t84 = jnp.log(0.1e1 + 0.29608749977793437516e2 / (0.51785e1 * t14 + 0.905775 * t11 + 0.1100325 * t17 + 0.1241775 * t25))
  t85 = (0.1e1 + 0.278125e-1 * t11) * t84
  t89 = t36 / t38 * t60 * (-0.310907e-1 * (0.1e1 + 0.5137e-1 * t11) * t71 + t33 - 0.19751673498613801407e-1 * t85)
  t91 = 0.19751673498613801407e-1 * t60 * t85
  t92 = jnp.log(0.2e1)
  t93 = 0.1e1 - t92
  t94 = jnp.pi ** 2
  t97 = t45 ** 2
  t98 = t47 ** 2
  t99 = lax_cond(t44, t97, t98)
  t100 = t52 ** 2
  t101 = lax_cond(t51, t97, t100)
  t103 = t99 / 0.2e1 + t101 / 0.2e1
  t104 = t103 ** 2
  t105 = t104 * t103
  t119 = (0.1e1 + 0.125 * t4 * t10 * (0.1e1 + 0.416675e-1 * t11)) / (0.1e1 + 0.125 * t4 * t10 * (0.1e1 + 0.740825e-1 * t11))
  t121 = s0 + 0.2e1 * s1 + s2
  t130 = jnp.sqrt(t121)
  t134 = t56 ** 2
  t139 = t130 / t8 / t7 * t134 / t103 / t14
  t141 = 0.45e1 + t139 / 0.4e1
  t144 = 0.45e1 + 0.36675 * t139
  t150 = 0.1e1 / t93
  t151 = t119 * t150
  t157 = jnp.exp(-(-t33 + t89 + t91) * t150 * t94 / t105)
  t160 = t94 / (t157 - 0.1e1)
  t161 = t121 ** 2
  t167 = t104 ** 2
  t173 = t141 ** 2
  t174 = t144 ** 2
  t181 = t121 / t8 / t37 * t56 / t104 * t19 / t3 * t5 * t141 / t144 / 0.96e2 + 0.21720231316129303386e-4 * t151 * t160 * t161 / t22 / t38 * t134 / t167 * t1 / t20 * t6 * t173 / t174
  t193 = jnp.log(0.1e1 + 0.6672455060314922e-1 * t119 * t181 * t150 * t94 / (0.1e1 + 0.6672455060314922e-1 * t151 * t160 * t181))
  res = -t33 + t89 + t91 + t93 / t94 * t105 * t193
  return res


def unpol(p, r, s=None, l=None, tau=None):
  params = p.params
  r0, s0, l0, tau0 = r, s, l, tau
  t1 = jnp.cbrt(3)
  t3 = jnp.cbrt(0.1e1 / jnp.pi)
  t4 = t1 * t3
  t5 = jnp.cbrt(4)
  t6 = t5 ** 2
  t7 = jnp.cbrt(r0)
  t9 = t6 / t7
  t10 = t4 * t9
  t13 = jnp.sqrt(t10)
  t16 = t10 ** 0.15e1
  t18 = t1 ** 2
  t19 = t3 ** 2
  t21 = t7 ** 2
  t24 = t18 * t19 * t5 / t21
  t30 = jnp.log(0.1e1 + 0.16081979498692535067e2 / (0.379785e1 * t13 + 0.8969 * t10 + 0.204775 * t16 + 0.123235 * t24))
  t32 = 0.621814e-1 * (0.1e1 + 0.53425e-1 * t10) * t30
  t33 = 0.1e1 <= p.zeta_threshold
  t34 = jnp.cbrt(p.zeta_threshold)
  t36 = lax_cond(t33, t34 * p.zeta_threshold, 1)
  t39 = jnp.cbrt(2)
  t54 = jnp.log(0.1e1 + 0.29608749977793437516e2 / (0.51785e1 * t13 + 0.905775 * t10 + 0.1100325 * t16 + 0.1241775 * t24))
  t57 = 0.19751673498613801407e-1 * (0.2e1 * t36 - 0.2e1) / (0.2e1 * t39 - 0.2e1) * (0.1e1 + 0.278125e-1 * t10) * t54
  t58 = jnp.log(0.2e1)
  t59 = 0.1e1 - t58
  t60 = jnp.pi ** 2
  t63 = t34 ** 2
  t64 = lax_cond(t33, t63, 1)
  t65 = t64 ** 2
  t66 = t65 * t64
  t80 = (0.1e1 + 0.125 * t4 * t9 * (0.1e1 + 0.416675e-1 * t10)) / (0.1e1 + 0.125 * t4 * t9 * (0.1e1 + 0.740825e-1 * t10))
  t81 = r0 ** 2
  t90 = jnp.sqrt(s0)
  t94 = t39 ** 2
  t99 = t90 / t7 / r0 * t94 / t64 / t13
  t101 = 0.45e1 + t99 / 0.4e1
  t104 = 0.45e1 + 0.36675 * t99
  t110 = 0.1e1 / t59
  t111 = t80 * t110
  t117 = jnp.exp(-(-t32 + t57) * t110 * t60 / t66)
  t120 = t60 / (t117 - 0.1e1)
  t121 = s0 ** 2
  t122 = t81 ** 2
  t128 = t65 ** 2
  t134 = t101 ** 2
  t135 = t104 ** 2
  t142 = s0 / t7 / t81 * t39 / t65 * t18 / t3 * t5 * t101 / t104 / 0.96e2 + 0.21720231316129303386e-4 * t111 * t120 * t121 / t21 / t122 * t94 / t128 * t1 / t19 * t6 * t134 / t135
  t154 = jnp.log(0.1e1 + 0.6672455060314922e-1 * t80 * t142 * t110 * t60 / (0.1e1 + 0.6672455060314922e-1 * t111 * t120 * t142))
  res = -t32 + t57 + t59 / t60 * t66 * t154
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