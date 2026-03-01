#!/usr/bin/env python3
"""
369 — Tesla number theory math aid and super calculator.
Single-file application: resonance, digital roots, triad checks, and extended arithmetic.
"""

from __future__ import annotations

import math
import sys
from decimal import Decimal, getcontext
from typing import List, Optional, Tuple, Callable, Any
from functools import reduce
import random

# -----------------------------------------------------------------------------
# CONSTANTS (Tesla triad)
# -----------------------------------------------------------------------------

TRIAD_A = 3
TRIAD_B = 6
TRIAD_C = 9
TRIAD_BASE = 369
TRIAD_SUM = TRIAD_A + TRIAD_B + TRIAD_C
TRIAD_PRODUCT = TRIAD_A * TRIAD_B * TRIAD_C
SCALE = 10**18
MAX_MAGNITUDE = 10**36
getcontext().prec = 80

# -----------------------------------------------------------------------------
# DIGIT & ROOT HELPERS
# -----------------------------------------------------------------------------


def digit_sum(n: int) -> int:
    """Sum of decimal digits of n."""
    n = abs(n)
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


def digital_root(n: int) -> int:
    """Digital root (repeated digit sum until single digit)."""
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r


def digit_sum_loop(n: int, max_iter: int = 100) -> int:
    """Repeated digit sum up to max_iter times."""
    for _ in range(max_iter):
        if n <= 9:
            return n
        n = digit_sum(n)
    return n


def digit_count(n: int) -> int:
    """Number of decimal digits."""
    if n == 0:
        return 1
    return len(str(abs(n)))


def digit_product(n: int) -> int:
    """Product of decimal digits (0 if any digit 0)."""
    if n == 0:
        return 0
    n = abs(n)
    p = 1
    while n:
        p *= n % 10
        n //= 10
    return p
