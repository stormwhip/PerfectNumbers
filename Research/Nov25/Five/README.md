# Root 5: Nov25 exact exclusions

Both commands require only Python's standard library and verify exact exponents against the canonical root-5 forbidden set `{3,7,11,13,19,31}` for hypothetical odd perfect `N <= 10^2400`.

```text
python -I -S -B Research/Nov25/Five/Verify148.py
python -I -S -B Research/Nov25/Five/Verify520.py
python -I -S -B Research/Nov25/Five/Simple520.py  # alternate source-free replay
```

- **(5,148), P5_I00034.** The 104-digit `q = σ(5^148)` is certified prime and divides `N`. A historical uncounted forest nomination was sanitized into [Forest148.json.gz](Forest148.json.gz), SHA-256 `59342e4bf2a1b4193e45af911feae42f298eac7781f4c8e0220b55bb5e7cdf20`. Exact recursive product and independent rational-coupon [ordinary replay](OrdinaryForest.py) both give an integer log10 floor of 2503 when `q` is not the Euler prime. If `q` is Euler, exact size allows only exponents 1, 5, 9, 13, 17, 21. Exact sigma residues exclude 5, 9, 17; forced divisor size excludes 13, 21; indicator duals checked with independent directed arithmetic exclude 1 with no additional prime hints. [Complete replay](Verify148.py).
- **(5,520), P5_I00097.** The [early replay](Early520.py) excludes every case with the Euler prime in `A = σ(5^520)`, every external Euler exponent `a >= 5`, and external `a = 1` with `s = v_5(q+1) < 445` (432 direct, 13 source-gap, 65 paid-emitter subchecks). It verifies trial roughness rather than assuming `A` prime or squarefree. In the remaining region, `q` is external to `5A` and `q >= Q = 2*5^445 - 1`.

  The [alternate replay](Simple520.py) hands off earlier, at `s=300`. Every smaller `s` is excluded by the direct root inequalities, so it does not invoke the source-gap or paid-emitter lemmas. The same terminal weights with `Q=2*5^300−1` give floor `log10 N >= 2456` with both arithmetic implementations.

  The [late terminal replay](Late520.py) uses existing authenticated factor edges and anonymous blocks. All explicit bases are smaller than `Q` and coprime to `A`. Every anonymous block is smaller than `Q`; it is stripped of the prime support of `A`, the explicit bases and already selected blocks of different source bases. Two alternative exponents at the same source need not be disjoint, since only one can occur. Other remaining primes are at least 5001 and ordinary, giving a monotone lower bound on log cost per log abundance. Contributions from `5`, `A`'s prime support, and the Euler prime are credited with upper bounds; their disjoint mandatory sizes `5^520`, `A`, and `Q` are counted separately. No assumption about which component generates `q` is used in this late region. The [exact dual](Late520Dual.json) is replayed with 11,326 options, 12,994 rows and 653 selected anonymous blocks. It gives floor `log10 N >= 2558` with integer interval and independent Decimal arithmetic. [Complete replay](Verify520.py); [optional SciPy discovery generator](FindLate520.py) is not needed for acceptance.

Discovery used the exact-component discipline of [Ochem–Rao](https://doi.org/10.1090/S0025-5718-2012-02563-4): a lower exponent bound is not an exact exponent and does not by itself activate its divisor sum. See [the separate pilot record](Partial.md) for negative and conditional results, which do not enter the ledger.
