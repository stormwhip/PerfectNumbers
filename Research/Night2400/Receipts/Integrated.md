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
