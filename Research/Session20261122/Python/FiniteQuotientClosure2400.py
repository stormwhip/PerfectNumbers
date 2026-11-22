#!/usr/bin/env python3
"""Finite-quotient cyclotomic certificates for three 10^2400 root shards.

All decisions use exact integers. A positive result means that every admissible
odd quotient Q in N=p^d*sigma(p^d)*Q has been rejected by a necessary condition.
This module is independent of solver PROVEN labels and external factor tables.
"""
from __future__ import annotations

from collections import Counter
from math import gcd, isqrt

BOUND = 10**2400
ROOT_ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
TARGETS = ((19, 936), (11, 1150), (11, 1152))
MAX_QUOTIENT = 2_000_000


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def spf_table(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for p in range(2, isqrt(limit) + 1):
        if spf[p] == p:
            for k in range(p * p, limit + 1, p):
                if spf[k] == k:
                    spf[k] = p
    return spf


def factor(n: int, spf: list[int]) -> list[tuple[int, int]]:
    result = []
    while n > 1:
        p = spf[n]
        v = 0
        while n % p == 0:
            n //= p
            v += 1
        result.append((p, v))
    return result


def sigma_from_factorization(items: list[tuple[int, int]]) -> int:
    value = 1
    for p, e in items:
        value *= (pow(p, e + 1) - 1) // (p - 1)
    return value


def odd_sigma(p: int, e: int) -> int:
    s = (pow(p, e + 1) - 1) // (p - 1)
    return s // (s & -s)


def finite_quotient_certificate(p: int, d: int, forbidden: tuple[int, ...],
                                bound: int = BOUND) -> dict:
    """Recompute a complete, finite certificate; raise on any open quotient."""
    if (p, d) not in TARGETS or bound != BOUND:
        raise ValueError("unapproved external root/size pin")
    expected_forbidden = set(ROOT_ORDER[:ROOT_ORDER.index(p)])
    if not expected_forbidden.issubset(set(forbidden)):
        raise ValueError("missing mandatory forbidden roots")
    m = d + 1
    if d % 2 or p >= m or m % 2 != 1 or not is_prime(m) or not is_prime(p):
        raise ValueError("cyclotomic prime-order precondition failed")
    sigma = (pow(p, m) - 1) // (p - 1)
    if sigma % 2 == 0:
        raise ValueError("expected odd cyclotomic sigma")
    A = sigma
    P = pow(p, d) * A
    R = bound // P
    if R < 1 or R > MAX_QUOTIENT or R >= pow(p, m):
        raise ValueError("quotient range cannot be exhaustively enumerated")

    # If q | Phi_m(p) for odd prime m>p, then ord_q(p)=m;
    # q=m is impossible since p!=1 (mod m). Every q is 1 (mod 2m).
    # Consequently the i-th distinct prime q_i of A is >= 2*i*m+1.
    # An upper bound t for omega(A) follows from (2m+1)^t <= A.
    t, v, base = 0, 1, 2 * m + 1
    while v <= A:
        v *= base
        t += 1
    t -= 1
    C = 1 + (t - 1).bit_length() if t else 0
    if C >= 2 * m:
        raise ValueError("harmonic abundance denominator not positive")
    # sigma(A)/A < 2m/(2m-C):
    # product_i(1+1/(2mi)) <= 1/(1-H_t/(2m)),
    # and H_t <= 1+ceil(log_2(t)) = C.

    spf = spf_table(R)
    counts = Counter()
    survivors = []
    forbidden_set = set(forbidden)
    val_A_cache = {}

    def valuation_in_A(q: int) -> int:
        if q not in val_A_cache:
            z, k = A, 0
            while z % q == 0:
                z //= q
                k += 1
            val_A_cache[q] = k
        return val_A_cache[q]

    for Q in range(1, R + 1, 2):
        factors = factor(Q, spf)
        sigma_Q = sigma_from_factorization(factors)

        # Submultiplicativity: sigma(xy)/(xy) <= f(x)*f(y).
        # f(p^d)<p/(p-1) and f(A)<2m/(2m-C).
        if p * sigma_Q * (2 * m) < 2 * (p - 1) * Q * (2 * m - C):
            counts["UNDER_ABUNDANCE"] += 1
            continue

        if any(q in forbidden_set for q, _ in factors):
            counts["FORBIDDEN_FACTOR"] += 1
            continue

        # For a non-exact d=m-1 option, m | (e+1).
        # Since e=d+v_p(Q), any positive v_p(Q) is at least m;
        # Q<p^m rules this out.
        if any(q == p for q, _ in factors):
            counts["ROOT_EXPONENT"] += 1
            continue

        # Euler: one prime has exponent 1 (mod 4) and is 1 (mod 4);
        # all other prime exponents are even. Root p here is 3 (mod 4).
        specials = 0
        invalid_euler = False
        for q, e in factors:
            total_e = e + valuation_in_A(q)
            if total_e % 2:
                if q % 4 != 1 or total_e % 4 != 1:
                    invalid_euler = True
                    break
                specials += 1
        if invalid_euler or specials > 1:
            counts["EULER_EXPONENT"] += 1
            continue

        # For q not dividing A or p, q^e is an exact component of N.
        # Thus odd(sigma(q^e)) | N = P*Q.
        candidate_N = P * Q
        if any(valuation_in_A(q) == 0 and
               candidate_N % odd_sigma(q, e) != 0 for q, e in factors):
            counts["SIGMA_FORCING"] += 1
            continue

        # gcd(A,Q)=1 gives exact multiplicativity in p^d, A, Q.
        # f(A)>1 (A>1). If f(p^d) f(Q)>2, N is overabundant.
        if gcd(A, Q) == 1 and sigma * sigma_Q > 2 * pow(p, d) * Q:
            counts["OVER_ABUNDANCE"] += 1
            continue

        survivors.append(Q)

    if survivors:
        raise ValueError(f"unresolved quotients for ({p},{d}): {survivors[:12]}")
    if sum(counts.values()) != (R + 1) // 2:
        raise ValueError("quotient enumeration coverage mismatch")
    return {
        "root": p, "exponent": d, "quotient_max": R,
        "quotients_checked": (R + 1) // 2,
        "omega_A_upper": t, "harmonic_C": C,
        "rejection_counts": dict(counts), "unresolved": 0,
    }


def main() -> None:
    import json
    result = [finite_quotient_certificate(
        p, d, tuple(ROOT_ORDER[:ROOT_ORDER.index(p)])) for p, d in TARGETS]
    expected = {
        (19, 936): (1411815, 705908),
        (11, 1150): (56941, 28471),
        (11, 1152): (3, 2),
    }
    for r in result:
        if (r["quotient_max"], r["quotients_checked"]) != expected[
                (r["root"], r["exponent"])]:
            raise RuntimeError("finite quotient census changed unexpectedly")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
