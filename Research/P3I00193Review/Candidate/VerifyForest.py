"""
Self-contained pure-integer verifier for Static Prime Forest certificates (Section 3.2).
Verifies that N > B = 10^2400 for (p, e) across all valid support cells of root p.
"""
import argparse
import json
import sys
from math import gcd, prod
from pathlib import Path
import check

CAP = check.B + 1

def cap_mul(a, b):
    p = a * b
    return CAP if p > CAP else p

def verify_forest_cell(cell_cert, p, e, pres, abs_, prime_fn):
    A = check.sigma(p, e)
    x0, d0, _, empty0 = check.node_state({p: e}, abs_)
    if cell_cert.get("kind") == "direct":
        check.require(empty0, "invalid direct cell")
        return True

    check.require(cell_cert.get("kind") == "forest", "expected forest or direct")
    roots = cell_cert["roots"]
    edges = cell_cert["edges"]          # dict: str(parent) -> list of int children
    cut_even = {int(k): int(v) for k, v in cell_cert["cut_even"].items()}
    cut_odd = {int(k): int(v) for k, v in cell_cert.get("cut_odd", {}).items()}

    # 1. Validate forest structure and primality
    U = {p}
    children = {}
    root_set = set()
    for r in roots:
        check.require(type(r) is int and r > 2 and r != p and r not in abs_ and prime_fn(r), f"invalid root {r}")
        check.require(r not in U, f"duplicate root {r}")
        check.require(r in pres or A % r == 0, f"unsupported root {r}")
        U.add(r)
        root_set.add(r)
        children[r] = []

    # BFS from roots to ensure tree/forest with unique parent, no cycles, and non-roots coprime to p*A
    queue = list(roots)
    visited = set(roots)
    while queue:
        u = queue.pop(0)
        chs = edges.get(str(u), [])
        for t in chs:
            check.require(type(t) is int and t > 2 and t not in abs_ and prime_fn(t), f"invalid child {t}")
            check.require(t not in U, f"duplicate or cyclic node {t}")
            check.require(A % t != 0, f"non-root node {t} divides A")
            U.add(t)
            visited.add(t)
            children[u].append(t)
            children[t] = []
            queue.append(t)

    # Ensure no orphan entries in edges
    for k in edges:
        check.require(int(k) in visited, f"orphan edge parent {k}")

    # 2. Strip root prime powers from A to get A_rem (coprime to all U)
    A_rem = A
    root_min_m = {}
    for r in roots:
        v = check.valuation(A_rem, r)
        if v > 0:
            A_rem //= r**v
        root_min_m[r] = max(1, v)
    # Double-check gcd(A_rem, prod(U)) == 1
    for u in U:
        check.require(A_rem % u != 0, f"A_rem divisible by {u}")

    base = cap_mul(pow(p, e), A_rem)

    # 3. Bottom-up exact-integer DP (memoized on (r, min_m))
    memo = {}
    def dp(r, min_m):
        key = (r, min_m)
        if key in memo:
            return memo[key]
        ce = cut_even[r]
        check.require(ce >= 2 and ce % 2 == 0, f"invalid cut_even for {r}")
        # Tail for even exponents: smallest even f >= max(min_m, ce)
        # Note: even if that f is not allowed by abs_, r^f is a valid monotone lower bound for all allowed even f >= f!
        fe_tail = max(min_m, ce)
        if fe_tail % 2 == 1:
            fe_tail += 1
        best_ord = CAP if fe_tail * r.bit_length() > 9000 else min(CAP, pow(r, fe_tail))
        best_eul = best_ord

        f_start = min_m if min_m % 2 == 0 else min_m + 1
        for f in range(f_start, ce, 2):
            if not check.allowed(r, f, abs_):
                continue
            s = check.sigma(r, f)
            while s % 2 == 0:
                s //= 2
            # Compute activated children and residual R(r, f) cleared of all U
            rem = s
            for u in U:
                if rem % u == 0:
                    while rem % u == 0:
                        rem //= u
            rf_val = CAP if f * r.bit_length() > 9000 else min(CAP, pow(r, f))
            prod_ord = cap_mul(rf_val, min(CAP, rem))
            child_pairs = []
            for ch in children[r]:
                if s % ch == 0:
                    vm = check.valuation(s, ch)
                    c_ord, c_eul = dp(ch, vm)
                    prod_ord = cap_mul(prod_ord, c_ord)
                    child_pairs.append((c_ord, c_eul))
            if prod_ord < best_ord:
                best_ord = prod_ord
            if prod_ord < best_eul:
                best_eul = prod_ord
            # Try giving Euler to one activated child
            for i in range(len(child_pairs)):
                cand = cap_mul(rf_val, min(CAP, rem))
                for j, (c_ord, c_eul) in enumerate(child_pairs):
                    cand = cap_mul(cand, c_eul if j == i else c_ord)
                if cand < best_eul:
                    best_eul = cand

        # Odd exponents if r % 4 == 1
        if r % 4 == 1:
            co = cut_odd[r]
            check.require(co >= 1 and co % 4 == 1, f"invalid cut_odd for {r}")
            fo_tail = max(min_m, co)
            while fo_tail % 4 != 1:
                fo_tail += 1
            tail_o = CAP if fo_tail * r.bit_length() > 9000 else min(CAP, pow(r, fo_tail))
            if tail_o < best_eul:
                best_eul = tail_o
            f_start_o = min_m
            while f_start_o % 4 != 1:
                f_start_o += 1
            for f in range(f_start_o, co, 4):
                if not check.allowed(r, f, abs_):
                    continue
                s = check.sigma(r, f)
                while s % 2 == 0:
                    s //= 2
                rem = s
                for u in U:
                    if rem % u == 0:
                        while rem % u == 0:
                            rem //= u
                rf_val = CAP if f * r.bit_length() > 9000 else min(CAP, pow(r, f))
                prod_o = cap_mul(rf_val, min(CAP, rem))
                for ch in children[r]:
                    if s % ch == 0:
                        vm = check.valuation(s, ch)
                        c_ord, _ = dp(ch, vm)
                        prod_o = cap_mul(prod_o, c_ord)
                if prod_o < best_eul:
                    best_eul = prod_o

        memo[key] = (best_ord, best_eul)
        return memo[key]

    # 4. Merge roots: at most one root uses Euler
    root_pairs = [dp(r, root_min_m[r]) for r in roots]
    best_total = base
    for c_ord, _ in root_pairs:
        best_total = cap_mul(best_total, c_ord)
    for i in range(len(root_pairs)):
        cand = base
        for j, (c_ord, c_eul) in enumerate(root_pairs):
            cand = cap_mul(cand, c_eul if j == i else c_ord)
        if cand < best_total:
            best_total = cand

    check.require(best_total > check.B, f"forest lower bound <= B (got {best_total.bit_length()*0.30103:.2f} digits)")
    return True

