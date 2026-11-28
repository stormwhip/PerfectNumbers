# 独立离线验证与回归测试报告（Validation.md）

## 1. 冷启动隔离验证记录

| 项目 | 实际记录值 |
|---|---|
| 验证命令 | `python3 -I -S -B -X int_max_str_digits=0 Verify.py` |
| 负向回归命令 | `python3 -I -S -B -X int_max_str_digits=0 Verify.py --run-negative-tests` |
| Python 版本 | `Python 3.11.2`（隔离模式 `-I -S -B`，纯标准库，零外部依赖、零网络访问） |
| 主验证退出码 | `0` |
| 负向测试退出码 | `0`（11/11 项篡改全部被拒绝） |
| 精确算术校验项数 | `40,943`（全部为精确 `int` / `Fraction` 比较，无 `assert`） |
| 递归素性认证数量 | `57` 个素数（Pratt 原根分解证书 + 12 基确定性 Miller–Rabin） |
| 证书文件 | `Certificates.json`（21,523 字节） |
| 证书 SHA-256 | `ef8ade9bd3fbce68c80ccc66f33041cc32313f7dd29810529a9201ce5f055bc8` |
| 总运行耗时 | `9.785s` |

## 2. 主验证输出实录

```text
[PASS] Certified 57 primes recursively (Pratt + deterministic MR12).
[PASS] Verified all 8 baseline Section 3 domain counts & strict tails.
[PASS] H_h85            -> CLOSED (exc_bases=1, log10_lb=2401.83 > 2400)
[PASS] H_h108           -> CLOSED (windows=108, inner_div_checked=38, exc_bases=1)
[PASS] H_h102           -> CLOSED (windows=102, inner_div_checked=50, exc_bases=1)
[PASS] G_h66            -> CLOSED (windows=66, QR outer-Euler for i>=1, exc_bases=1)
[PASS] B_f1_g58         -> CLOSED (exc_bases=3, w=19/10, log10_lb=2423.53 > 2400)
[PASS] B_f1_g16_j42     -> CLOSED (exc_bases=3, w=19/10, log10_lb=2493.52 > 2400)
[PASS] B_f1_g16_j40     -> CLOSED (exc_bases=3, w=19/10, log10_lb=2420.56 > 2400)
[PASS] E_t1_split_1109  -> PARTIAL_CLOSED (136/138 closed, tail=555, OPEN=[2, 4], U19_exc=4, U1109=1)

ALL VERIFICATIONS SUCCEEDED.
Certificate SHA-256 : ef8ade9bd3fbce68c80ccc66f33041cc32313f7dd29810529a9201ce5f055bc8
Arithmetic checks   : 40943
Elapsed time        : 9.785s
```

## 3. 负向回归测试实录（11/11 通过）

以下 11 项负向测试逐一对应交接手册第 7 节要求，验证 `Verify.py` 对任意证书篡改或数学违规均严格抛出 `VerificationError` 拒绝：

1. 删除分支真实子值（遗漏 `E_t1` 的 `h=4`）→ **REJECTED**
2. 伪素数标签（将合数 `91 = 7 * 13` 充当素数）→ **REJECTED**
3. 精确指数退化/入度溢出（$v_3(S) = 3 > v_3(X) = 2$）→ **REJECTED**
4. 允许两个 Euler 位置同时存在（`5^1, 13^1`）→ **REJECTED**
5. Euler 未锁定时忽略合法平方基（`25 = 5^2`）→ **REJECTED**
6. 漏掉第二个同余代表（阶-3 同余根数量检查）→ **REJECTED**
7. 篡改需求/未验证块假设（`H_h108` 需求篡改）→ **REJECTED**
8. 将 $N = B$ 误判为溢出（严格边界 `> B` 检查）→ **REJECTED**
9. 重复计费/破坏 $D$ 分块互素分解（`small_coprime_block` 篡改）→ **REJECTED**
10. 使用非规范禁素（对根 `7` 误加其后的 `11`）→ **REJECTED**
11. 将 `timeout` / `null` 视作 `CLOSED` → **REJECTED**

## 4. 八个精确指数最终结果汇总表

| 键 | 剩余基线前置条件 | 新闭合范围 | 仍开放范围 | 独立验证状态 | 证书 SHA-256 |
|---|---|---|---|---|---|
| `(31, 268)` | 基线已闭 75/76（余 `3229^102`） | 无 | A1 `[(31,268),(3229,102)]` | `OPEN` | `ef8ade9bd3fbce68...` |
| `(19, 222)` | 基线已闭 50/53 及既有子分支（余 18 个二级前缀） | **闭合 1 个完整二级前缀** `f=1,g=58` 及 **2 个三级前缀** `f=1,g=16,j=42,40` | 余 17 个二级前缀（其中 `f=1,g=16` 减至 7 个三级值） | `VERIFIED_CONDITIONAL`（退出码 `0`） | `ef8ade9bd3fbce68...` |
| `(7, 48)` | 基线已闭 27/31 | 无 | $v_t \in \{2, 4, 8, 10\}$ | `OPEN` | `ef8ade9bd3fbce68...` |
| `(3, 12)` | 基线已闭 98/100 及既有子分支 | 无 | D1, D2, D3 | `OPEN` | `ef8ade9bd3fbce68...` |
| `(19, 276)` | 基线已闭 64/70 | `t^1` 按 `1109` 分支 **闭合 136/138**（全部 $h \ge 6$，尾界 555） | `t^1` 中 `1109^2, 1109^4`；及 $v_t \in \{2, 8, 16, 18, 28\}$ | `VERIFIED_CONDITIONAL`（退出码 `0`） | `ef8ade9bd3fbce68...` |
| `(3, 6)` | 基线已闭 179/182 及既有子分支 | 无 | F1a/b/c, F2, F3 | `OPEN` | `ef8ade9bd3fbce68...` |
| `(7, 18)` | 基线已闭 30/44 | **闭合 1 个完整一级分支** `v_t = 66` | 余 13 个一级值 `{2,4,6,8,12,22,28,30,36,40,42,46,58}` | `VERIFIED_CONDITIONAL`（退出码 `0`） | `ef8ade9bd3fbce68...` |
| `(7, 16)` | 基线已闭 44/91 | **闭合 3 个完整一级分支** `v_t = 85, 102, 108` | 余 44 个一级值（原 47 个） | `VERIFIED_CONDITIONAL`（退出码 `0`） | `ef8ade9bd3fbce68...` |
