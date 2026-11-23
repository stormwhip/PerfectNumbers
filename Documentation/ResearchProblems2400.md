# 奇完全数下界 \(10^{2400}\) 的形式化研究问题

当前待证明的 1,221 个规范分片见 [合并审计清单](../Research/SupplierBatch/BatchAudit2400.json)。最新可复验状态见 [CurrentStatus2400.md](CurrentStatus2400.md)。

> **2026-11-22 状态更新：** 原根集互素类已具备独立证书（`log10 N >= 4183.209493`）；V21 含根 3,072 项尚无全量独立证明。本文正文部分 `2400.822998027028` 属于此前的区间 LP 原型数据，原始理论问题与历史分析保留。最新模块与未完成义务请见 [CurrentStatus2400.md](CurrentStatus2400.md)。

> **文档性质：** 数学问题定义与尚待证明的条件，2026-11-22。正式求解器为 V21，研究原型为 V22–V24。所有“已完成”状态只对应指定实验；当前尚未形成无条件下界定理的独立可核验证书。

## 0. 目标命题与必要记号

记 \(\sigma(n)=\sum_{d\mid n}d\)，奇完全数集合为

$$
\mathcal O=\{N\in\mathbb Z_{>0}:N\equiv1\pmod2,\ \sigma(N)=2N\}.
$$

本项目的**目标定理**为

$$
\boxed{\mathcal O\cap[1,10^{2400}]=\varnothing.}\tag{T}
$$

以下统一设 \(B=2400\)、\(H=B\log 10\)。假设存在 \(N\in\mathcal O\) 且 \(\log N\le H\)。由 Euler 结构定理，

$$
N=\pi^{4u+1}\prod_{j=1}^{r}p_j^{2a_j},\qquad
\pi\equiv1\pmod4,\quad u\ge0,\quad a_j\ge1,
$$

其中各素数互异，\(\pi\) 是唯一的 Euler 特殊素数。令

$$
h(p,e)=\log\frac{\sigma(p^e)}{p^e}
=\log\frac{1-p^{-(e+1)}}{1-p^{-1}}.
$$

则每个假设中的 \(N\) 同时满足

$$
\sum_{p^e\parallel N} h(p,e)=\log 2,\qquad
\sum_{p^e\parallel N}e\log p\le H.\tag{1}
$$

因子和整除关系提供必要条件

$$
p^e\parallel N\Longrightarrow
\operatorname{odd}\!\bigl(\sigma(p^e)\bigr)\mid N,\tag{2}
$$

其中 \(\operatorname{odd}(m)=m/2^{v_2(m)}\)。若 \(d+1\mid e+1\)，还成立

$$
\sigma(p^d)\mid\sigma(p^e),\qquad
\operatorname{odd}\!\bigl(\sigma(p^d)\bigr)\mid N.\tag{3}
$$

(1)–(3) 与 Euler 条件共同构成所有证明树剪枝和 LP 松弛必须保持的数学不变量。

## 1. 八根分割的完备性

令

$$
S_8=\{3,5,7,11,13,17,19,31\},\qquad
(q_1,\ldots,q_8)=(19,7,11,31,13,3,5,17).
$$

定义候选空间

$$
\mathcal U_B=\{N\in\mathcal O:N\le10^B\},
$$

及互斥的九类

$$
\begin{aligned}
\mathcal C_i&=\{N\in\mathcal U_B:q_i\mid N,\ q_j\nmid N\ (j<i)\},
&&1\le i\le8,\\
\mathcal C_\infty&=\{N\in\mathcal U_B:\gcd(N,\prod_{q\in S_8}q)=1\}.
\end{aligned}
$$

显然

$$
\mathcal U_B=\mathcal C_\infty\ \dot\cup\
\mathcal C_1\ \dot\cup\cdots\dot\cup\mathcal C_8.\tag{4}
$$

因此 (T) 等价于下列九个命题全部成立：

$$
\boxed{\mathcal C_\infty=\varnothing,\qquad
\forall i\in\{1,\dots,8\},\ \mathcal C_i=\varnothing.}\tag{5}
$$

**当前实证：** 对 \(\mathcal C_\infty\)，增强 LP 区间对偶程序给出十进对数下界 \(2400.822998027028\)；这是**待独立审计的程序输出**。对 \(\mathcal C_1,\dots,\mathcal C_8\)，V21 已能列出顶层任务，但尚无全部任务完成且通过独立验证的证书。

## 2. 核心难题 I：互素尾部 LP 的模型完备性与独立对偶证书

