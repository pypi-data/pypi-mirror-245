"""Generated from gga_x_optx.mpl."""

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
  t20 = 0.1e1 + t19
  t22 = jnp.cbrt(p.zeta_threshold)
  t23 = t22 * p.zeta_threshold
  t24 = jnp.cbrt(t20)
  t26 = lax_cond(t20 <= p.zeta_threshold, t23, t24 * t20)
  t27 = jnp.cbrt(t6)
  t29 = params.gamma ** 2
  t30 = params.b * t29
  t31 = s0 ** 2
  t32 = r0 ** 2
  t33 = t32 ** 2
  t35 = jnp.cbrt(r0)
  t40 = t35 ** 2
  t45 = (0.1e1 + params.gamma * s0 / t40 / t32) ** 2
  t53 = lax_cond(r0 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t26 * t27 * (params.a + t30 * t31 / t35 / t33 / r0 / t45))
  t55 = lax_cond(t10, t15, -t17)
  t56 = lax_cond(t14, t11, t55)
  t57 = 0.1e1 + t56
  t59 = jnp.cbrt(t57)
  t61 = lax_cond(t57 <= p.zeta_threshold, t23, t59 * t57)
  t63 = s2 ** 2
  t64 = r1 ** 2
  t65 = t64 ** 2
  t67 = jnp.cbrt(r1)
  t72 = t67 ** 2
  t77 = (0.1e1 + params.gamma * s2 / t72 / t64) ** 2
  t85 = lax_cond(r1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t61 * t27 * (params.a + t30 * t63 / t67 / t65 / r1 / t77))
  res = t53 + t85
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
  t12 = 0.1e1 + t11
  t14 = jnp.cbrt(p.zeta_threshold)
  t16 = jnp.cbrt(t12)
  t18 = lax_cond(t12 <= p.zeta_threshold, t14 * p.zeta_threshold, t16 * t12)
  t19 = jnp.cbrt(r0)
  t21 = params.gamma ** 2
  t23 = s0 ** 2
  t25 = jnp.cbrt(2)
  t26 = r0 ** 2
  t27 = t26 ** 2
  t33 = t25 ** 2
  t34 = t19 ** 2
  t40 = (0.1e1 + params.gamma * s0 * t33 / t34 / t26) ** 2
  t49 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t3 / t4 * t18 * t19 * (params.a + 0.2e1 * params.b * t21 * t23 * t25 / t19 / t27 / r0 / t40))
  res = 0.2e1 * t49
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