# 奇完全数证明进度看板

网站随 `main` 的提交重新构建。已打开的页面每分钟请求一次同源数据，并在切回页面时立即检查更新。页面展示累计闭片及截至日期筛选、最近批次净增量、根覆盖率、模型贡献、待证键分布、开放分片剩余指数数和可搜索的逐片台账。

## 发布与预览

GitHub Pages 使用仓库设置 **Pages → Build and deployment → Source → GitHub Actions**，由 [ProofDashboard](../.github/workflows/ProofDashboard.yml) 上传并部署生成目录。项目地址为 [stormwhip.github.io/PerfectNumbers/](https://stormwhip.github.io/PerfectNumbers/)。

在仓库根目录生成并预览页面。

```sh
python Dashboard/Build.py --ref main --out Build/Dashboard
python -m http.server 8000 --bind 127.0.0.1 --directory Build/Dashboard
```

## 数据依据

- 首批时间点来自[主线里程碑](../Records/Milestones.md)，时间使用对应的 Git 提交时间。后续节点从主线第一父链上的 `Research/*/OpenFrontier.json` 变更自动生成。一个快照批次写入一份最新的 `OpenFrontier.json`。闭片、开片、精确键和单指数片统计由逐片余集复算。
- [规范分片清单](../Research/FermatRootValuation/Results.csv)提供全部 3,072 个编号。当前余集中出现的分片标为开放，其余标为闭合。
- [Build.py](Build.py) 的 `CREDITS` 与 `LEDGER_CREDITS` 保留附有审阅依据的模型批次。合并后按净新增闭片量登记一条记录，重叠验证单列。缺少明确模型归属的闭片只进入主线总数。条件排除在整片闭合前不增加闭片数。
- 发布件包括静态页面和从账本提取的统计及待证指数。页面使用公开 Pages 地址，提交及报告入口指向 GitHub。
