# 31/598 与 19/682：只需六个整数多项式

| p,e | 全域 s | Kernel/Sponsor 后 | 原二阶 CRT 余窗 | 原逐盒叶 | 合并叶 | 包字节 | 结论 |
|---|---:|---:|---:|---:|---:|---:|---|
|31,598|599|219|31|7242|2|44715|完整指数接受|
|19,682|683|237|33|7062|4|21640|完整指数接受|

在冻结的19项之外，这两项可另计；相对于整个数据库的净增及分片映射须由合并端去重。两个大包亦分别独立全验通过，但不需要它们来复现结论。这不是将部分窗提升为指数：全域依然从零枚举，且包含高次、内部 Euler 与外部来源。每次需要剩余二阶格点判定时，验证器要求实际 `(C,c,z,T)` 及区间 `[lo,hi]` 由一个经数学验算的大盒覆盖；不能因为曾经遇见相同模数就跳过区间包含检查。每个实际指数虽有成千上万小盒，却各只有两个不同的完整同余类。因此可先尝试在许多小盒的**并的凸包**（含缝隙）上找同一个无根多项式；失败时才把集合对半拆分。发现程序用 FLINT，验证只用标准库与已建立的基线。

严格复验（在 `overnight` 目录）：
```
python -B Research/NightUniformReview/Verify31.py 31 598 --compact Research/NightUniformReview/later/short31.json.gz
python -B Research/NightUniformReview/Verify31.py 19 682 --compact Research/NightUniformReview/later/short19.json.gz
```

两条均实际 EXIT 0。SHA-256：31/598 `acc2968fd06bb9461cb1b40116fe7e1f1adf681008c263b38508a0b160ae75e3`；19/682 `25de6d5263435bdc55e30b3ec43135434e5d62818bb4b157186b35f91cfcd305`。`--collect` 只供发现，输出 NOT CERTIFIED，不能当作数学结论。
