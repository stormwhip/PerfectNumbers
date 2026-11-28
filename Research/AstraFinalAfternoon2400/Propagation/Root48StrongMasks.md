# 根 `(7,48)` 首值 2：局部丰度掩码逼至唯一二级余点

规范假设和 t 同[双价证明](Root48Price.md)，锚 `r=518019223567`，首值 `v_t=2`。在无 3 分支已排的前提下，原始九个二级余值中的 **`v_r∈{2,4,6,8,10,16,18,22}`** 获完整排除。`v_r=12, v_3≥6` 亦排；此中间批唯一剩 **`v_r=12, v_3=2`**，由后续[完整首值证明](Full48Square.md)另排。本包不单独报首值 2 整闭，也不把二级与支持叶重复计数。

## 重建而非假定局部禁集

因为已验 `3|N`，合法 3 域分成 `v_3=2` 与 `v_3≥6`，并且 5、11 都禁（见[掩码引理](Verify48Masks.py)）。固定 `r^h` 后，利用认证素数、逐个整除前三或四个精确输出，得到有限一组普通/潜在 Euler 的强迫质因数；所有 3 mod 4 的强迫数至少支付平方，其他只付一次，**不假设哪一个是 Euler**。把实际固定幂、已证明的强迫质量下限及 >=6 支中的 `3^6` 共同用于丰度。任何另一个可能素数 q 出现时，若再按 q 的最低可能幂支付就已 `σ/N>2`，则 q 在该精确支必禁。记录中的每个新增禁素数逐一用整数丰度重新生成结论；没有假定发现器的列表完备、也不借用其他支持支的禁集。新增禁令只对这一个精确前缀/支持支成立。

由此可用含更多禁止发射的[两种精确森林递归](Root48Forests.md)，再检查遍历唯一父级、认证所有根/所有者与严格单调尾。所有 17 个正3支持叶已冷验；若同一 h 的正3两支齐全，结合全首的 `3∤N` 森林才升为完整二级。

| 数据包 | `(v_r,3分支)`，6 代表 ≥6 | ECPP | SHA-256 |
|---|---|---:|---|
| [strong](Reserved438x12-orbit48strong.json.gz) | `(6,2),(8,2),(10,2)` | 1033 | `ad0d796471da29e6258e06b8f097ccb7ce88a0c48c29579fd5cc45ab7b7ab206` |
| [strongmore](Reserved438x12-orbit48strongmore.json.gz) | `(2,2),(2,6),(4,2),(16,2)` | 1193 | `7c56b29487df8df4da011208bb330e8250b227b2818a96f5441a011a9d66968f` |
| [strongextra](Reserved438x12-orbit48strongextra.json.gz) | `(4,6),(6,6),(8,6),(12,6),(18,2)` | 1189 | `4fa5f660fe33dee0adac10163c3c4f78a7a721e1115ce817493633f91024a6bc` |
| [strongtail](Reserved438x12-orbit48strongtail.json.gz) | `(10,6),(16,6),(22,2)` | 1241 | `722d375c60d553494ca3afaa53c532bcf04c5965961de26063830e80186db9dc` |
| [strong18](Reserved438x12-orbit48strong18.json.gz) | `(18,6)` | 1098 | `6bc632babfc127445116dea0c84a1fe2b50ce1ee9cecf77286f6830a108069de` |
| [strong22](Reserved438x12-orbit48strong22.json.gz) | `(22,6)` | 1140 | `d4af154238142ce86ffae3605b91dce1374f563d74cff066dd140b5f1d4c618b` |

```powershell
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/Verify48StrongMasks.py
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Propagation/Project48.py --sets-only
```

集合模式不执行证明，只检查笔记对应的相交/补集。没有该标志的[近闭合集成入口](Project48.py)重放所有数学及支持证书。本中间批合成后，首 t² 的完整二级排除为 47/48；[首 t² 补齐](Full48Square.md)和[首 t¹⁰ 的 85/85 合成](Full48Ten.py)均另有入口，首 t¹⁰ 不依赖本掩码。
