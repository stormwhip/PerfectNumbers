# PerfectNumbers

[打开证明进度看板](https://stormwhip.github.io/PerfectNumbers/) · [看板数据与发布说明](Dashboard/Readme.md)

目标定理为：对每个奇完全数 $N$，均有 $N>10^{2400}$。

main 当前状态（PR #11–#14 已合并）为 **`INCOMPLETE_FRONTIER`**。相对冻结基线 3029/3072，新增完整精确键 $(7,438)$、$(31,6)$、$(7,48)$，闭合两个分片；现为 **3031/3072**，仍有 **41 个开放分片、50 个精确键、33 个单指数分片**。全局下界尚未证明。[证明索引](Research/AstraFinalAfternoon2400/Proof.md) · [研究检查点](Research/AstraFinalAfternoon2400/Checkpoint.md) · [机器可读投影](Research/AstraFinalAfternoon2400/OpenFrontier.json) · [验收范围](Research/AstraFinalAfternoon2400/Validation.md)。PR #11 仅合并[撤回记录](Research/KimiFrontier/November28/Retraction.md)，不计新增证明。

## 最新理论研究（PR #13、#14）

两轮理论研究均已合并。新增回边赋值界、赋值—单位—丰度联合对偶、共享来源三次界、圆分块奇偶修正及平方余量方程；对 $(31,456),(31,466)$ 得 $v_{31}(q+1)\le401$，对 $(7,738)$ 得 $v_7(q+1)\le709$。根 19 的五前缀整数表已独立复算；其中四个前缀排除 2677 供给两份 19。根 31 的 $(31,268)$ 余域仍开放，旧全外位高次 Euler 摘要已订正。新增完整键和分片均为 0，不改变现行账本。

[第一轮理论](Research/UnitBalance2400/Readme.md) · [第二轮理论](Research/JointConservation2400/ResearchReport.md) · [合并审阅](Research/JointConservation2400/MergeReview.md)

| 文档 | 内容 |
|---|---|
| [Proof2400](Documentation/Proof2400.md) | 数学推导、已证范围与证书索引 |
| [CurrentStatus2400](Documentation/CurrentStatus2400.md) | 当前逐根统计与证据等级 |
| [ResearchProblems2400](Documentation/ResearchProblems2400.md) · [NextPlan2400](Documentation/NextPlan2400.md) | 待证命题与工作顺序 |
| [RepositoryMap](Documentation/RepositoryMap.md) | 目录、依赖与复验入口 |
| [Milestones](Records/Milestones.md) · [ExperimentLog](Records/ExperimentLog.md) | 版本进度与实验记录 |

## 独立复验

在仓库根目录使用 Python 3.11+，保留断言。依次检查目录和链接、晚间冻结账本、夜间增量的精确算术及逐片投影。

```sh
python Sources/Python/RepositoryStructureChecks.py
python -I -S -B Sources/Python/FinalSprintLedgerChecks.py
python -I -S -B -X int_max_str_digits=0 Research/Night2400/Replay.py
python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/Verify.py
python -I -S -B -X int_max_str_digits=0 Research/FinalNight2400/Verify.py
python -I -S -B Research/FinalNight2400/Project.py
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Verify.py
python -I -S -B Research/AstraFinalAfternoon2400/Audit/ProjectionAudit.py --accepted-full 7,438 --accepted-full 31,6 --accepted-full 7,48
```

夜间命令重放历史 13 个完整指数；仅核对其投影可附加 `--projection-only`。Gemini 默认入口重放 Gemini 已验收的算术、历史 45/46 枢轴证书、C10 条件证书及现行投影。FinalNight2400/Verify.py 重放本轮依赖，Project.py 仅复算投影。Astra 入口按清单复验本轮证书，独立投影入口只认证逐片集合差；完整算术冷重放与全局验收的区别见[验证说明](Research/FinalNight2400/Validation.md)。两项旧候选条件证明未登记。11 月 28 日 Gemini 补充包经数学审阅与联合阶补证，接受 143 个局部子域排除，未新增完整键或闭片：[审阅](Research/GeminiFrontier/November28/Review.md) · [条件账本](Research/GeminiFrontier/November28/Results.json)。局部复验：`python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/November28/ReviewVerify.py`。[晚间 18 个指数的复验](Research/FinalSprint/Proof.md)及[历史复验顺序](Documentation/Proof2400.md#历史复验命令)另列。V21 长时实验使用 [Linux/WSL2 脚本](Scripts/Run72hWSL.sh)。
