"""Generated from gga_k_lgap.mpl."""

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
  t3 = t2 ** 2
  t4 = jnp.cbrt(jnp.pi)
  t6 = t3 * t4 * jnp.pi
  t7 = r0 + r1
  t8 = 0.1e1 / t7
  t11 = 0.2e1 * r0 * t8 <= p.zeta_threshold
  t12 = p.zeta_threshold - 0.1e1
  t15 = 0.2e1 * r1 * t8 <= p.zeta_threshold
  t16 = -t12
  t18 = (r0 - r1) * t8
  t19 = lax_cond(t15, t16, t18)
  t20 = lax_cond(t11, t12, t19)
  t21 = 0.1e1 + t20
  t23 = jnp.cbrt(p.zeta_threshold)
  t24 = t23 ** 2
  t25 = t24 * p.zeta_threshold
  t26 = jnp.cbrt(t21)
  t27 = t26 ** 2
  t29 = lax_cond(t21 <= p.zeta_threshold, t25, t27 * t21)
  t30 = jnp.cbrt(t7)
  t31 = t30 ** 2
  t34 = jnp.cbrt(6)
  t35 = t34 ** 2
  t36 = params.mu[0] * t35
  t37 = jnp.pi ** 2
  t38 = jnp.cbrt(t37)
  t39 = 0.1e1 / t38
  t40 = jnp.sqrt(s0)
  t42 = jnp.cbrt(r0)
  t49 = params.mu[1] * t34
  t50 = t38 ** 2
  t51 = 0.1e1 / t50
  t53 = r0 ** 2
  t54 = t42 ** 2
  t62 = params.mu[2] / t37
  t64 = t53 ** 2
  t70 = jnp.exp(-t36 * t39 * t40 / t42 / r0 / 0.12e2 - t49 * t51 * s0 / t54 / t53 / 0.24e2 - t62 * t40 * s0 / t64 / 0.48e2)
  t77 = lax_cond(r0 <= p.dens_threshold, 0, 0.3e1 / 0.2e2 * t6 * t29 * t31 * (0.1e1 + params.kappa * (0.1e1 - t70)))
  t79 = lax_cond(t11, t16, -t18)
  t80 = lax_cond(t15, t12, t79)
  t81 = 0.1e1 + t80
  t83 = jnp.cbrt(t81)
  t84 = t83 ** 2
  t86 = lax_cond(t81 <= p.zeta_threshold, t25, t84 * t81)
  t88 = jnp.sqrt(s2)
  t90 = jnp.cbrt(r1)
  t97 = r1 ** 2
  t98 = t90 ** 2
  t105 = t97 ** 2
  t111 = jnp.exp(-t36 * t39 * t88 / t90 / r1 / 0.12e2 - t49 * t51 * s2 / t98 / t97 / 0.24e2 - t62 * t88 * s2 / t105 / 0.48e2)
  t118 = lax_cond(r1 <= p.dens_threshold, 0, 0.3e1 / 0.2e2 * t6 * t86 * t31 * (0.1e1 + params.kappa * (0.1e1 - t111)))
  res = t77 + t118
  return res


def unpol(p, r, s=None, l=None, tau=None):
  params = p.params
  r0, s0, l0, tau0 = r, s, l, tau
  t3 = jnp.cbrt(3)
  t4 = t3 ** 2
  t5 = jnp.cbrt(jnp.pi)
  t8 = 0.1e1 <= p.zeta_threshold
  t9 = p.zeta_threshold - 0.1e1
  t11 = lax_cond(t8, -t9, 0)
  t12 = lax_cond(t8, t9, t11)
  t13 = 0.1e1 + t12
  t15 = jnp.cbrt(p.zeta_threshold)
  t16 = t15 ** 2
  t18 = jnp.cbrt(t13)
  t19 = t18 ** 2
  t21 = lax_cond(t13 <= p.zeta_threshold, t16 * p.zeta_threshold, t19 * t13)
  t22 = jnp.cbrt(r0)
  t23 = t22 ** 2
  t26 = jnp.cbrt(6)
  t27 = t26 ** 2
  t29 = jnp.pi ** 2
  t30 = jnp.cbrt(t29)
  t33 = jnp.sqrt(s0)
  t34 = jnp.cbrt(2)
  t43 = t30 ** 2
  t46 = t34 ** 2
  t48 = r0 ** 2
  t58 = t48 ** 2
  t64 = jnp.exp(-params.mu[0] * t27 / t30 * t33 * t34 / t22 / r0 / 0.12e2 - params.mu[1] * t26 / t43 * s0 * t46 / t23 / t48 / 0.24e2 - params.mu[2] / t29 * t33 * s0 / t58 / 0.24e2)
  t71 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, 0.3e1 / 0.2e2 * t4 * t5 * jnp.pi * t21 * t23 * (0.1e1 + params.kappa * (0.1e1 - t64)))
  res = 0.2e1 * t71
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