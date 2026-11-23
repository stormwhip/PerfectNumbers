# 指标容量对偶与来源素数同余

本轮核验 Gemini 2026-11-23 的根 3、5 分片方法。原程序可以复现其报告的 96 个实际指数、29 个分片。核验发现，原程序将 \(e-s\) 全部计价为外部偶幂赋值，且遗漏了小 Euler 素数和部分外部来源素数的对偶扣款。下列结果使用重新证明的分支下界。

精确复验新增排除 **74 个实际指数**，关闭 **18 个顶层分片**。根 3 排除 29 个实际指数、关闭 9 个分片，根 5 排除 45 个实际指数、关闭 9 个分片。累计闭合 **1,869 / 3,072**，剩余 **1,203**。

## 记号

固定 \(p=3\) 或 \(5\)，\(p^e\parallel N\)，其中 \(e\) 为偶数。设 \(q^{a_q}\) 为 Euler 特殊素幂，\(s=v_p(\sigma(q^{a_q}))\)，\(P=p^{e+1}\)，\(A=(P-1)/(p-1)\)，\(N=p^eAT\)。其余素因子的指数 \(f\) 为偶数。由于 \(p-1\) 是 2 的幂，

\[
b(r,f)=v_p(\sigma(r^f))=
\begin{cases}v_p(f+1),&r\equiv1\pmod p,\\0,&r\not\equiv1\pmod p.\end{cases}
\]

根之前的素数禁用。对 \(e=2\)，程序使用 \(1+1/p+1/p^2\) 作为根丰度的尺寸下界。

## 指标容量对偶和删点

对每条有理权重 \(\theta_{r,f\to w}\ge0\) 的边，检查 \(w\mid\sigma(r^f)\)，故选中 \((r,f)\) 蕴含 \(w\mid N\)。记 \(\Theta_r\) 为汇入 \(r\) 的权重总和，\(L=\lambda\ln p\)，\(\alpha(r,f)=\ln(\sigma(r^f)/r^f)\)，则外部偶幂的约化代价为

\[
C(r,f)= f\ln r+\sum_w\theta_{r,f\to w}-\Theta_r-Lb(r,f)-\mu\alpha(r,f).
\]

对选中的外部偶幂求和，流项至多等于汇入已从求和中移除的节点的总权重。因而在 \(\sum_r\min(0,\inf_f C(r,f))\) 的基础上，扣除所有 \(w\mid A\) 的 \(\Theta_w\)，即可容纳这些目标。丰度需求同时扣除 \(\sum_{r\mid A}\ln(r/(r-1))\)。大素数尾部由 \(f\ge2\) 和 \(f\ge p^b-1\ge(p-1)b\) 验证，受检素数的指数尾部使用 \(f\le\lfloor\log_3(10^{2400})\rfloor\) 限制所有赋值断点。

设 \(C_r^-\le\min(0,\inf_f C(r,f))\) 为有向取整后的下界。另行计量某个外部素数 \(r\) 的尺寸时，它的最大额外扣款为

\[
\max\bigl(0,\Theta_r+\mu\ln(r/(r-1))+C_r^-\bigr).
\]

扣款含失去的入流和丰度，同时返还原来分配给该点的负约化代价。枚举受检集合的所有节点，包括入流为零的节点。集合之外的扣款由 \(\mu\ln(R/(R-1))\) 控制，其中 \(R\) 为受检素数截断值。对 \(q\) 的扣款只取 \(r\equiv1\bmod4\)；若 \(q\mid A\)，统一扣款仍是保守下界。大 Euler 素数 \(q>10^{18}-1\) 不接收任何流且丰度对数至多 \(1/(10^{18}-1)\)。源节点的流权重和对数乘子均以整数输入复验，区间计算使用有理数和有向取整。

## 来自 \(A\) 的赋值

对 \(r\mid A\) 的偶幂，设 \(c=v_r(A)\) 和 \(b_0=\lfloor\log_p(c+1)\rfloor\)。最多 \(b_0\) 个赋值单位可由已计入 \(A\) 的尺寸承担。若 \(b>b_0\)，则

\[
(f-c)\ln r\ \ge\ (b-b_0)(p^{b_0+1}-1-c)\ln r .
\]

首个正差为 \(p^{b_0+1}-1-c\)，后续差分只增大。对扫描到的因子，程序精确除出 \(r^c\)，累加 \(b_0\)，并取最小的每单位价格。剩余因子若都至少为 \(r_0\)，其免费单位总数至多 \(\lfloor\log_{r_0^{p-1}} A_{\rm rem}\rfloor\)，因为 \(c\ge p^{b_0}-1\ge (p-1)b_0\)。其收费单位至少消耗 \(\ln r_0\)。当 \(e+1\) 为素数时，供应赋值的 \(A\) 因子满足 \(r\equiv1\bmod 2p(e+1)\)，可沿此同余类扫描。

记免费单位总上界为 \(G\)，收费单位的统一价格为 \(\rho\)。外部对偶与内部尺寸合并后，赋值项使用 \(\min(L,\rho)\max(0,e-s-G)\)。若单独计量来源素数的尺寸，则先扣除其最大赋值；\(G\) 仍可作为其他内部素数的上界。

