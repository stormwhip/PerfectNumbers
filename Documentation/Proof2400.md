# 奇完全数 $10^{2400}$ 项目总证明

**目标定理。** 对任一奇完全数 $N$，有 $N>10^{2400}$。当前证明状态为 `INCOMPLETE_FRONTIER`。以下汇总已证的子域、通用引理与可复验的证明证书。

记 $B=10^{2400}$，$\sigma(n)=\sum_{d\mid n}d$，$I(n)=\sigma(n)/n$，$v_p(n)$ 为 $p$-赋值，$\operatorname{odd}(n)=n/2^{v_2(n)}$。以下取 $N$ 为满足 $\sigma(N)=2N$ 且 $N\le B$ 的假想奇数。由 Euler 结构，$N=q^aM^2$，其中 $q$ 为素数、$q\nmid M$ 且 $q\equiv a\equiv1\pmod4$。

**命题 1（当前已证明范围）。** 与八根均互素的情形满足 $\log_{10}N\ge4183.209493$，见[独立证书](../Research/Session20261122/Python/TerminalCertificate.py)。含根类共 3,072 个规范分片，已有 **2,990 个闭合，82 个开放**；开放分片含 **92 个不同的 $(p,e)$**。根 5 与根 17 的规范类均已闭合。其余各根的逐片集合见[现行账本](../Research/FinalSprint/Delta.json)，逐根分布见[当前状态](CurrentStatus2400.md)。

**11 月 26 日晚间批次。** 相对于[冻结基线](../Research/Session20261126/Delta.json)（2,974 片闭合、98 片开放、110 个待证键），[晚间精确指数证明](../Research/FinalSprint/Proof.md)新增排除 18 个不同的 $(p,e)$，其中根三的 970、990 已覆盖内、外来源。投影回分片后仅新增闭合 16 片：例如 $(7,90)$ 与 $(7,168)$ 都已排除，但 `P7_I00005` 尚余指数 12。新证书的复验与历史依赖的整套冷重放不是同一件事。

**11 月 26 日晚间前的批量命题（历史）。** 此批相对[11 月 25 日午间账本](../Research/Midday/Delta.json)的 2,868 个闭合新增 106 片，形成上述冻结基线。在如下规范根和实际指数下，$N>10^{2400}$：

* $p=19$：22, 24, 26, 28, 34, 38, 42, 44, 54, 56, 60, 76, 80, 90, 92, 106, 378, 400, 408, 438, 460, 490, 498, 540, 568, 570, 586, 592, 630, 642, 660。
* $p=7$：22, 30, 40, 42, 54, 58, 66, 76, 96, 100, 148, 178, 222, 432, 462, 540, 546, 568, 652, 658, 660, 772, 796, 820, 838, 856, 862, 928, 976。
* $p=11$：22, 24, 28, 34, 72, 210, 330, 360, 378, 408, 420, 478, 520, 522, 562, 570, 576, 598, 600, 672, 676。
* $p=31$：8, 196, 256, 280, 372, 400。
* $p=13$：24, 26, 330, 400, 438, 486, 556, 568, 570, 576, 598, 640, 646, 700, 738。
* $p=3$：10, 16, 18, 22, 28, 30, 36, 40, 42, 46, 48, 52, 58, 60, 66, 70, 72, 76, 78, 90, 100, 102, 118, 120, 130, 132, 136, 142, 160, 168, 1108, 1162。

**普通森林与精确枢轴。** 普通森林证书给出森林根 $K\subseteq\{q:q\mid A=\sigma(p^e)\}$，以及单父亲候选边。不以边本身断言整除。对某个真实节点 $z^f\parallel N$，取 $S=\operatorname{odd}(\sigma(z^f))$，剥除 $pA$ 及全部候选节点的素支持后得 $C$。该节点收取 $z^f C$；子节点 $u$ 仅于 $u\mid S$ 时激活，携带下界 $v_u(S)$。各激活来源互异，所有 $C$ 的乘积整除 $N$，且与显式素幂及初始余项支持不交。根处另收取 $p^e A/\prod_{z\in K}z^{v_z(A)}$。每棵树分别计算全偶与至多一处 Euler 奇指数的最低乘积，最后全森林只可打一次折扣。每个分支检查有限合法前缀；剩余指数只计首个尾指数的裸素幂，其后因单调性不会更低。实际整除、ECPP 链、禁素及尾界均由[双重整数重放](../Research/Session20261126/Replay.py)检查。各森林叶通过未舍入整数比较，不能只看十进对数的下取整。单枢轴包固定 $q\mid A$ 的实际指数，按 $p^e(A/q^c)q^f\le B$ 逐个枚举，其中 $c=v_q(A)$。在每个固定分支以 $X=p^e q^f$ 重建强制余项；禁素、赋值冲突、丰度过量或尺寸过大直接否决，其余分支均须通过两套整数森林遍历。完整尾由上述预算排除。普通森林可按既有整除提升引理复用，枢轴包只登记原指数。全部证书按 $(p,e)$ 求并集。由[逐片投影](../Research/Session20261126/Delta.json)，134 个不同实际指数共闭合 106 个规范分片。

**联合赋值与尺寸证书。** [供给森林](../Research/Session20261126/SupplyForest/Proof.md)在每个被真实激活的普通成分 $z^h$ 上，给 Teichmüller 供给账乘以 $\max(1,z^h/p^{\kappa v_p(\sigma(z^h))})$，所有低于一的比值已由统一亏损上界计入。对同一条有效指数分支，可以按非负整数权重乘两种下界，同时在左端取相应的 $N$ 次幂；不把分别属于两个冲突分支的价格相加。外部 Euler 一次幂 $q$ 单独计费时，至多一个余项可含 $q$，按全树一处退款处理。内部 $q\mid A$ 单列，不能直接使用外部价格。[严格算术重放](../Research/Session20261126/SupplyForest/VerifyCut.py)检查 Hensel 层、同余矩形、各合法指数及其尾。账本中相同 $(p,e)$ 的不同证法不重复计数。

**全局支持命题。** 在 $N\le B$ 下，若 $3,5\nmid N$（即二者均不整除），既有命中集要求 $7,11,13\mid N$。若再有 $17,19$ 均缺，[第一组对偶](../Research/Session20261126/GlobalSupport/Readme.md)给出向下取整的尺寸下界 $\log_{10}N\ge2467$，矛盾。因此 $17,19$ 必遇其一；若 $19$ 缺便必须含 $17$。在该补侧再分别禁止 $23$、$29$，证书下界为 2438 和 2408。因此 $3,5,19$ 都缺时，$17,23,29$ 均须出现。这里的证书均重建原始可行域及无界列，且经两种有向对数运算复验。此结论不假设 $v_p(N)$ 落在某个试验区间。

