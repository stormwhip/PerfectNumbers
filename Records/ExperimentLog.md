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

## Experiment 009 — Eight-prime LP complement certificate candidate

- Date: 2026-11-22.
- GitHub Actions: [Run 44993433027](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993433027); source commit `1cef5b26c356149bc7460f3c5cbc2e56e8330bb5`.
- Program: `Sources/Python/PrimeSetSearch.py` using `solve_and_certify`, `P_max=4000`, `a_cut=16`, and `certify=True` on final candidates.
- Goal: find reduced forbidden-prime sets with complement LP bound exceeding \(10^{2300}\).
- Both unrestricted greedy deletion and forced-delete-127 start converged to
  \(S_* = \{3,5,7,11,13,17,19,31\}\).
- Removed seven roots \(\{61,97,127,307,331,1093,398581\}\).
- Floating LP lower-bound exponent: **2390.111019072194**.
- Reported interval-dual lower-bound exponent: **2390.1110142932844**.
- Margin over exponent 2300: **90.1110142932844**.
- LP computation time: 8.997 seconds.
- The 7-prime core \(\{3,5,7,11,13,17,19\}\) gave float LP exponent **1936.450754**; whether a different seven-prime set can certify the target requires separate proof or exhaustive check.
- Status: **computational interval-dual result**; independently verify LP modeling, interval rounding and every forced-factor implication. No new unconditional odd-perfect-number bound has yet been proved.
- Next: use reduced-set tree branches with recorded order; benchmark root costs and validate the mathematical proof before claiming a speedup.

## Experiment 010 — V10 prime-adic obligation pruning prototype

- Date: 2026-11-22.
- Source candidate: `Sources/Cpp/ProofTreeV10.cpp`, preserves the full original 15-root ordering for isolated V9/V10 comparisons.
- Mathematical rule: for each known prime q, maintain the sum of known q-adic valuations from already established divisor-sum components; use Euler exponent parity and inexact-branch divisibility to calculate the smallest compatible exponent.
- Conservative special-prime adjustment: charge ordinary minimum exponents for all factors, then subtract the single largest possible positive saving for one Euler-special prime.
- Exact branch contradictions: reject a fixed exponent smaller than its cumulative forced valuation.
- Tests: `ProofCoreTestsV10.cpp` passed in [source quality run 44993665806](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993665806).
- Dataset benchmark: [Run 44993733799](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993733799), same pinned index and two threads. Exponent 1000, root 17: both PROVEN, 2770 branches, V9 2.32457 s, V10 2.23843 s. Exponent 1000, root 307: both PROVEN, 1531 branches, V9 1.14050 s, V10 1.15975 s. Exponent 1500, root 307: both PROVEN, 16490 branches, V9 8.27487 s, V10 8.31438 s. Exponent 2201, root 17: both timed out at 30 s; at the 20-second progress point, V9 had visited 228782 branches and V10 197448. Partial traversal rates are affected by parallel scheduling.
- Conclusion: no meaningful valuation-induced reduction in branches on completed test roots; the theoretical cut is sound under factorization assumptions, but its cost is not yet justified by these workloads.
- Dependency: source factor primality and arithmetic decision bounds still require independent verification before promoting V10 to a mathematical proof.

## Experiment 011 — Reduced-root proof-tree prototype (pending run)

- Date: 2026-11-22.
- Source: `ProofTreeReduced.cpp` retains V9's algorithm with root order filtered to \(19,7,11,31,13,3,5,17\).
- Research question: do seven removed top-level roots reduce or increase *total* tree runtime after removing their forbidden-prime constraints from the other roots?
- Benchmark: `ReducedRootBenchmark.yml` compares the complete 15-root and reduced eight-root trees at exponents 300 and 500, each with a fixed time cap and checksum-pinned database.
- Important distinction: total proof-tree branch counts and run times depend on the forbidden set; the number of roots alone is not a performance metric.
- Status: compiled and tested in [quality run 44993825335](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993825335); dataset-backed full-root comparisons [run 44993825296](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993825296) completed for both target exponents.
- Exponent 300: original V9 15 roots, 13,250 branches, **0.412029 s**; reduced eight-root tree, 14,238 branches, **0.454519 s**. All tested roots PROVEN and no unresolved roadblocks.
- Exponent 500: original V9 15 roots, 37,208 branches, **5.09176 s**; reduced eight-root tree, 40,733 branches, **5.5008 s**. All tested roots PROVEN and no unresolved roadblocks.
- Outcome: removing seven roots made the other root trees larger, resulting in a **slight slowdown** in these two low-exponent trials. An LP-certified smaller prime set alone does not guarantee faster factor-chain searches. Optimize branch ordering and introduce stronger branch cuts before expecting an end-to-end gain.

## Experiment 012 — Exhaustive root-order subset DP (queued)

- Date: 2026-11-22.
- V11 separates `ROOT_ORDER` from fixed `CIRC_ORDER`, making transition cost \(C(F,p)\) depend only on subset F and next root p.
- `RootOrderProfiler.cpp` evaluates all 1024 complete transitions at exponent 300 with one thread and a cold per-edge factorization cache.
- `RootOrderOptimizer.py` runs exact subset DP twice: minimizing branch count (time tie-break) and minimizing measured seconds (branch-count tie-break).
- Dataset: pinned `checkfacts.txt.gz` SHA-256 `ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119`.
- Workflow: [RootOrderOptimization.yml](../.github/workflows/RootOrderOptimization.yml).
- Status: source validation and exhaustive profile pending.

## Experiment 013 — Affine state-level LP dual certificates (prototype)

- Date: 2026-11-22.
- For each root-prefix subset \(F\subseteq S_*\), generate one interval-checked dual certificate for the LP with abundance target \(R=2\).
- The same dual multipliers remain feasible when only the abundance RHS changes, yielding a reusable affine lower bound \(L_F(R)=c_F+\lambda_F\ln R\).
- The generator checks 256 prefix masks and compares the affine dual against primal LP objectives at five abundance targets \(R\in\{1.1,1.25,1.5,2,3\}\).
- Runtime DFS can evaluate this bound in constant time using a safe upper bound on the abundancy of already fixed prime powers. The LP deliberately retains all primes outside prefix F, including state-forbidden and already-fixed primes, making it a relaxation.
- Status: Python certificate generation and C++ integration pending.
