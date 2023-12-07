"""Generated from lda_x_sloc.mpl."""

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
  t1 = params.b + 0.1e1
  t5 = r0 + r1
  t6 = t5 ** params.b
  t9 = (r0 - r1) / t5
  t10 = 0.1e1 + t9
  t12 = p.zeta_threshold ** t1
  t13 = t10 ** t1
  t14 = lax_cond(t10 <= p.zeta_threshold, t12, t13)
  t15 = 0.1e1 - t9
  t17 = t15 ** t1
  t18 = lax_cond(t15 <= p.zeta_threshold, t12, t17)
  res = -params.a / t1 * t6 * (t14 + t18) / 0.2e1
  return res


def unpol(p, r, s=None, l=None, tau=None):
  params = p.params
  r0, s0, l0, tau0 = r, s, l, tau
  t1 = params.b + 0.1e1
  t5 = r0 ** params.b
  t7 = p.zeta_threshold ** t1
  t8 = lax_cond(0.1e1 <= p.zeta_threshold, t7, 1)
  res = -params.a / t1 * t5 * t8
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