**根十三指数 568 的匿名终端。** 由两级以上的强迫素幂分割，在 2404 个状态中，除六个精确状态外，403 个分叉、1797 个质量终端、190 个固定 Euler 终端和八个丰度终端都按已有规则重算。六个特殊状态没有以猜测分解作前提：对 11 个互素的已剥离分圆块，验证合数性和非素数幂性以保证至少两个不同素因子；在与来源未分离的情形保守扣费。确定性模多项式上的区间积与 gcd 认证受价素数的全域粗度和 Teichmüller 类中的下界。再验内部 Euler 位置及外来源平方因子的格区间，保留唯一 Euler 例外后排尽剩余各窗。第五个几何和必须显式剥除有证据的因子 280483283 后才能接合公共主块界；不能把四个状态的结果直接外推。由[完整树和六个特殊状态](../Research/Session20261126/Anon568/Readme.md)排除 $(13,568)$。该证书按精确指数登记。

**定理（规范根三，指数 1162）。** 若规范根为 $3$ 且 $3^{1162}\parallel N$，则 $N>10^{2400}$。已有整数界穷尽 E0/E1/E2；只须处理一次 Euler 项 $q\nmid A=\sigma(3^{1162})$ 且 $3\mid q+1$。由下面的本原阶定理，每个向 $q$ 供给的 $r^f$ 都不供给 3。内部来源 $r\mid A$ 与外部来源 $r\nmid A$ 分别验收。对外部来源，因 $A\equiv5\pmod8$ 不是平方，必有奇重数因子需要补价；与内部供给的重数费用取最大值而非相加。独立有限筛排除 $A$ 所有不超过 10670571520001 的素因子。剩余 Euler 小前缀共有 14976 个位置，6 个未由整除或合数证据排除的位置由完整低阶子群枚举排除，得到统一基础下界 $10^{2219}$。详见[基础及来源重合证明](../Research/Session20261126/Joint/Additional.md)。

余块联合时，以 gcd 分割为两两互素的支撑块，对可能含来源的那一块在所有相关行一致扣除；在每个这样的假设内分别取森林与流入对偶的较大值，最后才对假设取最小值。[完整重放](../Research/Session20261126/JointReplay.py)强制执行范围筛以及两组 42 叶，外、内来源两组的最弱下界分别在叶 13、0，均严格越过阈值。该完整证书仅精确覆盖 1162，不作整除提升。$\square$

**定理（规范根三，指数 1108）。** 若 $3^{1108}\parallel N$ 且 $7,11,13,19,31$ 均不整除 $N$，则 $N>10^{2400}$。先以已有整数判据排尽 E0/E1/E2，并以本原阶定理及支撑二分穷尽外部 Euler 一次幂的来源。令 $A=\sigma(3^{1108})$；确定性范围筛检查 208340693 个筛后候选，证明 $A$ 的所有素因子都大于 10175119360001。对来源不整除 $A$ 的 E3a 证得公共基础 $>10^{2122}$（整数低前缀 5469575 个，须按小阶子群检验者 2909 个）；对来源整除 $A$ 的 E3b，改良余因子间隙和前缀证明基础 $>10^{2089}$。多源模型先从每条匿名余项中彻底剥除所有显式计价素数，再按每个素数的总流入容量给价，以免同一素数的净成本重复支付。内侧 42 叶均排除；外侧由普通 40 叶、扩展 16 号叶及独立 13 号叶组成，后者对 24 个弱来源原子合用 57 节点割树。外/内最弱辅助净成本分别为 640677831930、725613132094 纳奈特，加到相应的向下取整基础后，两侧均严格越过 $2400\ln10$ 的保守上界。完整有向取整、候选穷尽、无界列及固定数据绑定见[离线证明包与验收入口](../Research/Session20261126/Joint1108/Readme.md)。本结论仅登记 1108。$\square$

**条件批量定理（不计完整分片）。** 设规范根为 3，$e\ge824$，Euler 项为一次幂 $q$，$q\nmid\sigma(3^e)$ 且 $s=v_3(q+1)>0$。每个向 $q$ 供给的普通项 $r^f$ 都满足 $\operatorname{ord}_q(r)=f+1$，因此 $3\nmid f+1$ 且 $b=v_3(\sigma(r^f))=0$。若阶是真因子，奇数指标商至少为 3，故 $r^f>r^2(2q/3)^3$；又 $3^e r^f\sigma(r^f)/3^b\mid N$。与其余普通成分的赋值供给下界分别比较（不是相乘），在 $s\le701$ 和 $s\ge702$ 两域均得 $N>B$。详见[两个证明与精确端点](../Research/Session20261126/Source/SourceSquare.md)。[其他五根的双阶窗口](../Research/Session20261126/Source/OtherRoots.md)给出条件指数限制，不能把非空的窗口数计作完整指数。

**根十九的统一 Euler 位置限制（不限 $N$ 大小）。** 若 $19^e\parallel N$，$3\mid e+1$ 且 $e$ 为偶数，则 $3\cdot127=\sigma(19^2)\mid N$。令 $H$ 为八根的精确支持。若 $H=\{3,7,13,19,31\}$，必有 $13^1\parallel N,\;3^2\parallel N$；若 $H=\{3,5,19,31\}$，必有 $5^1\parallel N$，且 $v_3(N)=6,12$ 或为至少 14 的偶数；若 $H=\{3,5,13,19\}$，必有 $5^1\parallel N,\;3^2\parallel N$。前两层树分别对所示 Euler 候选与 3 枚举合法精确前缀和尾部，严格有理丰度下界或禁素排除其余各叶。只将 $19^2$ 用作丰度和流入的下界，不当作实际指数上界。各项因子均剥离 2 并证明素性。[独立枚举](../Research/Session20261126/LowSupport/Verify.py)保留每一个合法幸存叶，**不排除三个支持本身**。

**990 的历史条件引理（非现行缺口）。** [晚间完整证明](../Research/FinalSprint/Proof990.md)在以下无五引理的基础上补齐含五子域；本段只叙述晚间前的结论。若 $N\le10^{2400}$ 是规范根为 3、$3^{990}\parallel N$ 的奇完全数，则 $5\mid N$。终端证书分别覆盖 $5\nmid N$ 情况的外、内来源各 12 叶；不适用于 $5\mid N$。外来源叶 0 的 9800 个支撑原子中，粗区间未排的一项严格分解为 $5266228211\cdot4217468380980037880092527701441161\cdot237916085520023302947010376750220097331$，各质因子都不能是来源。对偶取整未越界且确实超过目标；完整前提、C++ 范围与逐域重放见[条件包](../Research/Session20261126/NoFive990/Readme.md)。此结果不会闭合 $(3,990)$；其附加 S8 支撑差量与已注册全指数分别统计。进一步，在同一假想反例中 $6\le v_5(N)\le370$ 且为偶数；若来源在 $A$ 外，其上界是 244。以供给分支整数界分别排除 $v_5\ge246$ 的外支与 $v_5\ge372$ 的两支，逐个删除几何和含禁素数的指数后，剩偶数候选数分别为64（外支）和98（全域）。这不是对 990 的完整排除。

