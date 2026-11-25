# 精确供给与合并短多项式窗

基线 `6732a1a894817457a1bc1b88b7d214ac4d6c9872`。这里只研究 `p^e || N, N≤10^2400` 及相应规范禁素域。窗口或未决几何盒不是完全数，也不等于已排除一个实际指数。本目录不写全局账本。

## 来源的联合区间

沿用 [DirectedSource](../Nov25/DirectedSource.py) 的高次 Euler、内部 Euler、已知供给源及外源判定。对 `p=7,11,19` 和本文例子，guard 过后不失一般性有 `q || N, q∤A=σ(p^e)`。记 `s=v_p(q+1)`；对未知内源 `r^c || A, r^f || N, q | σ(r^f)`，有偶数 `f`，`g=f-c≥0` 与 `b=v_p(σ(r^f))≤e−s`。保留原[分圆块尺寸和估值两套独立账](../NightUniformReview/Review.md)，绝不把它们直接相乘。设 `P=p^(e+1), Z=p^(s+b)`；由已有 D,E 引理，`r^g>q Z /[max(P,q)(P/Z+4)]`。这是用 `Z` 整除两个平衡分子的版本；当 `E=0` 将强迫 `b+s≥e+1`，与 `p^e || N` 矛盾。

**入账。** 在 `2N=σ(N)` 中，`A σ(r^f)/p^b`（奇数）整除 `N` 且与 `p` 互素，其 `r` 次数恰为 `c`。故 `p^e A σ(r^f)r^g /p^b | N`。由于 `σ(r^f)>r^f`，`r^(2f-c)<B p^b/(p^e A)`。此外，来自 `σ(r^f)` 的大小 `r^f>2q p^b/3`，与去掉源重复溢价的估值上界 `r^f≤B p^(κ(s+b))/(V_rest q)` 同时成立。这三条是相交，不是相乘。正供给的源不可能兼任零供给残块的特殊素数；`b=0` 保守退回对应估值溢价；尺寸账中仅 g 奇才需要退一个平方补位。

**精确搜索。** 对每个 `s` 写 `q=2p^s k−1, k` 正奇（这里仅处理 `s>0`），用禁素、精确 s、小除数及 Fermat 反证逐个排除前缀 k，首次未排者给下界 Q；Fermat 通过不作为素性证书。在 `b∈[i,j]` 中用 i 作必要下界，用 j 作放宽上界，若可能再二分，到单点再签多项式。假设真实 `r` 可达，则每层包含它。对子区间 `s0≤s≤s1`，同理采用 `Z_lo=p^(s0+i)`，`Z_hi=p^min(e,s1+j)`，`Q=min_s Q_s`：`q/max(P,q)`、`Z/(P/Z+4)`均单调递增。相关松弛保留了所有合法源；相邻窗口的凸包未必可证，必须实际重放。

**第二个短多项式。** 令 `w=σ(r^f)/(p^b q)`。它为正奇数且 p∤w；若 `r≤u`，则 `w≤σ(u^f)/(p^b Q)`（记号 `σ(u^f)` 此处指几何和 `1+…+u^f`，u 不必素）。对 `b>0, p∤f+1` 的每个非平凡根，

`σ_f(r)+p^b w ≡ 0 mod p^(b+s)`。

固定小 w，非平凡根是简单根；发现端以 `(r−1)` 乘上该式，独验端直接用 `σ_f` 及导数 Hensel，均与 `r=1 mod 2h` 合并。未穷尽或奇异情形保留。较大 w 使用基线 Coppersmith 型构造：若 r=z+Tj, r^c | C，候选整多项式在真实 j 处被 r^m 整除；系数范数的严格上界强迫为 0，再用有理因子/精确 Sturm 验算排除实际整根。[原始验证器](../NightMerge/LatticeLeaf.py)不运行 LLL。发现时合并同一 `(C,c,z,T)` 在不同 b、s 的有界区间；验证每次检查所需区间被已验闭区间的并完全覆盖，不跳过缝隙。

## 分层复验

- [Joint](Joint.py) + 历史区间覆盖搜索（探索脚本未包含在最小发布中） 为发现与主验；[Independent](Independent.py) 从整数 `(c,g)` 和全部 `b` 独立构造必要条件，标准库，无 FLINT。依赖的上游子引理是估值 profile、确定性素性、已审 CRT 矩形、整数短多项式验算；不宣称这些也是本轮重写。独验只验证**未知内源**；必须再逐 s 检查已知和外源空。根十九的完整闭合已被另一队用不相关森林证明，只作校准。
- `(11,718)`: 基线 115 个 s=426..540 存留，每窗外源均空，已知内源均空，剩下 only-rough；该性质由注意 `DirectedSource.run` 的先已知后粗源搜索次序可判。在已知内源命中时根本不会进入粗源循环。无格叶的联合表剩 99 窗；16 个空窗为 `426..431,531..540`。其余窗口必须有独立覆盖；完整性由余窗表决定。
- `(7,1018)`: 基线 214 窗且39有外源，尾 `443..448` 新空双验；`235` 虽无未知内源，外源仍存，不能移入空窗。
- `(19,676)`: 原112窗，精确 b 免叶删除12，短余因子再删280；440余位的初始粗盒收至约二百到三百位的同数量级上下界。属于校准。`(31,486)` 初始内部 Euler guard 不过；根13不可套用 `p=3 mod 4` 的二次互反符号。

以上是先前粗盒/格叶的历史基准。**后续的二阶供给数字筛及冻结复验入口**见 [DigitProof](DigitProof.md) 和 [Release](Release.py)，该路径不读取任何下述旧格包。根五模型只读审计见 [FiveAudit](FiveAudit.md)。研究目录中可能另有未发布的探索文件；发布时以冻结哈希清单为准。

旧格包复验命令（仅适用于含探索档案的研究工作树；不是最小发布所必需）：

```text
python -I -S -B Research/MiddaySupply/Independent.py Batch11.json --cap 65 --out IndependentBatch11.json
python -I -S -B Research/MiddaySupply/Independent.py Hull11Discover.json --cap 65 --leaves Hull11.json.gz --out IndependentHull11.json
python -I -S -B Research/MiddaySupply/Independent.py Batch11.json --band 450 458 --cap 65 --leaves Band11b.json.gz --out IndependentBand11b.json
```

`None`/`null` 代表该验证器穷尽对应未知内源域，不是已排除整个 p,e。在只有部分证书、超时或保留实例时，不发证。见单独汇总收据。
