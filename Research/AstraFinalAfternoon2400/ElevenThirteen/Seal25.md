# A fixed-Euler 107th-order terminal for (11,16)

In canonical `(11,16)` (`7,19∤N`, `v_11(N)=16`, odd perfect `N≤10^2400`), set `t=50544702849929377`, `s=239337374873`. The [nested union](Nested.md) fixes `v_t(N)=25` and exhausts the live exponents of `s`, which divides `σ(t^25)`. This note proves only its otherwise surviving exact `v_s(N)=16` child. The tree therefore covers a whole first fiber, not a whole key.

The Euler prime is already `t`, so all unfixed exponents `h` are even. From the three fixed components one computes `v_s(σ(11^16)σ(t^25)σ(s^16))=1`, leaving demand 15. For an unfixed supplying prime `r`, exact order `o=ord_s(r)` must divide the odd `h+1≤5100`. The factorization `s−1=8·107·279599737` is verified with deterministic primality checks, and `s>5100`. Thus no order-one source or LTE length shift is possible; every supplier has `o=107`, `h≥106`, and a true supply `b=v_s(r^107−1)` with `1≤b≤15`.

The strict price deficit at weight **106** satisfies `r^106<s^(106b)` and hence `r<s^b`; here least positive representatives are provably exhaustive despite the large weight, because it equals `o−1`. The verifier constructs all primitive 107th roots and their full unique Hensel lift classes at every exact depth; it rejects only compositeness, excluded/fixed labels or `X·lcm(D,r^106)>10^2400`, where `X=11^16 t^25 s^16` and `D` is the forced fixed odd remainder stripped of `X` support. Repeated occurrences of one base are not multiplied: use its greatest loss, or 1. This yields four exceptions, with exact product `U`. The final strict integer/rational inequality is `X s^(106·15)>10^2400 U`. It accounts for component sizes and supplies once, and does not add `D` a second time.

```
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/ElevenThirteen/Seal25.py
```

The standalone verifier checks all prime labels and outputs four exact-depth loss exceptions; [SecondTree.py](SecondTree.py) additionally binds this exact terminal to its checked prefix, verifies the other 56 forest leaves, and rejects missing children in all three splits. [Packet](Second-11-16-25.json.gz) SHA-256 `76d740a16a12f33694491bc7d043cee8e4de829372fbf5242fb2b55183c9ad9a`.
