# 11 月 26 日证明包

本目录是对主线 `2889e47f6db49c8a9bc8dda2c9153829c18a70ca` 的增量，不是完整的奇完全数下界证明。请以[当前状态](../../Documentation/CurrentStatus2400.md)和[全量开放清单](Delta.json)为准。账本中每一项 `proofs` 都指向一个可重放的完整排除；条件支持包、部分来源窗口和失败实验不登记在该列表中。

## 从干净检出重放

Python 3.11+，需要启用断言。完整重放还需 GCC/Clang C++17（支持 `unsigned __int128`），可通过 `CXX` 指定编译器可执行文件。这是用于 1162 的确定性素因子范围检查，不能以现成日志、可执行缓存或概率性素性结果代替。验证不需要在线因子服务、SciPy、PARI 或发现阶段的数据库。

```sh
python -I -S -B -X int_max_str_digits=0 Research/Session20261126/Replay.py
python -I -S -B Research/Session20261126/PacketTests.py
python -I -S -B Research/Session20261126/Support/Verify.py
python -I -S -B Research/Session20261126/GlobalSupport/Verify.py --integer-logs
python -I -S -B Research/Session20261126/SupportProjection.py
```

第一条重新计算全部新增实际指数及其分片投影，要求结果等于版本中的账本。`--write` 供研究分支重新生成账本用；并非普通验收所需。后一组支持命中结论依赖既有三个命中定理，其历史完整重放入口是 `Research/MiddayTerminal/ReleaseThirteen.py --baseline`。尚未闭合处不可用时间预算、未发现因子或未得到反例作否定。

## 阅读顺序

1. [总体证明](../../Documentation/Proof2400.md)：规范根、因子流入、Euler 唯一性、尺寸及丰度账的含义。
2. [增量账本](Delta.json)：按 `(root,e)` 而非证明包数去重，再要求分片的**全部**剩余实际指数被包含。[复验入口](Replay.py)只允许普通森林作指标整除提升；枢轴、条件树、联合供给、精确大指数证书一律不自动提升。
3. [联合供给森林](SupplyForest/Proof.md)、[枢轴断点](SupplyForest/Breakpoint/Proof.md)：区分一次 Euler 所在位置与其未知来源，处理多账本的共同指数选择及单一退款。[根三 1162](Joint/Additional.md)另需分别证内部、外部来源的所有叶。
4. [条件支持](Support/Readme.md)、[全局命中集](GlobalSupport/Readme.md)、[来源理论](Source/SourceSquare.md)：注意不同分母与适用假设。[支持投影](SupportProjection.py)给出条件与完整结果的精确交并。
5. [其余四个根三高指数的基础界](NextBase/README.md)和[根十九精确 Euler 位置限制](LowSupport/README.md)是**部分结果**，不独立计为完整指数。可选范围复验可用精确模块算术库 python-flint；已登记的完整指数验收不依赖它。
6. [实验日志](../../Records/ExperimentLog.md)与[可选发现器](Discover.py)。后者从 `data-v1` 的索引产生不可信候选标签；正式验收另做精确整除、素性证书、尾部完备性及严格阈值检查。
