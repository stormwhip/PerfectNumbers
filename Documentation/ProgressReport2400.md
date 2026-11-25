# 证明版本进度

[当前状态](CurrentStatus2400.md)提供逐根账本，[总证明](Proof2400.md)集中数学推导，[实验日志](../Records/ExperimentLog.md)保存参数和观测记录。V21 为冻结搜索基线。V2 为独立验证框架及实验性前沿。下表中的分片数为各批次已核对的累计值。

| 批次 | 闭合 / 3,072 | 开放 | 冻结证据 |
|---|---:|---:|---|
| 根 3、5 赋值与来源 | 1,805 | 1,267 | [复验报告](../Research/FermatRootValuation/FermatRootValuationReport.md) |
| 批量来源与扩大因子链 | 1,851 | 1,221 | [审计](../Research/SupplierBatch/BatchAudit2400.json) |
| 指标容量 | 1,869 | 1,203 | [审计](../Research/IndicatorCapacity/Audit2400.json) |
| Teichmüller 提升 | 2,015 | 1,057 | [审计](../Research/TeichmullerValuation/Audit2400.json) |
| Gemini 批次并集 | 2,027 | 1,045 | [审计](../Research/TeichmullerValuation/GeminiBatchAudit2400.json) |
| 来源间隙与多根因子链并集 | 2,192 | 880 | [审计](../Research/EveningMerge/Audit.json) |
| 夜间并集 | 2,646 | 426 | [审计](../Research/NightMerge/Audit.json) |
| 11 月 25 日上午 | 2,666 | 406 | [账本](../Research/Nov25/Delta.json) |
| 11 月 25 日午间 | 2,868 | 204 | [账本](../Research/Midday/Delta.json) |
| 11 月 25 日 SupportSplit | 2,868 | 204 | [九项条件排除](../Research/SupportSplit/Readme.md) |

原八根互素类的认证下界为 $\log_{10}N\ge4183.209493$。将根 $19$ 换为 $23$ 后，替换根集的互素类下界为 $\log_{10}N\ge3954.197016$，作为独立的历史实验保留。

历史进展报告的工程细节、性能试验和快照引用见[整理前报告](https://github.com/stormwhip/PerfectNumbers/blob/9d74c34dda8908a19542b855c78ef2feb8844b66/Documentation/ProgressReport2400.md)。