## Euler 分支及来源素数

- 小 \(q\) 分支使用 Euler 节点扣款。由奇数 \(a_q\equiv1\bmod4\) 和 LTE，\(s\le\lfloor\log_p(10^{18})\rfloor+\lfloor\log_p(1+\lfloor\log_3(10^{2400})\rfloor)\rfloor\)。大 \(q\) 的 \(s\le20\) 分支直接使用对偶。
- 大 \(q\)、\(a_q\ge5\) 且 \(s>20\) 时，令 \(j\) 为 \(v_p(a_q+1)\) 的上界。由 \(a_q+1\equiv2\bmod4\) 与尺寸上界求 \(j\)。此时 \(q\equiv\pm1\bmod p\) 且 \(q\ge2p^{s-j}-1\)。可在 \(p^e\max(A,q^5)\) 上另加偶幂尺寸。
- \(a_q=1,\ q\mid A\) 时，写 \(A=qu\)。由 \(q\equiv-1\bmod p^s\) 得 \((p-1)u\equiv1\bmod p^s\)，故 \((p-1)u\ge p^s+1\)。再乘 \(q\ge p^s-1\) 得 \(2s\le e+1\)，由 \(e\) 为偶数得 \(2s\le e\)。
- \(a_q=1,\ q\nmid A\) 时，存在偶幂来源 \(r^f\) 使 \(q\mid\sigma(r^f)\)。外部来源 \(r\nmid A\) 贡献 \(q r^f>2q^2/3\)。内部来源 \(r\mid A\) 则贡献 \(q r^\ell\)，其中 \(\ell=f-c\)。

对内部来源，令 \(U=(p-1)A/r^c\)，\(w=\sigma(r^f)/q\)，\(Y=p^s\)。定义

\[
D=Uw(r-1)-U-r^{\ell+1},\qquad
E=U\bigl(w+\sigma(r^{c-1})\bigr)-\sigma(r^\ell).
\]

由 \(Ur^c=P-1\) 及 \(q\equiv-1\bmod Y\) 得 \(D\equiv E\equiv0\bmod Y\)。又 \(D\equiv-P\bmod(r-1)\)，所以 \(D\ne0\)。若 \(E=0\)，乘以 \(r^c\) 得 \(P(w+\sigma(r^{c-1}))=w(q+1)\)，与 \(s+v_p(w)\le e\) 矛盾。因此 \(|D|,|E|\ge Y\)。

当 \(\ell=0\) 时，\(r\le\lfloor\sqrt{A}\rfloor\)，\(Uw(r-1)<Pr/q\) 且 \(U+r<3P/(2q)+r\)。用 \(q\ge2Y-1\) 和整数交叉乘法，可判断两侧均小于 \(Y\) 的情形并排除此分支。

当 \(\ell\ge1\) 时，若 \(r-1>2P/Y\)，由 \(E\) 的两项取较大者，得到 \(r^\ell>2Y/3\) 或 \(r^\ell>qY/(3P)\)。若 \(r-1\le2P/Y\)，则由 \(D\) 得 \(U\ge Y/2\)、\(r^{\ell+1}\ge Y/2\)、\(Uw(r-1)\ge Y\) 三者至少一项。利用 \(\sigma(r^f)<3r^f/2\) 以及 \(r\le2P/Y+1\)，分别得到 \(r^\ell>qY/(3P)\)、\(r^\ell>Y^2/(5P)\)、\(r^\ell>qY^2/(3P^2)\)。全部五个界都蕴含 \(r^\ell>(Y-1)Y^2/(3P^2)\)。

## 复验文件

- [证书目录](Certificates)保存 Gemini 两个有理权重证书。生成器中的浮点值仅供搜索；[验证器](VerifyIndicatorCapacity2400.py)独立重算全部边、价格与分支。
- [合并审计](AuditIndicatorCapacity2400.py)重放上一批证书，按规范分片枚举实际指数，仅在一个分片的所有剩余实际指数均被排除时关闭该分片。结果与剩余清单见 [Audit2400.json](Audit2400.json)。
- [回归检查](IndicatorCapacityTests.py)验证非法边、伪合数、负乘子、尾部失效、对数取整和已计入 \(A\) 的赋值。
- 64 位素性检查使用 Jim Sinclair 的确定性 Miller–Rabin 基集合。[基集合验证记录](https://miller-rabin.appspot.com/)

在仓库根目录运行

~~~sh
mkdir -p Build
python3 Research/IndicatorCapacity/IndicatorCapacityTests.py
python3 Research/IndicatorCapacity/AuditIndicatorCapacity2400.py --output Build/AuditSummary2400.json
cmp Research/IndicatorCapacity/Audit2400.json Build/AuditSummary2400.json
~~~

可用 C++17 编译 [生成器](GenerateIndicatorCapacityDuals.cpp)。生成器将候选证书写入当前目录，文件名为 CandidateDualP3.json 和 CandidateDualP5.json。
