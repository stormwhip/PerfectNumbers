# PerfectNumbers — 奇完全数 \(10^{2400}\) 下界研究

本仓库专注一个明确目标：证明每个奇完全数 \(N\) 都满足 **\(N>10^{2400}\)**，并提供可独立检查的完整计算证书。

**当前状态：** 在 \(N\) 与 \(S_8=\{3,5,7,11,13,17,19,31\}\) 全部互素的前提下，增强 LP 的区间对偶程序输出 \(\log_{10}N\ge2400.822998027028\)。这是一项**条件性数值结果**。全部八个根素数的穷尽排除及 LP 数值的独立严格审计仍未完成。

## 项目进展报告

**[10^2400 项目进展报告](Documentation/ProgressReport2400.md)**：前人工作、我们已完成的代码与实验、验证风险、下一步工作的优先级和验收条件。

## 当前工程

| 入口 | 作用 |
| --- | --- |
| [ProofTreeV16.cpp](Sources/Cpp/ProofTreeV16.cpp) | 当前八根 C++17 / GMP / OpenMP 证明树 |
| [BuildIndex.cpp](Sources/Cpp/BuildIndex.cpp) | Ochem 固定因子数据库索引构建 |
| [ProofCoreTestsV16.cpp](Sources/Cpp/ProofCoreTestsV16.cpp) | C++ 回归测试 |
| [IntervalCertificate61.py](Sources/Python/IntervalCertificate61.py) | 含 61 高次幂因子和蕴含的增强 LP |
| [PrefixDualCertificates.py](Sources/Python/PrefixDualCertificates.py) | 生成全部 256 个根前缀的增强对偶和 V16 的必要增益 CSV |
| [ConditionalPrime61.py](Sources/Python/ConditionalPrime61.py) | 61 指数条件化 LP 交叉检查 |
| [Prime61FactorChecks.py](Sources/Python/Prime61FactorChecks.py) | 精确整数等式及素性核验 |
| [ExperimentLog.md](Records/ExperimentLog.md) | 历史正反实验、运行编号、版本留痕 |
| [ValidationChecklist.md](Records/ValidationChecklist.md) | 证明级审计待办 |

### 小规模复现

在 Linux 或 WSL2 上安装 C++17、GMP、zlib、Python 及 Requirements.txt 中依赖。随后在仓库根目录执行：

    python3 -m pip install -r Requirements.txt
    python3 Sources/Python/Prime61FactorChecks.py
    python3 Sources/Python/ConditionalPrime61.py

    mkdir -p Build
    python3 -u Sources/Python/PrefixDualCertificates.py Build/PrefixDualBounds.csv
    g++ -std=c++17 -O2 Sources/Cpp/BuildIndex.cpp -lz -o Build/BuildIndex
    g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofTreeV16.cpp -lgmpxx -lgmp -o Build/ProofTreeV16
    g++ -std=c++17 -O2 -fopenmp Sources/Cpp/ProofCoreTestsV16.cpp -lgmpxx -lgmp -o Build/ProofCoreTestsV16
    ./Build/ProofCoreTestsV16

完整因子链运行需要 Ochem 提供的 checkfacts.txt.gz 固定数据库。其 SHA-256 为：

    ff1e84b119949ffcce57b29616d57ed5d03793ad3e4f74f1b203ad0e809f4119

数据库放入 Build 目录后，从该目录执行：

    ./BuildIndex checkfacts.txt.gz
    export OMP_NUM_THREADS=2
    ./ProofTreeV16 2400

单独运行某个根时，程序假定根顺序中此前的根素数已经被排除；**单根返回 PROVEN 不能代替全部八根证明**。

### GitHub Actions

- [QualityChecks.yml](.github/workflows/QualityChecks.yml)：源代码编译和轻量单元测试。
- [Conditional61Lp.yml](.github/workflows/Conditional61Lp.yml)：61 因子分解与增强 LP 数值复现。
- [FactorChain2400.yml](.github/workflows/FactorChain2400.yml)：**只在手动启动时运行**，默认仅编译；用户明确选择后才下载大型数据库并执行指数 2400 计算。

## 证明与历史版本

严格的无条件 \(N>10^{2400}\) 需要：全部八根穷尽树 + 互素 LP 独立证书 + 所有分支剪枝与因子数据的证明级审计。详见 [审计清单](Records/ValidationChecklist.md)。

旧版本 V1–V15、V17、历史实验代码及不再使用的工作流已移出当前主分支，完整内容可从[精简前快照 124ab214](https://github.com/stormwhip/PerfectNumbers/tree/124ab21449d4afd9d017a32faa9bd27253943c70)恢复；历史结果仍保存在 ExperimentLog 中。
