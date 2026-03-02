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
            menu_stats()
        elif choice == "6":
            menu_expression()
        else:
            print("Unknown option")


# -----------------------------------------------------------------------------
# DEMO / TESTS (run when executed)
# -----------------------------------------------------------------------------


def demo_triad() -> None:
    print("Demo: triad constants", triad_sum(), triad_product())
    for v in [9, 18, 369, 12345]:
        print(f"  {v}: digital_root={digital_root(v)}, is_triad_resonant={is_triad_resonant(v)}")


def demo_calculator() -> None:
    print("Demo: 2+3*4 =", safe_eval("2+3*4"))
    print("Demo: sqrt(16) =", safe_eval("sqrt(16)"))
    print("Demo: factorial(5) =", safe_eval("factorial(5)"))
    print("Demo: digital_root(12345) =", digital_root(12345))


def run_demos() -> None:
    demo_triad()
    demo_calculator()


# -----------------------------------------------------------------------------
# POLYGONAL NUMBERS & SERIES
# -----------------------------------------------------------------------------


def pentagonal(n: int) -> int:
    return n * (3 * n - 1) // 2 if n >= 0 else 0


def hexagonal(n: int) -> int:
    return n * (2 * n - 1) if n >= 0 else 0


def heptagonal(n: int) -> int:
    return n * (5 * n - 3) // 2 if n >= 0 else 0


def octagonal(n: int) -> int:
    return n * (3 * n - 2) if n >= 0 else 0


def polygonal(sides: int, n: int) -> int:
    if sides < 3 or n < 0:
        return 0
    return (n * ((sides - 2) * n - (sides - 4))) // 2


def catalan(n: int) -> int:
    if n > 15:
        raise ValueError("n too large for Catalan")
    return binomial(2 * n, n) // (n + 1)


def euler_partition_table(n: int) -> List[int]:
    """First n+1 partition numbers (0..n)."""
    if n > 25:
        n = 25
    p = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, 792, 1002, 1255, 1575, 1958]
    return p[: n + 1]


def euler_partition(n: int) -> int:
    return euler_partition_table(n)[-1] if n <= 25 else 0


# -----------------------------------------------------------------------------
# ENCODING / HASH-STYLE HELPERS
# -----------------------------------------------------------------------------


def triad_checksum(values: List[int]) -> int:
    h = 0
    for i, v in enumerate(values):
        h = (h * 31 + v + i) % TRIAD_BASE
    return h


def magnitude_checksum(n: int) -> int:
    return (digit_sum(n) + digital_root(n) + (n % TRIAD_BASE)) % (10**18)


def encode_triad_pair(a: int, b: int) -> int:
    if a >= TRIAD_BASE or b >= TRIAD_BASE:
        raise ValueError("Values must be < 369")
    return a * TRIAD_BASE + b


