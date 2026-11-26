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
