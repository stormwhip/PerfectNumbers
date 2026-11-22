import math
import time
from sympy import primerange, factorint, nextprime
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from mpmath import iv

iv.dps = 30  # 30位十进制精度区间算术

S_2012 = {127, 19, 7, 11, 331, 31, 97, 61, 13, 398581, 1093, 3, 5, 307, 17}

def has_forbidden_factor(p, a, S):
    for s in S:
        if p % s == 1:
            if (a + 1) % s == 0:
                return True
        else:
            if pow(p, a + 1, s) == 1:
                return True
    return False

def ln_sigma_m1_float(p, a):
    return math.log(p / (p - 1)) + math.log1p(-p ** (-(a + 1)))

def ln_sigma_m1_iv(p, a):
    p_iv = iv.mpf(p)
    return iv.log(p_iv / (p_iv - 1)) + iv.log(1 - p_iv ** (-(a + 1)))

def solve_and_certify(
    forbidden_S,
    existing_E=frozenset(),
    min_p=3,
    target_abund_ratio=2.0,
    allow_special=True,
    P_max=4000,
    a_cut=16,
    factor_limit=10**14,
    certify=False,
    return_affine=False,
)
    eff_forbidden = set(forbidden_S)
    if min_p > 3:
        for q in primerange(3, min_p):
            if q not in existing_E:
                eff_forbidden.add(q)

    skip = eff_forbidden | set(existing_E)
    base_primes = [p for p in primerange(min_p, P_max + 1) if p not in skip]
    explicit_primes = set(base_primes)

    options = {}
    implications = []

    def gen_options(p, do_factor=False):
        opts = []
        for a in range(2, a_cut, 2):
            if not has_forbidden_factor(p, a, eff_forbidden):
                opts.append((a, False, a * math.log(p), ln_sigma_m1_float(p, a), False))
                if do_factor and p ** a < factor_limit:
                    val = (p ** (a + 1) - 1) // (p - 1)
                    for q, k in factorint(val).items():
                        if q > 2 and q not in existing_E:
                            explicit_primes.add(q)
                            implications.append((p, a, False, q, k))
        opts.append((a_cut, False, a_cut * math.log(p), math.log(p / (p - 1)), True))

        if allow_special and p % 4 == 1:
            for a in range(1, a_cut, 4):
                if not has_forbidden_factor(p, a, eff_forbidden):
                    opts.append((a, True, a * math.log(p), ln_sigma_m1_float(p, a), False))
                    if do_factor and p ** a < factor_limit:
                        val = (p ** (a + 1) - 1) // (p - 1)
                        for q, k in factorint(val).items():
                            if q > 2 and q not in existing_E:
                                explicit_primes.add(q)
                                implications.append((p, a, True, q, k))
            a_spec_cut = a_cut + ((1 - a_cut) % 4)
            opts.append((a_spec_cut, True, a_spec_cut * math.log(p), math.log(p / (p - 1)), True))
        return opts

    for p in base_primes:
        options[p] = gen_options(p, do_factor=True)
    for q in list(explicit_primes):
        if q not in options:
            options[q] = gen_options(q, do_factor=False)

    var_meta = []  # (p, a, is_spec, is_tail_a)
    var_idx = {}
    c, bounds = [], []
    for p in sorted(explicit_primes):
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            var_idx[(p, a, is_spec, is_tail_a)] = len(c)
            var_meta.append((p, a, is_spec, is_tail_a))
            c.append(cost)
            bounds.append((0.0, 1.0))

    eta_tail = math.log(P_max / (P_max - 1)) / (2.0 * math.log(P_max))
    vid_y_tail = len(c)
    c.append(1.0 / eta_tail)
    bounds.append((0.0, None))

    vid_x_tail_spec = None
    if allow_special:
        vid_x_tail_spec = len(c)
        c.append(math.log(P_max))
        bounds.append((0.0, 1.0))

    n_vars = len(c)
    n_rows = (2 if allow_special else 1) + len(explicit_primes) + len(implications)
    A_ub = lil_matrix((n_rows, n_vars), dtype=float)
    b_ub = [0.0] * n_rows

    # 约束 0: 丰度
    for p in explicit_primes:
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            A_ub[0, var_idx[(p, a, is_spec, is_tail_a)]] = -abund
    A_ub[0, vid_y_tail] = -1.0
    if allow_special:
        A_ub[0, vid_x_tail_spec] = -math.log(P_max / (P_max - 1))
    b_ub[0] = -math.log(target_abund_ratio)

    row = 1
    if allow_special:
        for p in explicit_primes:
            for (a, is_spec, cost, abund, is_tail_a) in options[p]:
                if is_spec:
                    A_ub[row, var_idx[(p, a, is_spec, is_tail_a)]] = 1.0
        A_ub[row, vid_x_tail_spec] = 1.0
        b_ub[row] = 1.0
        row += 1

    prime_rows = {}
    for p in sorted(explicit_primes):
        prime_rows[p] = row
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            A_ub[row, var_idx[(p, a, is_spec, is_tail_a)]] = 1.0
        b_ub[row] = 1.0
        row += 1

    imp_start_row = row
    for (p, a, is_spec, q, k) in implications:
        A_ub[row, var_idx[(p, a, is_spec, False)]] = 1.0
        for (b, q_spec, _, _, q_tail) in options[q]:
            if is_spec and q_spec:
                continue
            if q_tail or b >= k:
                A_ub[row, var_idx[(q, b, q_spec, q_tail)]] = -1.0
        b_ub[row] = 0.0
        row += 1

    res = linprog(c, A_ub=A_ub.tocsc(), b_ub=b_ub, bounds=bounds, method="highs")
    assert res.success, f"LP failed: {res.message}"
    float_bound = res.fun / math.log(10)

    if not certify:
        if return_affine:
            raise ValueError("return_affine requires certify=True")
        return float_bound, None

    # --- 严格区间算术对偶校验 ---
    # 提取非负对偶变量 lambda = max(0, -marginals)
    lam = [iv.mpf(max(0.0, float(-m))) for m in res.ineqlin.marginals]

    # 严格截断 lam[0] <= c_tail.a，保证 y_tail 的检验数 >= 0
    P_iv = iv.mpf(P_max)
    c_tail_iv = (2 * iv.log(P_iv)) / iv.log(P_iv / (P_iv - 1))
    if lam[0].b > c_tail_iv.a:
        lam[0] = iv.mpf(c_tail_iv.a)

    # 累加 A^T * lam 到每个有界变量（u_i = 1）
    AT_lam = [iv.mpf(0)] * len(var_meta)
    for vid, (p, a, is_spec, is_tail_a) in enumerate(var_meta):
        p_iv = iv.mpf(p)
        abund_iv = iv.log(p_iv / (p_iv - 1)) if is_tail_a else ln_sigma_m1_iv(p, a)
        AT_lam[vid] -= lam[0] * abund_iv
        if allow_special and is_spec:
            AT_lam[vid] += lam[1]
        AT_lam[vid] += lam[prime_rows[p]]

    for idx, (p, a, is_spec, q, k) in enumerate(implications):
        l_imp = lam[imp_start_row + idx]
        if l_imp == 0:
            continue
        AT_lam[var_idx[(p, a, is_spec, False)]] += l_imp
        for (b, q_spec, _, _, q_tail) in options[q]:
            if is_spec and q_spec:
                continue
            if q_tail or b >= k:
                AT_lam[var_idx[(q, b, q_spec, q_tail)]] -= l_imp

    # 计算 -lam^T b_ub
    dual_obj = lam[0] * iv.log(iv.mpf(target_abund_ratio))
    if allow_special:
        dual_obj -= lam[1]
    for p in explicit_primes:
        dual_obj -= lam[prime_rows[p]]

    # 加上有界变量的负检验数惩罚 sum min(0, c_i + (A^T lam)_i)
    for vid, (p, a, is_spec, is_tail_a) in enumerate(var_meta):
        c_iv = iv.mpf(a) * iv.log(iv.mpf(p))
        rc_low = (c_iv + AT_lam[vid]).a
        if rc_low < 0:
            dual_obj += iv.mpf(rc_low)

    if allow_special:
        rc_spec_low = (iv.log(P_iv) - lam[0] * iv.log(P_iv / (P_iv - 1)) + lam[1]).a
        if rc_spec_low < 0:
            dual_obj += iv.mpf(rc_spec_low)

    rigorous_log10 = float((dual_obj / iv.log(iv.mpf(10))).a)
    if return_affine:
        # The constraint matrix is independent of the abundance RHS.
        # This same dual remains feasible for every target ratio R > 1.
        intercept_iv = dual_obj - lam[0] * iv.log(iv.mpf(target_abund_ratio))
        lambda0_lower = max(0.0, math.nextafter(float(lam[0].a), -math.inf))
        intercept_lower = math.nextafter(float(intercept_iv.a), -math.inf)
        return float_bound, rigorous_log10, lambda0_lower, intercept_lower
    return float_bound, rigorous_log10

