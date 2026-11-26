# Night2400 C6 — (13,310), P13_I00063

Offline with standard-library Python and assertions enabled, from the repository root:

```text
python -I -S -B Research/Night2400/C6/Verify.py
```

This candidate excludes exact first-pivot exponents **6, 10, 12** for odd perfect `N <= 10**2400` with `13^310 || N` in the inherited root-13 class (19, 7, 11, 31 do not divide N). It proves neither the entire key nor the shard. The 43-bit prime `q = 5424477432443` is verified by deterministic bounded primality and forced at valuation 1. The first split checks all raw exponents 1–135 and the size-only tail from 136: 90 are incompatible, 23 are directly impossible, and 22 survive the prefix arithmetic. Tests do not trust the historical support projection.

All eight canonical support masks over 3, 5 and 17 are checked at each covered exponent. Exponents 6 and 12 use eight dual forest checks each; exponent 10 uses seven dual forests and one strict exact abundancy exclusion at mask 240. Minimum decimal floors of the exact forest bounds, respectively, are 2401, 2400 and 2407. Both integer recurrences require a strictly greater bound than `10**2400`, including when the decimal floor is only 2400.

The [support packet](Support13x310.json.gz) SHA-256 is `28f22a2f84e8beef098d25b13fae920685b2d218b535e23f3ad6285225f56d30`. It includes ECPP chains for all 344 large prime labels. Official-data witness growth and PARI were used only in discovery; replay does not use them, a generated cache, a prior verdict, or another Night2400 candidate.
