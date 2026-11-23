# Odd Perfect Numbers Beyond \$10^{2400}\$ — 独立审计、零信任复现与深化推进报告 (`ResearchResult_v5.md`)

**日期：** 2026-11-23  
**最终定理目标：** 证明对所有奇完全数 \$N\$，恒有 \$N \> 10^{2400}\$，并构建独立可审计的有限计算证明。  
**全局状态：** `INCOMPLETE_FRONTIER`（九大外层类中 **2 类已无条件 `REPRODUCED_VERIFIED` 闭合**：\$\\mathcal{C}\_\\infty\$ 与 \$\\mathcal{C}\_8\$；3,072 个顶层分片中 **1,679 个达到 `REPRODUCED_VERIFIED`（54.65%）**，较 1,447 基线净增 **\+232 项**、较附录 A 报告净增 **\+30 项**；剩余开放分片降至 **1,393 个 `OPEN`**，其中仅 1 项为附录 A 的 `REPORTED_ONLY`；全量零信任统一审计 v5 耗时 **6.208 s** 一次通过，8 / 8 项强制对抗伪证测试全部拒绝）。

---

## 1\. 本轮实际执行记录（环境、时间与可重放命令）

### 1.1 实测硬件与软件环境

- **硬件**：Apple A18 Pro（6 物理核），8 GB 内存，macOS  
- **软件**：Python 3.14.7 (`/opt/homebrew/bin/python3`)，Apple `clang++` (`-O3 -std=c++17`)  
- **零外部 Python 包依赖**：纯标准库自主实现 **60 位十进制精度向外舍入纯整数区间算术**（`exact_iv.py`，`SCALE=10**60`，零浮点）、递归确定性试除 / Pratt 素性证书系统、C++17 平滑拉格朗日对偶优化器（`lp_dual_solver.cpp`）、C++17 128 位模乘分圆素因子查找器（`cyclotomic_finder.cpp`）、C++17 **128 位 Brent Pollard-Rho 分解器**（`rho128.cpp`，秒级分解高指数 65–125 位 \$\\sigma(p^e)\$）及全套独立零信任验证器。

### 1.2 端到端实测耗时与可重放命令

```sh
# 1. 附录 B 基线复现（实验 B，2.18 s）
python3 StandaloneReference2400.py --emit

# 2. 编译三个 C++17 核心加速工具并自测 60 位纯整数区间与 Pratt 验证器
clang++ -O3 -std=c++17 lp_dual_solver.cpp -o lp_dual_solver
clang++ -O3 -std=c++17 cyclotomic_finder.cpp -o cyclotomic_finder
clang++ -O3 -std=c++17 rho128.cpp -o rho128
python3 exact_iv.py

# 3. 全局 LP (C_inf, C_8)、实验 C (Root3_No5)、实验 D (Root5 可扩展性) 与实验 F (析取分裂)
python3 -u run_milestone2.py

# 4. 根 5 Ultra V3 LP (p_small=300, e<=60 + rho128 p<=1200 + 2/3-步链，32.68 s)
python3 -u root5_ultra_v3.py

# 5. 6 核并行 C++ 分圆筛 + 规则 VIII DAG (31 份) + 根 3 Ultra V3 LP + 全量零信任审计 v5 (6.208 s)
python3 -u scale_closures.py
python3 -u dag_boost_v3.py
python3 -u dag_parallel_v4.py
python3 -u final_push_v5.py
```

---

## 2\. 数学审计发现（审计 A–F 与实验 A）

