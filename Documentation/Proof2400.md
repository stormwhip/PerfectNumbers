# 奇完全数 \(10^{2400}\) 下界的合并证明

令 \(B=10^{2400}\)。本文件汇总已验收的排除结论及其证明规则。固定根序为 \((19,7,11,31,13,3,5,17)\)。取第一个整除 \(N\) 的根 \(p\)，其前面的根构成禁素数集合。与八个根均互素的情形由[原根集独立证书](../Research/Session20261122/Python/TerminalCertificate.py)排除，所得下界为 \(\log_{10}N\ge4183.209493\)。含根的 3,072 个规范分片已闭合 **2,192** 个，余 **880** 个。目标定理的当前状态为 INCOMPLETE_FRONTIER。

## 1. 覆盖规则

互素类证书将可能的素幂划分为有限显式选项、由因子约束引出的素幂选项和通用尾项。乘法丰度给出 \(\sum_{r^f\parallel N}\log(\sigma(r^f)/r^f)=\log 2\)。每条显式因子约束按整数模运算复核。对数用有向整数区间包围，取成本下端与丰度上端，因此实际反例在松弛模型中可行。非负对偶乘子给出模型成本下界，通用尾项的约化成本须非负。证书重算的整数下界超过 \(2400\log 10\) 的上端，排除这一类。

设 \(N=q^aM^2\)，其中 \(q\nmid M\)，\(q\equiv a\equiv1\pmod 4\)。每个分片的代表指数记为 \(d\)。精确分片要求 \(e=d\)，整除分片要求 \(d+1\mid e+1\)，其中 \(p^e\parallel N\)。指数受 \(p^e\le B\) 和 Euler 结构约束。由几何级数整除关系，后一类可共用 \(\sigma(p^d)\) 的因子见证。整数预筛以 \(p^e\operatorname{odd}(\sigma(p^e))>B\) 或禁素因子排除指数，其中 \(\operatorname{odd}\) 表示去掉全部 2 因子的奇数部分。

取每个分片中尚未被基线排除的全部合法 \(e\)。新证书以 \((p,e)\) 为键求并集。只有该分片的每个待证 \(e\) 都被覆盖时才新增一次闭合。例如 P31_I00038 需要同时排除 \(172\) 与 \(518\)。[审计清单](../Research/EveningMerge/Audit.json) 记录新增指数、完整闭合及开放分片的逐项指数。

## 2. 强制因子链、尺寸与丰度

设 \(X=\prod r_i^{f_i}\) 由已固定的实际素幂组成，\(S=\sigma(X)\)。则 \(\gcd(X,N/X)=1\) 且 \(S\mid 2N\)。由素数赋值得到
\[
D=\frac{S}{\gcd(S,2X)}\mid N/X.
\]
若 \(D\) 与 \(X\) 或禁素数积有公共因子，或 \(XD>B\)，即得矛盾。若 \(S/X>2\)，也可立即关闭该节点。

写 \(D=U\prod r^c\)，其中 \(r\) 是认证的奇素数，\(U\) 保留已去掉所列因子和试除范围内小素数的剩余整数。对每个 \(r\) 分别求合法最小偶指数 \(f\) 和可用的 Euler 指数 \(o\)。否决指数可用 \(r^{j+1}\equiv1\pmod{\ell(r-1)}\)，这里 \(\ell\) 为禁素数。若 Euler 位置尚空，先按偶幂付费，再取最多一次可行 Euler 折扣的最大值。若已有固定 Euler 项，剩余项一律用偶指数。乘以 \(XU\) 得整数尺寸下界。固定一个强制底数后，枚举预算内所有合法指数并重建 \(X,D\)。所有子分支均推出矛盾时，实际指数才获证。

丰度叶将已识别的未固定素数贡献上界设为 \(r/(r-1)\)。若 \(U\) 的因子均至少为 \(L\)，其贡献不超过 \((L/(L-1))^{\lfloor\log_L U\rfloor}\)。剩余预算里若有 \(j\) 个新素数，用最小 \(j\) 个允许的底数估计最大丰度及最小体积。允许一次 Euler 指数时，最小体积取这些底数的平方积除以其中最大者。所得总丰度上界严格小于 2 时排除。根 5 的 \(e=580\) 给出一个尺寸叶实例。其 319 位强制素因子模 4 为 3，偶指数 \(2,4,6,8\) 分别触发禁素数 \(3,11,7,3\)，故至少为十次幂，尺寸超过 \(B\)。

## 3. 根赋值供给与 Euler 来源

