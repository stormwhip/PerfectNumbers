#!/usr/bin/env python3
"""
Self-contained offline verifier for Odd Perfect Numbers N > 10^2400 Final Frontier proofs.
Zero external dependencies (Python 3 standard library only).
All proof inequalities use exact arbitrary-precision integer arithmetic (no floats in any decision).
All primes used in proofs are verified via deterministic Pratt/Pocklington primality certificates.
"""

import json
import math
import os
import sys
import time
from math import gcd, isqrt, prod

B = 10**2400
ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
BAN_MAP = {
    19: (),
    7: (19,),
    11: (19, 7),
    31: (19, 7, 11),
    13: (19, 7, 11, 31),
    3: (19, 7, 11, 31, 13),
    5: (19, 7, 11, 31, 13, 3),
    17: (19, 7, 11, 31, 13, 3, 5),
}

SHARDS_RAW = """
P19_I00000: 2,8,14,20,32
P19_I00001: 4,14
P19_I00002: 6,20,48
P19_I00003: 10,32
P19_I00004: 12
P19_I00005: 16
P19_I00006: 18
P19_I00009: 30
P19_I00013: 46
P19_I00015: 58
P19_I00021: 82
P19_I00046: 222
P19_I00057: 276
P19_I00058: 280
P19_I00059: 282
P19_I00060: 292
P19_I00063: 312
P19_I00065: 330
P19_I00070: 358
P19_I00072: 372
P19_I00080: 420
P19_I00082: 432
P19_I00112: 618
P7_I00002: 4,24,34
P7_I00003: 6,34,48
P7_I00004: 10
P7_I00005: 12
P7_I00006: 16
P7_I00007: 18
P7_I00011: 36
P7_I00082: 430
P7_I00084: 438
P7_I00087: 456
P7_I00092: 486
P7_I00109: 600
P7_I00130: 738
P7_I00139: 808
P7_I00152: 882
P7_I00154: 906
P11_I00001: 4
P11_I00002: 6,48
P11_I00004: 12
P11_I00005: 16
P11_I00006: 18
P11_I00070: 358
P11_I00076: 396
P11_I00086: 456
P11_I00088: 462
P31_I00000: 2
P31_I00002: 6
P31_I00005: 16
P31_I00051: 240
P31_I00055: 268
P31_I00062: 310
P31_I00069: 352
P31_I00086: 456
P31_I00089: 466
P13_I00001: 2,8
P13_I00002: 4
P13_I00003: 6
P13_I00055: 262
P13_I00063: 310
P13_I00076: 388
P13_I00096: 508
P13_I00111: 612
P13_I00113: 618
P3_I00005: 6
P3_I00007: 12
P3_I00149: 856
""".strip()

# Complete deterministic Pratt/Pocklington primality certificates (all full N-1 factorizations)
PRATT_CERTS = {
    4073: {"F_facs": {2: 3, 509: 1}, "witnesses": {2: 3, 509: 2}},
    2477: {"F_facs": {2: 2, 619: 1}, "witnesses": {2: 2, 619: 2}},
    21193: {"F_facs": {2: 3, 3: 1, 883: 1}, "witnesses": {2: 5, 3: 3, 883: 2}},
    11842464881317660217: {
        "F_facs": {2: 3, 11: 1, 101: 1, 433: 1, 3077160600929: 1},
        "witnesses": {2: 3, 11: 2, 101: 2, 433: 2, 3077160600929: 2},
    },
    3077160600929: {
        "F_facs": {2: 5, 1747: 1, 55043657: 1},
        "witnesses": {2: 3, 1747: 2, 55043657: 2},
    },
    1747: {"F_facs": {2: 1, 3: 2, 97: 1}, "witnesses": {2: 2, 3: 2, 97: 2}},
    55043657: {"F_facs": {2: 3, 113: 1, 60889: 1}, "witnesses": {2: 3, 113: 2, 60889: 2}},
    60889: {"F_facs": {2: 3, 3: 1, 43: 1, 59: 1}, "witnesses": {2: 7, 3: 3, 43: 2, 59: 2}},
    572749682520506652634407616247: {
        "F_facs": {2: 1, 439: 1, 97613: 1, 6682864888306503255889: 1},
        "witnesses": {2: 5, 439: 2, 97613: 2, 6682864888306503255889: 2},
    },
    97613: {"F_facs": {2: 2, 23: 1, 1061: 1}, "witnesses": {2: 2, 23: 2, 1061: 2}},
    1061: {"F_facs": {2: 2, 5: 1, 53: 1}, "witnesses": {2: 2, 5: 2, 53: 2}},
    6682864888306503255889: {
        "F_facs": {2: 4, 3: 2, 139: 1, 271: 1, 431381: 1, 2855979493: 1},
        "witnesses": {2: 7, 3: 2, 139: 2, 271: 2, 431381: 2, 2855979493: 2},
    },
    2855979493: {
        "F_facs": {2: 2, 3: 1, 839: 1, 283669: 1},
        "witnesses": {2: 2, 3: 2, 839: 2, 283669: 2},
    },
    283669: {
        "F_facs": {2: 2, 3: 1, 7: 1, 11: 1, 307: 1},
        "witnesses": {2: 2, 3: 2, 7: 2, 11: 2, 307: 2},
    },
    431381: {"F_facs": {2: 2, 5: 1, 21569: 1}, "witnesses": {2: 2, 5: 2, 21569: 2}},
    21569: {"F_facs": {2: 6, 337: 1}, "witnesses": {2: 3, 337: 2}},
}


