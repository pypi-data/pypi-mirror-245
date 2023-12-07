"""Generated from gga_x_kt.mpl."""

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
  t32 = jnp.cbrt(0.1e1 / jnp.pi)
  t34 = jnp.cbrt(4)
  t36 = params.gamma * t29 / t32 * t34
  t37 = jnp.cbrt(2)
  t38 = t37 ** 2
  t39 = t20 * t6
  t40 = jnp.cbrt(t39)
  t42 = t38 * t40 * t39
  t43 = r0 ** 2
  t44 = jnp.cbrt(r0)
  t45 = t44 ** 2
  t60 = lax_cond(r0 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t26 * t27 * (0.1e1 - t36 * t42 * s0 / t45 / t43 / (t42 / 0.4e1 + params.delta) / 0.18e2))
  t62 = lax_cond(t10, t15, -t17)
  t63 = lax_cond(t14, t11, t62)
  t64 = 0.1e1 + t63
  t66 = jnp.cbrt(t64)
  t68 = lax_cond(t64 <= p.zeta_threshold, t23, t66 * t64)
  t70 = t64 * t6
  t71 = jnp.cbrt(t70)
  t73 = t38 * t71 * t70
  t74 = r1 ** 2
  t75 = jnp.cbrt(r1)
  t76 = t75 ** 2
  t91 = lax_cond(r1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t5 * t68 * t27 * (0.1e1 - t36 * t73 * s2 / t76 / t74 / (t73 / 0.4e1 + params.delta) / 0.18e2))
  res = t60 + t91
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
  t24 = jnp.cbrt(0.1e1 / jnp.pi)
  t26 = jnp.cbrt(4)
  t29 = jnp.cbrt(2)
  t30 = t12 * r0
  t31 = jnp.cbrt(t30)
  t32 = t31 * t30
  t34 = r0 ** 2
  t35 = t19 ** 2
  t39 = t29 ** 2
  t52 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, -0.3e1 / 0.8e1 * t3 / t4 * t18 * t19 * (0.1e1 - params.gamma * t21 / t24 * t26 * t29 * t32 * s0 / t35 / t34 / (t39 * t32 / 0.4e1 + params.delta) / 0.9e1))
  res = 0.2e1 * t52
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