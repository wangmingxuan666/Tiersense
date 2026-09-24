# Method

[English](method.en.md) | [简体中文](method.md) · [Home](README.md) · [Usage guide](usage.en.md)

## 1. Objective

![StateComp framework](../../assets/statecomp-framework.png)

[View the original framework PDF](../../assets/statecomp-framework.pdf)

Before the agent's next generation, identify which visible historical steps are suitable for replacement with summaries.

A step consists of one assistant message and all associated tool results. System, developer, and user messages are not replacement candidates. Existing summaries can participate in subsequent scoring as visible steps.

TierSense-Compress returns recommendations and candidate spans. It does not generate summaries or modify the caller's conversation.

## 2. Task and message parsing

A non-empty explicit `task` takes precedence. Otherwise, the extraction layer obtains the task from supported original user inputs or the initial task block in the visible context, including recognized CodeBuddy `user_query` wrappers. If no task is available, the caller must provide `task`; assistant output is not substituted for the user's question.

Framework-specific histories should first be converted to role/content/tool_calls/tool_call_id messages while retaining an index mapping. Extracting the task from an original submission event and converting the current history are separate operations.

Later user requirements remain in the main agent's context. The current scoring template does not create a separate section for every later user update and should not be understood as a lossless encoding of the entire context.

## 3. State representation

### Compact main input

The original scoring template contains:

| Section | Content |
| --- | --- |
| Original Task | Original task, whitespace-normalized and limited to 1,500 characters |
| Previous Input | The second-most-recent assistant block and its tool information |
| Previous Output | Most recent assistant text, up to 1,500 characters |
| Previous Tool Calls | Most recent tool calls, up to 500 characters per arguments field |
| Previous Tool Results | Most recent tool results, up to 800 characters each |

The text portion of Previous Input is limited to 1,500 characters. After applying the chat template, the main input uses at most the first 4,096 tokens. This is a per-feature-extraction budget, not the total HTTP request size or summary output limit.

### Hidden vectors and earlier history

The current method uses a frozen **Qwen2.5-7B-Instruct** backbone. Mean pooling over token hidden states from layer 21 produces a 3,584-dimensional vector.

1. Split assistant messages and tool results into history blocks.
2. Exclude the two most recent blocks from the BM25 candidate pool.
3. Use the last history block as the query and retrieve up to three earlier blocks.
4. Encode each selected block; for blocks exceeding 4,096 tokens, use the first 2,048 and last 2,048 tokens.
5. Feed the hidden vectors and relevance, rank, and step-distance metadata to the state encoder.

BM25 Top3 is internal feature selection. It does not append retrieved text to the main agent, and it does not restrict compression decisions to those three blocks. Excluding the two most recent blocks from retrieval does not force the API to retain those steps.

### Late interaction

The main vector and block vectors are projected separately to 256 dimensions. Similarity-weighted pooling, element-wise interactions, and difference features are aggregated into a 512-dimensional state representation. This is block-level vector interaction, not exhaustive token-to-token interaction.

Hidden vectors and state representations can be cached. The cache reduces repeated computation; it is not an external conversation memory and cannot recover history deleted by the caller. A request may encode multiple historical prefixes rather than require just one forward pass.

## 4. Historical–current state pairing

For visible historical step i:

```text
m_i = State of the visible prefix before step i was generated
q_k = State of the current visible context
p_i = sigmoid(PairClassifier(m_i, q_k, m_i × q_k, |m_i − q_k|))
```

The classifier compares historical and current states to recommend summarization. Prefixes are reconstructed from the messages visible in this request; original history already replaced with summaries is not recovered.

The current internal decision threshold is 0.73. The public per-step fields are primarily `should_compress` and `confidence`. Confidence is support for the predicted class, not a guaranteed correctness probability. The caller's `options.confidence_threshold` filters recommendations without changing the internal classification threshold.

The lightweight network is trained with a combination of classification loss, supervised contrastive learning, and full-context teacher distillation. The backbone remains frozen for feature extraction. Effectiveness should be evaluated with the actual task, summarizer, and context replacement strategy.

## 5. From recommendation to execution

The execution policy follows this order:

```text
Check interval → Compression/confidence filtering → Continuous spans
               → Per-span step and token thresholds → Executable spans
```

When span and min_tokens are both set, each span must satisfy both:

```text
step_count > span AND token_count > min_tokens
```

Keep recommendations, insufficient-confidence steps, and user/system/developer messages separate spans. A tool step with a user message interleaved between its call and result is retained rather than included in an executable span.

Counts are not combined across separate spans. `span` is a minimum continuous-length threshold, not a maximum batch size.

## 6. Summarization and continuation

Using the same context snapshot, the caller extracts each executable span by `message_indices`, generates a summary, and updates the conversation. The summary model, content format, and storage location are chosen by the caller.

One simple strategy is in-place replacement: insert an assistant summary at the first selected message and remove only messages identified by the returned indices. Preserve user requirements and system constraints, and keep tool calls paired with their results. Save the updated history and use it for both the next main-model request and the next compression request.

Distinguish three stages: **the model recommends compression; a span satisfies execution conditions; a summary is generated and committed**. A successful API response does not mean that a summary has already been generated or that the task is complete.
