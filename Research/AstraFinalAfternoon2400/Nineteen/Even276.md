# `(19,276)`: seven exact forest cuts under the even first exponents 16 and 18

Baseline `495c59f55456a70994ce7848487e0c4e262c1984`. The exact root is `19^276 || N`, and `v_1176672733(N)=f`. On each first window below we split at one certified odd prime divisor `q` of the stripped mandatory odd sigma output.

| `f` | `q` | complete raw live exact exponents | strict raw tail | excluded in packet | still open |
|---:|---:|---|---:|---|---|
| 16 | 90938047640154004421283567941471211810894981635972737129272047925640491256883059096525979990283681579529 | 1,2,4,5,6 | 15 | 5,6 | 1,2,4 |
| 18 | 2395723558714191605903463333646981101789939140815259939 | 2,4,6,8,10,12 | 27 | 4,6,8,10,12 | 2 |

The checker independently rebuilds the first-pivot raw domain (70 live, tail 188), matches the frozen 64-case packet complement `1,2,8,16,18,28`, and reconstructs all second-pivot exponent domains from necessary divisibility, actual Euler compatibility, partial abundance and the monotone strict tail. Each listed exclusion checks two exact unrestricted-Euler recursions independently; all admissible Euler positions and the exterior alternative remain in the minimum. See [the same forest invariants](Forest222.md). The strict decimal lower floors at f=16 are 2404,2408, and at f=18 are 2403,2410,2417,2429,2537. The floors are diagnostics only. The exact dependency [Even276.json.gz](Even276.json.gz) has SHA-256 `36eb3b356815fd993ff88cc762e634a56264beb899576c9e74e70bdb03289b4e` and 49 ECPP certificates matched to actual use.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyEven276.py
```

The [cold verification](VerifyEven276.py) exited 0. This packet alone closes neither first fiber nor complete key nor shard; the separate [E18Upper.md](E18Upper.md) refines but does not close the remaining exact `f=18,q²` branch. No PR #11 result is used.
