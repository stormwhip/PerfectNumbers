#!/usr/bin/env python3
"""Exact cyclotomic/Euler primorial certificate for a canonical root shard.

All proof comparisons are integer-only. Return None when inconclusive.
"""
from __future__ import annotations
from functools import lru_cache
from math import isqrt

BOUND = 10**2400

def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))

@lru_cache(maxsize=32)
def odd_primes_below(limit: int) -> tuple[int, ...]:
    sieve = bytearray(b"\x01") * limit
    sieve[:2] = b"\x00\x00"
    for i in range(2, isqrt(limit - 1) + 1):
        if sieve[i]:
            sieve[i*i:limit:i] = b"\x00" * ((limit - 1 - i*i)//i + 1)
    return tuple(p for p in range(3, limit, 2) if sieve[p])

@lru_cache(maxsize=4096)
def cyclotomic_primorial_certificate(
    p: int, d: int, forbidden: tuple[int, ...], bound: int = BOUND,
) -> dict | None:
    """Strict rational bound, with all parameters externally pinned."""
    if bound != BOUND or p < 3 or p % 2 == 0 or d < 2 or d % 2:
        return None
    m = d + 1
    if m <= p or not is_prime(m) or not is_prime(p):
        return None
    a = (pow(p, m) - 1) // (p - 1)
    if a % 2 == 0:
        return None
    forced = pow(p, d) * a
    if forced > bound:
        return None
    r = bound // forced
    L = 2*m + 1

    # Every q|Phi_m(p) satisfies q=1 (mod 2m), since m>p.
    # Thus omega(a)<=floor(log_L(a)).
    t = 0
    z = a
    while z >= L:
        z //= L
        t += 1
    C = 1 + (t - 1).bit_length() if t else 0
    if C >= 2*m:
        return None

    small = [q for q in odd_primes_below(L)
             if q != p and q not in forbidden]
    product = 1
    sigma_num = 1
    sigma_den = 1
    count = 0
    checked = 0
    max_n, max_d = 0, 1

    # For k distinct q<L outside p, all but one have exponent>=2.
    # Therefore Q >=(r_1*...*r_k)^2/r_k.
    # The remaining size budget bounds large distinct prime factors.
    for q in (1, *small):
        if q != 1:
            next_product = product * q
            minimum = next_product * next_product // q
            if minimum > r:
                break
            product = next_product
            sigma_num *= q
            sigma_den *= q - 1
            count += 1
        else:
            minimum = 1
        remaining = r // minimum
        large_count = 0
        while remaining >= L:
            remaining //= L
            large_count += 1
        numerator = p * (2*m) * sigma_num * pow(L, large_count)
        denominator = (p-1) * (2*m-C) * sigma_den * pow(L-1, large_count)
        checked += 1
        if numerator * max_d > max_n * denominator:
            max_n, max_d = numerator, denominator
        if numerator >= 2 * denominator:
            return None

    return {"root": p, "exponent": d, "quotient_digits": len(str(r)),
            "omega_bound": t, "harmonic_C": C, "k_cases_checked": checked,
            "max_small_distinct_primes": count,
            "max_abundance_num": max_n, "max_abundance_den": max_d}
