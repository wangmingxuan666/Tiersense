<p align="center"><a href="https://tierflow.cn/tiersense"><img src="assets/tiersense-logo.png" alt="TierSense" width="500"></a></p>

<h1 align="center">TierSense</h1>

<p align="center"><strong>感知任务难度，判断何时压缩、何时召回。</strong></p>

<p align="center">
<a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
<a href="AUTHORS_STATEMENT.md"><img src="https://img.shields.io/badge/Authors-Statement-0969da" alt="Authors' statement"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a></p>

> **TierSense 系列总入口**：三个模块可以独立使用，也可按应用需要组合。这里集中提供项目导航、接入选择和[作者声明](AUTHORS_STATEMENT.md)。

## 三个模块，一个入口

| 模块 | 解决的问题 | 输出 | 使用指南 |
| --- | --- | --- | --- |
| [TierSense-Score](https://github.com/wangmingxuan666/Tiersense-score) | 当前任务有多难？ | 五路特征分数＋总分 | [难度打分](https://github.com/wangmingxuan666/Tiersense-score/blob/main/docs/usage.md) |
| [TierSense-Compress](https://github.com/wangmingxuan666/Tiersense-Compress) | 哪些历史步骤适合压缩？ | 逐步建议＋历史片段定位 | [历史压缩](https://github.com/wangmingxuan666/Tiersense-Compress/blob/main/docs/usage.md) |
| [TierSense-Memory-Decide](https://github.com/wangmingxuan666/Tiersense-memory-decide) | 现在是否需要压缩或召回？ | 两项判断＋各自置信度 | [记忆判断](https://github.com/wangmingxuan666/Tiersense-memory-decide/blob/main/docs/usage.md) |

三个模块提供决策信号，不代替应用执行模型切换、生成摘要或检索记忆。完整请求格式与最新功能说明以各子项目文档为准。

## 怎么选择

- **需要难度展示或模型路由依据**：使用 Score，应用自行配置分数到模型的映射。
- **需要选择可压缩的历史片段**：使用 Compress，再调用自己的摘要模型。
- **已有摘要／记忆系统，需要决定调用时机**：使用 Memory-Decide，按建议和业务条件执行。
- **想组合使用**：先阅读[组合接入说明](docs/agent-integration.md)。不是每个请求都必须调用三个接口。

## 快速开始

从 [TierSense 平台](https://tierflow.cn/tiersense) 获取调用 Key，选择对应的接口。以下地址沿用各项目当前文档，不因增加总仓库而改变。

| 功能 | POST 地址 |
| --- | --- |
| 难度打分 | `https://tierflow.cn/tiersense/v1/score` |
| 历史压缩选择 | `https://tierflow.cn/tiersense/v1/compress` |
| 压缩／召回判断 | `https://demo.tierflow.cn:1443/tiersense/v1/memory/decide` |

[查看三个接口的最小调用示例](docs/quickstart.md)。参数和返回结构不同，不能把某一个接口的字段直接用于另一个。

## 文档导航

- [快速调用](docs/quickstart.md)：三个接口的最小请求。
- [Agent 组合接入](docs/agent-integration.md)：调用位置、应用职责与使用边界。
- [作者声明](AUTHORS_STATEMENT.md)：集中维护的原声明与研究时间线材料。

这里是文档与项目导航总入口，不是合并后的推理服务，也不包含模型权重、生产配置或新的统一 SDK。三个原仓库及其历史保持独立；Memory Control 文章本次未上传。

## 欢迎进群交流

<p align="center"><a href="https://tierflow.cn"><img src="assets/tierflow-logo.png" alt="TierFlow" width="240"></a></p>

欢迎您使用我们的工作，也欢迎您提出宝贵意见。欢迎质疑、复现，也欢迎大家多多交流。

<img src="assets/community-qr.png" alt="TierFlow 官方交流群二维码与联系方式" width="640">
