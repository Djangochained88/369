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


def reverse_digits(n: int) -> int:
    """Reverse decimal representation."""
    n = abs(n)
    r = 0
    while n:
        r = r * 10 + n % 10
        n //= 10
    return r


def is_palindrome(n: int) -> bool:
    return n == reverse_digits(n)


def alternating_digit_sum(n: int) -> int:
    """Alternating sum of digits (d0 - d1 + d2 - ...)."""
    s = 0
    sign = 1
    n = abs(n)
    while n:
        s += sign * (n % 10)
        sign = -sign
        n //= 10
    return s


# -----------------------------------------------------------------------------
# TRIAD & RESONANCE (Tesla number theory)
# -----------------------------------------------------------------------------


def is_triad_resonant(n: int) -> bool:
    """True if digital root is 3, 6, or 9."""
    dr = digital_root(n)
    return dr in (TRIAD_A, TRIAD_B, TRIAD_C)


def triad_sum() -> int:
    return TRIAD_SUM


def triad_product() -> int:
    return TRIAD_PRODUCT


def mod_369(n: int) -> int:
    return n % TRIAD_BASE


def divisible_by_369(n: int) -> bool:
    return n % TRIAD_BASE == 0


def vortex_reduction(n: int) -> int:
    """Reduce to single digit by repeated digit sum."""
    while n >= TRIAD_BASE:
        n = digit_sum(n)
    return n


def vortex_to_triad(n: int) -> int:
    """Map vortex-reduced value to triad 3, 6, 9 or remainder."""
    n = vortex_reduction(n)
    if n in (TRIAD_A, TRIAD_B, TRIAD_C):
        return n
    if n % TRIAD_C == 0:
        return TRIAD_C
    return n % TRIAD_A


def phase_in_cycle(ts: float) -> int:
    """Phase within 3+6+9 cycle."""
    return int(ts) % TRIAD_SUM


def resonance_score(n: int) -> int:
    """Combined score from digital root, mod 369, digit sum."""
    dr = digital_root(n)
    m = mod_369(n)
    ds = digit_sum(n)
    return dr * TRIAD_BASE + m + ds


def triad_quotient(n: int) -> int:
    return n // TRIAD_SUM


def triad_remainder(n: int) -> int:
    return n % TRIAD_SUM


def is_divisible_by_triad_sum(n: int) -> bool:
    return n % TRIAD_SUM == 0


def flux_encode(n: int) -> int:
    """Encode as digital_root * 369 + (n % 369)."""
    return digital_root(n) * TRIAD_BASE + mod_369(n)


def flux_decode(encoded: int) -> Tuple[int, int]:
    dr = encoded // TRIAD_BASE
    mod_val = encoded % TRIAD_BASE
    return (dr, mod_val)


def magnitude_class(n: int) -> int:
    """Rough magnitude class by digit count."""
    dc = digit_count(n)
    if dc <= 1:
        return 0
    if dc <= 3:
        return 1
    if dc <= 6:
        return 2
    if dc <= 9:
        return 3
    return 4


def triad_class(n: int) -> int:
    """1=root 3, 2=root 6, 3=root 9, 0=other."""
    dr = digital_root(n)
    if dr == TRIAD_A:
        return 1
    if dr == TRIAD_B:
        return 2
    if dr == TRIAD_C:
        return 3
    return 0


# -----------------------------------------------------------------------------
# INTEGER ARITHMETIC (number theory)
# -----------------------------------------------------------------------------


def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def mod_inverse(a: int, m: int) -> int:
    """Modular inverse of a mod m (m must be prime or gcd(a,m)=1)."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m


def pow_mod(base: int, exp: int, mod: int) -> int:
    if mod == 0:
        raise ZeroDivisionError("mod must be non-zero")
    base = base % mod
    result = 1
    while exp:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial not defined for negative")
    if n > 200:
        raise ValueError("n too large for integer factorial")
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    r = 1
    for i in range(k):
        r = r * (n - i) // (i + 1)
    return r


def triangular(n: int) -> int:
    return n * (n + 1) // 2 if n >= 0 else 0


def is_triangular(t: int) -> bool:
    if t < 0:
        return False
    if t == 0:
        return True
    n = int((math.sqrt(8 * t + 1) - 1) / 2)
    return n * (n + 1) // 2 == t


def fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    if n <= 2:
        return 1
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def collatz_step(n: int) -> int:
    if n <= 0:
        raise ValueError("Positive integer required")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def collatz_length(n: int, max_steps: int = 1000) -> int:
    length = 0
    while n != 1 and length < max_steps:
        n = collatz_step(n)
        length += 1
    return length


def harmonic_mean(a: float, b: float) -> float:
    if a == 0 and b == 0:
        return 0.0
    if a + b == 0:
        raise ValueError("Harmonic mean undefined")
    return 2 * a * b / (a + b)


def geometric_mean(a: float, b: float) -> float:
    if a < 0 or b < 0:
        raise ValueError("Geometric mean requires non-negative")
    return math.sqrt(a * b)


def arithmetic_mean(a: float, b: float) -> float:
    return (a + b) / 2


def quadratic_mean(a: float, b: float) -> float:
    return math.sqrt((a * a + b * b) / 2)


def sigma_sum(n: int, k: int = 1) -> int:
    """Sum of integers from k to n inclusive."""
    if k > n:
        return 0
    return (n - k + 1) * (n + k) // 2


def sigma_sum_squares(n: int) -> int:
    return n * (n + 1) * (2 * n + 1) // 6


def sigma_sum_cubes(n: int) -> int:
    s = n * (n + 1) // 2
    return s * s


def sqrt_floor(n: int) -> int:
    if n < 0:
        raise ValueError("Square root of negative")
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    if n == 0:
        return True
    r = sqrt_floor(n)
    return r * r == n


# -----------------------------------------------------------------------------
# SUPER CALCULATOR — SCALAR OPERATIONS
# -----------------------------------------------------------------------------


def calc_add(*args: float) -> float:
    return sum(args)