if __name__ == "__main__":
    t0 = time.time()
    print("=== 1. 严格对偶证书校验 (S_2012, P_max=4000) ===")
    f_val, r_val = solve_and_certify(S_2012, P_max=4000, a_cut=16, certify=True)
    print(f"  浮点 LP 解:       10^{f_val:.6f}")
    print(f"  严格区间对偶下界: 10^{r_val:.6f}  (差值: {f_val - r_val:.2e})")

    print("\n=== 2. Roadblock 2 精确二分临界 b (目标剩余 > 10^686) ===")
    E = {3, 7, 13, 19, 127}
    primes = [p for p in primerange(500, 1500) if p not in E]
    lo, hi = 0, len(primes) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        p = primes[mid]
        val, _ = solve_and_certify(
            forbidden_S=set(), existing_E=E, min_p=p,
            target_abund_ratio=2.0 / 1.92522, allow_special=False,
            P_max=max(4000, p * 4), a_cut=16, certify=False
        )
        print(f"  测试 p = {p:4d} -> 剩余下界 10^{val:.2f}")
        if val > 686.0:
            hi = mid
        else:
            lo = mid + 1
    p_crit = primes[lo]
    print(f"  => Roadblock 2 临界素数 p = {p_crit}（仅需分支 < {p_crit} 的素数，原论文为 < 2625）")
    print(f"\n总耗时: {time.time() - t0:.2f}s")