#!/usr/bin/env python3
"""
Standalone, zero-network, Python 3 standard-library verifier for
Multi-Hop Indicator-Capacity Valuation-Flow Dual + Universal E_{c,l} Congruence
certificates for odd perfect numbers N <= 10^2400.

All inequalities are verified with certified fixed-point integer intervals
(scale S = 10^12), rounding strictly in the conservative direction at every step.
"""
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

SCALE = 10**12
FLOW_SCALE = 10**6
B_EXP_10 = 2400
ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
BOUND = 10**B_EXP_10
CERT_DIR = Path(__file__).resolve().parent / "Certificates"
SPECIAL_LIMIT = 10**18 - 1


def ilog(n, base):
    lo, hi = 0, n.bit_length() + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if base**mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


MAX_EXPONENT = ilog(BOUND, 3)


# ---------------------------------------------------------------------------
# 1. Certified Rational-Interval Logarithm (Exact Integer / Fraction Arithmetic)
# ---------------------------------------------------------------------------

def _log_in_1_2(num: int, den: int):
    """Return (lo, hi) integers with lo <= SCALE * ln(num/den) <= hi, for 1 <= num/den <= 2."""
    if num == den:
        return 0, 0
    u = Fraction(num - den, num + den)
    u2 = u * u
    M = 18
    term = u
    s = Fraction(0)
    for j in range(M + 1):
        s += term / (2 * j + 1)
        term *= u2
    s *= 2
    rem_hi = (2 * term) / ((2 * M + 3) * (1 - u2))
    lo = (s.numerator * SCALE) // s.denominator
    hi_frac = s + rem_hi
    hi = (hi_frac.numerator * SCALE + hi_frac.denominator - 1) // hi_frac.denominator
    return lo, hi


LN2_LO, LN2_HI = _log_in_1_2(2, 1)


@lru_cache(maxsize=65536)
def log_interval(num: int, den: int = 1):
    """Certified integer interval (lo, hi) such that lo <= SCALE * ln(num/den) <= hi."""
    if num <= 0 or den <= 0:
        raise ValueError("log_interval requires positive rational")
    if num == den:
        return 0, 0
    k = 0
    a, b = num, den
    while a >= 2 * b:
        b <<= 1
        k += 1
    while a < b:
        a <<= 1
        k -= 1
    ylo, yhi = _log_in_1_2(a, b)
    if k >= 0:
        return k * LN2_LO + ylo, k * LN2_HI + yhi
    else:
        return k * LN2_HI + ylo, k * LN2_LO + yhi


LN10_LO, LN10_HI = log_interval(10, 1)
LN_B_HI = B_EXP_10 * LN10_HI


# ---------------------------------------------------------------------------
# 2. Proven Deterministic Primality (< 2^64) and Number-Theoretic Helpers
# ---------------------------------------------------------------------------

def is_prime_proven_64(n: int) -> bool:
    """Deterministic Miller-Rabin proven exact for all 0 <= n < 2^64 (Sinclair 2011)."""
    if n < 2 or n >= (1 << 64):
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while (d & 1) == 0:
        d >>= 1
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def sieve_primes(limit: int):
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, math.isqrt(limit) + 1):
        if is_p[i]:
            is_p[i * i : limit + 1 : i] = bytearray(len(is_p[i * i : limit + 1 : i]))
    return [i for i, v in enumerate(is_p) if v]


def sigma_has_forb(r: int, f: int, forb) -> bool:
    for z in forb:
        if r % z == 1:
            if (f + 1) % z == 0:
                return True
        else:
            if pow(r, f + 1, z) == 1:
                return True
    return False


def get_f_min(r: int, forb) -> int:
    for f in range(2, 240, 2):
        if not sigma_has_forb(r, f, forb):
            return f
    raise ValueError(f"f_min > 240 for r={r}")


def prime_divides_sigma(w: int, r: int, f: int) -> bool:
    """Exact check whether prime w divides sigma(r^f) = (r^(f+1)-1)/(r-1)."""
    if r % w == 1:
        return (f + 1) % w == 0
    return pow(r, f + 1, w) == 1


def vp_sigma(p: int, r: int, f: int) -> int:
    """Exact v_p(sigma(r^f)) for p in {3, 5} and even f >= 2."""
    if p not in (3, 5):
        raise ValueError("vp_sigma specialized for p in {3, 5}")
    if r % p != 1:
        return 0
    t = f + 1
    c = 0
    while t % p == 0:
        t //= p
        c += 1
    return c


# ---------------------------------------------------------------------------
# 3. Certified Dual Verification (Zero Floating Point!)
# ---------------------------------------------------------------------------

class CertifiedDual:
    def __init__(self, mu, lam_p, const_no_target, theta_map, delta_src, delta_q):
        self.mu = mu
        self.lam_p = lam_p
        self.const_no_target = const_no_target
        self.theta_map = theta_map
        self.delta_src = delta_src
        self.delta_q = delta_q


