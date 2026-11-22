#!/usr/bin/env python3
"""Produce two genuine LP prefix certificates and 254 trivial safe lower bounds.

This screening mode is for matched root-31 and root-17 benchmarks only. For every
unselected mask, lambda=0, intercept=0 and all gains are zero (a valid but weak
nonnegative residual-size lower bound). It does not pretend to certify those
masks using the LP solver.
"""
import csv
import sys
from pathlib import Path
from IntervalCertificate import solve_and_certify

ROOTS = [19, 7, 11, 31, 13, 3, 5, 17]
SELECTED_MASKS = (7, 127)

def generate(out):
    rows = [(mask, 0.0, 0.0, 0.0) for mask in range(256)]
    removed, forced = [], []
    for mask in SELECTED_MASKS:
        forbidden = {p for i, p in enumerate(ROOTS) if mask & (1 << i)}
        f, lb, lam, b, deletion, required = solve_and_certify(
            forbidden_S=forbidden, P_max=4000, a_cut=16, certify=True,
            return_affine=True, return_forced_gains=True,
        )
        rows[mask] = (mask, lam, b, lb)
        removed += [(mask, p, gain) for p, gain in sorted(deletion.items())]
        forced += [(mask, p, gain) for p, gain in sorted(required.items())]
        print(f"PREFIX_CERT mask={mask} float={f:.12f} interval={lb:.12f} "
              f"deletionGains={len(deletion)} forcedGains={len(required)}", flush=True)
    out = Path(out)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(("mask", "lambda0_lower", "intercept_lower", "base_log10_lower"))
        w.writerows(rows)
    for filename, header, contents in (
        ("PrefixDualVariableGains.csv", ("mask", "prime", "gain_lower"), removed),
        ("PrefixDualForcedGains.csv", ("mask", "prime", "gain_lower"), forced),
    ):
        with out.with_name(filename).open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(contents)
    print(f"COMPLETE masks={SELECTED_MASKS} trivialOthers=254 "
          f"deletion={len(removed)} forced={len(forced)}", flush=True)

if __name__ == "__main__":
    generate(sys.argv[1] if len(sys.argv) > 1 else "PrefixDualBounds.csv")