设 \(F=S_8\)。对每个有限候选素数 \(p\notin F\) 和容许指数族 \(a\)，引入松弛变量 \(0\le x_{p,a}\le1\)。每个素数满足

$$
\sum_{a\in I_p}x_{p,a}\le1.\tag{6}
$$

欧拉特殊指数选项满足

$$
\sum_p\sum_{a\in I_p^{\mathrm{sp}}}x_{p,a}
+x_{\mathrm{sp,tail}}\le1.\tag{7}
$$

用 \(y_{\mathrm{tail}}\ge0\) 表示有限截断素数域以外的丰度贡献，用对数尺寸下界系数 \(c_{\mathrm{tail}}\) 约束其代价。用相应的 \(h(p,a)\) 建立

$$
\sum_{p,a} h(p,a)x_{p,a}
+y_{\mathrm{tail}}+h_{\mathrm{sp,tail}}x_{\mathrm{sp,tail}}
\ \ge\ \log2.\tag{8}
$$

对已经经证实的因子和整除 \(q^k\mid\sigma(p^a)\)，在精确指数选项中加入

$$
x_{p,a}\le\sum_{b\in J(q,k)}x_{q,b},\tag{9}
$$

其中右侧必须包含**全部**能容纳 \(q^k\mid N\) 的普通或特殊指数族，并适当放松未知高指数尾部。目标是使 LP 的对数尺寸目标 \(c^\top x\) 不超过映射来的真实 \(\log N\)。

**待证明的模型涵盖性命题：** 对任意 \(N\in\mathcal C_\infty\)，均存在相应 LP 可行解 \((x,y)\)，使

$$
c^\top x\le\log N.\tag{10}
$$

涵盖性包括：Euler 特殊指数的所有同余类、\(p\) 超过显式素数截止值 \(P_{\max}=4000\) 的无限素数尾、\(a\) 超过指数截止值 \(a_{\mathrm{cut}}=16\) 的尾，以及因子和蕴含关系的全部例外处理。式 (10) 是将 LP 最优值解释为真实奇完全数大小下界的关键。

**待构造的独立证书：** 将 LP 统一写为

$$
\min c^\top z\quad\text{s.t. }Az\le b,\quad
0\le z_i\le1\ (i\in I),\quad z_j\ge0\ (j\in J).
$$

寻找可独立复核的 \(\lambda\ge0\)，令 \(r=c+A^\top\lambda\)。验证所有无上界变量满足 \(r_j\ge0\)，并证明

$$
-\lambda^\top b+\sum_{i\in I}\min(0,r_i)
\ >\ 2400\log10.\tag{11}
$$

(11) 中的对数系数、对偶乘子、界端点及求和均应通过**有理数或严格区间包围**验证。SciPy/浮点求解器可以寻找候选 \(\lambda\)，最终正确性应由独立、短小的验证器确认。

**主要难点：** 当前 \(2400.822998027028\) 是生成器计算结果；数学证明还需要 (10) 的全域完备证明与 (11) 的导出型、可离线检查证书。

## 3. 核心难题 II：八棵因子链证明树的覆盖性、有限性及终结证据

对每个根 \(q_i\) 构造有限证明树 \(\mathcal T_i\)。节点 \(s\) 记录此前被禁止的素数集合 \(F_s\)、已选的素数幂代表 \((p,a,\tau)\)、由 (2)–(3) 强制出现而尚未分支的素数集合 \(U_s\)、尚未完整分解的因子和残余整数及 Euler 特殊素数状态。

每个“非精确”指数分支 \((p,d)\) 代表所有满足

$$
e\ge d,\qquad d+1\mid e+1\tag{12}
$$

的实际指数 \(e=v_p(N)\)；“精确”分支要求 \(e=d\)。对每个节点的待展开素数 \(p\)，设分支选项集合 \(\mathcal D(s,p)\)。

**覆盖引理：** 对满足节点所有约束的任意假想 \(N\)，存在至少一个 \(d\in\mathcal D(s,p)\)，使实际 \(e=v_p(N)\) 落入该精确/非精确选项。尤其应严格验证 \(p=3,7\) 的专门指数类、普通偶指数类，以及 \(e\equiv1\pmod4\) 的唯一 Euler 特殊指数类。

采用 (12) 的理由是：对偶指数 \(e\)，\(e+1\) 有奇素因子 \(\ell\)，令 \(d=\ell-1\) 即可获得 \(\sigma(p^d)\mid\sigma(p^e)\)；对特殊奇指数 \(e>1\)，\(e+1=2(2t+1)\) 也有奇素因子。特殊 \(e=1\) 应由精确选项覆盖。实现中还需证明所有尺寸预筛选均不会遗漏可行的 \(e\)。

