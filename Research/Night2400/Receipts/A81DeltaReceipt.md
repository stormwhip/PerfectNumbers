# A81 exact delta — independent reviewer-a receipt

Initially clean detached `53c297edb0aa27cebd4bb69d19446541f893b396` in `E:\PerfectNumbers-Night2400-reviewa`; only `Research/NightOrder/ECPP/` sparse-excluded. Python 3.11.9; no author cache or reserved folder used. Baseline `f7f9807a86c5f462940bcef68eb5406d875fbdac` already independently checked. Price12, MaskedForest, PivotCheck, Compose, ForestReplay, and PrimeCheck sources are unchanged from A79.

SHA-256:

```text
e2a57f004ba519bcfa8da4cdf64cb5c94afd566482f1dbbc2420a59f95768437  Research/Night2400/A/Fibers12.json.gz
72371c0cd80e60847ffb25a8b0ee0c2f06cb20f8b82969e9dcae184b7a76bb84  Research/Night2400/A/Verify.py
9b771704a2a84f022f2240995c6e741745d9bd28cfef50eef9c7f08064252f3e  Research/Night2400/A/Exact1x2.json.gz
9c4555611753d27a6cefe2dc0f6174e3f1955b8a9b1c7305bda20326724621f7  Research/Night2400/A/SupportLeaf12.py
2f6e8e114b04c9f35c3f52ead54345cb28e5091b314b2575dbf8d36b82f7c116  Research/Night2400/A/SupportLeaf12.json.gz
84d1fb5287dfd609e3707134d369a96c0f816bbf5d936a7b13fee27c75d6f87d  Research/Night2400/A/SupportLeaf2.json.gz
90cc0e4fcb38770ee3e569105f0535155791dd205ae7e9650449b71f33f29967  Research/Night2400/Receipts/ALateDeltaAudit.py
```

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/ALateDeltaAudit.py f7f9807a86c5f462940bcef68eb5406d875fbdac 1,2 1
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/ALateDeltaAudit.py f7f9807a86c5f462940bcef68eb5406d875fbdac 1,2 2
```

Independent stage loads the previous reviewer routine from local commit `c3219ae160f6b4f604fdf906c8f227b9fb109b14`, and compares all previous tree/certificate objects using duplicate-key rejecting JSON parsing. Rebuilds first/split domains and tails from integer sigma, validates abundance modes, independently enumerates each support packet's masks against its exact parent assignment, and binds every wrapper path/selected file to the exact prefix. The candidate stage uses only the original selected tree and its actually reachable ECPP entries, serialized in memory. Original exact and support dependency packets are verified by candidate calls through the matching wrapper; no substituted scoped payload or assumed proof.

- Fiber 1 scoped dependency chain: at `((7,12),(Q,1),(110563,2))` an exact-packet wrapper verifies `Exact1x2`, which in turn uses `SupportLeaf12` at the further exact assignment `(226741,2)`. The branch pivots are forced by incoming sigma products and the corresponding exact exponent is in the parent domain.
- Fiber 2 scoped dependency: `SupportLeaf2` attaches only at `((7,12),(Q,2),(200741603328100897,1))`. Both support packets have exactly one locked Euler component and recompute all 64 masks under that scope. Other contextual absences cannot activate these wrappers.

**f=1** UTC+08:00 2026-11-27 05:04:46.2788435 → 05:18:36.2932283, 830.005416 s, exit 0. [Transcript](A81Fiber1.txt): 832 outer forests, 17 outer splits, 8,120 outer ECPP. Exact1x2 adds 339 forests/8 splits/22 abundance/4,449 ECPP. Combined regular domain audit (without re-counting the admission domains) found 1,226 nested direct rejections and four no-five wrappers. SupportLeaf12 adds 32 direct, 23 abundance and 9 forests (839 ECPP). `PASS 1 2400`.

**f=2** UTC+08:00 2026-11-27 05:04:46.3558863 → 05:07:56.3540140, 189.987982 s, exit 0. [Transcript](A81Fiber2.txt): 1,797 outer forests, 34 splits, 1,840 nested direct exclusions, seven no-five branches, 6,094 outer ECPP. SupportLeaf2 closes 32 direct, 23 abundance and 9 forests (969 ECPP). Root common 84 direct not included in the nested subtotal. `PASS 2 2400`.

**Scope:** 81/83 first fibers from the previous 79 plus 1 and 2; root exponent and shard remain open for `[12,42]`. No credit for the separate f42 experiments in this receipt.
