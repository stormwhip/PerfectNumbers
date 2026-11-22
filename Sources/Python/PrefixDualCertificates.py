#!/usr/bin/env python3
"""Generate affine dual lower-bound certificates for every root-prefix subset."""
import csv
import math
import sys

from IntervalCertificate import solve_and_certify

ROOTS = [19, 7, 11, 31, 13, 3, 5, 17]
P_MAX = 4000
A_CUT = 16

def generate(output_path):
    rows = []
    for mask in range(1 << len(ROOTS)):
        forbidden = {p for i, p in enumerate(ROOTS) if mask & (1 << i)}
        primal, certified, lam0, intercept = solve_and_certify(
            forbidden, P_max=P_MAX, a_cut=A_CUT,
            target_abund_ratio=2.0, certify=True, return_affine=True
        )
        if not all(math.isfinite(x) for x in (primal, certified, lam0, intercept)):
            raise RuntimeError(f"Non-finite dual certificate for mask {mask}")
        if lam0 < 0:
            raise RuntimeError(f"Negative abundance multiplier for mask {mask}")
        for ratio in (1.1, 1.25, 1.5, 2.0, 3.0):
            trial, _ = solve_and_certify(
                forbidden, P_max=P_MAX, a_cut=A_CUT,
                target_abund_ratio=ratio, certify=False
            )
            affine = intercept + lam0 * math.log(ratio)
            primal_natural = trial * math.log(10.0)
            if affine > primal_natural + 2e-7:
                raise RuntimeError(
                    f"Affine dual exceeds primal LP: mask={mask}, R={ratio}, "
                    f"dual={affine}, primal={primal_natural}"
                )
        rows.append((mask, lam0, intercept, certified))
        print(f"CERT mask={mask} lambda0={lam0:.17g} intercept={intercept:.17g} "
              f"baseLog10={certified:.12f}", flush=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(("mask", "lambda0_lower", "intercept_lower", "base_log10_lower"))
        writer.writerows(rows)
    print(f"COMPLETE certificates={len(rows)} output={output_path}", flush=True)

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "PrefixDualBounds.csv"
    generate(output)
