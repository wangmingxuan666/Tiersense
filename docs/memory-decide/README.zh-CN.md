<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="../../assets/tiersense-logo.png" alt="TierSense" width="500"></a>
</p>

<h1 align="center">TierSense-Memory-Decide</h1>

<p align="center"><strong>学会何时压缩、何时召回，让 Agent 持续前行。</strong></p>
<p align="center">面向长程 Agent 的上下文记忆决策 API。</p>

<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="https://arxiv.org/abs/2609.27286"><img src="https://img.shields.io/badge/arXiv-2609.27286-b31b1b" alt="arXiv 2609.27286"></a>
  <a href="https://arxiv.org/pdf/2609.27286"><img src="https://img.shields.io/badge/Paper-Memory_Control-b31b1b" alt="Memory Control PDF"></a>
  <a href="usage.md"><img src="https://img.shields.io/badge/Docs-Usage_Guide-0969da" alt="使用指南"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#功能介绍">功能介绍</a> ·
  <a href="method.md">功能边界</a> ·
  <a href="usage.md">Agent 接入</a> ·
  <a href="#欢迎进群交流">交流社区</a>
</p>

<p align="center"><a href="README.md">English</a> · <strong><a href="README.zh-CN.md">简体中文</a></strong></p>

---

> **[TierSense 总入口](../../README.zh-CN.md)** · [难度打分](../../docs/score/README.zh-CN.md) · [历史压缩](../../docs/compress/README.zh-CN.md) · [压缩／召回判断](../../docs/memory-decide/README.zh-CN.md)
>
> 作者声明及研究时间线集中维护于总仓库：[查看作者声明](../../AUTHORS_STATEMENT.md)。

## 关于项目

**让 Agent 判断现在是否需要压缩历史、是否需要召回历史信息。**

TierSense-Memory-Decide 接收原始用户任务和 Agent 当前上下文，返回压缩、召回两项建议及各自的置信度。你的应用根据建议和实际业务条件，调用自己的摘要或检索模块，再继续任务。

它将「记忆决策」与「记忆执行」分开：不绑定主模型、摘要模型或记忆存储。

## 功能介绍

- **双路判断**：同时获得 `compression` 和 `recall` 建议。
- **明确结果**：每项返回 `predicted` 与 `confidence`。
- **上下文接入**：提交完整、有序消息，包含已经完成的工具调用与结果。
- **任务独立传入**：在用户问题进入 Agent 时保存 `task`，后续自动携带。
- **多种消息格式**：提供 CodeBuddy / WorkBuddy、Codex、Claude Code、DeepSeek Harness 的输入示例。
- **执行方式自由选择**：由应用选择历史、生成摘要、检索记忆及更新上下文。

适合代码助手、办公自动化、多轮对话与长程工具任务。支持的消息格式不等于已为所有 Agent 版本提供自动安装插件。

## 快速开始

在 [TierSense 平台](https://tierflow.cn/tiersense) 获取 API Key。当前接入地址：

```text
POST https://tierflow.cn/tiersense/v1/memory/decide
```

```bash
curl "https://tierflow.cn/tiersense/v1/memory/decide" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TierSense",
    "task": "检查 demo_report 项目的测试，说明失败原因。",
    "messages": [
      {"role": "user", "content": "检查 demo_report 项目的测试，说明失败原因。"},
      {"role": "assistant", "content": "已阅读测试文件，正在核对失败用例。"}
    ]
  }'
```

返回格式示例（不代表上述输入的固定结果）：

```json
{
  "compression": {"predicted": true, "confidence": 0.8, "positive_votes": 4},
  "recall": {"predicted": false, "confidence": 0.6, "positive_votes": 2},
  "confidence_type": "ensemble_agreement"
}
```

| 字段 | 含义 |
| --- | --- |
| compression.predicted | 是否建议考虑压缩历史 |
| recall.predicted | 是否建议考虑召回历史 |
| confidence | 对该项最终判断的支持程度，范围 0–1，不是校准后的正确概率 |

直接读取 `predicted`，不要用 `confidence` 重新判断“是／否”。例如 `false + 0.8` 表示支持“不执行”的判断。其他字段是兼容附加字段，业务接入无需依赖。

## 接入流程

```text
保存原始 task + 当前完整上下文 → TierSense-Memory-Decide
                                         ↓
                               压缩建议 + 召回建议
                                         ↓
下一次主模型调用 ← 更新后的上下文 ← 应用自己的摘要／检索模块
```

推荐在本轮工具结果全部返回后、下一次主模型请求前调用。没有可压缩旧历史或可召回记忆时，不执行对应操作。调用失败时保留上下文，不把失败伪装成“否”。

## 功能边界

本接口只判断**当前时机**，不返回逐历史步骤分数、选中步骤、消息索引、摘要或检索内容；不自动修改会话。

如果你需要逐步压缩建议与历史片段定位，请查看 [TierSense-Compress](../../docs/compress/README.zh-CN.md)。两者请求与返回契约不同，不能混用 `steps`、`execution.spans` 或压缩片段配置参数。

## 论文

[Memory Control Signals Emerge Before Action in Long Horizon Agents](https://arxiv.org/pdf/2609.27286)

阅读或下载作者提供的完整 PDF（35 页）。论文研究系统与本仓库的托管判断 API 并非同一公开范围；API 的功能边界以使用指南为准。

## 文档

- [功能边界与接入职责](method.md)：服务负责什么、应用负责什么。
- [用户使用指南](usage.md)：请求格式、四种 Agent 示例、Python 调用与业务接入。

本模块提供托管 API 文档与接入示例，不包含模型权重或自托管推理服务源码。

---


## 欢迎进群交流

<p align="center">
  <a href="https://tierflow.cn"><img src="../../assets/tierflow-logo.png" alt="TierFlow" width="240"></a>
</p>

<p align="center">由 TierFlow 团队带来 · 欢迎交流与合作</p>

扫描下方二维码加入官方交流群，交流 Agent 接入和记忆管理实践。

<img src="../../assets/community-qr.png" alt="TierFlow 官方交流群二维码与联系方式" width="640">
