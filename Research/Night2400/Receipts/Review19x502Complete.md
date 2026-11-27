# Independent replay of $(19,502)$

The complete replay certifies exclusion of the canonical exact pair $(19,502)$. The frozen ledger assigns this pair as the sole remaining member of `P19_I00094`.

## Complete replay

Detached clean tracked candidate `b5667687e63b16aebd8b1faf9cd141415e5615df`, CPython 3.11.9; gzip SHA-256 `27faabaa543d51c082763fa4674ddf917df6447e28ee202c578bd6cea8d872ea`. Uses frozen TreeCheck entry point and embedded ECPP; no author or factor cache.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Session20261126/TreeCheck.py Research/Night2400/F/Tree19x502.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/F/Tree19x502.json.gz
```

**PASS COMPLETE, all 17 first fibers and zero OPEN; both commands exit 0.** Cold replay started 2026-11-27 00:52:09.317 +08:00, ended 00:52:58.894 +08:00, elapsed 49.7380225 s. Frozen TreeCheck printed `(19,502,[1843,103,2038])`; the independent audit matches all counts, including 103 splits with root, 3347 incompatible exponents, and 2903 ECPP entries.

The root pivot is `14401804750392751≡3 mod 4`, compelled valuation 1; 35 odd exponents through 69 incompatible, 18 evens `[36,...,70]` excluded directly, first raw tail 71, live domain all 17 evens `[2,4,...,34]`. Root and all nested split child sets equal the independently rederived exact domains, now including former OPEN first fiber 16. There the pivot `3920383` has 23 exact live even children `2..46`; its subtree contains 50 splits and 916 exact forest terminals. Both forest recurrences require strict `>B`, every prefix size scan is inclusive at `B`, and every tail starts at the first strict overflow. No joint price is used in this packet. Frozen `FinalSprint/Delta.json` marks only remaining actual exponent 502 for `P19_I00094`, so closing that exact key closes the residual shard, not the stronger divisibility `19^502 | N` at any valuation.

## Earlier replay stages

The following stages all use the canonical root and exact exponent of the complete replay. Their conditional exclusions are included in the corresponding first-pivot domain above.

### Initial partition

With a strict size tail from 71, the admissible first-pivot values were the even integers from 2 through 34. The initial packet excluded 14 of 17 values, leaving $\{2,4,16\}$. The independent audit rebuilt all 29 nested domains. The replay took 10.255 s. [Original replay record](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/Night2400/Receipts/Review19x502.md).
