#!/usr/bin/env python3
"""Exact integer DP certificate: Euler prime exponents constrained by forbidden sigma factors.

For q<2m+1, q does not divide Phi_m(p); its exponent in N is exactly
its exponent in Q. Forbidden root factors of sigma(q^e) impose a provable
minimum allowed exponent. The DP minimizes the product for each k distinct
small primes, with at most one Euler-special odd exponent.
"""
from __future__ import annotations
from functools import lru_cache
from bisect import bisect_right
from CyclotomicPrimorialClosure2400 import is_prime, odd_primes_below, BOUND

@lru_cache(maxsize=10000)
def min_exponents(q: int, forbidden: tuple[int, ...]) -> tuple[int, int | None]:
    def bad(e: int) -> bool:
        for f in forbidden:
            if q % f == 1:
                if (e+1) % f == 0:
                    return True
            elif pow(q, e+1, f) == 1:
                return True
        return False
    # The finite scan never assumes an untested exponent is impossible.
    # If no valid e<=200 exists, the next even exponent is >=202.
    regular = next((e for e in range(2, 201, 2) if not bad(e)), 202)
    # Similarly, the next Euler exponent after 201 is at least 205.
    special = (next((e for e in range(1, 202, 4) if not bad(e)), 205)
               if q % 4 == 1 else None)
    return regular, special

@lru_cache(maxsize=64)
def weighted_cyclotomic_certificate(
    p: int, d: int, forbidden: tuple[int, ...], bound: int = BOUND,
) -> dict | None:
    """Recompute a strict upper bound on sigma(N)/N for all small-prime counts."""
    if bound != BOUND or p < 3 or not is_prime(p) or d < 2 or d % 2:
        return None
    m = d+1
    if m <= p or not is_prime(m):
        return None
    A = (pow(p, m)-1)//(p-1)
    P = pow(p, d)*A
    if P > bound:
        return None
    R = bound//P
    L = 2*m+1
    rem = A
    t = 0
    while rem >= L:
        rem //= L
        t += 1
    C = 1+(t-1).bit_length() if t else 0
    if C >= 2*m:
        return None

    # Sharper, exact rational cyclotomic abundance envelope:
    # sigma(A)/A < product_{i=1}^t (2*m*i+1)/(2*m*i).
    a_num, a_den = 1, 1
    for i in range(1, t+1):
        a_num *= 2*m*i+1
        a_den *= 2*m*i

    small = [q for q in odd_primes_below(L) if q != p and q not in forbidden]
    # Universal unweighted Euler-size bound limits the number of
    # distinct small primes that any Q<=R could contain.
    K, product = 0, 1
    for q in small:
        next_product = product*q
        if next_product*next_product//q > R:
            break
        product = next_product
        K += 1
    cap = R+1
    regular_dp = [cap]*(K+1)
    special_dp = [cap]*(K+1)
    regular_dp[0] = 1
    factor_num = [1]
    factor_den = [1]
    for q in small[:K]:
        factor_num.append(factor_num[-1]*q)
        factor_den.append(factor_den[-1]*(q-1))

    # The DP holds only exact integer lower bounds for the small part of Q.
    for q in small:
        e_regular, e_special = min_exponents(q, tuple(sorted(forbidden)))
        w_regular = pow(q, e_regular)
        w_special = pow(q, e_special) if e_special is not None else None
        for k in range(K-1, -1, -1):
            special_dp[k+1] = min(
                cap,
                special_dp[k+1],
                special_dp[k]*w_regular,
                regular_dp[k]*w_special if w_special is not None else cap,
            )
            regular_dp[k+1] = min(
                cap, regular_dp[k+1], regular_dp[k]*w_regular
            )

    # Any v distinct large primes are >= the first v actual primes >=L.
    # Their least product and greatest abundance both follow this
    # deterministic increasing-prime list.
    large_product = [1]
    large_ab_num = [1]
    large_ab_den = [1]
    for q in odd_primes_below(20000):
        if q < L:
            continue
        large_product.append(large_product[-1]*q)
        large_ab_num.append(large_ab_num[-1]*q)
        large_ab_den.append(large_ab_den[-1]*(q-1))
        if large_product[-1] > R:
            break
    if large_product[-1] <= R:
        return None  # Insufficient sieve coverage; never assert a false proof.

    examined, maximum_num, maximum_den = 0, 0, 1
    for k in range(K+1):
        min_cost = min(regular_dp[k], special_dp[k])
        if min_cost > R:
            continue
        remaining = R//min_cost
        large_count = bisect_right(large_product, remaining)-1
        num = p*a_num*factor_num[k]*large_ab_num[large_count]
        den = (p-1)*a_den*factor_den[k]*large_ab_den[large_count]
        examined += 1
        if num*maximum_den > maximum_num*den:
            maximum_num, maximum_den = num, den
        if num >= 2*den:
            return None
    return {"root": p, "exponent": d, "k_cases_checked": examined,
            "max_abundance_num": maximum_num,
            "max_abundance_den": maximum_den}
