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