| 审计项 | 审计对象 | 判定结论 | 严格数学依据与修复说明 |
| :---- | :---- | :---- | :---- |
| **审计 A** | 全局 LP（\$\\mathcal{C}\_\\infty, \\mathcal{C}\_8\$）涵盖性与弱对偶 | **有效（已独立重建并刷新记录）** | 逐项核验显式指数、高指数尾 `Allowed` 保守下界、\$q^k\\mid\\sigma(p^e)\$ 对目标素数高指数尾涵盖、额外大素数 Pratt 认证、连续偶尾斜率单调性 \$g(x)=\\frac{\\ln x}{\\ln(x/(x-1))}\$ 与 60 位纯整数弱对偶验证。修复高指数漏扫与额外素数排序后，\$\\mathcal{C}\_\\infty\$ 与 \$\\mathcal{C}\_8\$ 均创历史新高。 |
| **审计 B** | 规则 VI 条件化 LP 的 \$A^\*\$ 分解与强制素数 | **有效（强制 \$m\>p\$ 且逐项验 \$r\\nmid A\$）** | \$N=p^e A^\* Q\_{\\text{other}}\$ 两两互素，\$m=d+1\>p\$ 为奇素数时 \$f(A^\*)\<\\prod\_{j=1}^t\\frac{2mj+1}{2mj}=U\_A\$ 对任意高指数严格成立；对每条活跃蕴含目标 \$r\$ 显式验证 \$(r\<2m+1)\\lor(2m\\nmid(r-1))\\lor(p^m\\not\\equiv 1\\pmod r)\$ 确保 \$r\\nmid A\$。 |
| **审计 C** | 规则 VII 提升乘积 \$M\_{\\text{lift}}\\mid(A^\*/A)\$ | **原文整除宣称无效（`INVALIDATED`）；修复为数值下界后有效** | **实验 A 反例**：取 \$q\_1=5, q\_2=13\$，\$a\_1=a\_2=1, e\_0=2, e\_1=1\$，候选提升乘积为 \$M\_0=65, M\_1=13, M\_2=5\$；\$\\min(65,13,5)=5\$ 但 \$5\\nmid 13\$。**修复**：改为严格数值下界 \$A^*/A \\ge M\_{\\text{lift}}\$，仅用于 \$\\ln(p^e A^*)\\ge \\ln(P\\cdot M\_{\\text{lift}})\$，严禁用于下游整除或 `lcm`。 |
| **审计 D** | 规则 VIII LCM 状态与指数覆盖 | **有效（纯整数循环与精确 `math.lcm`）** | \$E\_{\\max}=v\_q(M\_{\\text{lcm}})+\\lfloor\\log\_q(B/M\_{\\text{lcm}})\\rfloor\$ 采用纯整数除法循环计算，零浮点；`SPLIT_EXPONENT` 逐项核对全部合法 Euler 指数无遗漏。 |
| **审计 E** | 附录 A 建议将 \$\\mathcal{C}\_8\$ LP 复用于“根 3 禁用 5” | **无效（`INVALIDATED`，实验 C 证伪）** | \$\\mathcal{C}*8\$ 含必现 \$17\\mid N\$ 且禁用 \$3\$；根 3 禁用 5 含必现 \$3\\mid N\$（丰度达 \$3/2\$）。实验 C 独立 60 位验证真实下界仅为 \$\\log*{10} N \\ge 217.82\$（绝非 2443）。 |
| **审计 F** | 分类统计与证书绑定 | **已严格重分并零信任审计** | 严格区分 `REPRODUCED_VERIFIED`（1,679）、`REPORTED_ONLY`（1）、`INVALIDATED`（2 项历史命题）、`OPEN`（1,393），互斥零重叠。 |

---

## 3\. 新数学定理、实验突破与完整证明

### 3.1 定理 1（终局互素类 \$\\mathcal{C}\_\\infty\$ 刷新记录 — `REPRODUCED_VERIFIED`）

对 \$S={3,5,7,11,13,17,19,31}\$，经 60 位纯整数区间独立复核 `TerminalCoprimeCertificate.json`（\$P\_{\\max}=4000\$，1,212 蕴含，2,636 Pratt，验证 0.938 s）： \$\$\\ln N \\ge 9659.544420544 \> 5526.204223185709 \\implies \\log\_{10} N \\ge \\mathbf{4195.086839541} \> 2400\\quad (+1795.09\\text{ 位余量}).\$\$

