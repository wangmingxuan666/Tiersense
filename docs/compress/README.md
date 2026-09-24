<p align="center">
  <a href="https://tierflow.cn/tiersense"><img src="../../assets/tiersense-logo.png" alt="TierSense" width="500"></a>
</p>

<h1 align="center">TierSense-Compress</h1>

<p align="center"><strong>Learn when to compress. Keep agents moving.</strong></p>
<p align="center">State-conditioned history compression for long-horizon agents.</p>

<p align="center">
  <a href="https://arxiv.org/abs/2609.27298"><img src="https://img.shields.io/badge/arXiv-2609.27298-b31b1b" alt="arXiv 2609.27298"></a>
  <a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="usage.en.md"><img src="https://img.shields.io/badge/Docs-Usage_Guide-0969da" alt="Usage guide"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#features">Features</a> ·
  <a href="method.en.md">Method</a> ·
  <a href="usage.en.md">Agent Integration</a> ·
  <a href="https://arxiv.org/pdf/2609.27298">Paper PDF</a> ·
  <a href="#join-the-community">Community</a>
</p>

<p align="center"><strong><a href="README.md">English</a></strong> · <a href="README.zh-CN.md">简体中文</a></p>

<p align="center"><strong>StateComp: Learning When to Compress History in Long Horizon Agents</strong></p>

---

> **[TierSense hub](../../README.md)** · [Score](../../docs/score/README.md) · [Compress](../../docs/compress/README.md) · [Memory-Decide](../../docs/memory-decide/README.md)
>
> Authors' statements and research timeline material are maintained centrally: [Read the statements](../../AUTHORS_STATEMENT.en.md).

## About the project

**Help agents decide which historical steps are ready for compression.**

TierSense-Compress takes the current context of a conversational or tool-using agent and returns per-step compression recommendations and continuous spans that satisfy your execution policy. Your application generates summaries and passes the updated context back to the main agent.

It separates **compression decisions** from **summary generation**, so you can choose your main model, summarizer, and compression frequency independently.

## Features

- **Per-step decisions:** `should_compress` and `confidence` for visible assistant steps.
- **Tool-aware grouping:** an assistant message and its associated tool results form one step.
- **Continuous-span selection:** configure check intervals, step counts, token thresholds, and confidence thresholds.
- **Exact indexing:** `message_indices` refer to the message array submitted in the request.
- **Mid-task integration:** submit the current context, optionally with an explicit `task`.
- **Your choice of summarizer:** the API selects spans; your application summarizes and updates the conversation.

Use cases include coding assistants, office automation, multi-turn conversations, and long-running tool-based tasks.

## Quick start

Get an API key from the [TierSense platform](https://tierflow.cn/tiersense), then call:

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
      {"role": "user", "content": "Calculate 17+28, then multiply by 2."},
      {"role": "assistant", "content": "17+28=45."},
      {"role": "user", "content": "Continue."}
    ]
  }'
```

Read the returned `steps`:

| Field | Meaning |
| --- | --- |
| should_compress | `true`: recommend compression; `false`: recommend keeping the original |
| confidence | Support for the predicted decision, from 0 to 1 |
| message_indices | Zero-based positions in the submitted message array |

This example has one historical step. Whether to compress it depends on the actual response.

## Integration flow

```text
Current context → TierSense-Compress → Selected spans
                                          ↓
Next model call ← Updated context ← Application-generated summaries
```

To enable a batch execution policy, add:

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

This checks every visible historical step and selects only compression recommendations meeting the confidence threshold. A continuous span must contain **at least 4 eligible steps** and **more than 2,000 tokens**. Process spans with `trigger_compression=true` in `execution.spans`.

## Method overview

![StateComp framework](../../assets/statecomp-framework.png)

[View the original framework PDF](../../assets/statecomp-framework.pdf)

The model encodes a compact state built from the original task and the two most recent steps. BM25 selects up to three earlier history blocks. Cached hidden vectors and late interaction produce a state representation, and a pairwise classifier compares historical states with the current state.

This is in-context compression selection, not external-memory retrieval. Summaries are generated by your application and retained in its current conversation.

## Documentation

- [Method](method.en.md): state construction, history selection, classification, and execution policy.
- [Usage guide](usage.en.md): request format, options, responses, Python integration, and examples.

This module provides method documentation and hosted API integration examples. It does not include model weights or self-hosted inference server source code.

---


### Join the community

<p align="center">
  <a href="https://tierflow.cn"><img src="../../assets/tierflow-logo.png" alt="TierFlow" width="240"></a>
</p>

<p align="center">From the TierFlow team · Open to discussion and collaboration</p>

Scan the QR code to join our discussion group. For the detailed research timeline, please contact the account holder directly.

<img src="../../assets/community-qr.png" alt="TierFlow official discussion group QR code and contact information" width="640">
