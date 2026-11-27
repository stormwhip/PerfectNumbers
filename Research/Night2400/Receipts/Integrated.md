# Integrated accepted-key regression

At integrated commit `7c50d7ca` (2026-11-27 UTC+08), the standard-library entry point completed with exit 0, using compiled-in key statuses and exact re-projection:

```sh
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py
```

```text
PASS complete (7, 28) 186.956 s
PASS complete (7, 130) 68.609 s
PASS complete (19, 162) 7.775 s
PASS complete (19, 316) 148.439 s
PASS projection 2994 78 88 with accepted-key arithmetic
```

The local full stdout is `Build/Night2400/IntegratedReplayFour.log`. This is a branch-integration regression, separate from the non-author cold candidate receipts. It does not rerun conditional packets or the entire historical library. The earlier wrapper used the wrong JSON status field for the 7×130 verifier and was corrected before this run; the arithmetic verifiers did not change.

At `1bcfcfbc`, the same entry point passed five-key arithmetic and projection (exit 0). Local stdout `Build/Night2400/IntegratedReplayFive.log`:

```text
PASS complete (7, 28) 244.806 s
PASS complete (7, 130) 84.546 s
PASS complete (19, 162) 11.015 s
PASS complete (19, 316) 155.021 s
PASS complete (19, 502) 45.694 s
PASS projection 2995 77 87 with accepted-key arithmetic
```

At `97eb04d7`, the same entry point passed six accepted keys (exit 0). Local stdout `Build/Night2400/IntegratedReplaySix.log`:

```text
PASS complete (7, 28) 216.448 s
PASS complete (7, 130) 71.137 s
PASS complete (7, 490) 23.370 s
PASS complete (19, 162) 8.047 s
PASS complete (19, 316) 128.883 s
PASS complete (19, 502) 44.649 s
PASS projection 2996 76 86 with accepted-key arithmetic
```

The next run started at the eight-key checkout `37da4f5d`, so it replayed exactly eight proofs (including `(7,420)` and `(13,372)`). Before its projection, the integration checkout advanced to `87fc66be`, so the printed projection is the nine-key ledger. Both steps passed, but this is **not** a nine-key arithmetic receipt. The entry point now refuses a changed accepted-key list; later integrated arithmetic is run from a fixed snapshot. Local stdout: `Build/Night2400/IntegratedReplayEight.log`.

A clean detached checkout of `5a8c2db3b28fdf0af4dc3d8292b5ae12a4c1eefd` then replayed all nine accepted keys and the unchanged projection (exit 0). Local stdout: `Build/Night2400/IntegratedReplayNine.log`; it ended with `PASS projection 2999 73 83 with accepted-key arithmetic`. This arithmetic replay is independent of the original discovery tools.

At detached `1df3994e2c80d8cd801331043153134723bcd8bf`, all ten accepted keys and exact projection completed cleanly (exit 0). The new `(19,238)` arithmetic replay took 728.729 seconds in this run. Local log `Build/Night2400/IntegratedReplayTen.log` ends with `PASS projection 3000 72 82 with accepted-key arithmetic`.

At detached `ebd75735f9394ee176dde0ac63d65864e068084a`, all twelve accepted keys and exact projection completed cleanly (exit 0). The new `(7,682)` and `(19,270)` took 589.726 and 240.440 seconds. Local log `Build/Night2400/IntegratedReplayTwelve.log` ends with `PASS projection 3002 70 80 with accepted-key arithmetic`.

Supplemental regression: `python -S -B -X int_max_str_digits=0 Research/Night2400/E/Test130.py --full` passed conditional accounting and six negative mutations, then rejected removal of a live deep sibling from the complete certificate. `python -S -B -X int_max_str_digits=0 Research/NightMerge/LatticeTests.py` verified the Sturm endpoints and 609 planted-divisor invariants; the C7 known-leaf regression continued to pass after the refined interior proof was added.

## PR #8 integration replay

The tracked snapshot at `48b58d97fcf5dff01097078f14721e9f9d1b392a` was replayed on Windows using Python 3.11.9. The thirteen case executions ran in parallel, with each running the corresponding verifier and status validation from [Replay.py](../Replay.py). The command below runs the same thirteen checks sequentially and then verifies the three projected JSON files.

```sh
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py
```

| Complete key | Observed replay seconds |
|---|---:|
| `(7,28)` | 388.237 |
| `(7,130)` | 141.253 |
| `(7,420)` | 419.037 |
| `(7,490)` | 40.221 |
| `(7,586)` | 40.353 |
| `(7,682)` | 877.361 |
| `(7,732)` | 1050.695 |
| `(13,372)` | 405.846 |
| `(19,162)` | 9.211 |
| `(19,238)` | 1062.964 |
| `(19,270)` | 321.484 |
| `(19,316)` | 250.367 |
| `(19,502)` | 90.221 |

All thirteen checks passed. Independent reconstruction from the frozen FinalSprint ledger matched all residual shard rows and the reverse index. The thirteen exclusions clear thirteen singleton shards, giving 3,003 closed, 69 open and 79 distinct open keys. Repository naming and relative Markdown links were checked on the integration snapshot. The FinalSprint ledger, Midday overlap and SupportSplit regressions also passed.

The four newly recorded first-pivot values at `(19,432)` passed the [prefix-price replay](../FrontierTree.py) on the [packet](../Fibers19x432Price.json.gz). This scoped result is recorded in the [proof index](../README.md). Full-history arithmetic replay remains pending.