### 3.2 定理 2（根 17 整类 \$\\mathcal{C}\_8\$ 刷新记录 — `REPRODUCED_VERIFIED`，闭合全部 125 项剩余分片）

对 \$F\_{17}={3,5,7,11,13,19,31}\$，经 60 位纯整数区间独立复核 `ClassC8Certificate.json`（\$P\_{\\max}=6000\$，1,291 蕴含，2,690 Pratt，验证 1.582 s）： \$\$\\ln N \\ge 6761.641633778 \> 5526.204223185709 \\implies \\log\_{10} N \\ge \\mathbf{2936.543650157} \> 2400\\quad (+536.54\\text{ 位余量}).\$\$ 根 17 达到 **297 / 297 \= 100%** 全闭合。

### 3.3 实验 C（根 3 禁用 5 专用 LP）与根 3 Ultra V3 LP（`REPRODUCED_VERIFIED`）

- `Root3No5Certificate.json`（`mandatory=[3]`，\$F={5,7,11,13,19,31}\$，\$P\_{\\max}=6000\$）：\$\\log\_{10} N \\ge \\mathbf{217.821703609}\$（`exceeds_2400=False`，证伪 \$\\mathcal{C}*8\$ 复用）；`Root3No5QotherCertificate.json` 在 \$\\Delta=\\ln(4/3)\$ 处得 \$\\log*{10} Q\_{\\text{other}} \\ge \\mathbf{207.3250}\$。  
- **`Root3_Ultra_V3Certificate.json`**（\$p\_{\\text{small}}=250, e\\le 50\$ \+ `rho128` \+ 2-步链，1,778 蕴含，3,557 Pratt，验证 1.922 s）：将根 3 基础下界从附录 A 的 `16.03` 推升至 **`28.5299` 位（\$+12.50\$ 位）**，将 `P3_I00368` 下界强化至 `2436.5350`。

### 3.4 实验 D 与 `rho128` 双层截断突破（根 5 突破 865 位、闭合超 300 项 — `REPRODUCED_VERIFIED`）

本轮通过诊断定位了小素数逃逸至 `even_tail` 及 65–125 位高指数 \$\\Phi\_m(p)\$（如 \$p=37,41,67,71,79,83,97,103,107,109\$）无 \$\\sigma\$-惩罚的问题，利用自研 C++17 `rho128` 批量分解全部 \$p\\le 1200\$ 的 65–125 位 \$\\sigma(p^e)\$ 及顶部 1,000 个 2-步额外素数，推动根 5 下界五级跳升：

| 根 5 LP 证书演进 | \$P\_{\\max}\$ | 小素数 \$e\_{\\text{ev}}\$ | 增强手段 | 基础 \$\\log\_{10} Q\_{\\text{other}}\$ 下界 | 规则 VI 闭合数 | 活跃蕴含 | Pratt 证书 | 验证耗时 |
| :---- | ----: | ----: | :---- | ----: | ----: | ----: | ----: | ----: |
| 附录 A 基线（`REPORTED_ONLY`） | 6,000 | 18 | 1-步 | `657.13` | 53 | 310 | — | — |
| `Root5_P6000`–`P15000` | 6k–15k | 18 | 全显式指数 1-步 | `716.1484` | 59 | 1,334–1,607 | 2,686–2,915 | 1.68–3.99 s |
| `Root5_P10000_2step` | 10,000 | 18 | \+ 2-步链 | `761.7555` | 63 | 1,577 | 2,964 | 2.749 s |
| `Root5_Ultra_E60` | 6,000 | 60 (\$p\\le 200\$) | \+ 合数代数传播 \+ 分圆筛 | `802.9232` | 67 | 1,581 | 3,060 | 2.464 s |
| `Root5_Ultra_Rho128` | 6,000 | 60 (\$p\\le 200\$) | \+ C++ `rho128` (\$p\\le 250\$) | `845.5642` | 70 | 1,860 | 3,656 | 2.566 s |
| **`Root5_Ultra_V3`（最新）** | 6,000 | **60 (\$p\\le 300\$)** | **\+ C++ `rho128` (\$p\\le 1200\$) \+ 深度 2-步** | **`865.2271`** | **72** | **2,587** | **5,440** | **3.254 s** |

