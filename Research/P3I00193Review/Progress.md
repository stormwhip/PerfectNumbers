# 根 3 联合计价研究（2026-11-25）

基线 `839a1b036e446e7f2bcc56d9bcddc8752af1ce88`。状态 `VERIFIED_PARTIAL_ONLY`；新增完整实际指数及闭合分片均为 0。冻结账本为 2868/3072，开放 204 片、244 个实际指数。计算使用本机与免费软件。

## 独立整数分支证明

设 $3^e\parallel N$，$\sigma(N)=2N$，$N\le B=10^{2400}$，$\gcd(N,7\cdot11\cdot13\cdot19\cdot31)=1$。Euler 项记为 $q^a$，$s=v_3(\sigma(q^a))$。普通项 $r^f$ 的赋值为 $k=v_3(f+1)$，满足 $r\equiv1\pmod3$、$f\ge3^k-1\ge2k$。底数 37 在 $k\ge1$ 时强制禁素数 7，故供应底数至少为 43。

E0 中 $s=0$，直接得 $N\ge3^e43^{2e}$。E1 中 $a\ge5$，逐个 $s=1,\ldots,e$ 使用

$$
N\ge3^e43^{2(e-s)}q^a.
$$

当 $q\equiv1\pmod3$，取 $q\ge37$、$a\ge\max(5,3^s-1)$。当 $q\equiv2\pmod3$，穷尽 $s_1+s_2=s$，取 $q\ge\max(5,2\cdot3^{s_1}-1)$、$a\ge\max(5,2\cdot3^{s_2}-1)$。代码以饱和整数乘幂逐项检验超过 $B$，覆盖所有 $s_2=0,\ldots,s$。

对普通供应项另建立乘法对偶。令 $R=10000$、$K=R^2$，对每个可用素数 $r<R$ 定义

$$
D_r=\max\left(1,\max_{k\text{ 可用}}\frac{K^k}{r^{3^k-1}}\right),\qquad D=\prod_{r<R}D_r.
$$

存在 277 个 $D_r>1$。$r\ge R$ 时 $r^f\ge K^k$；$r<R$ 时 $r^f\ge K^k/D_r$。因此总普通供给为 $U$ 时，普通部分 $O\ge K^U/D$。枚举在 $K^k\le r^{3^k-1}$ 时终止，因为 $(3^k-1)/k$ 严格递增；禁素筛触发后，更高层几何和均包含该禁素数。

E2 中 $a=1,q\mid A=\sigma(3^e),s\ge1$。写 $A=mq$，有 $m\equiv(3^s+1)/2\pmod{3^s}$、$q\ge2\cdot3^s-1$，推出 $s\le e/2$。于是 $U\ge e/2$，并有 $N\ge3^eK^{e/2}/D$。验证使用整数交叉相乘。

| $e$ | E0 的 $\lfloor\log_{10}$ 下界$\rfloor$ | E1 枚举的 $q\equiv2\pmod3$ 情形数 | E2 的 $\lfloor\log_{10}$ 下界$\rfloor$ |
|---:|---:|---:|---:|
| 856 | 3204 | 367652 | 3566 |
| 970 | 3631 | 471905 | 4077 |
| 990 | 3706 | 491535 | 4166 |
| 1108 | 4148 | 615494 | 4694 |
| 1162 | 4350 | 676865 | 4936 |

全部 E1 情形均严格超过 $B$。证书与执行入口为 [PartialResults.json](PartialResults.json)、[VerifyPartial.py](VerifyPartial.py)。这些证明不使用 $A$ 的未分解因子下界或原包的浮点供给表。

## 来源降阶

在外部 Euler 一次幂分支，$q\equiv2\pmod3$。若 $q\mid\sigma(r^f)$ 且 $b=v_3(f+1)\ge1$，写 $f+1=3^bm$。有限域中立方映射为双射，所以 $q\mid\sigma(r^{m-1})$：几何和的另一因子模 $q$ 非零。由 $\sigma(r^{m-1})<3r^{m-1}/2$ 得

$$
r^f>(2q/3)^3,\qquad N>\frac8{27}3^eq^4.
$$

代码精确检验 $8\cdot3^e(2\cdot3^s-1)^4>27B$。因此 $e=1162,s\ge967$ 及 $e=1108,s\ge981$ 时必有 $b=0$。这给出外部 Euler 的条件子域证明。

仅在原候选窗口及其余 Euler 基础推导有效的条件下，把 $b=0$ 代回原程序，基础项变为 2164.0459201493（1162）、2068.6216692053（1108）；后者仍假设 $R_A=10^{11}$。此实验未新增该试除范围的证书。参见 [ZeroSupplyCandidate.py](ZeroSupplyCandidate.py) 及 [结果](ZeroSupplyCandidate.json)。

## 42 叶、余块与来源重放

[ReplayCandidate.py](ReplayCandidate.py) 删除两个单重数优惠，按 $v(\ln u-2\ln3)$ 计 $u\equiv1\pmod3$ 的已知重数。来源范围使用必要条件 $r^fQ_s\le\lfloor B/(3^eA)\rfloor$，保留整数同余检查。扩展集合为原 1276 个辅助素数与全部 $<50000$ 的可用素数的并集，共 5829 个。

166 个 Pocklington 证书、$A$ 的两项试除、支持覆盖及全部 42 叶均已执行。这里“执行”记录每叶结果，不要求每叶超过 2400。叶名在原包中有重复，结果以位置索引区分。

