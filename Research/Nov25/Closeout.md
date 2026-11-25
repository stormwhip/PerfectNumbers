# 11 月 25 日研究收尾

本页以 PR #3 的固定提交 `e89dffd5a74debad80f695d6177f3d785e6268e8` 和其 [Audit.json](../NightMerge/Audit.json) 为比较基准。基线的 **2,646 / 3,072** 个闭合分片、426 个开放分片、562 个待证实际指数均保持原样。该阶段证书已随 [PR #4](https://github.com/stormwhip/PerfectNumbers/pull/4) 合并。

## 净增账本

| 根 p | 净排除实际指数 | 新闭合分片 | 剩余分片 | 剩余实际指数 |
|---:|---:|---:|---:|---:|
| 3 | 0 | 0 | 44 | 62 |
| 5 | 2 | 2 | 13 | 14 |
| 7 | 5 | 2 | 138 | 181 |
| 11 | 6 | 3 | 80 | 96 |
| 13 | 16 | 5 | 36 | 42 |
| 19 | 17 | 5 | 69 | 89 |
| 31 | 5 | 3 | 26 | 27 |
| **合计** | **51** | **20** | **406** | **511** |

累计 **2,666 / 3,072** 闭合，剩余 406 片中 365 片只剩一个实际指数。所有数字用 `(p,e)` 去重；一个分片只有全部剩余实际指数均被排除时才算闭合。[Delta.json](Delta.json) 包含完整净增、已闭合 ID 和逐片剩余指数。全局结论仍为 `INCOMPLETE_FRONTIER`；还没有证明完整的 `10^2400` 下界。

## 复验范围

新增 51 项在干净隔离工作树、证明提交 `d7671d9f` 上用标准库离线冷复验全部通过。独立聚合、证书清单 SHA-256、覆盖与去重回归也全部通过。另有 18 个条件包通过主复验，其中 13 个正支持子类和 4 个校准终局通过独立复验，1 个加权校准只做主复验。这 18 包不计作完整指数；同样不计概率素性、未决指数窗、浮点 LP 或搜索耗尽。

```text
python -I -S -B Research/Nov25/Ledger.py --workers 10 --check Research/Nov25/Delta.json
python -I -S -B Research/Nov25/ValidateLedgerIndependent.py
python -I -S -B Research/Nov25/ProofManifest.py --check
python -I -S -B Research/Nov25/RunLedgerChecks.py
python -I -S -B Research/Nov25/Five/Simple520.py
```

固定基线在另一干净工作树用 `python -I -S -B Research/NightMerge/Checkpoint.py --manifest-only` 恢复原清点；这不是对历史证书的全量验证。全量 `ParallelReplay.py --fresh` 另行限时尝试；不把未完成任务算作通过。其状态与通过任务见[历史基线部分冷验回执](BaselineColdPartial.json)。该回执不进入本轮净增账本。

## 后续进展

午间并集及其后工作见[当前状态](../../Documentation/CurrentStatus2400.md)和[下一步计划](../../Documentation/NextPlan2400.md)。本批次结束时的候选排序见[冻结计划](https://github.com/stormwhip/PerfectNumbers/blob/9d74c34dda8908a19542b855c78ef2feb8844b66/Research/Nov25/Forecast.md)。

[研究说明与复验入口](README.md) · [证书哈希清单](ProofManifest.json) · [本批剩余清单](Delta.json)
