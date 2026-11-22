import math
from sympy import primerange, factorint
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

# Ochem & Rao (2012) 的 15 个禁用素数
S_2012 = {127, 19, 7, 11, 331, 31, 97, 61, 13, 398581, 1093, 3, 5, 307, 17}

def has_forbidden_factor(p, a, S):
    """快速判断 sigma(p^a) 是否有 S 中的素因子（无需分解）"""
    for s in S:
        if p % s == 1:
            if (a + 1) % s == 0:
                return True
        else:
            if pow(p, a + 1, s) == 1:
                return True
    return False

def ln_sigma_m1(p, a):
    """精确计算 ln(sigma_{-1}(p^a)) = ln(p/(p-1)) + ln(1 - p^{-(a+1)})"""
    return math.log(p / (p - 1)) + math.log1p(-p ** (-(a + 1)))

def build_and_solve_lp(S, P_max=4000, a_cut=16, use_implications=True, factor_limit=10**14):
    base_primes = [p for p in primerange(3, P_max + 1) if p not in S]
    explicit_primes = set(base_primes)

    # 1. 对基础池中的小素数生成合法 (p, a) 选项，并收集二次因子
    # options[p] = list of (a, is_spec, cost, abund, is_tail_a)
    options = {}
    implications = []  # (p, a, is_spec, q, k)

    def gen_options_for_prime(p, do_factor=False):
        opts = []
        # 合法偶数幂次
        for a in range(2, a_cut, 2):
            if not has_forbidden_factor(p, a, S):
                opts.append((a, False, a * math.log(p), ln_sigma_m1(p, a), False))
                if do_factor and p ** a < factor_limit:
                    val = (p ** (a + 1) - 1) // (p - 1)
                    for q, k in factorint(val).items():
                        if q > 2:
                            explicit_primes.add(q)
                            implications.append((p, a, False, q, k))
        # 偶数高次幂打包项 (a >= a_cut)
        opts.append((a_cut, False, a_cut * math.log(p), math.log(p / (p - 1)), True))

        # 若 p == 1 (mod 4)，枚举合法特殊幂次 a == 1 (mod 4)
        if p % 4 == 1:
            for a in range(1, a_cut, 4):
                if not has_forbidden_factor(p, a, S):
                    opts.append((a, True, a * math.log(p), ln_sigma_m1(p, a), False))
                    if do_factor and p ** a < factor_limit:
                        val = (p ** (a + 1) - 1) // (p - 1)
                        for q, k in factorint(val).items():
                            if q > 2:
                                explicit_primes.add(q)
                                implications.append((p, a, True, q, k))
            a_spec_cut = a_cut + ((1 - a_cut) % 4)
            opts.append((a_spec_cut, True, a_spec_cut * math.log(p), math.log(p / (p - 1)), True))
        return opts

    for p in base_primes:
        options[p] = gen_options_for_prime(p, do_factor=use_implications)

    # 为外溢的二次素因子 q > P_max 生成选项（不再递归分解）
    for q in list(explicit_primes):
        if q not in options:
            options[q] = gen_options_for_prime(q, do_factor=False)

    # 2. 编排 LP 变量索引
    var_idx = {}
    c = []
    bounds = []
    for p in sorted(explicit_primes):
        for idx_in_p, (a, is_spec, cost, abund, is_tail_a) in enumerate(options[p]):
            vid = len(c)
            var_idx[(p, a, is_spec, is_tail_a)] = vid
            c.append(cost)
            bounds.append((0.0, 1.0))

    # 非特殊尾素数聚合变量 y_tail >= 0
    eta_tail = math.log(P_max / (P_max - 1)) / (2.0 * math.log(P_max))
    vid_y_tail = len(c)
    c.append(1.0 / eta_tail)
    bounds.append((0.0, None))

    # 特殊尾素数聚合变量 x_tail_spec in [0, 1]
    vid_x_tail_spec = len(c)
    c.append(math.log(P_max))
    bounds.append((0.0, 1.0))

    n_vars = len(c)
    num_primes = len(explicit_primes)
    num_imp = len(implications) if use_implications else 0
    # 约束总数：丰度(1) + 唯一特殊素数(1) + 每素数互斥(num_primes) + 蕴含约束(num_imp)
    n_rows = 2 + num_primes + num_imp
    A_ub = lil_matrix((n_rows, n_vars), dtype=float)
    b_ub = [0.0] * n_rows

    # 约束 0: -abundancy <= -ln(2)
    for p in explicit_primes:
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            A_ub[0, var_idx[(p, a, is_spec, is_tail_a)]] = -abund
    A_ub[0, vid_y_tail] = -1.0
    A_ub[0, vid_x_tail_spec] = -math.log(P_max / (P_max - 1))
    b_ub[0] = -math.log(2.0)

    # 约束 1: 唯一特殊素数 <= 1
    for p in explicit_primes:
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            if is_spec:
                A_ub[1, var_idx[(p, a, is_spec, is_tail_a)]] = 1.0
    A_ub[1, vid_x_tail_spec] = 1.0
    b_ub[1] = 1.0

    # 约束 2..: 每个素数至多选一个幂次 <= 1
    row = 2
    for p in sorted(explicit_primes):
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            A_ub[row, var_idx[(p, a, is_spec, is_tail_a)]] = 1.0
        b_ub[row] = 1.0
        row += 1

    # 二次因子蕴含约束: x_{p,a} - sum_{b >= k} x_{q,b} <= 0
    if use_implications:
        for (p, a, is_spec, q, k) in implications:
            A_ub[row, var_idx[(p, a, is_spec, False)]] = 1.0
            for (b, q_spec, _, _, q_tail) in options[q]:
                if is_spec and q_spec:
                    continue  # p 已占特殊素数，q 只能取偶次幂
                if q_tail or b >= k:
                    A_ub[row, var_idx[(q, b, q_spec, q_tail)]] = -1.0
            b_ub[row] = 0.0
            row += 1

    res = linprog(c, A_ub=A_ub.tocsc(), b_ub=b_ub, bounds=bounds, method="highs")
    assert res.success, f"LP failed: {res.message}"
    return res.fun / math.log(10)  # 返回 log10(N) 下界

if __name__ == "__main__":
    exp_A = build_and_solve_lp(S_2012, P_max=4000, use_implications=False)
    exp_B = build_and_solve_lp(S_2012, P_max=4000, use_implications=True)
    print(f"Ochem-Rao (2012) 原始贪心法 (15 primes):  10^1735")
    print(f"Model A (唯一特殊素数 + 精确丰度):         10^{exp_A:.2f}")
    print(f"Model B (+ 二次因子蕴含约束):              10^{exp_B:.2f}")