# 文献核查：哪些外部定理能约束 $10^{2400}$ 的剩余反例？

**结论。** 本次核到的正式大小下界是 Ochem–Rao 的 $N>10^{1500}$；作者网页另报计算达到 $10^{2200}$。二者均不能替代 $10^{2400}$ 的证明。对现有树，最值得直接引入的是 Nielsen 的素数同余提升界（下文 §2）：在普通来源的大小预算内，该界没有通常写出的 $10^{1000}$ 截断。其次是 Clayton–Hansen 的重数不等式与 Zelinsky 的支持积上界。它们给出必要条件；本文没有据此证明任何完整开放键，也不更新覆盖计数。

以下 $N$ 是假想奇完全数，$N=\pi^\alpha m^2$，$(m,\pi)=1$，$\pi\equiv\alpha\equiv1\pmod4$，$\pi$ 为素数；$k=\omega(N)$，$\Omega(N)=\sum_{p\mid N} v_p(N)$；$p_1<\cdots<p_k$ 是按**大小**排列的全部素因子。项目的规范根按另一个固定次序选出，不能代入 $p_1$。本文的“核到”指核对论文陈述及使用条件，不指独立重做原作者的大型计算；编号以注明的版本为准。

## 1. 从整树下界到可移植的局部规则

|论文与核查位置|可引用的结论|不能继承的结论|
|---|---|---|
|Brent–Cohen, *A new lower bound for odd perfect numbers*, Math. Comp. 53 (1989), 431–437；[作者论文及证明树入口](https://maths-people.anu.edu.au/~brent/pub/pub100.html)|作者摘要明确给出 $K=10^{160}$ 的完整搜索。此项核至作者摘要，不指定未核的定理号。|其叶是针对这个阈值的；不能平移目标。|
|Brent–Cohen–te Riele, *Improved techniques for lower bounds for odd perfect numbers*, Math. Comp. 57 (1991), 857–868，[原文](https://maths-people.anu.edu.au/~brent/pd/rpb116.pdf)，[树与附注](https://maths-people.anu.edu.au/~brent/pub/pub116.html)|定理 1：没有小于 $10^{300}$ 的奇完全数；等号因奇偶性不可能。作者对困难的偶指数成分 $q^a\parallel N$ 建立有附加检验的界。|定理 2 的 $q^{5a/2}$ 不是对任意已知偶次幂都成立的界；本文不使用该条件定理。|
|Ochem–Rao, *Odd perfect numbers are greater than $10^{1500}$*, Math. Comp. 81 (2012), 1869–1877，[作者原文](https://www.lirmm.fr/~ochem/opn/opn.pdf)／[期刊](https://doi.org/10.1090/S0025-5718-2012-02563-4)|仅假定 $N$ 是奇完全数。定理 1：$N>10^{1500}$；定理 2：$\Omega(N)\ge101$；定理 3：$\max_{p\mid N}p^{v_p(N)}>10^{62}$。|第三项不是 $p_k>10^{62}$，也不是对每个素幂的界。三个见证不能看成互素因子相乘。|

[Ochem 研究页](https://www.lirmm.fr/~ochem/opn/)区分论文和后续计算。页面提出的 $10^{2200}$ 不是 2012 年定理 1；页面的更强重数和 $m$ 的界也不作为本稿证明前提。没有把目标合数表的名称当作已达下界。

**Ochem–Rao §3 的三个细节。** (i) 按顺序排除小素数；第 $j$ 个禁素只在前 $j-1$ 个已缺且假设尺寸上限成立的域内处理。原文按全局最大可分支的已知素因子扩展，不局限于上一行。(ii) 若 $d+1\mid a+1$，则 $\sigma(p^d)\mid\sigma(p^a)$；整除代表可传递强制因子和尺寸下界，但不能传递**精确赋值**、$I(p^d)$ 作为丰度上界或针对 $d$ 的赋值冲突。标准分支使用 $p/(p-1)$ 作上界；精确分支才能使用精确丰度。(iii) 合数余块 $C$ 已证明所有素因子 $\ge L>1$ 时，至多有 $\lfloor\log C/\log L\rfloor$ 个不同底数，其支持的极限丰度至多 $(L/(L-1))^{\lfloor\log C/\log L\rfloor}$。这是上界，不给出 $C$ 的素性、平方自由性或与别块互素性。

已有支持贡献至多 $A<2$ 时，若最小新素因子为 $u$，还需至少 $t=\lceil\log(2/A)/\log(u/(u-1))\rceil$ 个新底数。在已收取 $M\mid N$ 且这些底数均不整除 $M$ 的前提下，Euler 奇指数至多一次，故 $N\ge Mu^{2t-1}$。这给出下一未知素数的**上界**，不是证明该素数一定出现在余块 $C$。无禁素树一侧用 $\log I(p^a)/\log(p^a)$ 比较每单位体积的丰度收益；原文报告的 $10^{1735}$ 只是在其特定禁素侧的终端量，不能作全局下界。

## 2. 大素因子与素数同余提升：一条能直接用于普通来源的界

Nielsen, *Odd perfect numbers, Diophantine equations, and upper bounds*, Math. Comp. 84 (2015), 2549–2567：[原刊 DOI](https://doi.org/10.1090/S0025-5718-2015-02941-X)，[作者原稿 PDF](https://mathdept.byu.edu/~pace/BestBound_web.pdf)。以下编号与作者原稿正文核对；引理 3.3 的素数上界是 $10^4$，而定理 2.6 的两个底数界是整数 $105$，两者勿混。

- 推论 1.8：$10^{12}p_k^2N<2^{4^k}$；定理 3.8：$k\ge10$。第一个界是固定 $k$ 下的**上**界，第二个界不意味着 $k=10$。定理 2.6 在 $k\le9$、不同奇素数 $p,q<105$、$p^a,q^b$ 为精确成分且 $10^{100}<p^a<q^b$ 下排除共同的 $\ge10^{11}$ 的 $\sigma$ 素因子。不能用于今天 $k\ge10$ 的对象来阻止两个来源共享一个大素数。
- **引理 3.3**：若 $q<10^4$ 是奇素数，$r$ 为奇素数，$n\ge1$ 且 $r^{q-1}\equiv1\pmod{q^n}$，则 $r\ge\min(q^{n-2},10^{1000})$，除非 $(r,q)=(40663372766570611389846294355914421,7)$。该引理本身不需要 $k\le9$。这一点与定理 2.6 不同。
- Goto–Ohno, *Odd perfect numbers have a prime factor exceeding $10^8$*, Math. Comp. 77 (2008), 1859–1868，[原刊](https://doi.org/10.1090/S0025-5718-08-02050-9)，[作者稿存档](https://arquivo.pt/noFrame/replay/20200913070650/https://www.ma.noda.tus.ac.jp/u/tg/perfect/perfect.pdf)：作者稿定理 1.1，$p_k>10^8$。已知支中若已有这样的素因子，不能再追加一个。Acquaah–Konyagin, [*On prime factors of odd perfect numbers*](https://doi.org/10.1142/S1793042112500935)，另给每一素因子 $r^3<3N$；此项仅核到作者摘要转录及 Zelinsky 的交叉引述，未核原刊编号，不作为下面的必需依赖。

**预算下的推论（普通来源；非新外部定理）。** 设 $N\le10^{2400}$，普通成分 $r^f\parallel N$，$f\ge2$ 偶，目标 $q\le31$ 为不同奇素数，$d=\operatorname{ord}_q(r)>1$，$q\mid\sigma(r^f)$，$z=v_q(\sigma(r^f))$。除上列例外外，
\[
 r\ \ge\ q^{\,z-v_q(f+1)-2}.
\]
证明：$d\mid f+1$，$d\mid q-1$。对奇素数 $q$ 应用 LTE，$z=v_q(r^d-1)+v_q(f+1)$，且 $v_q(r^{q-1}-1)=v_q(r^d-1)$。由于 $r^f\sigma(r^f)\mid N$（两项互素且 $\sigma(r^f)$ 为奇数），$r^{2f}<N$，故 $r<10^{600}<10^{1000}$。代入引理 3.3，最小值不可能取 $10^{1000}$，即得。例外素数模 7 阶为 6，不整除奇数 $f+1$，因此亦不是这样的普通来源。若 $d=1$，分母 $r-1$ 抵消，正确式为 $z=v_q(f+1)$，不应按 Teichmüller 贡献收费。证毕。

这条界覆盖八个根的小目标，包括非最小的提升代表。但它只给出来源成本 $r^f\ge q^{f(z-v_q(f+1)-2)}$，不是任意指定权重。若两个目标共用该来源，两个下界只能先取最大，不能相乘。若独立采用 Acquaah–Konyagin 的最大素因子界，则一次 Euler 来源也小于 $10^{801}$，但奇指数时不能使用上段 $r^f\sigma(r^f)\mid N$ 的断言。

## 3. 数量约束：把“至少几个素因子”变成正确的剩余重数

|原始论文|版本、条件及结果|
|---|---|
|Nielsen, [*Odd perfect numbers have at least nine distinct prime factors*](https://arxiv.org/abs/math/0602485)，[期刊](https://doi.org/10.1090/S0025-5718-07-01990-4)|作者稿定理 22：$k\ge9$；定理 23：若 $3\nmid N$，则 $k\ge12$。前者由 2015 年定理 3.8 改进。|
|Hare, [*New techniques for bounds on the total number of prime factors of an odd perfect number*](https://arxiv.org/abs/math/0501070v2)，[期刊](https://doi.org/10.1090/S0025-5718-07-02033-9)|作者稿定理 1.1：$\Omega\ge75$；原文通过约束未知素数来绕开难分解合数。该数已被 101 改进。|
|Ochem–Rao, [*On the number of prime factors of an odd perfect number*](https://www.lirmm.fr/~ochem/opn/opnf.pdf)，Math. Comp. 83 (2014), 2435–2439|仅需奇完全。定理 1：$7\Omega\ge18k-31$；定理 2：$\Omega\ge2k+51$。后者与线性斜率更大的界应取最大。|
|Clayton–Hansen, [*On inequalities involving counts of the prime factors of an odd perfect number*](https://math.colgate.edu/~integers/x79/x79.pdf)，Integers 23 (2023), A79|定理 1.3：$37\Omega\ge99k-187$；定理 1.4 **附加 $3\nmid N$**：$19\Omega\ge51k-46$。论文通过受限圆分分解导出的计数不等式证明；不是说任意两普通素数的输出没有公共因子。|

例如，由 $37\Omega\ge99k-187$ 与 $\Omega\ge2k+51$ 比较，前者在 $25k>2074$，即 $k\ge83$ 时严格胜出（指未取整的右端）。后者在 $k\ge26$ 时超过定数 101。这说明斜率强并不保证每叶都获益。若已固定精确成分 $X$，$k=k_X+j$、$\Omega_X=\Omega(X)$，且其他所有底数至少为 $L>1$，对可行的 $j$ 令 $U(k)$ 为本节适用下界与 101 的最大值取上整，则
\[
 N\ge X L^{\max(0,U(k_X+j)-\Omega_X,\;2j-\delta)},
\]
其中 Euler 未固定时 $\delta=1$，已固定时 $\delta=0$。这是同一批新成分的三种重数下界，故取最大而非相加。高指数根已经贡献 $e$ 个重数，$\Omega\ge101$ 不会自动强制额外的 101 个底数。若已有匿名余块仅知整除，不能假定它是额外精确成分，或把它再乘入上式而不剥离共同支持。

## 4. 支持积、倒数和与顺序统计量

定义 $I(n)=\sigma(n)/n$，$H(n)=\prod_{p\mid n}p/(p-1)$，$T(n)=\sum_{p\mid n}1/p$。$I(N)=2<H(N)$；未知素数每一个只计一次。令 $S=H(N)-2$。

**Zelinsky，[*The sum of the reciprocals of the prime divisors of an odd perfect or odd primitive non-deficient number*](https://arxiv.org/abs/2402.14234)，[正式刊本，Integers 25 (2025), A59](https://math.colgate.edu/~integers/z59/z59.pdf)。** 刊本与 arXiv v5 编号不同，已对照两版：

- 刊本命题 3（v5 命题 4）：若 $n$ 原始非亏，即 $I(n)\ge2$ 而一切真因子亏，$p_1$ 为其最小素因子，$S=H(n)-2$，则 $T(n)\ge\log2-25/(64p_1)+S/2-S^2/4$。奇完全数自动原始非亏。
- 刊本命题 5（v5 命题 6）：对奇完全数，$H(N)\le2+9/(4p_1^2)$。刊本推论 1（v5 推论 16）：**若 $p_1\ge11$**，$T(N)<\log2-11/(50p_1^2)$。若只知 $p_1\ge L$ 则可在 **$H$ 上界**右端放 $L$，但不能在该 **$T$ 上界**右端放 $L$（方向相反）。
- 将精确乘积恒等式 $H(N)/2=\prod_{r^a\parallel N}(1-r^{-a-1})^{-1}$ 与命题 5 合并：已知精确列的任何子积若大于 $1+9/(8p_1^2)$，便排除该分支。另可直接以已知素支持 $D$ 比较 $H(D)>2+9/(4p_1^2)$，此版本不要求各列指数精确。一个未知因子的全部贡献不能同时按若干互不确定的身份计入。
- 刊本命题 9：$\pi\equiv-1\pmod{165}$ 不可能是 Euler 素数。原因不是“一切奇完全数都不被 165 整除”，而是刊本引理 11：$165\mid N$ 强制 $5\parallel N$；$\pi+1\mid2N$ 将要求另一个 Euler 素数。可直接对**已证明了这一同余的 Euler 候选**应用，不是对全体 $q\mid\sigma(p^e)$ 的排除。

**Zelinsky，[*On the small prime factors of a non-deficient number*](https://arxiv.org/abs/2005.12118)，[正式刊本，Integers 23 (2023), A13](https://math.colgate.edu/~integers/x13/x13.pdf)。** 若 $u$ 是素数而 $c>1$，令 $b_c(u)$ 为从 $u$ 开始的连续素数中使 $\prod r/(r-1)>c$ 的最短前缀长度。命题 9、推论 11：奇数 $N$ 完全或丰，则 $k\ge1+b_{4/3}(p_2)$，且 $p_2\le3k-1$。命题 19：对**奇完全数** $k\ge3+b_{256/255}(p_4)$；关键是引理 18 的前三个真实成分丰度积 $<255/128$。不是任意三个已知成分按任意次序都可替代前三项。引理 15–17 还给 $105\nmid N$，$165\mid N\Rightarrow 5\parallel N$，以及 $195\mid N\Rightarrow (5\parallel N\ \text{或}\ 3^2\parallel N)$。这些限制不需要认定某个大合数为素数。

**有效常数，而不是渐近口号。** 同文定理 7 在 $1<c\le3$、$u\ge853$ 为素数时给出
\[
 b_c(u)\ge \frac{u^c}{c\log u}-\frac{1.669u^c}{c\log^2 u}-\frac{0.662u^c}{c\log^3u}-\frac u{\log u}-\frac{1.2762u}{\log^2u}+1.
\]
其引理 4 使用 [Rosser–Schoenfeld 的原论文](https://doi.org/10.1215/ijm/1255631807)：$\prod_{p\le x}p/(p-1)$ 的上下包络分别为 $e^\gamma\log x(1\pm1/(2\log^2x))$，下界要求 $x>3$，上界要求 $x\ge286$。这里阈值核自 Zelinsky 引理 4，未复核 1962 年刊本编号；没有把其渐近定理 5 当作有限下界。实际计算极短前缀时直接保留有理乘积通常更强。

**限制同余类的素数。** Bennett–Martin–O’Bryant–Rechnitzer, [*Explicit bounds for primes in arithmetic progressions*](https://arxiv.org/abs/1802.00085)，Illinois J. Math. 62 (2018), 427–532，v3 定理 1.2、1.3。取其已核的统一子域：$3\le h\le10^5$，$(b,h)=1$，$x\ge8\cdot10^9$，则
\[
 |\theta(x;h,b)-x/\varphi(h)|<c_hx/\log x,\qquad |\pi(x;h,b)-\operatorname{Li}(x)/\varphi(h)|<c_hx/\log^2 x,
\]
$h\le10^4$ 可取 $c_h=1/840$，否则取 $1/160$。$\theta$ 是该类中素数的对数和，$\pi$ 是计数函数。若上界严格小于 $j$，则该类第 $j$ 个素数必大于 $x$；若已证有 $t$ 个**不同**来源属于该类，将适用的第 $j$ 素数下界逐个相乘才是来源乘积下界。不把整个同余类的 $\theta$ 当作整除 $N$ 的素数和；也不把大 CRT 模数或 $x<8\cdot10^9$ 放入上述统一常数。没有对本次实际余域证明达到所需的同类来源数。

## 5. 小素数筛的量词与证明责任

Yamada, [*On the divisibility of odd perfect numbers, quasiperfect numbers and amicable numbers by a high power of a prime*](https://arxiv.org/abs/1609.08795)，Integers 20 (2020), A91，作者稿 v6 定理 1.1。就本问题取其特例 $h(N)=2/1$：将不同素数的精确成分分成 $s$ 个不限指数的 $p_i^{\alpha_i}$ 与其余 $r_j^{\beta_j}$；须给定一个非空有限素数集 $\mathcal P$，对**每一个**后者都有 $\ell\mid\beta_j+1$ 对某 $\ell\in\mathcal P$ 成立。此时对每个 $\epsilon>0$ 有素因子 $<C_0(1,s,2,\mathcal P,\epsilon)$，$C_0$ 取原文 (1)、(2) 及定理定义的最大值。不是“存在一个已知根 $e+1$ 被某素数整除，就有相同的最小素因子界”。即使借 $N\le10^{2400}$ 取得巨大而有限的指数集，定理中的 $x_1\ge\exp(\exp(9))$，相应 $C_0$ 对这个目的没有新增小素因子限制。

**判定文献是否真的闭合一键。** 首先写明根序与精确指数；其次对每个可能的 Euler 位置、真实最小素因子范围及普通／特殊来源分别代入适用条件；最后在相同分支以互素账或同一尺寸下界比较，严格推出 $N>10^{2400}$ 或逻辑矛盾。当前这些文献能加强已有分支的必要条件，但本稿未发现可不经剩余分支论证而推出目标的正式定理。本文没有使用“奇完全数不存在”、Wieferich 普遍稀少性或任何素数分布猜想。