def decode_triad_pair(encoded: int) -> Tuple[int, int]:
    return (encoded // TRIAD_BASE, encoded % TRIAD_BASE)


def encode_triad_triple(a: int, b: int, c: int) -> int:
    if a >= TRIAD_BASE or b >= TRIAD_BASE or c >= TRIAD_BASE:
        raise ValueError("Values must be < 369")
    return a * TRIAD_BASE * TRIAD_BASE + b * TRIAD_BASE + c


def decode_triad_triple(encoded: int) -> Tuple[int, int, int]:
    a = encoded // (TRIAD_BASE * TRIAD_BASE)
    b = (encoded // TRIAD_BASE) % TRIAD_BASE
    c = encoded % TRIAD_BASE
    return (a, b, c)


def magnitude_phase_encode(mag: int, phase: int, scale: int = 10**18) -> int:
    if phase >= scale:
        raise ValueError("Phase must be < scale")
    return mag * scale + phase


def magnitude_phase_decode(encoded: int, scale: int = 10**18) -> Tuple[int, int]:
    return (encoded // scale, encoded % scale)


# -----------------------------------------------------------------------------
# ADDITIONAL MEANS & SCALAR OPS
# -----------------------------------------------------------------------------


def harmonic_triad(a: float, b: float, c: float) -> float:
    if a == 0 or b == 0 or c == 0:
        return 0.0
    return 3.0 / (1.0 / a + 1.0 / b + 1.0 / c)


def geometric_triad(a: float, b: float, c: float) -> float:
    if a < 0 or b < 0 or c < 0:
        raise ValueError("Non-negative required")
    return (a * b * c) ** (1.0 / 3.0)


def arithmetic_triad(a: float, b: float, c: float) -> float:
    return (a + b + c) / 3.0


def weighted_average(values: List[float], weights: List[float]) -> float:
    if len(values) != len(weights) or not values:
        raise ValueError("Length mismatch or empty")
    s = sum(w * v for v, w in zip(values, weights))
    w_sum = sum(weights)
    if w_sum == 0:
        raise ValueError("Weights sum to zero")
    return s / w_sum


def percentile(arr: List[float], pct: float) -> float:
    if not arr or pct < 0 or pct > 100:
        raise ValueError("Invalid input")
    s = sorted(arr)
    idx = int(len(s) * pct / 100)
    if idx >= len(s):
        idx = len(s) - 1
    return s[idx]


def linear_interpolate(x0: float, y0: float, x1: float, y1: float, x: float) -> float:
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


# -----------------------------------------------------------------------------
# BIT & INTEGER HELPERS
# -----------------------------------------------------------------------------


def bit_count(n: int) -> int:
    n = abs(n)
    c = 0
    while n:
        c += n & 1
        n >>= 1
    return c


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def next_power_of_two(n: int) -> int:
    if n <= 0:
        return 1
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n |= n >> 32
    return n + 1


def log2_floor(n: int) -> int:
    if n <= 0:
        raise ValueError("Positive required")
    r = 0
    while n > 1:
        n >>= 1
        r += 1
    return r


# -----------------------------------------------------------------------------
# TKINTER CALCULATOR GUI (optional)
# -----------------------------------------------------------------------------

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    _TK_AVAILABLE = True
except ImportError:
    _TK_AVAILABLE = False


def _gui_eval(expr: str) -> str:
    try:
        result = safe_eval(expr)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def launch_gui_calculator() -> None:
    if not _TK_AVAILABLE:
        print("tkinter not available; run without GUI.")
        return

    root = tk.Tk()
    root.title("369 Super Calculator")
    root.geometry("520x420")
    root.resizable(True, True)

    main = ttk.Frame(root, padding=10)
    main.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    expr_var = tk.StringVar()
    ttk.Label(main, text="Expression (e.g. 2+3*4, sqrt(16), digital_root(12345)):").grid(row=0, column=0, columnspan=2, sticky="w")
    entry = ttk.Entry(main, textvariable=expr_var, width=60)
    entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))
    main.columnconfigure(0, weight=1)

    out_text = scrolledtext.ScrolledText(main, height=12, width=70, state="disabled")
    out_text.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 8))
    main.rowconfigure(2, weight=1)

    def do_eval() -> None:
        expr = expr_var.get().strip()
        if not expr:
            return
        result = _gui_eval(expr)
        out_text.config(state="normal")
        out_text.insert(tk.END, f"{expr}\n  => {result}\n")
        out_text.see(tk.END)
        out_text.config(state="disabled")

    def do_clear() -> None:
        out_text.config(state="normal")
        out_text.delete(1.0, tk.END)
        out_text.config(state="disabled")

    ttk.Button(main, text="Evaluate", command=do_eval).grid(row=3, column=0, sticky="w", padx=(0, 4))
    ttk.Button(main, text="Clear", command=do_clear).grid(row=3, column=1, sticky="w")

    entry.bind("<Return>", lambda e: do_eval())
    entry.focus()
    root.mainloop()


# -----------------------------------------------------------------------------
# EXTRA MENU: POLYGONAL & PARTITIONS
# -----------------------------------------------------------------------------


def menu_polygonal() -> None:
    print("Polygonal: triangular(3), pentagonal(4), hexagonal(5), polygonal(sides,n)")
    n = int(input("n: ").strip() or "0")
    print("  triangular(n) =", triangular(n))
    print("  pentagonal(n) =", pentagonal(n))
    print("  hexagonal(n)  =", hexagonal(n))
    print("  heptagonal(n) =", heptagonal(n))
    print("  octagonal(n)  =", octagonal(n))
    s = int(input("sides (for polygonal): ").strip() or "3")
    print("  polygonal(sides,n) =", polygonal(s, n))


