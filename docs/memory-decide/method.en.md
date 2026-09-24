# Scope and integration responsibilities

[English](method.en.md) | [简体中文](method.md) · [Home](README.md) · [Usage guide](usage.en.md)

## Separate decisions from execution

Provide the original task and current messages to obtain compression and recall recommendations for the current moment. Both may be positive or negative independently.

| Stage | TierSense-Memory-Decide | Your agent |
| --- | --- | --- |
| Original task | Accept task; support recognized task extraction | Capture and pass the original question |
| Current context | Accept messages and completed tool results | Supply real, complete, ordered history |
| Whether to compress / recall | Return predicted and confidence | Check that eligible history / memory exists |
| History selection and summaries | No execution or selected indices | Select complete blocks and generate summaries |
| Memory retrieval and injection | No retrieval or retrieved text | Store, retrieve, deduplicate, and inject information |
| Continue the task | No main-agent model call | Pass the actual updated context to the main model |

## Difference from TierSense-Compress

[TierSense-Compress](../../docs/compress/README.md) provides per-step compression recommendations and history-span selection. This API provides two current-time memory decisions. Do not assume its options, steps, or execution.spans are available here.

## Integration principles

- Call only after all tool results are available; preserve tool pairing.
- Pass task explicitly to retain the original question when joining mid-task.
- Check execution preconditions; skip operations without eligible history or stored memory.
- Commit context changes only after successful execution; preserve context on failure.
- Confidence supports the decision; it is not task success probability.
- Agent examples describe supported formats, not a claim of complete end-to-end acceptance for every version.

This page covers public product behavior and integration responsibilities, not internal training or inference implementation.
