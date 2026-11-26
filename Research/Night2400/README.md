# Overnight exact-exponent overlay (2026-11-26/27, UTC+08)

Frozen GitHub main: `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. On this research branch, the frozen 2,990/3,072 closures increase to **2,991/3,072**; **81** shards and **91** distinct exact keys remain. The global lower bound is **not** established. [Ledger increment](Delta.json), [key → shards](KeyToShards.json), [shard → remainder](ShardToKeys.json).

## Complete key after non-author cold replay

* `(19,316)` / `P19_I00064`: [argument and certificate](D/README.md). Replays both exact forest recurrences, checks all 128 support masks with 19 present, and excludes the full pivot tail from 50. This closes the shard because `[316]` was its entire frozen remainder. The 21 additional support cases are not counted as 21 shards. Candidate `700d089093a20dca10d30eab5a97bc7aa4a22523`; cold arithmetic 230.913 s.

## Separate conditional results

* `(19,162)`, `P19_I00036`: first-pivot values 2 and 6 excluded; **4** remains. [Packet](Fibers19x162.json.gz) and [checker](VerifyFibers.py); cold candidate `ee67b04926df3346cf7443d4c5e2467d3335a24a`, 8.536 s.
* `(19,420)`, `P19_I00080`: first-pivot values 8, 10 and 12 excluded; **2,4,6** remain. [Proof and checker](C/README.md); cold candidate `1f20e3d284b8c8a329f6412c35a58b711b9829ef`, 124.720 s.

* `(7,12)`, `P7_I00005`: 51 of 83 live first-pivot values excluded; **32** remain. [Packet and checker](A/README.md), [cold receipt](Receipts/Review7x12.md).
* `(7,130)`, `P7_I00031`: first-pivot values 1, 2, 8, 9 and 10 excluded; **4,6** remain. [Packet and checker](E/README.md), [cold receipt](Receipts/Review7x130.md).

These do not enter the full-key ledger. [Mainline regression receipt](Receipts/Mainline.md) lists independent scope and does not claim a full-history cold replay. Independent receipts for [(19,316)](Receipts/Review19x316.md), [(19,162)](Receipts/Review19x162.md) and [(19,420)](Receipts/Review19x420.md) include the endpoint audits.

## Offline replay

From the repository root, with normal Python assertions enabled and no discovery or factor cache:

```sh
python -I -S -B -X int_max_str_digits=0 Research/Night2400/D/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/Fibers19x162.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/C/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/A/Verify.py
python -I -S -B Research/Night2400/Project.py Research/FinalSprint/Delta.json --verified Research/Night2400/VerifiedKeys.json --out Build/Night2400/Reproject
```

The projection checks ledger identity and arithmetic-independent bookkeeping only. Full-key membership is populated after acceptance of the offline mathematical proof; an arbitrary input to the projection does not constitute a proof.
