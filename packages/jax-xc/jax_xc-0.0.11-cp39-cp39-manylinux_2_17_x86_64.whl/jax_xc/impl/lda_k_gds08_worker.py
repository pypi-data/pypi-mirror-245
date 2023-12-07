"""Generated from lda_k_gds08_worker.mpl."""

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
  t3 = r0 + r1
  t4 = 0.1e1 / t3
  t5 = (r0 - r1) * t4
  t7 = 0.1e1 + t5 <= p.zeta_threshold
  t8 = p.zeta_threshold - 0.1e1
  t10 = 0.1e1 - t5 <= p.zeta_threshold
  t11 = -t8
  t12 = lax_cond(t10, t11, t5)
  t13 = lax_cond(t7, t8, t12)
  t17 = 0.2e1 * r0 * t4 <= p.zeta_threshold
  t20 = 0.2e1 * r1 * t4 <= p.zeta_threshold
  t21 = lax_cond(t20, t11, t5)
  t22 = lax_cond(t17, t8, t21)
  t25 = jnp.log((0.1e1 + t22) * t3)
  t27 = t25 ** 2
  t32 = lax_cond(r0 <= p.dens_threshold, 0, (0.1e1 + t13) * (params.B * t25 + params.C * t27 + params.A) / 0.2e1)
  t34 = lax_cond(t7, t11, -t5)
  t35 = lax_cond(t10, t8, t34)
  t37 = lax_cond(t17, t11, -t5)
  t38 = lax_cond(t20, t8, t37)
  t41 = jnp.log((0.1e1 + t38) * t3)
  t43 = t41 ** 2
  t48 = lax_cond(r1 <= p.dens_threshold, 0, (0.1e1 + t35) * (params.B * t41 + params.C * t43 + params.A) / 0.2e1)
  res = t32 + t48
  return res


def unpol(p, r, s=None, l=None, tau=None):
  params = p.params
  r0, s0, l0, tau0 = r, s, l, tau
  t3 = 0.1e1 <= p.zeta_threshold
  t4 = p.zeta_threshold - 0.1e1
  t6 = lax_cond(t3, -t4, 0)
  t7 = lax_cond(t3, t4, t6)
  t8 = 0.1e1 + t7
  t10 = jnp.log(t8 * r0)
  t12 = t10 ** 2
  t17 = lax_cond(r0 / 0.2e1 <= p.dens_threshold, 0, t8 * (params.B * t10 + params.C * t12 + params.A) / 0.2e1)
  res = 0.2e1 * t17
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