# Overnight exact-exponent overlay (2026-11-26/27, UTC+08)

Frozen GitHub main: `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. On this research branch, the frozen 2,990/3,072 closures increase to **2,995/3,072**; **77** shards and **87** distinct exact keys remain. The global lower bound is **not** established. [Ledger increment](Delta.json), [key → shards](KeyToShards.json), [shard → remainder](ShardToKeys.json).

## Complete key after non-author cold replay

* `(19,316)` / `P19_I00064`: [argument and certificate](D/README.md). Replays both exact forest recurrences, checks all 128 support masks with 19 present, and excludes the full pivot tail from 50. This closes the shard because `[316]` was its entire frozen remainder. The 21 additional support cases are not counted as 21 shards. Candidate `700d089093a20dca10d30eab5a97bc7aa4a22523`; cold arithmetic 230.913 s.
* `(7,28)` / `P7_I00009`: [argument and certificate](D2/Readme.md), [cold receipt](Receipts/Review7x28.md). All 64 support masks consistent with canonical root 7 were replayed: 13 old forests, 27 new forests, 24 strict abundancy contradictions, with no unresolved exponent tails. The frozen remainder was `[28]`. Candidate `2fcb9397f1410e8fac959fcb0f90fece8770d527`; cold arithmetic 230.074 s.
* `(7,130)` / `P7_I00031`: [exact tree and proof](E/README.md), [cold receipt](Receipts/Review7x130Complete.md). All seven live first-pivot values closed: 61 splits including the root, 769 forests, nine price leaves and zero open paths. The frozen remainder was `[130]`. Candidate `8ebfc3058ac351c68c9bcbee5191fe9c37bb303a`; clean replay 47.040 s.
* `(19,162)` / `P19_I00036`: [complete packet and proof](E2/README.md), [cold receipt](Receipts/Review19x162Complete.md). The complete first-pivot domain `[2,4,6]` is closed. In the genuinely new valuation-four part, the second pivot has the complete live domain `[2,4,6,8]` and strict tail from 19; all four double-checked forests pass. Frozen remainder `[162]`. Candidate `d18dd5ea26b674525a4a842d37a3c8d98619ab5b`; cold arithmetic 9.262 s.
* `(19,502)` / `P19_I00094`: [standard tree and proof](F/README.md), [cold receipt](Receipts/Review19x502Complete.md). All 17 live first-pivot values are covered, with 1,843 forests, 103 splits, 2,038 direct contradictions and no open branches. Frozen remainder `[502]`. Candidate `b5667687e63b16aebd8b1faf9cd141415e5615df`; cold arithmetic 49.738 s.

## Separate conditional results

* `(19,420)`, `P19_I00080`: first-pivot values 8, 10 and 12 excluded; **2,4,6** remain. [Proof and checker](C/README.md); cold candidate `1f20e3d284b8c8a329f6412c35a58b711b9829ef`, 124.720 s.
* `(19,330)`, `P19_I00065`: first-pivot values 8, 10 and 12 excluded; **2,4,6** remain. [Proof and checker](C2/README.md), [cold receipt](Receipts/Review19x330.md).

* `(7,12)`, `P7_I00005`: 68 of 83 live first-pivot values excluded; **15** remain at the recorded cold snapshot. [Packet and checker](A/README.md), [cold receipt](Receipts/Review7x12Expanded.md).
* `(19,82)`, `P19_I00021`: 2, 4, 8 and 10 excluded; first-pivot value **6** still has 84 of 128 support masks open. [Packet and checker](C4/README.md), [cold receipt](Receipts/Review19x82.md).
* `(3,12)`, `P3_I00007`: new first-pivot exclusion **2** at 797161, leaving **1,66,96** after the inherited 96. [Baseline replay](B/BaselineReplay.md), [packet](B/Fiber2.json.gz), [non-author cold receipt](Receipts/Review3x12V2.md).
* `(13,372)`, `P13_I00073`: two disjoint cold-replayed packages cover **23 of 25** live pivot fibers; **2,12** remain. [18-fiber packet](Fibers13x372.json.gz), [receipt](Receipts/Review13x372.md); [five-fiber packet and proof](C5/README.md), [receipt](Receipts/Review13x372C5.md).

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
