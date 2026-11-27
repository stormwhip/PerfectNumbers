# 最终验证摘要

**状态：INCOMPLETE_FRONTIER；不是 PROVED。** 验收基线及增量的逻辑层级如下，各项不可混算。

|层级|实际结果|能证明什么|
|---|---|---|
|顶层指数与八根互素类|3072 个分片编号及旧/新 82/57 条键关联重算；互素类整数对偶 floor=4183.209493|覆盖顶层问题，不证明所有分片原有叶节点|
|历史指定的五个入口|全部直接 PASS；[命令、耗时、换行错误及修复](Audit/Baseline.md)|指定历史账本和算术包通过，不是全历史冷验|
|本轮 25 个完整键|各自独立复跑其完整依赖，全部通过，时间见[逐键列表](Proof.md)|在其规范类中排除每个精确键|
|完整键到分片|[独立投影](AuditNext/Projection25.md)：一对一清空 25 个单键片，其他成员无变化|3029 闭、43 开、53 键、35 单键片|
|清洁检出确认|在 b41e79d2 的 LF 工作树通过结构/项目投影、两个根集合的原始指数枚举；在 cdbd4793 的另一清洁工作树验证数字及 3072 片。Windows 与 WSL CPython 3.14.4 均重算投影|排除了原工作区未跟踪文件导致的统计偏差|
|五键冻结集成回归|[完整 PASS，3124.604 秒](ColdBatch.md)|该提交的全部新入口串行完成；有采样 CPU/RSS|
|两个额外的大批次|[完整明细](AdditionalReplay.json)：98/148 和 110/285 回执为正，其余在截止前停止，未取得结论|不可算成全仓端到端通过，亦非数学否定|

从 Git 原始内容运行时保留断言，勿用 -O。快速交付检查：

~~~sh
python Sources/Python/RepositoryStructureChecks.py
python -I -S -B Research/FinalNight2400/AuditCoverage.py
python -I -S -B Research/FinalNight2400/ReportChecks.py
python -I -S -B Research/FinalNight2400/Project.py
~~~

完整新增算术入口为 [Verify.py](Verify.py)；不带参数重放其中列出的逐键证明和局部补充，投影程序单独运行不能认证这些数学命题。全定理尚有 43 个非空余集，旧证明的全局依赖、逐证书的端到端冷重放与 72 小时验收仍未完成。