def menu_partition() -> None:
    n = int(input("n (0..25): ").strip() or "0")
    if n < 0 or n > 25:
        n = min(25, max(0, n))
    print("  euler_partition(n) =", euler_partition(n))


def menu_encoding() -> None:
    print("1. encode_triad_pair(a,b)  2. decode_triad_pair(enc)")
    print("3. encode_triad_triple(a,b,c)  4. decode_triad_triple(enc)")
    c = input("Choice: ").strip()
    try:
        if c == "1":
            a, b = map(int, input("a b (0..368): ").split())
            print(encode_triad_pair(a, b))
        elif c == "2":
            enc = int(input("encoded: "))
            print(decode_triad_pair(enc))
        elif c == "3":
            a, b, c = map(int, input("a b c (0..368): ").split())
            print(encode_triad_triple(a, b, c))
        elif c == "4":
            enc = int(input("encoded: "))
            print(decode_triad_triple(enc))
        else:
            print("Unknown")
    except Exception as e:
        print("Error:", e)


# -----------------------------------------------------------------------------
# FILE HELPERS (read/write numbers)
# -----------------------------------------------------------------------------


def read_numbers_from_file(path: str) -> List[float]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for part in line.split():
                try:
                    out.append(float(part))
                except ValueError:
                    pass
    return out


