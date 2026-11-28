# Canonical `(19,222)` first 18: complete `g=12` and two additional exact leaves

Frozen `495c59f55456a70994ce7848487e0c4e262c1984`. In this packet the canonical root exponent is 222 and exact first exponent is `v_7579985624053(N)=18`. For second prime `r=3705121363`, **exact `v_r(N)=12` is impossible**. At the previously split second values `2` and `22`, both conditional exact `v_108501737266216818637411(N)=4` are also impossible. This is one complete second fiber and two disjoint tertiary leaves; it is not a first-fiber or full-key closure.

All three terminals use independent strictly integer forest recurrences, retain every legal Euler position, and do not use an extra absence. Their decimal floors are 2405 for the whole `g=12` prefix, 2406 for `(g,j)=(2,4)`, and 2400 (strictly over `10^2400`) for `(22,4)`. The direct `g=12` witness benefits from two newly ECPP-certified prime factors of `σ(r^12)`; these are checked as actual compulsory roots, not assumed from factorizations. The [verifier](Verify18Extra222.py) reconstructs live scope and consumes all 140 ECPP records. [Packet](Extra18x222.json.gz) SHA-256 `6bbeb54c6a1ee3a538cf073f938565a97537ee8a0293a5a7950292fc72da850d`, cold author replay exit 0.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/Verify18Extra222.py
```

After accepted earlier packets, first 18 retains `g=2,16,22`, with nested j lists `[6,10]`, `[2,4,6,10,12,16]`, `[2,6,10,12]` respectively. First 1 still survives. No global projection change.
