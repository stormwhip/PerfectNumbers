# 高偶指数计数与平方行输出：低指数键及两个困难纤维

设 $N=q^\alpha\prod p^{b_p}$ 为奇完全数，$q\equiv\alpha\equiv1\pmod4$，记 $H=\#\{p:b_p\ge4\}$，这里 $p$ 不含 Euler 素数且 $b_p$ 是**实际**偶指数。以[50 键余集](../AstraFinalAfternoon2400/OpenFrontier.json)为准。本文不改正式账本；整键增量为零。

## 1. 两种全域约束（文献的直接推论）

- **已发表。** Fletcher–Nielsen–Ochem, *Sieve methods for odd perfect numbers* (2012), [作者原文 p. 2, Main Theorem](https://www.lirmm.fr/~ochem/opn/OPNS_Adam_Pace.pdf)，[DOI](https://doi.org/10.1090/S0025-5718-2011-02576-7)。若**每个**非特殊指数 $b$ 均满足 $3\mid b+1$ 或 $5\mid b+1$（每项可选不同素数），则最小素因子严格位于 $10^8$ 与 $10^{1000}$ 之间。下界证明以 $\Phi_3,\Phi_5$ 迭代强迫、过丰及受禁整除建树；上界来自筛法。无需假定 $b\in\{2,4\}$，也无需 Euler 指数受这两个余类限制。50 个键均含 $p\le31$，所以每键必有普通指数 $b\ge6$ 且 $\gcd(b+1,15)=1$。14 键须在**根之外**找到这一行：19 的 2,4,8,14,20,32；7 的 4,24,34；11 的 4；31 的 2；13 的 2,4,8。余 36 键该见证可以是根，不能另收一笔。特别地，$H=0$ 排除。
- **预印本。** Ochem–Zelinsky, *On odd perfect numbers with exactly one even exponent greater than 2*，[arXiv:2607.19746v1，2026-07-22，§1 Thm 1](https://arxiv.org/html/2607.19746v1#Thmtheorem1)，[作者程序及数据](https://www.lirmm.fr/~ochem/opn/restrained/)，[作者发表目录列作 submitted](https://www.lirmm.fr/~ochem/publi.htm)。若 $H=1$，唯一的高偶指数基是 **3**，其指数至少 **23,000,000,000**。证明分别排除 $v_3=0,2$，再在 3 为该高基时用筛与因子链得下界。反例预算内 $3^{23000000000}>10^{2400}$（$3^5>10^2$ 已足够），因此全部 50 键均可取 $H\ge2$，不宣称对无预算的 OPN 已证明 $H\ge2$。引用的是作者预印本定理，未重跑计算。这不是把一项高指数与其余未知指数误认作 $H=1$。
- **已发表。** Yamada, *On a theorem of Kanold on odd perfect numbers*, [作者终稿 Thm 1](https://arxiv.org/html/2312.17059v2#Thmtheorem1)，[DOI](https://doi.org/10.1007/s13226-023-00530-y)。若整数 $t\mid b+1$ 对**所有**非特殊指数成立，则 $t^5\mid N$，证明把 $t$ 化为素数幂并用圆分赋值及互发方程。不要求 $t$ 是素数，但不能用单个根的指数、或有限前缀的 gcd 代替全域 gcd。Evans–Pearlman, *Nonexistence of odd perfect numbers of a certain form* (2007), [作者原稿 pp. 1–2](https://mathweb.ucsd.edu/~revans/nonexistence.pdf)，[DOI](https://doi.org/10.1080/00150517.2007.12428226)，关于所有半指数 $\beta_i=b_i/2\equiv32\pmod{65}$ 等限制不是一个固定 $b_i$ 的排除。对当前小根，涉及 3 或 5 的公共模数限制已被上面更强的混合条件覆盖。
- **已发表。** Ochem–Rao, *On the number of prime factors of an odd perfect number* (2014), [原文 Thm 2](https://www.lirmm.fr/~ochem/opn/opnf.pdf)：$\Omega\ge2\omega+51$，由因子树计算证明。精确改写为 $\sum_{b_p\ge4}(b_p-2)\ge53-\alpha$。若 $H=2$，根是其中一个，指数 $e$，另一根指数 $f$ 满足 $f\ge55-\alpha-e$（取不小于右端的偶数及至少 4）。例如 $\alpha=1,e=4$ 时 $f\ge50$，$e=6$ 时 $f\ge48$。此式不证明又有第三行；若两个高普通基都不小于 $L$，它们的乘积至少 $L^{\max(8,57-\alpha)}$。未采用作者网页后推的未发表 +55。

## 2. 不用因子分解的丰度定理（Proved）

**定理。** 若 $3,7,11,19$ 都不整除 $N$，则 $H\ge3$。本结论不需 $10^{2400}$ 预算。特别地，规范根 31 或 13（先序已禁 19,7,11）下若 $3\nmid N$，其全部四个及六个开放键都满足 $H\ge3$。这是对十键的统一子域排除，并不排除 $H\ge3$ 的情形。

**证明。** 假设 $H\le2$。$q+1\mid\sigma(q^\alpha)$ 及 $3\nmid N$ 强迫 $q\equiv1\pmod3$。每个普通平方行 $x^2\parallel N$ 必有 $x\equiv2\pmod3$，否则 $3\mid\Phi_3(x)$。它的输出 $M=\Phi_3(x)=x^2+x+1$ 的每个素因子 $r$ 满足 $r\equiv1\pmod3$（$r\ne3$，阶三）。所以只可落在集合 $R$：Euler 与模 3 为 1 的高普通基；设其大小为 $k\le3$。模 3 为 2 的高普通基至多 $3-k$ 个。按真值从小到大，$R$ 的前三个可用下界为 $13,31,37$（7,19 禁止）。

用 [Ochem–Zelinsky, Lemma 3](https://arxiv.org/html/2607.19746v1#Thmtheorem3)（为 [Bennett–Levin, Prop. 1](https://arxiv.org/html/1312.4037v1#Thmtheorem1) 的特例）：$\Phi_3(x)=r^j$、$x,r$ 素时 $j>1$ 不可能。因此单素支持的平方行只能有 $M=r$；单调性使每个 $r\in R$ 至多对应一个 $x$。这种单支持平方基与负类高基合计至多三者、实际彼此不同，最小三个可用基为 $5,17,23$。混合支持的平方基 $x\ge17$：$\Phi_3(5)=31$ 为单支持，11 禁。此时 $\sqrt M<x+1\le9(x-1)/8$，所以 $\log I(x^2)<1/(x-1)\le(9/8)/\sqrt M$。令 $u_r=(\sqrt r-1)^{-1}$。每组指数向量仅对应至多一个 $x$（严格单调），几何级数给出
\[
 \sum_{\text{混合行}}\log I(x^2)<\tfrac98\sum_{S\subseteq R,\ |S|\ge2}\prod_{r\in S}u_r
\]
（无混合行时取非严格上界）。$u_{13}<2/5,\ u_{31}<2/9,\ u_{37}<1/5,\ u_{307}<1/16$。以下全用 $I(r^v)<r/(r-1)$。

1. $k\le2$：混合对数小于或等于 $1/10$。故丰度小于 $(13/12)(31/30)(5/4)(17/16)(23/22)(10/9)<2$。
2. $k=3$ 且单支持行不超过一个：没有负类高基；混合对数小于 $(9/8)[(2/5)(2/9)+(2/5)(1/5)+(2/9)(1/5)+(2/5)(2/9)(1/5)]<27/100$。总丰度小于 $(13/12)(31/30)(37/36)(5/4)(100/73)<2$。
3. $k=3$ 且至少两个单支持行：这些不同的 $x$ 中至少一个 $\ge17$，从而 $R$ 中最大基至少 $\Phi_3(17)=307$。上一式把 $1/5$ 换成 $1/16$ 得混合对数 $<3/20$。总丰度小于 $(13/12)(31/30)(37/36)(5/4)(17/16)(23/22)(20/17)<2$。

指数还原只用 $\exp(u)<1/(1-u)$，$0<u<1$。三种情形都违背 $I(N)=2$。该方法迁移自 Ochem–Zelinsky §2 对指数向量的计数；新增的是**两个**高基、三个潜在输出素数、禁素条件及有理丰度证书，不是该预印本的原定理。不声称优先权。

## 3. $(31,268)$ 的 $H=2$：强迫 Euler 及小范围 gcd（Partial）

由[末纤维](../JointConservation2400/Root31x268.md#L3-L17)，有 $X=31^{268}3229^{102}\parallel N$（意为两个实际幂、余因子与之互素），$A=\Phi_{269}(31)/3229$、$C=\Phi_{103}(3229)$、$D=AC$，$X,A,C$ 两两互素，$XD\mid N$ 且 $XD>10^{1508}$，$D$ 无 $\le10^8$ 的素因子，规范根禁 7,11,19。[独立审阅](../AstraFinalAfternoon2400/Audit/Root31EulerReceipt.md#L3-L19)。

**定理。** 在此纤维的 $H=2$ 类，必有 $3^2,13^2,61^\alpha\parallel N$，三者分别是精确成分，Euler 素数为 61；$\alpha\equiv9\pmod{12}$，且 $G_\alpha=\gcd(A,\sigma(61^\alpha))$ 有 $s>10^8$、$s\equiv2\pmod3$ 的素因子。特别一次 Euler 全域排除。

**证明。** 上节排除 $3\nmid N$。仅有两个高基都已固定，3 不能为 Euler，故 $3^2\to13$。若 13 为 Euler，$7\mid13+1\mid\sigma(13^\alpha)$ 与禁素矛盾，所以 $13^2\to3\cdot61$。若 61 非 Euler，则 $61^2\to3\cdot13\cdot97$，97 不能为 Euler（$7\mid98$）；于是 $13^2,61^2,97^2$ 三行各供 3，违背 $v_3(N)=2$。唯一 Euler 为 61，指数任意高也不能逃脱这一论证。若 $3\mid\alpha+1$，则 $\Phi_3(61)\mid\sigma(61^\alpha)$ 再次强迫普通平方 $97^2$，此行与 $13^2,61^\alpha$ 再供至少三份 3，矛盾。

令 $U(n)=n/3^{v_3(n)}\bmod3$。所有平方行输出 $\Phi_3(x)$ 的 $U$ 为 1：若 $x\equiv1\pmod3$，$\Phi_3(x)/3=x+(x-1)^2/3\equiv1\pmod3$；其余情形直接算出。$U(N)=1$ 因全部非 3 非 Euler 行指数偶且 $61\equiv1$。两高行输出的单位分别是 $269\equiv2,103\equiv1\pmod3$。由 $U(\sigma(N))=U(2N)=2$，得 $U(\sigma(61^\alpha))=1$；又 $3\nmid\alpha+1$，故 $\alpha+1\equiv1\pmod3$，联立 Euler 同余得 $\alpha\equiv9\pmod{12}$。

$A\equiv2\pmod3$，故某个 $s\equiv2\pmod3$ 在 $A$ 中为奇重数。$s>10^8$，不可能是两个高基或 Euler，$s^2\parallel N$。根行供应 $v_s(A)=1$（总容量仅 2），另一高行输出 $C$ 与 $A$ 互素。所有普通平方的 $\Phi_3(x)$ 都不含模 3 为 2 的素数，因此 **Euler 行必须再恰供一份 $s$**，即 $s\mid G_\alpha$。这排除 $G_\alpha=1$ 或 $G_\alpha\le10^8$ 的整个参数域；并不假设 $A$ 平方自由。更强的是 $A$ 内所有负类奇重数素数均需这样补齐。

**有限命题，尚未核验。** $61\nmid XD$，故 $61^\alpha<10^{892}$。$61^9>60^9=10077696\cdot10^9>10^{16}$，得 $\alpha<504$。所以只剩 $\alpha=9+12j,\ 0\le j\le41$（42 项）。对每项若用整数幂模 $A$ 求 $\gcd(A,\sum_{i=0}^\alpha61^i)$，并证 gcd 无符合上述条件的素因子，则排尽 **$H=2$ 而非整键**。切勿在模 $A$ 不可逆时盲除 $60$，用几何和倍增即可。未运行这一验算，不断言 gcd 均为 1 或均小于粗度阈值。

## 4. $(19,222)$ 五行的高基计数（Proved，局部）

采用[五个已验精确前缀](../JointConservation2400/Root19x222.md#L11-L19)的记号。第 2–5 行各有至少三个不同的高普通基（第 2 行 $19,r,u$；第 3 行 $19,t,v$；第 4、5 行 $19,t,r,v$）。第 1 行已有 $19^{222},r^{22}$，Euler 为 $t^1$，$u^2$ 且 $u\equiv1\pmod3$ 强迫 3。若 $H=2$，则 $3^2\to13^2\to61^2\to97^2$（后三基都异于固定高基和 Euler），$13,61,97$ 三个平方行各供一份 3，越过 $v_3(N)=2$。故五个前缀全部须 $H\ge3$，第一行至少再有一个不同高基。不能推广为整个 222 键排除。