def write_numbers_to_file(path: str, values: List[float]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for v in values:
            f.write(str(v) + "\n")


def menu_file_stats() -> None:
    path = input("File path (numbers, one per line or space-sep): ").strip()
    if not path:
        return
    try:
        arr = read_numbers_from_file(path)
        if not arr:
            print("No numbers found")
            return
        print("  count =", len(arr))
        print("  sum   =", calc_sum(arr))
        print("  mean  =", calc_mean(arr))
        print("  median=", calc_median(arr))
        print("  stdev =", calc_stdev(arr))
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("Error:", e)


# -----------------------------------------------------------------------------
# RANDOM TRIAD DEMO
# -----------------------------------------------------------------------------


def random_triad_demo(count: int = 20) -> None:
    print(f"Random {count} integers: digital_root, mod_369, is_triad_resonant")
    for _ in range(count):
        n = random.randint(1, 10**9)
        print(f"  {n} -> dr={digital_root(n)} mod369={mod_369(n)} resonant={is_triad_resonant(n)}")


# -----------------------------------------------------------------------------
# EXPANDED MAIN MENU
# -----------------------------------------------------------------------------


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
        print("7. Polygonal numbers")
        print("8. Partition number (Euler)")
        print("9. Encode/decode triad pair/triple")
        print("10. File stats (read numbers from file)")
        print("11. Random triad demo")
        if _TK_AVAILABLE:
            print("12. Open GUI calculator")
        print("13. Resonance (sum/product/ratio)")
        print("14. Round to triad")
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
            menu_stats()
        elif choice == "6":
            menu_expression()
        elif choice == "7":
            menu_polygonal()
        elif choice == "8":
            menu_partition()
        elif choice == "9":
            menu_encoding()
        elif choice == "10":
            menu_file_stats()
        elif choice == "11":
            random_triad_demo()
        elif choice == "12" and _TK_AVAILABLE:
            launch_gui_calculator()
        elif choice == "13":
            menu_resonance()
        elif choice == "14":
            menu_round_triad()
        else:
            print("Unknown option")


# -----------------------------------------------------------------------------
# TRIAD SERIES GENERATORS
# -----------------------------------------------------------------------------


def triad_resonant_up_to(limit: int) -> List[int]:
    """List of triad-resonant numbers in [1..limit] (digital root 3,6,9)."""
    return [n for n in range(1, limit + 1) if is_triad_resonant(n)]


def digital_root_sequence(start: int, length: int) -> List[int]:
    """First `length` values of repeated digital root applied to start, start+1, ..."""
    return [digital_root(start + i) for i in range(length)]


def mod_369_sequence(length: int, start: int = 0) -> List[int]:
    return [(start + i) % TRIAD_BASE for i in range(length)]


def vortex_sequence(n: int, steps: int = 20) -> List[int]:
    out = [n]
    for _ in range(steps - 1):
        if n < TRIAD_BASE:
            break
        n = digit_sum(n)
        out.append(n)
    return out


def flux_encoded_sequence(length: int, seed: int = 1) -> List[int]:
    return [flux_encode(seed + i) for i in range(length)]


# -----------------------------------------------------------------------------
# VALIDATION & FORMATTING
# -----------------------------------------------------------------------------


def validate_triad_pair(a: int, b: int) -> bool:
    return 0 <= a < TRIAD_BASE and 0 <= b < TRIAD_BASE


def validate_triad_triple(a: int, b: int, c: int) -> bool:
    return (
        0 <= a < TRIAD_BASE
        and 0 <= b < TRIAD_BASE
        and 0 <= c < TRIAD_BASE
    )


def format_triad_info(n: int) -> str:
    return (
        f"n={n} digit_sum={digit_sum(n)} digital_root={digital_root(n)} "
        f"mod369={mod_369(n)} resonant={is_triad_resonant(n)}"
    )


def format_magnitude_phase(mag: int, phase: int) -> str:
    return f"magnitude={mag} phase={phase} encoded={magnitude_phase_encode(mag, phase)}"


# -----------------------------------------------------------------------------
# ADDITIONAL CALCULATOR OPERATIONS
# -----------------------------------------------------------------------------


def calc_inv(x: float) -> float:
    if x == 0:
        raise ZeroDivisionError("Inverse of zero")
    return 1.0 / x


def calc_square(x: float) -> float:
    return x * x


def calc_cube(x: float) -> float:
    return x * x * x


def calc_cbrt(x: float) -> float:
    return x ** (1.0 / 3.0) if x >= 0 else -((-x) ** (1.0 / 3.0))


def calc_asin(x: float) -> float:
    if x < -1 or x > 1:
        raise ValueError("Domain [-1,1] for asin")
    return math.asin(x)


def calc_acos(x: float) -> float:
    if x < -1 or x > 1:
        raise ValueError("Domain [-1,1] for acos")
    return math.acos(x)


def calc_atan(x: float) -> float:
    return math.atan(x)


def calc_atan2(y: float, x: float) -> float:
    return math.atan2(y, x)


def calc_sinh(x: float) -> float:
    return math.sinh(x)


def calc_cosh(x: float) -> float:
    return math.cosh(x)


def calc_tanh(x: float) -> float:
    return math.tanh(x)


def calc_degrees_to_radians(deg: float) -> float:
    return math.radians(deg)


def calc_radians_to_degrees(rad: float) -> float:
    return math.degrees(rad)


def calc_sign(x: float) -> float:
    if x > 0:
        return 1.0
    if x < 0:
        return -1.0
    return 0.0


def calc_trunc(x: float) -> int:
    return int(math.trunc(x))


def calc_round(x: float, ndigits: int = 0) -> float:
    return round(x, ndigits)


# -----------------------------------------------------------------------------
# ARRAY EXTENSIONS
# -----------------------------------------------------------------------------


def calc_diff(arr: List[float]) -> List[float]:
    """Consecutive differences arr[i+1]-arr[i]."""
    if len(arr) < 2:
        return []
    return [arr[i + 1] - arr[i] for i in range(len(arr) - 1)]


def calc_running_sum(arr: List[float]) -> List[float]:
    return calc_cumsum(arr)


def calc_running_max(arr: List[float]) -> List[float]:
    out = []
    m = float("-inf")
    for x in arr:
        if x > m:
            m = x
        out.append(m)
    return out


def calc_running_min(arr: List[float]) -> List[float]:
    out = []
    m = float("inf")
    for x in arr:
        if x < m:
            m = x
        out.append(m)
    return out


def calc_normalize(arr: List[float]) -> List[float]:
    """Normalize to [0,1] by (x - min) / (max - min)."""
    if not arr:
        return []
    lo, hi = min(arr), max(arr)
    if hi == lo:
        return [0.5] * len(arr)
    return [(x - lo) / (hi - lo) for x in arr]


def calc_standardize(arr: List[float]) -> List[float]:
    """Z-score: (x - mean) / stdev."""
    if len(arr) < 2:
        return [0.0] * len(arr)
    m = calc_mean(arr)
    s = calc_stdev(arr)
    if s == 0:
        return [0.0] * len(arr)
    return [(x - m) / s for x in arr]


def slice_sum(arr: List[float], start: int, length: int) -> float:
    if start < 0 or length <= 0 or start + length > len(arr):
        raise ValueError("Invalid slice")
    return sum(arr[start : start + length])


def slice_mean(arr: List[float], start: int, length: int) -> float:
    return slice_sum(arr, start, length) / length


# -----------------------------------------------------------------------------
# BATCH INTEGER HELPERS
# -----------------------------------------------------------------------------


def batch_gcd(values: List[int]) -> int:
    if not values:
        return 0
    g = abs(values[0])
    for v in values[1:]:
        g = gcd(g, abs(v))
    return g


def batch_lcm(values: List[int]) -> int:
    if not values:
        return 0
    l = abs(values[0])
    for v in values[1:]:
        l = lcm(l, abs(v))
    return l


def batch_factorial(ns: List[int]) -> List[int]:
    return [factorial(n) for n in ns]


def batch_triangular(ns: List[int]) -> List[int]:
    return [triangular(n) for n in ns]


def batch_fibonacci(ns: List[int]) -> List[int]:
    return [fibonacci(n) for n in ns]


def sum_mod_369(values: List[int]) -> int:
    s = 0
    for v in values:
        s = (s + (v % TRIAD_BASE)) % TRIAD_BASE
    return s


def product_mod_369(values: List[int]) -> int:
    if not values:
        return 0
    p = 1
    for v in values:
        p = (p * (v % TRIAD_BASE)) % TRIAD_BASE
    return p


# -----------------------------------------------------------------------------
# SAFE EVAL EXTENDED NAMESPACE
# -----------------------------------------------------------------------------

_SAFE_NAMES["harmonic_mean"] = harmonic_mean
_SAFE_NAMES["geometric_mean"] = geometric_mean
_SAFE_NAMES["triangular"] = triangular
_SAFE_NAMES["pentagonal"] = pentagonal
_SAFE_NAMES["hexagonal"] = hexagonal
_SAFE_NAMES["catalan"] = catalan
_SAFE_NAMES["euler_partition"] = euler_partition
_SAFE_NAMES["sqrt_floor"] = sqrt_floor
_SAFE_NAMES["is_perfect_square"] = is_perfect_square
_SAFE_NAMES["sigma_sum"] = sigma_sum
_SAFE_NAMES["sigma_sum_squares"] = sigma_sum_squares
_SAFE_NAMES["sigma_sum_cubes"] = sigma_sum_cubes


# -----------------------------------------------------------------------------
# EXTENDED DEMO
# -----------------------------------------------------------------------------


def demo_polygonal() -> None:
    print("Polygonal numbers n=1..5:")
    for n in range(1, 6):
        print(f"  n={n} tri={triangular(n)} pent={pentagonal(n)} hex={hexagonal(n)}")


def demo_partition() -> None:
    print("Euler partition p(0)..p(10):", [euler_partition(n) for n in range(11)])


def demo_encoding() -> None:
    a, b = 3, 6
    enc = encode_triad_pair(a, b)
    print(f"encode_triad_pair(3,6)={enc} decode={decode_triad_pair(enc)}")
    enc3 = encode_triad_triple(3, 6, 9)
    print(f"encode_triad_triple(3,6,9)={enc3} decode={decode_triad_triple(enc3)}")


def demo_means() -> None:
    x, y = 4.0, 9.0
    print(f"harmonic_mean(4,9)={harmonic_mean(x, y)}")
    print(f"geometric_mean(4,9)={geometric_mean(x, y)}")
    print(f"arithmetic_mean(4,9)={arithmetic_mean(x, y)}")


def run_demos() -> None:
    demo_triad()
    demo_calculator()
    demo_polygonal()
    demo_partition()
    demo_encoding()
    demo_means()


# -----------------------------------------------------------------------------
# RESONANCE & FLUX HELPERS
# -----------------------------------------------------------------------------


def resonance_product(a: int, b: int) -> int:
    return (a * b) % TRIAD_BASE


def resonance_sum(a: int, b: int) -> int:
    return (a % TRIAD_BASE + b % TRIAD_BASE) % TRIAD_BASE


def triad_weighted_sum(a: int, b: int, c: int) -> int:
    return a * TRIAD_A + b * TRIAD_B + c * TRIAD_C


def round_to_triad(n: int) -> int:
    return (n // TRIAD_SUM) * TRIAD_SUM

