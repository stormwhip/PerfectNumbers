# Teichmüller 提升的根素数赋值计价

2026-11-24。本轮给出根 \(19,7,11,31,13\) 的统一赋值判据。根 3、5 的赋值公式依赖 \(p-1\) 为 2 的幂，这五个根需要新的判据。新判据只用每个根的一张有限“亏损表”，即可一次处理所有大指数分片。

合并审计新增闭合 **146 个顶层分片**：根 19、7、11、31、13 分别为 24、32、42、21、27。累计闭合 **2,015 / 3,072**，剩余 **1,057**。全局状态仍为 `INCOMPLETE_FRONTIER`。

## 1. 结论

设 \(N\le B=10^{2400}\) 为奇完全数，\(p\in\{19,7,11,31,13\}\)，\(p^e\parallel N\)，且原根顺序中 \(p\) 之前的根都不整除 \(N\)。令 \(A=\sigma(p^e)\)，

\[
\kappa=\min\{o-1:\ o\mid p-1,\ o\text{ 为奇数},\ o\ge3\}.
\]

五个根的 \(\kappa\) 分别为 \(2,2,4,2,2\)。对偶数 \(e\)，下列条件同时成立时不存在这样的 \(N\)：

\[
p^{3e}>B\,U_e D_e,\tag{a}
\]
\[
\forall s\in[0,e]:\quad
(2p^s-1)\,p^e\cdot
\begin{cases}
p^{\kappa(e-s)}/U_e,& 2s\le e,\\
\max\bigl(A,\ p^{\kappa(e-s)}/U_e\bigr),& 2s>e
\end{cases}
\ >\ B.\tag{b}
\]

\(U_e\)、\(D_e\) 是第 3 节定义的有限亏损积。对 \(p=13\) 的奇指数 \(e\equiv1\pmod4\)，条件为 \(p^{(1+\kappa)e}>BU_e\)。分片中每个合法实际指数都被排除时，该分片闭合。

## 2. 赋值等式

\(\sigma(N)=2N\) 且 \(p\nmid\sigma(p^e)\)，所以其他素幂向 \(p\) 提供的赋值之和恰为 \(e\)：

\[
e=\sum_{r^f\parallel N,\ r\ne p}v_p(\sigma(r^f)).
\]

设 \(o=\operatorname{ord}_p(r)\)。若 \(o=1\)，由 LTE 得 \(v_p(\sigma(r^f))=v_p(f+1)\)。若 \(o>1\)，则 \(p\mid\sigma(r^f)\) 当且仅当 \(o\mid f+1\)，此时

\[
v_p(\sigma(r^f))=\lambda(r)+v_p\!\left(\frac{f+1}{o}\right),\qquad
\lambda(r)=v_p(r^o-1)\ge1 .
\]

称 \(\lambda(r)\) 为 \(r\) 的**层级**。非 Euler 素数的 \(f\) 为偶数，\(f+1\) 为奇数，故只出现奇数阶 \(o\)。Euler 素数的 \(f\equiv1\pmod4\)，\(f+1\equiv2\pmod4\)，故 \(o\not\equiv0\pmod4\)。

## 3. Teichmüller 提升与亏损

\((\mathbb Z/p^t)^\times\) 为循环群。其中阶整除 \(o\)（\(p\nmid o\)）的元素构成唯一的 \(o\) 阶子群，模 \(p\) 约化是同构。因此 \(r\equiv a\pmod p\) 且 \(r^o\equiv1\pmod{p^t}\) 蕴含

\[
r\equiv\omega_t(a)=a^{p^{t-1}}\bmod p^t .
\]

记 \(x_t(a)\in(0,p^t)\) 为该剩余类的最小正代表。若 \(r\ne x_t(a)\)，则 \(r>p^t\)。若 \(r=x_t(a)\) 且层级恰为 \(t\)，则 \(x_t(a)\ne x_{t+1}(a)\)。理由是层级不小于 \(t+1\) 时，\(x_t(a)<p^{t+1}\) 本身就是模 \(p^{t+1}\) 的最小代表。每个素数只有一个 \((a,t)\)。

**非 Euler 亏损。** 对奇数 \(o\ge3\) 的类，若 \(x=x_t(a)\) 恰为层级 \(t\)、可能为素数、为奇数、非禁用根，且 \(x^{o-1}<p^{\kappa t}\)，记亏损 \(p^{\kappa t}/x^{o-1}\)。\(U_e\) 为层级 \(\le e\) 的全部亏损之积，向上取整。

