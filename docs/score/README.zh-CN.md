<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="../../assets/tiersense-logo.png" alt="TierSense" width="500"></a>
</p>

<h1 align="center">TierSense-Score</h1>

<p align="center"><strong>感知任务难度，让模型路由理解上下文。</strong></p>
<p align="center">输入一个问题或 Agent 上下文，获得五路难度分数和一个综合分数。</p>

<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="usage.md"><img src="https://img.shields.io/badge/Docs-Usage_Guide-0969da" alt="使用指南"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#功能特性">功能特性</a> ·
  <a href="usage.md">Agent 接入</a> ·
  <a href="#加入社区">社区</a>
</p>

<p align="center"><a href="README.md">English</a> · <strong><a href="README.zh-CN.md">简体中文</a></strong></p>

---

> **[TierSense 总入口](../../README.zh-CN.md)** · [难度打分](../../docs/score/README.zh-CN.md) · [历史压缩](../../docs/compress/README.zh-CN.md) · [压缩／召回判断](../../docs/memory-decide/README.zh-CN.md)
>
> 作者声明及研究时间线集中维护于总仓库：[查看作者声明](../../AUTHORS_STATEMENT.md)。

## 项目介绍

**在 Agent 每次调用模型前，获得当前任务的难度信号。**

TierSense-Score 接收完整问题或 Agent 当前消息历史，返回五路特征难度分 `domain1–domain5` 和综合 `score`。你可以展示任务难度、观察执行过程中的分数变化，也可以将分数用于自己的模型路由策略。

两种使用方式：直接评估一个问题；或在 Agent 入口保存原始任务，每轮结合上下文评分。

## 功能特性

- <strong>单问题评分：</strong>直接提交完整问题文本。
- <strong>逐步感知：</strong>内部以任务和最近两个 step 构建评分状态。
- **五路特征分：**`domain1–domain5` 各为 0–2。
- <strong>综合难度分：</strong>返回经过标定的 0–10 分数。
- <strong>理解工具上下文：</strong>按调用 ID 关联工具调用与结果。
- <strong>接入 Agent：</strong>支持提交 Chat、Responses、Anthropic 消息历史与原始任务。

适用于代码助手、办公自动化、数学问题、多轮对话与工具任务。

## 快速开始

在 [TierSense 平台](https://tierflow.cn/tiersense) 获取 API Key，调用官网接口地址：

```text
POST https://tierflow.cn/tiersense/v1/score
```

```bash
curl "https://tierflow.cn/tiersense/v1/score" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TierSense",
    "messages": "修复多分类报表，处理同分与未知标签并添加测试。"
  }'
```

该问题在 2026-09-22 公网测试中的实际返回：

```json
{
  "feature_scores": {
    "domain1": 1.138822513813567,
    "domain2": 0.30560258244498567,
    "domain3": 1.2662245543458972,
    "domain4": 1.0611952851875979,
    "domain5": 0.0
  },
  "score": 2.9608480135599775
}
```

| 字段 | 范围 | 含义 |
| --- | --- | --- |
| feature_scores.domain1–domain5 | 各 0–2 | 五路特征难度分 |
| score | 0–10 | 综合难度分 |

总分经过内部加权与标定，不是五路直接相加，也不是任务成功率。

### Python

```bash
python3 -m pip install requests
```

```python
import os
import requests

response = requests.post(
    "https://tierflow.cn/tiersense/v1/score",
    headers={"Authorization": "Bearer " + os.environ["TIERSENSE_API_KEY"]},
    json={
        "model": "TierSense",
        "messages": "修复多分类报表，处理同分与未知标签并添加测试。"
    },
    timeout=(10, 120),
)
response.raise_for_status()
result = response.json()
print(result)
```

### JavaScript（服务端）

```javascript
// 在服务端调用，将 API Key 保存在环境变量中。
const response = await fetch(
  "https://tierflow.cn/tiersense/v1/score",
  {
    method: "POST",
    headers: {
      Authorization: "Bearer " + process.env.TIERSENSE_API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "TierSense",
      messages: "修复多分类报表，处理同分与未知标签并添加测试。"
    })
  }
);
if (!response.ok) throw new Error("判断请求失败");
const result = await response.json();
console.log(result);
```

## 接入流程

```text
用户输入问题 → 保存 task
                  ↓
当前 messages + task → TierSense-Score → 本轮难度分数
                  ↓
             Agent 调用主模型
                  ↓
             执行工具、更新历史
                  └→ 下一轮再次评分
```

在用户输入入口保存原始问题，每次模型调用前提交 `task` 和当前非空 `messages`：

```json
{
  "model": "TierSense",
  "task": "修复登录接口的并发问题，并补充回归测试。",
  "messages": [
    {"role": "user", "content": "修复登录接口的并发问题，并补充回归测试。"},
    {"role": "assistant", "content": "已定位共享状态，准备补充回归测试。"}
  ]
}
```

分数单独记录，Agent 继续使用原始消息历史。[使用指南](usage.md) 提供 Python 接入方法与原生工具消息示例。

## 文档

- [使用指南](usage.md)：输入格式、返回结果、Python 调用与 Agent 接入。
- [English usage guide](usage.en.md).
- [TierSense-Compress](../../docs/compress/README.zh-CN.md)：历史压缩决策配套项目。

本仓库提供托管 API 文档与接入示例，暂不包含模型权重和自部署推理服务源码。

---

## 加入社区

<p align="center">
  <a href="https://tierflow.cn"><img src="../../assets/tierflow-logo.png" alt="TierFlow" width="240"></a>
</p>

<p align="center">来自 TierFlow 团队 · 欢迎交流与合作</p>

扫描二维码，加入官方交流群。

<img src="../../assets/community-qr.png" alt="TierFlow 官方交流群二维码与联系方式" width="640">