- 仅靠 `Root5_Ultra_V3` 的规则 VI 即连续闭合 **72 项**（`P5_I00185`–`P5_I00256`，较附录 A 的 53 项净增 **\+19 项**！）；叠加修复版规则 VII（`max_k=4,000,000`）再闭合 **2 项**（`P5_I00180` 提升 54 位、`P5_I00182` 提升 46 位），根 5 累计闭合达 **301 / 481**（较附录 A \+18 项）！

### 3.5 定理 3（实验 F 新剪枝规则：析取素数分裂对偶界 — Disjunctive Prime-Split LP Dual Bound）

因 \$17-1=2^4\$ 无奇素因子，对一切奇素数 \$m\>5\$ 恒有 \$17\\nmid\\Phi\_m(5)\$，故任一根 5 开放分片候选必满足 \$17\\nmid N\$ 或 \$17\\mid Q\_{\\text{other}}\$，严格有 \$\\ln Q\_{\\text{other}}\\ge\\min(L\_{\\text{out}}(\\Delta), L\_{\\text{in}}(\\Delta))\$。其中 \$17\\nmid N\$ 分支 `Root5No17Certificate.json` 已 60 位区间验证达到 **`1100.4484` 位**（单支覆盖 **96** 项）。同理，本轮还实现并验证了基于 \$5\\nmid\\Phi\_m(3)\$ 的根 3 `SPLIT_PRESENCE(5)` 路障分裂框架（`root3_presence5_dags.py`），在 \$5\\nmid N\$ 分支用 `Root3No5QotherCertificate.json`（207.33 位）单叶闭合，在 \$5\\mid N\$ 分支穷尽 \$5^e\$（其中 \$e=2,4,5,8,9\$ 均由 \$F\_3\$ 立即排除），发现瓶颈位于 \$5^1\\parallel N\$ 分支需结合更深层小素数路障分裂。

---

## 4\. 独立可复现核心源码（新增 `rho128.cpp` 全文）

*(前期 `exact_iv.py`、`cyclotomic_finder.cpp`、`lp_dual_solver.cpp` 与附录 B `StandaloneReference2400.py` 保持完全兼容；以下附上本轮推动根 5 与根 3 突破的 C++17 128 位 Brent Pollard-Rho 核心源码 `rho128.cpp`。)*

