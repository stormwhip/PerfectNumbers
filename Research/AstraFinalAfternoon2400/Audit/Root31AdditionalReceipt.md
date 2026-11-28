# Independent root-31 forest review: broader packets

Baseline `495c59f55456a70994ce7848487e0c4e262c1984`; all claims retain `19,7,11∤N`, odd perfect `N≤10^2400`, and exact respective `v31`. **Conditional only**, both keys remain open. The [independent checker](Check31Forest.py) reconstructs the full split domains, including each nested domain, and applies the independent parity-capacity forest recurrence described in [Upper receipt](Root31UpperReceipt.md). The only imported proof primitive is [frozen prime/ECPP arithmetic](../../NightSevenForest/Release/PrimeCheck.py), not a candidate loader, arithmetic recurrence or list of children. Invoke with `python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Audit/Check31Forest.py <packet>`.

## `(31,268)`, pivot 3229

[Certificate268Broad.json.gz](../ThirtyOne/Certificate268Broad.json.gz), SHA-256 `03bc15b40a8a0fc49610227af74b5b1553a582de78927cc58192ac76ee0d5416`. Exit 0. All 76 initial live exact values recovered, raw tail 458. Independent PASS 46 strict forests, one nested split (prime `30044742693389`, exact children `[1,4,6,10,12,13,16,18,21]`, strict tail 43), 393 ECPP chains. Minimum floor 2400 is a strict integer lower bound `>B`, not an equality. **Accepted firsts**:

```text
106,108,112,114,118,120,124,130,132,136,142,144,148,150,154,160,162,166,
168,172,174,178,180,184,186,190,192,196,198,202,204,208,214,216,220,222,226,228
```

This is 38/76 and supersedes the six in [Upper receipt](Root31UpperReceipt.md); add 32, not 38+6. It does not use the frozen unaccepted 75/76 historical candidate or remove `3229^102`.

## `(31,6)`, pivot 917087137

[Certificate6.json.gz](../ThirtyOne/Certificate6.json.gz), SHA-256 `49c8cc39aaaa10d41723a7f78ee73537ca292962f9a1b912f9250d87efbcc1a3`. Exit 0. All 53 initial live exact values recovered, strict tail 267. Independent PASS 57 strict forests, one nested split (prime `30675589854920415267716138411985841559029`, exact children `[1,2,4,6,8,10,12,13,14,16,18,20,21]`, strict tail 43), 1018 ECPP chains. Minimum floor 2400, all comparisons strict. **Accepted 45/53**, leaving exactly `{2,36,52,58,72,78,108,120}`. No transfer from `(31,268)` or other previously certified keys, and no shard projection.
