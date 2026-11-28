# `(19,276)`: complete second window `t^16,Q^1`

Frozen main `495c59f55456a70994ce7848487e0c4e262c1984`. Define `t=1176672733`, `Q=90938047640154004421283567941471211810894981635972737129272047925640491256883059096525979990283681579529`. For an odd perfect `N≤10^2400` with canonical 19 and exact exponents `19^276,t^16`, the precise Q-window has `[1,2,4,5,6]`, raw tail 15. [The previous forest overlay](Even276.md) excluded 5 and 6. This packet rules out `Q¹` entirely. Only `Q²` and `Q⁴` are still open under first `t^16`; there is no first-fiber credit.

`Q≡1 (mod 4)` and its actual exponent is 1, so its row fixes Euler. The mandatory prime `R=537069791622427053730040164091678112653` divides `σ(Q)/2`. The checker reconstructs **all eight** viable R exponents `[2,4,6,8,10,12,14,16]`, strict raw tail **35**. Both exact forest recurrences certify strictly > `10^2400` at every leaf, with diagnostic integer decimal floors 2416,2403,2420,2418,2424,2472,2494,2638, respectively. This proof uses neither Hensel pricing nor the withdrawn PR #11 result.

[Verifier](VerifyFirst16Q1.py) isolated cold replay exited 0, using 57 verified ECPP labels. [First16Q1.json.gz](First16Q1.json.gz) SHA-256 `166c9604dee56e87f6190ff0fb2f5a9c56efe9eba208ba24b0bed5bcd13112bf`.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyFirst16Q1.py
```
