# Agent integration

[简体中文](agent-integration.md) · [Home](../README.md)

## Start with independent modules

The three modules are not a mandatory pipeline. Use the one that matches your needs. Your application owns the main agent, summarizer, and memory store. Capture the original task and pass it with real messages where supported.

## Optional composition

```text
All current tool results arrive
        ↓
Complete current context + original task
        ↓
Memory-Decide: compress / recall now? (optional)
        ├─ Compression → Compress selects candidates → Application summarizes
        └─ Recall → Application retrieves stored memory → Deduplicates and injects
        ↓
Score: assess the context about to reach the main model (optional)
        ↓
Application routing policy selects model → Agent continues
```

This is an integration suggestion, not a claim of unified end-to-end evaluation or guaranteed quality/cost improvement. Do not call all three APIs every round merely to use the entire suite.

## Application responsibilities

- Wait for all tool results and preserve call/result pairing.
- Verify that eligible history or stored memories exist before execution.
- A positive Memory-Decide compression result does not guarantee Compress will select a span; preserve history when no candidate is available.
- Retain traceable originals according to your memory policy; commit replacement only after successful summarization.
- Deduplicate recall content and choose an appropriate order if both decisions are positive.
- Define your own score thresholds and model mapping.
- Preserve context and record failures; do not fabricate successful or negative results.
- Do not transfer one endpoint's confidence semantics or execution options to another.

This hub does not change existing endpoints, authentication, or response formats. It adds no unified API or automatic execution plugin.
