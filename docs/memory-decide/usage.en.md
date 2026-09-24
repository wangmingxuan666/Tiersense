# Usage guide

[English](usage.en.md) | [简体中文](usage.md) · [Home](README.md) · [Scope](method.en.md)

Pass the original user task and the agent's current context to receive two recommendations: **whether to compress history and whether to recall historical information**, each with its own confidence.

The API only makes decisions. It does not generate summaries, perform retrieval, modify context, or return compression scores for individual historical steps.

## 1. Quick start

```text
POST https://tierflow.cn/tiersense/v1/memory/decide
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get a key from the [TierSense platform](https://tierflow.cn/tiersense).

```bash
curl 'https://tierflow.cn/tiersense/v1/memory/decide' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "TierSense",
    "task": "Check the demo_report tests and explain failures.",
    "messages": [
      {"role": "user", "content": "Check the demo_report tests and explain failures."},
      {"role": "assistant", "content": "Read the test files; reviewing the failing cases."}
    ]
  }'
```

All tasks, projects, and tool results below are fictional format examples, not fixed prediction results.

## 2. Request fields

| Field | Type | Description |
| --- | --- | --- |
| model | string | Use `TierSense` |
| task | string; recommended on every call | Original user question for this task |
| messages | message-object array or string; required | Complete, ordered context currently used by the agent |
| system | optional string or supported text-block array | For formats with system instructions outside messages |

### Capture the original task once

Save the user's question **before passing it to the agent**, then automatically include that text as `task` on subsequent requests. Users do not need to type it twice.

If task is omitted, supported original user messages or recognized CodeBuddy `user_query` wrappers can supply it. If the original question is no longer present or cannot be resolved, explicitly supply task. Do not replace it with assistant output, tool results, or a later “continue”.

### Send the current context

Include user follow-ups, assistant messages, completed tool calls, and corresponding results. Keep any summaries or recalled information already present in the agent's actual context.

- Tool calls and results must be paired. Wait for all parallel results.
- Do not send streaming deltas, partial messages, or unfinished tool calls.
- Standard roles include `system`, `developer`, `user`, `assistant`, and `tool`.
- Standard `function.arguments` is a valid JSON string representing an object. Match `tool_call_id` to the call's `id`.
- You do not need to remove supported developer messages manually.

Plain text can be sent as a string:

```json
{
  "model": "TierSense",
  "task": "Organize meeting action items.",
  "messages": "Three action items are recorded. The procurement owner remains unconfirmed; review the meeting notes next."
}
```

Prefer an object array for multi-turn history and tools. Do not use `"messages": ["one large transcript"]`.

## 3. Four agent input examples

These are supported message-format examples, not agent SDKs or automatic plugins. Replace them with your real task and completed messages; never fabricate tool results.

### CodeBuddy / WorkBuddy: standard tool messages

```json
{
  "model": "TierSense",
  "task": "Check the demo_report tests and explain failures.",
  "messages": [
    {"role": "user", "content": "Check the demo_report tests and explain failures."},
    {
      "role": "assistant",
      "content": "Run the existing tests first.",
      "tool_calls": [
        {"id": "cb_demo_1", "type": "function", "function": {"name": "Bash", "arguments": "{\"command\":\"pytest demo_report/tests -q\"}"}}
      ]
    },
    {"role": "tool", "tool_call_id": "cb_demo_1", "content": "1 failed, 8 passed"}
  ]
}
```

### Codex: completed Responses messages and tool items

```json
{
  "model": "TierSense",
  "task": "Check the demo_report tests and explain failures.",
  "messages": [
    {"role": "developer", "content": "Inspect existing tests; do not change unrelated files."},
    {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "Check the demo_report tests and explain failures."}]},
    {"type": "function_call", "call_id": "cx_demo_1", "name": "exec_command", "arguments": "{\"cmd\":\"pytest demo_report/tests -q\"}"},
    {"type": "function_call_output", "call_id": "cx_demo_1", "output": "1 failed, 8 passed"}
  ]
}
```

Send complete messages or completed items, not individual raw streaming events.

### Claude Code: tool_use and tool_result

```json
{
  "model": "TierSense",
  "task": "Check the demo_report tests and explain failures.",
  "system": "You are a coding assistant.",
  "messages": [
    {"role": "user", "content": "Check the demo_report tests and explain failures."},
    {"role": "assistant", "content": [
      {"type": "text", "text": "Run the existing tests first."},
      {"type": "tool_use", "id": "cl_demo_1", "name": "Bash", "input": {"command": "pytest demo_report/tests -q"}}
    ]},
    {"role": "user", "content": [
      {"type": "tool_result", "tool_use_id": "cl_demo_1", "content": "1 failed, 8 passed", "is_error": true}
    ]}
  ]
}
```

### DeepSeek Harness: assembled tool messages

```json
{
  "model": "TierSense",
  "task": "Check the demo_report tests and explain failures.",
  "messages": [
    {"role": "user", "content": [{"type": "text", "text": "Check the demo_report tests and explain failures."}]},
    {"role": "assistant", "content": [{"type": "tool-call", "id": "ds_demo_1", "name": "bash", "arguments": "{\"command\":\"pytest demo_report/tests -q\"}"}]},
    {"role": "tool", "toolCallId": "ds_demo_1", "isError": true, "content": [{"type": "text", "text": "1 failed, 8 passed"}]}
  ]
}
```

Other agents may use supported standard message formats. This is not a guarantee of compatibility with every agent version or every multimodal or event type.

## 4. Reading the response

```json
{
  "compression": {"predicted": true, "confidence": 0.8, "positive_votes": 4},
  "recall": {"predicted": false, "confidence": 0.6, "positive_votes": 2},
  "confidence_type": "ensemble_agreement"
}
```

| Business field | Meaning |
| --- | --- |
| compression.predicted | true: consider compressing history; false: not recommended now |
| recall.predicted | true: consider recalling history; false: not recommended now |
| confidence | Support for that final decision, from 0 to 1; not a calibrated correctness probability |

`predicted: false, confidence: 0.8` supports **not** performing the operation. It does not mean an 80% probability of needing compression. Read predicted directly rather than applying another yes/no threshold to confidence.

`positive_votes` and `confidence_type` are compatibility metadata. Application logic only needs predicted and confidence.

A positive compression decision does not mean a summary has been generated. A positive recall decision does not mean content has been found. Responses contain no per-step scores, summaries, or retrieved text.

## 5. Python integration

Install `requests`, then set the `TIERSENSE_API_KEY` environment variable:

```python
import os
import requests

