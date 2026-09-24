<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="../../assets/tiersense-logo.png" alt="TierSense" width="500"></a>
</p>

<h1 align="center">TierSense-Memory-Decide</h1>

<p align="center"><strong>Learn when to compress and recall. Keep agents moving.</strong></p>
<p align="center">Context-aware memory decisions for long-horizon agents.</p>

<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="https://arxiv.org/abs/2609.27286"><img src="https://img.shields.io/badge/arXiv-2609.27286-b31b1b" alt="arXiv 2609.27286"></a>
  <a href="https://arxiv.org/pdf/2609.27286"><img src="https://img.shields.io/badge/Paper-Memory_Control-b31b1b" alt="Memory Control PDF"></a>
  <a href="usage.en.md"><img src="https://img.shields.io/badge/Docs-Usage_Guide-0969da" alt="Usage guide"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#features">Features</a> ·
  <a href="method.en.md">Scope</a> ·
  <a href="usage.en.md">Agent Integration</a> ·
  <a href="#join-the-community">Community</a>
</p>

<p align="center"><strong><a href="README.md">English</a></strong> · <a href="README.zh-CN.md">简体中文</a></p>

---

> **[TierSense hub](../../README.md)** · [Score](../../docs/score/README.md) · [Compress](../../docs/compress/README.md) · [Memory-Decide](../../docs/memory-decide/README.md)
>
> Authors' statements and research timeline material are maintained centrally: [Read the statements](../../AUTHORS_STATEMENT.en.md).

## About the project

**Help agents decide whether to compress history or recall historical information now.**

TierSense-Memory-Decide takes the original user task and the agent's current context, and returns two recommendations with their respective confidence values. Your application uses its own summarization and retrieval modules to act on these recommendations and continue the task.

It separates **memory decisions** from **memory execution**, without tying your application to a main model, summarizer, or memory store.

## Features

- **Two decisions:** compression and recall recommendations in one response.
- **Explicit outputs:** `predicted` and `confidence` for each decision.
- **Context integration:** submit complete, ordered messages, including completed tool calls and results.
- **Explicit task:** capture the original user question once and pass it as `task` on subsequent requests.
- **Multiple message formats:** examples for CodeBuddy / WorkBuddy, Codex, Claude Code, and DeepSeek Harness.
- **Application-owned execution:** choose history, generate summaries, retrieve memories, and update context in your own agent.

Use cases include coding assistants, office automation, multi-turn conversations, and long-running tool tasks. Message-format support does not mean an automatic integration plugin is available for every agent version.

## Quick start

Get an API key from the [TierSense platform](https://tierflow.cn/tiersense). Current endpoint:

```text
POST https://tierflow.cn/tiersense/v1/memory/decide
```

```bash
curl "https://tierflow.cn/tiersense/v1/memory/decide" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TierSense",
    "task": "Check the demo_report tests and explain failures.",
    "messages": [
      {"role": "user", "content": "Check the demo_report tests and explain failures."},
      {"role": "assistant", "content": "Read the test files; reviewing the failing cases."}
    ]
  }'
```

Example response shape, not a promised result for the input above:

```json
{
  "compression": {"predicted": true, "confidence": 0.8, "positive_votes": 4},
  "recall": {"predicted": false, "confidence": 0.6, "positive_votes": 2},
  "confidence_type": "ensemble_agreement"
}
```

| Field | Meaning |
| --- | --- |
| compression.predicted | Whether to consider compressing history |
| recall.predicted | Whether to consider recalling historical information |
| confidence | Support for the final decision, from 0 to 1; not a calibrated correctness probability |

Read `predicted` directly. Do not turn confidence into another yes/no classifier: `false + 0.8` supports the negative decision. Other response fields are compatibility metadata and are not required by application logic.

## Integration flow

```text
Original task + current context → TierSense-Memory-Decide
                                          ↓
                              Compression + recall decisions
                                          ↓
Next model call ← Updated context ← Application summary / retrieval modules
```

Call after all tool results have arrived and before the next main-model request. Do not execute compression without eligible history or recall without stored memory. On failure, preserve context and do not fabricate a negative decision.

## Scope

The API decides **whether now is an appropriate time**. It does not return per-step scores, selected steps, message indices, summaries, or retrieved text, and it does not modify your conversation.

For per-step compression recommendations and history-span selection, see [TierSense-Compress](../../docs/compress/README.md). The contracts differ: do not reuse its `steps`, `execution.spans`, or span-selection options here.

## Paper

[Memory Control Signals Emerge Before Action in Long Horizon Agents](https://arxiv.org/pdf/2609.27286)

Read or download the full author-provided PDF (35 pages). The research system described in the paper and the hosted decision API have different scopes; see the usage guide for the API contract.

## Documentation

- [Scope and integration responsibilities](method.en.md): what the API does and what your application implements.
- [Usage guide](usage.en.md): request formats, four agent examples, Python calls, and integration.

This module provides hosted API documentation and integration examples. It does not include model weights or self-hosted inference server source code.

---


## Join the community

<p align="center">
  <a href="https://tierflow.cn"><img src="../../assets/tierflow-logo.png" alt="TierFlow" width="240"></a>
</p>

<p align="center">From the TierFlow team · Open to discussion and collaboration</p>

Scan the QR code to join our discussion group and exchange ideas about agent integration and memory management.

<img src="../../assets/community-qr.png" alt="TierFlow official discussion group QR code and contact information" width="640">
