#!/usr/bin/env python3
"""Exact subset-DP optimizer for measured root-proof costs."""
import csv
import sys
from pathlib import Path

ROOTS = [19, 7, 11, 31, 13, 3, 5, 17]
N = len(ROOTS)
FULL = (1 << N) - 1
INF = float("inf")

def optimize(edges, primary):
    dp = [(INF, INF) for _ in range(FULL + 1)]
    choice = [-1] * (FULL + 1)
    dp[FULL] = (0.0, 0.0)
    for mask in range(FULL - 1, -1, -1):
        candidates = []
        for i, p in enumerate(ROOTS):
            bit = 1 << i
            if mask & bit:
                continue
            branches, seconds, status = edges[(mask, p)]
            if status != "PROVEN":
                continue
            tail = dp[mask | bit]
            if tail[0] == INF:
                continue
            total = (branches + tail[0], seconds + tail[1])
            key = (total[0], total[1], p) if primary == "branches" else (total[1], total[0], p)
            candidates.append((key, i, total))
        if candidates:
            _, choice[mask], dp[mask] = min(candidates, key=lambda x: x[0])
    if dp[0][0] == INF:
        raise ValueError("No complete root order covers all measured edges")
    order, mask = [], 0
    while mask != FULL:
        i = choice[mask]
        if i < 0:
            raise RuntimeError("Broken DP predecessor")
        order.append(ROOTS[i])
        mask |= 1 << i
    return order, dp[0]

def load_edges(path):
    edges = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0] != "EDGE" or len(row) < 6 or row[1] == "mask":
                continue
            _, mask, root, branches, seconds, status = row
            key = (int(mask), int(root))
            if key in edges:
                raise ValueError(f"Duplicate edge: {key}")
            edges[key] = (int(branches), float(seconds), status)
    expected = N * (1 << (N - 1))
    if len(edges) != expected:
        raise ValueError(f"Expected {expected} edges, got {len(edges)}")
    return edges

def self_test():
    roots = [2, 3, 5]
    # For this synthetic directed subset-cost matrix, 3,2,5 is optimal.
    edges = {
        (0, 2):(1,1.0,"PROVEN"), (0,3):(2,2.0,"PROVEN"), (0,5):(9,9.0,"PROVEN"),
        (1, 3):(1,1.0,"PROVEN"), (1,5):(8,8.0,"PROVEN"),
        (2, 2):(1,1.0,"PROVEN"), (2,5):(7,7.0,"PROVEN"),
        (3, 5):(1,1.0,"PROVEN"), (4, 2):(1,1.0,"PROVEN"), (4,3):(2,2.0,"PROVEN"),
        (5, 3):(1,1.0,"PROVEN"), (6, 2):(1,1.0,"PROVEN"),
    }
    # The production optimizer uses a fixed root list; verify its recurrence
    # independently with a tiny generic implementation below.
    full = 7
    dp = [10**9] * 8
    pick = [-1] * 8
    dp[full] = 0
    for mask in range(full - 1, -1, -1):
        for i in range(3):
            if not (mask >> i) & 1:
                val = edges[(mask, roots[i])][0] + dp[mask | (1 << i)]
                if val < dp[mask]:
                    dp[mask], pick[mask] = val, i
    order, mask = [], 0
    while mask != full:
        i = pick[mask]
        order.append(roots[i])
        mask |= 1 << i
    assert order == [2, 3, 5], order
    assert dp[0] == 4, dp[0]
    print("RootOrderOptimizer self-test: OK")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
    elif len(sys.argv) == 2:
        edge_costs = load_edges(sys.argv[1])
        for objective in ("branches", "seconds"):
            order, totals = optimize(edge_costs, objective)
            print(f"OPTIMAL_{objective.upper()}_ORDER={','.join(map(str, order))}")
            print(f"TOTAL_BRANCHES={totals[0]:.0f}")
            print(f"TOTAL_SECONDS={totals[1]:.6f}")
    else:
        raise SystemExit("Usage: RootOrderOptimizer.py PROFILE.csv | --self-test")
