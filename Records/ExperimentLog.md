> **仓库精简记录（2026-11-22）**：主目标统一为 \(N>10^{2400}\)，过时的 V1–V15/V17 源代码、旧 CI 工作流与实验性脚本已从当前主分支删除。历史运行日志仍在本文及 Actions 中，全部旧文件可从 [精简前原始快照](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70) 恢复。当前入口为 [CurrentStatus2400](../Documentation/CurrentStatus2400.md)、冻结 V21 的 ProofTreeV21.cpp 与实验性独立验证器 V2。

# Experiment Log

This log separates **imported historical claims**, **directly observed experiments**, and **proof-checked results**. Dates use YYYY-MM-DD.

## 2026-11-26 森林前缀深化

基线 `2889e47f`，因子候选来自 data-v1（SHA-256 `ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119`）及精确分圆余项。244 个指数的首轮搜寻取每种奇偶模式 36 个合法精确指数；超过候选下界 1600 的分支扩大到 128 项，以薄弱模式的真实几何和重新选择子节点。全域第一次扫描只有 (3,46) 的浮点分数超过 2400。经深化后 11 个不同种子获两套整数复验；其它搜寻结果不作为排除证据。[逐包 SHA-256、整数下界和剩余清单](../Research/Session20261126/Delta.json)。

### 第二阶段：精确枢轴、联合供给与独立复验

固定主线的午间全账本已重放，返回 `PASS 267 actuals; 202 new shards; 204 remain`（本机原始日志 SHA-256 `05f1a3494495aa2e7761e7ff6a35ef2be1c71ecda18c3598a7cdc73fb50952ba`）；八根互素类另重放，8,897 个选项、12,455 行、8,616 条因子关系，下界 `4183.209493`。这不是声称所有历史 3,072 个任务都重新计算完毕。

在初始森林之上扩大至 256/384/512 个合法前缀选项，用弱叶的圆分余项寻找因子，并按实际来源重新分配子树归属。公共数据库与 ECM 的输出只作提示，节点最终重验素性、因子及 Euler 位置；误入候选的标签 2 被正式验证器拒绝，移除后重新搜索。若普通树仍不足，则穷尽一个或多个强制素数的精确幂，每个幸存子域单独生成森林。供给森林使用同一指数选择的赋值与尺寸联合下界。第三级检查点：74 个完整证明包有重复，独立冷回放并集为 **64** 个不同实际指数、**47** 个新增完整分片。另有 389 个条件支持证书，与三个新全局命中定理分开登记。

失败对照：仅给原普通森林附加单个丰度乘子，在测试的 116 个候选上未产生新过线；这是对该次松弛和价格网格的实验结果，不是对丰度路线的否定。对若干困难的固定枢轴分支只用 1,201 以下素数、普通前缀 24 的终端松弛，测试值包括 (3,78) 的 789 与 (13,640) 的 2021，均未过线。单靠增加不活跃标签或成功因子分解不能作为证明。

## 2026-11-25 根 3 指数 1162 候选审计

- 原包标准库重放 39.11 s：166 个素性证书、1,276 个显式辅助素数及 42 个叶节点通过，程序报告 2400.93。
- 扩大 Euler 来源枚举后 1,276 个显式辅助素数通过（20.27 s）；删除单重数净成本优惠后，最弱叶重算为 2399.9768082683。结果尚未获数学验收，新增指数和分片均为 0。[审计及输入摘要](../Research/P3I00193Review/Readme.md)。

## 2026-11-25 支持分割与仓库整理

