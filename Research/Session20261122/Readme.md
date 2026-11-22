# 2026-11-22 证明树研究原型归档

本目录保存 V21 的函数级剖析与 V22–V24 的候选优化。它们来自 [原始研究分支 research/exact-sigma-size-v22](https://github.com/stormwhip/PerfectNumbers/tree/research/exact-sigma-size-v22)，复制为可追溯的独立研究材料。

**正式主分支搜索基线仍是 [ProofTreeV21.cpp](../../Sources/Cpp/ProofTreeV21.cpp)。** 新增的 V2 独立验证器、前沿账本、G1 实验搜索器目前处于小规模测试及集成阶段。当前整体状态见 [CurrentStatus2400.md](../../Documentation/CurrentStatus2400.md)。

## C++ 原型及回归

| 文件 | 功能 | 当前判断 |
| --- | --- | --- |
| [ProofTreeV21Profile.cpp](Cpp/ProofTreeV21Profile.cpp) | 给 V21 的因子和、素性、数据库、LP、残余与状态复制计时 | 性能诊断工具 |
| [ExactSigmaDivisor.hpp](Cpp/ExactSigmaDivisor.hpp) | 精确 \(\sigma(p^a)\) 奇数部分整除及乘积 LCM 原语 | 数学规则与测试 |
| [ProofTreeV22.cpp](Cpp/ProofTreeV22.cpp) | 精确整除剪枝与延迟触发实验 | 完成分片耗时增加 |
| [ProofTreeV23.cpp](Cpp/ProofTreeV23.cpp) | 避免对未改变残余进行第二次 GMP 素性检测 | 两个完成分片性能改善 |
| [ProofTreeV24.cpp](Cpp/ProofTreeV24.cpp) | 用乘积 GCD 替代残余的逐项互素检查 | 混合性能结果 |
| [ProofCoreTestsV22.cpp](Cpp/ProofCoreTestsV22.cpp) | V22 原语与回归 | CI 通过 |
| [ProofCoreTestsV23.cpp](Cpp/ProofCoreTestsV23.cpp) | V23 基础回归 | CI 通过 |
| [ProofCoreTestsV24.cpp](Cpp/ProofCoreTestsV24.cpp) | V24 与 V21 的 4,000 组差分测试 | CI 通过 |

此目录内的 C++ 文件保留了相互 `#include` 的原文件名。例：

```bash
g++ -std=c++17 -O2 -fopenmp Research/Session20261122/Cpp/ProofCoreTestsV24.cpp -lgmpxx -lgmp -o /tmp/ProofCoreTestsV24
/tmp/ProofCoreTestsV24
```

## 实验报告与固定证据

- [V22 精确整除剪枝理论与负向实验](Reports/ExactSigmaDivisibilityV22.md)：[首轮 CI](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011182741)、[延迟版 CI](https://github.com/stormwhip/PerfectNumbers/actions/runs/45011614919)。
- [V23 去重复素性检测](Reports/V23PrimalityPerformance.md)：[对照 CI](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012354324)，完整分片性能改善约 25%–30%。
- [V24 合数残余乘积 GCD](Reports/V24CompositePerformance.md)：[对照 CI](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012698021)，等价性测试通过，性能尚不稳定。
- [V21 函数开销剖析](https://github.com/stormwhip/PerfectNumbers/actions/runs/45012070442)。

原研究分支保留 [ExactSigmaV22Pilot.yml](https://github.com/stormwhip/PerfectNumbers/blob/research/exact-sigma-size-v22/.github/workflows/ExactSigmaV22Pilot.yml)、[V23PrimalityPilot.yml](https://github.com/stormwhip/PerfectNumbers/blob/research/exact-sigma-size-v22/.github/workflows/V23PrimalityPilot.yml)、[V24CompositePilot.yml](https://github.com/stormwhip/PerfectNumbers/blob/research/exact-sigma-size-v22/.github/workflows/V24CompositePilot.yml) 和 [ProofTreeV21Profiler.yml](https://github.com/stormwhip/PerfectNumbers/blob/research/exact-sigma-size-v22/.github/workflows/ProofTreeV21Profiler.yml)；归档代码与研究分支对应版本一致。

## Roadblock 对偶研究

- [固定点对偶原型](Python/RoadblockDual.py)与[复现实验](Python/RoadblockDualTests.py)。
- [理论推导、实验结果与接入难点](Reports/CertifiedRoadblockDual.md)。

## 终局 LP 证书与分界扫描

- [终局证书、路障事件扫描与复现](Reports/CertifiedTerminalAndBoundaryProfile.md)。
- [证书验证器](Python/TerminalCertificate.py)、[原根集证书](Certificates/TerminalOriginal.json.gz)、[替换根集证书](Certificates/TerminalReplacement.json.gz)。
- [分界扫描原型](Python/RoadblockBoundaryProfile.py)及[随机差分测试](Python/RoadblockBoundaryProfileTests.py)。

## 路障乘子精确搜索

- [整数格点二分推导与实测](Reports/RoadblockMultiplierSearch.md)。
- [参考实现](Python/RoadblockMultiplierSearch.py)和[穷举对照](Python/RoadblockMultiplierSearchTests.py)。

## 下一步数学研究

优先推进 [形式化难题 IV：状态条件化 LP 早期剪枝](../../Documentation/ResearchProblems2400.md#5-核心难题-iv可早期证明的状态条件化-lp-剪枝)。需要同时保持证明完备性、可校验证书，以及在完整困难分片上的总运行时收益。


## 2026-11-22 独立验证与可恢复前沿

[独立验证集成总报告](Reports/IndependentProofIntegration2400.md) 详细列出 V2 验证器、SQLite 账本、全量审计、G1 实验搜索器及所有未完成工作。

| 组件 | 路径 | 当前状态 |
| --- | --- | --- |
| V2 独立验证器 | [IndependentVerifierV2.py](Python/IndependentVerifierV2.py) | 已有合成与篡改测试；尚未核验全量真实 DAG |
| 前沿账本 | [FrontierLedgerV2.py](Python/FrontierLedgerV2.py) | 有原子提交与故障注入 |
| 全量验收 | [AuditRunner2400.py](Python/AuditRunner2400.py) | 完整清单逻辑；仍需全部真实证书 |
| Worker 桥接 | [FrontierWorkerDriver.py](Python/FrontierWorkerDriver.py) | 初步接口；闭合证书输出尚未打通 |
| V21 Frontier | [ProofTreeV21Frontier.cpp](../../Sources/Cpp/ProofTreeV21Frontier.cpp) | G1 已集成，完整路障/LP 待接入 |
| 单飞缓存 | [SingleFlightFactCache.hpp](../../Sources/Cpp/SingleFlightFactCache.hpp) | 独立实现；未集成真实因子查询 |

完整原根集 3,072 项与 72 小时验收尚未完成。

## 2026-11-22 independent proof integration

See [IndependentProofIntegration2400.md](Reports/IndependentProofIntegration2400.md) for the external-pin verifier, durable frontier ledger, V21 frontier codec, proof audits, exact mathematical obligations and unresolved 10^2400 blockers. The experimental searcher's `PROVEN_UNAUDITED` is not an independently certified theorem. New regression checks: `PrimeCutoffGCDTests.py` and `SingleFlightFactCacheTests.cpp`.
