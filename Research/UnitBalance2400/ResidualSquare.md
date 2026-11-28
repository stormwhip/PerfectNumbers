# 不枚举 Euler 素数的平方余量方程

**目的。** 把外部一次 Euler 域按未知平方而非按根指数之后的因子链重参数化。本节不声称这比已有方法快，也不声称全体 Euler 指数为一。背景是 [Dris, *A new approach to odd perfect numbers via GCDs*, 预印本](https://arxiv.org/abs/2202.08116) 所研究的 Euler 行与平方部分的公因子；以下等价式只依赖乘法性，有独立推导。

**引理 1（保留共享重数的平方补齐）。** 对正奇数 $D$，写 $k(D)=\prod_{v_l(D)\text{ 奇}}l$。若 $D\mid V^2$，则存在唯一正整数 $z$ 使 $V^2=Dk(D)z^2$（取 $V>0$）。特别地 $k(uv)=k(u)k(v)/\gcd(k(u),k(v))^2$。

**证明。** 逐素数考察：平方指数至少为不小于 $v_l(D)$ 的最小偶数，其余指数仍为非负偶数。乘积式是奇偶位相加的结果。∎

**定理 2（外部一次 Euler 的反向判据）。** 给定奇素数 $p$、正偶数 $e$，置 $X=p^e,A=\sigma(X)$。取 $1\le s\le e$ 和正奇数 $m$，$(m,p)=1$，$Q=2p^sm-1$。以下两项等价：

1. 存在奇完全数 $N\le B$ 有 $p^e\parallel N$，$Q$ 为其一次 Euler 素数且 $Q\nmid A$。
2. $Q$ 为素数，$Q\nmid A$，且有正整数 $z$，置 $F=Am k(Am)$、$T=Fz^2$，满足
\[
 (T,2pQ)=1,\qquad XQT\le B,\qquad Am\,\sigma(T)=p^{e-s}QT . \tag{*}
\]
若还要求规范根，则两侧都加上相同前序禁素。乘子 $m$ 和因子和 $A$ 可以有公因子。

**证明。** 正向：$N=XQT$，$T$ 为奇平方，且与 $pQ$ 互素。$A(Q+1)\mid2N$，$Am$ 与 $pQ$ 互素，故 $Am\mid T$。即便 $A$ 和 $m$ 不互素，其乘积也确实出现于两个不同来源。引理 1 给出 $T=Fz^2$。用 $\sigma(N)=A(Q+1)\sigma(T)=2N$ 消去 $2p^s$ 得到 $(*)$。反向：由互素性、$Q\equiv1\pmod4$ 以及 $(*)$，$N=XQT$ 的除数和正好等于 $2N$，精确指数和 Euler 身份均满足。∎

**一个无需分解 $A$ 的剪枝。** 总有 $m\le\lfloor\sqrt{B/(XAp^s)}\rfloor$，因为 $Q\ge p^sm$ 且 $T\ge Am$。在 $(m,A)=1$ 的子域，还必须
\[
  X(2p^sm-1)A\,k(A)\,m\,k(m)\le B .
\]
对 $(3,856)$，已证 $A$ 的最小素因子大于 $100097600001$，故所有 $m\le100097600001$ 自动满足互素前提，且 $k(A)\ge13000000000001$，可直接代入。见[已审计的素因子范围](../AstraFinalAfternoon2400/Audit/Root3x856Receipt.md)及[平方核端点](../AstraFinalAfternoon2400/Audit/Root3Native698Receipt.md)。若 $m$ 与 $A$ 共享奇重数因子，不能继续乘这两个独立核。例如 $A=m=5$ 时 $k(Am)=1$ 而不是 25。

**从平方侧出发（不依赖分片的等价式）。** 对任意奇平方 $U>1$，置 $D=2U-\sigma(U)$。存在一次 Euler 素数使 $QU$ 完全，当且仅当 $D>0$，$D\mid\sigma(U)$，$Q=\sigma(U)/D$ 是与 $U$ 互素且 $1\bmod4$ 的素数。因为 $(Q+1)\sigma(U)=2QU$ 等价于 $QD=\sigma(U)$。且 $D=2U/(Q+1)$，所以 $QU\le B$ 时，$U$ 的大小与亏量 $D$ 不是独立参数。这是一次 Euler 子域的替代覆盖；没有把未知的 $\sigma(U)$ 变成显式常数。高次 Euler 仍须另证。

**后续有限命题的边界。** 对 $(3,856)$ 可依来源位置分 $s=680,\ldots,856$（内部）或 $s=699,\ldots,856$（外部），逐 $s$ 取上述完整 $m$ 上界。对每个未由合数证据或禁素排除的 $Q$，只须排除 $1\le z\le\lfloor\sqrt{B/(XQF)}\rfloor$ 中的 $(*)$。缺少 $k(Am)$ 实值时不能用未经证明的平方自由性产生这个区间；可改用 $k(Am)$ 的已证下界给出包含真实 $z$ 的区间，在最终判据中仍须使用真实的 $F$。根三 $m=1$ 的部分范围另见[素数深度定理](UnitBalance.md)。这些区间的非存在性**没有得到证明**，即使能够列出端点也不属于 Verification Pending 的闭键。根本难点是给 $\sigma(Fz^2)$ 建立利用精确亏量的界，而不只是以 $F$ 的不同素因子个数估计丰度。