**次级素数 3 的条件预算。** 规范根 $p\ne3$，$p^e\parallel N$，若 $b=v_3(\sigma(p^e))>0$，则 $3^h\parallel N$ 的 $h$ 为正偶数。在 Euler 成分不供给 3 的子域，其余普通成分必须供给 $h-b$；每个正供应素数 $t$ 满足 $t\equiv1\pmod3$，若供给 $j$ 单位则指数至少 $3^j-1$。取 $K=10^8$，只对 $t<10^4$ 给出一次最坏折让 $D_t=\max(1,\max_j K^j/t^{3^j-1})$，已因禁素排除的等级可跳过；不论未知素数多少，所有 $t\ge10^4$ 无须折让。对强迫出现的 $3^h$、原根和其它供应者各计一次，得 $N\prod D_t\ge p^e3^hK^{h-b}$。右端对 $h$ 递增。[整数检查](../Research/Session20261126/SecondarySupply.py)给出原 244 实际指数中全部 16 个强迫 3 的非三根键的首个不可能 $h$；例如 $(19,26)$ 时 $b=3$，本子域排除 $h\ge354$。计价含额外底数折让是保守的，不意味着 Euler 正供给子域也被排除。

**支持条件上的对偶复用。** 若同一组底数的选项至多取一个，自由选取时约化费用取 $\min(0,\min_j c_j)$。在已知精确指数 $e$ 时，该组必须取对应精确列，故可替换成 $c_e$，保留同一组非负对偶乘子及无界列检查。这只在 $e$ 对应显式精确列时适用，不能用尾列冒充精确列。[条件证书与独立键表](../Research/Session20261126/Support/Readme.md)以冻结的 6,556 个幸存支持为母集，与完整实际指数分开去重。

## 1. 覆盖规则

**引理 1（规范根与分片）。** 固定根序为 $(19,7,11,31,13,3,5,17)$。若至少一根整除 $N$，取首个整除 $N$ 的根 $p$，其前面的根均为禁素数。对该类令 $e=v_p(N)$。精确分片要求 $e=d$，整除分片要求 $d+1\mid e+1$，其中 $d$ 为该分片的代表指数。

**证明。** 根序给出互斥分割。指数的允许域由 $p^e\le B$ 和 Euler 结构确定。若 $d+1\mid e+1$，由几何级数恒等式有 $\sigma(p^d)\mid\sigma(p^e)$，可共用其因子见证。整数预筛在 $p^e\operatorname{odd}(\sigma(p^e))>B$ 或出现禁素因子时排除该指数。分片覆盖以已复验的指数全集与历史基线为准。$\square$

互素类证书将可能的素幂划分为有限显式选项、由因子约束引出的素幂选项和通用尾项。乘法丰度给出 $\sum_{r^f\parallel N}\log(\sigma(r^f)/r^f)=\log 2$。每条显式因子约束按整数模运算复核。对数用有向整数区间包围，取成本下端与丰度上端，因此实际反例在松弛模型中可行。非负对偶乘子给出模型成本下界，通用尾项的约化成本须非负。证书重算的整数下界超过 $2400\log 10$ 的上端，排除这一类。

取每个分片中尚未被基线排除的全部合法 $e$。新证书以 $(p,e)$ 为键求并集。只有该分片的每个待证 $e$ 都被覆盖时才新增一次闭合。例如 P31_I00038 需要同时排除 $172$ 与 $518$。[午间审计清单](../Research/Midday/Delta.json)记录该历史批次的指数与分片；现行剩余集合以[晚间逐片投影](../Research/FinalSprint/Delta.json)为准。

## 2. 强制因子链、尺寸与丰度

**引理 2（固定素幂的剩余因子）。** 对已固定的实际素幂积 $X=\prod_i r_i^{f_i}$ 与 $S=\sigma(X)$，有 $S/\gcd(S,2X)\mid N/X$。

**证明。** $\gcd(X,N/X)=1$ 且 $S\mid 2N$。由素数赋值得到
$$
D=\frac{S}{\gcd(S,2X)}\mid N/X.
$$
若 $D$ 与 $X$ 或禁素数积有公共因子，或 $XD>B$，即得矛盾。若 $I(X)>2$，由丰度的乘法性亦得矛盾。$\square$

写 $D=U\prod r^c$，其中 $r$ 是认证的奇素数，$U$ 保留已去掉所列因子和试除范围内小素数的剩余整数。对每个 $r$ 分别求合法最小偶指数 $f$ 和可用的 Euler 指数 $o$。否决指数可用 $r^{j+1}\equiv1\pmod{\ell(r-1)}$，这里 $\ell$ 为禁素数。若 Euler 位置尚空，先按偶幂付费，再取最多一次可行 Euler 折扣的最大值。若已有固定 Euler 项，剩余项一律用偶指数。乘以 $XU$ 得整数尺寸下界。固定一个强制底数后，枚举预算内所有合法指数并重建 $X,D$。所有子分支均推出矛盾时，实际指数才获证。

丰度叶将已识别的未固定素数贡献上界设为 $r/(r-1)$。若 $U$ 的因子均至少为 $L$，其贡献不超过 $(L/(L-1))^{\lfloor\log_L U\rfloor}$。剩余预算里若有 $j$ 个新素数，用最小 $j$ 个允许的底数估计最大丰度及最小体积。允许一次 Euler 指数时，最小体积取这些底数的平方积除以其中最大者。所得总丰度上界严格小于 2 时排除。根 5 的 $e=580$ 给出一个尺寸叶实例。其 319 位强制素因子模 4 为 3，偶指数 $2,4,6,8$ 分别触发禁素数 $3,11,7,3$，故至少为十次幂，尺寸超过 $B$。

## 3. 根赋值供给与 Euler 来源

固定 $p^e\parallel N$ 后，$\sigma(N)=2N$ 要求各成分总共提供 $e$ 个 $p$-赋值单位。已固定成分贡献 $v_p(S)$。对普通偶幂 $r^f$，以乘法阶和 LTE 定位可能的供给，再对每一级增量指数付费。若 $p=3,5$，有 $v_p(\sigma(r^f))>0$ 的普通成分必满足 $r\equiv1\pmod p$，此时第 $j$ 个单位需要 $f\ge p^j-1$。某一级的几何和出现禁素因子时，其后各级同样不可用。已计入 $X$ 或 $D$ 的幂先扣除，剩余费用才进入新下界。根 3 的整数链还按二进制统一单位价格计算折让，分别枚举 Euler 已占用、在已知强制底数和在其它底数的情形。两类尺寸下界可分别剪枝，其乘积须有不重叠的因子账。