def verify_forest_cert(cert, pairs):
    p, e = cert["p"], cert["e"]
    check.require(type(p) is type(e) is int and e % 2 == 0, "invalid (p, e)")
    cells = check.support_cells(p)
    check.require(cert["cells"].keys() == cells.keys(), "support cells not exhaustive")
    prime_fn = check.primality_checker(cert.get("primes", {}))
    for name, (pres, abs_) in cells.items():
        verify_forest_cell(cert["cells"][name], p, e, pres, abs_, prime_fn)
    # Return all covered open pairs: (p, e) plus any (p, f) with (e+1) | (f+1) if transferable
    covered = set()
    if (p, e) in pairs:
        covered.add((p, e))
    if cert.get("transferable", False):
        # Static prime forest only uses p^e * S(p, e), divisibility by S(p, e), F_p, and support cells,
        # so it transfers to every even f with (e+1) | (f+1)!
        for pp, ff in pairs:
            if pp == p and ff % 2 == 0 and (ff + 1) % (e + 1) == 0:
                covered.add((pp, ff))
    return covered

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", type=Path,
                        default=Path(__file__).with_name("PerfectNumbers2400_Gemini_Standalone.md"))
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()
    rows, pairs = check.load_ledger(args.markdown)
    excluded = set()
    for path in args.files:
        cert = json.loads(path.read_text(encoding="utf-8"))
        cov = verify_forest_cert(cert, pairs)
        excluded |= cov
        print(f"PASS {path.name}: covers {sorted(cov)}")
    closed, left = check.project(rows, excluded)
    print(f"Total excluded pairs: {len(excluded)} / {len(pairs)}, closed shards: {len(closed)} / {len(rows)}")
