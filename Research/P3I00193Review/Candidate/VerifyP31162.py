"""
Self-contained, zero-trust, outward-rounded (40-digit Decimal + exact rational dual)
independent verifier for P3_I00193 ((p, e) = (3, 1162)) against B = 10^2400.

Requires ONLY Python 3 standard library + Appendix B's check.py.
"""
import json
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check

getcontext().prec = 50
EPS = Decimal("1e-35")

def ln_lo(x):
    return Decimal(x).ln() - EPS

def ln_hi(x):
    return Decimal(x).ln() + EPS

def frac_dec(num, den):
    return Decimal(num) / Decimal(den)

LN10_LO = ln_lo(10)
LN10_HI = ln_hi(10)
LN3_LO = ln_lo(3)
LN3_HI = ln_hi(3)
LN2_LO = ln_lo(2)
LN2_HI = ln_hi(2)
LN43_LO = ln_lo(4) - ln_hi(3)
ALPHA_HI = Decimal(4) * LN3_HI
TARGET_NATS_HI = Decimal(2400) * LN10_HI

ABS3 = {7, 11, 13, 19, 31}
SMALL_P_50K = list(check.small_primes(50000))

def verify_trial_division_A(R_A, R_A_all):
    """Deterministically verify no prime r == 1 (mod 6978) <= R_A divides A = S(3, 1162),
    and no prime r == 1 (mod 2326) <= R_A_all divides A."""
    d = 1163
    # 1. r == 1 (mod 6978) up to R_A
    step = 6 * d
    for r in range(1 + step, R_A + 1, step):
        if r % 5 == 0 or r % 7 == 0 or r % 11 == 0 or r % 13 == 0:
            continue
        if pow(3, d, r) == 1:
            check.require(not check.prime64(r), f"Found prime factor {r} <= {R_A} of A with r == 1 mod 3!")
    # 2. r == 1 (mod 2326) up to R_A_all
    step2 = 2 * d
    for r in range(1 + step2, R_A_all + 1, step2):
        if r % 3 == 0 or r % 5 == 0 or r % 7 == 0 or r % 11 == 0 or r % 13 == 0:
            continue
        if pow(3, d, r) == 1:
            check.require(not check.prime64(r), f"Found prime factor {r} <= {R_A_all} of A!")
    return True