- 基线提交：[`9d74c34d`](https://github.com/stormwhip/PerfectNumbers/commit/9d74c34dda8908a19542b855c78ef2feb8844b66)。冻结账本 Git blob 为 `3a7b6812aafed3dddd228c34ed9575324d242887`。
- 用 `python3 -I -S -B Research/SupportSplit/Verify.py` 从固定提交的程序和账本复验。结果为 11,398 个组合、4,833 个基础排除、9 个新增条件排除、6,556 个开放组合，完整实际指数新增为 0。[证据表与命令](../Research/SupportSplit/Readme.md)。
- 主证明合并支持分割推导，版本进度表索引各批冻结账本。上午批次的候选排序见[历史快照](https://github.com/stormwhip/PerfectNumbers/blob/9d74c34dda8908a19542b855c78ef2feb8844b66/Research/Nov25/Forecast.md)。当前闭合分片为 2,868，开放分片为 204。
- [本次整理的 GitHub Actions](https://github.com/stormwhip/PerfectNumbers/actions/runs/45618993851)已通过。干净检出验证了 255 个登记证书的摘要与分片投影、SupportSplit 条件排除、历史精确审计及 Python、C++ 回归。
- PR #5 的已验收隔离重放与原始摘要见[发布审计](../Research/Midday/ReleaseAudit.md)。

## 2026-11-24 Euler-source interval replay

- Baseline commit: `37eb94b0a2cd18daed980b902fd913da3420e434`. The input derives from the checked-in exact-exponent exclusions and open shard manifests.
- Replay: Python 3.11.9 on Windows, `python Research/EulerSourceIntervals/VerifyEulerSourceIntervals2400.py --output Build/AuditEulerSourceIntervals2400.json`.
- Root 3: 350 input exponents, 48 with expanded coverage, 3,473 additional Euler-one valuation combinations. Root 5: 183 input exponents, 28 with expanded coverage, 717 additional combinations. The comparison is against the direct valuation and size bound.
- For `(3,1330)`, six exact first-power factors checked. The internal-source replay excludes `f = c` for `s = 1284..1330` and `c = 1` for `s = 1327..1330`. These are branch-level results. See the [historical source-interval report](https://github.com/stormwhip/PerfectNumbers/blob/ea08da38e38ab3309da4360ea2bb60ecb616a025/Documentation/ResearchReport2400.md).

## 2026-11-23 Indicator-capacity proof replay

Replaying the supplied Gemini verifier reproduced its reported 96 exclusions and 29 closures. The corrected verifier prices valuations supplied by factors of the root divisor, handles missing indicator targets in each Euler/supplier branch, and rechecks the supplied rational flows. The merged replay accepted 74 actual exponents and 18 previously open shards. The C++17 generator reproduced both certificate files byte for byte. Seven verifier regression groups passed locally. See the [proof and replay instructions](../Research/IndicatorCapacity/Readme.md).

## Experiment 000 — Repository Reorganization

- Date: 2026-11-22
- Purpose: Normalize the repository into English PascalCase paths; preserve all original source versions and the original PDF.
- Inputs: repository commit `1c7d0661ff1356105e5395b3bb02c49394491ee6`.
- Change: relocate C++, Python, report and reference files; update workflow references and README; make expensive workflows manual.
- Verification: Git tree blob-SHA preservation for relocated source files. Compilation and large-data experiments are pending.
- Proof impact: **none**. No new bound is claimed.

## 2026-11-22 — Independent proof framework and PascalCase structure

- Baseline before renaming: commit `7d7c1c6`. Target: eliminate odd perfect numbers up to `10^2400`.
- Status: original coprime-class certificate independently verified with `log10 N >= 4183.209493`. Original manifest: 3072 top-level exponent shards, no complete independently verified closure.
- Integrated external-pinned Python verifier, SQLite frontier ledger, read-only audit runner, experimental G1 search with V2 frontier codec, and preliminary Worker bridge. Historical proof-tree V21 remains the reference executable.
- Rename `Research/Session20261122/` to `Research/Session20261122/`; rename the local research `README.md` to `Readme.md` while preserving certificate and unmodified prototype blob hashes. Add canonical [current status](../Documentation/CurrentStatus2400.md) and update inbound relative links.
- The directory rewrite and regression workflow do not imply new mathematical results or a 72-hour benchmark.
- Pending: complete SPLIT/LEAF DAG export, original V21 roadblock/conditional LP parity, certified large primes, full original-root acceptance and timing.

## 2026-11-22 — Repository naming and local-link audit

- Base: `7d7c1c6`; repository restructuring commits: `0f9f0c4`, `b19aed8`, `784c07e`.
- Compared old/new remote Git trees: 41 research files relocated, 31 blobs byte-identical and 10 Markdown files updated with status/path references; original/replacement terminal certificate blobs unchanged.
- Current remote tree: 97 tracked files, 20 Markdown documents; all file/folder components meet PascalCase except required GitHub special paths.
- Fetched all 20 Markdown documents and checked relative link targets against the actual remote tree: 0 missing local links.
- Added manual integrity/smoke CI and repository path/link validation script; manual CI remains to be run, so no new Python/C++ test pass is claimed from this restructuring action.
- The mathematical theorem remains `INCOMPLETE_FRONTIER`.

## Imported historical observations (unverified in this session)

- 2012 published reference bound: `10^1500`.
- Historical project handoff reports a V4 15-root proof-tree experiment at exponent 1500 (about 1054 seconds, approximately 33 million branches, zero failed roadblocks).
- Historical handoff reports an LP endgame exponent of about 3129.458561 for the complement of the 15-prime set.
- These entries are not newly reproduced runs. Original claims and parameters are preserved in [historical project snapshot](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70).

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
- Workflow: [RootOrderOptimization.yml](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70).
- Status: source validation and exhaustive profile pending.

## Experiment 013 — Affine state-level LP dual certificates (prototype)

- Date: 2026-11-22.
- For each root-prefix subset \(F\subseteq S_*\), generate one interval-checked dual certificate for the LP with abundance target \(R=2\).
- The same dual multipliers remain feasible when only the abundance RHS changes, yielding a reusable affine lower bound \(L_F(R)=c_F+\lambda_F\ln R\).
- The generator checks 256 prefix masks and compares the affine dual against primal LP objectives at five abundance targets \(R\in\{1.1,1.25,1.5,2,3\}\).
- Runtime DFS can evaluate this bound in constant time using a safe upper bound on the abundancy of already fixed prime powers. The LP deliberately retains all primes outside prefix F, including state-forbidden and already-fixed primes, making it a relaxation.
- Status: Python certificate generation and C++ integration pending.

## Experiment 012 result — Exact subset DP and full-tree validation

- Date: 2026-11-22.
- Exhaustive profile: [Run 44995685025](https://github.com/stormwhip/PerfectNumbers/actions/runs/44995685025), all 1024 transitions PROVEN at exponent 300.
- Exact DP result for exponent 300: both branch-count and measured-time objectives selected \(19,11,7,31,13,3,5,17\), with predicted 14,168 branches and 0.540929 seconds from cold-cache edge sums.
- Complete-tree comparison: [Run 44995684900](https://github.com/stormwhip/PerfectNumbers/actions/runs/44995684900).
- Exponent 300: canonical order 14,238 branches / 0.687752 s; DP order 14,168 branches / 0.644600 s.
- Exponent 500: canonical order 40,733 branches / 7.99203 s; exponent-300 DP order 41,271 branches / 7.80897 s.
- Interpretation: the DP order gives a modest improvement at exponent 300; the exponent-300 optimum does not minimize branch count at exponent 500. A target-specific profile is required. Wall time improved slightly at 500 despite 1.32% more branches, consistent with ordering/cache effects.

## Experiment 015 — Target-specific root-order profile at exponent 500 (queued)

- Date: 2026-11-22.
- Rationale: the exponent-300 optimum increased the branch count at exponent 500, so optimize the exact target used in the next test.
- Method: measure all 1024 subset transitions at exponent 500 with one thread and cold factorization cache per edge; run exact branch-count and elapsed-time subset DP.
- Workflow: [RootOrderOptimization500.yml](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70).

## Experiment 016 — Dual variable-removal gains (V13, pending)

- Date: 2026-11-22.
- For each prefix LP, compute an interval enclosure of every variable's reduced cost.
- If the reduced-cost interval is strictly negative, deleting that variable removes a guaranteed negative upper-bound penalty from the dual objective. The lower endpoint of this gain is accumulated by prime.
- At each state, remove LP variables for primes already forbidden or already represented in the branched set. The original dual remains feasible for the reduced variable set; the gain is added only when the entire reduced-cost interval is negative.
- V13 benchmark compares against V12 on identical root order and targets.
- Status: proof-core tests, certificate generation, and full-root performance pending.

## Experiment 014 result — Affine state-level LP pruning (V12)

- Date: 2026-11-22.
- Certificate generation: [Run 44996209525](https://github.com/stormwhip/PerfectNumbers/actions/runs/44996209525), all 256 prefix certificates generated; direct primal checks at five abundance targets completed.
- Matched-root benchmark: same optimized root order, two threads; [run 44996209525](https://github.com/stormwhip/PerfectNumbers/actions/runs/44996209525).
- Exponent 1000 root 17: V11 7,709 branches / 4.01683 s; V12 7,709 / 3.93147 s; 0 LP cuts.
- Exponent 1000 root 31: V11 21,408 / 9.97656 s; V12 21,408 / 9.95329 s; 0 LP cuts.
- Exponent 1500 root 17: V11 187,909 / 33.9337 s; V12 187,909 / 33.7992 s; V12 added 4 state-level LP cuts.
- Exponent 2201 root 17: both versions timed out at 30 seconds; no completion claim.
- Conclusion: affine LP cut is valid as a relaxation and executes correctly, but its first form provides only marginal gains. V13 adds certified dual gains from removing variables belonging to state-forbidden or already-branched primes.

## Experiment 015 result — Exponent-500 exact root-order DP

- Date: 2026-11-22.
- Completed GitHub Actions [run 44996427816](https://github.com/stormwhip/PerfectNumbers/actions/runs/44996427816).
- All **1024/1024** directed subset transitions completed PROVEN at exponent 500.
- Branch-count-minimizing order: `19,7,11,31,13,3,5,17`, **40,733** branches (summed single-root edges), cost sum **9.184198 s** on the serial cold-cache profiler.
- Measured-time-minimizing order: `19,11,7,31,13,3,5,17`, **41,271** branches, measured-cost sum **9.053779 s**.
- This differs from the exponent-300 branch optimum and reconfirms that ordering optima are target-dependent; the 500 timing advantage of approximately 1.42% is a profile-based estimate, not a fresh complete-tree timing benchmark.
- The branch-minimizing order matches the canonical reduced-root order at exponent 500. Root order alone has not produced a large performance breakthrough.
 
## Experiment 017 — Early-state dual and forced-prime cuts (bounded experiment)

- Date: 2026-11-22.
- Source: `ProofTreeV14.cpp` (moves previously certified affine LP test before forced-prime branching) and `ProofTreeV15.cpp` (adds per-prime forced-option reduced-cost gain), keeping V13 as baseline.
- Model: prefix duals for masks 7 and 127 from the same LP implementation; all other masks use trivial zero affine lower bounds, explicitly recorded by the generator.
- Certificates: `TargetedPrefixCertificates.py` emits `PrefixDualBounds.csv`, `PrefixDualVariableGains.csv`, and `PrefixDualForcedGains.csv`.
- The mathematical gain formula and conditions are documented in `Documentation/ForcedPrimeDualCuts.md`.
- Source compilation and core tests: [Quality run 44998627399](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998627399) **PASS**, including `ProofCoreTestsV14: OK` and `ProofCoreTestsV15: OK`. An earlier quality run had an incorrectly initialized test state; the test fixture was corrected, while the V14/V15 proof-tree source code was unchanged.
- Dataset-backed benchmark: [run 44998508242](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998508242), fixed checksum, two threads; test results to follow.

## Experiment 017 result — V13 / V14 / V15 early-state LP comparison

- Completed [GitHub Actions run 44998508242](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998508242) on 2026-11-22; original run source commit `6f280b542fe004725f141cb4e60b16740a1795d5`.
- All three sources used the same root order \(19,7,11,31,13,3,5,17\), the same checksum-pinned factor database and two OpenMP threads. The targeted certificate generator computed genuinely interval-derived affine bounds for masks **7** and **127**, with 254 safe zero-bound placeholders.
- Generated certificate: mask **7** (forbidden 19,7,11), \(L\approx19.36078970\); mask **127** (forbidden the first seven roots), interval-dual lower exponent **1644.682315669432**. Two-mask generation emitted 119 variable-deletion gains and 1396 forced-prime gains; counts include many primes not reached by benchmark states.
- Exponent **1000**, root **17**: V13 PROVEN, 7,709 branches, 6.03015s, 0 LP cuts; V14 PROVEN, **0 branches**, 0.006410s, 1 early LP cut; V15 PROVEN, **0 branches**, 0.000328s, 1 early LP cut. Single-run submillisecond time is unstable and not an overall tree-speedup measure.
- Exponent **1000**, root **31**: all three PROVEN, **21,408 branches**; times V13 15.192s, V14 15.204s, V15 15.236s; **0 LP cuts** for each.
- Exponent **1500**, root **17**: V13 PROVEN, **187,909 branches**, 52.102s, 4 late LP cuts; V14 PROVEN, **0 branches**, 0.005236s, 1 early LP cut; V15 PROVEN, **0 branches**, 0.005872s, 1 early LP cut. The seven-prime complementary LP bound exceeds \(10^{1500}\), so a first-node cut is mathematically expected; this is a **root-specific simplification**, not evidence for exponent 2300.
- Exponent **2201**, root **17**: all versions TIMEOUT after 30s. At 20s progress: V13 348,799 visited branches, V14 252,930, V15 330,134. Parallel visitation order differs; incomplete counters cannot determine final speedups. No completed root proof or bound improvement at 2201/2300.
- **Conclusion**: early application of the already available affine LP correctly removes a redundant late root for bounds below 1644.68; this insight provides a useful terminal condition for root-order DP at moderate targets. For the intended exponent 2300, we need a substantially stronger state-conditioned LP or separate factor-chain pruning.
- Quality assurance: first V15 test fixture inherited a nonzero known-size field and failed its assertion; the fixture was reset in commit `b4b966848c49bdebfe71c4ba5ba25b0710e32ba2`. [Run 44998627399](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998627399) passed V13/V14/V15 regression tests plus all legacy core checks.

## Experiment 018 — Corrected interval arithmetic for forced-prime LP gains

- Date: 2026-11-22.
- Audit finding: V15 used reduced-cost lower endpoints in both the forced minimum and the baseline penalty. Subtracting a lower bound for the baseline penalty can overstate the forced-prime gain. V15 forced-gain tables are therefore marked non-proof-grade.
- Corrected bound for intervals \(r_i\in[\ell_i,u_i]\):
  \[
  G_q\ge \min_i\ell_i-\sum_i\min(0,u_i).
  \]
- Added `forced_prime_gain_lower` using outward-rounded endpoint conversion and accumulation in `DualGainBounds.py`, exhaustive endpoint regression tests, and V16 C++ accumulation with downward rounding.
- V16 benchmark regenerates the two targeted prefix certificates from the corrected function and compares V13/V14/V15/V16 at exponents 1000, 1500, 2201, and 2300.
- Workflow: [ForcedPrimeLpBenchmark.yml](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70).
- Status: implementation committed; source tests and corrected dataset-backed benchmark pending.

## Experiment 019 — Strengthened eight-prime complement LP crosses exponent 2400

- Date: 2026-11-22. [Initial conditional test 45000659931](https://github.com/stormwhip/PerfectNumbers/actions/runs/45000659931); strengthened-and-repeated [run 45001172416](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001172416).
- Source: `Sources/Python/IntervalCertificate61.py`, a separate auditable LP fork. For precisely `p=61` and exponents `a=10,12`, factor the divisor sums even though `p^a\ge 10^{14}`, adding the resulting exact forced-prime implications to the same LP.
- `sigma(61^10)=199*859*4242586390571`; `sigma(61^12)=187123*14421466756460791`. [Independent exact-product and deterministic-sized primality checks](../Sources/Python/Prime61FactorChecks.py) passed in run 45001172416. All factors are below `2^64`.
- Previously, eight-prime complement `S8={3,5,7,11,13,17,19,31}` had interval-dual exponent lower endpoint **2390.111014293284**. The **enhanced, unconditional-on-61** complement LP gives **2400.822998027028**, exceeding target 2400 by **0.822998027028**. This is a complement-only computational certificate, **not an unconditional OPN bound**.
- The strengthened LP simultaneously reports these exponent-61 subcases, all assuming `N` coprime to `S8`: `61^6 || N`: **2425.846325041447**; `61^10 || N`: **2465.876803180284**; `61^12 || N`: **2511.641527478704**; `nu_61(N)>=16`: **2400.822993303349**; `nu_61(N)>=10`: **2400.822993303349**.
- Exhaustiveness of 61 exponent partition: all odd exponents imply forbidden 31 since `61=-1 mod 31`; even exponents 2,4,8,14 imply one of forbidden `3,5,13,19` through the exact `sigma` identities or `sigma(61^2)|sigma(61^14)`. Remaining possibilities are 6,10,12, and even >=16.
- **Next mathematical gate**: independently audit the entire LP primal relaxation (finite-exponent options, tail, every implication) and recheck a machine-readable dual witness using exact/interval arithmetic; separately finish all eight containing-prime proof trees at exponent 2400. The current 0.823 exponent margin should not be reported as a completed theorem before these steps.

## Experiment 020 — V17 Euler-special-slot coupling (pilot)

- Date: 2026-11-22. Source `ProofTreeV17.cpp`, distinct from V16's corrected independent forced-prime gains.
- For every forced unbranched prime `q`, store interval lower bounds of the cheapest ordinary and Euler-special option, and an upper bound on its baseline negative reduced-cost penalty.
- Since **at most one** forced prime may be special, joint minimum selected reduced cost is bounded by `sum(o_q)-max(0,max_q(o_q-s_q))`, or `sum(o_q)` if the special slot has already been consumed. Its difference from the upper baseline penalty is an outward-rounded LP gain. This **replaces** V16's independent forced gain; the gains are never double-counted.
- Synthetic C++ regression and exhaustive endpoint Python tests pass. First data-backed pilot failed due a V16-only test-fixture leftover. Second pilot failed when the CSV loader rejected subnormal floats and CRLF row endings; both implementation-level issues were corrected in isolated V17 files. Latest pilot [45001125412](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001125412) is the expected decisive comparison.
- The pilot uses two actual prefix dual certificates (masks 7 and 127) and 254 explicitly trivial safe zero lower bounds; complete 256-mask integration is a separate future step.

## Experiment 020 result — V16 versus V17 Euler-coupled pilot

- Date: 2026-11-22. Completed [GitHub Actions run 45001125412](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001125412), same fixed data SHA-256, 2 OpenMP threads, target-prefix LP certificates for masks 7 and 127.
- Source checks: **PASS** in [45001125407](https://github.com/stormwhip/PerfectNumbers/actions/runs/45001125407). Pilot includes `ProofCoreTestsV17: OK`, `EulerDualTests: OK`.
- Three prototype fixes were needed before valid dataset-backed comparison: adapt a V16 test fixture to V17's replaced gain, accept subnormal CSV values, and permit Python csv.writer's CRLF endings in the strict numeric parser. The workflow now fails when any previously-unexpected test case returns UNRESOLVED, rather than merely logging the exception.
- **Exponent 1000, root 31:** V16 PROVEN 21,408 branches, 15.2643s, 0 LP cuts; V17 PROVEN 21,408 branches, 15.1971s, 0 LP cuts.
- **Exponent 1500, root 17:** V16 and V17 PROVEN with 0 branches and one first-node LP cut; times 0.0039564s versus 0.00395872s respectively (unreliable at this duration).
- **Exponent 2201, root 17:** both TIMEOUT at 30s. At 20s, V16 had visited 334,635 branches and reported 6,398 LP cuts; V17 333,745 branches and 6,446 cuts. Incomplete traversal numbers are sensitive to scheduling.
- **Exponent 2300, root 17:** both TIMEOUT at 30s. At 20s, V16 had visited 294,456 branches and reported 566 LP cuts; V17 268,547 branches and 315 cuts. **Do not interpret the lower visited-node count as a speedup**, since neither search completed.
- **Outcome:** the coupled-dual formula and its regression tests are valid computational prototypes, but **no substantive end-to-end runtime improvement has been demonstrated** at the two terminating cases, nor a completed root proof at 2201/2300. The augmented eight-prime complementary LP result >2400 (experiment 019) is the stronger research finding this round.


## Experiment 2026-11-22 — Certified one-node root contradictions and root-order optimization

- Objective: close canonical root shards using independently checkable exact integer arithmetic before invoking the factor-chain search. Root set fixed at `{3,5,7,11,13,17,19,31}`, current order `(19,7,11,31,13,3,5,17)`, target `10^2400`.
- Formal certificate 1, `FORBIDDEN_FACTOR`: `q` is a forbidden earlier odd root dividing `sigma(p^d)`, so `q|N`, contradiction.
- Formal certificate 2, `SIGMA_DIVISOR_SIZE`: since `sigma(p^d)|sigma(p^e)|2N`, and `gcd(p,sigma(p^d))=1`, `p^d*odd(sigma(p^d))|N`. Strictly greater than `10^2400` is a complete one-node contradiction.
- Local independent pure-Python exact integer census (canonical 3,072 options): 14 forbidden-factor branches and 1,382 sigma-size branches, with no overlap. Thus 1,396 direct mathematical closures (45.44%) and 1,676 remaining open at top level. Breakdown by root: 19→129, 7→191, 11→152, 31→116, 13→146, 3→311, 5→217, 17→134.
- Root-order subset DP and exhaustive 40,320 permutations: original root set current combined 1,396, optimum 1,397; replacement root set current combined 1,390, optimum 1,393. Production V21 order is unchanged.
- An additional trial incorporating squared forced factors from small divisors `q<=5000` into these root-level size certificates found **0 extra closures** over 1,396, so it is not enabled. This was a finite pilot, not a universal impossibility result.
- Fixed missing `SigmaPrecheck.hpp` include path in experimental Frontier C++; implemented overflow-safe modular sigma geometric sum and checked equivalent local C++ source against GMP in 36,100 exact cases (PASS). Pushed repository test source and updated manual CI workflow.
- Added `DirectRootClosures2400.py`, `DirectRootClosuresTests.py`, `AuditDirectRoot2400.py`, `RootOrderDirectClosureDP.py`; extended `IndependentVerifierV2.py` and `AuditRunner2400.py` to accept mathematically verified one-node DAGs without relying on solver `PROVEN` status.
- Current validation: independent local integer experiments and local C++ GMP differential test passed. **GitHub-side direct Python verifier tests, the archived terminal-certificate + 3,072-shard audit, and the updated repository CI have not yet been run in this session.** No completed 72-hour proof or unconditional bound is claimed.
- Detailed proof, reproduction commands and open problems: [DirectRootClosure2400.md](../Research/Session20261122/Reports/DirectRootClosure2400.md).

## 2026-11-23 — Cyclotomic finite-quotient closure pilot

- Derived the restriction `q = 1 (mod 2(d+1))` for every prime factor of `sigma(p^d)=Phi_{d+1}(p)` when `d+1` is odd prime and greater than `p`.
- Bounded `sigma(A)/A` by the exact rational expression `2m/(2m-C)`, where `C=1+ceil(log2(omega_upper(A)))`, without factoring the 1,000+-digit integer `A`.
- Enumerated every admissible odd quotient `Q=N/(p^d A)` for three previously open tasks, using exact abundance, Euler structure, sigma forcing and forbidden-root contradictions: `(19,936):705908`, `(11,1150):28471`, `(11,1152):2`. All **734,381** candidates were excluded.
- New verifier leaf: `FINITE_QUOTIENT_CYCLOTOMIC`, restricted to the three fixed original-partition root pins. Added `FiniteQuotientClosure2400.py`, independent verifier integration, `FiniteQuotientClosureTests.py`, and manual CI regression entry.
- Current local integer-verified research total: 1,396 immediate certificates + 3 finite exhaustive certificates = **1,399/3,072**; open candidate tasks **1,673**. Fresh GitHub CI/full manifest audit and 72-hour end-to-end verification remain pending; theorem status is `INCOMPLETE_FRONTIER`.
- Proof and reproduction: [FiniteQuotientCyclotomic2400.md](../Research/Session20261122/Reports/FiniteQuotientCyclotomic2400.md).


## 2026-11-23 — Certified forced-prime exponent closure and bounded progression scan

- Root order \`(19,7,11,31,13,3,5,17)\`; last full auditable census: 1,628 accepted, 1,444 open out of 3,072.
- Independent exact integer proof for previously open \`P3_I00368\` (\`p=3,d=2476\`): \`q=980893\` is prime and divides \`sigma(3^2476)\` to exact valuation one. Size bound requires \`v_q(N)<=7\`. Legal exponent cases \`1,2,4,5,6\` each contradict a forbidden prime divisor of \`sigma(q^e)\` or \`lcm(3^d*sigma(3^d),q^e,sigma(3^d)*odd(sigma(q^e))) > 10^2400\`. Exact integers were checked locally; forced LCMs have 2,405 and 2,429 decimal digits for exponents 4 and 6.
- Independent root-only certificate implementation, verifier rule \`FORCED_PRIME_EXPONENT_EXHAUSTION\`, positive/negative regression, and CI smoke command committed. Expected direct-root census 1,448 (formerly 1,447); full merged audit is projected at 1,629/3,072 accepted but **has not been rerun**. Official completed merged-audit baseline remains 1,628.
- Optimization: when \`m=d+1\` is prime and \`m>p\`, enumerate candidate forced primes only in \`q=1 (mod 2m)\`. Restartable scanner writes JSONL \`PROGRESS\` and \`CLOSED\` witnesses. Its \`SEARCHED_OPEN\` records are inconclusive rather than proofs.
- Local standard-library Python pilot (approximate development-machine wall times): all roots, residual<=500 digits, \`q<=2e6\`: 299 scanned, 4 identified forced-prime closed leaves (three overlapped existing baseline), ~0.38 s; root 3, \`q<=1e8\`, residual<=500: 68 scanned, one closed, ~0.83 s; root 5, \`q<=1e8\`, residual<=1000: 99 scanned, none closed, ~1.75 s. An all-root \`q<=2e9\` development run was interrupted at 120 seconds with only a partial checkpoint and **no full-result claim**.
- New report: [ForcedPrimeExponentPilot2400.md](../Research/Session20261123/Reports/ForcedPrimeExponentPilot2400.md). Runtime verification: \`python3 Research/Session20261122/Python/ForcedPrimeExponentClosure2400.py --verify --root 3 --exponent 2476 --forced-prime 980893\`. Six-hour optional scan: \`python3 -u Research/Session20261122/Python/ForcedPrimeExponentClosure2400.py --root all --prime-limit 2000000000 --residual-digits 1000 --hours 6 --checkpoint Build/ForcedPrimeScan2400.jsonl\`.
- Status remains \`INCOMPLETE_FRONTIER\`; no complete 72h end-to-end run and no unconditional \`10^2400\` theorem.

## 2026-11-23 — Fermat root valuation and supplier proofs at exponent 2400

- Rebuilt all 3,072 canonical shards and 5,090 legal exponents for roots 3 and 5. The standard-library verifier accepted both checked-in CSVs. The standalone multiplicative verifier independently replayed 135 root-3 and 106 root-5 shards.
- Replayed the original coprime certificate and root-class audit. The historical proofs cover 1,629 shards, with 65 in common with the 241 Fermat root proofs. The merged audit added 176 closures and returned 1,805 closed, 1,267 open, and `INCOMPLETE_FRONTIER`.
- Replay commands and proofs are in [FermatRootValuationReport.md](../Research/FermatRootValuation/FermatRootValuationReport.md).

## 2026-11-23 — Supplier-product and valuation-dual batch

- Parent audit: `26cb81d5c95a6d6505b54b3ef78fd52edf920f9d`. Replay with `python3 Research/SupplierBatch/VerifyBatch2400.py --output Build/AuditSummary2400.json`.
- Exact replay added 40 shards via 51 actual-exponent exclusions and six via finite factor trees. The merged audit returned 1,851 closed, 1,221 open, and `INCOMPLETE_FRONTIER`.
- [Proof notes](../Research/SupplierBatch/PerfectNumbers2400BatchReport.md) · [machine-readable audit](../Research/SupplierBatch/BatchAudit2400.json).

## 2026-11-24 — Teichmüller valuation pricing for roots 19, 7, 11, 31, 13

- Parent audit: `Research/IndicatorCapacity/Audit2400.json` (1,869 closed, 1,203 open), replayed in full before the new rule is applied.
- New rule: `v_p(sigma(r^f)) = lambda(r) + v_p((f+1)/o)` with `o = ord_p(r)`. A prime of p-adic level `t` is either `> p^t` or equals the Teichmüller lift `a^(p^(t-1)) mod p^t`. The finitely many lifts that are cheap form a constant deficit `U`, so the non-Euler part of `N` is at least `p^(kappa*K)/U` with `kappa = 2,2,4,2,2`. The Euler branches give `N >= p^(3e)/U` (exponent >= 5) or `(2p^s-1) p^e max(A, p^(kappa(e-s))/U)` (exponent 1).
- Result: 146 new shard closures (19:24, 7:32, 11:42, 31:21, 13:27). The merged audit reproduced 2,015 closed and 1,057 open, with status `INCOMPLETE_FRONTIER`. All six regression groups passed.
- Independent check: a separate computation used digit-by-digit Hensel lifting, SymPy primality testing and exact fractions. It reproduced every new shard ID, its full list of actual exponents and rules, and the remaining manifest. Of the 173 distinct root/exponent pairs covered by the additions, 146 use the new rule and 27 use the prior size inequality.
- Replay: `python3 Research/TeichmullerValuation/AuditTeichmullerValuation2400.py --output Build/AuditTeichmuller2400.json`. Proof: [Readme](../Research/TeichmullerValuation/Readme.md).


## 2026-11-25 晚间：支持集合与指数分割

冻结午间账本 blob `3a7b6812aafed3dddd228c34ed9575324d242887`。精确有理数本地筛选 11,398 个支持组合，基础排除 4,833；一层分割新增 8，低指数二层分割新增 1，余 6,556。未与历史条件叶去重，无完整实际指数/规范分片新增。证明及复验状态见 [SupportSplit](../Research/SupportSplit/Readme.md)，发布版复验器已提交，待干净检出执行。未使用付费计算资源。

## 2026-11-25 根 3 联合模型续研

独立整数验证排除五指数的 E0/E1/E2；42 叶保守重算、5829 来源素数、34972 余块检查已执行。重建最弱叶对偶为 169.4957938419；全池丰度检查发现 7 叶仍低于目标。已保存七叶的共同池实验。新增完整实际指数及闭合分片均为 0。[推导和重放入口](../Research/P3I00193Review/Progress.md)。
