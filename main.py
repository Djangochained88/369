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


def calc_sub(a: float, b: float) -> float:
    return a - b


def calc_mul(*args: float) -> float:
    return reduce(lambda x, y: x * y, args, 1.0)


def calc_div(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b


def calc_pow(a: float, b: float) -> float:
    if a == 0 and b < 0:
        raise ValueError("0 to negative power undefined")
    return a ** b


def calc_sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("Square root of negative")
    return math.sqrt(x)


def calc_log(x: float, base: float = math.e) -> float:
    if x <= 0:
        raise ValueError("Log of non-positive")
    if base <= 0 or base == 1:
        raise ValueError("Invalid log base")
    return math.log(x, base)


def calc_log10(x: float) -> float:
    return math.log10(x) if x > 0 else float("nan")


def calc_exp(x: float) -> float:
    return math.exp(x)


def calc_sin(x: float) -> float:
    return math.sin(x)


def calc_cos(x: float) -> float:
    return math.cos(x)


def calc_tan(x: float) -> float:
    return math.tan(x)


def calc_degrees(rad: float) -> float:
    return math.degrees(rad)


def calc_radians(deg: float) -> float:
    return math.radians(deg)


def calc_floor(x: float) -> int:
    return math.floor(x)


def calc_ceil(x: float) -> int:
    return math.ceil(x)


def calc_abs(x: float) -> float:
    return abs(x)


def calc_mod(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Modulo by zero")
    return a % b


def calc_percent(part: float, whole: float) -> float:
    if whole == 0:
        raise ZeroDivisionError("Percent of zero whole")
    return 100.0 * part / whole


def calc_percent_change(old_val: float, new_val: float) -> float:
    if old_val == 0:
        return float("inf") if new_val != 0 else 0.0
    return 100.0 * (new_val - old_val) / old_val


def calc_compound(principal: float, rate: float, periods: int) -> float:
    return principal * (1 + rate) ** periods


def calc_npr(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    return factorial(n) // factorial(n - r)


def calc_ncr(n: int, r: int) -> int:
    return binomial(n, r)


# -----------------------------------------------------------------------------
# SUPER CALCULATOR — ARRAY OPERATIONS
# -----------------------------------------------------------------------------


def calc_sum(arr: List[float]) -> float:
    return sum(arr)


def calc_product(arr: List[float]) -> float:
    return reduce(lambda a, b: a * b, arr, 1.0)


def calc_mean(arr: List[float]) -> float:
    if not arr:
        raise ValueError("Empty array")
    return sum(arr) / len(arr)


def calc_median(arr: List[float]) -> float:
    if not arr:
        raise ValueError("Empty array")
    s = sorted(arr)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def calc_variance(arr: List[float], sample: bool = False) -> float:
    if len(arr) < 2:
        return 0.0
    m = calc_mean(arr)
    n = len(arr)
    var = sum((x - m) ** 2 for x in arr) / (n - 1 if sample else n)
    return var


def calc_stdev(arr: List[float], sample: bool = False) -> float:
    return math.sqrt(calc_variance(arr, sample))


def calc_min(arr: List[float]) -> float:
    if not arr:
        raise ValueError("Empty array")
    return min(arr)


def calc_max(arr: List[float]) -> float:
    if not arr:
        raise ValueError("Empty array")
    return max(arr)


def calc_range(arr: List[float]) -> Tuple[float, float]:
    if not arr:
        raise ValueError("Empty array")
    return (min(arr), max(arr))


def calc_dot(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Length mismatch")
    return sum(x * y for x, y in zip(a, b))


def calc_cumsum(arr: List[float]) -> List[float]:
    out = []
    s = 0.0
    for x in arr:
        s += x
        out.append(s)
    return out


def calc_cumprod(arr: List[float]) -> List[float]:
    out = []
    p = 1.0
    for x in arr:
        p *= x
        out.append(p)
    return out


# -----------------------------------------------------------------------------
# BATCH TRIAD HELPERS
# -----------------------------------------------------------------------------


def batch_digital_roots(values: List[int]) -> List[int]:
    return [digital_root(v) for v in values]


def batch_triad_resonant(values: List[int]) -> List[bool]:
    return [is_triad_resonant(v) for v in values]


def batch_mod_369(values: List[int]) -> List[int]:
    return [v % TRIAD_BASE for v in values]


def batch_digit_sums(values: List[int]) -> List[int]:
    return [digit_sum(v) for v in values]


def count_triad_resonant(values: List[int]) -> int:
    return sum(1 for v in values if is_triad_resonant(v))


def any_triad_resonant(values: List[int]) -> bool:
    return any(is_triad_resonant(v) for v in values)


def all_triad_resonant(values: List[int]) -> bool:
    return len(values) > 0 and all(is_triad_resonant(v) for v in values)


# -----------------------------------------------------------------------------
# PARSER & EVAL (safe expression)
# -----------------------------------------------------------------------------

_SAFE_NAMES: dict = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "round": round,
    "pow": pow,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "factorial": factorial,
    "gcd": gcd,
    "lcm": lcm,
    "digital_root": digital_root,
    "digit_sum": digit_sum,
    "triad_sum": triad_sum,
    "triad_product": triad_product,
    "mod_369": mod_369,
    "is_triad_resonant": is_triad_resonant,
    "triangular": triangular,
    "fibonacci": fibonacci,
    "binomial": binomial,
}


def safe_eval(expr: str) -> Any:
    """Evaluate expression with allowed names only."""
    return eval(expr, {"__builtins__": {}}, _SAFE_NAMES)


# -----------------------------------------------------------------------------
# CLI MENU
# -----------------------------------------------------------------------------


def menu_triad_info() -> None:
    n = int(input("Enter integer: ").strip() or "0")
    print(f"  digit_sum      = {digit_sum(n)}")
    print(f"  digital_root   = {digital_root(n)}")
    print(f"  mod_369        = {mod_369(n)}")
    print(f"  is_triad_resonant = {is_triad_resonant(n)}")
    print(f"  vortex_to_triad   = {vortex_to_triad(n)}")
    print(f"  resonance_score   = {resonance_score(n)}")
    print(f"  triad_class       = {triad_class(n)}")


def menu_super_calc() -> None:
    print("Enter expression (e.g. 2+3*4, sqrt(16), factorial(5)). Type 'q' to quit.")
    while True:
        try:
            line = input("369> ").strip()
            if not line or line.lower() == "q":
                break
            result = safe_eval(line)
            print(f"  => {result}")
        except Exception as e:
            print(f"  Error: {e}")


def menu_batch_triad() -> None:
    line = input("Enter integers separated by spaces: ").strip()
    try:
        values = [int(x) for x in line.split()]
    except ValueError:
        print("Invalid integers")
        return
    print("  digital_roots:", batch_digital_roots(values))
    print("  triad_resonant:", batch_triad_resonant(values))
    print("  mod_369:", batch_mod_369(values))
    print("  count_triad_resonant:", count_triad_resonant(values))


def menu_number_theory() -> None:
    print("1. gcd(a,b)  2. lcm(a,b)  3. factorial(n)  4. binomial(n,k)")
    print("5. triangular(n)  6. fibonacci(n)  7. collatz_length(n)")
    choice = input("Choice (1-7): ").strip()
    try:
        if choice == "1":
            a, b = map(int, input("a b: ").split())
            print("gcd =", gcd(a, b))
        elif choice == "2":
            a, b = map(int, input("a b: ").split())
            print("lcm =", lcm(a, b))
        elif choice == "3":
            n = int(input("n: "))
            print("factorial =", factorial(n))
        elif choice == "4":
            n, k = map(int, input("n k: ").split())
            print("binomial =", binomial(n, k))
        elif choice == "5":
            n = int(input("n: "))
            print("triangular =", triangular(n))
        elif choice == "6":
            n = int(input("n: "))
            print("fibonacci =", fibonacci(n))
        elif choice == "7":
            n = int(input("n: "))
            print("collatz_length =", collatz_length(n))
        else:
            print("Unknown choice")
    except Exception as e:
        print("Error:", e)


def menu_stats() -> None:
    line = input("Enter numbers separated by spaces: ").strip()
    try:
        arr = [float(x) for x in line.split()]
    except ValueError:
        print("Invalid numbers")
        return
    if not arr:
        print("Empty list")
        return
    print("  sum     =", calc_sum(arr))
    print("  mean    =", calc_mean(arr))
    print("  median  =", calc_median(arr))
    print("  min     =", calc_min(arr))
    print("  max     =", calc_max(arr))
    print("  stdev   =", calc_stdev(arr))
    print("  variance=", calc_variance(arr))


def menu_expression() -> None:
    print("Allowed: + - * / // % **, sqrt, sin, cos, tan, log, log10, exp, factorial, gcd, lcm,")
    print("  digital_root, digit_sum, mod_369, triangular, fibonacci, binomial, pi, e")
    expr = input("Expression: ").strip()
    try:
        result = safe_eval(expr)
        print("Result:", result)
    except Exception as e:
        print("Error:", e)


def main_menu() -> None:
    while True:
        print()
        print("=== 369 — Tesla number theory & super calculator ===")
        print("1. Triad info (digit sum, digital root, resonance)")
        print("2. Super calc (expression eval)")
        print("3. Batch triad (list of integers)")
        print("4. Number theory (gcd, lcm, factorial, etc.)")
        print("5. Stats (mean, median, stdev of list)")
        print("6. Single expression eval")
        print("0. Quit")
        choice = input("Choice: ").strip()
        if choice == "0":
            break
        if choice == "1":
            menu_triad_info()
        elif choice == "2":
            menu_super_calc()
        elif choice == "3":
            menu_batch_triad()
        elif choice == "4":
            menu_number_theory()
        elif choice == "5":
