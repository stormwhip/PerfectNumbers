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

[Certificate268Extended.json.gz](../ThirtyOne/Certificate268Extended.json.gz), SHA-256 `7149879dc331c745a4c38c40b81d29ac4283849c9697da534586ac52daa324b4`, independently passed (exit 0). It covers **69/76**, with 91 nested splits, 2785 strict forest leaves, and 7115 ECPP subjects. Minimum decimal floor 2400 remains a strict comparison; no residue disappears through rounding. Its exact outstanding firsts are `{4,24,72,82,102,156,210}`. This supersedes the 60-first package (9 more, not a further 69).

Definitive [Certificate268Union73.json.gz](../ThirtyOne/Certificate268Union73.json.gz), SHA-256 `015161d6cedeaa45fa5a566dc7fc690f13c3f683e934b0ad8b579ea93b663a75`, independently passed both the full domain walk and all arithmetic, each exit **0**. Verified **73/76**, with 206 internal splits, 6891 strict forest leaves, 11795 ECPP subjects and minimum decimal floor 2400 (strict). The only three open branches are null at the first level, `{102,156,210}`. This latest union supersedes all earlier (31,268) forest totals. The [historical 75/76 provisional claim](../../FinalNight2400/Report.md#L53-L55) remains unaccepted and supplies no missing first, and the [Euler masks](Root31EulerReceipt.md) do not close those three firsts. No projection of `(31,268)`.

## `(31,2)`, pivot 331

[Certificate2.json.gz](../ThirtyOne/Certificate2.json.gz), SHA-256 `808ced76f1ed0b513ad63ad93d78fffff9e285b382910a222abc67db8d547f12`. Independent exit 0: 143 directly live with size tail 952, **56/143** first fibers accepted, 4 nested splits, 96 strict forests and 2029 certified ECPP subjects. Minimum floor 2401. Accepted full-local list:

```text
16,18,22,28,30,34,36,42,46,52,58,60,64,66,70,72,78,82,84,88,90,94,96,
100,102,106,108,112,114,118,124,126,132,136,138,144,148,154,160,166,168,174,
180,184,190,198,202,204,210,214,216,220,228,232,234,238
```

The immutable [Certificate2Extended.json.gz](../ThirtyOne/Certificate2Extended.json.gz), SHA-256 `2eecfec2b31852de23f9b31f093fa680a029cc97d5dd1ebd0053332c44a3c1f5`, independently passed (exit 0). Same exact 143/952 initial domain/tail, 114 exact firsts accepted, 29 open; 12 nested splits, 239 strict leaves, 2688 ECPP subjects. Minimum floor 2400 was strictly compared at every leaf. This supersedes the 56-first packet (58 additional firsts, not another 114 to add).

[Certificate2More.json.gz](../ThirtyOne/Certificate2More.json.gz), SHA-256 `e6955d8768ac33b917343eab41e0540bf8b4b73e53935b38f249fbb673cdfc9e`, is structurally identical to the Extended packet at every previously proved first. Independently compared the pinned archive trees and cold-ran exactly the three newly nonnull firsts `{262,310,420}` through `Check31Forest.accept(path, only=[262,310,420])`: exit 0, all 14 new splits, 569 strict leaves, 1430 reached ECPP subjects, minimum floor 2400 (strict). The old 114 arithmetic proofs are retained, not repeated. The exact conditional forest union at this checkpoint is **117/143**, leaving 26.

Two disjoint narrow packets [Certificate2Fiber268.json.gz](../ThirtyOne/Certificate2Fiber268.json.gz), SHA-256 `f4722749c187f09aca91508b6f28cd915ffdd75044db7b53ccb043ff921f3c0a`, and [Certificate2Fiber276.json.gz](../ThirtyOne/Certificate2Fiber276.json.gz), SHA-256 `7a471fb6dc9ea4bf91632c16f667ba82e2dd34ed04e2efd10e25cf7ea6d59b67`, passed as separate strict trees (exit 0). Each has one forest leaf, no internal split, and directly closes only its exact first. Reached four and two ECPP subjects respectively, with floors 3078 and 3098. The forest union becomes 119/143; the disjoint [analytic first 400](Root31Price400Receipt.md) gives **120/143**, leaving 23. None is the unrelated root key `(31,268)` or a whole `(31,2)` closure.

[Certificate2Followup131.json.gz](../ThirtyOne/Certificate2Followup131.json.gz), SHA-256 `327683e54e81452029ee229a33346de4649f8445a82908510a2194437b978c5e`, preserves every proof tree already present in the pinned 117 package. Its exact extra list is `{12,24,40,48,156,162,196,226,268,276,316,382,388,400}`. The independently accepted individual 268,276,400 receipts above cover three; the remaining eleven were tested exactly once with `Check31Forest.accept(path, only=...)`, independently regenerating each nested domain and all 775 strict forest leaves and 2977 reached ECPP subjects, exit 0. Both special `331^316` terminal prefixes (`1510189^f,3²,13²,61¹`, f=52,58) match their sealed ancestry; [independent price](Check31Price316.py) directly checks every feasible odd order pair including absent axes, reserve ≤LCM−1, and separates the 331-LTE length power (331 divides no pertinent base order). A common cubic reserve is charged once, noncubic orders at least two each, so weight 2 gives legitimate least-residue coverage. The Euler slot is fixed at 61, no square atom. Independently regenerate all lifted roots, reverse CRT and necessary lcm-size constraints; get losses `[10,0,0]` at f52 and `[6,0,0]` at f58 and both strict prices. The union is now **131/143** with residuals `{4,6,130,150,172,178,192,222,240,250,280,282}`. This supersedes previous totals, not 131 additional fibers.

## `(31,6)`, pivot 917087137

[Certificate6.json.gz](../ThirtyOne/Certificate6.json.gz), SHA-256 `49c8cc39aaaa10d41723a7f78ee73537ca292962f9a1b912f9250d87efbcc1a3`. Exit 0. All 53 initial live exact values recovered, strict tail 267. Independent PASS 57 strict forests, one nested split (prime `30675589854920415267716138411985841559029`, exact children `[1,2,4,6,8,10,12,13,14,16,18,20,21]`, strict tail 43), 1018 ECPP chains. Minimum floor 2400, all comparisons strict. **Accepted 45/53**, leaving exactly `{2,36,52,58,72,78,108,120}`. No transfer from `(31,268)` or other previously certified keys, and no shard projection.

The immutable superset [Certificate6More.json.gz](../ThirtyOne/Certificate6More.json.gz), SHA-256 `bc6344ec0340d571541b0748891601be92be613c609330d4be8986397ec3942f`, also passed the independent same command (exit 0). It adds 2, 58 and 78, for **48/53** accepted, leaving `{36,52,72,108,120}`. Strict raw tail 267; 148 strict leaves, five exact nested splits, and 1660 ECPP records. This supersedes the 45-fiber result; use only the new total or its disjoint increment.

[Certificate6High.json.gz](../ThirtyOne/Certificate6High.json.gz), SHA-256 `2befb24113ee03e72e5a3154aea2c8ffbbcadb3c2a80df9166fdf9731aceb8fe`, passed the independent checker (exit 0) with six strict forests at 108,110,112,114,116,120, 14 ECPP subjects (including 953/980 decimal-digit labels), and minimum floor 2620. Of these six, only 108 and 120 are disjoint from More. The accepted union is now 50/53, with `{36,52,72}` open at this checkpoint.
