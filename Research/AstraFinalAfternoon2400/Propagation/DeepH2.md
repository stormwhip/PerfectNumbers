# Deep exact leaves for the team's remaining `27431^2` tree

Use the canonical assumptions of the [mixed proof](Mixed438x12.md), now with exact `v_27431=2`, and `a=752487193`, `c=50047294070406095227`. This packet claims **only the seven exact leaves** below, not closure of the full `27431^2` fiber. The root-seven team also covered `a^28` and `a^22 c^8` independently; those two must not be counted twice. Their final branch matrix may select `a^22 c^2`, `a^22 c^10`, `a^22 c^12`, `a^46`, and `a^52` if those are its actual uncovered leaves.

| packet | additional exact valuations | checked method | SHA-256 |
|---|---|---|---|
| [sub2](Reserved438x12-sub2.json.gz) | `a^28` and `a^22 c^2` | 2 dual reserved forests, 822 vertices, 96 ECPP | `cb8acc872e031f464a8f39abaacef4515c04a4262fb938ee9cc639a99b7e31a2` |
| [price2](Reserved438x12-price2.json.gz) | `a^22 c^8`, `a^22 c^10`, `a^22 c^12` | 3 absolute size leaves after verifying the complete exact Euler supply/cofactor partitions, 3 ECPP | `ecf7e579233527650520aee207386702b1d77f2cb2f3b353de68d5aab55db142` |
| [high2](Reserved438x12-high2.json.gz) | `a^46`, `a^52` | 2 absolute size leaves checking 878 Euler windows each, no extra ECPP | `d095abec21ba9275de03d74ceb9d4753c0b3643f73342233a1de46a4c91f8c85` |

For sub2 the scaled strict floors `floor(10^6 LB/B)` are 130652114 and 1170978268. The three price2 rows seal 876, 878, and 878 distinct exact Euler-supply windows respectively; all eliminate by `XDQF` after outside checks, no crossover needed. The analytic [Euler location rule](Proof.md#L9) is replayed, matrices are literal exact integers, any unused ECPP record rejects. No overlap certificates or database queries are used during replay.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/VerifyReserved438x12.py sub2
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/VerifyReserved438x12.py price2
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/VerifyReserved438x12.py high2
```

A host tree can use `verify_h2_cuts()` from the [checker](VerifyReserved438x12.py) after inserting its directory into `sys.path`. It returns seven tuples sorted by prime; match the host's *entire* exact prefix, not only the final label/exponent, and assert that each declared delegated prefix is actually reached exactly once. This allows reuse without copying primality banks or weakening the host's domain regeneration.
