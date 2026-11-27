# Night2400 C10 — the first Euler fiber of (19,58), P19_I00015

Offline, from the repository root, using standard-library Python with assertions enabled:

```text
python -I -S -B Research/Night2400/C10/Verify.py
```

The candidate concerns odd perfect `N <= 10**2400` with `19^58 || N`. The 247-bit certified forced prime `Q = 155306613932666028670208812450645212905178047040045530562317564121001023821` is fixed at exponent **1**, so it is the Euler component. The verifier rebuilds the complete first split, but **makes no coverage claim for any of its other ten live fibers**.

Under `Q^1 || N`, the certified 244-bit prime `T = 25884435655444338111701468741774202150863007840007588427052927353500170637` is forced. Its only live exponents are `2,4,6,8,10,12,14`: the checker separately verifies eight direct siblings, 15 incompatible siblings and the monotone size tail at 31. The packet completely excludes **4, 8, 12, 14** for this second split, and proves only the explicitly covered subtrees of 2 and 6. It leaves **11 exact paths open**, listed by the checker: two at `T^2`, eight at `T^6`, and `T^10` itself. Thus it is not a complete first fiber, key, or shard.

The [packet](EulerF1.json.gz), SHA-256 `f52b0f8b3fd0f8e869e0e38f7d6ac34cf0254a1082dce5c2ad8df3f2ca7f5c90`, represents open leaves as JSON null. All other leaves must pass either two exact forest recurrences or the [prefix-aware joint price](PrefixPrice.py); null leaves are reported rather than counted as proved. The fixed Euler assumption lets the verifier price all unseen suppliers at exponent >=2, with the exact `LCM` budget protecting against charging a forced cofactor twice. The `T^12` price with targets `(19,T)` has receipt `(4,[0,0,0])`; for `T^10`, ideal all-target valuation price has floor 2352 and is insufficient. The optional discovery factor cache, scout and PARI are not loaded by replay.
