# 续研短检查点 · 11-28 00:52 北京时间，截止 07:30

main 基线 1447d41b；研究分支 research/final-night-20261127，已推送 8fb5ef61，[PR 10](https://github.com/stormwhip/PerfectNumbers/pull/10)，不合并。12 个新完整键见[总索引](Proof.md)。[投影](OpenFrontier.json)：3016/3072 闭片、56 开片、66 键、48 单键片。全局仍 INCOMPLETE_FRONTIER。历史五入口全部通过；[五键冻结回归](ColdBatch.md) 3124.604 秒，非全历史冷重放。

近端：19^618 仅余 2477 的赋值 2；3^12 仅余 797161 的 1、96。主攻 11^396 已正式登记 114/116，剩 2、8。19^312、7^430、19^372 已完整计入。19^618 全键候选等待独立重放。发现脚本 Build/GP396.py、Price396.py 与 Resolve396.py 持久保存每个子树，区分候选文件和已封存包。继续用 job_list 取活跃任务，按 job_output 收取，不重复运算。团队按当前 task board；审阅结论按[结果账本](Results.json)而非聊天摘要。待合入有多个已验证条件包，非全键不减片。避免整目录暂存，结构检查和独立算术都须通过。