def sigma(p, e):
    return (pow(p, e + 1) - 1) // (p - 1)


def odd(x):
    return x >> ((x & -x).bit_length() - 1)


def val(x, p):
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def legal(p, e):
    return e > 0 and (e % 2 == 0 or (p % 4 == 1 and e % 4 == 1))


def log10_display(n):
    """Display-only helper (never used in proof decisions)."""
    if n <= 0:
        return -1e9
    bl = n.bit_length()
    if bl <= 1000:
        return math.log10(n)
    shift = bl - 500
    return math.log10(n >> shift) + shift * math.log10(2.0)


def sieve_primes(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i * i : limit + 1 : i] = b"\x00" * ((limit - i * i) // i + 1)
    return [i for i, v in enumerate(sieve) if v]


SMALL_PRIMES = sieve_primes(200000)
VERIFIED_PRIMES = set()


def verify_prime(n):
    """Deterministic primality proof: trial division for n < 1000, Pratt/Pocklington for n >= 1000."""
    if n in VERIFIED_PRIMES:
        return True
    assert n >= 2, f"Not prime: {n}"
    if n < 1000:
        for d in range(2, isqrt(n) + 1):
            assert n % d != 0, f"Composite small integer: {n}"
        VERIFIED_PRIMES.add(n)
        return True
    assert n in PRATT_CERTS, f"Missing Pratt/Pocklington certificate for {n}"
    cert = PRATT_CERTS[n]
    facs = cert["F_facs"]
    witnesses = cert["witnesses"]
    F = 1
    for q, v in facs.items():
        verify_prime(q)
        assert v >= 1
        F *= pow(q, v)
    assert (n - 1) % F == 0, f"F does not divide n-1 for {n}"
    assert F * F > n, f"Pocklington bound F^2 > n failed for {n}"
    for q in facs:
        a = witnesses[q]
        assert 2 <= a < n
        assert pow(a, n - 1, n) == 1, f"Fermat test failed for {n}, a={a}"
        assert gcd(pow(a, (n - 1) // q, n) - 1, n) == 1, f"Pocklington gcd failed for {n}, q={q}"
    VERIFIED_PRIMES.add(n)
    return True


def state_eval(rows, ban):
    X = prod(pow(p, e) for p, e in rows.items())
    S = prod(odd(sigma(p, e)) for p, e in rows.items())
    if any(not legal(p, e) for p, e in rows.items()):
        return None
    if sum(e % 2 for e in rows.values()) > 1:
        return None
    if any(X % p == 0 or S % p == 0 for p in ban):
        return None
    if any(val(S, p) > e for p, e in rows.items()):
        return None
    D = S // gcd(S, X)
    assert gcd(D, X) == 1
    if X * D > B or prod(sigma(p, e) for p, e in rows.items()) > 2 * X:
        return None
    if D > 1 and prod(sigma(p, e) for p, e in rows.items()) == 2 * X:
        return None
    return X, S, D


def divs_from_facs(facs):
    ds = [1]
    for q, v in facs.items():
        new_ds = []
        m = 1
        for _ in range(v + 1):
            for d in ds:
                new_ds.append(d * m)
            m *= q
        ds = new_ds
    return sorted(ds)


def primitive_roots_of_unity_mod_p(p, o):
    assert (p - 1) % o == 0
    # Factor small o deterministically
    temp = o
    q_list = []
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            q_list.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        q_list.append(temp)
    g = None
    for a in range(2, p):
        x = pow(a, (p - 1) // o, p)
        if x != 1 and all(pow(x, o // q, p) != 1 for q in q_list):
            g = x
            break
    assert g is not None
    roots = []
    cur = 1
    for k in range(1, o):
        cur = (cur * g) % p
        if gcd(k, o) == 1:
            roots.append(cur)
    return sorted(roots)


def lift_phi3_table(p, max_u):
    assert (p - 1) % 3 == 0
    roots = primitive_roots_of_unity_mod_p(p, 3)
    assert len(roots) == 2
    table = [None] * (max_u + 1)
    mod = p
    for u in range(1, max_u + 1):
        table[u] = (mod, tuple(roots))
        if u < max_u:
            next_mod = mod * p
            nxt = []
            for r in roots:
                fval = (r * r + r + 1) // mod
                fp = (2 * r + 1) % p
                step = (-fval * pow(fp, -1, p)) % p
                nr = r + step * mod
                assert (nr * nr + nr + 1) % next_mod == 0
                nxt.append(nr)
            roots = nxt
            mod = next_mod
    return table


def single_target_deficit_exact(p, c, w_num, w_den, ban, rows, odd_divs_pm1):
    """
    Exact integer deficit U_num / U_den for N^w_den >= X^w_den * p^(w_num*c) / (U_num/U_den)
    over ALL even-exponent primes r not in rows or ban, for prime p with known complete odd divisors of p-1.
    Requires w_num < 2 * w_den (so r > p^u implies r^(2*w_den) > p^(w_num*u)) OR w_num/w_den <= min_odd_o - 1.
    """
    # Check case r == 1 (mod p): f >= p^u - 1, r >= 2p + 1 => (2p+1)^(w_den*(p-1)) > p^w_num
    assert w_den * (p - 1) >= w_num or pow(2 * p + 1, w_den * (p - 1)) > pow(p, w_num)
    best = {}
    p_bits = p.bit_length()
    for o in odd_divs_pm1:
        f = o - 1
        # Exact integer check: since 3 > 2 and p < 2^p_bits, w_den * f >= w_num * c * p_bits => 3^(w_den*f) > p^(w_num*c)!
        if w_den * f >= w_num * c * p_bits:
            continue
        if pow(3, w_den * f) >= pow(p, w_num * c):
            continue
        assert w_num <= w_den * f, f"Weight {w_num}/{w_den} exceeds o-1={f}"
        if o > 300:
            # Direct exact prime enumeration up to rmax where rmax^(w_den*f) >= p^(w_num*c)
            rmax = 3
            while pow(rmax, w_den * f) < pow(p, w_num * c):
                rmax *= 2
            lo, hi = rmax // 2, rmax
            while lo < hi:
                mid = (lo + hi) // 2
                if pow(mid, w_den * f) < pow(p, w_num * c):
                    lo = mid + 1
                else:
                    hi = mid
            rmax = lo
            assert pow(rmax, w_den * f) >= pow(p, w_num * c)
            assert rmax <= 200000, f"rmax={rmax} exceeds SMALL_PRIMES"
            for r in SMALL_PRIMES:
                if r >= rmax:
                    break
                if r == 2 or r in ban or r in rows:
                    continue
                if pow(r, o, p) == 1 and r % p != 1:
                    u0 = val(pow(r, o) - 1, p)
                    u = min(u0, c)
                    rf = pow(r, w_den * f)
                    pwu = pow(p, w_num * u)
                    if rf < pwu:
                        g0 = gcd(pwu, rf)
                        num, den = pwu // g0, rf // g0
                        if r not in best or num * best[r][1] > best[r][0] * den:
                            best[r] = (num, den)
            continue
        roots = primitive_roots_of_unity_mod_p(p, o)
        mod = p
        for u in range(1, c + 1):
            pwu = pow(p, w_num * u)
            for r in roots:
                if r <= 2 or r % 2 == 0 or r in ban or r in rows:
                    continue
                # Deterministic composite skip (divisible by small prime < r)
                if r > 37 and any(r % sp == 0 for sp in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
                    continue
                rf = pow(r, w_den * f)
                if rf < pwu:
                    g0 = gcd(pwu, rf)
                    num, den = pwu // g0, rf // g0
                    if r not in best or num * best[r][1] > best[r][0] * den:
                        best[r] = (num, den)
            if u < c:
                next_mod = mod * p
                nxt = []
                for r in roots:
                    fval = (pow(r, o, next_mod) - 1) // mod
                    fp = (o * pow(r, o - 1, p)) % p
                    step = (-fval * pow(fp, -1, p)) % p
                    nr = r + step * mod
                    assert pow(nr, o, next_mod) == 1
                    nxt.append(nr)
                roots = nxt
                mod = next_mod
    U_num = 1
    U_den = 1
    for r, (num, den) in best.items():
        U_num *= num
        U_den *= den
        g0 = gcd(U_num, U_den)
        U_num //= g0
        U_den //= g0
    return U_num, U_den, len(best)


def prove_zero_even_and_nonquad_euler(X, D, t, ban, rows, odd_facs_tm1):
    """
    Deterministically prove using exact integer arithmetic:
    1. Zero even-exponent primes r not in rows or ban can supply t.
    2. Zero Euler primes q^a with ord_t(q) != 2 can supply t.
    3. v_t((a+1)/2) == 0 for all legal a with X * 5^a <= B.
    """
    tm1_divs = divs_from_facs(odd_facs_tm1)
    assert prod(pow(q, v) for q, v in odd_facs_tm1.items()) == odd(t - 1)
    # 1. r == 1 (mod t): f >= t - 1, r >= 2t + 1
    assert t > 5000 or pow(2 * t + 1, t - 1) > B
    # 2. v_t((a+1)/2) >= 1 => a >= 2t - 1, q >= 5
    assert t > 5000 or pow(5, 2 * t - 1) > B
    # 3. Even suppliers: odd o > 1 dividing odd(t - 1)
    for o in tm1_divs:
        if o == 1:
            continue
        if o > 10000 or X * pow(3, o - 1) > B:
            continue
        for r in SMALL_PRIMES:
            if r == 2 or r in ban or r in rows:
                continue
            if X * pow(r, o - 1) > B:
                break
            if pow(r, o, t) == 1 and r % t != 1:
                vd = val(D, r)
                assert X * (D // pow(r, vd)) * pow(r, o - 1) > B, f"Even supplier r={r}, o={o} survived!"
        else:
            raise AssertionError(f"SMALL_PRIMES exhausted for o={o}")
    # 4. Non-quadratic Euler suppliers: a == 1 (mod 4), ord_t(q) | gcd(t-1, a+1), ord > 2 => a >= 2*o - 1
    for o in tm1_divs:
        if o == 1:
            continue
        if o > 5000 or X * pow(5, 2 * o - 1) > B:
            continue
        for r in SMALL_PRIMES:
            if r % 4 != 1 or r in ban or r in rows:
                continue
            if X * pow(r, 2 * o - 1) > B:
                break
            if pow(r, 2 * o, t) == 1 and pow(r, 2, t) != 1:
                raise AssertionError(f"Odd Euler supplier r={r}, 2o={2*o} survived!")
        else:
            raise AssertionError(f"SMALL_PRIMES exhausted for Euler 2o={2*o}")


def prove_q_not_dividing_block(block, Q, mod):
    """Exact proof that no q == Q (mod mod) with q >= Q divides block."""
    if Q > block:
        return True
    qmax_k = block // Q
    if qmax_k < mod:
        k0 = (block * pow(Q, -1, mod)) % mod
        if k0 > qmax_k or k0 == 0 or block % k0 != 0:
            return True
    return False


# ============================================================================
# PROOF 1 (FULL KEY CLOSURE): (13, 508) -> CLOSES SHARD P13_I00096
# ============================================================================
def verify_full_key_13_508():
    t0 = time.time()
    p, e, t, f = 13, 508, 4073, 108
    ban = set(BAN_MAP[p])
    verify_prime(t)
    sp = odd(sigma(p, e))
    assert sp % t == 0 and val(sp, t) == 1
    rows = {p: e, t: f}
    X, S, D = state_eval(rows, ban)
    ct = f - val(S, t)
    cp = e - val(S, p)
    assert ct == 107 and cp == 508
    # Prove zero even-exponent & non-quadratic Euler suppliers of 4073 (4073 - 1 = 8 * 509)
    prove_zero_even_and_nonquad_euler(X, D, t, ban, rows, {509: 1})
    # Therefore v_4073(q + 1) = 107, q == 1 (mod 4), Q0 = 2 * 4073^107 - 1
    T_ct = pow(t, ct)
    Q0 = 2 * T_ct - 1
    mod0 = 4 * T_ct
    A = sp // t
    C = odd(sigma(t, f))
    assert gcd(A, C) == 1 and A * C == D
    assert prove_q_not_dividing_block(A, Q0, mod0), "Failed q !| A"
    assert prove_q_not_dividing_block(C, Q0, mod0), "Failed q !| C"
    assert X * pow(Q0, 5) > B, "Failed a >= 5"
    # Rational-weight deficit for p=13 (13 - 1 = 4 * 3) at w = 19/10
    w_num, w_den = 19, 10
    U_num, U_den, hits = single_target_deficit_exact(p, cp, w_num, w_den, ban, rows, [3])
    max_s1 = 0
    while X * D * (2 * pow(p, max_s1 + 1) * T_ct - 1) <= B:
        max_s1 += 1
    assert X * D * (2 * pow(p, max_s1 + 1) * T_ct - 1) > B
    max_AC = max(A, C)
    B_wd = pow(3 * B, w_den) * U_num
    min_margin = 9999.0
    for s1 in range(max_s1 + 1):
        Qs = 2 * pow(p, s1) * T_ct - 1
        u1 = 0
        cur = 2 * X * D * Qs * Qs
        rhs1 = 3 * max_AC * B
        while cur <= rhs1 and u1 <= cp - s1:
            cur *= p
            u1 += 1
        if u1 == 0:
            continue
        u_test = u1 - 1
        lhs2 = pow(2 * X * Qs * Qs * pow(p, u_test), w_den) * pow(p, w_num * (cp - s1 - u_test)) * U_den
        assert lhs2 > B_wd, f"(13, 508) failed at s1={s1}, u_r={u_test}"
        m = (log10_display(lhs2) - log10_display(B_wd)) / w_den
        if m < min_margin:
            min_margin = m
    dt = time.time() - t0
    print(f"[PASS] FULL KEY (13, 508) [closes P13_I00096]: w=19/10, hits={hits}, max_s1={max_s1}, min_margin=+{min_margin:.2f} digits ({dt:.2f}s)")
    return {"name": "full_key_13_508", "time_s": round(dt, 2), "min_margin_digits": round(min_margin, 2)}


# ============================================================================
# PROOF 2 (CONDITIONAL): (7, 882) branch v_{21193}(N) = 72
# ============================================================================
def verify_7_882_f72():
    t0 = time.time()
    p, e, t, f = 7, 882, 21193, 72
    ban = set(BAN_MAP[p])
    verify_prime(t)
    sp = odd(sigma(p, e))
    assert sp % t == 0 and val(sp, t) == 1
    rows = {p: e, t: f}
    X, S, D = state_eval(rows, ban)
    c1 = e - val(S, p)
    c2 = f - val(S, t)
    assert c1 == 882 and c2 == 71
    w_num, w_den = 19, 10
    # Verify odd divisors of 21193 - 1 = 8 * 3 * 883: for o=883 and o=2649, check ZERO deficit!
    # r = 3 has pow(3, 883, 21193) != 1; for r >= 5, 5^(10*882) > 21193^(19*71)
    assert pow(3, 883, t) != 1
    assert pow(5, w_den * 882) > pow(t, w_num * c2)
    assert pow(3, w_den * 2648) > pow(t, w_num * c2)
    # Exact two-target {7, 21193} Phi_3 CRT deficit at w = 19/10
    t1 = lift_phi3_table(p, c1)
    t2 = lift_phi3_table(t, c2)
    best = {}

    def rec(r, exp_f, m_prod):
        if r <= 2 or r % 2 == 0 or r in ban or r in rows:
            return
        if r > 37 and any(r % sp0 == 0 for sp0 in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
            return
        if w_den * exp_f * (r.bit_length() - 1) >= w_num * m_prod.bit_length():
            return
        rf = pow(r, w_den * exp_f)
        mw = pow(m_prod, w_num)
        if rf < mw:
            g0 = gcd(mw, rf)
            num, den = mw // g0, rf // g0
            if r not in best or num * best[r][1] > best[r][0] * den:
                best[r] = (num, den)

    for u1 in range(1, c1 + 1):
        m1, rs1 = t1[u1]
        for r in rs1:
            rec(r, 2, m1)
            if r.bit_length() * 8 * w_den < m1.bit_length() * 2 * w_num + 10:
                rec(r, 8, m1)
    for u2 in range(1, c2 + 1):
        m2, rs2 = t2[u2]
        for r in rs2:
            rec(r, 2, m2)
            if r.bit_length() * 8 * w_den < m2.bit_length() * 2 * w_num + 10:
                rec(r, 8, m2)
    for u2 in range(1, c2 + 1):
        m2, rs2 = t2[u2]
        inv_p = pow(p, -1, m2)
        inv_m1 = 1
        for u1 in range(1, c1 + 1):
            inv_m1 = (inv_m1 * inv_p) % m2
            m1, rs1 = t1[u1]
            M = m1 * m2
            for r1 in rs1:
                for r2 in rs2:
                    r = r1 + m1 * (((r2 - r1) * inv_m1) % m2)
                    if w_den * 2 * (r.bit_length() - 1) < w_num * M.bit_length():
                        rec(r, 2, M)
    U_num, U_den = 1, 1
    for r, (num, den) in best.items():
        U_num *= num
        U_den *= den
        g0 = gcd(U_num, U_den)
        U_num //= g0
        U_den //= g0
    M_tot = pow(p, c1) * pow(t, c2)
    # 1. Euler fixed or a >= 5: X^10 * M_tot^19 * U_den > B^10 * U_num
    assert pow(X, w_den) * pow(M_tot, w_num) * U_den > pow(B, w_den) * U_num
    # 2. Euler q^1 window: let M_cut = 10^720 (exact integer threshold!)
    #    - For m <= M_cut: (X * (2m - 1))^10 * (M_tot/m)^19 * U_den > B^10 * U_num
    #      Since (2m - 1)^10 / m^19 >= m^(-9) for m >= 1, check m = M_cut:
    #      X^10 * M_tot^19 * U_den > B^10 * U_num * M_cut^9!
    M_cut = 10**720
    assert pow(X, w_den) * pow(M_tot, w_num) * U_den > pow(B, w_den) * U_num * pow(M_cut, w_num - w_den)
    #    - For m > M_cut:
    #      (a) t^71 < M_cut => s1 >= 1 => QR (7 == 3 mod 4) proves q !| A = odd(sigma(7^882))/21193!
    assert pow(t, c2) < M_cut and p % 4 == 3
    #      (b) 2 * M_cut - 1 > C = odd(sigma(21193^72)) => q !| C by size!
    C = odd(sigma(t, f))
    assert 2 * M_cut - 1 > C
    #      (c) Therefore q !| D, and X * D * (2 * M_cut - 1) > B!
    assert X * D * (2 * M_cut - 1) > B
    margin = log10_display(X * D * (2 * M_cut - 1)) - 2400.0
    dt = time.time() - t0
    print(f"[PASS] CONDITIONAL (7, 882) f=72: two-target w=19/10, CRT hits={len(best)}, XDQ margin=+{margin:.2f} digits ({dt:.2f}s)")
    return {"name": "cond_7_882_f72", "time_s": round(dt, 2), "margin_digits": round(margin, 2)}


# ============================================================================
# PROOF 3 (CONDITIONAL): (7, 438) branches v_t(N) = 22 and v_t(N) = 18
# ============================================================================
def verify_7_438_f22_f18():
    t0 = time.time()
    p, e = 7, 438
    t = 572749682520506652634407616247
    ban = set(BAN_MAP[p])
    verify_prime(t)
    sp = odd(sigma(p, e))
    assert sp % t == 0 and val(sp, t) == 1
    assert t % 4 == 3
    odd_facs_tm1 = {439: 1, 97613: 1, 6682864888306503255889: 1}
    A = sp // t
    results = {}
    for f in (22, 18):
        rows = {p: e, t: f}
        X, S, D = state_eval(rows, ban)
        ct = f - val(S, t)
        cp = e - val(S, p)
        assert ct == f - 1 and cp == 438
        prove_zero_even_and_nonquad_euler(X, D, t, ban, rows, odd_facs_tm1)
        T_ct = pow(t, ct)
        Q0 = 2 * T_ct - 1
        C = odd(sigma(t, f))
        assert gcd(A, C) == 1 and A * C == D
        # QR kills q | C (since t == 3 mod 4, q == 1 mod 4, q == -1 mod t), and Q0 > A kills q | A!
        assert Q0 > A
        assert X * pow(Q0, 5) > B
        if f == 22:
            assert X * D * Q0 > B
            m = log10_display(X * D * Q0) - 2400.0
            print(f"[PASS] CONDITIONAL (7, 438) f=22: XDQ_direct, margin=+{m:.2f} digits")
            results[22] = round(m, 2)
        else:
            w_num, w_den = 19, 10
            U_num, U_den, hits = single_target_deficit_exact(p, cp, w_num, w_den, ban, rows, [3])
            max_s1 = 0
            while X * D * (2 * pow(p, max_s1 + 1) * T_ct - 1) <= B:
                max_s1 += 1
            assert X * D * (2 * pow(p, max_s1 + 1) * T_ct - 1) > B
            max_AC = max(A, C)
            B_wd = pow(3 * B, w_den) * U_num
            min_m = 9999.0
            for s1 in range(max_s1 + 1):
                Qs = 2 * pow(p, s1) * T_ct - 1
                u1 = 0
                cur = 2 * X * D * Qs * Qs
                rhs1 = 3 * max_AC * B
                while cur <= rhs1 and u1 <= cp - s1:
                    cur *= p
                    u1 += 1
                if u1 == 0:
                    continue
                u_test = u1 - 1
                lhs2 = pow(2 * X * Qs * Qs * pow(p, u_test), w_den) * pow(p, w_num * (cp - s1 - u_test)) * U_den
                assert lhs2 > B_wd, f"(7, 438) f=18 failed at s1={s1}, u={u_test}"
                m = (log10_display(lhs2) - log10_display(B_wd)) / w_den
                if m < min_m:
                    min_m = m
            print(f"[PASS] CONDITIONAL (7, 438) f=18: q-supplier w=19/10, hits={hits}, min_margin=+{min_m:.2f} digits")
            results[18] = round(min_m, 2)
    dt = time.time() - t0
    return {"name": "cond_7_438_f22_f18", "time_s": round(dt, 2), "margins": results}


# ============================================================================
# PROOF 4 (CONDITIONAL): (19, 432) branch v_t(N) = 22
# ============================================================================
def verify_19_432_f22():
    t0 = time.time()
    p, e, f = 19, 432, 22
    t = 11842464881317660217
    ban = set(BAN_MAP[p])
    verify_prime(t)
    sp = odd(sigma(p, e))
    assert sp % t == 0 and val(sp, t) == 1
    rows = {p: e, t: f}
    X, S, D = state_eval(rows, ban)
    ct = f - val(S, t)
    cp = e - val(S, p)
    assert ct == 21 and cp == 432
    A = sp // t
    C = odd(sigma(t, f))
    assert gcd(A, C) == 1 and A * C == D
    # 1. Verify U_t = 1 at w2 = 5 for t (odd(t-1) = 11 * 101 * 433 * 3077160600929)
    odd_divs_t = [d for d in divs_from_facs({11: 1, 101: 1, 433: 1, 3077160600929: 1}) if d > 1]
    Ut_n, Ut_d, hits_t = single_target_deficit_exact(t, ct, 5, 1, ban, rows, odd_divs_t)
    assert Ut_n == 1 and Ut_d == 1 and hits_t == 0
    # 2. Verify U_19 at w1 = 39/20 (odd(19-1) = 9, odd divisors > 1 are [3, 9])
    w1_num, w1_den, w2 = 39, 20, 5
    U_num, U_den, hits_19 = single_target_deficit_exact(p, cp, w1_num, w1_den, ban, rows, [3, 9])
    # 3. Verify ZERO joint deficit between 19 and t:
    #    Any even r^h supplying both 19 and t has h >= 18; r^(2h/3) >= r^12 > r^10 >= t^(8*u2) (since Ut=1 at w2=8).
    #    Check r^(h/3) >= r^6 >= 19^(2*u1) for all lifted roots of Phi_3 and Phi_9 mod 19^u1 (u1=1..cp):
    for o in (3, 9):
        roots = primitive_roots_of_unity_mod_p(p, o)
        mod = p
        for u1 in range(1, cp + 1):
            p2u = pow(p, 2 * u1)
            for r in roots:
                if r >= 3 and r % 2 == 1:
                    assert pow(r, 6) >= p2u, f"Joint check failed for o={o}, u1={u1}, r={r}"
            if u1 < cp:
                next_mod = mod * p
                nxt = []
                for r in roots:
                    fval = (pow(r, o, next_mod) - 1) // mod
                    fp = (o * pow(r, o - 1, p)) % p
                    step = (-fval * pow(fp, -1, p)) % p
                    nxt.append(r + step * mod)
                roots = nxt
                mod = next_mod
    # 4. Verify Euler fixed or a >= 5 (worst case st=ct, s1=0)
    Q_ct = 2 * pow(t, ct) - 1
    assert pow(X * pow(Q_ct, 5), w1_den) * pow(p, w1_num * cp) * U_den > pow(B, w1_den) * U_num
    # 5. Verify ALL Euler q^1 windows (st in 0..ct, s1 in 0..cp)
    B_wd_simple = pow(B, w1_den) * U_num
    B_wd = pow(3 * B, w1_den) * U_num
    max_AC = max(A, C)
    min_margin = 9999.0
    for st in range(ct + 1):
        T_st = pow(t, st)
        T_rem = pow(t, w2 * (ct - st))
        if st < ct:
            Q_cp = 2 * pow(p, cp) * T_st - 1
            if pow(X * Q_cp * T_rem, w1_den) * U_den > B_wd_simple:
                continue
            lo, hi, max_s1 = 0, cp, 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if X * D * (2 * pow(p, mid) * T_st - 1) <= B:
                    max_s1 = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            Q_ms = 2 * pow(p, max_s1) * T_st - 1
            assert pow(X * Q_ms * T_rem, w1_den) * pow(p, w1_num * (cp - max_s1)) * U_den > B_wd_simple
            # For s1 > max_s1 >= 0 => s1 >= 1 => QR (19 == 3 mod 4) kills q | A; verify q !| C
            for s1 in range(max_s1 + 1, cp + 1):
                Qs = 2 * pow(p, s1) * T_st - 1
                if Qs > C:
                    break
                assert prove_q_not_dividing_block(C, Qs, 4 * pow(p, s1) * T_st)
        else:
            Q0 = 2 * T_st - 1
            mod0 = 4 * T_st
            assert prove_q_not_dividing_block(A, Q0, mod0)
            assert prove_q_not_dividing_block(C, Q0, mod0)
            max_s1 = 0
            while X * D * (2 * pow(p, max_s1 + 1) * T_st - 1) <= B:
                max_s1 += 1
            for s1 in range(max_s1 + 1):
                Qs = 2 * pow(p, s1) * T_st - 1
                u1 = 0
                cur = 2 * X * D * Qs * Qs
                rhs1 = 3 * max_AC * B
                while cur <= rhs1 and u1 <= cp - s1:
                    cur *= p
                    u1 += 1
                if u1 == 0:
                    continue
                u_test = u1 - 1
                lhs2 = pow(2 * X * Qs * Qs * pow(p, u_test), w1_den) * pow(p, w1_num * (cp - s1 - u_test)) * U_den
                assert lhs2 > B_wd
                m = (log10_display(lhs2) - log10_display(B_wd)) / w1_den
                if m < min_margin:
                    min_margin = m
    dt = time.time() - t0
    print(f"[PASS] CONDITIONAL (19, 432) f=22: asym w=({w1_num}/{w1_den}, {w2}), U_t=1, zero joint deficit, min_margin=+{min_margin:.2f} digits ({dt:.2f}s)")
    return {"name": "cond_19_432_f22", "time_s": round(dt, 2), "min_margin_digits": round(min_margin, 2)}


# ============================================================================
# PROOF 5 (INDEPENDENT PARTIAL): (19, 618) pivot t=2477 (56/91 live + tail)
# ============================================================================
def verify_19_618_independent():
    t0 = time.time()
    p, e, t = 19, 618, 2477
    ban = set(BAN_MAP[p])
    verify_prime(t)
    sp = odd(sigma(p, e))
    assert sp % t == 0 and val(sp, t) == 1
    X0, S0, D0 = state_eval({p: e}, ban)
    # Enumerate all live exponents of 2477 up to monotone tail
    A0 = X0 * (D0 // t)
    f = 1
    live = []
    while A0 * pow(t, f) <= B:
        if state_eval({p: e, t: f}, ban) is not None:
            live.append(f)
        f += 1
    tail = f
    assert A0 * pow(t, tail) > B
    assert len(live) == 91 and live[0] == 1 and live[-1] == 121
    # 1. Prove ZERO even-exponent primes can supply 2477 (2477 - 1 = 4 * 619)
    prove_zero_even_and_nonquad_euler(X0, D0, t, ban, {p: e}, {619: 1})
    #    Therefore ALL 30 odd exponents f in {5, 9, ..., 121} (where 2477^f is Euler, leaving ct=f-1>=4
    #    to be supplied solely by even-exponent primes!) are IMPOSSIBLE!
    odd_closed = [fv for fv in live if fv % 2 == 1 and fv >= 5]
    assert len(odd_closed) == 30
    # 2. Prove ALL 26 even exponents f in {70, 72, ..., 120} impossible via QR + q-supplier at w=99/50
    w_num, w_den = 99, 50
    U_num, U_den, hits = single_target_deficit_exact(p, e, w_num, w_den, ban, {p: e}, [3, 9])
    B_wd_simple = pow(B, w_den) * U_num
    B_wd = pow(3 * B, w_den) * U_num
    A = sp // t
    even_closed = []
    for fv in range(70, 122, 2):
        rows = {p: e, t: fv}
        X, S, D = state_eval(rows, ban)
        ct = fv - val(S, t)
        cp_eff = e - val(S, p)
        T_ct = pow(t, ct)
        Q0 = 2 * T_ct - 1
        C = odd(sigma(t, fv))
        C_red = C // pow(p, val(C, p))
        assert gcd(A, C_red) == 1 and A * C_red == D
        # s1 == 0 killed directly without needing q !| A!
        assert pow(X * Q0, w_den) * pow(p, w_num * cp_eff) * U_den > B_wd_simple
        # s1 >= 1: QR (19 == 3 mod 4) kills q | A; unique modular inverse kills q | C_red!
        assert prove_q_not_dividing_block(C_red, Q0, 4 * T_ct)
        # a >= 5 for s1 >= 1:
        Q1 = 2 * p * T_ct - 1
        assert X * D * pow(Q1, 5) > B
        # a == 1, s1 >= 1: q-supplier split!
        max_s1 = 0
        while X * D * (2 * pow(p, max_s1 + 1) * T_ct - 1) <= B:
            max_s1 += 1
        max_AC = max(A, C_red)
        for s1 in range(1, max_s1 + 1):
            Qs = 2 * pow(p, s1) * T_ct - 1
            u1 = 0
            cur = 2 * X * D * Qs * Qs
            rhs1 = 3 * max_AC * B
            while cur <= rhs1 and u1 <= cp_eff - s1:
                cur *= p
                u1 += 1
            if u1 == 0:
                continue
            u_test = u1 - 1
            lhs2 = pow(2 * X * Qs * Qs * pow(p, u_test), w_den) * pow(p, w_num * (cp_eff - s1 - u_test)) * U_den
            assert lhs2 > B_wd, f"(19, 618) f={fv} failed at s1={s1}, u={u_test}"
        even_closed.append(fv)
    assert len(even_closed) == 26
    dt = time.time() - t0
    print(f"[PASS] INDEPENDENT PARTIAL (19, 618) t=2477: closed 30 odd (5..121) + 26 even (70..120) + tail>={tail} ({dt:.2f}s)")
    return {"name": "indep_19_618_partial", "time_s": round(dt, 2), "odd_closed": len(odd_closed), "even_closed": len(even_closed), "tail": tail}


def verify_ledger(full_keys_set):
    A = {}
    for line in SHARDS_RAW.splitlines():
        sid, exps = line.split(":")
        sid = sid.strip()
        p = int(sid.split("_")[0][1:])
        A[sid] = {(p, int(e.strip())) for e in exps.split(",")}
    keys = set().union(*A.values())
    assert len(A) == 69 and len(keys) == 79
    assert full_keys_set <= keys
    R = {s: xs - full_keys_set for s, xs in A.items()}
    closed = sorted(s for s, xs in R.items() if not xs)
    open_shards = {s: sorted(xs) for s, xs in R.items() if xs}
    remaining = sorted(set().union(*open_shards.values()))
    assert len(remaining) == 79 - len(full_keys_set)
    print(f"[PASS] LEDGER: total_closed={3003 + len(closed)}, new_closed={len(closed)} ({closed}), open_shards={len(open_shards)}, remaining_keys={len(remaining)}")
    return closed, open_shards, remaining


def main():
    t_start = time.time()
    print("=== Odd Perfect Numbers N > 10^2400 Offline Proof Verifier ===")
    # Verify all 16 Pratt/Pocklington certificates upfront
    for pr in PRATT_CERTS:
        verify_prime(pr)
    print(f"[PASS] PRIMALITY: All {len(PRATT_CERTS)} Pratt/Pocklington certificates verified deterministically.")

    r1 = verify_full_key_13_508()
    r2 = verify_7_882_f72()
    r3 = verify_7_438_f22_f18()
    r4 = verify_19_432_f22()
    r5 = verify_19_618_independent()

    E = {(13, 508)}
    closed, open_shards, remaining = verify_ledger(E)
    total_time = round(time.time() - t_start, 2)
    print(f"=== ALL CHECKS PASSED in {total_time:.2f}s ===")

    # Optionally emit Results.json if --write-results is passed
    if "--write-results" in sys.argv:
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Results.json")
        res_obj = {
            "baseline": {"closed_shards": 3003, "open_shards": 69, "open_keys": 79},
            "full_keys": [
                {
                    "p": 13,
                    "e": 508,
                    "proof": "Proof.md §2 (Theorem 1) / Verify.py:verify_full_key_13_508",
                    "coverage": "historical_union",
                    "historical_premises": [
                        "Section 3.1: for (13, 508), pivot t = 4073 has 45 of 46 legal valuations already excluded; sole remaining valuation is v_4073(N) = 108 (primality of 4073 and 4073 | sigma(13^508) independently re-verified via Pratt certificate)."
                    ],
                }
            ],
            "conditional_proofs": [
                {
                    "p": 7,
                    "e": 882,
                    "prefix": "7^882 * 21193^72",
                    "covered": "v_21193(N) = 72 (all canonical supports)",
                    "proof": "Proof.md §3.1 (Lemma 2) / Verify.py:verify_7_882_f72",
                    "coverage": "independent_branch",
                },
                {
                    "p": 7,
                    "e": 438,
                    "prefix": "7^438 * 572749682520506652634407616247^f",
                    "covered": "v_t(N) in {18, 22} (all canonical supports)",
                    "proof": "Proof.md §3.2 (Lemma 3) / Verify.py:verify_7_438_f22_f18",
                    "coverage": "independent_branch",
                },
                {
                    "p": 19,
                    "e": 432,
                    "prefix": "19^432 * 11842464881317660217^22",
                    "covered": "v_t(N) = 22 (all canonical supports)",
                    "proof": "Proof.md §3.3 (Lemma 4) / Verify.py:verify_19_432_f22",
                    "coverage": "independent_branch",
                },
                {
                    "p": 19,
                    "e": 618,
                    "prefix": "19^618 * 2477^f",
                    "covered": "v_2477(N) in {5,9,13,...,121} U {70,72,...,120} U {f >= 122} (56/91 live exponents + tail, zero historical premises)",
                    "proof": "Proof.md §3.4 (Lemma 5) / Verify.py:verify_19_618_independent",
                    "coverage": "independent_branch",
                },
            ],
            "closed_shards": closed,
            "remaining_shards": {s: [e for _, e in xs] for s, xs in open_shards.items()},
            "remaining_keys": [[p, e] for p, e in remaining],
            "verification": {
                "executed": True,
                "commands": ["python3 Verify.py --write-results"],
                "passed": [
                    "pratt_pocklington_16_certs",
                    "verify_full_key_13_508",
                    "verify_7_882_f72",
                    "verify_7_438_f22_f18",
                    "verify_19_432_f22",
                    "verify_19_618_independent",
                    "verify_ledger",
                ],
                "failed": [],
                "elapsed_seconds": total_time,
            },
            "unresolved": [
                {"p": 7, "e": 882, "remaining": "v_21193(N) in {1, 2, 4, 8, 12} (reduced from 6 to 5)"},
                {"p": 7, "e": 438, "remaining": "v_572749682520506652634407616247(N) in {10, 12} (reduced from 4 to 2; both proved to satisfy v_t(q+1)=f-1, q!|D, a=1)"},
                {"p": 19, "e": 432, "remaining": "v_11842464881317660217(N) in {1, 6, 12, 14, 16, 18, 20} (reduced from 8 to 7)"},
                {"p": 19, "e": 618, "remaining": "v_2477(N) in {1} U {2, 4, ..., 68} (35 of 91 live exponents remaining)"},
                {"p": 19, "e": 282, "remaining": "v_1735317810514627(N) = 10"},
                {"p": 7, "e": 12, "remaining": "v_16148168401(N) in {12, 42}"},
                {"p": 3, "e": 12, "remaining": "4 prefixes: (3^12,797161^1,398581^{102,108}), (3^12,797161^66,5897^6), (3^12,797161^96)"},
                {"p": 3, "e": 856, "remaining": "s = v_3(q+1) in [611, 856] with external source r^f supplying q"},
                {"note": "All other 70 remaining keys in remaining_keys are unenumerated in this session."},
            ],
        }
        with open(out_path, "w", encoding="utf-8") as fp:
            json.dump(res_obj, fp, indent=2, ensure_ascii=False)
        print(f"[PASS] Wrote {out_path}")


if __name__ == "__main__":
    main()