```c
// Fast C++17 __uint128_t Brent's Pollard-Rho Factorizer (up to 125-bit integers).
// Used ONLY for candidate factor discovery; all primes are certified by Pratt/trial in Python.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using u64 = uint64_t; using u128 = unsigned __int128;

u128 parse_u128(const std::string& s) {
    u128 v = 0; for (char c : s) if (c >= '0' && c <= '9') v = v * 10 + (c - '0'); return v;
}
std::string to_str(u128 v) {
    if (v == 0) return "0";
    std::string s; while (v > 0) { s.push_back('0' + (int)(v % 10)); v /= 10; }
    std::reverse(s.begin(), s.end()); return s;
}
u128 mul_mod(u128 a, u128 b, u128 m) {
    u128 res = 0; a %= m;
    while (b > 0) { if (b & 1) { res += a; if (res >= m) res -= m; } a <<= 1; if (a >= m) a -= m; b >>= 1; }
    return res;
}
u128 pow_mod(u128 a, u128 e, u128 m) {
    u128 r = 1; a %= m;
    while (e > 0) { if (e & 1) r = mul_mod(r, a, m); a = mul_mod(a, a, m); e >>= 1; }
    return r;
}
u128 gcd128(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }
bool is_prime128(u128 n) {
    if (n < 2) return false;
    static const u64 small[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (u64 p : small) { if (n == p) return true; if (n % p == 0) return false; }
    u128 d = n - 1; int s = 0; while ((d & 1) == 0) { d >>= 1; ++s; }
    for (u64 a : small) {
        if ((u128)a >= n) continue;
        u128 x = pow_mod(a, d, n); if (x == 1 || x == n - 1) continue;
        bool comp = true;
        for (int r = 1; r < s; ++r) { x = mul_mod(x, x, n); if (x == n - 1) { comp = false; break; } }
        if (comp) return false;
    }
    return true;
}
u128 brent_rho(u128 n, int max_steps = 40000) {
    if (n % 2 == 0) return 2;
    for (u64 c = 1; c <= 12; ++c) {
        u128 y = 2, r = 1, q = 1, g = 1, ys = 2, x = 2; int steps = 0;
        while (g == 1 && steps < max_steps) {
            x = y; for (u128 i = 0; i < r; ++i) y = (mul_mod(y, y, n) + c) % n;
            u128 k = 0;
            while (k < r && g == 1 && steps < max_steps) {
                ys = y; u128 lim = std::min((u128)128, r - k);
                for (u128 i = 0; i < lim; ++i) {
                    y = (mul_mod(y, y, n) + c) % n;
                    u128 diff = (x > y) ? (x - y) : (y - x); q = mul_mod(q, diff, n);
                }
                g = gcd128(q, n); k += lim; steps += (int)lim;
            }
            r <<= 1;
        }
        if (g == n) {
            do { ys = (mul_mod(ys, ys, n) + c) % n; g = gcd128((x > ys) ? (x - ys) : (ys - x), n); } while (g == 1);
        }
        if (g > 1 && g < n) return g;
    }
    return n;
}
void factor_rec(u128 n, std::vector<u128>& out) {
    if (n <= 1) return;
    if (is_prime128(n)) { out.push_back(n); return; }
    u128 d = brent_rho(n, 25000); if (d == n) return;
    factor_rec(d, out); factor_rec(n / d, out);
}
int main() {
    std::ios::sync_with_stdio(false); std::cin.tie(nullptr);
    std::string line;
    while (std::cin >> line) {
        u128 n = parse_u128(line); std::vector<u128> fac;
        static const u64 sm[] = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97};
        for (u64 p : sm) while (n % p == 0) { fac.push_back(p); n /= p; }
        if (n > 1) factor_rec(n, fac);
        std::sort(fac.begin(), fac.end()); fac.erase(std::unique(fac.begin(), fac.end()), fac.end());
        std::cout << fac.size(); for (u128 x : fac) std::cout << " " << to_str(x); std::cout << "\n";
    }
}
```

---

## 5\. 输出证书、稳定 SHA-256 与 8 / 8 对抗拒绝验证结果

