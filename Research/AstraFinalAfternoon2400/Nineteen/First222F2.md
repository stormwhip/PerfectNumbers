# Canonical `(19,222)`: complete first-pivot exponent `f=2`

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. Let `N≤10^2400` be an odd perfect number with canonical root 19 and `19^222 || N`. Then `t² || N` for `t=7579985624053` is impossible. This is a complete **first fiber**, not a complete key or shard.

## Exact coverage

The frozen first raw domain has 53 viable exponents and strict tail **144**. The [historical first/second procedure](../../FinalNight2400/Root222/Two.py) and [frozen tertiary procedure](../../FinalNight2400/Root222/Thirds.py) reduced first `f=2` to four secondary exponents of `r=3705121363`, exactly `2,16,22,46` (secondary raw tail **189**). The exact complement is finished as follows.

| `g=v_r(N)` | Frozen unresolved exact tertiary values at `q=2032322226061` | Certificate removing all of them |
|---:|---|---|
| 2 | 2,4,18,28 | [Forest I](Forest222.md) for 2,28 and [Forest II](Forest222Stage2.md) for 4,18 |
| 16 | 1,2,4,18,28 | [Inert](Proof.md) for 1 and [Forest III](Forest222Stage3.md) for 2,4,18,28 |
| 22 | 1,2,4,18,28 | [Inert](Proof.md) for 1, [plain](Plain222J2.md) for 2, [masked](Mask222J4.md) for 4, nested checks below for 18, [nested j28](Root222J28.md) for 28 |
| 46 | Entire second window, no tertiary split | [Forest II](Forest222Stage2.md) strict direct witness |

At `g=22,j=18`, the [upper packet](Root222J18.json.gz) splits at `K=45031669`, a forced prime dividing `σ(t²)`. There are 47 exact live K exponents before strict raw tail **126**. The [upper verifier](VerifyRoot222J18.py) excludes 46, with 200 checked ECPP chains; only `v_K(N)=2` is delegated. At that prefix, `W=5642747947` is forced through `σ(K²)`. The [low verifier](VerifyRoot222J18Low.py) reconstructs all 24 viable W exponents `2,4,…,48`, strict raw tail **97**. The [low packet](Root222J18Low.json.gz) covers all 24: 20 exact forest terminals and four strictly excessive abundancy terminals, with 113 ECPP chains. The final `v_W=12` forest uses a separately certified 82-digit prime divisor of its actual geometric sum and locally proves that 5 and 11 must be absent. Its lower bound has decimal floor 2424 in the accepted integer replay. No anonymous cofactor is treated as prime.

Each applicable absence is proved before use from distinct compelled prime masses and strict `σ(X)/X>2` inequalities; every subsequent forest compares unrounded integer bounds, with both recurrence implementations agreeing on strictness. Euler parity is either physically fixed by an odd exact row or conservatively minimized over every legal position, including an outside position. All high exponent tails are monotone in original compulsory size and keep equality at the threshold in the live window. No arithmetic from withdrawn PR #11 was used.

| Nested data | SHA-256 |
|---|---|
| [Root222J18.json.gz](Root222J18.json.gz) | `27012a6a365936e0b7a3ebf8138f6fd4963188467f451179b9a3f05979c2c4b9` |
| [Root222J18Low.json.gz](Root222J18Low.json.gz) | `31c89ddfd47a10015dfba559424fbc7e38a3a313696f86c2249c4d716e6841ba` |
| [Root222J28.json.gz](Root222J28.json.gz) | `011b3d4230d46ce366bb8de2ba622f3a644f26ebe56ffc24bfa9919de824ec9e` |

[The composition verifier](VerifyFirst222F2.py) rebuilds the exact original scope, matches each complement, and cold-replays the required new proof packs. It does not claim to rerun all frozen historical arithmetic, which was accepted separately. Author cold replay returned exit 0 with the message `COMPLETE (19,222) canonical exact first exponent 2`. This leaves first `f=1,18` at `(19,222)` (51/53 firsts, no exact key or shard change).

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyFirst222F2.py
```