根 3、5 的外部 Euler 一次幂分支使用以下联合界。令 $A=\sigma(p^e)$、$s=v_p(q+1)>0$、$Y=p^s$、$P=p^{e+1}$、$Q=2Y-1$。若 $q\nmid A$，则 $q\mid\sigma(N)$ 强制存在另一个普通成分 $r^f$ 满足 $q\mid\sigma(r^f)$。记 $c=v_r(A)$。当 $2^p p^eQ^{p+1}\ge3^p B$ 时，该来源提供零个 $p$-赋值单位。若 $f+1=p^jm$ 且 $j\ge1$，由 $p\nmid q-1$ 可将上面的整除降到 $\sigma(r^{m-1})$，从而 $r^f>(2q/3)^p$，与尺寸预算矛盾。对已在 $A$ 中出现的来源，$\sigma(r^f)/q$ 和 $r^c\mid A$ 的同余给出
$$
r^{f-c}>\frac{Y}{\max(1,P/q)(P/Y+4)}.
$$
当 $c=0$ 时可直接使用 $r^f>2q/3$。

当 $c>0$ 时令 $U=(P-1)/r^c$、$w=\sigma(r^f)/q$、$t=r^{f-c}$、$H=\max(1,P/q)$、$\delta=P/Y$。两个整除量为
$$
D_1=Uw(r-1)-U-rt,\qquad
D_2=Uw+U\sigma(r^{c-1})-\sigma(r^{f-c}).
$$
由 $Ur^c=P-1$ 和 $qw(r-1)=r^{f+1}-1$ 得 $Y\mid D_1$，且 $D_1\equiv-P\bmod(r-1)$，所以 $D_1\ne0$。恒等式
$$
r^c D_2=P\bigl(w+\sigma(r^{c-1})\bigr)-w(q+1)
$$
给出 $Y\mid D_2$。若 $D_2=0$，则 $v_p(w)+s\ge e+1$，与 $\sigma(N)=2N$ 的根赋值 $e$ 矛盾。又 $Uw< Htr/(r-1)$。当 $r-1<\delta+2$ 时，用 $D_1$ 的上下界得到 $Y\le |D_1|<(\delta+4)Ht$。当 $r-1\ge\delta+2$ 时，若 $D_2<0$ 则 $|D_2|<3t/2$，若 $D_2>0$ 则 $Y\le D_2<3Ht/2+\delta Y/(\delta+2)$。两种情形都给出上式所需的 $t>Y/((\delta+4)H)$。

其它供应者的第 $j$ 个单位在 $A$ 已付 $r^d$ 时至少再付 $r^{\max(d,p^j-1)-\max(d,p^{j-1}-1)}$。对大未知因子，用剩余整数给出免费单位总数 $G$ 的上界。分圆分块可加强该界。若 $r>h$ 且 $r\mid\Phi_h(p)$，则 $\operatorname{ord}_r(p)=h$。潜在免费供应者满足 $r\equiv1\bmod\operatorname{lcm}(2h,p)$，且 $r^{p-1}\mid\Phi_h(p)$。可沿等差数列试平方整除，取首个可能的底数下界。把最便宜的 $i$ 个边际成本的乘积记为 $C(i)$，非供应奇次补价去掉可能属于来源的最大一笔后记为 $J$。上面三笔费用对应不同的超额素幂，因此以下整数判据足以排除该分支
$$
p^e A Q^2Y\, C(\max(0,e-s-G))\,J
\ \ge\ B\max(P,Q)(P/Y+4).
$$

Euler 项 $q\mid A$ 时，根 3 利用 $\operatorname{ord}_q(3)$ 为奇数及二次互反推出 $q\equiv1\bmod 3$，所以 $s=v_3(a+1)$。根 5 对 $q\equiv-1\bmod5$ 令 $t=v_5(q+1)$。从 $A=qC$ 与 $4C\equiv1\bmod5^t$ 得 $2t\le e$，故 $s\le e/2+5$。对其它五根的赋值判据，以 Teichmüller 供给价格为基线，对各已知强制底数取合法指数的最小额外费用。Euler 占用某底数时扣掉该底数的全部普通供给价格。$a=1$ 时按 $q$ 是已知因子、未知内部因子或外部因子分支，短等差区间可用精确整数枚举。$a\ge5$ 使用已证 Euler 供给尺寸界。根 5 的丰度与赋值联合叶使用已验证的有理对偶，删去已单独计价的因子、相应流入及可能的 Euler 和来源价格后应用，详细证书由两套遍历重算。

### 夜间增量：来源自身的赋值也提高间隙模数

在上段内部来源的记号下，令 $b=v_p(w)$。因为 $q\ne p$，这也是 $v_p(\sigma(r^f))$。由 $s+b\le e$，取 $Z=p^{s+b}$，有 $Z\mid P$ 且 $Z\mid w(q+1)$。此处**并不要求** $Z\mid q+1$。两个恒等式分别为
$$
r^cD_1=P(w(r-1)-1)-(q+1)w(r-1),\qquad r^cD_2=P(w+\sigma(r^{c-1}))-w(q+1).
$$
既然 $p\nmid r$，两个非零整数均被 $Z$ 整除。复用上段的正负号估计，取 $H=\max(1,P/q)$、$\delta=P/Z$，即可得 $r^{f-c}>Z/[H(P/Z+4)]$。若只能证明 $b\ge b_0$，用 $Z=p^{s+b_0}$ 仍保守；Euler 素数本身的下界仍是 $q\ge Q=\max(5,2p^s-1)$，不得把 Q 中的 $p^s$ 改为 Z。

已知 $r^c\mid C$、$r\equiv z\pmod T$ 时，还可在剩余有限区间上排除整个未知素因子，而不分解 C。若 $\gcd(T,C)=1$，把 $r=\mathrm{center}+Tk$ 写成区间中央的整数多项式，令 $b'=\mathrm{center}\,T^{-1}\bmod C$。真解满足 $r\mid k+b'$。取 $m\ge1$，则 $C^{\lceil(m-i)/c\rceil}(k+b')^i$（$0\le i\le m$）及 $k^j(k+b')^m$ 在真解处均被 $r^m$ 整除。发现器可用 LLL 建议整数线性组合 $F(k)=\sum a_j k^j$，但[标准库验证器](../Research/NightMerge/LatticeLeaf.py)逐项重建整数系数；只有 $\sum |a_j|K^j<r_{\min}^m$（$|k|\le K$）时才推出 $F(k)=0$。随后用精确除法及 Sturm 计数排除整数根，区间的覆盖和两个端点也须复核。一个实例是 $(11,760)$：全 761 个赋值，共有三个难窗，补入 28 项可验证短多项式后才计闭合。余因子方向的矩形计数和整段共享短证书见[独立核验](../Research/NightUniformReview/Verify31.py)。这些都是条件排除规则，并非全根类定理。