**Euler 亏损。** 对 \(o\ge3,\ o\not\equiv0\pmod4\) 的类，令 \(f_{\min}(o)\) 为满足 \(f\ge5,\ f\equiv1\pmod4,\ o\mid f+1\) 的最小 \(f\)。若 \(x\equiv1\pmod4\) 且 \(x^{f_{\min}}<p^{2t}\)，记亏损 \(p^{2t}/x^{f_{\min}}\)。\(D_e\) 取层级 \(\le e\) 的最大亏损，因为 Euler 素数只有一个。

程序只用费马基 2 与 65,536 以下的试除剔除**已证明的合数**。保留伪素数只会增大亏损，判据仍然成立。

## 4. 单个素数的尺寸下界

**引理 1（非 Euler 素数）。** 设 \(r^f\parallel N\)，\(f\) 为偶数，\(k=v_p(\sigma(r^f))\)。则 \(r^f\ge p^{\kappa k}/\delta_r\)，其中 \(\delta_r\) 为 \(r\) 的亏损，非亏损素数取 1。

*证明。* 若 \(o=1\)，有 \(f\ge p^k-1\ge(p-1)k\)，而 \(r\equiv1\pmod{2p}\) 给出 \(r>p\)。由 \(\kappa\le p-1\) 得结论。若 \(o\ge3\) 为奇数，写 \(t=\lambda(r)\)、\(j=v_p((f+1)/o)\)，则 \(k=t+j\)，\(f\ge op^j-1\)。分解

\[
r^f\ge r^{o-1}\cdot r^{o(p^j-1)} .
\]

第一项在 \(r>p^t\) 时大于 \(p^{(o-1)t}\ge p^{\kappa t}\)；在 \(r=x_t(a)\) 时等于 \(p^{\kappa t}/\delta_r\)。第二项满足 \(r^{o(p^j-1)}\ge3^{3(p-1)j}\ge p^{\kappa j}\)，程序验证 \(3^{3(p-1)}\ge p^\kappa\)。\(\square\)

**引理 2（Euler 素数，\(f\ge5\)）。** \(q^f\ge p^{2k}/D_e\)，其中 \(k=v_p(\sigma(q^f))\)。

*证明。* 若 \(o=1\)，\(f\ge2p^k-1\ge2k\) 且 \(q>p\)。若 \(o=2\)，写 \(s=v_p(q+1)\)、\(j=v_p((f+1)/2)\)，有 \(k=s+j\)，\(q\ge2p^s-1\)，\(q^2\ge p^{2s}\)。当 \(j\ge1\) 时 \(f\ge2p^j-1\)，所以 \(q^{f-2}\ge p^{2p^j-3}\ge p^{2j}\)。其余情形 \(L=\operatorname{lcm}(o,2)\ge6\)，\(f_{\min}+1=L\)，\(f+1\ge Lp^j\)，故 \(f-f_{\min}\ge6(p^j-1)\)。于是 \(q^{f-f_{\min}}\ge3^{6(p-1)j}\ge p^{2j}\)。\(q^{f_{\min}}\) 在 \(q>p^t\) 时大于 \(p^{5t}\)，否则至少为 \(p^{2t}/D_e\)。\(\square\)

**引理 3（\(q\mid A\) 的限制）。** Euler 指数为 1 且 \(s=v_p(q+1)\) 时，若 \(q\mid A\) 则 \(2s\le e\)。

*证明。* 若 \(s\ge e+1\)，则 \(q\ge2p^{e+1}-1>A\)。否则写 \(A=qu\)。由 \((p-1)A=p^{e+1}-1\equiv-1\) 和 \(q\equiv-1\pmod{p^s}\)，得 \((p-1)u\equiv1\pmod{p^s}\)。又 \((p-1)u\ge6\)，所以 \((p-1)u\ge p^s+1\)。于是 \((p^s+1)(2p^s-1)\le p^{e+1}-1\)，即 \(2p^{2s}<p^{e+1}\)，得 \(2s\le e\)。\(\square\)

## 5. 定理的证明

设 \(e\) 为偶数，Euler 素数为 \(q^f\)，\(k_q=v_p(\sigma(q^f))\)。非 Euler 素数（不含 \(p\)）的赋值和为 \(K=e-k_q\)。由引理 1，它们的素幂之积至少为 \(p^{\kappa K}/U_e\)，因为每个亏损素数的层级不超过 \(e\)。