def verify_euler_bounds(e, R_A):
    """Exhaustively verify E0, E1, E2 > 2400*ln(10), and compute exact outward-rounded M_E3_lo and s_min."""
    # Build exact ordinary v_3-supplier prefix table up to R_max = 100000
    R_max = 100000
    marginals = []
    for r in check.small_primes(R_max):
        if r <= 3 or r in ABS3 or r % 3 != 1:
            continue
        if any(pow(r, 3, q * (r - 1)) == 1 for q in ABS3):
            continue
        f1 = 2
        while f1 <= 5000 and not check.allowed(r, f1, ABS3):
            f1 += 6
        if f1 > 5000:
            continue
        v1 = check.valuation(f1 + 1, 3)
        c1 = (Decimal(f1) * ln_lo(r)) / Decimal(v1)
        marginals.append((c1, v1))
        step = 3**(v1 + 1)
        f2 = step - 1
        while f2 <= 5000 and (f2 % 2 != 0 or not check.allowed(r, f2, ABS3)):
            f2 += 2 * step
        if f2 <= 5000:
            v2 = check.valuation(f2 + 1, 3)
            c2 = (Decimal(f2 - f1) * ln_lo(r)) / Decimal(v2 - v1)
            marginals.append((c2, v2 - v1))
    marginals.sort(key=lambda x: x[0])
    pref = [Decimal(0)]
    max_m = Decimal(0)
    for cpu, cnt in marginals:
        for _ in range(cnt):
            pref.append(pref[-1] + cpu)
            max_m = cpu
            if len(pref) > e + 5:
                break
        if len(pref) > e + 5:
            break
    check.require(max_m <= Decimal(2) * ln_lo(R_max), "R_max too small for exact ordinary supply table")

    A = check.sigma(3, e)
    ln_pe_lo = Decimal(e) * LN3_LO
    ln_A_lo = ln_lo(A)
    ln_A_hi = ln_hi(A)
    base_lo = ln_pe_lo + ln_A_lo
    unit_A_lo = Decimal(2) * ln_lo(R_A)
    max_free = int(ln_A_hi // unit_A_lo)

    def in_A_extra(u_in):
        val = Decimal(u_in) * unit_A_lo - ln_A_hi
        return val if val > 0 else Decimal(0)

    def extra_ord_full(U):
        best = Decimal("1e30")
        for u_in in range(0, min(U, max_free + 2) + 1):
            c = in_A_extra(u_in) + pref[U - u_in]
            if c < best:
                best = c
        return best

    # Case E0: s = 0
    lb_E0 = base_lo + extra_ord_full(e)
    check.require(lb_E0 > TARGET_NATS_HI, f"E0 failed: {lb_E0/LN10_HI:.2f}")

    # Case E1: a >= 5, s >= 1
    lb_E1 = Decimal("1e30")
    for s in range(1, e + 1):
        # q == 1 mod 3: q >= 37 (since 7,13,19,31 in ABS3), a >= max(5, 3^s - 1)
        c_q1 = Decimal(max(5, 3**s - 1)) * ln_lo(37) if s <= 10 else Decimal("1e20")
        # q == 2 mod 3: s = s1 + s2, q >= max(5, 2*3^s1 - 1), a >= max(5, 2*3^s2 - 1)
        c_q2 = Decimal("1e30")
        for s2 in range(0, min(s, 8)):
            s1 = s - s2
            a_min = max(5, 2 * (3**s2) - 1)
            q_min = max(5, 2 * (3**s1) - 1)
            c_q2 = min(c_q2, Decimal(a_min) * ln_lo(q_min))
        ln_qa = min(c_q1, c_q2)
        extra_q = ln_qa - ln_A_hi
        if extra_q < 0: extra_q = Decimal(0)
        tot = base_lo + extra_q + extra_ord_full(e - s)
        if tot < lb_E1:
            lb_E1 = tot
    check.require(lb_E1 > TARGET_NATS_HI, f"E1 failed: {lb_E1/LN10_HI:.2f}")

    # Case E2: a = 1, q | A => (2*3^s - 1)*(3^s + 1) <= 2*A = 3^(e+1) - 1 => s <= e // 2
    s_max_E2 = 0
    for s in range(1, e + 1):
        if (2 * (3**s) - 1) * (3**s + 1) <= 2 * A:
            s_max_E2 = s
        else:
            break
    lb_E2 = min(base_lo + extra_ord_full(e - s) for s in range(1, s_max_E2 + 1))
    check.require(lb_E2 > TARGET_NATS_HI, f"E2 failed: {lb_E2/LN10_HI:.2f}")

    # Case E3 (a = 1, q not | A):
    # Verify b >= 7 is impossible: r >= 43, f >= 3^7 - 1 = 2186 => r^f / A > 10^2400!
    check.require(Decimal(3**7 - 1) * ln_lo(43) - ln_A_hi > TARGET_NATS_HI, "b >= 7 check failed")

    # Exhaustively compute:
    #   M_E3_lo = min over all (s in [1..e], b in [0..6], u_in in [0..min(e-s-b, max_free+2)])
    #             of base_lo + min(euler_3a(s, b), euler_3b(s, b)) + in_A_extra(u_in) + ALPHA_HI * (e - s - b - u_in)
    # Wait: for u_aux = e - s - b - u_in, since M_true >= base_lo + euler + in_A_extra(u_in) + sum_{r in N_other, forest} (f*ln(r)),
    # rewriting f*ln(r) = (f*ln(r) - ALPHA_HI*v3) + ALPHA_HI*v3 gives:
    #   ln(N) >= [base_lo + euler + in_A_extra(u_in) + ALPHA_HI * u_aux] + [net_cost(forest) + net_cost(N_other)]!
    # Wait: that requires EVERY prime r not | A (other than q, r_source) to have net_cost >= 0!
    # Check: for r == 1 mod 3, r >= 43, f >= 2: 2*ln(43) = 7.522 > 4*ln(3) = 4.394! So net_cost is ALWAYS strictly positive!
    # Also find s_min = smallest s for which base_lo + min(e3a, e3b) + extra_ord_full(e - s - b) <= TARGET_NATS_HI!
    M_E3a_lo = Decimal("1e30")
    M_E3b_lo = Decimal("1e30")
    s_min = e + 1
    ln_23_lo = ln_lo(2) - ln_hi(3)
    for s in range(1, e + 1):
        q_min = max(5, 2 * (3**s) - 1)
        ln_q_lo = ln_lo(q_min)
        for b in range(0, 7):
            if s + b > e:
                continue
            # E3a: q * r^f, where r^f > (2/3)*q*3^b AND r^f >= 43^(3^b - 1) if b > 0
            ln_rf_1 = ln_23_lo + ln_q_lo + Decimal(b) * LN3_LO
            ln_rf_2 = Decimal(3**b - 1) * ln_lo(43) if b > 0 else Decimal(0)
            e3a = ln_q_lo + max(ln_rf_1, ln_rf_2)

            # E3b: q * t, where t = r^(f-c) > Z / (H * (delta + 4)), Z = 3^(s+b), P = 3^(e+1), delta = 3^(e+1-s-b)
            # For q >= q_min:
            #   if q < P: H = P/q => q*t > q^2 * Z / (P * (delta + 4)) >= q_min^2 * Z / (P * (delta + 4))
            #   if q >= P: H = 1 => q*t > q * Z / (delta + 4) >= P * Z / (delta + 4) (larger than q_min^2*Z/(P*(delta+4)) when q_min < P!)
            # Note: since s <= e, q_min = 2*3^s - 1 < 3^(e+1) = P, so minimum over all q >= q_min is strictly at q = q_min!
            exp_d = e + 1 - s - b
            ln_d4_hi = ln_hi(3**exp_d + 4) if exp_d <= 80 else (Decimal(exp_d) * LN3_HI + Decimal(4) / Decimal(3**exp_d) + EPS)
            ln_qt_d12 = Decimal(2) * ln_q_lo + Decimal(s + b) * LN3_LO - Decimal(e + 1) * LN3_HI - ln_d4_hi
            ln_t_val = (Decimal(3**b - 1) * ln_lo(R_A) - ln_A_hi) if b > 0 else Decimal(0)
            if ln_t_val < 0: ln_t_val = Decimal(0)
            e3b = max(ln_q_lo + ln_t_val, ln_qt_d12)

            # Check s_min using full ordinary cost
            if base_lo + min(e3a, e3b) + extra_ord_full(e - s - b) <= TARGET_NATS_HI:
                if s < s_min:
                    s_min = s

            # Compute M_E3a_lo, M_E3b_lo with ALPHA_HI * u_aux
            rem_U = e - s - b
            best_u = Decimal("1e30")
            for u_in in range(0, min(rem_U, max_free + 2) + 1):
                c = in_A_extra(u_in) + ALPHA_HI * Decimal(rem_U - u_in)
                if c < best_u:
                    best_u = c
            if base_lo + e3a + best_u < M_E3a_lo:
                M_E3a_lo = base_lo + e3a + best_u
            if base_lo + e3b + best_u < M_E3b_lo:
                M_E3b_lo = base_lo + e3b + best_u

    return lb_E0, lb_E1, lb_E2, M_E3a_lo, M_E3b_lo, s_min

def verify_not_euler_source(primes_to_check, s_min, e):
    """Verify by exact 4-line congruence killer that NO prime r in primes_to_check
    can be the Euler source of q (with 3^s | q+1, s in [s_min, e]) in E3a."""
    A = check.sigma(3, e)
    mod_s = [3**s for s in range(s_min, e + 1)]
    min_q = [2 * m - 1 for m in mod_s]
    S_min = min_q[0]
    B_rem = check.B // (pow(3, e) * A) # max allowed r^f * S(r, f)
    # Also verify A % r != 0 and r < S_min for every r
    for r in sorted(primes_to_check):
        check.require(r > 3 and r not in ABS3, f"invalid aux prime {r}")
        check.require(A % r != 0, f"aux prime {r} divides A!")
        check.require(r < S_min, f"aux prime {r} >= q_min!")
        # Find range of even f where S(r, f) >= S_min and r^f * S(r, f) <= B_rem
        # Since S(r, f) > r^f and r^f * S(r, f) > r^(2f):
        # f_hi: smallest even f with r^(2f) > B_rem
        # f_lo: largest even f with r^(f+1) < S_min
        lr = float(ln_lo(r))
        f_lo = max(2, int(float(ln_lo(S_min)) / lr) // 2 * 2 - 2)
        f_hi = int(float(ln_hi(B_rem)) / (2.0 * lr)) // 2 * 2 + 2
        # Verify bounds strictly in integer arithmetic
        while f_lo > 2 and check.sigma(r, f_lo) >= S_min:
            f_lo -= 2
        while pow(r, f_hi) * check.sigma(r, f_hi) <= B_rem:
            f_hi += 2
        for f in range(f_lo, f_hi + 2, 2):
            if not check.allowed(r, f, ABS3):
                continue
            S = check.sigma(r, f)
            if S < S_min:
                continue
            if pow(r, f) * S > B_rem:
                break
            b = check.valuation(S, 3)
            S3 = S // (3**b)
            for idx, m in enumerate(mod_s):
                if S < min_q[idx]:
                    break
                w0 = (-S3) % m
                if w0 == 0:
                    w0 = m
                check.require((3**b) * w0 * min_q[idx] > S,
                              f"Congruence killer failed for r={r}, f={f}, s={s_min+idx}!")
    return True

def verify_forest(fcert, abs_set, strip_pool, prime_fn):
    """Verify ordinary-only Static Prime Forest and return (G_forest_lo_nats, max_ab_hi, res_small_ab_hi, U_no3)."""
    roots = fcert["roots"]
    edges = fcert["edges"]
    cut_even = {int(k): int(v) for k, v in fcert["cut_even"].items()}

    U = {3}
    children = {}
    for r in roots:
        check.require(type(r) is int and r > 3 and r not in abs_set and r not in strip_pool and prime_fn(r), f"bad root {r}")
        check.require(r not in U, f"dup root {r}")
        U.add(r)
        children[r] = []

    queue = list(roots)
    visited = set(roots)
    while queue:
        u = queue.pop(0)
        for t in edges.get(str(u), []):
            check.require(type(t) is int and t > 3 and t not in abs_set and t not in strip_pool and prime_fn(t), f"bad child {t}")
            check.require(t not in U, f"dup/cycle child {t}")
            U.add(t)
            visited.add(t)
            children[u].append(t)
            children[t] = []
            queue.append(t)
    for k in edges:
        check.require(int(k) in visited, f"orphan edge {k}")

    strip_all = U | set(strip_pool)
    # Track any small primes < 50000 dividing residuals R(r, f) (to bound residual abundance rigorously!)
    small_res_primes = set()

    memo_dp = {}
    def dp(r, min_m):
        key = (r, min_m)
        if key in memo_dp: return memo_dp[key]
        ce = cut_even[r]
        check.require(ce >= 2 and ce % 2 == 0, f"bad cut_even {r}")
        fe_tail = max(min_m, ce)
        if fe_tail % 2 == 1: fe_tail += 1
        # Monotone tail net cost: fe*ln_lo(r) - ALPHA_HI * (ln_hi(fe+1)/LN3_LO) if r%3==1
        # Check monotonicity: derivative wrt f is ln(r) - 4/(f+1) > 0 since r >= 5 => ln(5)=1.609 and for r%3==1, r>=43 => ln(43)=3.76 > 4/3!
        v3_tail_hi = (ln_hi(fe_tail + 1) / LN3_LO) if r % 3 == 1 else Decimal(0)
        best = Decimal(fe_tail) * ln_lo(r) - ALPHA_HI * v3_tail_hi

        f_start = min_m if min_m % 2 == 0 else min_m + 1
        for f in range(f_start, ce, 2):
            if not check.allowed(r, f, abs_set):
                continue
            s = check.sigma(r, f)
            while s % 2 == 0: s //= 2
            v3 = check.valuation(s, 3)
            rem = s
            for u in strip_all:
                if rem % u == 0:
                    while rem % u == 0: rem //= u
            # Compute strictly valid NET contribution of residual `rem` (accounting for possible v_3-suppliers dividing rem!)
            net_rem_lo = Decimal(0)
            if rem > 1:
                tmp = rem
                for q in SMALL_P_50K:
                    if q * q > tmp: break
                    if tmp % q == 0:
                        vq = 0
                        while tmp % q == 0:
                            tmp //= q
                            vq += 1
                        if q % 3 == 2 or (vq == 1 and q >= 81):
                            net_rem_lo += Decimal(vq) * ln_lo(q)
                        else:
                            # q == 1 (mod 3) and (vq >= 2 or q < 81); q >= 43 since ABS3 = {7,11,13,19,31}
                            net_rem_lo += Decimal(vq) * (ln_lo(q) - Decimal(2) * LN3_HI)
                if tmp > 1:
                    if tmp < 50000:
                        if tmp % 3 == 2 or tmp >= 81:
                            net_rem_lo += ln_lo(tmp)
                        else:
                            net_rem_lo += ln_lo(tmp) - Decimal(2) * LN3_HI
                    else:
                        # All prime factors of tmp are >= 50000
                        net_factor_50k = Decimal(1) - (Decimal(2) * LN3_HI) / ln_lo(50000)
                        net_rem_lo += net_factor_50k * ln_lo(tmp)

            cur = Decimal(f) * ln_lo(r) - ALPHA_HI * Decimal(v3) + net_rem_lo
            for ch in children[r]:
                if s % ch == 0:
                    cur += dp(ch, check.valuation(s, ch))
            if cur < best:
                best = cur
        memo_dp[key] = best
        return best

    G_lo = sum(dp(r, 2) for r in roots)

    # Exact upper bound on max path abundance (forest nodes + small primes < 50000 in realized residuals)
    memo_ab = {}
    def max_ab(r):
        if r in memo_ab: return memo_ab[r]
        best_ch = Decimal(0)
        for f in range(2, cut_even[r], 2):
            if not check.allowed(r, f, abs_set): continue
            s = check.sigma(r, f)
            while s % 2 == 0: s //= 2
            tot_ch = Decimal(0)
            if strip_pool:
                rem = s
                for u in strip_all:
                    if rem % u == 0:
                        while rem % u == 0: rem //= u
                if rem > 1:
                    tmp = rem
                    for q in SMALL_P_50K:
                        if q * q > tmp: break
                        if tmp % q == 0:
                            tot_ch += ln_hi(q) - ln_lo(q - 1)
                            while tmp % q == 0: tmp //= q
                    if 1 < tmp < 50000:
                        tot_ch += ln_hi(tmp) - ln_lo(tmp - 1)
            for ch in children[r]:
                if s % ch == 0:
                    tot_ch += max_ab(ch)
            if tot_ch > best_ch:
                best_ch = tot_ch
        memo_ab[r] = (ln_hi(r) - ln_lo(r - 1)) + best_ch
        return memo_ab[r]

    ab_hi = sum(max_ab(r) for r in roots)
    # Remaining residual primes are strictly >= 50000 (and ordinary, since q_Euler > 10^500),
    # so their combined abundance is at most [ln(50000/49999) / (2*ln(50000))] * 2400*ln(10).
    res_ab_hi = Decimal(0)
    if strip_pool:
        res_ab_hi = ((ln_hi(50000) - ln_lo(49999)) / (Decimal(2) * ln_lo(50000))) * TARGET_NATS_HI

    return G_lo, ab_hi, res_ab_hi, U - {3}

def verify_lp_dual(lp_cert, abs_set, U_forest, required_ab_lo):
    """Independently verify exact rational dual of the net-cost LP on N_other using 50-digit outward-rounded Decimal."""
    P = lp_cert["P"]
    P_set = set(P)
    L = lp_cert["L"]
    check.require(P_set.isdisjoint(abs_set), "LP pool overlaps absent")
    check.require(P_set.isdisjoint(U_forest), "LP pool overlaps U_forest")
    check.require(3 not in P_set, "3 in LP pool")
    # Verify L is the smallest prime > 3 outside P_set | abs_set | U_forest
    excl = P_set | abs_set | U_forest | {2, 3}
    true_L = next(q for q in SMALL_P_50K if q not in excl)
    check.require(L == true_L, f"LP L={L} != true_L={true_L}")

    # Upper bound on external abundance-to-net-cost ratio for primes >= L
    c_ord_net_hi = (ln_hi(L) - ln_lo(L - 1)) / (Decimal(2) * (ln_lo(L) - Decimal(2) * LN3_HI))

    # Load non-negative dual multipliers as exact Fractions -> Decimal
    sel_lam = {int(k): frac_dec(v[0], v[1]) for k, v in lp_cert["sel_dual"].items()}
    for r, v in sel_lam.items():
        check.require(v >= 0 and r in P_set, "bad sel_dual")
    lam_ab = frac_dec(lp_cert["ab_dual"][0], lp_cert["ab_dual"][1])
    lam_u = frac_dec(lp_cert["u_dual"][0], lp_cert["u_dual"][1])
    check.require(lam_ab >= 0 and lam_u >= 0, "negative ab/u dual")

    # Organize inflow duals: (r_src, f_src) -> list of (t, v, lam_val) and t -> list of (v, lam_val)
    inf_pos = {} # (r_src, f_src) -> sum of lam_val
    inf_neg = {} # t -> list of (v, lam_val)
    for r_src, f_src, t, v, num, den in lp_cert["inf_dual"]:
        lv = frac_dec(num, den)
        check.require(lv >= 0 and r_src in P_set and t in P_set, "bad inf_dual")
        # Verify S(r_src, f_src) actually has v_t >= v!
        S_check = check.sigma(r_src, f_src)
        check.require(check.valuation(S_check, t) >= v, f"false inflow {r_src}^{f_src} -> {t}^{v}")
        inf_pos[(r_src, f_src)] = inf_pos.get((r_src, f_src), Decimal(0)) + lv
        inf_neg.setdefault(t, []).append((v, lv))

    # Check reduced cost of log_Next >= 0 (unbounded variable!):
    # c_Next + (-lam_ab * c_ord_net_hi) + (-lam_u) >= 0
    rc_next = Decimal(1) - lam_ab * c_ord_net_hi - lam_u
    check.require(rc_next >= 0, f"log_Next reduced cost negative: {rc_next}")

    # Check reduced cost of every variable x_{r, f} in [0, 1];
    # any slight negative reduced cost from rational rounding is rigorously penalized by min(0, rc) * 1!
    rc_penalty = Decimal(0)
    for r in P:
        fmax = 40 if r < 100 else (20 if r < 400 else 10)
        l_sel = sel_lam.get(r, Decimal(0))
        infs_for_r = inf_neg.get(r, [])
        for f in range(2, fmax + 1, 2):
            if not check.allowed(r, f, abs_set):
                continue
            S = check.sigma(r, f)
            v3 = check.valuation(S, 3)
            rem = S
            while rem % 2 == 0: rem //= 2
            while rem % 3 == 0: rem //= 3
            for t in P:
                if rem % t == 0:
                    while rem % t == 0: rem //= t
            for u in U_forest:
                if rem % u == 0:
                    while rem % u == 0: rem //= u
            cost_lo = Decimal(f) * ln_lo(r) - ALPHA_HI * Decimal(v3)
            # Upper bound on abundance log(S(r,f)/r^f) = ln(S) - f*ln(r)
            ab_hi = ln_hi(S) - Decimal(f) * ln_lo(r)
            u_lo = ((Decimal(1) - (Decimal(2) * LN3_HI) / ln_lo(L)) * ln_lo(rem)) if rem > 1 else Decimal(0)
            rc = cost_lo + l_sel - lam_ab * ab_hi + lam_u * u_lo + inf_pos.get((r, f), Decimal(0))
            for v_req, lv in infs_for_r:
                if f >= v_req:
                    rc -= lv
            if rc < 0:
                rc_penalty += rc # strictly negative adjustment (since x_{r,f} <= 1)

        # Tail variable for r
        fe = fmax + 2
        while not check.allowed(r, fe, abs_set): fe += 2
        v3_tail_hi = (ln_hi(fe + 1) / LN3_LO) if r % 3 == 1 else Decimal(0)
        cost_lo = Decimal(fe) * ln_lo(r) - ALPHA_HI * v3_tail_hi
        ab_hi = ln_hi(r) - ln_lo(r - 1)
        rc = cost_lo + l_sel - lam_ab * ab_hi
        for v_req, lv in infs_for_r:
            rc -= lv # tail covers all v_req!
        if rc < 0:
            rc_penalty += rc

    # Dual objective = -sum(sel_lam) + lam_ab * required_ab_lo + rc_penalty
    dual_obj_lo = -sum(sel_lam.values(), Decimal(0)) + lam_ab * required_ab_lo + rc_penalty
    return dual_obj_lo

def verify_partition(leaves, base_present, base_absent, split_primes):
    """Exhaustively verify that `leaves` cover every truth assignment to `split_primes`."""
    # For Cell 10: 4 split primes -> 16 assignments.
    # For Cell 11: 27 split primes -> check exact sequential decision-list structure!
    if len(split_primes) <= 10:
        for mask in range(1 << len(split_primes)):
            pres = set(base_present)
            abs_ = set(base_absent)
            for i, q in enumerate(split_primes):
                if (mask >> i) & 1: pres.add(q)
                else: abs_.add(q)
            covered = any(set(lf["present"]).issubset(pres) and set(lf["absent_extra"]).issubset(abs_) for lf in leaves)
            check.require(covered, f"Uncovered truth assignment mask={mask}")
    else:
        # Sequential decision list: leaf 0 is all-absent, leaf i+1 is split_primes[:i] absent & split_primes[i] present!
        neg = [lf for lf in leaves if set(lf["absent_extra"]) == set(split_primes) and set(lf["present"]) == set(base_present)]
        check.require(len(neg) == 1, "Missing negative leaf in sequential partition")
        for i, q in enumerate(split_primes):
            pos = [lf for lf in leaves if set(lf["absent_extra"]) == set(split_primes[:i]) and set(lf["present"]) == set(base_present) | {q}]
            check.require(len(pos) == 1, f"Missing positive leaf for {q} in sequential partition")
    return True

def main():
    t0 = time.time()
    cert_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("certs/P3_e1162_complete.json")
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    p, e = cert["p"], cert["e"]
    check.require(p == 3 and e == 1162, "Certificate is not for (3, 1162)")
    R_A = cert["R_A"]
    R_A_all = cert["R_A_all"]

    print(f"[1/6] Checking Pocklington primality certificates ({len(cert['primes'])} primes)...")
    prime_fn = check.primality_checker(cert["primes"])
    for k in cert["primes"]:
        check.require(prime_fn(int(k)), f"Pocklington failed for {k}")

    print(f"[2/6] Running deterministic trial division on A = S(3, 1162) up to R_A={R_A:,} (mod 3) and R_A_all={R_A_all:,} (all)...")
    verify_trial_division_A(R_A, R_A_all)

    print("[3/6] Verifying Euler cases E0, E1, E2 > 10^2400 and computing outward-rounded M_E3_lo...")
    lb_E0, lb_E1, lb_E2, M_E3a_lo, M_E3b_lo, s_min = verify_euler_bounds(e, R_A)
    M_E3_lo = min(M_E3a_lo, M_E3b_lo)
    gap_hi = (TARGET_NATS_HI - M_E3_lo) / LN10_LO
    print(f"      E0 >= {lb_E0/LN10_HI:.2f}d | E1 >= {lb_E1/LN10_HI:.2f}d | E2 >= {lb_E2/LN10_HI:.2f}d")
    print(f"      E3a >= {M_E3a_lo/LN10_HI:.2f}d | E3b >= {M_E3b_lo/LN10_HI:.2f}d | s_min = {s_min} | gap <= {gap_hi:.2f}d")

    print("[4/6] Checking exhaustive support partitions for Cell 10 and Cell 11...")
    verify_partition(cert["cell10"], [], [5], [17, 23, 29, 37, 41])
    ban27 = [17, 23, 29, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157]
    verify_partition(cert["cell11"], [5], [], ban27)

    # Collect all auxiliary primes across all forests and LP pools for disjointness check
    all_aux_primes = set()
    for lf in cert["cell10"] + cert["cell11"]:
        if lf["forest"]:
            all_aux_primes.update(lf["forest"]["roots"])
            for chs in lf["forest"]["edges"].values():
                all_aux_primes.update(chs)
        if lf["lp"]:
            all_aux_primes.update(lf["lp"]["P"])

    print(f"[5/6] Verifying disjointness from A, q, and Euler source r_source for {len(all_aux_primes)} auxiliary primes...")
    verify_not_euler_source(all_aux_primes, s_min, e)

    # Abundance upper bound for A (all prime factors > R_A_all = 10^8, at most 70 factors -> < 10^-6),
    # q (> 10^500 -> < 10^-500), and r_source in E3a (outside P U U_forest, so >= L -> ln(L/(L-1)) < 0.0005)!
    ab_A_q_hi = Decimal("1e-5")

    print(f"[6/6] Verifying all {len(cert['cell10'])} Cell 10 leaves and {len(cert['cell11'])} Cell 11 leaves...")
    min_total_digits = Decimal("1e9")
    for cell_name, leaves in [("Cell 10", cert["cell10"]), ("Cell 11", cert["cell11"])]:
        for lf in leaves:
            abs_set = ABS3 | set(lf["absent_extra"])
            strip_pool = lf["lp"]["P"] if lf["lp"] else []
            if lf["forest"]:
                G_lo, ab_f_hi, res_ab_hi, U_no3 = verify_forest(lf["forest"], abs_set, strip_pool, prime_fn)
                # Ensure every forest root is guaranteed present!
                check.require(set(lf["forest"]["roots"]).issubset(set(lf["present"])), f"root not in present in {lf['name']}")
            else:
                G_lo, ab_f_hi, res_ab_hi, U_no3 = Decimal(0), Decimal(0), Decimal(0), set()

            if lf["lp"]:
                L = lf["lp"]["L"]
                ab_rsrc_hi = ln_hi(L) - ln_lo(L - 1) # upper bound on abundance of r_source >= L
                req_ab_lo = LN43_LO - ab_f_hi - res_ab_hi - ab_A_q_hi - ab_rsrc_hi
                LP_lo = verify_lp_dual(lf["lp"], abs_set, U_no3, req_ab_lo)
            else:
                LP_lo = Decimal(0)

            tot_nats = M_E3_lo + G_lo + LP_lo
            tot_digits = tot_nats / LN10_HI
            if tot_digits < min_total_digits:
                min_total_digits = tot_digits
            check.require(tot_nats > TARGET_NATS_HI,
                          f"{lf['name']} FAILED: {tot_digits:.2f} <= 2400 (G={G_lo/LN10_HI:.2f}, LP={LP_lo/LN10_HI:.2f})")
            print(f"      PASS {lf['name']:24s}: E3({M_E3_lo/LN10_HI:.2f}) + Forest({G_lo/LN10_HI:.2f}) + LP_dual({LP_lo/LN10_HI:.2f}) = {tot_digits:.2f} > 2400")

    print(f"\nALL CHECKS PASSED! P3_I00193 ((p, e) = (3, 1162)) UNCONDITIONALLY EXCLUDED (min log10 N >= {min_total_digits:.2f} > 2400) in {time.time()-t0:.2f}s!")

if __name__ == "__main__":
    main()
