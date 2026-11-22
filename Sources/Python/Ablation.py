import math
import time
from concurrent.futures import ProcessPoolExecutor
from sympy import primerange, factorint
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

S_2012 = {127, 19, 7, 11, 331, 31, 97, 61, 13, 398581, 1093, 3, 5, 307, 17}
S_BCR = {127, 19, 7, 11, 31, 13, 3, 5}

def has_forbidden_factor(p, a, S):
    for s in S:
        if p % s == 1:
            if (a + 1) % s == 0:
                return True
        else:
            if pow(p, a + 1, s) == 1:
                return True
    return False

def ln_sigma_m1(p, a):
    return math.log(p / (p - 1)) + math.log1p(-p ** (-(a + 1)))

def solve_lp_core(
    forbidden_S,
    existing_E=frozenset(),
    min_p=3,
    target_abund_ratio=2.0,
    allow_special=True,
    P_max=4000,
    a_cut=16,
    factor_limit=10**14,
):
    """
    通用严格 LP 下界求解器：
    - forbidden_S: 绝对禁止出现在 N 中的素数（sigma(p^a) 也不得含其中因子）
    - existing_E:  已在 M 中的素数（不再作为新素数选择，但 sigma(p^a) 含其中因子不违禁、不计额外代价）
    - min_p:       新素数的下界（所有 < min_p 且不在 existing_E 中的奇素数自动并入禁用集）
    """
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
                opts.append((a, False, a * math.log(p), ln_sigma_m1(p, a), False))
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
                    opts.append((a, True, a * math.log(p), ln_sigma_m1(p, a), False))
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

    var_idx = {}
    c, bounds = [], []
    for p in sorted(explicit_primes):
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            var_idx[(p, a, is_spec, is_tail_a)] = len(c)
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

    # 约束 0: 丰度达标
    for p in explicit_primes:
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            A_ub[0, var_idx[(p, a, is_spec, is_tail_a)]] = -abund
    A_ub[0, vid_y_tail] = -1.0
    if allow_special:
        A_ub[0, vid_x_tail_spec] = -math.log(P_max / (P_max - 1))
    b_ub[0] = -math.log(target_abund_ratio)

    row = 1
    # 约束 1: 唯一特殊素数
    if allow_special:
        for p in explicit_primes:
            for (a, is_spec, cost, abund, is_tail_a) in options[p]:
                if is_spec:
                    A_ub[row, var_idx[(p, a, is_spec, is_tail_a)]] = 1.0
        A_ub[row, vid_x_tail_spec] = 1.0
        b_ub[row] = 1.0
        row += 1

    # 每素数单幂次互斥
    for p in sorted(explicit_primes):
        for (a, is_spec, cost, abund, is_tail_a) in options[p]:
            A_ub[row, var_idx[(p, a, is_spec, is_tail_a)]] = 1.0
        b_ub[row] = 1.0
        row += 1

    # 二次因子蕴含约束
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
    return res.fun / math.log(10)

def _worker_endgame(args):
    label, S = args
    val = solve_lp_core(S, P_max=4000, a_cut=16)
    return (label, len(S), val)

def _worker_roadblock2(p):
    # 论文图 1 Roadblock 2: M' > 10^814, a' = 1.92522, 目标 10^1500 (剩余需 > 10^686)
    E = {3, 7, 13, 19, 127}
    val = solve_lp_core(
        forbidden_S=set(),
        existing_E=E,
        min_p=p,
        target_abund_ratio=2.0 / 1.92522,
        allow_special=False,  # 13^1 已占用唯一特殊素数
        P_max=max(4000, p * 4),
        a_cut=16,
    )
    return (p, val)

if __name__ == "__main__":
    t0 = time.time()

    # 任务 1：极小 S 消融（BCR 8素数 + S_2012 逐个留一法）
    endgame_tasks = [("S_BCR (8 primes)", S_BCR)]
    for s in sorted(S_2012):
        endgame_tasks.append((f"S_2012 \\ {{{s}}}", S_2012 - {s}))

    # 任务 2：Roadblock 2 候选最小素数 p 扫描（论文需枚举到 b = 2625）
    rb2_candidates = [5, 11, 17, 23, 29, 37, 43, 53, 67, 83, 101, 131, 167, 211, 307, 503]

    with ProcessPoolExecutor() as ex:
        fut_eg = [ex.submit(_worker_endgame, t) for t in endgame_tasks]
        fut_rb = [ex.submit(_worker_roadblock2, p) for p in rb2_candidates]

        eg_results = [f.result() for f in fut_eg]
        rb_results = [f.result() for f in fut_rb]

    print("=== 实验 1：终局下界消融 (基准 S_2012 = 10^3129.46) ===")
    for label, sz, val in sorted(eg_results, key=lambda x: -x[2]):
        print(f"  {label:<22} (|S|={sz:2d}) -> 10^{val:.2f}")

    print("\n=== 实验 2：Roadblock 2 实测 (论文 b = 2625, 剩余阈值 10^686) ===")
    for p, val in rb_results:
        flag = "  <-- 已超 10^686，无需再枚举 >= p !" if val > 686.0 else ""
        print(f"  min_p = {p:4d} -> 剩余规模下界 10^{val:7.2f}{flag}")

    print(f"\n总耗时: {time.time() - t0:.2f}s")