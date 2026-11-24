# Euler 指数为 1 的筛法与高次 Euler 分支估价

Claude 的一批证书排除了四个根与实际指数对 `(19, 752)`、`(7, 1138)`、`(11, 838)`、`(13, 862)`。相对 2,015 项闭合的 Teichmüller 基线，后两项关闭 `P11_I00144` 和 `P13_I00149`。后者覆盖的另一实际指数 1725 由基线尺寸判据排除。前两项对应的分片仍有其他待证指数。

四个实际指数及两个分片均已列入 [Gemini 批次审计](../TeichmullerValuation/GeminiBatchAudit2400.json)。在两批证书的并集上重算分片清单，净增闭合为 0，累计 2,027 / 3,072 项，剩余 1,045 项。

## 判据与证明

记 \(\kappa=\kappa_p\)（19、7、31、13 为 2，11 为 4），\(U(n)\) 为附录 B 的非 Euler 亏欠常数（只计层级 \(\le n\) 的 Teichmüller 提升）。\(s=v_p(\sigma(q^a))\)。

**R1（层级截断）。** \(v_p(\sigma(N))=v_p(2N)=e\)，\(v_p(\sigma(p^e))=0\)，Euler 素数贡献 \(s\)，所以其余（偶指数）素数恰好贡献 \(e-s\) 个单位。层级为 \(t\) 的亏欠素数一旦有贡献，至少贡献 \(t\) 个单位，故只有 \(t\le e-s\) 的亏欠素数可能出现，基线中的 \(U(e)\) 可换成 \(U(e-s)\)。非 Euler 部分仍有 \(R\ge p^{\kappa(e-s)}/U(e-s)\)。

**R3（\(a\ge5\) 五次定价）。** 断言 \(q^a\ge\max\bigl(p^{5s}/D_5(s),\,5^5\bigr)\)，其中 \(D_5(s)=\max_{t\le s}\lceil p^{5t}/x_t^{f_0}\rceil\)，取遍满足 \(x_t\equiv1\pmod4\)、精确层级 \(t\)、非前序根、非 \(p\)、非已证合数、\(x_t^{f_0}<p^{5t}\) 的提升，\(f_0=\operatorname{lcm}(o,2)-1\)。按 \(o=\operatorname{ord}_p q\) 分情形：

- \(o=1\)：由 LTE，\(s=v_p(a+1)\)。\(a+1\equiv2\pmod4\) 且 \(p^s\mid a+1\)，故 \(a\ge2p^s-1\ge5s\)，又 \(q>p\)，所以 \(q^a>p^{5s}\)。
- \(o=2\)：\(s=t+j\)，\(t=v_p(q+1)\ge1\)，\(j=v_p((a+1)/2)\)。\(q\ge2p^t-1\ge p^t\)，\(a\ge\max(5,2p^j-1)\)。\(j=0\) 时 \(q^5\ge p^{5t}\)；\(j\ge1\) 时 \(2p^j-1\ge5+5j\) 给出 \(t(2p^j-1)\ge5t+5j\)。
- \(o\ge3\) 且 \(4\nmid o\)：\(s=t+j\)，\(t=v_p(q^o-1)\)，\(\operatorname{lcm}(o,2)p^j\mid a+1\)，故 \(a\ge f_0+6(p^j-1)\)，\(f_0\ge5\)。若 \(q\ne x_t\) 则 \(q>p^t\)，\(q^{f_0}>p^{5t}\)；否则 \(q^{f_0}=x_t^{f_0}\ge p^{5t}/D_5(s)\)。余下因子 \(q^{a-f_0}\ge3^{6(p^j-1)}\ge p^{5j}\)。
- \(4\mid o\)：\(a+1\equiv2\pmod4\) 不被 \(o\) 整除，\(s=0\)。
- 恒有 \(q\ge5\)，\(a\ge5\)，所以 \(q^a\ge3125\)。

于是需要对每个 \(0\le s\le e\) 检查
\(p^{e+\kappa(e-s)}\max(p^{5s},3125D_5(s))>B\,U(e-s)\,D_5(s)\)。
整数辅助不等式由 `check_r3_lemmas` 与基线 `check_lemmas` 验证。

**R2（\(a=1\) 合数筛）。** \(a=1\) 时 \(q+1=jp^s\)，\(q\equiv1\pmod4\) 给出 \(j\equiv2\pmod4\)，\(v_p(q+1)=s\) 给出 \(p\nmid j\)。基线判据 (b)/(c) 形如 \(q\cdot X>B\cdot U(e-s)\)，\(X\) 与 \(q\) 无关，对 \(q\) 单调。因此只需对 \(j=2,6,10,\dots\)（跳过 \(p\mid j\)）逐个排除，直到某个 \(j_{\rm stop}\) 使 \(q=j_{\rm stop}p^s-1\) 满足判据。\(2s>e\) 时沿用基线引理 3（\(q\mid A\Rightarrow2s\le e\)，对一切合法 \(q\) 成立），可用 \(\max(AU,p^{\kappa(e-s)})\)。每个被跳过的 \(j\) 带一个见证：素数 \(l<2^{16}\) 满足 \(l\mid q\) 且 \(q\ne l\)（码 \(l\)），或 \(2^{q-1}\not\equiv1\pmod q\)（码 0）。

**R4（可能为素数的 \(q\)）。** \(\sigma(q)=q+1=jp^s\mid\sigma(N)=2N\)，故奇数 \(j/2\mid N\)。\(j/2\) 的素因子不是 \(p\)（\(p\nmid j\)），也不是 \(q\)（它们整除 \(q+1\)），所以指数为偶，\(\mathrm{sq}(j/2)=\prod r^{2\lceil v_r/2\rceil}\mid N\)。若 \(q\nmid A\)（代码显式检查），则 \(\operatorname{lcm}(A,\mathrm{sq}(j/2))\) 整除 \(N/(qp^e)\)，于是 \(qp^e\max(\operatorname{lcm}(A,\mathrm{sq}(j/2))U,\ p^{\kappa(e-s)})>BU(e-s)\) 排除该 \(j\)（码 −1）。\(q\mid A\) 时规则失败，直接返回未证。

**R5（前序根）。** 若前序根 \(z\mid j/2\)，则 \(z\mid q+1\mid2N\)，与 \(z\nmid N\) 矛盾（码 \(-z\)）。

## 复验

在本目录使用 Python 3.10+ 运行：

```sh
python3 EulerOneSieve.py --check ActualExponentRecords.json
for p in 19 7 11 13; do python3 IndependentReplay.py "$p" 0 || exit 1; done
```

两个入口均从同一份见证重放四条实际指数证明。第二个入口共享基础赋值估价 \(U\)，另行实现 \(D_5\)、见证检查和整数不等式，并保留未经过素性过滤的 Euler 亏损候选。仓库的 [Gemini 合并审计](../TeichmullerValuation/GeminiBatchProof2400.md) 负责生成当前开放分片清单。
