# Research Milestones

| Milestone | Status | Supporting evidence | Next gate |
| --- | --- | --- | --- |
| 2012 published bound \(N>10^{1500}\) | Published external reference | [OchemRao2012](../References/OchemRao2012.pdf) | Reproduce locally for regression |
| Local V4 search at exponent 1500 | Reported in historical handoff | [LegacyResearchHandoff](../Documentation/LegacyResearchHandoff.md) | Recover full run log and repeat independently |
| Complement-case LP endgame around exponent 3129 | GitHub computation observed; mathematical audit open | [Python workflow run 44990184125](https://github.com/stormwhip/PerfectNumbers/actions/runs/44990184125) | Independently audit the model and interval dual certificate |
| GitHub directory and filename normalization | Completed 2026-11-22 | Reorganization commit | Compile and test renamed entry points |
| V6 conservative roadblock and composite accounting | Core regression passed (2026-11-22) | [ProofTreeV6](../Sources/Cpp/ProofTreeV6.cpp) and [ProofCoreTests](../Sources/Cpp/ProofCoreTests.cpp) | Compilation and core checks passed; dataset-backed V5/V6 benchmark pending |
| V7 block-parallel heavy roadblocks | Compilation and core checks passed; performance pending | [ProofTreeV7](../Sources/Cpp/ProofTreeV7.cpp) | Multi-thread equivalence, regression and benchmark |
| V8 periodic diagnostics | Completed; 50s progress measured | [Probe 44991559032](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991559032) | Optimize ordinary DFS; large roadblocks were not encountered |
| V9 deep task scheduling | Terminating-case comparison completed | [Run 44992192309](https://github.com/stormwhip/PerfectNumbers/actions/runs/44992192309) | Repeat measurements; strengthen pruning for exponent 2201 |
| Complete unconditional exponent 2200 | Not yet verified in this project | [Bounded exponent-2201 probe](https://github.com/stormwhip/PerfectNumbers/actions/runs/44991101998) timed out on roots 17 and 307 | Instrument high-exponent searches, optimize, then prove all 15 roots plus audited endgame |
| Exceed unconditional exponent 2200 | Research target | Pending | Reproducible, rigorously checked proof tree and certificate |

The numerical LP bound applies to the complementary forbidden-prime-free case. It must be combined with independently certified factor-chain branches to establish an unconditional lower bound.

| Reduced prime set for exponent 2300 | Eight-prime candidate with interval-dual output | [Run 44993433027](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993433027) | Independent LP audit and reduced-set proof-tree benchmarking |

| V10 prime-adic obligation cuts | Candidate, quality checks pending | [ProofTreeV10](../Sources/Cpp/ProofTreeV10.cpp) | Compile, regress, and compare complete roots |

| V10 valuation-cut benchmark | Completed; no material branch reduction at measured targets | [Run 44993733799](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993733799) | Target cuts on states with substantial repeated factor valuations |
| Reduced eight-root tree benchmark | Completed; slower at exponent 300 and 500 | [Run 44993825296](https://github.com/stormwhip/PerfectNumbers/actions/runs/44993825296) | Optimize root order and deep-pruning policies |

| V11 root-order subset DP | Profiler and exact optimizer implemented; full 1024-edge run pending | [RootOrderProfiler](../Sources/Cpp/RootOrderProfiler.cpp) | Compare optimal order against canonical order at 300 and 500 |

| V11 root-order subset DP | 1024/1024 edges proven; complete-tree gains modest and target-dependent | [Run 44995684900](https://github.com/stormwhip/PerfectNumbers/actions/runs/44995684900) | Profile at exponent 500 before selecting production order |

| V12 affine state-level LP | 256 interval-derived prefix certificates generated; 4 extra cuts in one completed test | [Run 44996209525](https://github.com/stormwhip/PerfectNumbers/actions/runs/44996209525) | Add state-forbidden variable-removal gains (V13) |

| Exponent-500 exact subset DP | All 1024 edges completed; branch-optimal canonical order, distinct time optimum | [Run 44996427816](https://github.com/stormwhip/PerfectNumbers/actions/runs/44996427816) | Assess higher-exponent transferability |
| Early-state V14 and forced-prime V15 | Both compile and core tests pass; matched benchmark running | [Run 44998627399](https://github.com/stormwhip/PerfectNumbers/actions/runs/44998627399) | Quantify early LP cuts and compare complete roots |
