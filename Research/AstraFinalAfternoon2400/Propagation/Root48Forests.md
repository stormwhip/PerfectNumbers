# 根 `(7,48)` 的进一步二级森林与 `3∤N` 分支

规范假设：N 为奇完全数、`N≤10^2400`、`19∤N`，且 `v_7(N)=48`。`t=6106505825833677713` 为由根强迫的素数。这里只涉及 t 的精确首赋值 **2** 或 **10**，且不关闭任何完整首值；t⁴/t⁸ 由根七队另行核验。

## 严格森林——新增互斥精确纤维

| 包 | 首 t 赋值 | 已闭普通锚赋值 | ECPP | SHA-256 |
|---|---:|---|---:|---|
| [orbit48sq](Reserved438x12-orbit48sq.json.gz) | 2 | `32,34,…,72` | 1299 | `6e15628e47f40b77b9be338808ea7de296bd441b8b694d028e0bccd382d9c437` |
| [orbit48sqmid](Reserved438x12-orbit48sqmid.json.gz) | 2 | `14,20,24,26,28,30` | 1180 | `14d863e14df2f448059cf3e13b37b38f6bd885a145aa8edd852e15b1d1a460ce` |
| [orbit48](Reserved438x12-orbit48.json.gz) | 10 | `84,86,88,90,94,96` | 1167 | `50cd57b092351d72b2a85cde87a6dd832eccf5580cad3f472980a3eb475520dc` |
| [orbit48ten](Reserved438x12-orbit48ten.json.gz) | 10 | `38,44,48,50,54,56,60,62,64,66,68,70,72,74,76,78,80,82` | 1183 | `3c920b0b7a74aec6b7fd840d211b9ff1fc0c8d6a5e3a0303c243e0be7c600014` |
| [orbit48tenlow](Reserved438x12-orbit48tenlow.json.gz) | 10 | `14,20,22,24,26,32,34` | 1175 | `48a3419388bae5eed977223a87c6af414638e6db041f67a6b154380cc86211e7` |
| [orbit48tenfresh](Reserved438x12-orbit48tenfresh.json.gz) | 10 | `30,40` | 1162 | `dda375d32a8338e71e791abd1557251d7494c1ecb5e749afd02a222f56ca1efe` |
| [orbit48tennested](Reserved438x12-orbit48tennested.json.gz) | 10 | `8,18` | 1230 | `8682e8805af445a6bae2780090d7fde0453acaf92646fbcf16923375c63dab11` |
| [orbit48tenhard](Reserved438x12-orbit48tenhard.json.gz) | 10 | `4,6,12,16,28,42,52,58` | 1266 | `1cf3892714b02d9ef60cbd07a3c1e28f39f32496078b2ef62b81a8474ca4ba33` |
| [orbit48tenhard10](Reserved438x12-orbit48tenhard10.json.gz) | 10 | `10` | 1230 | `54828bd8702af8264b8a9d0f62a34b4f1e8e8d96feb654617777910658fd89e7` |
| [orbit48tenhardfinal](Reserved438x12-orbit48tenhardfinal.json.gz) | 10 | `2,36,46` | 1314 | `4f0a44e51eaf08b0dbce96095342e6c36ef9012c3bdde8df71959eac6800ff3c` |

文件名中保留打包器的旧前缀，**这些记录不是 `(7,438)`，也没有预留固定 Euler**。锚为首 2 时的 `518019223567` 和首 10 时的 `531983`，继续用[双目标包](Root48Price.md) 证过的直接域。各包互斥并与[价格](Root48Price.md)及[付账重合](Root48Overlap.md)批数学互斥，核对的是完整 `(f,h)` 前缀，不拿二级指数的同值跨锚去重。

每个森林按 [冻结 Compose](../../Nov25/Compose/Compose.py) 通用账本与 [独立递归](../../Night2400/A/MaskedForest.py) 双算：每个认证根由固定 D 强迫；每个子标签只有一个父级，且必须在真实指数的 sigma 中整除才激活；未知额外入流只增加义务，未入图的重合先按全部支持剥离以防双付。唯一 Euler 最多分配给一处分量，亦可在整个图外。每个候选指数或实试、或由首个未试裸幂的单调尾覆盖。两套精确算术结果必须严格 `>B`。ECPP 标签逐个认证至确定性 64 位端点；每个包里非 64 位证书使用集合完整匹配。

所有表中包均已冷验。三类**不加 3 支持条件**的互斥证明并集留下：

- t²：从 48 直接值中排 **39**，剩 **`{2,4,6,8,10,12,16,18,22}`**。
- t¹⁰：从 85 直接值中排 **85**，首值完整排除；[完整合成](Full48Ten.py) 为 34 双价 + 4 CRT + 47 互斥森林。

首 t² 的后续[强掩码证明](Root48StrongMasks.md) 把余域压到 `h=12, v_3=2`，再由[完整首 2 比对](Full48Square.md)覆盖。整键需要把所有不同首值合并，见[完整键证明](Full48.md)，并仍不得仅凭键证明自动计作整片。

## 另一个分割方向：t² 强制 3 整除

[orbit48no3](Reserved438x12-orbit48no3.json.gz) 的严格森林只在 `3∤N` 这一掩码下使用；其范围是整个首 t²，**不是**全首排除。它与上面的二级排除是不同切面，可以合取，但不能把二者相加报作额外二级值。冻结规范条件下 t² 强迫 29、61。若 3 出现，则 3 至少为平方；加入 5 即丰度 >2。11 若出现，其指数 ≥4（11² 发禁素19）；当 3 至少四次时直接使丰度 >2，当 3² 时其发射 13 也使丰度 >2。3⁴ 发射 11，故也不可能。这给合法支持分割 `v_3=0`、`v_3=2`、`v_3≥6` 偶值；后两支尚须处理，仅第一支由本包整支关闭。[掩码 verifier](Verify48Masks.py) 的 `lemma()` 重算所有丰度不等式及直接整除，而非假借 t⁸ 已证结论。

```powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/Verify48Forest.py
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/Verify48Masks.py
```

两入口无需因式分解或网络。所有探索的未完成森林/超时叶均不在本包。