### 夜间增量：静态素数森林与无关指数的支持排除

对固定根取 $A=\sigma(p^e)$，指定一组经认证的 $A$ 的素因子为森林根。每个候选次级素数只可有一个父节点，且不整除 $pA$；只有它**确实整除父节点当前精确指数的几何和**时才触发。把 $pA$ 及所有潜在森林素数的支持从每个实际触发节点的奇因子和中去净。剩下的各项可相乘：它们来自不同精确素幂的因子和，其乘积本来就是 $\sigma(N)$ 的因子；即使余因子之间不互素，其重数也不会丢失。这笔纯外部费用与已剥除支持的成本没有重叠。自叶向根以整数比较求各合法指数的最低成本，尾段仅保留单调的素幂下界，允许唯一 Euler 例外在任一触发节点或完全在森林外。[重放](../Research/NightLowRoute/Release/ForestReplay.py)在每个包检查无环、父亲唯一、素性、实际整除、所有 Euler 位置及指数尾。与共享指数的充分条件不同，森林若只排除一个实际指数，仍须在所有相关分片回填，而非按受益分片数直接加分。

另有不取具体 $e$ 的结论：在八根中任选以下一根允许出现、其余七根均不整除 $N$，则在只允许 19、31、13 的三个类别分别得到 $\log_{10}N\ge2658.984830,3116.739321,2494.264085$。验证器重建松弛、恢复符合新禁素表的选项、重新核验所有使用的整除蕴含、有向对数和无界尾的非负约化成本。允许 17 的相应证书也超过目标，但并非新的 17 类结论。复验：[19/31/17 子类](../Research/NightUniform/TerminalWitness.py) 配 [SevenList](../Research/NightUniform/SevenList.json)，[13 子类](../Research/NightUniform/TerminalUnionWitness.py) 配 [SevenAllow13](../Research/NightUniform/SevenAllow13.json)。这些是整类的支持条件结论；规范分片通常还包含其它根共存的情形，故不直接增加闭合数。

进一步对已知分圆块的最大公因子和平方核逐一验证后，[显式六根对偶](../Research/NightUniform/TerminalSixWitness.py)、[未分解余因子对偶](../Research/NightUniform/TerminalAnonymousWitness.py)、[带至多一笔 Euler 折扣的对偶](../Research/NightUniform/ParityTerminalWitness.py)给出六个联合排除：在共同禁素集合 $\{3,5,7,11\}$ 上，再禁止 $\{13,17,19,31\}$ 的任意两项，均有严格的 $N>10^{2400}$ 下界。这里余因子只用整数整除和经过认证的大小、丰度及平方核界，**不把合数当作素数**。因此在共同四禁类中，四个较大的根至少出现三个。它限制一个完整根支持族，但不消灭该族的全部规范分片。对根 31 且已禁 19 的任务，禁止 3、5、13 三者共存于缺席集合已不可能；可把它分成“至少含3、5、13之一”三个可重叠但穷尽的子证书。[三路森林](../Research/NightLowRoute/Release/SixReplay.py)先重放所需终端引理，再验证三个子域，而不把三个子证书计为三个分片。

更强的统一结论可以直接省去 17、19、31 三个禁素数：**若 $\gcd(N,3\cdot5\cdot7\cdot11\cdot13)=1$，则 $\log_{10}N\ge2414.338356$**。所以目标区间内的假想反例至少被 3、5、7、11、13 中之一整除。证明先重验两个历史端局证书，重建 13,622 个选项、9,518 条蕴含（其中 238 条重新验素性和整除），再对 95 个彼此不交且不与显式底数重叠的未分解块核验试除界、匿名成本和最大可能丰度；有向整数对偶下界为 `112754367180120485945614959425350704`（按验证器的固定缩放），不依赖平方核猜测。命令：`python -I -S -B Research/NightUniform/RoughTerminalWitness.py Research/NightUniform/FiveAvoid.json`。这是对所有含根分片均可调用的**必要条件**，不能将某分片中只有一部分素因子支持被排除误作整个分片关闭。

更强的**四根必要条件**：若 $\gcd(N,3\cdot5\cdot7\cdot11)=1$，则 $\log_{10}N\ge2411.108934$。因此在目标范围内，3、5、7、11 中至少有一项整除 $N$，不再需要 13 才能保证命中。做法是把原终端模型的 114 个较大目标底数进一步拆为合法的精确指数与保守的高幂尾项；重验整除后，其中的因子和可迫使下一层显式底数或 287 个互素匿名块。粗块的完整素支持从通用尾移除，没有把匿名 Euler 另收一次。精确重放共 14,526 个变量、14,445 行、10,070 条边。[主验证器](../Research/NightUniform/SecondaryTerminalWitness.py)绑定[证书](../Research/NightUniform/FourAvoid.json)；[独立重建](../Research/NightFiveReview/TerminalAudit/Audit.py)不导入原模型和对偶程序，用不同的有向对数仍得到同一下舍结果。它不排除被这四个数之一整除的情况，也不凭此额外记一片。

上述机制还给出本夜更强的命题：**任一 $N\le 10^{2400}$ 的假想奇完全数，必被 3、5、7 之一整除。** 若三者全部不整除，[三根证书](../Research/NightUniform/ThreeAvoid.json)给出 $\log_{10}N\ge2406.575051$（向下舍入）。相对四根，此处允许同一底数的不同精确指数对应的匿名块有交集，因为真实整数最多取其中一个；不同底数同时激活的匿名块仍需互素。879 个非平方块中，419 个为 3 mod 4，必含某个奇重数且不是 Euler 的素因子，不可用 Euler 优惠免去补幂；另 460 个按至多一个总 Euler 槽作保守退款。[标准复验](../Research/NightUniform/ThreeHittingWitness.py)与[独立完整重建](../Research/NightFiveReview/ThreeTerminal/Independent.py)不共享原模型和对数计算，均核验所有 10,852 条边且得到同一下舍界。在固定根序下，这个结果可作为许多分片的严格前置（例如已禁 7 时需要 3 或 5），**不是**已排除含有这些素数的全部反例。

### 11 月 25 日增量