固定 \(p^e\parallel N\) 后，\(\sigma(N)=2N\) 要求各成分总共提供 \(e\) 个 \(p\)-赋值单位。已固定成分贡献 \(v_p(S)\)。对普通偶幂 \(r^f\)，以乘法阶和 LTE 定位可能的供给，再对每一级增量指数付费。若 \(p=3,5\)，有 \(v_p(\sigma(r^f))>0\) 的普通成分必满足 \(r\equiv1\pmod p\)，此时第 \(j\) 个单位需要 \(f\ge p^j-1\)。某一级的几何和出现禁素因子时，其后各级同样不可用。已计入 \(X\) 或 \(D\) 的幂先扣除，剩余费用才进入新下界。根 3 的整数链还按二进制统一单位价格计算折让，分别枚举 Euler 已占用、在已知强制底数和在其它底数的情形。两类尺寸下界可分别剪枝，其乘积须有不重叠的因子账。

根 3、5 的外部 Euler 一次幂分支使用以下联合界。令 \(A=\sigma(p^e)\)、\(s=v_p(q+1)>0\)、\(Y=p^s\)、\(P=p^{e+1}\)、\(Q=2Y-1\)。若 \(q\nmid A\)，则 \(q\mid\sigma(N)\) 强制存在另一个普通成分 \(r^f\) 满足 \(q\mid\sigma(r^f)\)。记 \(c=v_r(A)\)。当 \(2^p p^eQ^{p+1}\ge3^p B\) 时，该来源提供零个 \(p\)-赋值单位。若 \(f+1=p^jm\) 且 \(j\ge1\)，由 \(p\nmid q-1\) 可将上面的整除降到 \(\sigma(r^{m-1})\)，从而 \(r^f>(2q/3)^p\)，与尺寸预算矛盾。对已在 \(A\) 中出现的来源，\(\sigma(r^f)/q\) 和 \(r^c\mid A\) 的同余给出
\[
r^{f-c}>\frac{Y}{\max(1,P/q)(P/Y+4)}.
\]
当 \(c=0\) 时可直接使用 \(r^f>2q/3\)。

当 \(c>0\) 时令 \(U=(P-1)/r^c\)、\(w=\sigma(r^f)/q\)、\(t=r^{f-c}\)、\(H=\max(1,P/q)\)、\(\delta=P/Y\)。两个整除量为
\[
D_1=Uw(r-1)-U-rt,\qquad
D_2=Uw+U\sigma(r^{c-1})-\sigma(r^{f-c}).
\]
由 \(Ur^c=P-1\) 和 \(qw(r-1)=r^{f+1}-1\) 得 \(Y\mid D_1\)，且 \(D_1\equiv-P\bmod(r-1)\)，所以 \(D_1\ne0\)。恒等式
\[
r^c D_2=P\bigl(w+\sigma(r^{c-1})\bigr)-w(q+1)
\]
给出 \(Y\mid D_2\)。若 \(D_2=0\)，则 \(v_p(w)+s\ge e+1\)，与 \(\sigma(N)=2N\) 的根赋值 \(e\) 矛盾。又 \(Uw< Htr/(r-1)\)。当 \(r-1<\delta+2\) 时，用 \(D_1\) 的上下界得到 \(Y\le |D_1|<(\delta+4)Ht\)。当 \(r-1\ge\delta+2\) 时，若 \(D_2<0\) 则 \(|D_2|<3t/2\)，若 \(D_2>0\) 则 \(Y\le D_2<3Ht/2+\delta Y/(\delta+2)\)。两种情形都给出上式所需的 \(t>Y/((\delta+4)H)\)。

其它供应者的第 \(j\) 个单位在 \(A\) 已付 \(r^d\) 时至少再付 \(r^{\max(d,p^j-1)-\max(d,p^{j-1}-1)}\)。对大未知因子，用剩余整数给出免费单位总数 \(G\) 的上界。分圆分块可加强该界。若 \(r>h\) 且 \(r\mid\Phi_h(p)\)，则 \(\operatorname{ord}_r(p)=h\)。潜在免费供应者满足 \(r\equiv1\bmod\operatorname{lcm}(2h,p)\)，且 \(r^{p-1}\mid\Phi_h(p)\)。可沿等差数列试平方整除，取首个可能的底数下界。把最便宜的 \(i\) 个边际成本的乘积记为 \(C(i)\)，非供应奇次补价去掉可能属于来源的最大一笔后记为 \(J\)。上面三笔费用对应不同的超额素幂，因此以下整数判据足以排除该分支
\[
p^e A Q^2Y\, C(\max(0,e-s-G))\,J
\ \ge\ B\max(P,Q)(P/Y+4).
\]