def verify_dual_entry(p: int, forb: tuple, R_act: int, W_max: int, entry: dict,
                      primes_R: list) -> CertifiedDual:
    """Strictly verify one dual certificate using exact integer intervals."""
    if p not in (3, 5) or forb != ROOTS[:ROOTS.index(p)] or W_max != SPECIAL_LIMIT:
        raise ValueError("Unexpected root or special-prime cutoff")
    if not 100000 <= R_act <= 500000:
        raise ValueError("Unsupported active-prime cutoff")
    forb_set = set(forb)
    mu, mu_den, lam_p, lam_den = (
        entry[key] for key in ("mu_num", "mu_den", "lam_p_num", "lam_p_den"))
    if (any(type(x) is not int for x in (mu, mu_den, lam_p, lam_den))
            or mu < 0 or mu_den != 1 or lam_p < 0 or lam_den != 1):
        raise ValueError("Dual multipliers must be non-negative integers")

    ln_p_lo, ln_p_hi = log_interval(p, 1)

    def get_ab_max_hi(q):
        if q <= 200000:
            _, hi = log_interval(q, q - 1)
            return hi
        return (SCALE + (q - 2)) // (q - 1)

    # 1. Verify every flow edge [r, f, w, q_flow]
    flows = entry["flows"]
    edge_pen = {}
    theta_map = {}
    active_extra = set()
    max_f_per_r = {}

    scale_mult = SCALE // FLOW_SCALE
    assert scale_mult * FLOW_SCALE == SCALE

    for edge in flows:
        if len(edge) != 4 or any(type(x) is not int for x in edge):
            raise ValueError("Malformed flow edge")
        r, f, w, q_flow = edge
        if q_flow <= 0:
            raise ValueError(f"Non-positive flow {q_flow} on edge ({r},{f})->{w}")
        if r == w or r == p or w == p or r in forb_set or w in forb_set:
            raise ValueError(f"Illegal prime in edge ({r},{f})->{w}")
        if min(r, w) <= 2 or w > W_max or r >= (1 << 64):
            raise ValueError(f"Prime exceeds W_max or 2^64 in edge ({r},{f})->{w}")
        if f < 2 or (f % 2 != 0):
            raise ValueError(f"Non-even exponent f={f} in edge ({r},{f})->{w}")
        if not is_prime_proven_64(r):
            raise ValueError(f"Non-prime source r={r}")
        if not is_prime_proven_64(w):
            raise ValueError(f"Non-prime target w={w}")
        if sigma_has_forb(r, f, forb):
            raise ValueError(f"Edge ({r},{f})->{w} uses forbidden sigma(r^f)")
        if not prime_divides_sigma(w, r, f):
            raise ValueError(f"Divisibility failed: {w} does not divide sigma({r}^{f})")

        flow_scaled = q_flow * scale_mult
        edge_pen[(r, f)] = edge_pen.get((r, f), 0) + flow_scaled
        theta_map[w] = theta_map.get(w, 0) + flow_scaled
        if r > R_act:
            active_extra.add(r)
        if f > max_f_per_r.get(r, 0):
            max_f_per_r[r] = f

    # 2. Verify global tail condition for ALL primes r > R_act not in active_extra and not in theta_map
    ln_R_lo, _ = log_interval(R_act, 1)
    ab_R_hi = get_ab_max_hi(R_act)
    if 2 * ln_R_lo < mu * ab_R_hi:
        raise ValueError(f"Tail check failed for r > {R_act}, r != 1 mod {p}")
    if (p - 1) * ln_R_lo < lam_p * ln_p_hi + mu * ab_R_hi:
        raise ValueError(f"Tail check failed for r > {R_act}, r == 1 mod {p}")

    # 3. Verify all primes r in (allowed <= R_act) U active_extra U set(theta_map.keys())
    allowed_R = [r for r in primes_R if r > 2 and r != p and r not in forb_set]
    check_set = sorted(set(allowed_R) | active_extra | set(theta_map.keys()))

    total_neg = 0
    # Primes beyond the checked set have no incoming edges and nonnegative cost.
    delta_src = delta_q = mu * ab_R_hi

    for r in check_set:
        lr_lo, _ = log_interval(r)
        ab_max_hi = get_ab_max_hi(r)
        theta_r = theta_map.get(r, 0)
        mf = max_f_per_r.get(r, 0)
        fm = get_f_min(r, forb)
        f_cap = max(fm, mf + 2) if mf > 0 else fm
        if r <= 80:
            f_cap = max(f_cap, 64)
        elif r <= 300:
            f_cap = max(f_cap, 42)
        if theta_r > 0:
            f_need = int((theta_r + mu * ab_max_hi) // lr_lo) + 2
            if f_need % 2 == 1:
                f_need += 1
            f_cap = max(f_cap, min(40, f_need))

        tail_rc = f_cap * lr_lo - theta_r - mu * ab_max_hi
        if r % p == 1:
            pb = p
            for b in range(1, ilog(MAX_EXPONENT + 1, p) + 1):
                fb = pb - 1
                f_lb = max(f_cap, fb)
                rc_b = f_lb * lr_lo - theta_r - b * lam_p * ln_p_hi - mu * ab_max_hi
                if rc_b < tail_rc:
                    tail_rc = rc_b
                pb *= p

        best_rc = tail_rc
        for f in range(fm, f_cap, 2):
            if sigma_has_forb(r, f, forb):
                continue
            vp = vp_sigma(p, r, f)
            pen = edge_pen.get((r, f), 0)
            if r <= 500 and f <= 60:
                num_s = (r ** (f + 1) - 1) // (r - 1)
                den_s = r ** f
                _, ab_hi = log_interval(num_s, den_s)
            else:
                ab_hi = ab_max_hi
            rc = f * lr_lo + pen - theta_r - lam_p * vp * ln_p_hi - mu * ab_hi
            if rc < best_rc:
                best_rc = rc

        if best_rc < 0:
            total_neg += best_rc

        adj = theta_r + mu * ab_max_hi + min(0, best_rc)
        delta_src = max(delta_src, adj)
        if r % 4 == 1:
            delta_q = max(delta_q, adj)

    return CertifiedDual(mu, lam_p, total_neg, theta_map, delta_src, delta_q)


# ---------------------------------------------------------------------------
# 4. Exact Per-Exponent Verification (Universal E_{c,l} + All Branches)
# ---------------------------------------------------------------------------

def bound_abundancy_A_hi(p: int, e: int, small_primes: list) -> int:
    """Certified upper bound on SCALE * sum_{r | A} ln(r / (r - 1)) for A = odd(sigma(p^e))."""
    m = e + 1
    is_m_prime = m >= 2 and all(m % d != 0 for d in range(2, math.isqrt(m) + 1))
    _, ln_p_hi = log_interval(p, 1)
    ln_A_hi = (e + 1) * ln_p_hi

    if is_m_prime:
        step = 2 * m
        ln_first_lo, _ = log_interval(step + 1, 1)
        max_k = ln_A_hi // ln_first_lo + 1
        ab_hi = 0
        for j in range(1, max_k + 1):
            d = step * j
            ab_hi += (SCALE + d - 1) // d
        return ab_hi
    else:
        ab_hi = 0
        for r in small_primes:
            if r > 20000:
                break
            if r == 2 or r == p:
                continue
            if prime_divides_sigma(r, p, e):
                _, h = log_interval(r, r - 1)
                ab_hi += h
        ln_cut_lo, _ = log_interval(20011, 1)
        max_k = ln_A_hi // ln_cut_lo + 1
        for j in range(max_k):
            d = 20010 + 2 * j
            ab_hi += (SCALE + d - 1) // d
        return ab_hi


def interior_budget(p, e, A, primes):
    """Bound free p-valuation from A; price every additional unit using T."""
    m = e + 1
    prime_m = is_prime_proven_64(m)
    gift = 0
    rate = None
    remainder = A
    if prime_m:
        # A-primes supplying p must be 1 modulo 2mp.
        step = 2 * m * p
        cutoff = 5_000_000
        candidates = range(step + 1, cutoff + 1, step)
        next_candidate = cutoff + (1 - cutoff) % step
        if next_candidate <= cutoff:
            next_candidate += step
    else:
        cutoff = 20_000
        candidates = (r for r in primes if r <= cutoff and r % p == 1)
        next_candidate = cutoff + 1
    for r in candidates:
        if pow(p, m, r) != 1 or not is_prime_proven_64(r) or A % r:
            continue
        c = 0
        while remainder % r == 0:
            remainder //= r
            c += 1
        b0 = ilog(c + 1, p)
        gift += b0
        price = (p**(b0 + 1) - 1 - c) * log_interval(r)[0]
        rate = price if rate is None else min(rate, price)
    # For unseen factors, b0 free units imply r^c >= r^((p-1)*b0).
    gift += ilog(remainder, next_candidate**(p - 1))
    unknown_rate = log_interval(next_candidate)[0]
    return gift, unknown_rate if rate is None else min(rate, unknown_rate)


def l_zero_impossible(p, e, s):
    P = p**(e + 1)
    Y = p**s
    Q = 2 * Y - 1
    upper_r = math.isqrt((P - 1) // (p - 1))
    # D has a positive term < P*r/q and a negative part
    # < 3*P/(2*q) + r, because q < 3*r^c/2.
    return P * upper_r <= Y * Q and 3 * P + 2 * Q * upper_r <= 2 * Y * Q


def verify_exponent(p, e, duals, primes):
    """Check every Euler and supplier branch for one actual exponent."""
    if p not in (3, 5) or e < 2 or e % 2:
        raise ValueError("Expected an even root exponent for 3 or 5")
    A = (p**(e + 1) - 1) // (p - 1)
    peA = p**e * A
    if peA > BOUND:
        return True, "base-size"
    if any(A % r == 0 for r in ROOTS[:ROOTS.index(p)]):
        return True, "forbidden-factor"

    ln_p_lo, ln_p_hi = log_interval(p)
    # For all e >= 2, sigma(p^e)/p^e is at least 1 + 1/p + 1/p^2.
    geom_lo, _ = log_interval(p*p + p + 1, p*p)
    ln_peA_lo = 2 * e * ln_p_lo + geom_lo
    _, ln_p_ab_hi = log_interval(p, p - 1)
    ab_A_hi = bound_abundancy_A_hi(p, e, primes)
    ab_q_hi = (SCALE + SPECIAL_LIMIT - 1) // SPECIAL_LIMIT
    gift, interior_rate = interior_budget(p, e, A, primes)
    target = LN2_LO - ln_p_ab_hi - ab_A_hi
    dual_lines = []
    for d in duals:
        overlap = sum(th for w, th in d.theta_map.items() if A % w == 0)
        base = d.mu * target + d.const_no_target - overlap
        slope = min(d.lam_p * ln_p_lo, interior_rate)
        dual_lines.append((base, slope, d.mu * ab_q_hi, d.delta_src, d.delta_q))

    def lower(k, special_small=False, remove_supplier=False):
        k = max(0, k - gift)
        if special_small:
            return max(0, max(base + slope*k - dq for base, slope, _, _, dq in dual_lines))
        return max(0, max(base + slope*k - aq - (ds if remove_supplier else 0)
                          for base, slope, aq, ds, _ in dual_lines))

    supplier_max = ilog(MAX_EXPONENT + 1, p)
    small_s_max = ilog(SPECIAL_LIMIT + 1, p) + ilog(MAX_EXPONENT + 1, p)
    if ln_peA_lo + lower(e - min(e, small_s_max), special_small=True) <= LN_B_HI:
        return False, "small-Euler"
    if ln_peA_lo + lower(e - min(e, 20)) <= LN_B_HI:
        return False, "small-valuation"

    # For q > SPECIAL_LIMIT, a_q + 1 <= max_a + 1 and is 2 modulo 4.
    max_a = ilog(BOUND, SPECIAL_LIMIT + 1)
    special_lte_max = ilog((max_a + 1) // 2, p)
    q_improvement = log_interval(5, 3)[0]
    ln_two_thirds = log_interval(2, 3)[0]
    ln_one_third = log_interval(1, 3)[0]

    for s in range(21, e + 1):
        k = e - s
        all_even = lower(k)
        q5_lo = 5 * ((s - special_lte_max) * ln_p_lo + q_improvement)
        if max(ln_peA_lo, e * ln_p_lo + q5_lo) + all_even <= LN_B_HI:
            return False, "Euler-exponent-at-least-five"
        if 2 * s <= e and ln_peA_lo + all_even <= LN_B_HI:
            return False, "Euler-prime-divides-A"

        q_lo = s * ln_p_lo + q_improvement
        without_supplier = lower(k - supplier_max, remove_supplier=True)
        if ln_peA_lo + 2 * q_lo + ln_two_thirds + without_supplier <= LN_B_HI:
            return False, "exterior-supplier"

        interior_supplier = lower(k - supplier_max)
        if ln_peA_lo + q_lo + interior_supplier <= LN_B_HI:
            if not l_zero_impossible(p, e, s):
                return False, "interior-supplier-gap-zero"
            # D and E imply r^gap > (p^s-1)*p^(2s)/(3*p^(2e+2)).
            gap_lo = (3 * s * ln_p_lo - 2 * (e + 1) * ln_p_hi
                      + ln_two_thirds + ln_one_third)
            gap_lo = max(0, gap_lo)
            if ln_peA_lo + q_lo + gap_lo + interior_supplier <= LN_B_HI:
                return False, "interior-supplier-positive-gap"

    return True, "indicator-capacity"


def load_duals(primes):
    result = {}
    for p in (3, 5):
        data = json.loads((CERT_DIR / f"DualP{p}.json").read_text(encoding="utf-8"))
        if data["root"] != p or not data["duals"]:
            raise ValueError("Invalid dual bank")
        cutoff = data["R_act"]
        primes_R = [r for r in primes if r <= cutoff]
        result[p] = [verify_dual_entry(p, tuple(data["forbidden"]), cutoff,
                                      data["W_max"], entry, primes_R)
                     for entry in data["duals"]]
    return result