- \(f\ge5\)：由引理 2 及 \(\kappa\ge2\)，\(N\ge p^e\cdot p^{2K}/U_e\cdot p^{2k_q}/D_e=p^{3e}/(U_eD_e)\)。条件 (a) 给出矛盾。
- \(f=1\)：\(\sigma(q)=q+1\)，所以 \(k_q=s=v_p(q+1)\)，\(q\ge2p^s-1\)，且 \(N\ge p^e q\,p^{\kappa(e-s)}/U_e\)。若 \(2s>e\)，由引理 3 得 \(q\nmid A\)。由 \(A\mid N\) 和 \(\gcd(A,pq)=1\)，\(A\) 整除非 Euler 素幂之积，故该积至少为 \(\max(A,p^{\kappa(e-s)}/U_e)\)。条件 (b) 给出矛盾。

对 \(p=13\) 与奇指数 \(e\equiv1\pmod4\)，\(p\) 本身是 Euler 素数，其余素数都是非 Euler 素数，\(K=e\)，故 \(N\ge p^{(1+\kappa)e}/U_e\)。\(\square\)

**为什么一次能关掉很多分片。** 基础尺寸判据只用 \(p^eA\approx p^{2e}\)。新判据给出 \(N\gtrsim p^{(1+\kappa)e}\) 或 \(p^{2.5e}\)，例如 \(f=1\)、\(2s>e\) 时取 \(s\approx e/2\) 得到 \(p^{e}\cdot p^{e/2}\cdot p^{e}\)。亏损表把 \(p\)-进小素数的例外压缩为常数：各根的 \(\log_p U_{\max}\) 依次为 5.42、6.82、17.21、3.21、3.09，五个根的 Euler 亏损表均为空。表中层级最低的例外为根 19 的 \(7,11\)（\(t=1\)）、\(2819\)（\(t=4\)），根 7 的 \(3376853\)（\(t=8\)），根 11 的 \(5\)、\(3\)、\(174625993\)、\(205122373\)，根 31 的 \(5,439,521,6287\)，根 13 的 \(3\)。

## 6. 复验

[验证器](VerifyTeichmullerValuation2400.py) 只用 Python 标准库与整数比较。[合并审计](AuditTeichmullerValuation2400.py) 先完整重放指标容量审计，再对五个根的全部开放分片重建亏损表并检验每个合法实际指数。[回归检查](TeichmullerValuationTests.py) 用小模数穷举核对赋值等式、Teichmüller 层级与引理 1、2 的单素数界，并检验篡改亏损表会被拒绝。

在仓库根目录运行：

~~~sh
mkdir -p Build
python3 Research/TeichmullerValuation/TeichmullerValuationTests.py
python3 Research/TeichmullerValuation/AuditTeichmullerValuation2400.py --output Build/AuditTeichmuller2400.json
cmp Research/TeichmullerValuation/Audit2400.json Build/AuditTeichmuller2400.json
~~~

开发机实测：亏损表与五根审计约 35 秒，加上指标容量审计的完整重放约 90 秒。

全量重放通过后，复核另用 Hensel 逐位提升重建例外表，并用精确分数和独立枚举核对了每个新增分片的实际指数及规则。五根分别有 6、8、13、8、7 个非 Euler 例外，Euler 指数至少为 5 的分支均有 `D_e=1`。新增分片覆盖 173 个根与实际指数对，其中 146 个使用新判据，27 个使用尺寸判据。

## 7. 剩余问题

五个根仍有 727 个开放分片，最大开放代表指数依次为 750、1128、838、642、862。在开放分片的首个失败指数中，631 个失败于 Euler 指数 \(f\ge5\) 的分支 (a)，87 个失败于 \(f=1,\ 2s\le e\)，9 个（根 11）失败于 \(f=1,\ 2s>e\)。

分支 (a) 使用下界 \(N\ge p^{3e}/(U_eD_e)\)。可以进一步研究如何计入 \(A=\sigma(p^e)\) 的素因子，同时控制它们与赋值来源的重叠。当 \(e+1\) 为奇素数时，可利用分圆值的素因子同余限制。其他方向包括按剩余类细化赋值下界，以及将指标容量对偶推广到 \(o>1\)。
