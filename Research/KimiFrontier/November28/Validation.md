# 验证记录

## 环境、输入与边界

- 冻结基线：`db71cc42ad2a62e3e362b8874757c1cff0b7772f`。
- 本地环境：Windows，CPython 3.12；命令使用隔离模式 `-I -S -B`，保留显式检查。
- 证书 SHA-256：`db374e6b6ea58c9d8dcec07aa09ea44efdca6962e891492da894ca211634dd21`。
- 主验证器 SHA-256：`1e20416365769f38ce752ac99f075b90e5e7db463b321a376b6a65149b4c35a0`。
- 独立复验器 SHA-256：`60c67ffdff9ed1efeea58f12b8ad539b439d503b49b999d5084d5d1df9b3c023`。
- 本记录不是全部历史分片的端到端冷重放，也没有运行 72 小时全局验收。

## 主验证器

命令：
```sh
python -I -S -B -X int_max_str_digits=0 Research/KimiFrontier/November28/Verify.py
```

最终结果：退出码 `0`，总墙钟时间 `0.879508 s`（验证器内部算术耗时 `0.709870 s`）。共 `11952` 项显式检查，认证固定素数，重建首枢轴 70 个合法赋值及尾界 188，重建本纤维 138 个合法子值及严格尾界 555，重算 5 个 `19` 亏格底数、`1109` 零亏格和全部 138 个终端整数比较。输出为 `VERIFIED_CONDITIONAL`、`fiber_closed=true`、`new_local_exclusions=2`、`new_complete_keys=0`、`new_closed_shards=0`。

## 第二套独立复算

命令：
```sh
python -I -S -B -X int_max_str_digits=0 Research/KimiFrontier/November28/Independent.py
```

最终结果：退出码 `0`，总墙钟时间 `0.851410 s`（内部耗时 `0.691840 s`），`1812` 项检查，输出 `INDEPENDENT_PASS`。该实现不导入主验证器；固定素数改用无符号 64 位确定性七底 Miller–Rabin，Hensel 提升改用 $r\mapsto r^p$ 的递推，并独立重建分支、需求、亏格表及终端比较。对任意大小的候选底数，Miller–Rabin 见证只用于证明合数；通过测试者仍保守保留。

## 负向回归

命令：
```sh
python -I -S -B -X int_max_str_digits=0 Research/KimiFrontier/November28/Verify.py --run-negative-tests
```

退出码 `0`，总墙钟时间 `1.929493 s`。以下五项均被拒绝：

1. 从新增成果中遗漏真实子值 `h=4`；
2. 将目标 `19` 的权重改为不满足阶 1 支配的 7；
3. 把合数 91 冒充固定素数；
4. 将精确亏格乘积的分子加 1；
5. 从终端证书中删除 `h=4`。

这里的退出码 0 表示所有负向用例均按预期触发 `VerificationError`，不是接受被篡改的证书。

## 历史基线与仓库检查

历史补充包复验命令
```sh
python -I -S -B -X int_max_str_digits=0 Research/GeminiFrontier/November28/ReviewVerify.py
```
已在原始 LF 字节上通过，确认旧证书仍只余 `h=2,4`。仓库结构检查
```sh
python -I -S -B Sources/Python/RepositoryStructureChecks.py
```
退出码 `0`，输出 `REPOSITORY_STRUCTURE_OK files=21092 markdown_links_verified=YES`；该文件数是检查时的已追踪基线文件数，不包含本包新增文件。

## 验收边界

本包新增排除两个局部精确子域，并由此闭合首枢轴赋值 1 的完整纤维。`(19,276)` 仍有首赋值 `2,8,16,18,28`，所以完整精确键增量和规范分片闭合增量均为 0；全局投影保持 `3029/3072`、43 个开放分片、53 个开放精确键，状态保持 `INCOMPLETE_FRONTIER`。
