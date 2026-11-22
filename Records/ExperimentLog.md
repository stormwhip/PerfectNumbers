# Experiment Log

This log separates **imported historical claims**, **directly observed experiments**, and **proof-checked results**. Dates use YYYY-MM-DD.

## Experiment 000 — Repository Reorganization

- Date: 2026-11-22
- Purpose: Normalize the repository into English PascalCase paths; preserve all original source versions and the original PDF.
- Inputs: repository commit `1c7d0661ff1356105e5395b3bb02c49394491ee6`.
- Change: relocate C++, Python, report and reference files; update workflow references and README; make expensive workflows manual.
- Verification: Git tree blob-SHA preservation for relocated source files. Compilation and large-data experiments are pending.
- Proof impact: **none**. No new bound is claimed.

## Imported historical observations (unverified in this session)

- 2012 published reference bound: `10^1500`.
- Historical project handoff reports a V4 15-root proof-tree experiment at exponent 1500 (about 1054 seconds, approximately 33 million branches, zero failed roadblocks).
- Historical handoff reports an LP endgame exponent of about 3129.458561 for the complement of the 15-prime set.
- These entries are not newly reproduced runs. Original claims and parameters are preserved in [LegacyResearchHandoff](../Documentation/LegacyResearchHandoff.md).

## Future experiment template

Record the date, Git commit SHA, command, compiler and libraries, CPU and memory, dataset SHA-256, root(s), target exponent, wall-clock time, counts of branches and unresolved roadblocks, full terminal output or artifact URI, and a one-line conclusion distinguishing experiment success from a proof claim.

## Experiment 001 — V6 conservative roadblock and residual accounting

- Date: 2026-11-22
- Base: V5 preserved unchanged. New candidate: `Sources/Cpp/ProofTreeV6.cpp`.
- Changes: replace finite-sieve exhaustion with an analytic infinite-tail fractional relaxation; avoid skipping abundance when composite residuals overlap; recompute composite lower size bounds after new factor information; reduce diagnostic atomic contention.
- Tests: `Sources/Cpp/ProofCoreTests.cpp` checks exponent coverage for p=3,7,11,13,17 through a=2048; tests overlapping composite lower-size accounting and a roadblock with ample remaining size.
- Execution: **PASS** — GitHub Actions run 44990984163, commit 9dc5cd68883f7e8d831c1afdc2c819598d4ed288. All six tree versions and the index builder compiled, `ProofCoreTests: OK`, and Python syntax checks passed. Dataset-backed performance comparison has not yet run.
- Proof impact: no new certified unconditional lower bound at this stage.

## Experiment 002 — Retrieved V5 all-root benchmark at exponent 300

- Date (original run): 2026-11-22; date retrieved: 2026-11-22.
- Source commit: `1c7d0661ff1356105e5395b3bb02c49394491ee6`.
- Workflow: [Run 44990168041](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990168041), `workflow_dispatch`.
- Inputs: `exponent=300`, `prime=all`, 2 GitHub Actions CPU threads.
- Data: 106,206,170 lines, 41,322,879 factor groups; snapshot SHA-256 pinned in `Readme.md`.
- Result: all 15 roots printed `PROVEN` with `failed_rb=0`.
- Total reported branches: **13,250**, circular branches: **0**, tree elapsed: **0.390215 s** (excluding database download and indexing).
- Status: real retrieved execution log, **not** a proof-grade independent verification of all mathematical assumptions.
