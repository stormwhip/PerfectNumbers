# A79 f=4 independent delta receipt

Initially clean detached `f7f9807a86c5f462940bcef68eb5406d875fbdac` in `E:\PerfectNumbers-Night2400-reviewa`; sparse omits only `Research/NightOrder/ECPP/`; no reserved path or author cache used. Comparing with prior accepted A78 `ac69476668cc98f8e5b445d39b5ec76d723c0ae2`. Candidate transitive PivotCheck/Compose/ForestReplay/PrimeCheck sources are unchanged from A78.

SHA-256:

```text
69347f43301312df23e0d6737837de682d233b30b8f05fcf4538c6b1b7e3464f  Research/Night2400/A/Fibers12.json.gz
d553a9795e70eb85e0db5eebf27750efe464cced82e03d370ae4d349b7df68ac  Research/Night2400/A/Verify.py
348d82fbf1bcbaf72580e1be19cbbc8911729b41696653ee57e51553a76c2863  Research/Night2400/A/MaskedForest.py
14184ebd341868b0428aea2a64dd439e007489c456a1e2254d304b1f6faacc9a  Research/Night2400/Receipts/A79DeltaAudit.py
```

```text
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/A79DeltaAudit.py
```

The independent portion compares all 78 A78 tree objects and all prior ECPP chains byte-semantically after decoding both certificates and rejecting duplicate JSON keys. It verifies that the only added first fiber is `4`, reconstructs all ordinary and masked split domains from `sigma` products, exact valuations and monotone integer size bounds, and confirms the conditional absence argument using `σ(7^12)/7^12 × 13/9 × 6/5 > 2` once 5 (respectively 3) is compulsory. It separately partitions all Euler modes in abundance leaves, and all 64 masks if a `support-abundance` leaf occurs. The script then sends the unmodified `f=4` tree and its original used ECPP chains as an in-memory filtered packet to the candidate verifier: primality, both strict integer forest recursions (including the new masked condition) and exact used certificate set are checked, without re-running inherited trees. No derived packet file produced. [Per-split output](A79DeltaOutput.txt).

Delta run exit **0**; UTC+08:00 2026-11-27 **03:43:52.8222518 → 03:47:53.1702242**, stopwatch **240.491239 s**. `PASS 4 2400`, 1,250 forests, 40 splits, 1,443 direct inside f=4 (1,527 with 84 in the common root domain), 142 abundance leaves and 335 checked Euler modes, 2 `no-three` wrappers, no new price leaf. The 7,905 used ECPP chains include all 6,145 new entries. The filtered replay's `UNCOVERED` line purposefully omits the inherited 78 trees; the actual 79-tree packet gap is stated below.

**Scope:** 79/83 first fibers by the previously accepted 78 plus the delta of one. Remaining exact first exponents `[1,2,12,42]`; no root exponent/shard closure or acceptance of new collateral advances in f=1/2 by this receipt.
