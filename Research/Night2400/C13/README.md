# Night2400 C13 — (19,280), P19_I00058

Cold replay from the repository root, standard-library Python, assertions enabled:

```text
python -I -S -B Research/Night2400/C13/Verify.py
python -I -S -B Research/Night2400/C13/Verify.py --deep2
```

Assume odd perfect `N <= 10**2400` and `19^280 || N`. The 49-bit prime `q=353998162545967` is certified and forced. The exact first split yields 29 live exponents, 29 direct exclusions, 58 incompatibilities and a size-only tail at 117. This packet claims a complete exclusion only for **first exponent 22**; no inherited first-fiber verdict is needed for its proof.

At exponent 22, the 51-bit certified prime `1822778365160689` is forced. Its exact split has 26 live children, all covered by two exact forest recurrences; additionally there are 27 direct exclusions, 17 incompatible exponents and the monotone size tail at 71. Every forest is strictly above `10**2400`, even when the printed decimal floor is 2400.

The separate `--deep2` check excludes only the 77 exact prime-power paths listed in its packet. Each step is checked for exact admissibility and compulsion; no unlisted sibling is claimed. These exclusions reduce the supplied f2 scout gaps from 92 to 15. With exponent tuples in the scout path order, those 15 are `(280,2,4,2,2)`, `(280,2,4,2,4)`, `(280,2,4,8)`, `(280,2,4,10)`, `(280,2,6,12,22)`, `(280,2,6,18)`, `(280,2,6,22)`, `(280,2,6,28)`, `(280,2,6,30)`, `(280,2,6,36)`, `(280,2,6,40)`, `(280,2,6,42)`, `(280,2,10,22)`, `(280,2,10,28)`, `(280,2,10,36)`.

Packet SHA-256: [exact 22](Fiber22.json.gz), `5cdf36e489cb0fbeb25b20a00bbc27c0a89a0204b4f0abc07c32ba2ec3123321`; [77 conditional paths at 2](Paths2.json.gz), `2e8230b7e7c98f4ee89ab29389fcda7db8aa4ca81ceb383082ec630ffa57dd6c`.

The two other delegated first fibers 16 and 18 are not covered by this packet. Exact direct-plus-abundancy discovery found 40/128 support masks excluded for each, but the remaining 88 showed no near-closing root forests, so they were not sealed. No ECM run was repeated. Cold replay does not load any discovery file, factor index, generated cache, PARI, or another Night2400 packet.