本轮在夜间快照之上排除 51 个实际指数，闭合 20 个规范分片。49 个证书沿用静态森林或分圆整除推广。已知强制素因子的每个孩子只在其指定父节点的真实几何和提供所需赋值时激活。根五的两个指数分别由单独证书闭合。对于 $(5,148)$，把强制素因子 $q=\sigma(5^{148})$ 的普通与 Euler 位置分开，普通侧用两套森林检查，Euler 侧逐一枚举尺寸允许的六个指数。对于 $(5,520)$，先用整数不等式排除内部 Euler 和外部的早期分支，再用有向取整的终端对偶覆盖其余外部一次幂分支。[证明包与复验](../Research/Nov25/Closeout.md#复验范围)。

## 4. 素性与重放

每个作为素数使用的因子先验证其整除关系及素性。小于 $2^{64}$ 的候选用确定性七底 Miller–Rabin。大因子的 ECPP 链逐层绑定当前整数 $n$，验证曲线判别式为单位，验证 $[s]P$ 在每个素因子剩余域中非零且 $[q][s]P=O$，其中子素数 $q>(n^{1/4}+1)^2$。若 $n$ 合数，最小素因子 $\ell\le\sqrt n$，Hasse 界与该阶为 $q$ 的点矛盾。链尾回到确定性范围。预算用尽或只有概率素性见证的指数继续开放。

| 批次或规则 | 复验入口 | 证明数据 |
| --- | --- | --- |
| 原根集互素类 | [TerminalCertificate.py](../Research/Session20261122/Python/TerminalCertificate.py) | [原根互素类证书](../Research/Session20261122/Certificates/TerminalOriginal.json.gz) |
| 历史含根基线 | [历史复验命令](#历史复验命令) | [Teichmüller](../Research/TeichmullerValuation/Audit2400.json)、[Gemini](../Research/TeichmullerValuation/GeminiBatchAudit2400.json) |
| 根 3 来源与供应，6 项及 3 片 | [CheckShards.py](../Research/GapSupply2400/CheckShards.py)、[Independent.py](../Research/GapSupply2400/Independent.py) | [扫描记录](../Research/GapSupply2400/LiftDeep.json) |
| 根 3，42 项来源与 87 项多层链，重合 26 项 | [IndependentEvening.py](../Research/EveningRoot3/IndependentEvening.py)、[Replay.py](../Research/ThreeChainNext/Replay.py) | [来源](../Research/EveningRoot3/BothAudit.json)、[链](../Research/ThreeChainNext/Certificates.json) |
| 根 5，81 项 | [CheckCertificate.py](../Research/RootFiveNext/CheckCertificate.py) | [证书](../Research/RootFiveNext/RootFiveCertificate.json) |
| 根 7、11、13、19、31，共 346 项 | [VerifyOrderSupply.py](../Research/OrderSupplyNext/VerifyOrderSupply.py)、[IndependentTree.py](../Research/EveningTree/IndependentTree.py) | [341 项](../Research/OrderSupplyNext/Accepted.json)，另五项 $(7,570),(11,318),(13,544),(13,634),(31,362)$ |
| 规范分片映射 | [VerifyFrontier.py](../Research/EveningMerge/VerifyFrontier.py) | [合并清单](../Research/EveningMerge/Audit.json) |

在仓库根运行 `python -B Research/EveningMerge/VerifyFrontier.py --workers 6` 可复验新增证书及并集，历史基线另按[历史复验命令](#历史复验命令)重放。从 2,027 个已闭合分片出发，第一批新增 3 个，第二批净排除 530 个实际指数并新增 162 个完整分片。

Euler 来源的分圆指数约简曾在 533 个根 3、5 实际指数上做区间复验，扩大了其中 76 项的覆盖。分支级推导及部分覆盖记录见[历史来源区间报告](https://github.com/stormwhip/PerfectNumbers/blob/ea08da38e38ab3309da4360ea2bb60ecb616a025/Documentation/ResearchReport2400.md)。

两批逐分支推导、发布命令及原始统计保存在 [PR #1 快照](https://github.com/stormwhip/PerfectNumbers/tree/4aad42d895d44782d69e28ed065ca4fda2401b1d/Research/GapSupply2400)和 [PR #2 快照](https://github.com/stormwhip/PerfectNumbers/tree/ea08da38e38ab3309da4360ea2bb60ecb616a025/Research)。[当前状态](CurrentStatus2400.md)与[下一步计划](NextPlan2400.md)使用同一份审计清单。

### 历史复验命令

在仓库根目录运行，夜间回执写到仓库外。

~~~sh
mkdir -p Build
python3 -S Research/Session20261122/Python/TerminalCertificate.py verify Research/Session20261122/Certificates/TerminalOriginal.json.gz
python3 Research/FermatRootValuation/IndependentCheck.py
python3 Research/IndicatorCapacity/IndicatorCapacityTests.py
python3 Research/IndicatorCapacity/AuditIndicatorCapacity2400.py --output Build/AuditSummary2400.json
cmp Research/IndicatorCapacity/Audit2400.json Build/AuditSummary2400.json
python3 Research/TeichmullerValuation/TeichmullerValuationTests.py
python3 Research/TeichmullerValuation/AuditTeichmullerValuation2400.py --output Build/AuditTeichmuller2400.json
cmp Research/TeichmullerValuation/Audit2400.json Build/AuditTeichmuller2400.json
python3 Research/TeichmullerValuation/AuditGeminiBatch2400.py --remaining Build/RemainingBeforeGapSupply2400.json
python3 Research/EveningMerge/VerifyFrontier.py --workers 6
python3 -B Research/NightMerge/ParallelReplay.py --workers 10 --fresh --receipts ../PerfectNumbersNightReceipts
python3 -I -S -B Research/Nov25/Ledger.py --workers 10 --check Research/Nov25/Delta.json
~~~

## 5. 11 月 25 日午间证明

本轮以 [PR #4 合并提交](https://github.com/stormwhip/PerfectNumbers/commit/6732a1a894817457a1bc1b88b7d214ac4d6c9872) 为基线，排除 267 个实际指数，闭合 202 个规范分片。该批逐根统计见[午间账本](../Research/Midday/Delta.json)，逐包复验见[午间证书](../Research/Midday/README.md)。

设 $N$ 为满足 $N\le 10^{2400}$ 的假想奇完全数。普通森林从经认证的 $\sigma(p^e)$ 素因子出发，按父节点真实指数激活子节点。对登记为可提升的普通森林，若 $e+1\mid f+1$，则 $\sigma(p^e)\mid\sigma(p^f)$，可在保留原剥离支撑及成本的前提下排除指数 $f$。前缀树、Euler 位置分割和支持分割逐个实际指数登记。

根 5 规范类要求 $5\mid N$ 且 $19,7,11,31,13,3$ 均不整除 $N$。整数对偶排除了该类最后 14 个实际指数。指数 6 与 48 同属一个分片，故本轮闭合 13 片，累计闭合该类全部 481 片。最弱证书 $(5,18)$ 给出向下取整界 $\log_{10}N\ge2406$。[根 5 证书](../Research/MiddayFive/README.md)

### 支持命中集

历史命中集 $\{3,5,7\}$ 与本轮的 $\{3,5,11\}$、$\{3,5,13\}$ 联合推出
$$
\gcd(N,15)=1\quad\Longrightarrow\quad 7\cdot 11\cdot 13\mid N.
$$
两条新证明利用前置命中集确定强制支持，再在各个补侧重建整数对偶。第二条的末支下界取整为 2400，严格不等式由未舍入的整数比较得到。分片仍按全部实际指数记账。[命中集推导](../Research/MiddayTerminal/Triple.md) · [第二条的完整依赖复验](../Research/MiddayTerminal/ReleaseThirteen.py)

根 5 的全部分片闭合后，若 $3,7$ 均不整除 $N$，历史命中集强迫 $5\mid N$，于是 $11,13,19,31$ 中至少有一个整除 $N$。根序中 17 位于 5 之后，允许 17 出现仍在根 5 类的覆盖范围内。

### 根 5 的多源整数对偶

1. 选取一组经认证的显式素数 `V`，包含所有小于阈值 `L` 的允许奇素数。每个底数最多选择一个指数选项：有限精确前缀、普通高幂尾，或合法的 Euler 高幂尾；实际已固定的根指数一定选择。目标是从这些选项和未知素数贡献构造一个**包含每个真实反例**的松弛模型。
2. 对每个选中的精确素幂 `r_i^f_i || N`，将几何和的奇部写为 `S_i = U_i ∏_{q∈V} q^{a_iq}`，其中 `gcd(U_i,∏V)=1`。不同 `i` 来自不同素幂，所以 `∏ S_i` 整除 `σ(N)` 的奇部 `N`。因此所有 `log U_i` 可以同时计入尺寸；**不需要各 `U_i` 两两互素**。对 `q∈V`，总流入 `∑a_iq` 不超过其实际指数。显式尾若使用下界 `h` 而实际为 `f>h`，可付 `(f−h)log q` 的剩余价。流入约束与“某一来源强迫目标指数至少为 k”的蕴含是两个必要不等式，不是把同一素幂乘两次。
3. 每个 `U_i` 全部素因子至少为 `L`，它的素支持可以免费获得至多 `⌊log_L U_i⌋ log(L/(L−1))` 的对数丰度。若不同 `U_i` 含同一素数，免费丰度可能重复，方向是放宽而非加强。尚未列入的素数既不在 `V`，又不在任何已计入的余块中：普通素数的指数至少二，故每个至少付 `2log L`，丰度至多 `log(L/(L−1))`。外部 Euler 素数单列一枚折扣，并与显式奇指数选项合并限制为至多一次。
4. 尺寸系数向下、丰度贡献上界向上。对 `Ax≤b` 与非负整数权重 `w`、固定分母 `W`，任一真实可行点满足 `W C·x ≥ −w·b + (WC+wA)·x`。同底数至多选一项，余项下界可按组取 `min(0,min_j reduced_j)`；无界余量列的约化成本必须非负。若重建的整数右端严格大于 `2400 W` 乘 `log(10)` 的上端，就排除了该反例。浮点求解只负责提议 `w`。第二套验证器用 Decimal 相邻可表示数包围对数，重新生成所有素幂、取整方向、行和稀疏对偶。两套实现对同一紧凑[证书](../Research/MiddayFive/Accepted.json.gz)给出一致的十四项结论。

### Euler 位置分割

For the canonical scenario, `7^700 || N` and `19 ∤ N`, set `A=(7^701−1)/6` and let `E` denote the unique Euler prime. The root itself is ordinary. Partition the problem into five pairwise disjoint cases, the four exact possibilities for `E` below and their complement. This is not the assumption that a forest contains the Euler prime: the last class includes **every prime outside the graph**.

| Euler 位置 | $\lfloor\log_{10}N\rfloor$ 下界 |
|---|---:|
| 表中四个素数以外 | 2400 |
| 11777 | 2404 |
| 194674901 | 2403 |
| 3680030201 | 2446 |
| 4751504889569509596346336866349490924895794713 | 2430 |

第一行的结论来自严格整数比较。该分支允许除表中四个素数外的任一合法 Euler 位置，也允许 Euler 素数位于已激活森林之外。其余四支分别固定表中的 $q$ 为 Euler 素数，删除其旧入边，将它升为独立强制根并从各外部余项中去净。若 $q\mid A$，以实际幂 $q^f$ 代替基线的 $q^{v_q(A)}$，其中 $f\ge v_q(A)$ 且 $f\equiv1\pmod4$。若 $q\nmid A$，最低重数为 1。对每支复核无环、可达性、素性、实际整除与单调裸幂尾界。五支穷尽 Euler 位置，故排除 $(7,700)$。

[Euler7x700 证书](../Research/Midday/Euler7x700.json.gz)经[单折扣递归](../Research/Midday/ModeCheck.py)和[独立位置计价](../Research/Midday/IndependentModes.py)复验。相同方法排除 $(7,172)$ 与 $(13,562)$，分别使用四支和十一支。三项均按精确指数登记。

### 强制素数的支持分割

**引理 3（支持二分）。** 对任一认证素数 $q$，若 $q\mid N$ 与 $q\nmid N$ 两支各有完整矛盾证书，则该实际指数被排除。

**证明。** 两支互斥且穷尽。在 $q\mid N$ 支，将 $q$ 提为独立根，删除旧入边，并从外部费用剥离其素支持，最低重数为 $\max(1,v_q(A))$。在 $q\nmid N$ 支，任何使 $q\mid\sigma(r^f)$ 的实际指数 $f$ 均不相容。两支各自验证全部合法 Euler 位置、精确指数选项及完整尾段。$\square$

实例为 $(11,682)$（$q=45894788532144820046483641$）和 $(7,112)$（$q=1187565393391461169$）。[复验入口](../Research/Midday/SupportCover.py)提供两套整数计价，二者共用森林结构检查。

### 两个完整实际指数的实例

* **低指数 `(31,10)`**：令 `q=150332843`，其素性和对 `σ(31^10)` 的整除均验算。先用缺 7 时的三根命中前提，继而穷尽 3、5 以及 13、17 的合法支持情况；四个子域共 283 个叶。只含 3 不含 5 的最后子域中，原先剩下 `v_q(N)=40,52`，再分发射因子 5659、107 及其后继，覆盖含尾在内的 204 个叶，无例外。它排除的是规范实际指数 10，并非所有含 31 的整数。[完整支持证明](../Research/MiddaySupport/README.md)
* **高指数 `(11,718)`**：对 `s=v_11(q+1)` 的全部 719 种可能，主、独立路线分别重建已知源、未知内部源和外部源。最后四个棘手窗里 `q | σ_4(r)` 强迫 `ord_q(r)=5`；在 `r²|C`、`r<q` 的分支检查模 `q` 的四个非平凡五次单位根。只有整域输出 `open=[]` 才获证；`(7,1018)` 的相同整域标准要求全 1,019 个 `s`。[赋值与二阶同余证明](../Research/MiddaySupply/DigitProof.md) · [全域回执](../Research/MiddaySupply/FullReceipt.json)

### 证书来源与去重

一份研究结果可能有多种证明。下表是**发布登记表实际选用**的来源；按不同 `(p,e)` 求并集。未注册的替代证明、条件命中集、局部区间及超时均不加分。分片与证明来源不是一一对应，故不把来源各自宣称的分片数相加。

|登记目录|覆盖的不同实际指数|
|---|---:|
|[Midday](../Research/Midday)|98|
|[MiddayDirected](../Research/MiddayDirected)|113|
|[MiddayFive](../Research/MiddayFive)|14|
|[MiddayForest](../Research/MiddayForest)|14|
|[MiddayGraph](../Research/MiddayGraph)|5|
|[MiddaySupport](../Research/MiddaySupport)|1|
|[MiddayThree](../Research/MiddayThree)|24|
|**不同键并集**|**267**|


按**证明类型**清点，普通森林覆盖 231 个不同 `(p,e)`，精确前缀树覆盖 5 个，专用证明覆盖 32 个；其中 `(13,80)` 同时在森林和前缀树中，因此是 **231 + 5 + 32 − 1 = 267**。森林内部也已去重：例如根 7 的指数 324、624 既有直接证书，也能分别从 64、124 的指标整除关系提升。特殊验证中的 14 个根五实际指数共用一个对偶包。`(7,1018)` 与 `(11,718)` 均有独立的全域赋值证明；前者在登记表中选择了体积较小的支持二分包，不重复计数。


### 晚间支持集合分割（条件结果）

记 $S_8=\{19,7,11,31,13,3,5,17\}$，$H=\{r\in S_8:r\mid N\}$。固定 $(p,e,H)$ 后，$S_8\setminus H$ 为禁素集合。八根之外的素因子仍可出现。

**引理 4（固定支持上的尺寸与丰度下界）。** 设 $X$ 为已固定实际素幂之积，$R=\operatorname{odd}(\sigma(X))$。取所有在 $X$ 外强制出现的显式素数，组成集合 $T$。对每个 $r\in T$，令 $f_r$ 为保守普通指数下界，$g_r$ 为可用的 Euler 指数下界。令 $R_0$ 为从 $R$ 中剥除 $X$ 及 $T$ 的全部素支持所得余项，则
$$
 I(N)\ge I(X)\prod_{r\in T}I(r^{f_r})
 \min\left(1,\min_r\frac{I(r^{g_r})}{I(r^{f_r})}\right),
$$
$$
 N\ge X R_0\prod_{r\in T}r^{f_r}
 \min\left(1,\min_r r^{g_r-f_r}\right).
$$

**证明。** 由 $R\mid N$，各底数的实际指数至少为相应的 $v_r(R)$。固定指数不足或 $R$ 含禁素数时即得矛盾。对显式底数，指数还须与正重数、分支尾下界及 Euler 同余相容。若 $r^{j+1}\equiv1\pmod{\ell(r-1)}$，则禁素数 $\ell$ 整除 $\sigma(r^j)$，故该指数可跳过。有限搜索无结果时采用只含最低重数和奇偶条件的下界。各乘积至多在一处改用 Euler 指数，对两项分别取最小折扣。若 $X$ 已含奇指数，或无可用的 $g_r$，折扣为 1。$R_0$ 与显式素幂支持互斥，且 $R_0\mid N$，故尺寸计价无重叠。$\square$

**命题 2（九项条件排除）。** 对[登记表](../Research/SupportSplit/Readme.md#条件排除证据)的九个 $(p,e,H)$，其对应子域为空。

**证明。** 对表中强制底数，枚举 $1\le v_r(N)\le8$ 的合法指数和尾段 $v_r(N)\ge9$。必要时细分第二个底数。逐叶用整数或有理数比较验证矛盾，所用充分条件为引理 4 的丰度下界严格大于 2，或尺寸下界严格大于 $B$。所有叶都覆盖后方排除该 $H$。[独立复验](../Research/SupportSplit/Verify.py)在 11,398 个组合中复现 4,833 个基础排除及九项新增排除。各实际指数均保留一个或多个开放支持。$\square$

**命题 3（根十九的禁素条件）。** 对任一奇完全数 $N$，若 $19^e\parallel N$ 且 $15\mid e+1$，则 $5\nmid N$。此命题独立于尺寸截止 $B$。

**证明。** $\sigma(19^{14})=3\cdot31\cdot127\cdot151\cdot211\cdot911\cdot2460181\mid N$。其中 $3,31,127,151,211,911$ 均为 $3\bmod4$ 的素数，故实际指数均为正偶数。令
$$
 K=I(19^{14})I(31^2)I(127^2)I(151^2)I(211^2)I(911^2).
$$
若 $5\mid N$，则按 $v_3(N)=2,4,\ge6$ 分三支。前两支分别由 $\sigma(3^2)=13$ 和 $\sigma(3^4)=11^2$ 强制 $13$ 和 $11$，第三支至少含 $3^6$。三个丰度下界分别为 $KI(3^2)I(5)I(13)$、$KI(3^4)I(5)I(11)$、$KI(3^6)I(5)$。有理数比较均严格大于 2。$\square$


### 历史候选审计（根 3，指数 1162；由本轮完整证书补齐）

设普通素数 $u$ 的实际偶指数为 $h$。当 $u\equiv1\pmod3$ 时，$v_3(h+1)\le h/2$，故净成本至少为 $h(\ln u-2\ln3)$；多个余块须按总重数计价，不能分别采用单次重数的平方补价。`P3_I00193` 的森林与 LP 余块存在共享因子，原候选未获数学验收。见[独立审计](../Research/P3I00193Review/Readme.md)。

## 参考资料

1. P. Ochem and M. Rao, “Odd perfect numbers are greater than $10^{1500}$”, Mathematics of Computation 81 (2012). [原文](../References/OchemRao2012.pdf)。
2. [午间发布审计](../Research/Midday/ReleaseAudit.md)，含固定提交、复验命令及隔离回执。

根 3 的五个高指数 E0/E1/E2 已有独立整数分支证明。令普通供给总量为 $U$，以 $K=10^8$ 及 277 个有限折让因子构造 $O\ge K^U/\prod_rD_r$；E1 穷尽 Euler 的赋值拆分，E2 取 $U\ge e/2$。外部来源降阶给出 $N>8\cdot3^eq^4/27$，从而在 $(e,s)=(1162,s\ge967)$ 或 $(1108,s\ge981)$ 的窗口有来源赋值为零。推导、整数证书与未完成的联合丰度条件见[续研](../Research/P3I00193Review/Progress.md)。该历史子批次的完整闭合增量为 0；当前 1162、1108 的结论分别见本文前部两条精确指数定理。
