# Overnight exact-exponent overlay (2026-11-26/27, UTC+08)

Frozen GitHub main: `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. On this research branch, the frozen 2,990/3,072 closures increase to **3,001/3,072**; **71** shards and **81** distinct exact keys remain. The global lower bound is **not** established. [Ledger increment](Delta.json), [key → shards](KeyToShards.json), [shard → remainder](ShardToKeys.json).

## Complete key after non-author cold replay

* `(19,238)` / `P19_I00050`: [complete hybrid tree and proof](F2/README.md), [cold receipt](Receipts/Review19x238Complete.md). All nine first-pivot values closed. Frozen remainder `[238]`. Candidate `18d1aad0ae80a4d474c9cfa1dc8a938e3d025dbf`; clean replay 748.712 s, including the sole stock price leaf.
* `(19,316)` / `P19_I00064`: [argument and certificate](D/README.md). Replays both exact forest recurrences, checks all 128 support masks with 19 present, and excludes the full pivot tail from 50. This closes the shard because `[316]` was its entire frozen remainder. The 21 additional support cases are not counted as 21 shards. Candidate `700d089093a20dca10d30eab5a97bc7aa4a22523`; cold arithmetic 230.913 s.
* `(7,28)` / `P7_I00009`: [argument and certificate](D2/Readme.md), [cold receipt](Receipts/Review7x28.md). All 64 support masks consistent with canonical root 7 were replayed: 13 old forests, 27 new forests, 24 strict abundancy contradictions, with no unresolved exponent tails. The frozen remainder was `[28]`. Candidate `2fcb9397f1410e8fac959fcb0f90fece8770d527`; cold arithmetic 230.074 s.
* `(7,130)` / `P7_I00031`: [exact tree and proof](E/README.md), [cold receipt](Receipts/Review7x130Complete.md). All seven live first-pivot values closed: 61 splits including the root, 769 forests, nine price leaves and zero open paths. The frozen remainder was `[130]`. Candidate `8ebfc3058ac351c68c9bcbee5191fe9c37bb303a`; clean replay 47.040 s.
* `(7,420)` / `P7_I00081`: [complete tree and proof](E4/README.md), [cold receipt and independent price checks](Receipts/E4Receipt.md). All ten first-pivot values closed; this is canonical root 7, not `(19,420)`. Frozen remainder `[420]`. Candidate `78744f67339140524e96fdceaa4b9bdb4b310af4`; clean replay 181.084 s.
* `(7,490)` / `P7_I00093`: [complete tree and proof](E3/README.md), [cold receipt](Receipts/Review7x490Complete.md). All 14 first-pivot fibers are covered, with 277 forests and no unresolved siblings. The frozen remainder was `[490]`. Candidate `c5c07d2074044f524b941a5c767fc917fc8bc39d`; clean replay 28.269 s.
* `(7,586)` / `P7_I00106`: [complete certificate and proof](E5/README.md), [cold receipt](Receipts/Review7x586Complete.md). All 35 live first-pivot values covered with 448 forests, 22 nested splits, and zero open; frozen remainder `[586]`. Candidate `bb2794d7d61e363e32a467cfffcc84c0c32d2541`; clean replay 27.288 s.
* `(7,682)` / `P7_I00123`: [complete proof](E6/README.md), [cold receipt](Receipts/Review7x682Complete.md). All 32 live first-pivot values covered, including anonymous valuation 58 by a simultaneous two-target price and low valuation 6 by complete exact trees. Frozen remainder `[682]`. Candidate `e9e799ad1c744ec8ec311456f474f287f4718ab9`; clean replay 489.978 s.
* `(13,372)` / `P13_I00073`: [complete disjoint-union proof](Proof13x372.md), [cold receipt](Receipts/Review13x372Complete.md). All 25 live first-pivot values covered by 18+5+1+1, including the eight support masks at 2 and every descendant at 12. Frozen remainder `[372]`. Candidate `551e1a25f837fdc01121c6b7b0d037d2f217af79`; clean replay 169.247 s.
* `(19,162)` / `P19_I00036`: [complete packet and proof](E2/README.md), [cold receipt](Receipts/Review19x162Complete.md). The complete first-pivot domain `[2,4,6]` is closed. In the genuinely new valuation-four part, the second pivot has the complete live domain `[2,4,6,8]` and strict tail from 19; all four double-checked forests pass. Frozen remainder `[162]`. Candidate `d18dd5ea26b674525a4a842d37a3c8d98619ab5b`; cold arithmetic 9.262 s.
* `(19,502)` / `P19_I00094`: [standard tree and proof](F/README.md), [cold receipt](Receipts/Review19x502Complete.md). All 17 live first-pivot values are covered, with 1,843 forests, 103 splits, 2,038 direct contradictions and no open branches. Frozen remainder `[502]`. Candidate `b5667687e63b16aebd8b1faf9cd141415e5615df`; cold arithmetic 49.738 s.

## Separate conditional results

* `(19,420)`, `P19_I00080`: first-pivot values 8, 10 and 12 excluded; **2,4,6** remain. [Proof and checker](C/README.md); cold candidate `1f20e3d284b8c8a329f6412c35a58b711b9829ef`, 124.720 s.
* `(19,330)`, `P19_I00065`: first-pivot values 8, 10 and 12 excluded; **2,4,6** remain. [Proof and checker](C2/README.md), [cold receipt](Receipts/Review19x330.md).

* `(7,12)`, `P7_I00005`: 78 of 83 live first-pivot values excluded; **1,2,4,12,42** remain. One exact descendant of value 1 is separately excluded across 64 support masks, not the whole fiber. [Packet and checker](A/README.md), [latest receipt](Receipts/Review7x12Latest.md), [independent quadratic-price audit](Receipts/Review7x12Full77.md).
* `(19,46)`, `P19_I00013`: 11 of 14 live first-pivot values excluded; **6,10,12** remain, with 24 further scoped deep paths under 6 and 10 excluded. [Initial receipt](Receipts/Review19x46.md), [additional proof](C11/README.md), [additional cold receipt](Receipts/Review19x46Additional.md).
* `(19,58)`, `P19_I00015`: ten of eleven first-pivot values excluded, only **1** remains with 11 explicit deep gaps. [Initial receipt](Receipts/Review19x58.md), [low-Euler subtree](C10/README.md), [low-Euler receipt](Receipts/Review19x58Low.md).
* `(19,82)`, `P19_I00021`: 2, 4, 8 and 10 excluded; first-pivot value **6** still has 84 of 128 support masks open. [Packet and checker](C4/README.md), [cold receipt](Receipts/Review19x82.md).
* `(3,12)`, `P3_I00007`: new first-pivot exclusion **2** at 797161, leaving **1,66,96** after the inherited 96. Under 1, two secondary values `102,108` remain; under 66, only secondary value `6` remains; 96 is unresolved. [Baseline replay](B/BaselineReplay.md), [first-fiber receipt](Receipts/Review3x12V2.md), [two independent partial replays](Receipts/BPartialReceipt.md), [independently checked Euler-window restrictions](Receipts/Review3x12Parity.md).
* `(7,430)`, `P7_I00082`: independently confirmed first-pivot values **6,8,10,14,16** excluded; **2,4,12** remain. [Initial receipt](Receipts/Review7x430.md), [masked increment](G5/Readme.md), [cold receipt](Receipts/Review7x430Additional.md).
* `(7,438)`, `P7_I00084`: eight of twelve first-pivot values excluded; **10,12,18,22** remain. [Initial cold receipt](Receipts/Review7x438.md), [additional exact 2/16 receipt](Receipts/Review7x438Additional.md).
* `(19,270)`, `P19_I00056`: seven of eleven first-pivot values excluded, **4,10,12,16** remain. [Packet](Fibers19x270.json.gz), [cold receipt](Receipts/Review19x270.md).
* `(19,280)`, `P19_I00058`: 25 of 29 first-pivot values excluded at the lead snapshot; **2,16,18,22** remain at that snapshot. [Packet](Fibers19x280.json.gz), [cold receipt](Receipts/Review19x280.md).
* `(19,372)`, `P19_I00072`: ten of 15 first-pivot values excluded; additionally, three support masks exhaust all their remaining exact descendants. [Proof](G4/Readme.md), [cold receipt](Receipts/Review19x372.md).
* `(19,432)`, `P19_I00082`: 11 complete first-pivot values and six complete projected support masks excluded. [Scoped certificate](G2/Readme.md), [cold receipt](Receipts/Review19x432.md).
* `(13,262)`, `P13_I00055`: 22 of 29 first-pivot values excluded. [Packet](Fibers13x262.json.gz), [cold receipt](Receipts/Review13x262And31x310.md).
* `(31,310)`, `P31_I00062`: 21 of 26 first-pivot values excluded at the lead snapshot. [Packet](Fibers31x310.json.gz), [cold receipt](Receipts/Review13x262And31x310.md).
* `(31,352)`, `P31_I00069`: 17 of 31 first-pivot values excluded, including value 2 under all 16 masks and seven values by the LCM supply refinement. [Scoped certificate](C8/README.md), [cold receipt](Receipts/Review31x352.md).
* `(11,12)`, `P11_I00004`: first-pivot values 4 and 5 excluded across all 32 canonical masks; values 1, 2 and 8 have additional scoped exclusions. [Proof](C9/README.md), [cold receipt](Receipts/Review11x12.md).
* `(11,358)`, `P11_I00070`: nine complete first-pivot fibers and 213 compatible mask/valuation cells excluded. **91 raw cells** remain under 25 masks. [Proof and checker](G/Readme.md), [cold receipt](Receipts/Review11x358.md).
* `(13,310)`, `P13_I00063`: 14 of 22 first-pivot values excluded, eight open. [Proof and checker](C6/README.md), [cold receipt](Receipts/Review13x310.md).

These do not enter the full-key ledger. [Mainline regression receipt](Receipts/Mainline.md) lists independent scope and does not claim a full-history cold replay. Independent receipts for [(19,316)](Receipts/Review19x316.md), [(19,162)](Receipts/Review19x162.md) and [(19,420)](Receipts/Review19x420.md) include the endpoint audits.

## Offline replay

From the repository root, with normal Python assertions enabled and no discovery or factor cache:

```sh
python -I -S -B -X int_max_str_digits=0 Research/Night2400/D/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/D2/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E2/Fibers19x162Complete.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C2/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C4/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/B/DomainAudit.py Research/Night2400/B/Fiber2.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/E/Verify130.py Research/Night2400/E/Tree7x130.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Session20261126/TreeCheck.py Research/Night2400/F/Tree19x502.json.gz
python -I -S -B Research/Night2400/Project.py Research/FinalSprint/Delta.json --verified Research/Night2400/VerifiedKeys.json --out Build/Night2400/Reproject
```

Use `python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py` for accepted complete-key arithmetic followed by projection, or see the [integration receipt](Receipts/Integrated.md). The standalone projection checks ledger identity and arithmetic-independent bookkeeping only. Full-key membership is populated after acceptance of the offline mathematical proof; an arbitrary input to the projection does not constitute a proof.
