# Native roadblock pilot and root-coverage audit

> **进度标注（2026-11-22）**：本文记录对应阶段的数学推导、实验数据和当时的搜索状态。最新研究进度、独立验证器 V2、可恢复前沿及全量未闭合项目，统一见 [CurrentStatus2400.md](../../../Documentation/CurrentStatus2400.md)。本文历史计时和程序 `PROVEN` 均不作为 `10^2400` 完整证明。


## Native selector

The experimental branch uses V21 with an optional \(2^{40}\) fixed-point roadblock check. Shadow mode evaluates the new selector and retains the historical branching decision. Certified mode uses the legacy boundary as an initial proposal, then expands the candidate boundary after failed attempts. Each attempt tests a cheap multiplier and up to 14 supergradient steps. A returned boundary passes a strict integer comparison; an exhausted search returns an unresolved node. The pilot does not use the legacy result as a fallback witness. The bounded search need not find the smallest certifiable boundary.

The size allowance is rebuilt from downward logarithms of expanded prime powers and disjoint, counted residuals. The abundance deficit uses upper endpoints, conservative maximum abundances for standard branches, and verified residual factor-count bounds. The selector can use the same checked cutoff product to strengthen residuals. A slacker set of modular exclusions in the candidate table preserves a valid lower bound. The experiment covers the roadblock decision under V21's factor and state assumptions. Other V21 pruning and probable-prime assumptions still require independent proof witnesses.

The standalone C++17 core passed endpoint monotonicity checks through 300,000 and strict comparison tests. A separate local differential test checked 12,007 native log intervals against the narrower Python integer intervals, including near-one ratios and 48-bit operands.

## Matched shard pilots

The two runs on shards 35, 130, 0 and 100 used the same runner within each comparison, two OpenMP threads, the same input database and tables, and a 45-second cap.

| Root-19 shard | Legacy, after the overlap fix | Certified mode, after the overlap fix |
| --- | --- | --- |
| 35 | Reported PROVEN, 2.056 s | Reported PROVEN, 1.738 s |
| 130 | Reported PROVEN, 0.113 s | Reported PROVEN, 0.133 s |
| 0 | TIMEOUT | TIMEOUT |
| 100 | TIMEOUT | TIMEOUT |

The completed shards had the same counts (45,987 and 2,230) and zero circular branches. Neither difficult shard reached a roadblock in the initial 45-second window. In the first run, at about 40 seconds, legacy visited 951,508 and 1,724,433 nodes on shards 0 and 100 respectively; certified mode visited 958,855 and 1,725,621. Both modes reported zero circular branches and zero state-LP prunes at that point. The comparison therefore gives no evidence of a roadblock speed gain for those difficult shards.

- [First matched run and raw logs](https://github.com/stormwhip/PerfectNumbers/actions/runs/45028889201)
- [Matched repeat with the overlap fix](https://github.com/stormwhip/PerfectNumbers/actions/runs/45029205305)
- [Historical census identifying reached-roadblock shards](https://github.com/stormwhip/PerfectNumbers/actions/runs/45005912683)

## Reached-roadblock cohort

The historically identified shards 66, 132, 138 and 149 were each tested in legacy, shadow and certified mode. All 12 runs returned the program's `PROVEN` status with zero failed roadblocks.

| Root-19 shard | Legacy elapsed | Shadow elapsed | Certified elapsed |
| --- | ---: | ---: | ---: |
| 66 | 0.693 s | 1.146 s | 1.063 s |
| 132 | 0.370 s | 0.832 s | 0.809 s |
| 138 | 0.648 s | 0.898 s | 0.869 s |
| 149 | 0.318 s | 0.450 s | 0.449 s |

Each of shadow and certified mode logged 25 reached-node decisions. In both samples, 24 used the historical boundary and one expanded it from 277 to 554. The bounded search failing at 277 is not a refutation of the old boundary. In certified mode, shard 66 explored 27,424 branches versus 26,642 in legacy mode; the other three branch totals stayed identical. The certified mode lost wall time on all four matched shards. These single-run measurements include process initialization, the legacy proposal, and integer rechecking. They support keeping the native implementation on the experimental branch. [Reached-node run and raw logs](https://github.com/stormwhip/PerfectNumbers/actions/runs/45029482863)

## Correctness fix for circular sizing

When the circular search selects an unexpanded \(q\) that is already a factor of a counted residual \(c\), the old exponent budget can charge both \(c\) and an exponent of \(q\). For example \(q=1009\) and \(c=1009\cdot1013\) permit a size requirement of \(\operatorname{lcm}(q^2,c)=1009^2\cdot1013\). Charging \(q^2c\) can omit the exponent-2 branch for a budget between those integers. This is a counterexample to the size-accounting rule. It does not establish that a particular previously completed shard omitted a feasible state.

The fix registers the chosen prime in the set of known unexpanded primes and reruns disjoint residual accounting before exponent enumeration or the branch size check. Dropping the overlapping residual from the size sum is conservative. The C++ regression checks that the exponent-2 option is restored in this case. [Main CI](https://github.com/stormwhip/PerfectNumbers/actions/runs/45029521634)

## Independent top-level coverage

The included Python verifier uses exact powers to find the maximum possible exponent at each root, then marks every legal ordinary and Euler exponent covered by at least one scheduled option. For a standard option \(d\), divisibility \(d+1\mid e+1\) implies \(\sigma(p^d)\mid\sigma(p^e)\). For \(p=3\), if \(e+1\) has only prime factors 3 and 5, exact exponents 2 and 4 handle \(e+1=3,5\), while the remaining multiples of 9, 15, or 25 are covered by standard options. For \(p=7\), the corresponding single excluded prime is 3, so exact exponent 2 and the standard multiple of 9 suffice. Root classes are disjoint by the first included prime; exponent tasks within one class can overlap.

The verifier counts 3,072 reference tasks for the original set and 3,058 for its \(19\to23\) replacement. It matched all 287 actual C++ root-19 task entries in the first pilot, in listing order, and rejected a modified task exponent. Both prior terminal certificates were independently rerun. The count for the replacement is a mathematical reference partition, since V21's root and prefix tables still use the original set.

## Outstanding

Complete an eight-class search on one fixed root set, independently verify all internal branch and closure witnesses, and measure the full wall time on declared hardware. The scheduler's per-shard completion records and the root manifest audit alone cannot verify the internal search tree. The timeouts and matched samples above yield no supported finite upper bound for the full run.
