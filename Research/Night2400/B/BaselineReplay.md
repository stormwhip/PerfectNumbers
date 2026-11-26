# Baseline receipt for the four remaining 797161 fibers

Worktree `E:\PerfectNumbers-Night2400-b`, branch `research/night2400-b`, pinned initial HEAD `49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec`. All commands were run from the checkout root with Python 3.11, isolated and without site packages. The domain command completed at about 23:22 UTC+08 on 2026-11-26. The five proof packets ran in order in harness job `pwsh-4a01eadc0be6426f` started at about 23:22 UTC+08 and completed exit 0 by about 23:48 UTC+08 (these are model-visible time bounds, not per-process CPU timings). Its output is in the delegated research-b session; the exact offline commands below reproduce the receipt without consulting that session.

```sh
python -I -S -B Research/FinalSprint/LowBranches/AllDelta.py . Research/FinalSprint/LowBranches/Branches.json.gz Research/FinalSprint/LowBranches/Wave2/Branches.json.gz Research/FinalSprint/LowBranches/Wave3/Branches.json.gz Research/FinalSprint/LowBranches/Wave4/Branches.json.gz
python -I -S -B Research/Session20261126/LowBranches/Verify.py --repo .
python -I -S -B Research/FinalSprint/LowBranches/Verify.py . Research/FinalSprint/LowBranches/Branches.json.gz
python -I -S -B Research/FinalSprint/LowBranches/Wave2/Verify.py . Research/FinalSprint/LowBranches/Wave2/Branches.json.gz
python -I -S -B Research/FinalSprint/LowBranches/Wave3/Verify.py . Research/FinalSprint/LowBranches/Wave3/Branches.json.gz
python -I -S -B Research/FinalSprint/LowBranches/Wave4/Verify.py . Research/FinalSprint/LowBranches/Wave4/Branches.json.gz
```

Domain output for the scoped root class:

```text
root 12 prime 797161 domain 100 prior 90 new [46, 60, 72, 88, 106, 112] excluded 96 left [1, 2, 66, 96]
New complete exponents: 0; new complete shards: 0.
```

Historical verifier returned `[12, 797161, 100, 90, [1, 2, 46, 60, 66, 72, 88, 96, 106, 112]]`. Wave 1 explicitly passed 46 and 106; wave 2 passed 60, 72, 88, 112. Waves 3 and 4 passed their root-six-primary branches, contributing no new scoped valuation. Wave 2's exceptional paired-price occurrence passed with 6747 CRT combinations, zero probes and strict floor near 2453.54; it uses `3^12,797161^112,6781^1,3391^102` with Euler occupied by 6781 and residual supplies `(111,101)`. Those values cannot be imported into other prefixes.

An independent primary endpoint recomputation via `python -I -S -B Research/Night2400/B/DomainAudit.py Research/Night2400/B/Fiber2.json.gz` also passed in harness job `pwsh-8a090bf13b3246f9` (2026-11-27, 00:10–00:14 UTC+08). The raw last possible exponent from `3^12 * 797161^f <= 10^2400` is 405, with 406 beginning the strict size tail. After the necessary tests there are 100 primary valuations. With the supplied new complete `f=2` proof merged, the independently reconstructed remainder is `[1,66,96]`. The `f=2` secondary first size-only tail is 324; the complete pre-tail survivor list has 71 values, with 325 forests, 2 deeper splits, 2585 ECPP certificate keys, and minimum checked strict-bound floor 2400.

Final combined receipt: harness job `pwsh-ba61b6049ba94f46` ran the same independent audit with all three final packets (`Fiber1`, `Fiber2`, `Fiber66`) from about 02:03–02:29 UTC+08 on Nov 27 and completed exit 0. It returned `new_primary_exclusions: [2]`, `secondary_only: {"1": 77, "66": 96}`, `remaining: [1,66,96]`, and `complete_exponent: false`. The partial packets' unresolved sets are `[102,108]` at 398581 and `[6]` at 5897, respectively.
