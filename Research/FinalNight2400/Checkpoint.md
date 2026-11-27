# 续研短检查点 · 2026-11-27 23:58 北京时间

- 截止：11-28 07:30 +08。持续研究目标已启用。工作根 E:/PerfectNumbers；唯一发布分支 research/final-night-20261127；[PR 10](https://github.com/stormwhip/PerfectNumbers/pull/10) 仅草稿，不合并。main 实查 1447d41b806f43ec5775e0cef7eaa7739ab67388。最近数学提交 a90bfe48eea50373ff68f797823973f07c922f67。
- [逐片账本](OpenFrontier.json)：3004→3012 闭片，68→60 开片，78→70 键，60→52 单键片。完整排除 (19,58),(31,310),(13,262),(13,310),(31,352),(31,16),(11,358),(11,462)。**INCOMPLETE_FRONTIER**。范围、逐根精确指数、回执用[总索引](Proof.md)；条件记录用[Results](Results.json)，后续结果可能覆盖早期条件记录，不做累加。
- 五个用户要求的基线命令均实际通过；见[基线验收](Audit/Baseline.md)。单键完整依赖冷重放均通过；没有全库历史冷重放结论。独立 LF 检出 4ebbccc7 上第一批集成冷回归仍在跑（lead job pwsh-abc6bd62098d49c2，Build/MonitorCold.py），待收取时间和峰值采样，不能外推至更新后的 HEAD。
- 最新已验收关键余域：(3,12) 的 797161 只余 1、96；(7,12) 的 Q^12 只余 T²，Q^42 仍在；(19,618) 已登记只余 2477 的 2、4、6，6 的进一步候选待审；(19,282) 仍余首枢轴 10；(13,388) 六纤维增量待审，不能算全键。新证据须按完整精确键投影。
- 本轮主研究：已完成 (19,358) 双强迫来源 645/968 条件格；(11,396) 已过 42 个高纤维。新增 56 个低纤维的 Low.py + LowForests.json.gz 默认重放 job pwsh-ba9fdedc54cf4474，另请 ten 审计。若通过，仍余 [2,4,6,8,12,22,24,26,36,70,78,82,96,106,112,126,136,138]。发现用 Build/Root396.py，封包 Build/Seal396.py；两项均不是证明依赖。
- 团队继续工作：three=3；seven=7^12/7^438；nineteen=19^618/19^282；others=13^388；sieve=7^430；dual=19^330/420；ten=19^280/46 并做数学审阅；audit=独立验收。待办含 19^282,h28 全纤维审计、19^280 十一路径包名规范化/提交、19^618 低树、7^906 匿名约束、3^12 匿名约束及 (3,6) f1 的更多低纤维。每个 agent 自行收取其后台作业；lead 只记自己的。
- 工程：不要 git add 整个 Research，含巨大未封存实验与证书。先读证明/回执、跑针对性测试，显式路径暂存，再运行 RepositoryStructureChecks 和 Project；仅 VERIFIED_FULL → Project.py --write。保持 PascalCase，查看输入哈希与 CLI 参数。如需 WSL GP/ECM，路径 Build/NumberTools/root/usr；只供发现。下一轮不要重读全库或未压缩历史对话。
