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

## Experiment 003 — Retrieved Python LP and interval-dual execution

- Date (original run): 2026-11-22; date retrieved: 2026-11-22.
- Source commit: `1c7d0661ff1356105e5395b3bb02c49394491ee6`.
- Workflow: [Run 44990184125](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990184125).
- Code: historical Python baseline, ablation and interval-certificate scripts (now under `Sources/Python`).
- Reported floating LP objective: \(\log_{10}N =3129.458561\) for the forbidden-prime-free complementary case.
- Reported interval-dual lower endpoint: \(\log_{10}N =3129.458561\) after rounding to six decimals; floating minus certified value \(7.77\times10^{-8}\).
- Historical Roadblock 2 numerical scan: transition at prime `859`; this threshold scan itself used floating optimization.
- Result: **the programs ran and produced these values**. Independent verification of every LP relaxation constraint, infinite-tail argument and certificate rounding is still pending.

## Experiment 004 — V7 block-parallel circular cases (code candidate)

- Date: 2026-11-22.
- Base: V6 preserved unchanged; V7 is a separate code version.
- Change: partition large roadblock prime cases into disjoint ordered blocks. Each task starts from the forbidden-prefix state of all earlier prime cases; within a block the original sequential exclusion order is retained. Task submissions are throttled to limit memory overhead.
- Activation: circular roadblock bound `b > 2000`, at least 256 eligible primes, and more than one OpenMP thread.
- Validation: PASS in [source quality run 44991317752](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991317752), commit `9002859367742813d9fb15f91a946d8ef2a45a9e`: indexer and V1–V7 compiled, `ProofCoreTests: OK`, `ProofCoreTestsV7: OK`, and Python syntax check passed. Dataset-backed comparison and independent prefix-partition review remain pending.
- Performance rationale: improve utilization of multi-core hosts for heavy nested circular searches.

## Experiment 005 — Bounded exponent 2201 targeted probe

- Launched 2026-11-22 from commit `f04f35e99081d5c0a3ceb1440788ca15598c516f`.
- Workflow: [Run 44991101998](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991101998).
- Uses the checksum-pinned factor database and both V5 and V6.
- Intended runs: V5/V6 at exponent 1000, root 17 (35s cap each); V6 at exponent 2201 for roots 17 and 307 (120s cap each).
- Each root result is classified as `TREE_SUCCESS`, `UNRESOLVED`, or `TIMEOUT`. A timeout is inconclusive; individual successes do not constitute the complete all-root proof.
- Final result: workflow completed successfully as a bounded diagnostic, with the following per-case results:
  - V5, exponent 1000, root 17: `TREE_SUCCESS`; 2,770 branches; circular 0; 0 failed roadblocks; 2.28969 s.
  - V6, exponent 1000, root 17: `TREE_SUCCESS`; 2,770 branches; circular 0; 0 failed roadblocks; 2.25512 s.
  - V6, exponent 2201, root 17: `TIMEOUT` after 120 s; no completed root result.
  - V6, exponent 2201, root 307: `TIMEOUT` after 120 s; no completed root result.
- The database checksum passed and the index builder reported 106,206,170 lines / 41,322,879 groups.
- Logs: [Run 44991101998](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991101998) (artifact `TargetedProbeLogs`). The timeout cases had no periodic progress counters, motivating progress instrumentation in a subsequent version.

## Experiment 006 — V8 periodic progress diagnostics (planned)

- Date: 2026-11-22.
- Source: `Sources/Cpp/ProofTreeV8.cpp`, based on V7 and preserving prior versions.
- Modification: independent timer reporter emits flushed `[PROGRESS]` events every 10 seconds with total and circular branch counts, failed roadblock count, maximum roadblock prime bound, and elapsed wall time.
- Purpose: characterize the bottleneck on exponent-2201 roots 17 and 307 even when a bounded experiment times out.
- Planned probe: 60-second cap per root, fixed factorization snapshot, 2 OpenMP threads, uploaded logs.
- Validation: **PASS**, [GitHub Actions 44991559025](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991559025), index builder and V1–V8 compiled, core tests and Python syntax passed.
- Results: [Run 44991559032](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991559032), fixed checksum database of 106,206,170 entries and 41,322,879 groups; V8 at exponent 2201, root 17: **TIMEOUT** after 60 seconds; at elapsed 50 s, 403,628 total branches, 0 circular, 0 failed roadblocks, maximum roadblock bound 3. Root 307: **TIMEOUT** after 60 seconds; at elapsed 50 s, 412,952 total branches, 7,974 circular, 0 failed roadblocks, maximum roadblock bound 29. The `TargetedProbeLogs` artifact in the workflow contains 10-second progress logs.
- Bottleneck: the first 50 seconds are dominated by ordinary factor-chain DFS, not by the heavy roadblock path (`b > 2000`) targeted in V7. Future work should optimize ordinary DFS task scheduling.

## Experiment 007 — V9 bounded deep task scheduling (candidate)

- Date: 2026-11-22.
- Base: `ProofTreeV8.cpp`; original V8 remains available unchanged for comparison.
- Mechanism: allow independent exponent branches to become OpenMP tasks through depth 11; cap outstanding task reservations at eight per available thread. When the queue is at capacity, execute locally; task completion always releases reservations. Preserve the same exponent enumeration and contradiction checks.
- Motivation: root-17 and root-307 searches at exponent 2201 show hundreds of thousands of ordinary DFS branches during short probes.
- Validation: source quality checks **PASS** in [run 44991821429](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991821429) (V1–V9 compilation, core tests, Python syntax). Matched root/exponent *time-capped* benchmark [44991855026](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991855026): all four trials TIMEOUT after 35 seconds at exponent 2201. At 30 seconds p=17 V8 222,022 branches, V9 245,875 (+10.7%); p=307 V8 233,773 branches with 6,443 circular and V9 299,786 with 0 circular (+28.2%). Parallel visit order differs, so branch-count growth is **not proof of an end-to-end performance improvement**. Full terminating-case comparison is pending.
- Status: compiled and bounded diagnostics complete; no full-search acceleration or new proof certificate established.

## Experiment 008 — Completed-case V8/V9 timing comparison

- Date: 2026-11-22.
- Source: [GitHub Actions run 44992192309](https://github.com/stormwhip/PerfectNumbers/actions/runs/44992192309), commit `11d07509166cf1fe24f900a7a2a7b084f6f534`.
- Environment: Ubuntu GitHub Actions 2 threads, OMP_NUM_THREADS=2, GMP + zlib, checksum-pinned factor database.
- Target: exponent 1000; two separately selected roots (each root tested in the same historical forbidden order).
- Root 17: V8 `PROVEN`, 2,770 branches, 0 circular, 0 failed roadblocks, **2.29845 s**; V9 `PROVEN`, 2,770 branches, 0 circular, 0 failed roadblocks, **2.25049 s** (single-run time reduction **2.09%**).
- Root 307: V8 `PROVEN`, 1,531 branches, 0 circular, 0 failed roadblocks, **1.15197 s**; V9 `PROVEN`, 1,531 branches, 0 circular, 0 failed roadblocks, **1.13924 s** (single-run time reduction **1.11%**).
- Full logs archived as `CompletedCaseBenchmarkLogs` in the run.
- Interpretation: correct matching counters for the two completed roots, limited performance improvement at exponent 1000; single trials are susceptible to timing variation. Full unconditional proof at exponent 2201 remains incomplete.
- Future priorities: independent proof audit of arithmetic bounds and exponent coverage; new mathematically stronger pruning; longer tests of V9 on high-exponent bottlenecks.