Euler 项 \(q\mid A\) 时，根 3 利用 \(\operatorname{ord}_q(3)\) 为奇数及二次互反推出 \(q\equiv1\bmod 3\)，所以 \(s=v_3(a+1)\)。根 5 对 \(q\equiv-1\bmod5\) 令 \(t=v_5(q+1)\)。从 \(A=qC\) 与 \(4C\equiv1\bmod5^t\) 得 \(2t\le e\)，故 \(s\le e/2+5\)。对其它五根的赋值判据，以 Teichmüller 供给价格为基线，对各已知强制底数取合法指数的最小额外费用。Euler 占用某底数时扣掉该底数的全部普通供给价格。\(a=1\) 时按 \(q\) 是已知因子、未知内部因子或外部因子分支，短等差区间可用精确整数枚举。\(a\ge5\) 使用已证 Euler 供给尺寸界。根 5 的丰度与赋值联合叶使用已验证的有理对偶，删去已单独计价的因子、相应流入及可能的 Euler 和来源价格后应用，详细证书由两套遍历重算。

## 4. 素性与重放

每个作为素数使用的因子先验证其整除关系及素性。小于 \(2^{64}\) 的候选用确定性七底 Miller–Rabin。大因子的 ECPP 链逐层绑定当前整数 \(n\)，验证曲线判别式为单位，验证 \([s]P\) 在每个素因子剩余域中非零且 \([q][s]P=O\)，其中子素数 \(q>(n^{1/4}+1)^2\)。若 \(n\) 合数，最小素因子 \(\ell\le\sqrt n\)，Hasse 界与该阶为 \(q\) 的点矛盾。链尾回到确定性范围。预算用尽或只有概率素性见证的指数继续开放。

| 批次或规则 | 复验入口 | 证明数据 |
| --- | --- | --- |
| 原根集互素类 | [TerminalCertificate.py](../Research/Session20261122/Python/TerminalCertificate.py) | [原根互素类证书](../Research/Session20261122/Certificates/TerminalOriginal.json.gz) |
| 历史含根基线 | [仓库复验命令](../Readme.md#复验) | [Teichmüller](../Research/TeichmullerValuation/Audit2400.json)、[Gemini](../Research/TeichmullerValuation/GeminiBatchAudit2400.json) |
| 根 3 来源与供应，6 项及 3 片 | [CheckShards.py](../Research/GapSupply2400/CheckShards.py)、[Independent.py](../Research/GapSupply2400/Independent.py) | [扫描记录](../Research/GapSupply2400/LiftDeep.json) |
| 根 3，42 项来源与 87 项多层链，重合 26 项 | [IndependentEvening.py](../Research/EveningRoot3/IndependentEvening.py)、[Replay.py](../Research/ThreeChainNext/Replay.py) | [来源](../Research/EveningRoot3/BothAudit.json)、[链](../Research/ThreeChainNext/Certificates.json) |
| 根 5，81 项 | [CheckCertificate.py](../Research/RootFiveNext/CheckCertificate.py) | [证书](../Research/RootFiveNext/RootFiveCertificate.json) |
| 根 7、11、13、19、31，共 346 项 | [VerifyOrderSupply.py](../Research/OrderSupplyNext/VerifyOrderSupply.py)、[IndependentTree.py](../Research/EveningTree/IndependentTree.py) | [341 项](../Research/OrderSupplyNext/Accepted.json)，另五项 \((7,570),(11,318),(13,544),(13,634),(31,362)\) |
| 规范分片映射 | [VerifyFrontier.py](../Research/EveningMerge/VerifyFrontier.py) | [合并清单](../Research/EveningMerge/Audit.json) |

在仓库根运行 `python -B Research/EveningMerge/VerifyFrontier.py --workers 6` 可复验新增证书及并集，历史基线另按[仓库命令](../Readme.md#复验)重放。从 2,027 个已闭合分片出发，第一批新增 3 个，第二批净排除 530 个实际指数并新增 162 个完整分片。

Euler 来源的分圆指数约简曾在 533 个根 3、5 实际指数上做区间复验，扩大了其中 76 项的覆盖。分支级推导及部分覆盖记录见[历史来源区间报告](https://github.com/stormwhip/PerfectNumbers/blob/ea08da38e38ab3309da4360ea2bb60ecb616a025/Documentation/ResearchReport2400.md)。

两批逐分支推导、发布命令及原始统计保存在 [PR #1 快照](https://github.com/stormwhip/PerfectNumbers/tree/4aad42d895d44782d69e28ed065ca4fda2401b1d/Research/GapSupply2400)和 [PR #2 快照](https://github.com/stormwhip/PerfectNumbers/tree/ea08da38e38ab3309da4360ea2bb60ecb616a025/Research)。[当前状态](CurrentStatus2400.md)与[下一步计划](NextPlan2400.md)使用同一份审计清单。