[ResidualAudit.py](ResidualAudit.py) 检查全部 34972 个显式清洗余块：与 $A$ 的 gcd 全为 1，全部小于 $Q_{1067}$。因此在候选窗口内排除了这些余块含 $q$ 的可能性。结果见 [ResidualResults.json](ResidualResults.json)。大于等于 50000 的未知余因子与来源 $r$ 的重叠仍待排除或分配费用。

## 新对偶与丰度缺口

索引 9（`cell10_no17_23_29_37`）的保守原对偶给出

$$
2160.2289501116+70.2759852520+169.4718729047
=2399.9768082683.
$$

[RebuildDual.py](RebuildDual.py) 重求同一候选松弛的对偶。新 LP 项为 169.4957938419，候选合计约为 2400.0007292056。[VerifyDualRational.py](VerifyDualRational.py) 对 1441 个有界列和一个无界外部列复验：先用正确舍入的 80 位 Decimal 对数的相邻数作包围，再以精确有理数执行全部运算，并扣除有界列的负约化成本。输入 [RebuiltDual.json](RebuiltDual.json)，结果 [RationalDualResults.json](RationalDualResults.json)。该结果认证所列松弛的数值对偶。

原丰度上界只沿已激活森林节点累加。未激活节点仍可整除 $N$，而 LP 又排除了整个森林池；这些节点的丰度须补计。改用整个森林池的 $\sum_u\ln(u/(u-1))$ 后，原对偶的 7 叶降至 2400 以下，索引为 0、2、3、4、8、9、12。索引 9 为 2380.1067450181，全体最小值为索引 4 的 2266.6975376161。这些仍是候选模型重算值。新对偶的微小余量不能补齐这项模型缺口。

已构造 [JointPoolExperiment.py](JointPoolExperiment.py)：为森林与 LP 并集中的每个素数只设一组指数选择变量，全部节点贡献丰度，全部余块共用一个外部体积约束，不另加森林下界。七叶净成本的浮点最优值见 [JointPoolResults.json](JointPoolResults.json)，约为 198.6270、254.7163、216.9089、212.8113、215.2328、227.8331、204.3218。该松弛仍需更强的多源流入及来源重叠约束，并需导出严格对偶。

另一条路线为 [WeightedForestExperiment.py](WeightedForestExperiment.py)。记 $C_u(h)=h\ln u-4\ln3\,v_3(\sigma(u^h))$、$I_u(h)=\ln(\sigma(u^h)/u^h)$。固定丰度乘子 $\lambda$，对每个森林底数置 $w_u=\min(0,\inf_h\{C_u(h)-\lambda I_u(h)\})$。全部节点先收取 $\sum_uw_u$；树中已激活节点再收取 $C_u(h)-\lambda I_u(h)-w_u$，并在同一次动态规划中处理余块费用与小余因子丰度。这样，未激活节点也通过可选费用进入丰度账。已测试原乘子及十分之一网格上的缩放。其[候选辅助成本](WeightedForestResults.json)依次为 261.9285、276.5126、257.1300、189.6650、231.3174、226.0741、263.7689。

在 $b=0$ 的候选基础项 2164.0459201493 及其余分配条件下，对两条新路线逐叶取较强结果，四叶的候选值超过目标，剩下三叶的数值缺口如下。此表包含浮点松弛值和待严格认证的 Decimal 动态规划值。

| 叶索引 | 较强候选路线 | 候选合计 | 距 2400 |
|---:|---|---:|---:|
| 4 | 共同素数池 | 2376.8572430836 | 23.1427569164 |
| 8 | 加权森林 | 2395.3632830604 | 4.6367169396 |
| 9 | 共同素数池 | 2391.8790533336 | 8.1209466664 |

## 总重数验收条件

对奇素数 $u$，由 $\sigma(N)=2N$ 有

$$
\sum_{v^h\parallel N}v_u(\sigma(v^h))=v_u(N).
$$

每个已实现源列产生的余块需求因此必须进入同一个总重数预算。若 $u\equiv1\pmod3$，可用统一单位净成本 $\ln u-2\ln3$；若 $u\equiv2\pmod3$，可用 $\ln u$。森林源和 LP 源共享 $u=13567$ 的原反例已加入回归。单独购买某余块中一次 $u$ 的平方补价不能跨源相加。

验收仍需完成：大余因子与 $r$ 的分离或联合付费；$A,q,r$ 和外部体积的同素数账；所有森林节点和已付余块的丰度归属；完整联合模型的无限指数尾、严格对偶与全部叶覆盖。当前 E3 仍开放，五个实际指数均留在冻结前沿。

## 复验

从仓库根目录执行；证明验证仅用 Python 标准库。SciPy 仅供重新搜索候选对偶和联合松弛。

```sh
python -I -S -B Research/P3I00193Review/VerifyPartial.py
python -I -S -B Research/P3I00193Review/ReplayCandidate.py
python -I -S -B Research/P3I00193Review/ResidualAudit.py
python -I -S -B Research/P3I00193Review/VerifyDualRational.py
python -I -S -B Research/P3I00193Review/Tests.py
python Research/P3I00193Review/RebuildDual.py
python Research/P3I00193Review/JointPoolExperiment.py
python -I -S -B Research/P3I00193Review/WeightedForestExperiment.py
```

输入文件保留原始内容，仅按仓库规则规范文件名；映射及 SHA-256 见 [InputManifest.json](InputManifest.json)。原候选程序的闭合输出属于历史待审主张；当前验收以本目录明确的空 `accepted_actuals` 为准。

本轮各项验证及旧账本额外回归的已完成范围见 [Validation.md](Validation.md)；旧账本全量算术重放标记为未完成。
