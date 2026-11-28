# Independent root-31 forest review: broader packets

Baseline `495c59f55456a70994ce7848487e0c4e262c1984`; all claims retain `19,7,11∤N`, odd perfect `N≤10^2400`, and exact respective `v31`. **Conditional only**, both keys remain open. The [independent checker](Check31Forest.py) reconstructs the full split domains, including each nested domain, and applies the independent parity-capacity forest recurrence described in [Upper receipt](Root31UpperReceipt.md). The only imported proof primitive is [frozen prime/ECPP arithmetic](../../NightSevenForest/Release/PrimeCheck.py), not a candidate loader, arithmetic recurrence or list of children. Invoke with `python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Audit/Check31Forest.py <packet>`.

## `(31,268)`, pivot 3229

[Certificate268Broad.json.gz](../ThirtyOne/Certificate268Broad.json.gz), SHA-256 `03bc15b40a8a0fc49610227af74b5b1553a582de78927cc58192ac76ee0d5416`. Exit 0. All 76 initial live exact values recovered, raw tail 458. Independent PASS 46 strict forests, one nested split (prime `30044742693389`, exact children `[1,4,6,10,12,13,16,18,21]`, strict tail 43), 393 ECPP chains. Minimum floor 2400 is a strict integer lower bound `>B`, not an equality. **Accepted firsts**:

```text
106,108,112,114,118,120,124,130,132,136,142,144,148,150,154,160,162,166,
168,172,174,178,180,184,186,190,192,196,198,202,204,208,214,216,220,222,226,228
```

This is 38/76 and supersedes the six in [Upper receipt](Root31UpperReceipt.md); add 32, not 38+6. It does not use the frozen unaccepted 75/76 historical candidate or remove `3229^102`.

The immutable superset [Certificate268.json.gz](../ThirtyOne/Certificate268.json.gz), SHA-256 `8c5bf616e336e655e1fa3f5398c048f4a0a0cc30cc059c79fa19a2319246f445`, also independently passed (exit 0). It covers **60/76**, including both earlier packages, in 18 nested splits and 344 strict forests with 2186 ECPP chains (minimum floor 2400, verified strict). The exact first residuals are `{4,10,12,16,24,72,78,82,84,88,90,94,96,102,156,210}`. For combined accounting this is a disjoint increment of 22 over Broad, not 60+38.

## `(31,2)`, pivot 331

[Certificate2.json.gz](../ThirtyOne/Certificate2.json.gz), SHA-256 `808ced76f1ed0b513ad63ad93d78fffff9e285b382910a222abc67db8d547f12`. Independent exit 0: 143 directly live with size tail 952, **56/143** first fibers accepted, 4 nested splits, 96 strict forests and 2029 certified ECPP subjects. Minimum floor 2401. Accepted full-local list:

```text
16,18,22,28,30,34,36,42,46,52,58,60,64,66,70,72,78,82,84,88,90,94,96,
100,102,106,108,112,114,118,124,126,132,136,138,144,148,154,160,166,168,174,
180,184,190,198,202,204,210,214,216,220,228,232,234,238
```

The immutable [Certificate2Extended.json.gz](../ThirtyOne/Certificate2Extended.json.gz), SHA-256 `2eecfec2b31852de23f9b31f093fa680a029cc97d5dd1ebd0053332c44a3c1f5`, independently passed (exit 0). Same exact 143/952 initial domain/tail, 114 exact firsts accepted, 29 open; 12 nested splits, 239 strict leaves, 2688 ECPP subjects. Minimum floor 2400 was strictly compared at every leaf. This supersedes the 56-first packet (58 additional firsts, not another 114 to add).

## `(31,6)`, pivot 917087137

[Certificate6.json.gz](../ThirtyOne/Certificate6.json.gz), SHA-256 `49c8cc39aaaa10d41723a7f78ee73537ca292962f9a1b912f9250d87efbcc1a3`. Exit 0. All 53 initial live exact values recovered, strict tail 267. Independent PASS 57 strict forests, one nested split (prime `30675589854920415267716138411985841559029`, exact children `[1,2,4,6,8,10,12,13,14,16,18,20,21]`, strict tail 43), 1018 ECPP chains. Minimum floor 2400, all comparisons strict. **Accepted 45/53**, leaving exactly `{2,36,52,58,72,78,108,120}`. No transfer from `(31,268)` or other previously certified keys, and no shard projection.

The immutable superset [Certificate6More.json.gz](../ThirtyOne/Certificate6More.json.gz), SHA-256 `bc6344ec0340d571541b0748891601be92be613c609330d4be8986397ec3942f`, also passed the independent same command (exit 0). It adds 2, 58 and 78, for **48/53** accepted, leaving `{36,52,72,108,120}`. Strict raw tail 267; 148 strict leaves, five exact nested splits, and 1660 ECPP records. This supersedes the 45-fiber result; use only the new total or its disjoint increment.

[Certificate6High.json.gz](../ThirtyOne/Certificate6High.json.gz), SHA-256 `2befb24113ee03e72e5a3154aea2c8ffbbcadb3c2a80df9166fdf9731aceb8fe`, passed the independent checker (exit 0) with six strict forests at 108,110,112,114,116,120, 14 ECPP subjects (including 953/980 decimal-digit labels), and minimum floor 2620. Of these six, only 108 and 120 are disjoint from More. The accepted union is now 50/53, with `{36,52,72}` open at this checkpoint.
