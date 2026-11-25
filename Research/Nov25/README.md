# 11 月 25 日：10^2400 下界后续研究

**当前结果：净排除 51 个实际指数、闭合 20 个分片。** 见[收尾报告](Closeout.md)与[精确剩余清单](Delta.json)。

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

[证书](Five/Forest148.json.gz) 验证 `q=σ(5^148)` 的素性，故 `q∣N`。若 q 为普通素数，两个整数森林递推都给出 `floor(log10 N) ≥ 2503`。若 q 为 Euler 素数，精确尺寸界只允许 `a=1,5,9,13,17,21`；禁素排除 `5,9,17`，精确两来源的强制乘积排除 `13,21`，两个定向赋值/丰度模型排除 `a=1`。森林只用于普通 q 分支，未将此前的条件结果算作完整指数。

```text
python -I -S -B Research/Nov25/Five/Verify148.py
python -I -S -B Research/Nov25/Ledger.py --check Research/Nov25/Delta.json
```

## 三个普通静态森林：`(13,76)`、`(19,86)`、`(19,274)`

历史发现数据只有候选图；初次丢弃无证节点后的 9 项先导均未过界。对三个候选补齐 149 条 ECPP 链，再由固定仓库的整数复验器检查全部节点素性、合法幂和单一 Euler 优惠，得到 `floor(log10 N)` 分别至少 2463、2430、2418。每条图覆盖所有适用 Euler 模式（分别 3、6、9 种）。这三项只消除原分片的部分义务，未另闭合分片。在最终复验中不读取历史缓存或运行 PARI。

```text
python -I -S -B Research/Nov25/ForestPackets.py Research/Nov25/Forests/P13x76QFine13x76.json.gz Research/Nov25/Forests/P19x86HDir19x86.json.gz Research/Nov25/Forests/P19x274QFine19x274.json.gz
```

## 单指数分片：四份森林与根五的 `(5,520)`

四份森林完成 `(13,42)`（`P13_I00013`）、`(13,418)`（`P13_I00080`）、`(19,102)`（`P19_I00025`）、`(31,396)`（`P31_I00076`）。根 19 的 102 指数比较严格的整数乘积；向下舍入的指数为 2400，仍严格大于 `10^2400`。

`(5,520)` 闭合 `P5_I00097`。两个定向算术实现核查所有根 σ 内 Euler 和高 Euler 指数，并排除外 Euler 指数 1 的 `s<445`（432 个直接界、13 个来源间隙、65 个付费源子检验）。剩 `s≥445` 时 q 不整除根 σ，且 `q≥2·5^445−1`。把 `5^520·σ(5^520)·q` 与剩余丰度成本分开计；后者用分支指数选项和经验证、不会同分支重复收费的粗块。终端对偶在整数日志与向外舍入 Decimal 两套算术下均给 `floor(log10 N) ≥ 2558`。这一步不假定普通发射源在根 σ 内还是外，也不需要分解根 σ。

```text
python -I -S -B Research/Nov25/Five/Verify520.py
python -I -S -B Research/Nov25/ForestPackets.py Research/Nov25/Forests/P13x42CacheD13x42.json.gz Research/Nov25/Forests/P13x418CacheD13x418.json.gz Research/Nov25/Forests/P19x102CacheD19x102.json.gz Research/Nov25/Forests/P31x396CacheD31x396.json.gz
```

## 定向 Euler 来源先导（未入账）

在来源树中保留 [Nielsen §3](https://arxiv.org/html/math/0602485v1#S3) 的两种 LTE 情形：`r≡1 (mod p)` 只供给 `v_p(f+1)`，其余可供给类用阶及 Teichmüller 提升。先重放按来源位置扣价的已有码框架，再把精确的普通发射源 `r^f` 定价为 `r^f/p^(κ·v_p(σ(r^f)))`，删去的只是该来源自己的已有收费；外来源不退已有粗块或已证素因子的费用。已把 Euler 指数限定为 1 且 q 不整除根 σ 时，窄盒中用 `q≡2p^s−1 (mod 4p^s)`、`v_p(q+1)=s` 过滤。精确两来源与 Euler 幂的出流相乘，不能仅对各个 σ 取最小公倍数。进位未判定和宽盒一律保留。

- `(19,676)`：对照余 119 个 s（4 个允许外来源）；定向余 112 个 s，外来源余 0。内部未知分支仍开放。
- 初版定向实现的另外三个对照：`(7,1018)` 余窗 219→214；`(11,718)` 120→115；`(31,486)` 未通过内部 Euler 前置界，根本未扫描。前两个仍开放，最后一项的缺省空结果不表示完整排除。
- 对 `(19,676)` 的 `s=172,191,230,270,283` 做格证探测：5,585 个整数小盒被矩形/短枚举排空，5 个代表性宽盒未过拟试格证的预筛；无多项式证书、无完整 s 闭合。首阻碍为 `c=1,f=2`、约 2,819 位的粗块；模数约 742 位，示例盒超出预试格证能力。只增加证书维数不作为下一轮默认路线。

```text
python -I -S -B Research/Nov25/DirectedExperiment.py --p 19
python -B Research/Nov25/LatticeScout.py --p 19 --s 172 --s 191 --s 230 --s 270 --s 283 --seconds 270 --output <仓库外文件>
```

格证探测需要 SymPy 和 python-flint；如非标准安装，可用 `--flint-path` 指向已有发行目录。每个候选叶须过原有精确多项式与 Sturm 校验；探测结果不进入账本。另见[支持、Pollard p−1 与根三单位约束试验](PrimeCuts.md)。

## 追加森林批次

十九根、十三根、三十一根的 28 个静态种子分别补齐缺失的素性链，然后逐项复验。能入账的证书显式列在 [Ledger.py](Ledger.py)；[Delta.json](Delta.json) 是去重后的输出，而不是独立的证明输入。

另为七根和十一根试验按首坏来源重新分配森林所有者，并补充新的圆分因子。[先导与复验说明](Seven/README.md) 将浮点发现排名与固定 [七／十一根算术](../NightSevenForest/Release/Replay.py) 的整数结果分开。最初 `(7,234)`、`(11,220)`、`(7,252)`、`(11,132)` 四项均通过；留存的整数界分别向下舍入为 2400、2419、2400、2436，其中 2400 表示严格超过阈值。四项减少分片义务但未单独关闭分片。

```text
python -I -S -B Research/Nov25/Seven/Verify.py Research/Nov25/Seven/Best11x2201.pack.json.gz Research/Nov25/Seven/Best7x2341.pack.json.gz
python -I -S -B Research/Nov25/Ledger.py --workers 8 --check Research/Nov25/Delta.json
```

## 根五简化交叉复验

`python -I -S -B Research/Nov25/Five/Simple520.py` 以相同终端权重将分界前移至 `s=300`。`q∣A` 的内部 Euler 总供给至多 265；外部高幂的 521 个 s 和外部一次幂的前 300 个 s 都直接以指标定价排除。其余外部一次幂给 `q≥2·5^300−1`，两个日志实现仍得到下界 `floor(log10 N) ≥ 2456`。它不调用来源间隙或付费来源分支，不另记一项。