**节点终结引理：** 对每个叶节点 \(\ell\)，提供能由独立程序验证的矛盾证据，例如

$$
\text{必要因子与禁用素数冲突};\qquad
\log N_{\min}(\ell)>H;\qquad
\log\frac{\sigma(N)_{\min}}{N}>\log2;
$$

或给出满足第 2 节证书形式的状态 LP 下界。遇到无法继续分类的合数残余时，必须提供有证明效力的尺寸/丰度上界或继续细分任务。

**形式化完成标准：**

$$
\forall i\le8,\quad
\mathcal T_i\text{ 为有限的覆盖树，且每个叶节点均附有有效的矛盾证书}.\tag{13}
$$

程序打印 `PROVEN` 是求解器状态；(13) 需要证明树结构、每条推理规则及独立验证器共同确认。

## 4. 核心难题 III：无穷素数尾的 roadblock 证实

设在节点 \(s\) 上还需获得的最小对数丰度为 \(\Delta_s>0\)，剩余对数尺寸预算为 \(M_s\)。对候选分界素数 \(b\)，设 \(\mathcal R_s(b)\) 为符合当前特殊素数名额、排除素数、强制素数和因子和约束，且**所有尚未展开的新素数均不小于 \(b\)** 的松弛剩余配置集合。

定义其最小必要尺寸

$$
L_s(b)=\inf\left\{
\sum_{p^e\in R}e\log p:
R\in\mathcal R_s(b),\
\sum_{p^e\in R} h(p,e)\ge\Delta_s
\right\}.\tag{14}
$$

使用任何乐观松弛 \(\underline L_s(b)\le L_s(b)\)，只要能严格证明

$$
\underline L_s(b)>M_s,\tag{15}
$$

便知任何真实延拓都必须引入某个尚未展开的素数 \(p<b\)，从而可对这些素数作有限的环形分支（circular branches）。

**待证明：** V21 的分数背包、\(a=2/4\) 候选流、唯一特殊素数名额、\(300000\) 以上的无限尾部估计满足 \(\underline L_s(b)\le L_s(b)\)；求解 \(b\) 的二分判定所需单调性成立；所有剩余候选素数均被枚举。对尚未完成的复合残余，还需证明任何用于限制其可能丰度的最小素因子界是严格有效的。

**计算难点：** roadblock 的保守上界必须足够强，使 (15) 在深层困难节点频繁成立，同时每次计算的 CPU 成本有限。

## 5. 核心难题 IV：可早期证明的状态条件化 LP 剪枝

当前预计算的 256 个前缀 LP 对偶证书，只依赖被排除的八根子集，并可用当前已知/强制素数进行调整。困难分支需要更细的条件。

对搜索状态 \(s\)，定义它所代表的所有数学可行延拓 \(\mathcal F(s)\)。目标是寻找容易计算、证书可验证的函数 \(L(s)\)，满足

$$
\forall N\in\mathcal F(s),\qquad \log N\ge L(s).\tag{16}
$$

若 \(L(s)>H\)，便可在分解后续因子和之前关闭该子树。可考虑的附加线性约束包括

$$
\sum_{a\in I_q}x_{q,a}=1\quad(q\in U_s),\qquad
x_{p,a}=1\quad\bigl((p,a)\text{为已确定指数}\bigr),\tag{17}
$$

以及由 \(\sigma(p^a)\) 已知因子强制的素数和估值约束。

**形式化算法研究问题：** 构造低成本证书族 \(\{\lambda_s\}\)，使 (16) 对任意真实延拓成立，且在固定基准任务族 \(\mathcal B\) 上显著减小

$$
W(\mathcal B)=\sum_{s\in\mathcal B}
\text{求解其所代表子树所需的工作量}.\tag{18}
$$

重点是**尽量在昂贵的素性测试和因子分解之前剪枝**，同时衡量证书计算、存取和校验成本。证书数量减少或单纯剪枝计数增加均不足以证明总运行时间缩短。

## 6. 核心难题 V：算术规则、外部数据和独立验证器的可靠性

所有叶节点使用的推理规则必须转化为可独立验证的离散证据：