| 产物 | 规模 | 严格 60 位区间下界 / 覆盖结论 | 规范字节串 SHA-256 |
| :---- | :---- | :---- | :---- |
| `RootManifest.json` | 3,072 条 | 全 8 根指数穷尽覆盖 | `7f26dc5021f891e5dfbb8cb79aaa16eb345e3f80c0152054e369d84b0a5bef8b` |
| `OpenManifest.json`（基线） | 1,625 条 | 1,447 基线叶 \+ 734,381 奇商 | `72187f9c4e3ff01d905394a0bd09fced28268119af18d15cfff35954ece66c6e` |
| **`OpenManifest_v5.json`（最新）** | **1,393 条** | **1,679 项 `REPRODUCED_VERIFIED` 闭合** | `84b3e6bf66b16227cb3576c58a52199cfafdedbe45f8b09856a8c0c9f008ddd5` |
| `TerminalCoprimeCertificate.json` | 1,212 蕴含, 2,636 Pratt | \$\\log\_{10} N \\ge \\mathbf{4195.086839541} \> 2400\$ | `2ad9db90c903c0cd831338e01dfb8e147d690899e68a2a9faea6aab7ed0c0cd0` |
| `ClassC8Certificate.json` | 1,291 蕴含, 2,690 Pratt | \$\\log\_{10} N \\ge \\mathbf{2936.543650157} \> 2400\$ | `189eaa6c96b135d71b2a13a831623f67d013229037821de248ad76f15d8f0195` |
| **`Root5_Ultra_V3Certificate.json`** | 2,587 蕴含, 5,440 Pratt | \$\\log\_{10} Q \\ge \\mathbf{865.2271}\$（闭合 72 项 VI） | `946888f54b45149c32e8e9df67d9fa59d71e5d3c98faf094b0b9cf2eafd19bfd` |
| **`Root3_Ultra_V3Certificate.json`** | 1,778 蕴含, 3,557 Pratt | \$\\log\_{10} Q \\ge \\mathbf{28.5299}\$（闭合 1 项 VI） | `36b76277e81dd520723f2aa143b57c9615f8a6830abbaf2a732ecdc005258f6a` |
| `Root3No5Certificate.json`（实验 C） | 1,341 蕴含, 2,620 Pratt | \$\\log\_{10} N \\ge \\mathbf{217.821703609}\$（证伪复用） | `c907fbdf3a99909e41b9d7e6bccca7fbcd742b78f09d5e282427e4b3afbfbf01` |
| `Root5No17Certificate.json`（实验 F） | 1,547 蕴含, 2,952 Pratt | \$\\log\_{10} Q \\ge \\mathbf{1100.4484}\$（\$17\\nmid N\$ 分支） | `b7b2cf997fb4b4937e51cb1553565e495405f9d308306cd205077647a6c06326` |

- **八项强制对抗伪证拒绝测试**：(i) 删禁用根 31、(ii) 伪造 Pratt \$g=1\$、(iii) 虚构 \$\\sigma\$ 幂次 \$k+5\$、(iv) 负对偶乘子 \$\\lambda\_0\<0\$、(v) 删 `SPLIT_EXPONENT` 子边、(vi) 分裂未强制素数 \$q=101\$、(vii) 开放任务虚构尺寸超界、(viii) \$\\min(13,5)=5\$ 伪称公因子/LCM —— **8 / 8 全部显式拒绝**。

---

## 6\. 逐根最新严格统计与全部新增闭合明细

### 6.1 逐根状态矩阵（严格零信任 `REPRODUCED_VERIFIED` 计数）

| 根 \$p\$ | 总分片 | 基线 I–V | \+\$\\mathcal{C}\_8\$ 整类 | \+规则 VI | \+修复版规则 VII | \+规则 VIII DAG | 累计 `REPRODUCED_VERIFIED` | 剩余 `OPEN` | 附录 A `REPORTED_ONLY` |
| ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: |
| 19 | 287 | 130 | 0 | 0 | 0 | 3 | **133** | 154 | 0 |
| 7 | 412 | 191 | 0 | 0 | 0 | **6** (+4 新) | **197** | 215 | 0 |
| 11 | 341 | 154 | 0 | 0 | 0 | **5** (+3 新) | **159** | 182 | 0 |
| 31 | 253 | 116 | 0 | 0 | 0 | **2** (+1 新) | **118** | 135 | 0 |
| 13 | 325 | 146 | 0 | 0 | 0 | **7** (+3 新) | **153** | 172 | 1 (`P13_I00165`) |
| 3 | 676 | 311 | 0 | 1 | 1 | **8** (+2 新) | **321** | 355 | 0 |
| 5 | 481 | 227 | 0 | **72** (+19 新) | **2** | 0 | **301** | **180** | 0 |
| 17 | 297 | 172 | **125** | 0 | 0 | 0 | **297 (100%)** | **0** | 0 |
| **合计** | **3,072** | **1,447** | **125** | **73** | **3** | **31** | **1,679 (54.65%)** | **1,393** | **1** |

