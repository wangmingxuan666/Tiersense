<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="../../assets/tiersense-logo.png" alt="TierSense" width="500"></a>
</p>

<h1 align="center">TierSense-Score</h1>

<p align="center"><strong>Understand task difficulty. Route with context.</strong></p>
<p align="center">Five difficulty scores and one overall score for questions and agent workflows.</p>

<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="usage.en.md"><img src="https://img.shields.io/badge/Docs-Usage_Guide-0969da" alt="Usage guide"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#features">Features</a> ·
  <a href="usage.en.md">Agent Integration</a> ·
  <a href="#join-the-community">Community</a>
</p>

<p align="center"><strong><a href="README.md">English</a></strong> · <a href="README.zh-CN.md">简体中文</a></p>

---

> **[TierSense hub](../../README.md)** · [Score](../../docs/score/README.md) · [Compress](../../docs/compress/README.md) · [Memory-Decide](../../docs/memory-decide/README.md)
>
> Authors' statements and research timeline material are maintained centrally: [Read the statements](../../AUTHORS_STATEMENT.en.md).

## About the project

**Give your agent a difficulty signal before its next model call.**

TierSense-Score accepts a complete question or an agent's current message history and returns five feature difficulty scores (`domain1–domain5`) and an overall `score`. Use the result to display difficulty, observe how a task evolves, or inform your own model-routing policy.

Two entry points, one API: score a standalone question, or capture the original task and score each round of an agent workflow.

## Features

- **Question scoring:** submit a complete question as plain text.
- **Step-aware scoring:** build the scoring state from the task and the two most recent steps.
- **Five feature scores:** each `domain1–domain5` value ranges from 0 to 2.
- **One overall score:** a calibrated difficulty signal from 0 to 10.
- **Tool-aware context:** associate tool calls with their results using call IDs.
- **Agent integration:** submit Chat, Responses, or Anthropic message history alongside the original task.

Use cases include coding assistants, office automation, mathematical questions, and multi-step tool workflows.

## Quick start

Get an API key from the [TierSense platform](https://tierflow.cn/tiersense), then call the official endpoint:

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

Recorded response for this question on September 22, 2026:

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

| Field | Range | Meaning |
| --- | --- | --- |
| feature_scores.domain1–domain5 | 0–2 each | Five feature difficulty scores |
| score | 0–10 | Overall calibrated difficulty |

The overall score uses internal weighting and calibration; it is not the direct sum of the five features or a probability of success.

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

### JavaScript (server-side)

```javascript
// Call from your server; keep the API key in an environment variable.
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
if (!response.ok) throw new Error("Scoring request failed");
const result = await response.json();
console.log(result);
```

## Integration flow

```text
User question → Save task
                    ↓
Current messages + task → TierSense-Score → Difficulty scores
                    ↓
           Agent calls its model
                    ↓
           Execute tools, update messages
                    └→ Score the next round
```

Capture the question at the agent's input boundary. Before every model call, send it as `task` with the current non-empty `messages` history:

```json
{
  "model": "TierSense",
  "task": "Fix the login race condition and add regression tests.",
  "messages": [
    {"role": "user", "content": "Fix the login race condition and add regression tests."},
    {"role": "assistant", "content": "Located the shared state; preparing regression tests."}
  ]
}
```

Keep scores in a separate record. Your agent continues using its original messages. The [usage guide](usage.en.md) includes Python integration and native tool-message examples.

## Documentation

- [Usage guide](usage.en.md): inputs, responses, Python calls, and agent integration.
- [中文使用指南](usage.md): 单问题评分、Agent 逐轮接入与工具消息示例.
- [TierSense-Compress](../../docs/compress/README.md): the companion project for history-compression decisions.

This module provides hosted API documentation and integration examples. Model weights and self-hosted inference server source code are not included.

---

## Join the community

<p align="center">
  <a href="https://tierflow.cn"><img src="../../assets/tierflow-logo.png" alt="TierFlow" width="240"></a>
</p>

<p align="center">From the TierFlow team · Open to discussion and collaboration</p>

Scan the QR code to join our discussion group.

<img src="../../assets/community-qr.png" alt="TierFlow official discussion group QR code and contact information" width="640">