URL = "https://tierflow.cn/tiersense/v1/memory/decide"
API_KEY = os.environ["TIERSENSE_API_KEY"]

def decide_memory(task, messages):
    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "TierSense", "task": task, "messages": messages},
        timeout=(10, 120),
    )
    response.raise_for_status()
    return response.json()

question = "Check the demo_report tests and explain failures."
messages = [
    {"role": "user", "content": question},
    {"role": "assistant", "content": "Read the test files; reviewing failing cases."},
]
result = decide_memory(question, messages)
print("Compress:", result["compression"]["predicted"])
print("Recall:", result["recall"]["predicted"])
```

### JavaScript (server-side)

Keep the API key in the server-side TIERSENSE_API_KEY environment variable, not browser code. This example uses a server-side JavaScript runtime with fetch.

```javascript
const response = await fetch(
  "https://tierflow.cn/tiersense/v1/memory/decide",
  {
    method: "POST",
    headers: {
      Authorization: "Bearer " + process.env.TIERSENSE_API_KEY,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "TierSense",
      task: "Check the demo_report tests and explain failures.",
      messages: [
        {role: "user", content: "Check the demo_report tests and explain failures."},
        {role: "assistant", content: "Read the test files; reviewing the failing cases."}
      ]
    })
  }
);
if (!response.ok) throw new Error(`Memory decision failed: HTTP ${response.status}`);
const result = await response.json();
console.log(result);
```

## 6. Where it fits in an agent

Call **after the current tool results are complete and before the next main-model request**.

```text
User submits question → integration saves task → agent proceeds
Before the next main-model request:
    Obtain complete current messages with paired tool calls/results
    If neither eligible old history nor stored memory exists: continue
    Otherwise call TierSense(task, messages)
        Success: combine predicted with execution preconditions
        Failure: keep context, record the error, do not fabricate “false”
    Pass the resulting actual messages to the main model
```

Only compress when eligible old history exists. Only recall when memory has actually been stored. Even a positive decision cannot authorize an operation on nonexistent data.

Your application implements history selection, summarization, retrieval, and deduplication. Preserve original context on execution failure and keep tool call/result pairs intact. If both decisions are positive, choose an execution order appropriate for your workflow and avoid undoing one operation with the other.

## 7. Common integration questions

| Situation | What to do |
| --- | --- |
| Joining mid-task; original question is absent | Pass the saved original question as task |
| Empty or unresolvable task | Supply task explicitly; do not use assistant output |
| Malformed input / HTTP 422 | Check messages, content types, and tool pairing; the gateway may simplify error details |
| HTTP 401 / 403 | Check the platform key and access authorization |
| Timeout or server error | Preserve context and record the failure; do not treat it as a negative decision |
| Requesting selected history indices | This API does not return them; implement selection in the application |
| No history yet, but positive compression | Do not execute compression without eligible history |

These examples document the public contract. They are not a new benchmark result or a guarantee that every task will benefit.
