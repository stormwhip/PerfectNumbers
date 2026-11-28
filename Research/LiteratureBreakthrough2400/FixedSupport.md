# 固定支撑平方源：哪种文献算法确实覆盖第五行？

**结论。** 在核查的公开计算中未找到可直接套到 $(19,222)$ 第五前缀四个具名受者的完整解表。能直接引用的是**求全的方法**，不是这组输入的求解结果。这里固定 $T=\{19,t,r,v\}$，采用[第五前缀的已审计缺口](../JointConservation2400/Root19x222.md#L11-L21) $(222,17,21,9)$；$T$ 不含 3，各元素均 $1\bmod3$。只处理实际平方行 $x^2$（或普通行 $3\mid h+1$ 的子因子 $F(x)=x^2+x+1$），且 $F(x)$ 的支撑确实在 $T\cup\{3\}$ 内。不能用 $F(x)$ 投影到 $T$ 上的部分代替整个 $F(x)$。

| 原文及定位 | 算法所需输入与实际覆盖 | 在这里的裁决 |
|---|---|---|
| [Alvarado、Koutsianas、Malmskog、Rasmussen、Vincent、West，*A robust implementation for solving the S-unit equation and several applications*，2020 作者版，§§2.1、3–6、8.2](https://arxiv.org/html/1903.00977v5) | 给定数域 $K$ 及含全部无穷位的固定有限 $S$，解两个 $S$-单位之和为 1。复/实对数与 $p$ 进对数给初界，LLL 降界后筛尽。其小域表包含例如 $[K:\mathbb Q]\le5$、$K$ 仅在 2、3 分歧且有限 $S$ 限制在 6 上方的**指数界**；不等于给所有小域任意 $S$ 的解表。 | 取 $K=\mathbb Q(\omega)$、$\omega^2+\omega+1=0$。$U=(x-\omega)/(\omega^2-\omega)$、$V=-(x-\omega^2)/(\omega^2-\omega)$ 为 $S$-单位且 $U+V=1$。取 $S$ 为无穷位及 $3\prod_{p\in T}p$ 上的素理想。每个 $p\in T$ 分裂为两位，3 分歧为一位，此 $S$-单位秩为 **9**，不在上述小 $S$ 数据范围内。反向解须验证 $x=\omega+(\omega^2-\omega)U$ 为正奇素数、检查范数与指数容量。 |
| [von Känel、Matschke，*Solving S-unit, Mordell, Thue, Thue–Mahler and generalized Ramanujan–Nagell equations via the Shimura–Taniyama conjecture*，Mem. AMS 286 (2023)，Theorem F、§6.2 Algorithm 6.2](https://arxiv.org/html/1605.06079v1#S6.SS2) | 处理固定有理有限素集 $S$、$\mathcal O=\mathbb Z[1/S]$ 及给定非零 $b,c$ 的 $y^2+b=cu$，$y\in\mathcal O,u\in\mathcal O^\times$。定理 F 对其数据库**实际收录的三元组**给完备性；算法路线需相应 Mordell–Weil 基等输入。 | 取 $b=3$，$c=4$ 或 $12$。按四个非 3 指数模 3 分解，$F(x)=A z^3$，$A=3^\varepsilon\prod_{p\in T}p^{e_p}$、$0\le e_p\le2$；$Y=4A(2x+1),X=4Az$，则 $Y^2=X^3-48A^2$。至多 **162** 条确定 Mordell 曲线，不是 162 个点。反向须 $4A\mid X,Y$，$z$ 有指定支撑、$Y/(4A)$ 对应奇素底且容量合规。没有找到这 162 条曲线全部有受证基和完整整数点表，不能承诺以此快速解完。 |
| [Gherga、Siksek，*Efficient Resolution of Thue–Mahler Equations*，2024 修订作者版，§1 式 (2)–(3)、例 1.1、§§6–10](https://arxiv.org/html/2207.14492v2#S1) | 齐次整系数二元型 $G$ 在 $\mathbb Q$ 上不可约，次数 $d\ge3$，$\gcd(X,Y)=1$，右边为已知系数乘固定不同素数的非负幂；主实现还规范化 $\gcd(a_0,Y)=1$。其 $S$-单位与格筛仅需一个根域。例 1.1 的十三个三次型来自指定导子。 | $X^2+XY+Y^2$ **是二次**，不能直接调用其求解器。较高圆分子因子 $\Phi_d(X,Y)$ 若次数 $\varphi(d)\ge3$ 且目标支撑已定，则可用，最后须取 $Y=1$ 并校验实际成分。文中示例并非这四个受者输入。 |

**可直接交给验证器的任务（Proved 归约，未执行）。** 比较上述重型方法，现有赋值上限使第五前缀反而适合简单的整数证书。对 $\varepsilon=0,1$ 和 $0\le(a,b,c,d)\le(222,17,21,9)$ 构造
\[
 P=3^\varepsilon19^a t^b r^c v^d,\quad W=4P-3.
\]
完整表只须 **$2\cdot223\cdot18\cdot22\cdot10=1\,766\,160$ 次**确切整数平方判别，无不定高度的外部搜索。$W$ 平方时取唯一可能正底 $x=(\sqrt W-1)/2$，核验 $F(x)=P$、奇性、素性及 $x$ 不在固定源底、必要时查 $x\mid D_i$。若只求不遗漏的上界，可把素性未证者留作额外候选。$\varepsilon\le1$ 是由 $v_3(F(x))$ 给出；$P$ 不含其它素数是输入域的定义，而不是从 $P\mid\sigma(N)$ 自动得出。每一真解有唯一向量；四目标容量同时针对固定四行之外全部流入，不可把每一行各自的向量独立加到上限上。求出表后能拿到具体可累加的证据：对任意选定的目标子集，按不同实际底最多选一次，并对四坐标加总受容量约束；若纯行所供上限不达要求，差额不得不由**混合行或其它指数**供给，并非直接反证。特定 111 层已有[更小的余因子证书](ReverseCofactor.md)，不用为它单独做 176 万次判别。

**根 31 三高层。** 对固定二目标 $31,3229$ 的纯行，已有[确定短表与两个母块内的完全排除](Height.md)；不应以新的 $S$-单位包重复替代。若要把已知第三高普通底 $z$ 和 Euler $q$ 加入 $T$，必须先固定它们的值；“恰三高”仅限制个数，不固定 $z$ 或 $q$。一次 Euler 的确切区别是：若固定前缀对 $q$ 已供一份，则剩余平方行一律无 $q$ 因子；若未供，至多一条实际平方行可额外带 $q$，且只带一份。这样可把求全分成固定 $z$ 的 $q$-自由方程与至多一条例外行，但不能把可变 $q$ 并入同一张定支撑解表。未证明四目标纯行集合为空，也未解决两键的混合支撑。