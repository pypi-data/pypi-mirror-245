"""Generated from gga_x_herman.mpl."""

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
  t29 = t2 ** 2
  t31 = jnp.cbrt(0.1e1 / jnp.pi)
  t33 = t29 / t31
  t34 = jnp.cbrt(4)
  t36 = r0 ** 2
  t37 = jnp.cbrt(r0)
  t38 = t37 ** 2
  t48 = lax_cond(r0 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t26 * t27 * (0.1e1 + 0.66666666666666666668e-3 * t33 * t34 * s0 / t38 / t36))
  t50 = lax_cond(t10, t15, -t17)
  t51 = lax_cond(t14, t11, t50)
  t52 = 0.1e1 + t51
  t54 = jnp.cbrt(t52)
  t56 = lax_cond(t52 <= p.zeta_threshold, t23, t54 * t52)
  t59 = r1 ** 2
  t60 = jnp.cbrt(r1)
  t61 = t60 ** 2
  t71 = lax_cond(r1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t56 * t27 * (0.1e1 + 0.66666666666666666668e-3 * t33 * t34 * s2 / t61 / t59))
  res = t48 + t71
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
  t21 = t3 ** 2
  t23 = jnp.cbrt(0.1e1 / jnp.pi)
  t26 = jnp.cbrt(4)
  t28 = jnp.cbrt(2)
  t29 = t28 ** 2
  t31 = r0 ** 2
  t32 = t19 ** 2
  t42 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t3 / t4 * t18 * t19 * (0.1e1 + 0.66666666666666666668e-3 * t21 / t23 * t26 * s0 * t29 / t32 / t31))
  res = 0.2e1 * t42
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