#!/usr/bin/env python3
"""Generate all 256 enhanced LP prefix certificates and both gain tables for V16.

Unlike the old prototype, this uses the sigma(61^10) and sigma(61^12)
implications which yielded the eight-prime complement output > 2400.
No placeholder prefixes are used.
"""
import csv
import math
import sys
from pathlib import Path
from IntervalCertificate61 import solve_and_certify

ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
P_MAX = 4000
A_CUT = 16
MIN_GAIN = 1e-300  # Skipping subnormal gains is a safe relaxation.

def generate(path):
    rows, removals, required = [], [], []
    for mask in range(256):
        forbidden = {q for i, q in enumerate(ROOTS) if mask & (1 << i)}
        primal, certified, lam0, intercept, removal, forced = solve_and_certify(
            forbidden, P_max=P_MAX, a_cut=A_CUT,
            target_abund_ratio=2.0, certify=True,
            return_affine=True, return_forced_gains=True,
        )
        if not all(math.isfinite(v) for v in (primal, certified, lam0, intercept)):
            raise ArithmeticError(f"non-finite certificate for mask {mask}")
        if lam0 < 0.0:
            raise ArithmeticError(f"negative abundance multiplier for mask {mask}")
        for ratio in (1.1, 2.0, 3.0):
            primal_r, _ = solve_and_certify(
                forbidden, P_max=P_MAX, a_cut=A_CUT,
                target_abund_ratio=ratio, certify=False,
            )
            dual_r = intercept + lam0 * math.log(ratio)
            if dual_r > primal_r * math.log(10.0) + 2e-7:
                raise ArithmeticError(
                    f"affine dual mismatch: mask={mask} ratio={ratio} "
                    f"dual={dual_r} primal={primal_r*math.log(10.0)}"
                )
        rows.append((mask, lam0, intercept, certified))
        removals.extend((mask, q, gain) for q, gain in sorted(removal.items())
                        if math.isfinite(gain) and gain >= MIN_GAIN)
        required.extend((mask, q, gain) for q, gain in sorted(forced.items())
                        if math.isfinite(gain) and gain >= MIN_GAIN)
        print(f"CERT mask={mask} certified_log10={certified:.12f} "
              f"removed={len(removal)} forced={len(forced)}", flush=True)
    if len(rows) != 256:
        raise ArithmeticError("incomplete prefix set")
    if rows[255][3] <= 2400.0:
        raise ArithmeticError("eight-prime complement LP failed the 2400 target")
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    for dest, header, data in (
        (out, ("mask", "lambda0_lower", "intercept_lower", "base_log10_lower"), rows),
        (out.with_name("PrefixDualVariableGains.csv"), ("mask", "prime", "gain_lower"), removals),
        (out.with_name("PrefixDualForcedGains.csv"), ("mask", "prime", "gain_lower"), required),
    ):
        with dest.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(data)
    print(f"COMPLETE masks=256 terminal_log10={rows[255][3]:.12f} "
          f"removal_gains={len(removals)} forced_gains={len(required)}", flush=True)

if __name__ == "__main__":
    generate(sys.argv[1] if len(sys.argv) > 1 else "PrefixDualBounds.csv")
