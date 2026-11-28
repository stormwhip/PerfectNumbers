# Canonical `(19,222)`: close the entire second window `f=1,g=2`

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. Let `t=7579985624053`, `r=3705121363`, `q=3789992812027`. For an odd perfect `N≤10^2400` with exact canonical prefix `[19^222,t^1,r²]`, `q` is forced through `(t+1)/2`. The original surviving third exponents `[2,4,12,16,18,42]` have strict original tail 144. [Forest I](Forest222.md) removed 12 and 42; [Forest II](Forest222Stage2.md) removed 2 and 4; [Forest III](Forest222Stage3.md) removed 18. This integer forest excludes the final exact `q^16` and therefore completes the whole second window `(f,g)=(1,2)`.

The [verifier](VerifyRoot222F1G2.py) re-enumerates the complete original third-pivot domain and verifies the disjoint difference with earlier packs. Because `t^1` fixes Euler, every forest row has its ordinary exponent; two independent recurrences bound them with the strict usual integer threshold comparison and monotone tail. Both diagnostics are floor 2405. The [packet](Root222F1G2.json.gz) has 178 matched ECPP labels and SHA-256 `4224ec34fe814bf643e791f9f709ce2cbcb1c0873b515caf8acef663ec9f15fb`. Cold exit 0.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyRoot222F1G2.py
```

No first-fiber, full key or shard credit for this supplement. Remaining first exponents after the separate [f=2 completion](First222F2.md) are 1 and 18.
