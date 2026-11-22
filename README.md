# PerfectNumbers

奇完全数规模下界的计算研究。项目将终局线性规划（LP）和因子链搜索用于同一套下界证明。

## Python 实验

在 GitHub 仓库的 **Actions → Python experiments → Run workflow** 启动实验。修改 Python 脚本、依赖或工作流并推送时也会触发实验。每个脚本的输出单独保存在该次运行的对应步骤中。

| 脚本 | 用途 |
| --- | --- |
| `复现程序/baseline.py` | 对比两种终局 LP 模型 |
| `复现程序/test.py` | 禁用素数留一实验与路障参数扫描 |
| `复现程序/ScriptA.py` | 终局区间对偶校验与 Roadblock 2 浮点阈值搜索 |

## 因子链证明树

C++/GMP 证明树、索引生成器和已有日志的原始位置记录在 [交接文档](复现程序/gemini.md)。迁移这部分后，长跑实验可使用手动触发的独立工作流。

原始分解库 `checkfacts.txt.gz` 大小为 698719834 字节。可作为私有 Release 的附件保存，由因子链工作流按版本下载并核对 SHA-256。

```text
ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119
```

## 资料

- [路线 A 技术报告](a.tex)
- [Ochem–Rao 2012 原论文](S0025-5718-2012-02563-4.pdf)