1. **因子和与素性：** 对每个声称的素数提供确定性素性证书；所有声称的分解要通过精确乘法验证。GMP 的 `mpz_probab_prime_p` 返回“可能为素数”不足以单独承担数学证明。
2. **浮点判定：** 对所有可能关闭分支的比较，证明使用向外舍入的区间仍有严格正余量；当区间跨过阈值时保留分支。
3. **复合残余：** 对每个残余 \(c\)，证明所有使用的最小素因子界、互素性条件和允许丰度上界；重叠残余的尺寸贡献必须避免重复计算。
4. **覆盖与完整性：** 根分割 (4)、子节点分割 (12)、每一任务的退出状态和合并逻辑都要可重验。

目标证书应采用**生成器—验证器分离**的结构：昂贵求解器输出有限有向无环证明图（DAG）或证明树 \(\Pi\)，短小独立验证器 \(V\) 对所有节点、边和终结证明进行验证：

$$
V(\Pi,\text{认证输入})=\texttt{ACCEPT}\quad\Longrightarrow\quad(T).\tag{19}
$$

(19) 的正确性本身应由对验证器全部推理规则的数学证明保证。

## 7. 核心难题 VI：72 小时内的总成本及可恢复计算

令 \(\mathcal K_i\) 为根 \(q_i\) 下全部互斥指数分片，\(w_{i,k}\) 为完整结束并生成证书所需的计算工作量。若可用 \(P\) 个等效计算核心，则至少必须满足

$$
T_{\mathrm{wall}}\ \ge\
\frac{\sum_{i=1}^{8}\sum_{k\in\mathcal K_i}w_{i,k}}{P}.\tag{20}
$$

若某个分片无法进一步切分，则其完整用时还给出一项最大临界路径下界。工程要求为

$$
\boxed{T_{\mathrm{wall}}\le72\text{ 小时}=259200\text{ 秒}}\tag{21}
$$

且输出全部可复核证书。当前根 19 的 287 个顶层分片，在 1 秒上限实验中有 164 个完成、123 个超时；这些截断数据不能估计 \(\sum w_{i,k}\) 的长尾。

**待解决：** 证明数学任务分区覆盖且无漏检，允许深层分片及重启状态无损保存，在固定硬件与固定输入条件下估计总工作量和关键路径，并完成全部八根。

## 8. 最新实验对研究方向的约束

| 实验 | 已验证事实 | 对数学研究的启示 |
|---|---|---|
| 增强 \(S_8\)-互素 LP | 数值下界指数 \(2400.822998027028\)，独立审计未完成 | 优先完成模型涵盖性与可独立检查的对偶证书 |
| V21 根 19 分片普查 | 287 个中 164 个 1 秒内完成、123 个超时 | 必须研究困难子树的长尾与深层任务拆分 |
| V22 精确 \(\sigma\)-整除剪枝 | 精确算术规则成立，已完成分片中运行变慢 | 数学剪枝需要在较早层次且低成本触发 |
| V23 素性测试去重 | 完成的两个分片耗时较 V21 降低约 25%–30% | 因子和残余的素性检测为可测量的性能瓶颈 |
| V24 乘积 GCD | 4000 组差分测试通过，完成分片性能表现不一致 | 继续通过完整分片比较，避免凭操作次数判定收益 |

实验报告在 [Research/Session20261122/](../Research/Session20261122/Readme.md)，正式求解器和数学资料入口见 [RepositoryMap](RepositoryMap.md)。

## 9. 最小研究闭环与严格验收标准

按照依赖关系，当前任务可写成

$$
\begin{gathered}
\text{LP 涵盖性}\ +\ \text{独立区间对偶证书}
\Longrightarrow \mathcal C_\infty=\varnothing,\\[2mm]
\text{有限指数覆盖}\ +\ \text{正确剪枝}\ +\
\text{八根证明树全部验证}
\Longrightarrow \bigcup_{i=1}^{8}\mathcal C_i=\varnothing,\\[2mm]
\mathcal C_\infty=\varnothing
\ \land\ \bigcup_{i=1}^{8}\mathcal C_i=\varnothing
\Longrightarrow \mathcal U_B=\varnothing.
\end{gathered}\tag{22}
$$

当前最需要突破的**数学研究问题**是：在保证 (12)、(15)、(16) 与无限尾部严格正确的前提下，设计能在浅层剪除大量困难子树的、可检查的条件化证明规则。随后再通过独立证书和 72 小时完整运行验证 (T)。

---

**证据入口：** [V21 主代码](../Sources/Cpp/ProofTreeV21.cpp) · [256 前缀 LP 生成器](../Sources/Python/PrefixDualCertificates.py) · [验收清单](../Records/ValidationChecklist.md) · [原始实验记录](../Records/ExperimentLog.md) · [研究实验归档](../Research/Session20261122/Readme.md)。
