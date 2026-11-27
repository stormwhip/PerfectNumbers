# Independent replay of $(19,162)$

The complete replay certifies exclusion of the canonical exact pair $(19,162)$. The frozen ledger assigns this pair as the sole remaining member of `P19_I00036`.

## Complete replay

**PASS COMPLETE; `[2,4,6]` all covered, zero OPEN.** Detached clean tracked candidate `d18dd5ea26b674525a4a842d37a3c8d98619ab5b`, CPython 3.11.9. Packet SHA-256 `ad2d23ca3817e8a04577246028c2d80c8b942d208a990326127b323c2a711b58`. The stock entry point was materialized byte-for-byte locally from `850bee532621cdf5aca0fea142ef4364015007ad:Research/Night2400/VerifyFibers.py`, Git blob `851e597b656f8c0db640e07409d7aebee7b86742`, SHA-256 `6e5d4c19f0b353f5a80998e120fe6b00c7f5dc285c42a241461f762db1987b6c`; no author caches.

```powershell
python -I -S -B -X int_max_str_digits=0 Research/Night2400/VerifyFibers.py Research/Night2400/E2/Fibers19x162Complete.json.gz
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Receipts/FiberPartition.py Research/Night2400/E2/Fibers19x162Complete.json.gz
```

Replay 2026-11-27 00:34:31.827–00:34:40.932 +08:00, elapsed 9.262487 s; both commands exit 0. Result `[5,1,8,1]` forest/nested split/direct/price, price receipt `[[0,[2,0,4]]]`. 109 embedded ECPP entries. Independent data-only domain audit: root pivot is 512-bit, compelled valuation 1, odd valuations `[1,3,5,7,9,11,13]` legally impossible, `[8,10,12]` fail exact size, tail begins strictly beyond `B` at 14. For first fiber 4, a new 168-bit pivot `342824539081437076343940054698469728805379685794103≡3 mod 4` has exactly four live children `[2,4,6,8]`, all forest-covered; its raw monotone tail starts at 19. Both levels accept equality in the prefix budget; terminal forest checks both exact integer bounds strictly `>B`. The first-pivot 2 forest and 6 price close the other branches. Earlier independent arithmetic separately reconstructed the price-six proof from the original byte-identical leaf.

The frozen `FinalSprint/Delta.json` row `P19_I00036` has only `remaining_actuals=[162]`; the complete partition discharges that exact residual shard. No stronger exclusion of `19^162 | N` at a different exact valuation is claimed.

## Earlier replay stages

The following stages all use the canonical root and exact exponent of the complete replay. Their conditional exclusions are included in the corresponding first-pivot domain above.

### Initial partition

The admissible first-pivot domain was $\{2,4,6\}$, with a strict size tail from 14. A dual-checked forest at 2 and an existing price leaf at 6 left valuation 4 as the single outstanding case. The replay took 8.536 s. [Original replay record](https://github.com/stormwhip/PerfectNumbers/blob/b4b2a30601ef5e3f135c47c846c1e9801af57b3f/Research/Night2400/Receipts/Review19x162.md).
