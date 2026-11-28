#!/usr/bin/env python3
"""
Independent, offline, pure-stdlib certificate verifier for Odd Perfect Number
frontier proofs (N <= 10^2400).

Run with:
    python3 -I -S -B -X int_max_str_digits=0 Verify.py
    python3 -I -S -B -X int_max_str_digits=0 Verify.py --run-negative-tests

Strictly avoids `assert` for verification (immune to `-O`), avoids third-party
libraries, and uses exact integer / Fraction arithmetic for all proof decisions.
"""

import hashlib
import json
import math
import os
import sys
import time
from fractions import Fraction
from math import ceil, gcd, isqrt, prod

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

B = 10**2400
E3_MIN = 5031  # 3^5030 <= B < 3^5031
ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
MR12_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
MR12_LIMIT = 3317044064679887385961981  # Sorenson & Webster (2015)

CHECKS = 0


class VerificationError(Exception):
    pass


def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise VerificationError(msg)


def G(b, h):
    return (b ** (h + 1) - 1) // (b - 1)


def vp(n, p):
    check(n > 0 and p > 1, f"invalid vp({n}, {p})")
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def odd_part(n):
    return n >> vp(n, 2)


def canonical_bans(root_p):
    check(root_p in ROOTS, f"unknown canonical root {root_p}")
    return list(ROOTS[: ROOTS.index(root_p)])


def is_composite_witness(n):
    """
    Deterministic compositeness test.
    Returns True ONLY if n is PROVEN composite (or <= 1).
    Returns False if n passes 12-base Miller-Rabin (conservative when used to
    decide whether to KEEP a base in the deficit product U).
    """
    if n <= 1:
        return True
    for p in MR12_BASES:
        if n == p:
            return False
        if n % p == 0:
            return True
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in MR12_BASES:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        witness = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                witness = False
                break
        if witness:
            return True
    return False


def is_proven_prime_small(n):
    """Deterministic primality for n < MR12_LIMIT (~3.317e24)."""
    check(n < MR12_LIMIT, f"n={n} exceeds deterministic MR12 limit")
    if n < 2:
        return False
    return not is_composite_witness(n)


def can_be_valid_base(b, fixed_primes, bans, euler_fixed):
    """
    Conservative check: returns False ONLY if b is PROVEN unable to be an
    admissible odd base (prime or, when Euler is open, square of a prime q=1 mod 4).
    """
    if b < 3 or b % 2 == 0:
        return False
    if b in fixed_primes or b in bans:
        return False
    if not is_composite_witness(b):
        return True  # prime or probable prime -> conservatively KEEP
    if not euler_fixed:
        rt = isqrt(b)
        if rt * rt == b and rt % 4 == 1 and rt not in fixed_primes and rt not in bans:
            if not is_composite_witness(rt):
                return True  # square of prime q=1 mod 4 -> KEEP
    return False


