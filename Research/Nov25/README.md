# 11 月 25 日：10^2400 下界后续研究

- 固定起点：`e89dffd5a74debad80f695d6177f3d785e6268e8`（PR #3 的起始快照）。
- 固定清单：[`Audit.json`](../NightMerge/Audit.json)，规范 LF 字节的 SHA-256 `3efc593b3950340cee799f0be02ee19be4c1c1caf1b8f501eefb3021dcb5d902`。快照为 2,646 / 3,072 个闭合分片、426 个剩余分片。
- 这里只计相对此快照的净新增；以不同的 `(p,e)` 去重，只有原开放分片全部剩余实际指数被复验排除才算闭合。实验输出不自动算作证书。
- 各批证书和复验命令随检查点保留。独立草稿 PR 不合并；目标不是在此时间窗口内承诺闭合全部分片。
- 时间窗口：北京时间 09:45 转入收尾，10:00 停止研究（UTC 01:45、02:00）。

## 起始检查点

已检出固定提交并核对清单哈希；426 片含 562 个不同实际 `(p,e)`。此检查点不声称已复验 PR #3 的全部基线证书。

## 08:04：先导实验（未入账）

- **共享 σ 锚点：** [AnchorPilot.py](AnchorPilot.py) 用确定性 64 位素性测试和乘积校验复验五个精确来源。8 个对照目标均开放。7283 使两个 `(p,330)` 的首条未决链从 1 节点推进到 5；9059 使两个 `(p,646)` 从 1 到 2。加入两层精确来源后，`(11,646)` 访问 10 节点，3 层后为 11（赋值剪枝 2→3）；`(19,646)` 两种均为 11（赋值剪枝均为 3）。没有完整排除，不继续盲目加深。`q²∣N` 不足以激活 `σ(q²)`；必须分支确立 `q²∥N`。
- **尺寸与平方核：** [SizeExperiment.py](SizeExperiment.py) 对 11 个目标比较普通尺寸/Euler 优惠与粗块平方核补价。试除到 20,001，额外剪枝和净新增均为 0；`(19,676)` 两侧都达到 150 节点上限。另用 [RootDiscovery.py](RootDiscovery.py) 对每根最大的 8 项做整除与概率素性筛选，未发现任何可尝试认证且达到 `q³≥3·10^2400` 的候选，不把概率素性或复合余块视为证书。
- **既有弱森林：** 用 `python -I -S -B Research/NightMerge/LiftTarget.py Lift19x120.json.gz 19 120` 重放返回 `target not excluded`，故不入账。

文献核对：[Brent–Cohen–te Riele (1991)](https://maths-people.anu.edu.au/~brent/pub/pub116.html)、[Ochem–Rao (2012)](https://doi.org/10.1090/S0025-5718-2012-02563-4) 的因子链要求来源为精确素数幂；本轮先导按此区分上下界和实际指数。[Hansen–Nielsen](https://arxiv.org/html/2204.08971v1) 的同型 Φ₃ 素数乘积假设不能从共享一个素因子推出。[Acquaah–Konyagin](https://doi.org/10.1142/S1793042112500935) 的最大素因子界只用于假设已为奇完全数的对象（[Zelinsky §2 的引述](https://arxiv.org/html/2402.14234v2)），不能用于一般丰数或把 `q³/3` 与无关除数相乘。

```text
python -I -S -B Research/Nov25/Ledger.py
python -I -S -B Research/Nov25/AnchorPilot.py
python -I -S -B Research/Nov25/SizeExperiment.py
python -B Research/Nov25/RootDiscovery.py --limit 8
```

前三条仅需标准库；最后一条仅为发现筛选，需要 SymPy。

## 首个净新增：`(5,148)`，闭合 `P5_I00034`

[证书](five/Forest148.json.gz) 验证 `q=σ(5^148)` 的素性，故 `q∣N`。若 q 为普通素数，两个整数森林递推都给出 `floor(log10 N) ≥ 2503`。若 q 为 Euler 素数，精确尺寸界只允许 `a=1,5,9,13,17,21`；禁素排除 `5,9,17`，精确两来源的强制乘积排除 `13,21`，两个定向赋值/丰度模型排除 `a=1`。森林只用于普通 q 分支，未将此前的条件结果算作完整指数。

```text
python -I -S -B Research/Nov25/five/Verify148.py
python -I -S -B Research/Nov25/Ledger.py --check Research/Nov25/Delta.json
```
