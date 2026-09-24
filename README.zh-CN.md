<p align="center"><a href="https://tierflow.cn/tiersense"><img src="assets/tiersense-logo.png" alt="TierSense" width="500"></a></p>

<h1 align="center">TierSense</h1>

<p align="center"><strong>感知任务难度，判断何时压缩、何时召回。</strong></p>

<p align="center">
<a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
<a href="AUTHORS_STATEMENT.md"><img src="https://img.shields.io/badge/Authors-Statement-0969da" alt="Authors' statement"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a></p>

> **TierSense 系列总入口**：三个模块可以独立使用，也可按应用需要组合。这里集中提供项目导航、接入选择和[作者声明](AUTHORS_STATEMENT.md)。

> [!IMPORTANT]
> **作者声明｜独立技术路线与研究时间线**
>
> 我们深表遗憾在这个时代，发表工作竟要澄清自己的工作是什么时候开始做的。但是我们依旧要做。
>
> 我们郑重声明：三个方法及两篇文章在**北京时间 2026 年 9 月 14 日之前已完稿，实际时间完稿时间会更早（有微信截图证明，见文末）**，Jev 出现的时间为 **2026 年 9 月 15 日**。这是我们投入约半年、才终于对外发布的工作，绝不是在 Jev 出现后几天内用 AI 快速拼凑出来的文章。且两篇文章是研究过程中产生的分支，均是经过检验后产生的完整研究，经过反复打磨在近期挂出来的。如果想了解具体时间线，欢迎与该账号本人联系。
>
> **本方法与 Jev 采用完全不同的技术路线，具有自己的机理发现。我们认为这是独立技术路线上的超越，而非对 Jev 的复刻或几天内的追随。**这里表达的是作者对原创性与技术路线的判断，不是宣称已经公布了覆盖所有任务的性能优越性证明。
>
> 我们反对以“auto research”之名快速拼凑、缺乏实质研究的内容，也不赞同仅凭发布时间，就给认真投入的工作贴上这样的标签。我们始终希望为社区带来真正的贡献，也认可 AI 辅助研究能够产出高质量成果；但我们不希望这项投入心血完成的方法与文章，在未经认真了解的情况下，被简单归为“自动水文”。
>
> 与此同时，我们理解大家对研究质量的担忧，也很高兴有人愿意站出来发声、维护有价值的学术讨论。我们希望与您一道，做出并发表真正有价值的工作，让认真研究得到认真对待，而不是让长期投入的成果在一夜之间被轻率地判为“水文”。如果您对此感兴趣，欢迎加入官方交流群，与我们一起交流、探索，开展更多有趣且扎实的研究。
>
> 欢迎您使用我们的工作，也欢迎您提出宝贵意见。欢迎质疑、复现，也欢迎大家多多交流。

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

## 研究时间线截图

<img src="assets/wechat-timeline.png" alt="作者提供的研究时间线微信截图" width="600">
