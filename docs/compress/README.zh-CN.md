<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="../../assets/tiersense-logo.png" alt="TierSense" width="500"></a>
</p>

<h1 align="center">TierSense-Compress</h1>

<p align="center"><strong>学会何时压缩，让 Agent 持续前行。</strong></p>
<p align="center">面向长程 Agent 的状态条件历史压缩。</p>

<p align="center">
  <a href="https://arxiv.org/abs/2609.27298"><img src="https://img.shields.io/badge/arXiv-2609.27298-b31b1b" alt="arXiv 2609.27298"></a>
  <a href="https://arxiv.org/pdf/2609.27298"><img src="https://img.shields.io/badge/Paper-StateComp-b31b1b" alt="StateComp PDF"></a>
  <a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="usage.md"><img src="https://img.shields.io/badge/Docs-Usage_Guide-0969da" alt="使用指南"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#功能介绍">功能介绍</a> ·
  <a href="method.md">方法说明</a> ·
  <a href="usage.md">Agent 接入</a> ·
  <a href="https://arxiv.org/pdf/2609.27298">论文 PDF</a> ·
  <a href="#欢迎进群交流">交流社区</a>
</p>

<p align="center"><a href="README.md">English</a> · <strong><a href="README.zh-CN.md">简体中文</a></strong></p>

<p align="center"><strong>StateComp: Learning When to Compress History in Long Horizon Agents</strong></p>

---

> **[TierSense 总入口](../../README.zh-CN.md)** · [难度打分](../../docs/score/README.zh-CN.md) · [历史压缩](../../docs/compress/README.zh-CN.md) · [压缩／召回判断](../../docs/memory-decide/README.zh-CN.md)
>
> 作者声明及研究时间线集中维护于总仓库：[查看作者声明](../../AUTHORS_STATEMENT.md)。

## 关于项目

**让 Agent 知道哪些历史步骤适合压缩。**

TierSense-Compress 面向多轮对话和工具型 Agent。输入当前上下文，返回逐步压缩建议，以及满足你所设条件的连续历史片段。调用方使用自己的摘要模型生成摘要，再将更新后的上下文交给主 Agent 继续执行。

它将「判断是否适合压缩」与「生成摘要」分开，让你可以独立选择主模型、摘要模型和压缩频率。

## 功能介绍

- **逐步判断**：对当前可见的 assistant 历史步骤返回 `should_compress`、`confidence`。
- **工具上下文适配**：一个 assistant 及其关联工具结果作为一个步骤处理。
- **连续片段选择**：配置检查间隔、连续步骤数、token 门槛和置信度门槛。
- **精确定位**：返回 `message_indices`，对应本次提交的消息数组。
- **中途接入**：直接提交当前上下文；可显式提供 `task`，也可从支持的用户输入中提取任务。
- **摘要模型自由选择**：接口负责选择片段，调用方负责摘要和会话更新。

适合代码助手、办公自动化、多轮问答，以及包含工具调用的长任务。

## 快速开始

在 [TierSense 平台](https://tierflow.cn/tiersense) 获取 API Key，然后调用：

```text
POST https://tierflow.cn/tiersense/v1/compress
```

```bash
curl "https://tierflow.cn/tiersense/v1/compress" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TierSense",
    "messages": [
      {"role": "user", "content": "计算17+28，然后乘2"},
      {"role": "assistant", "content": "17+28=45"},
      {"role": "user", "content": "继续"}
    ]
  }'
```

读取返回的 `steps`：

| 字段 | 含义 |
| --- | --- |
| should_compress | `true` 建议压缩；`false` 建议保留 |
| confidence | 对当前建议的支持程度，范围 0–1 |
| message_indices | 此步骤在输入消息数组中的位置，从 0 开始 |

这个例子只有一个历史步骤，是否建议压缩以实际响应为准。

## 接入流程

```text
当前上下文 → TierSense-Compress → 选中片段
                                     ↓
下一次主模型调用 ← 更新后的上下文 ← 调用方生成摘要
```

需要批量执行策略时，在请求中增加：

```json
{
  "options": {
    "check_interval": 1,
    "span": 3,
    "min_tokens": 2000,
    "confidence_threshold": 0.7
  }
}
```

含义：每个可见历史步骤检查一次；只采用建议压缩且置信度达标的步骤；同一片段至少连续 **4 步**、合计**超过 2000 tokens** 才进入摘要流程。读取 `execution.spans` 中 `trigger_compression=true` 的片段即可。

## 方法概览

![StateComp 方法框架图](../../assets/statecomp-framework.png)

[查看原始框架图 PDF](../../assets/statecomp-framework.pdf)

模型将原始任务与最近两步构成的紧凑状态编码为主向量，用 BM25 选取最多三个较早历史块，通过缓存隐藏向量与 late interaction 聚合形成状态表示，再对历史状态和当前状态进行配对判断。

这是上下文内的压缩选择，不是外部记忆召回；摘要由调用方生成，并留在调用方的当前会话中。

## 文档

- [方法说明](method.md)：状态构造、历史块选择、模型判断与执行策略。
- [使用指南](usage.md)：请求格式、参数、返回值、Python 接入和使用案例。

本模块提供方法文档与托管 API 接入示例；不包含模型权重或自托管推理服务源码。

---


### 欢迎进群交流

<p align="center">
  <a href="https://tierflow.cn"><img src="../../assets/tierflow-logo.png" alt="TierFlow" width="240"></a>
</p>

<p align="center">由 TierFlow 团队带来 · 欢迎交流与合作</p>

扫描下方二维码加入官方交流群。如果想了解具体研究时间线，欢迎与该账号本人联系。

<img src="../../assets/community-qr.png" alt="TierFlow 官方交流群二维码与联系方式" width="640">
