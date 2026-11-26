# Night2400 C6 — (13,310), P13_I00063

Offline with standard-library Python and assertions enabled, from the repository root:

```text
python -I -S -B Research/Night2400/C6/Verify.py
```

This candidate excludes exact first-pivot exponents **6, 10, 12, 20, 22, 32, 38, 48, 50, 52, 56, 58, 60, 66** for odd perfect `N <= 10**2400` with `13^310 || N` in the inherited root-13 class (19, 7, 11, 31 do not divide N). It proves neither the entire key nor the shard. The 43-bit prime `q = 5424477432443` is verified by deterministic bounded primality and forced at valuation 1. The first split checks all raw exponents 1–135 and the size-only tail from 136: 90 are incompatible, 23 are directly impossible, and 22 survive the prefix arithmetic. Tests do not trust the historical support projection.

All eight canonical support masks over 3, 5 and 17 are checked at each of exponents 6, 10, 12, 20, 22, 32, 38 and 48. Exponents 10 and 32 each use seven dual forests and one strict exact abundancy exclusion at mask 240; the other six each use eight dual forests. Both integer recurrences require a strictly greater bound than `10**2400`, including when the decimal floor is only 2400.

The six higher exponents use the frozen exact [joint price](../../FinalSprint/JointValuation.py) with both fixed prime coordinates and the inherited exclusions. The remaining live exponents are **2, 16, 18, 28, 36, 40, 42, 46**. For exponent 2 the official data already completely factors the pivot emission, but a bounded witness-growth run still gave floors only 1744–1994 on tested support masks, and the ideal two-target price has floor 1086, ruling out that particular pricing approach without a stronger prefix.

The support packets, including all required ECPP witnesses, have these SHA-256 digests:

- [6, 10, 12](Support13x310.json.gz): `28f22a2f84e8beef098d25b13fae920685b2d218b535e23f3ad6285225f56d30`
- [20, 22, 32](SupportNext.json.gz): `4b4335a6fdc34a5e7cdbfafc5d68f240949d0c05ee314eab6bb9d1bdbeffbb31`
- [38, 48](SupportMiddle.json.gz): `2ab8e956c3fa2a557913a972c20e4dd2f12c312edf562e25e0ad84626109b32a`

Official-data witness growth and PARI were used only in discovery; replay does not use them, a generated cache, a prior verdict, or another Night2400 candidate.