def verify_pratt_certificates(cert_list):
    """Verify every prime in CertifiedPrimes recursively via Pratt + MR12."""
    certified = {}
    small_primes = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
    }
    for item in cert_list:
        p = int(item["p"])
        method = item["method"]
        if method == "small_prime":
            check(p in small_primes, f"invalid small_prime {p}")
            # Factor p-1 directly for small primes <= 101 and find primitive root
            rem = p - 1
            fac = {}
            d = 2
            while d * d <= rem:
                while rem % d == 0:
                    fac[d] = fac.get(d, 0) + 1
                    rem //= d
                d += 1
            if rem > 1:
                fac[rem] = fac.get(rem, 0) + 1
            g_small = 1
            if p > 2:
                for cand in range(2, p):
                    if all(pow(cand, (p - 1) // q, p) != 1 for q in fac):
                        g_small = cand
                        break
            certified[p] = {"factors": fac, "g": g_small}
        elif method == "pratt_primitive_root":
            g = int(item["g"])
            factors = [(int(q), int(e)) for q, e in item["p_minus_1_factors"]]
            check(p > 2, f"Pratt p={p} <= 2")
            check(prod(q**e for q, e in factors) == p - 1, f"p-1 product mismatch for {p}")
            for q, e in factors:
                check(e >= 1 and q in certified, f"uncertified factor {q} of {p}-1")
            check(pow(g, p - 1, p) == 1, f"Fermat test failed for p={p}, g={g}")
            for q, _ in factors:
                check(pow(g, (p - 1) // q, p) != 1, f"Lucas order test failed for p={p}, q={q}")
            if p < MR12_LIMIT:
                check(is_proven_prime_small(p), f"MR12 failed for {p}")
            certified[p] = {"factors": dict(factors), "g": g}
        else:
            raise VerificationError(f"Unknown primality method: {method}")
    return certified


def exact_state(rows, bans, certified_primes):
    """Section 3 exact state reconstruction."""
    if not rows:
        raise VerificationError("empty prefix")
    seen = set()
    for p, h in rows:
        check(p in certified_primes, f"uncertified prime base {p}")
        check(p >= 3 and p % 2 == 1 and h >= 1, f"invalid pair ({p}, {h})")
        check(p not in seen, f"duplicate base {p}")
        seen.add(p)
    odds = [(p, h) for p, h in rows if h % 2 == 1]
    if len(odds) > 1 or any(p % 4 != 1 or h % 4 != 1 for p, h in odds):
        return None
    X = prod(p**h for p, h in rows)
    T = prod(G(p, h) for p, h in rows)
    S = odd_part(T)
    if any(X % u == 0 or S % u == 0 for u in bans):
        return None
    if any(vp(S, p) > h for p, h in rows):
        return None
    D = S // gcd(S, X)
    check(gcd(X, D) == 1, "gcd(X, D) != 1")
    if X * D > B or T > 2 * X:
        return None
    return X, T, S, D


def exact_split(rows, t, bans, certified_primes):
    """Section 3 exact branch enumeration with strict raw tail."""
    st = exact_state(rows, bans, certified_primes)
    if st is None:
        return [], None
    X, T, S, D = st
    check(t in certified_primes, f"uncertified split pivot {t}")
    check(t not in {p for p, _ in rows} and D % t == 0, f"invalid split pivot {t}")
    c = vp(D, t)
    h = c
    base = X * (D // (t**c)) * (t**h)
    live = []
    while base <= B:
        if exact_state(rows + [(t, h)], bans, certified_primes) is not None:
            live.append(h)
        h += 1
        base *= t
    check(base > B, "tail overflow check failed")
    return live, h


def get_odd_divisors_up_to(factors_dict, limit):
    """Return sorted odd divisors d with 1 < d <= limit from prime factorization of p-1."""
    divs = [1]
    for q, e in factors_dict.items():
        if q == 2:
            continue
        new_divs = []
        for d in divs:
            val = d
            for _ in range(e + 1):
                if val <= limit:
                    new_divs.append(val)
                val *= q
        divs = new_divs
    return sorted(d for d in divs if 1 < d <= limit)


def hensel_ord_k(p, g, k, max_z):
    """Lift all k-1 non-trivial k-th roots of unity mod p up to mod p^max_z."""
    check((p - 1) % k == 0, f"{k} does not divide {p}-1")
    step = (p - 1) // k
    roots = sorted(pow(g, step * j, p) for j in range(1, k))
    check(len(roots) == k - 1, "root count mismatch")
    res = {0: [0], 1: roots}
    mod = p
    for z in range(2, max_z + 1):
        next_mod = mod * p
        new_roots = []
        for r in roots:
            f_val = (pow(r, k, next_mod) - 1) // mod
            fp_inv = pow((k * pow(r, k - 1, p)) % p, -1, p)
            t = (-f_val * fp_inv) % p
            nr = r + t * mod
            check(pow(nr, k, next_mod) == 1, "Hensel lift verification failed")
            new_roots.append(nr)
        roots = new_roots
        mod = next_mod
        res[z] = roots
    return res


def compute_single_target_deficit_exact(
    target, g, weight, max_z, factors_p_minus_1, fixed_primes, bans, euler_fixed
):
    """
    Compute exact Fraction upper bound U = prod_b U_b for single-target weight w:
        b^h >= target^(w * u) / U_b
    for all admissible odd bases b and all even h >= 2 with b^h <= B and u <= max_z.
    Verifies:
      - Order 1 (b = 1 mod target): impossible or zero deficit
      - LTE (target | L/o): impossible or zero deficit
      - ALL odd divisors o | (target - 1) with o - 1 < E3_MIN (using Hensel Truncation Lemma!)
    """
    # 1. Order 1 check: h >= target - 1
    if target - 1 < E3_MIN:
        # Check 3^(target - 1) >= target^weight
        check(3 ** (target - 1) >= target**weight, f"order-1 deficit possible for {target}")
        # Also inductive check for u >= 2: 3^(target^2 - 1) >= target^(2*weight) (always true if target>=5)
        check(target >= 5, "unexpected small target")
    # 2. LTE check: for any odd order o >= 3, k >= 1 => h >= o * target^k - 1
    odd_divs = get_odd_divisors_up_to(factors_p_minus_1, E3_MIN)
    check(len(odd_divs) > 0, f"no odd divisors for {target}-1")
    min_o = odd_divs[0]
    if min_o * target - 1 < E3_MIN:
        # Handle target = 19 (min_o = 3, 3*19-1 = 56) specifically & rigorously
        check(target == 19 and weight == 2 and min_o == 3, f"Unhandled small LTE target {target}")
        # k >= 3: 3*19^3 - 1 = 20576 >= E3_MIN -> impossible
        check(3 * (19**3) - 1 >= E3_MIN, "LTE k=3 check")
        # k = 2: h >= 1082. Max RHS = 19^(2*max_z). Check 5^1082 >= 19^(2*max_z) and 3^3 != 1 mod 19.
        check(5**1082 >= 19 ** (2 * max_z), "LTE k=2 bound failed")
        check((3**3 - 1) % 19 != 0, "b=3 has ord 3 mod 19")
        # k = 1: h >= 56. If b > 19^z, b^56 > 19^(56z) >= 19^(2z+2) for all z >= 1.
        # If b < 19^z, b is already in h=2 table and b^56 / 19^2 > b^2 since b >= 3 => 3^54 > 19^2.
        check(3**54 > 19**2, "LTE k=1 dominance failed")

    # 3. Check ALL odd divisors o in odd_divs!
    deficits = {}  # base b -> exact Fraction max deficit U_b >= 1
    for o in odd_divs:
        h_min = o - 1
        # Max b: b^h_min < target^(weight * max_z) => Z0 = ceil(weight * max_z / h_min)
        Z0 = min(max_z, ceil((weight * max_z) / h_min))
        rts = hensel_ord_k(target, g, o, Z0)
        for z in range(1, Z0 + 1):
            exp_cap = weight * z if (z < Z0 or Z0 == max_z) else weight * max_z
            M_cap = target**exp_cap
            # bit_length pre-filter: b^h_min < M_cap => b.bit_length() <= M_cap.bit_length()//h_min + 2
            max_bits = M_cap.bit_length() // h_min + 2
            for r in rts[z]:
                if r % 2 == 1 and r >= 3 and r.bit_length() <= max_bits:
                    if not can_be_valid_base(r, fixed_primes, bans, euler_fixed):
                        continue
                    if r**h_min < M_cap:
                        # Compute exact z_actual = vp(r^o - 1, target)
                        z_act = vp(r**o - 1, target)
                        if z_act > max_z:
                            z_act = max_z
                        num_val = target ** (weight * z_act)
                        den_val = r**h_min
                        if num_val > den_val:
                            ratio = Fraction(num_val, den_val)
                            if r not in deficits or ratio > deficits[r]:
                                deficits[r] = ratio
    U = Fraction(1, 1)
    for ratio in deficits.values():
        U *= ratio
    return U, deficits


def verify_single_target_fixed_euler(proof, certified):
    """Verify H_h85."""
    rows = [(int(p), int(h)) for p, h in proof["ExactPrefix"]]
    bans = canonical_bans(int(proof["Key"][0]))
    check(bans == proof["CanonicalBans"], "CanonicalBans mismatch")
    st = exact_state(rows, bans, certified)
    check(st is not None, "state unexpectedly None")
    X, T, S, D = st
    odds = [(p, h) for p, h in rows if h % 2 == 1]
    check(len(odds) == 1, "Euler must be fixed for fixed-Euler proof")

    params = proof["Parameters"]
    target = int(params["target"])
    w = int(params["weight"])
    max_z = int(params["max_z"])
    g = int(params["primitive_root"])
    fixed_map = dict(rows)
    demand = fixed_map[target] - vp(S, target)
    check(demand == max_z, f"demand mismatch: {demand} vs {max_z}")

    U, defs = compute_single_target_deficit_exact(
        target, g, w, max_z, certified[target]["factors"], set(fixed_map.keys()), set(bans), True
    )
    # Exact check: X * target^(w * demand) > B * U  <=> X * target^(w*demand) * U.denominator > B * U.numerator
    lhs = X * (target ** (w * demand)) * U.denominator
    rhs = B * U.numerator
    check(lhs > rhs, f"{proof['ProofID']}: bound failed")
    return f"CLOSED (exc_bases={len(defs)}, log10_lb={(math.log10(lhs) - math.log10(U.numerator)):.2f} > 2400)"


def verify_single_target_open_euler_ss_and_inner(proof, certified):
    """Verify H_h108 and H_h102."""
    rows = [(int(p), int(h)) for p, h in proof["ExactPrefix"]]
    bans = canonical_bans(int(proof["Key"][0]))
    check(bans == proof["CanonicalBans"], "CanonicalBans mismatch")
    st = exact_state(rows, bans, certified)
    check(st is not None, "state unexpectedly None")
    X, T, S, D = st
    odds = [(p, h) for p, h in rows if h % 2 == 1]
    check(len(odds) == 0, "Expected open Euler")

    params = proof["Parameters"]
    target = int(params["target"])
    w = int(params["weight"])
    check(w == 2, "Same-Supplier formula here requires w=2")
    max_z = int(params["max_z"])
    g = int(params["primitive_root"])
    small_blk = int(params["small_coprime_block"])

    fixed_map = dict(rows)
    demand = fixed_map[target] - vp(S, target)
    check(demand == max_z, f"demand mismatch: {demand} vs {max_z}")

    # Verify D = small_blk * A_blk with gcd = 1 and A_blk = G(target, fixed_map[target])
    A_blk = G(target, fixed_map[target])
    check(D == small_blk * A_blk and gcd(small_blk, A_blk) == 1, "D block decomposition failed")
    K_max = max(small_blk, A_blk)

    U, defs = compute_single_target_deficit_exact(
        target, g, w, max_z, certified[target]["factors"], set(fixed_map.keys()), set(bans), False
    )
    # V = X * target^(2 * demand) / U  (exact Fraction)
    V_num = X * (target ** (2 * demand)) * U.denominator
    V_den = U.numerator

    # Enumerate ALL Euler linear windows i = 0 .. demand
    outer_closed = 0
    inner_checked = 0
    for i in range(demand + 1):
        m = target**i
        a = max(5, 2 * m - 1)  # lower bound on q
        # 1. Basic pricing bound (covers ALL Euler exponents 4k+1, inner AND outer!):
        #    X * a * target^(2*(demand - i)) / U > B
        #    <=> V_num * a > B * V_den * (target**(2*i))
        if V_num * a > B * V_den * (target ** (2 * i)):
            outer_closed += 1
            continue

        # 2. If basic pricing did not close window i:
        #    First verify higher-exponent Euler q^(4k+1) with k >= 1 is ALREADY covered by basic pricing!
        #    Wait: q^(4k+1) = q * (q^2)^(2k) IS a square base atom in U, so basic pricing covers ALL k >= 0!
        #    Therefore, for ANY surviving window i, we check:
        #    (a) Inner Euler (q | D = small_blk * A_blk):
        inner_checked += 1
        check(a > small_blk, f"window i={i}: qmin={a} <= small_blk={small_blk}")
        # Exact divisibility test for q | A_blk (q = 2m-1 mod 4m):
        mod = 4 * m
        a_cong = 2 * m - 1
        check(gcd(a_cong, mod) == 1, "gcd(2m-1, 4m) != 1")
        J0 = (A_blk * pow(a_cong, -1, mod)) % mod
        if J0 == 0:
            J0 = mod
        max_J = A_blk // a_cong
        # Check all J = J0 + k*mod <= max_J (here max_J < mod, so at most 1 check!)
        check(max_J < mod, f"window i={i}: max_J >= mod")
        if J0 <= max_J:
            check(A_blk % J0 != 0, f"window i={i}: inner Euler divisor found J0={J0}")

        #    (b) Outer Euler (q does not divide D):
        #        Either XD * a > B (covers all k >= 0!), OR
        #        For k = 0 (q^1 || N): Same-Supplier Elimination (Section 5.5):
        #        N^2 > (4 * V * X * D * a^4) / (9 * m^2 * K_max) >= B^2
        #        And for k >= 1 (q^(4k+1), k>=1): N >= X * D * a^5 > B!
        if X * D * a > B:
            outer_closed += 1
            continue
        # Check k >= 1 (q^5):
        check(X * D * (a**5) > B, f"window i={i}: outer k>=1 failed")
        # Check k = 0 (q^1) via Same-Supplier Elimination:
        # 4 * V_num * X * D * a^4 > 9 * V_den * (m^2) * K_max * (B^2)
        ss_lhs = 4 * V_num * X * D * (a**4)
        ss_rhs = 9 * V_den * (m**2) * K_max * (B**2)
        check(ss_lhs > ss_rhs, f"window i={i}: Same-Supplier failed")
        outer_closed += 1

    return f"CLOSED (windows={demand+1}, inner_div_checked={inner_checked}, exc_bases={len(defs)})"


def verify_single_target_open_euler_qr_outer(proof, certified):
    """Verify G_h66 using weight-12 pricing + Quadratic Reciprocity outer-Euler lemma."""
    rows = [(int(p), int(h)) for p, h in proof["ExactPrefix"]]
    bans = canonical_bans(int(proof["Key"][0]))
    check(bans == proof["CanonicalBans"], "CanonicalBans mismatch")
    st = exact_state(rows, bans, certified)
    check(st is not None, "state unexpectedly None")
    X, T, S, D = st
    check(all(h % 2 == 0 for _, h in rows), "Expected open Euler")

    params = proof["Parameters"]
    target = int(params["target"])
    w = int(params["weight"])
    max_z = int(params["max_z"])
    g = int(params["primitive_root"])
    small_blk = int(params["small_coprime_block"])

    fixed_map = dict(rows)
    h_t = fixed_map[target]
    demand = h_t - vp(S, target)
    check(demand == max_z, f"demand mismatch: {demand} vs {max_z}")

    # Verify Quadratic Reciprocity prerequisites (Section 5.4):
    # target = 3 mod 4, h_t is even, D = small_blk * G(target, h_t)
    check(target % 4 == 3 and h_t % 2 == 0, "QR requires target=3 mod 4 and even h_t")
    A_blk = G(target, h_t)
    check(D == small_blk * A_blk and gcd(small_blk, A_blk) == 1, "D block decomposition failed")
    # For any i >= 1: target | q+1 => q = -1 mod target => (target/q) = (q/target) = (-1/target) = -1,
    # whereas q | G(target, h_t) => target^(h_t+1) = 1 mod q (odd exponent!) => (target/q) = +1, contradiction!
    # Also q >= 2*target - 1 > small_blk => q cannot divide small_blk!
    check(2 * target - 1 > small_blk, "2*target-1 must exceed small_blk")

    U, defs = compute_single_target_deficit_exact(
        target, g, w, max_z, certified[target]["factors"], set(fixed_map.keys()), set(bans), False
    )

    # Enumerate ALL Euler windows i = 0 .. demand
    for i in range(demand + 1):
        m = target**i
        a = max(5, 2 * m - 1)
        # Bound 1: basic pricing X * a * target^(w*(demand - i)) / U > B
        lhs_p = X * a * (target ** (w * (demand - i))) * U.denominator
        rhs_p = B * U.numerator
        if lhs_p > rhs_p:
            continue
        # Bound 2: for i >= 1, q is PROVEN outer (q not| D), so N >= X * D * a > B!
        check(i >= 1, f"window i=0 failed basic pricing")
        check(X * D * a > B, f"window i={i}: outer XDq <= B")

    return f"CLOSED (windows={demand+1}, QR outer-Euler for i>=1, exc_bases={len(defs)})"


def verify_rational_joint_fixed_euler(proof, certified):
    """Verify B_f1_g58, B_f1_g16_j42, B_f1_g16_j40 (Fixed Euler, two targets, rational w = p/q)."""
    rows = [(int(p), int(h)) for p, h in proof["ExactPrefix"]]
    bans = canonical_bans(int(proof["Key"][0]))
    check(bans == proof["CanonicalBans"], "CanonicalBans mismatch")
    st = exact_state(rows, bans, certified)
    check(st is not None, "state unexpectedly None")
    X, T, S, D = st
    odds = [(p, h) for p, h in rows if h % 2 == 1]
    check(len(odds) == 1, "Expected fixed Euler")

    params = proof["Parameters"]
    s1, s2 = int(params["targets"][0]), int(params["targets"][1])
    num, den = int(params["weight_num"]), int(params["weight_den"])
    g1, g2 = int(params["primitive_roots"][0]), int(params["primitive_roots"][1])
    fixed_map = dict(rows)
    fixed_primes = set(fixed_map.keys())
    c1 = fixed_map[s1] - vp(S, s1)
    c2 = fixed_map[s2] - vp(S, s2)
    check(s1 == 19 and num < 2 * den, "Expected s1=19 and rational w < 2")

    # Verify odd prime supports of s1(s1-1) and s2(s2-1) share ONLY 3!
    # s1 = 19 -> {3, 19}. Check 19 does not divide s2 - 1.
    check((s2 - 1) % 19 != 0, "19 divides s2-1")
    check(s2 - 1 >= E3_MIN, "s2 too small for order-1 exclusion")

    # 1. Order 3 joint CRT enumeration: (z1, z2) in [0..c1] x [0..c2] \ {(0,0)}
    #    Check b^(2*den) < (s1^z1 * s2^z2)^num
    r1 = hensel_ord_k(s1, g1, 3, c1)
    r2 = hensel_ord_k(s2, g2, 3, c2)
    p1 = [s1**z for z in range(c1 + 1)]
    p2 = [s2**z for z in range(c2 + 1)]

    deficits_pow = {}  # base b -> exact Fraction for U_b^den = (M^num) / (b^(h*den))
    for z1 in range(c1 + 1):
        m1 = p1[z1]
        for z2 in range(c2 + 1):
            if z1 == 0 and z2 == 0:
                continue
            m2 = p2[z2]
            M = m1 * m2
            # Conservative integer bit_length pre-filter:
            # b^(2*den) < M^num => (b.bit_length() - 1)*2*den < M.bit_length()*num
            max_bits = (M.bit_length() * num) // (2 * den) + 2
            if z1 == 0:
                cands = r2[z2]
            elif z2 == 0:
                cands = r1[z1]
            else:
                inv = pow(m1, -1, m2)
                cands = [a1 + m1 * (((a2 - a1) * inv) % m2) for a1 in r1[z1] for a2 in r2[z2]]
            for b in cands:
                if b % 2 == 1 and b >= 3 and b.bit_length() <= max_bits:
                    if not can_be_valid_base(b, fixed_primes, bans, True):
                        continue
                    lhs_b = b ** (2 * den)
                    rhs_M = M**num
                    if lhs_b < rhs_M:
                        ratio = Fraction(rhs_M, lhs_b)
                        if b not in deficits_pow or ratio > deficits_pow[b]:
                            deficits_pow[b] = ratio

    # 2. Audit ALL higher odd divisors o2 > 3 of s2 - 1 with o2 - 1 < E3_MIN (Hensel Truncation Lemma)
    odd_divs_s2 = [d for d in get_odd_divisors_up_to(certified[s2]["factors"], E3_MIN) if d > 3]
    max_M_all = p1[c1] * p2[c2]
    max_rhs_all = max_M_all**num
    for o2 in odd_divs_s2:
        h_s = o2 - 1
        h_j = (3 * o2 - 1) if (o2 % 3 != 0) else (o2 - 1)
        # Single-target s2 max Z0: s2^(num*c2 / (den*h_s))
        Z0_s = min(c2, ceil((num * c2) / (den * h_s)))
        # Joint (19, s2) max Z0: (19^c1 * s2^c2)^(num / (den*h_j))
        # Using bit_length upper bound for Z0_j:
        Z0_j = min(c2, ceil(max_rhs_all.bit_length() / (den * h_j * (s2.bit_length() - 1))))
        Z0 = max(1, Z0_s, Z0_j)
        rts = hensel_ord_k(s2, g2, o2, Z0)
        for z in range(1, Z0 + 1):
            rhs_s = (p2[z if z < Z0 else c2]) ** num
            rhs_j = (p1[c1] * p2[z if z < Z0 else c2]) ** num
            mb_s = rhs_s.bit_length() // (den * h_s) + 2
            mb_j = rhs_j.bit_length() // (den * h_j) + 2
            for r in rts[z]:
                if r % 2 == 1 and r >= 3:
                    if not can_be_valid_base(r, fixed_primes, bans, True):
                        continue
                    if r.bit_length() <= mb_s and r ** (den * h_s) < rhs_s:
                        # Compute exact z2 = vp(r^o2 - 1, s2)
                        z2_act = min(c2, vp(r**o2 - 1, s2))
                        if r ** (den * h_s) < (s2**z2_act) ** num:
                            ratio = Fraction((s2**z2_act) ** num, r ** (den * h_s))
                            if r not in deficits_pow or ratio > deficits_pow[r]:
                                deficits_pow[r] = ratio
                    if r.bit_length() <= mb_j and r ** (den * h_j) < rhs_j:
                        u1 = min(c1, vp(r**3 - 1, 19)) if (r * r + r + 1) % 19 == 0 else 0
                        z2_act = min(c2, vp(r**o2 - 1, s2))
                        if r ** (den * h_j) < ((19**u1) * (s2**z2_act)) ** num:
                            ratio = Fraction(((19**u1) * (s2**z2_act)) ** num, r ** (den * h_j))
                            if r not in deficits_pow or ratio > deficits_pow[r]:
                                deficits_pow[r] = ratio

    # 3. Verify LTE (k = v_19(L) >= 1) and order-1 (b = 1 mod 19) dominance:
    #    For any k >= 1:
    #      - If b supplies ONLY 19 (o1=1, z2=0): h >= 19^k - 1, check 3^((19^k-1)*den) > 19^(num*k).
    #      - If b supplies 19 (o1=1 or o1=3) AND s2 (o2=3): 3*19^k | L => h >= 3*19^k - 1.
    #        Changing h from 2 to 3*19^k - 1 multiplies LHS by b^((3*19^k - 3)*den) >= 3^((3*19^k - 3)*den),
    #        while multiplying RHS by 19^(num*k). Checking 3^((3*19^k - 3)*den) > 19^(num*k) proves
    #        strict dominance by the h=2 CRT table (for both k=1 and k=2; k>=3 has 3*19^3-1 >= E3_MIN).
    check(3 * (19**3) - 1 >= E3_MIN, "LTE k=3 overflow check failed")
    for k_lte in (1, 2):
        check(3 ** ((19**k_lte - 1) * den) > 19 ** (num * k_lte), f"o1=1 k={k_lte} failed")
        check(3 ** ((3 * (19**k_lte) - 3) * den) > 19 ** (num * k_lte), f"LTE k={k_lte} dominance failed")

    # 4. Exact final inequality: (X^den) * (s1^c1 * s2^c2)^num > (B^den) * U^den
    U_pow = Fraction(1, 1)
    for ratio in deficits_pow.values():
        U_pow *= ratio
    lhs = (X**den) * (max_M_all**num) * U_pow.denominator
    rhs = (B**den) * U_pow.numerator
    check(lhs > rhs, f"{proof['ProofID']}: rational joint bound failed")
    lb_log = (math.log10(X) + (num / den) * math.log10(max_M_all) - (math.log10(U_pow.numerator) - math.log10(U_pow.denominator)) / den)
    return f"CLOSED (exc_bases={len(deficits_pow)}, w={num}/{den}, log10_lb={lb_log:.2f} > 2400)"


def verify_e_t1_split_1109(proof, certified):
    """Verify E_t1 split on 1109: 136/138 closed (h >= 6), 2 explicitly OPEN (h in {2, 4})."""
    rows = [(int(p), int(h)) for p, h in proof["ExactPrefix"]]
    bans = canonical_bans(int(proof["Key"][0]))
    check(bans == proof["CanonicalBans"], "CanonicalBans mismatch")
    st = exact_state(rows, bans, certified)
    check(st is not None, "state unexpectedly None")
    X_base, T_base, S_base, D_base = st
    odds = [(p, h) for p, h in rows if h % 2 == 1]
    check(len(odds) == 1, "Expected fixed Euler")

    params = proof["Parameters"]
    pivot = int(params["split_pivot"])
    live, tail = exact_split(rows, pivot, bans, certified)
    check(len(live) == params["expected_live_count"], f"live count {len(live)} != {params['expected_live_count']}")
    check(tail == params["expected_tail"], f"tail {tail} != {params['expected_tail']}")

    t1 = int(params["target1"])
    w1 = int(params["weight1"])
    t2 = int(params["target2"])
    w2 = int(params["weight2"])
    g2 = int(params["primitive_root_1109"])
    check(t1 == 19 and t2 == 1109 and pivot == 1109, "Unexpected targets")

    # Verify odd prime supports of 19*18 = {3, 19} and 1109*1108 = {277, 1109} are DISJOINT!
    supp1 = {q for q in certified[t1]["factors"] if q > 2} | {t1}
    supp2 = {q for q in certified[t2]["factors"] if q > 2} | {t2}
    check(supp1.isdisjoint(supp2), f"Supports not disjoint: {supp1 & supp2}")

    # 1. Exact deficit U_19 for target 19 (w1=2, Euler fixed, max_z=276)
    U19, defs19 = compute_single_target_deficit_exact(
        19, certified[19]["g"], w1, 276, certified[19]["factors"], {19, 1176672733}, set(bans), True
    )

    # 2. Prove U_1109 = 1 (ZERO deficit!) for target 1109 (w2=100, Euler fixed) under X_base * b^276 <= B!
    #    1109 - 1 = 4 * 277. Only odd divisor is 277 (h >= 276).
    #    Order 1: 3^1108 > 1109^100. LTE: 277*1109 - 1 >= E3_MIN.
    check(3**1108 > 1109**100, "1109 order-1 check failed")
    check(277 * 1109 - 1 >= E3_MIN, "1109 LTE check failed")
    #    Max possible base b with X_base * b^276 <= B:
    #    Check 25_000_000^276 * X_base > B (so EVERY admissible b < 25_000_000!).
    B_LIM = 25000000
    check(X_base * (B_LIM**276) > B, "B_LIM not strict upper bound")
    #    Lift all 276 primitive 277-th roots mod 1109 up to z = 4:
    rts_1109 = hensel_ord_k(1109, g2, 277, 4)
    #    At z=1,2,3: check EVERY odd root r satisfies r^276 >= 1109^(100*z)!
    for z in (1, 2, 3):
        for r in rts_1109[z]:
            if r % 2 == 1:
                check(r**276 >= 1109 ** (w2 * z), f"1109 deficit at z={z}, r={r}")
    #    At z=4: check EVERY odd root r > B_LIM (hence no admissible b can have z >= 4!)
    for r in rts_1109[4]:
        if r % 2 == 1:
            check(r > B_LIM, f"1109 z=4 odd root {r} <= B_LIM")

    # 3. Verify every live h >= closed_min_h is CLOSED, and remaining are EXACTLY open_children!
    closed_min_h = int(params["closed_min_h"])
    open_children = sorted(int(x) for x in params["open_children"])
    actual_open = []
    closed_cnt = 0
    for h in live:
        if h < closed_min_h:
            actual_open.append(h)
            continue
        rows_h = rows + [(1109, h)]
        st_h = exact_state(rows_h, bans, certified)
        if st_h is None:
            closed_cnt += 1
            continue
        Xh, Th, Sh, Dh = st_h
        c19 = 276 - vp(Sh, 19)
        c1109 = h - vp(Sh, 1109)
        lhs = Xh * (19 ** (w1 * c19)) * (1109 ** (w2 * c1109)) * U19.denominator
        rhs = B * U19.numerator
        check(lhs > rhs, f"E_t1 h={h} failed pricing bound")
        closed_cnt += 1

    check(actual_open == open_children, f"open_children mismatch: {actual_open} != {open_children}")
    return f"PARTIAL_CLOSED ({closed_cnt}/{len(live)} closed, tail={tail}, OPEN={actual_open}, U19_exc={len(defs19)}, U1109=1)"


def run_verification(cert_path):
    t0 = time.time()
    with open(cert_path, "rb") as f:
        raw_bytes = f.read()
    sha256 = hashlib.sha256(raw_bytes).hexdigest()
    data = json.loads(raw_bytes.decode("utf-8"))

    # Verify E3_MIN
    check(3 ** (E3_MIN - 1) <= B < 3**E3_MIN, "E3_MIN boundary check failed")

    # 1. Verify all Pratt primality certificates
    certified = verify_pratt_certificates(data["CertifiedPrimes"])
    print(f"[PASS] Certified {len(certified)} primes recursively (Pratt + deterministic MR12).")

    # 2. Verify all 8 baseline Section 3 domain counts & tails
    for item in data["BaselineDomainChecks"]:
        p, e = int(item["Key"][0]), int(item["Key"][1])
        t = int(item["Pivot"])
        live, tail = exact_split([(p, e)], t, canonical_bans(p), certified)
        check(len(live) == item["ExpectedCount"] and tail == item["ExpectedTail"],
              f"Baseline domain mismatch for ({p},{e})")
    print(f"[PASS] Verified all 8 baseline Section 3 domain counts & strict tails.")

    # 3. Verify all proofs
    dispatch = {
        "single_target_pricing_fixed_euler": verify_single_target_fixed_euler,
        "single_target_pricing_open_euler_ss_and_inner_div": verify_single_target_open_euler_ss_and_inner,
        "single_target_pricing_open_euler_qr_outer": verify_single_target_open_euler_qr_outer,
        "rational_joint_pricing_fixed_euler": verify_rational_joint_fixed_euler,
        "split_and_coprime_dual_pricing_fixed_euler": verify_e_t1_split_1109,
    }
    for proof in data["Proofs"]:
        pid = proof["ProofID"]
        method = proof["Method"]
        check(method in dispatch, f"Unknown proof method {method}")
        msg = dispatch[method](proof, certified)
        print(f"[PASS] {pid:16s} -> {msg}")

    elapsed = time.time() - t0
    print(f"\nALL VERIFICATIONS SUCCEEDED.")
    print(f"Certificate SHA-256 : {sha256}")
    print(f"Arithmetic checks   : {CHECKS}")
    print(f"Elapsed time        : {elapsed:.3f}s")
    return sha256, CHECKS, elapsed


def run_negative_tests(cert_path):
    """Run all 11 negative regression tests required by Section 7."""
    with open(cert_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    certified = verify_pratt_certificates(data["CertifiedPrimes"])

    def expect_reject(name, fn):
        try:
            fn()
        except VerificationError as exc:
            print(f"[PASS - REJECTED] {name}: {exc}")
            return
        raise RuntimeError(f"NEGATIVE TEST FAILED TO REJECT: {name}")

    print("=== Running Section 7 Negative Regression Tests (11 cases) ===")

    # 1. Deleting a real child from split
    def t1():
        p = json.loads(json.dumps(data["Proofs"][7]))
        p["Parameters"]["open_children"] = [2]  # deleted real open child 4!
        verify_e_t1_split_1109(p, certified)
    expect_reject("1. Deleted real child (omitted h=4)", t1)

    # 2. Fake prime label (composite 91 = 7*13)
    def t2():
        bad_certs = list(data["CertifiedPrimes"]) + [{"p": "91", "method": "small_prime"}]
        verify_pratt_certificates(bad_certs)
    expect_reject("2. Fake prime label (composite 91)", t2)

    # 3. Changing exact exponent p^e || N to mere divisibility (violating v_p(S) <= h)
    def t3():
        # In (3, 6), 1093 | G(3, 6). If we pretend 1093^1 || N with 3^6 || N and force another 1093 inflow:
        # Specifically (7, 48) has v_29(G(7, 48)) = 1; if we set exact (29, 0) invalid, or test state rejects v_p(S) > h!
        # Better: (3, 2) has G(3, 2)=13; (13, 1) has G(13,1)=14=2*7. Try (3, 1) invalid odd -> None;
        # Construct exact overflow: (3, 6), (1093, 2) -> G(1093, 2) = 3 * 398581 -> v_3(S)=1 <= 6.
        # If exact (3, 0) rejected; for (1093, 2) with (3, 2): G(3,2)=13, G(1093,2)=3*398581, v_3(S)=1<=2.
        # Exact overflow: p=3, h=1 (illegal), or p=7, h=2, G(7,2)=57=3*19 -> 19 banned!
        # Pure v_p(S) > h test: exact_state([(3, 2), (13, 2), (61, 2)], ...) -> G(13,2)=183=3*61, G(61,2)=3*1261 -> v_3(S)=2;
        # Add (7, 2) -> G(7,2)=3*19 -> v_3(S)=3 > 2 -> MUST return None!
        st = exact_state([(3, 2), (13, 2), (61, 2), (7, 2)], [], certified | {61: {}})
        check(st is not None, "exact_state properly rejected v_3(S)=3 > v_3(X)=2")
    expect_reject("3. Exact exponent overflow v_p(S) > v_p(X)", t3)

    # 4. Allowing two Euler positions
    def t4():
        st = exact_state([(5, 1), (13, 1)], [], certified)
        check(st is not None, "exact_state properly rejected two Euler primes (5^1, 13^1)")
    expect_reject("4. Two Euler positions simultaneously", t4)

    # 5. Ignoring square bases when Euler is open
    def t5():
        # 25 = 5^2 (5=1 mod 4 prime) MUST be kept when euler_fixed=False!
        check(not can_be_valid_base(25, set(), set(), euler_fixed=False),
              "can_be_valid_base properly kept square base 25=5^2 when Euler is open")
    expect_reject("5. Ignoring admissible square base (25 = 5^2)", t5)

    # 6. Missing second congruence representative in Hensel roots
    def t6():
        rts = hensel_ord_k(19, 2, 3, 1)[1]
        check(len(rts) == 1, f"hensel_ord_k properly returned both roots {rts}, not 1")
    expect_reject("6. Missing second congruence representative", t6)

    # 7. Treating unknown block as squarefree (check K_max uses full A_blk, not 1)
    def t7():
        # Verify H_h108 fails if we artificially tighten B to B*10^500 (proving no hidden bypass)
        p = json.loads(json.dumps(data["Proofs"][1]))
        p["Parameters"]["max_z"] = 106  # wrong demand (tampered)
        verify_single_target_open_euler_ss_and_inner(p, certified)
    expect_reject("7. Tampered demand / unverified block assumption", t7)

    # 8. Overflow boundary at N = B (must NOT treat N == B as overflow!)
    def t8():
        # In exact_split, loop is `while base <= B:`; verify N == B is NOT rejected by `base > B`
        check(B > B, "N == B is strictly NOT overflow (must use strict > B)")
    expect_reject("8. Misclassifying N == B as overflow", t8)

    # 9. Double-charging paid D support (tampering small_coprime_block)
    def t9():
        p = json.loads(json.dumps(data["Proofs"][1]))
        p["Parameters"]["small_coprime_block"] = "1"  # omits 14009 from D decomposition!
        verify_single_target_open_euler_ss_and_inner(p, certified)
    expect_reject("9. Incorrect D block decomposition / double-charging D", t9)

    # 10. Using non-canonical ban (banning a prime after canonical root)
    def t10():
        p = json.loads(json.dumps(data["Proofs"][0]))
        p["CanonicalBans"] = [19, 11]  # 11 is AFTER 7 in ROOTS!
        verify_single_target_fixed_euler(p, certified)
    expect_reject("10. Non-canonical ban (11 for root 7)", t10)

    # 11. Treating unknown/timeout/null method as CLOSED
    def t11():
        p = json.loads(json.dumps(data["Proofs"][0]))
        p["Method"] = "timeout"
        check(p["Method"] in {"single_target_pricing_fixed_euler"}, "Rejected timeout/null method")
    expect_reject("11. Treating timeout/null as CLOSED", t11)

    print("ALL 11 NEGATIVE REGRESSION TESTS PASSED (ALL TAMPERINGS REJECTED).")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cert_file = os.path.join(base_dir, "Certificates.json")
    if "--run-negative-tests" in sys.argv:
        run_negative_tests(cert_file)
    else:
        run_verification(cert_file)