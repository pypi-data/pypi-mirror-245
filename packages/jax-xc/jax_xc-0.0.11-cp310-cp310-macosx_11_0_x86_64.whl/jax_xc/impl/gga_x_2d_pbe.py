"""Generated from gga_x_2d_pbe.mpl."""

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
  t2 = jnp.sqrt(jnp.pi)
  t3 = 0.1e1 / t2
  t4 = r0 + r1
  t5 = 0.1e1 / t4
  t8 = 0.2e1 * r0 * t5 <= p.zeta_threshold
  t9 = p.zeta_threshold - 0.1e1
  t12 = 0.2e1 * r1 * t5 <= p.zeta_threshold
  t13 = -t9
  t15 = (r0 - r1) * t5
  t16 = lax_cond(t12, t13, t15)
  t17 = lax_cond(t8, t9, t16)
  t18 = 0.1e1 + t17
  t20 = jnp.sqrt(p.zeta_threshold)
  t21 = t20 * p.zeta_threshold
  t22 = jnp.sqrt(t18)
  t24 = lax_cond(t18 <= p.zeta_threshold, t21, t22 * t18)
  t26 = jnp.sqrt(0.2e1)
  t27 = jnp.sqrt(t4)
  t28 = t26 * t27
  t29 = 0.1e1 / jnp.pi
  t31 = r0 ** 2
  t43 = lax_cond(r0 <= p.dens_threshold, 0, -0.2e1 / 0.3e1 * t3 * t24 * t28 * (0.14604e1 - 0.21196816 / (0.4604 + 0.221591796875e-1 * t29 * s0 / t31 / r0)))
  t45 = lax_cond(t8, t13, -t15)
  t46 = lax_cond(t12, t9, t45)
  t47 = 0.1e1 + t46
  t49 = jnp.sqrt(t47)
  t51 = lax_cond(t47 <= p.zeta_threshold, t21, t49 * t47)
  t54 = r1 ** 2
  t66 = lax_cond(r1 <= p.dens_threshold, 0, -0.2e1 / 0.3e1 * t3 * t51 * t28 * (0.14604e1 - 0.21196816 / (0.4604 + 0.221591796875e-1 * t29 * s2 / t54 / r1)))
  res = t43 + t66
  return res


def unpol(p, r, s=None, l=None, tau=None):
  params = p.params
  r0, s0, l0, tau0 = r, s, l, tau
  t3 = jnp.sqrt(jnp.pi)
  t5 = 0.1e1 <= p.zeta_threshold
  t6 = p.zeta_threshold - 0.1e1
  t8 = lax_cond(t5, -t6, 0)
  t9 = lax_cond(t5, t6, t8)
  t10 = 0.1e1 + t9
  t12 = jnp.sqrt(p.zeta_threshold)
  t14 = jnp.sqrt(t10)
  t16 = lax_cond(t10 <= p.zeta_threshold, t12 * p.zeta_threshold, t14 * t10)
  t18 = jnp.sqrt(0.2e1)
  t19 = jnp.sqrt(r0)
  t23 = r0 ** 2
  t35 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, -0.2e1 / 0.3e1 / t3 * t16 * t18 * t19 * (0.14604e1 - 0.21196816 / (0.4604 + 0.44318359375e-1 / jnp.pi * s0 / t23 / r0)))
  res = 0.2e1 * t35
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