# 现行 50 个精确键：分类、条件证书及审读边界

**基准。** [main `facd7f1c3d2713e8c8d9579e29a8972211d56a3a`](https://github.com/stormwhip/PerfectNumbers/tree/facd7f1c3d2713e8c8d9579e29a8972211d56a3a)，并非上一批证书的输入提交 `495c59f`。设奇完全数 $N\le B=10^{2400}$，$p$ 是按 $19,7,11,31,13,3,5,17$ 顺序第一个整除 $N$ 的根，**不是最小素因子**；$p^e\parallel N$。八根均缺的情形已有 $\log_{10}N\ge4183.209493$。含根的 3072 片中 3031 闭合、41 开放，33 个开放片是单键片；根 5 和 17 各自的规范类全部闭合。分片与精确键不是一一对应；例如 $(7,34)$ 同在 `P7_I00002`、`P7_I00003`。本表对键去重，**没有新闭片**。逐片成员以[双向余集][front]为准，新增三整键的算术范围见[验收边界][accept]。

## 九项属性的读法

表中同一行的每个精确指数均继承本节的第 3–7 列；分组行不表示在不同指数下可移植局部证书。

1. **根与指数**：表中 $e$ 均为正偶数，故根不是 Euler 素数。各根开放片/键分别为 19：13/18，7：12/14，11：4/5，31：4/4，13：5/6，3：3/3。
2. **指标**：第二列给 $n=e+1$ 的素分解；单个数字表示质数，不表示 $\Phi_n(p)$ 是质数。
3. **强制因子**：每行均强制整个奇整数 $A=\sigma(p^e)\mid N$。表列举勘核到的具名素因子；“块”表示此处只用整数整除和阶，不是假定没有已知因子，更非把未分解数当作素数。列出的因子如未注明完整，不保证穷尽。条件首枢轴 $t$ 的子代仅在其精确指数确定后强制。
4. **精确赋值**：根赋值为 $e$；对每个奇素数 $r$，$v_r(N)=\sum_{z^h\parallel N}v_r(\sigma(z^h))$（求和限素底），故 $r\mid A$ 时 $v_r(N)\ge v_r(A)$ 而非必取等号。除唯一 $q^\alpha$（$q\equiv\alpha\equiv1\pmod4$）外皆为偶次。“缺表”指在所引资料中未提取到更强的逐键余值表，不能解释为未用过赋值筛。$s=v_p(q+1)$ 是**线性** Euler 供给，不一定是 $v_p(\sigma(q^\alpha))$。
5. **圆分结构**：$A=\prod_{d\mid n,\ d>1}\Phi_d(p)$。若 $n=\ell$ 则仅一个块；$\ell^2$ 对应 $\ell,\ell^2$ 两块；不同素数 $a,b$ 的乘积对应 $a,b,ab$ 三块。奇素数 $r\mid\Phi_d(p)$ 若 $r\nmid d$，则 $\operatorname{ord}_r(p)=d$（模 $r$ 的 $X^d-1$ 无重根），$r\equiv1\pmod{2d}$；不可略去 $r\mid d$ 的例外。
6. **大小下界**（每键的精确式，不用四舍五入的位数）：$L_0(p,e)=p^eA\mid N$，因 $A\equiv1\pmod p$。若 $t\mid A$、$v_t(N)=f$，则 $L_1=L_0t^{f-v_t(A)}\mid N$。若固定整个精确前缀 $X$（互异素幂之积），$\operatorname{lcm}(X,\operatorname{odd}(\sigma(X)))\mid N$。参考[总证明 §2][proof]。这些是**逐键可代入的下界，不是仓库的最优下界**；没有各活叶统一、经审阅的最强数值表。只在 $L>B$ 时删叶，不能用 $\lfloor\log_{10}L\rfloor=2400$ 决定严格性。
7. **丰度**：每键都有 $I(N/p^e)=2p^e/A$，且 $N/p^e$ 必含 $A$。例如对具名素因子集合 $T\subseteq\{r:r\mid A\}$ 必有 $\prod_{r\in T} I(r^{v_r(A)})\le 2p^e/A$。固定额外精确前缀 $X$ 后要求 $I(N/X)=2/I(X)$；不能把部分支持上的丰度失败推广到整键。在 $N\le B$ 下 $3,5,7$ 至少有一个出现；若 $3,5$ 均缺，则 $7,11,13$ 都出现，且 $17,19$ 至少有一项出现（[总证明][proof]）。[历史支持位图][support]给每个现行键一个可查的**上覆盖**，不是最新余域计数或可实现性证据。没有据此构造逐键“最佳丰度”。
8. **为何未闭**及 9. **共有结构**分别由末列的具体活域及类别给出。L＝低精确指数/多支持，直接根质量弱，必须把后续赋值或丰度耦合；P＝强制大素数已知但其幂次未定，森林只排部分整条首纤维；J＝多个已付枢轴需联合供给，单目标价不可各付一次；A＝大圆分块的因子可兼任供应者、Euler 或其来源，阶与粗度未决定重数。这是剩余证明义务分类，**不表示存在一个满足所有剪枝的实际候选整数**。

## 精确键逐根表

**全表共用的因子与圆分索引。** 对下表每个 $(p,e)$，在[历史 110 键逐键 TSV](https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/Session20261126/OpenFrontier.tsv)按前两列取对应行，直接取得所登记的全部 `known_small_prime_divisors`、`indices` 和剥除所列因子后的 `unchecked_remainder_bits`；这些列不因全局前沿缩小而变化。例如 $(19,8)$ 列 3,127,523,29989，$(19,10)$ 列 104281，$(19,12)$ 列 599,29251，$(19,32)$ 列 3,67,127,2113,104281，$(7,24)$ 列 2551,2801，$(19,222)$ 另有 2677，$(19,276)$ 另有 1109。[对应检验器](https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/Session20261126/CheckFrontier.py#L7-L18)核查所列小素因子的素性、整除及余块位长，**未声称所有小于阈值的因子都已列出**；空格不等于素性或全区间粗度证明。最后的 `ordinary_forest_score_discovery_only` 不作大小证书。取键全集与分片归属仍须用当前[双向余集][front]，不能用历史 110 代替 50。下表具名因子为该查表结果的补充或便于阅读的摘录。

|$(p,e)$|$e+1$（分组按顺序对应）|具名强制因子或块|尚需覆盖的域、证据与共性|
|---|---|---|---|
|19：2,8,14,20,32|3，$3^2$，$3\cdot5$，$3\cdot7$，$3\cdot11$|均含 $\Phi_3(19)=3\cdot127$；14 另含 $151,911$，20 另含 $701,70841$|L。$v_3(A)=v_3(e+1)$，3 是普通成分。对 14，[支持筛][ss]余八种八根支持，皆含 3、31 且禁 5（必要而非充分）；2、20 也有表中完整支持排除。各支持下 Euler 的位置与 $v_3$ 条件见[总证明][proof]。|
|19：4,6|5，7|分别 $A=151\cdot911,\ 701\cdot70841$|L。由 $\Phi_5(19),\Phi_7(19)$ 的整数乘积即可核对；缺统一首赋值表。|
|19：10,12,16,18|11，13，17，19|各自 $\Phi_n(19)$；18 时指标素数 19 不除块（$A\equiv1\pmod{19}$）|L。只有一个指标，不能由指标数量强制第二个不同本原因子；逐键支持上覆盖见[位图][support]，缺统一深层余表。|
|19：30|31|$t=243270318891483838103593381595151809701$|P。历史无额外掩码的首域余 1,2,12,18；三个特定完整掩码另已排，不能推广到所有支持（[精确回执][r30]）。|
|19：46|47|$t=\Phi_{47}(19)$ 本身有素性认证|P/A。首值 6,10,12。前两支各有下一枢轴；$t^{12}$ 下 Euler 一次且在 $\sigma(t^{12})$ 外。[精确子域及定价表][r46]。|
|19：48|$7^2$|$701,70841$ 来自 $\Phi_7(19)$，另有 $\Phi_{49}(19)$|L。两个不同指标只保证相应阶的因子，未固定两块的全部重数或根供给。|
|19：222|223|$t=7579985624053$，第二枢轴 $r=3705121363$|J。$(v_t,v_r)=(1,22)$ 下 $v_{3789992812027}=2,16$；$(18,2)$ 和 $(18,22)$ 下 $v_{108501737266216818637411}$ 分别为 10 和 6,10。[仅余五个精确第三值][r222]，不是五个完整叶证明。|
|19：276|277|$t=1176672733$|P/J。现余 $v_t=2,8,16,28$；16 下指定 104 位第二枢轴仍有 2、4 两值。首值 1,18 是经新证书独立排除，不引用已撤回的推导（[交付清单][r276]）。|
|19：358|359|$38518547,1491133067$|J。[联合价与森林][r358]排除 968 个双枢轴精确值对中的 877 个；余 91 个不能用两个单坐标投影的计数替代。|
|19：432|433|$t=11842464881317660217$|P/J。早期余 1,6,12,14,16,18,20,22；后由[20、22 的联合价][r432]和[18 的独立回执][r432b]缩至 1,6,12,14,16。$A/t$ 不能因未分解即视为素数。|
|7：4,6,10,24|5，7，11，$5^2$|4：2801；6：$29,4733$；10：$1123,293459$；24：2801 来自 $\Phi_5(7)$|L。前三个相应几何和分别等于 2801、$29\cdot4733$、$1123\cdot293459$。24 还有 $\Phi_{25}(7)$；只可共享整除因子，不共享精确排除。|
|7：12|13|$Q=16148168401$|P。$v_Q=12,42$；前者下，令 $T=\sigma(Q^{12})/13$，则只余 $v_T(N)=2$，而 3453283 仍有未排指数；后者下 $v_{173}=2,6,10$。[两支证书][r712]。|
|7：16,18|17，19|首枢轴分别 2767631689、4534166740403|P。[首域与裸幂尾][r716]、[后续补证][g28]；不能把历史第一批余数当作当前全集。|
|7：34|$5\cdot7$|$A=29\cdot2801\cdot4733\cdot2127431041\cdot77192844961$|P/L。最后一素数作首枢轴；78 个直接可行值已排 57，余 21。前序禁 19；Euler 奇次不能预删。[完整因子与精确表][r734]。|
|7：456,738,906|457，739，907|匿名 $\Phi_n(7)$；每一素因子均 $1\bmod 2n$|A。[三键共用的供应/平方深度约束][anon]。906 还必须 $\omega(A)\ge3$、$s\le679$；若 $\alpha\ge5$ 或 $s=0$ 则 $\omega(A)\ge4$，不需平方自由假设（[因子数][r906]、[线性上界][r906s]）。不能移用到另两键。|
|7：486|487|$t=349667,u=1229048719$，各有一单位初始流入|J。$i=v_t(N),j=v_u(N)$ 正偶，$v_t(q+1)=i-1$ 对所有 Euler 指数成立。1517 个联合格点中[排 905 个、余 612 个][r486]，不能将 $i,j$ 当独立。|
|7：600|601|$\Phi_{601}(7)$ 单块|A。阶仅给出 $r\equiv1\pmod{1202}$，本表未定位具名首枢轴或单键完整余表。|
|7：808|809|$\Phi_{809}(7)$ 合数，素因子均 $1\bmod1618$|A。[$s\le707$][r808]；[若平方自由则至少三素因子][r808sf]，不许把有重因子的双因子情形一同删除。|
|11：4,6,16,18,48|5，7，17，19，$7^2$|九组低键的[完整分解表][fac]含这五键；首枢轴分别 3221、45319、50544702849929377、6115909044841454629、100641220283951395639601683|P。按此顺序首值余 169,77,18,21,10。16 与 48 的逐值列表和 $v_t=24$ 的后继障碍见[最终回执][r1113]。|
|31：2|3|$A=3\cdot331$|P。[131/143 后的 12 个 $v_{331}$][r312]：4,6,130,150,172,178,192,222,240,250,280,282。|
|31：268|269|3229，且 $v_{3229}(A)=1$|P/J/A。[独立覆盖][r31268]只余 $3229^{102}\parallel N$；$A/3229$ 与 $\Phi_{103}(3229)$ 的未名支持、内外 Euler 和来源仍竞用已计质量。|
|31：456,466|457，467|匿名单块 $\Phi_n(31)$，已证合数、非平方、无 $\le10^8$ 素因子|A。$\alpha\ge5$ 时分别排 $s\ge140,136$，但不排一次 Euler；更高指数的阶梯上界以及来源形状见[条件表][r31]。456 与 $(7,456)$ 同指标，**不**保证有同一因子、也不保证支持互斥。|
|13：2,4,6,8|3，5，7，$3^2$|[完整分解][fac]依次为 $3\cdot61,30941,5229043,3^2\cdot61\cdot1609669$|P/L。各取最大因子作首枢轴，依次余 246,94,35,76 个首值；尾与整纤维覆盖见[分域回执][r1113]。|
|13：612,618|613，619|匿名单块（2265、2287 比特）；素因子均 $1\bmod2n$|A。主线独立接受的 $s$ 上界分别 535、532；$s\ge303,306$ 时分别强迫 $q^1$ 且 $q\nmid A$，$s\ge466,460$ 时发射者必须在 $A$ 内（各与所剩上界交）。[精确条件][pos13]、[独立端点][end13]。不将作者侧 612 的额外未独立集成窗口升级。|
|3：6,12|7，13|$A$ 分别是 1093、797161|P/A。6：首值 2,156,256；2 下 $v_{398581}=102,108,150$，156 下 $v_{2035349}=46$。12：首值 1,96，1 下 $v_{398581}=102,108$；**66 已整纤维排除**。最深若干窗口虽缩小，仍未覆盖这些前缀。[历史与覆盖][low3]、[新增条件][new3]。|
|3：856|857|$A=\Phi_{857}(3)$ 的素因子皆 $1\bmod1714$ 且 $\ge100097600002$；平方自由核 $K\ge13000000000001$|A。$q^1$、$q\nmid A$、$s>0$ 时，发射 $q$ 的普通底数若在 $A$ 外则 $s\ge699$，若在 $A$ 内则 $s\ge680$；两类互斥且穷尽：$v_q(\sigma(N))=v_q(2N)=1$，故恰有一个素幂发出一个 $q$；$q\nmid A$ 且 $q\nmid\sigma(q)$，该素幂必为普通成分。$K$ 是奇重数因子的乘积，**不是**每个素因子的下界。[两类阈值][dom3]、[核回执][ker3]。|

## 为什么证书并集还没有形成定理

* **证什么。** [算术证明索引][acceptedkeys]记录的 $(7,438),(31,6),(7,48)$ 都是整键，但只有前两者清空分片。典型森林终端重建每个固定素幂的真正奇因子和；只激活被实际整除的孩子，剥净显式支持后才可对不同来源的剩余流入相乘。Euler 奇指数总容量为一，不能每棵子树各免一次。首枢轴的 $f$ 从合法流入下界走到第一次严格裸幂超支，**中间不能跳过奇 Euler 选项**。参见[独立递推及尾段含义][forest]；证明数据哈希、算术入口、独立审阅在[活动账本][ledger]按精确条件挂接。
* **不证什么。** [投影器][proj]从冻结输入核对集合差与正反映射，不验证每个整数终端；反之两个实现同读一张漏域表也不能证明覆盖。848 条活动条件允许相交，既不是 848 个整键，也不是互不相交的反例数。全历史从零冷重放及固定机器 72 小时验收尚未完成。本次只读来源、手核小等式，未运行验证、搜索、分解或优化代码。
* **已知失败 1：高权最小提升。** $\operatorname{ord}_{19}(83)=3$，$83^2+83+1=19\cdot367$，$83^2<19^6$，而 $83\equiv7\pmod{19}$。权 6、阶 3 的正亏格仅推出 $b<19^{3z}$，不能只查 $b<19^z$。[撤回说明][withdraw]；反例否定的是枚举论证，不是 $(19,276)$ 本身。
* **已知失败 2：匿名质量与来源共用。** 指定 $q$ 在已付 $A$ 内不能再收整个 $q$；若发射者 $r\mid A$，只可另收真实的超额幂。对同一来源分别得到两个 $N$ 的下界时，乘积是 $N^2$ 的下界。[五个匿名键的松弛见证][anon]按 $(7,906),(7,738),(7,456),(13,612),(13,618)$ 顺序给出标量模型对数下取整 2317、1889、1174、2063、2084；它们既非真实反例，**也不是这些键的数学下界**。这些见证说明即使验证线性 Euler 候选素性，仅靠该组标量不等式仍不足。应查实际同余、块的奇重数核、以及每个具体来源是否能同时提供所需流入。
* **已知失败 3：局部支持或因子身份冒充整域。** $(19,432)$ 早期高 Euler 情况及非对称分摊缺证，[审阅拒收][with432]；后来的真证书是互素有效长度的联合预算，并非被拒论证复活。$(19,276)$ 的 $t^{16}$ 子代也曾用未认证合数作标签，被冷验拒绝。[原始记录][r276]。支持分割只有在全部合法掩码及其全部精确指数、尾段都覆盖后才能移除对应键。

**可检验的共同问题。** 低根域要把多个仍可能的支持与同一实际幂次的流入、丰度同时绑定；大指标域需要识别或限制已付几何块中的内部供应者，外部和内部情形分别计费。在二者之间，$(31,268)$ 虽仅有一个首指数，却立即产生两个大匿名块；$(19,222)$ 虽仅有五个第三值，仍须解决各自后继的全域。这两种瓶颈不能靠增加“已排局部格点”的统计量消除。

[front]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/OpenFrontier.json
[accept]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Validation.md
[proof]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Documentation/Proof2400.md
[support]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/Session20261126/OpenSupport.json
[ss]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/SupportSplit/Readme.md#L19-L27
[r30]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/Night2400/Receipts/Review19x30.md#L19-L29
[r46]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/TenNext/Proof46.md
[r222]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Nineteen/Frontier222.md
[r276]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Nineteen/ReleaseInventory.md#L25-L33
[r358]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/Triple/ForestSupplement.md
[r432]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/Dual/Proof.md
[r432b]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/Others/F18Review.md
[r712]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Seven/Proof.md#L5-L28
[r716]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/LowSeven/Summary.md
[g28]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/GeminiFrontier/November28/Review.md
[r734]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Propagation/Root34.md
[anon]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/Session20261126/Anonymous/AnonymousGuard.md
[r906]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/AuditNext/FourFactors906.md
[r906s]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/AuditNext/SieveUpperReview.md
[r486]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/PairSeven/Emitter.md
[r808]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root7x808Receipt.md
[r808sf]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root808SquarefreeReceipt.md
[fac]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/ElevenThirteen/Coverage.py#L13-L19
[r1113]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/ElevenThirteen/FinalReceipt.md
[r312]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root31AdditionalReceipt.md#L28-L38
[r31268]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root31Q156Q210Receipt.md
[r31]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/ThirtyOne/Proof.md#L21-L34
[pos13]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Propagation/Anonymous13.md
[end13]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root13GeneralWindowReceipt.md
[low3]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/FinalNight2400/Report.md#L30-L36
[new3]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/RootThreeFinalShort.md
[dom3]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Results.json#L6362-L6404
[ker3]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root3Native698Receipt.md
[acceptedkeys]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Proof.md
[ledger]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Results.json
[forest]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/Audit/Root31UpperReceipt.md#L3-L9
[proj]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/AstraFinalAfternoon2400/VerifyLedger.py
[withdraw]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/KimiFrontier/November28/Retraction.md
[with432]: https://github.com/stormwhip/PerfectNumbers/blob/facd7f1c3d2713e8c8d9579e29a8972211d56a3a/Research/GeminiFrontier/Review.md#L29-L35
