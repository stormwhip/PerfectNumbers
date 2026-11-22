#!/usr/bin/env python3
"""Genuine LP prefix certificates for all eight 2400 root masks; 247 trivial safe others.

This is an inexpensive pilot for performance, not the full 256-mask proof.
"""
import csv
import sys
from pathlib import Path
from IntervalCertificate61 import solve_and_certify

ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
MASKS = (0, 1, 3, 7, 15, 31, 63, 127, 255)

def generate(output):
    rows = [(mask, 0.0, 0.0, 0.0) for mask in range(256)]
    removal, forced = [], []
    for mask in MASKS:
        forbidden = {q for i, q in enumerate(ROOTS) if mask & (1 << i)}
        primal, lower, slope, intercept, rg, fg = solve_and_certify(
            forbidden, P_max=4000, a_cut=16, certify=True,
            return_affine=True, return_forced_gains=True)
        rows[mask] = (mask, slope, intercept, lower)
        removal.extend((mask, q, gain) for q, gain in sorted(rg.items()) if gain > 0)
        forced.extend((mask, q, gain) for q, gain in sorted(fg.items()) if gain > 0)
        print(f"PREFIX mask={mask} lower={lower:.12f} "
              f"removed={len(rg)} forced={len(fg)}", flush=True)
    if rows[255][3] <= 2400:
        raise ArithmeticError("Terminating eight-prime LP bound below 2400")
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    for dest, header, data in (
        (p, ("mask","lambda0_lower","intercept_lower","base_log10_lower"), rows),
        (p.with_name("PrefixDualVariableGains.csv"), ("mask","prime","gain_lower"), removal),
        (p.with_name("PrefixDualForcedGains.csv"), ("mask","prime","gain_lower"), forced),
    ):
        with dest.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(data)
    print("COMPLETE real_masks=9 trivial_masks=247",flush=True)

if __name__ == "__main__":
    generate(sys.argv[1] if len(sys.argv)>1 else "PrefixDualBounds.csv")
