# 续研检查点 · 11-28 02:30 +08；截止 07:30

基线 main=1447d41b；PR [10](https://github.com/stormwhip/PerfectNumbers/pull/10)，仅研究分支，不合并。已发布 779a69ad：16 个完整键（详[Proof](Proof.md)），3020/3072 闭合、52 片开放、62 个键、44 个单键片。状态 INCOMPLETE_FRONTIER。五个指定历史入口 PASS；首批五键联合冷验 3124.604s，不是全库冷验。

16 键包含 19^618、11^396、7^882；不要因旧工作记录仍称候选而重复登记。P0 的 19^282 仍余首赋值10，次级 4/12/22；3^12 仍余 1/96；7^12 的首层仍余12/42；细分域见[机器账本](Results.json)及未登记的独立收据。19^280 和19^330 全键候选须等最终数学+冷验。主攻 19^292 已发布38/59，新增10在审；11^396 工作已结束。19^292 探索 Build/Recover292.py；首批高阶定价试验 Price.py 可能太慢，可删减后再用。lead 作业一律用 job_list/job_output 收取；旧 NightMerge 全族285包冷验，3 workers，收据写 Build/ReceiptsColdBatchOne。团队研究至07:30，不要重置有效人员，见 task board。逐片只扣 VERIFIED_FULL；文件名 PascalCase，入 Git 仅正式包。近期优先：跟进19^280、19^330、11^456等候选，更新 PR/投影；压缩回复，只报实质更新。
