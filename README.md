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

源码位于 [cpp/](cpp/)，包含分解索引生成器以及 C++/GMP 证明树 v1 至 v5。源码变更会在 Actions 中触发编译检查。要运行证明树，打开 **Actions → C++ factor-chain experiments → Run workflow**，填写目标指数并选择一个根素数或 `all`。单根实验沿用原证明树的禁用顺序，结果对应选中的根分支。过往实验记录见 [交接文档](复现程序/gemini.md)。

工作流优先从私有 Release `data-v1` 下载 698719834 字节的 `checkfacts.txt.gz`。Release 下载不可用时，工作流尝试从 [Ochem 的项目页](https://www.lirmm.fr/~ochem/opn/) 下载。两条路径均核对同一个 SHA-256，通过后才构建索引并运行 v5。只有选中的每个根分支都输出 `PROVEN` 且失败路障数为零时，工作流才通过。

```text
ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119
```

## 资料

- [路线 A 技术报告](a.tex)
- [Ochem–Rao 2012 原论文](S0025-5718-2012-02563-4.pdf)