### 6.2 修复版规则 VII 闭合明细（3 项，数值下界 \$A^\*/A \\ge M\_{\\text{lift}}\$ \+ Pratt 认证）

- `P5_I00180`（\$p=5, d=1086\$，全新闭合）：提升素数 \$q\\in{4349, 12815731}\$，\$M\_{\\text{lift}}\$ 达 **54 位**，严格下界 \$\\log\_{10} N \\ge \\mathbf{2423.1843} \> 2400\$；  
- `P5_I00182`（\$p=5, d=1092\$，全新闭合）：提升素数 \$q=1202715341\$，\$M\_{\\text{lift}}\$ 达 **46 位**，严格下界 \$\\log\_{10} N \\ge \\mathbf{2423.3089} \> 2400\$；  
- `P3_I00368`（\$p=3, d=2476\$，复现强化）：提升素数 \$q\\in{34679, 980893, 76217291}\$，\$M\_{\\text{lift}}\$ 达 **47 位**，严格下界 \$\\log\_{10} N \\ge \\mathbf{2436.5350} \> 2400\$。

### 6.3 31 份零信任核验规则 VIII DAG 汇总（共 8,997 节点：2,347 分裂、6,650 叶、8 个 LP 尾叶）

- **复现附录 A（18 / 19 项）**：`P19_I00153, P19_I00154, P19_I00156, P7_I00221, P7_I00222, P11_I00186, P11_I00187, P31_I00137, P13_I00169, P13_I00173, P13_I00174, P13_I00177, P3_I00352, P3_I00354, P3_I00359, P3_I00361, P3_I00362, P3_I00365`。  
- **本轮全新零信任闭合（13 项）**：`P7_I00208`（1,090 节点）、`P7_I00215`（949 节点）、`P7_I00217`（582 节点）、`P7_I00218`（80 节点）、`P11_I00173`（783 节点）、`P11_I00174`（863 节点）、`P11_I00184`（74 节点）、`P31_I00129`（2,072 节点）、`P13_I00161`（239 节点）、`P13_I00164`（130 节点）、`P13_I00172`（7 节点）、`P3_I00329`（1,341 节点）、`P3_I00360`（10 节点）。

---

## 7\. 失败日志、未证命题与精确停止原因

1. **未复现的附录 A 单项**：仅 `P13_I00165`（\$p=13, d=982\$）保留在 1,393 个 `OPEN` 中（标为 `REPORTED_ONLY`）。  
2. **`SPLIT_PRESENCE(5)` 在根 3 的实测诊断**：17 个 \$\\log\_{10} R \< 208\$ 的根 3 分片上，\$5\\nmid N\$ 分支均单叶闭合，但 \$5^1\\parallel N\$ 分支因 \$\\sigma(5)=6\$ 未引入新素数而无法仅靠单层 \$\\Phi\_m(3)\$ 因子闭合，需结合后续小素数 Roadblock 循环分裂。  
3. **72 小时端到端实测**：`NOT_MEASURED`（尚余 1,393 个开放顶层分片）。

---

## 8\. 针对剩余 1,393 个开放分片的下一步独立任务书

1. **继续挖掘根 5（剩余 180 项）**：将 `rho128` 结合 **ECM / SIQS** 覆盖 125–160 位 \$\\sigma(p^e)\$（针对 \$p\\le 500\$ 的高指数选项）并引入 3-步 \$\\sigma\$-蕴含，冲击 920–1000 位基础下界；同时对 \$17\\mid Q\_{\\text{other}}\$ 实施 \$17\$-指数析取分裂。  
2. **C++17 \+ GMP 多线程 Roadblock \+ 动态状态 LP**：针对剩余 1,393 项中大预算低指数分片（如 `P19_I00000/I00035/I00100` 及根 3 的 \$5^1\\parallel N\$ 支路），构建带严格无穷尾证书的 Roadblock 新素数循环分裂与原子断点账本，随后开展 72 小时端到端全量实测。