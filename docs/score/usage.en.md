# Usage guide

[English](usage.en.md) | [简体中文](usage.md) · [Home](README.md)

Updated: September 24, 2026.

Contents: [Endpoint](#1-endpoint-and-format) · [Question](#2-score-a-question) · [Agent integration](#3-integrate-with-an-agent) · [Protocols](#4-tool-message-formats) · [FAQ](#5-common-questions)

## 1. Endpoint and format

Get a key from the [TierSense platform](https://tierflow.cn/tiersense).

```text
POST https://tierflow.cn/tiersense/v1/score
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

| Field | Type | Purpose |
| --- | --- | --- |
| model | string | Set to TierSense |
| messages | string or message-object array | A complete question or current non-empty conversation |
| task | optional string | Original task captured at the agent's user-input boundary |

For the public endpoint, messages must be non-empty. Use a string for one question and an array for an agent's history.

## 2. Score a question

```bash
export TIERSENSE_API_KEY="YOUR_API_KEY"
curl "https://tierflow.cn/tiersense/v1/score" \
  -H "Authorization: Bearer ${TIERSENSE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"TierSense","messages":"Fix the CSV export and add regression tests."}'
```

Questions can describe mathematics, programming, document work, or other tasks.

| Response field | Range | Interpretation |
| --- | --- | --- |
| feature_scores.domain1–domain5 | 0–2 each | Five feature difficulty signals |
| score | 0–10 | Weighted and calibrated overall difficulty |

The score is not the direct sum of the feature values or a probability of task success. Wording, task domain, and execution state can affect it. See the README for a recorded response with its original input.

### Python

```bash
python3 -m pip install requests
```

```python
import os
import requests

SCORE_URL = "https://tierflow.cn/tiersense/v1/score"
API_KEY = os.environ["TIERSENSE_API_KEY"]


def score_difficulty(messages, *, task=None):
    body = {"model": "TierSense", "messages": messages}
    if task is not None:
        body["task"] = task
    response = requests.post(
        SCORE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=body,
        timeout=(10, 120),
    )
    response.raise_for_status()
    return response.json()


result = score_difficulty("Fix the CSV export and add regression tests.")
print(result["score"])
print(result["feature_scores"])
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

## 3. Integrate with an agent

Call TierSense immediately before each main-model request. Save the original question before the agent adds its framework instructions, then reuse it as task.

```python
# Reuse score_difficulty from the previous section.

def on_new_task(user_question, session):
    session["tiersense_task"] = user_question


def before_model_call(messages, session):
    scores = score_difficulty(
        messages,
        task=session["tiersense_task"],
    )
    print("Current difficulty:", scores["score"])
    print("Feature scores:", scores["feature_scores"])
    return scores


# Connect these functions to your existing agent:
# on_new_task(user_question, session)
# scores = before_model_call(messages, session)
# response = existing_model_call(messages=messages)
```

Keep task state per conversation. A subagent uses its own delegated task. Replace task when the user starts a new goal; incorporate important new constraints when the same task changes. A “continue” message or tool result does not replace the original goal.

Keep scores separately from the agent's messages. Your application can use them in its model-selection policy.

### Capture points

| Agent | Capture task from | Submit as messages |
| --- | --- | --- |
| CodeBuddy / CBC | Original user submission | Current Chat or Anthropic messages |
| Codex | Task submitted to the CLI / SDK | Responses items, including tool calls and outputs |
| Claude Code | User input; UserPromptSubmit.prompt when using that hook | Current Anthropic history |
| DeepSeek Harness | Original user input received by the harness | Current history, including native tool-call / toolCallId fields |
| OpenClaw | User-message entry point | Supported message records |
| Custom agent | Application input handler | Chat, Responses, or Anthropic history |

These are integration points: your code captures the task and submits the current snapshot. Protocol support does not imply that every version of every client has completed an end-to-end integration test.

### Without a saved task

Submit the full conversation starting with the user's original question. Known framework wrappers are handled during task extraction:

```json
{
  "model": "TierSense",
  "messages": [
    {
      "role": "user",
      "content": "<system-reminder>Framework reminder</system-reminder><user_query>Fix login and add tests.</user_query>"
    }
  ]
}
```

If no genuine task can be extracted, supply task explicitly. System and developer messages and recognized framework reminders are excluded from the scoring copy. Arbitrary instructions embedded in user text cannot always be identified as framework metadata; capturing task at entry makes the intended target explicit.

## 4. Tool-message formats

Preserve IDs connecting calls and results, especially when parallel tools share a name. Submit the history intended for the next model call. Internally, TierSense builds its scoring state from task and the two most recent steps.

### Chat: CodeBuddy and custom agents

```json
{
  "model": "TierSense",
  "task": "Fix the login race condition.",
  "messages": [
    {"role":"system","content":"You are a coding assistant."},
    {"role":"user","content":"Fix the login race condition."},
    {
      "role":"assistant",
      "content":"Reading the implementation.",
      "tool_calls":[
        {"id":"c1","type":"function","function":{"name":"Read","arguments":"{\"path\":\"app.py\"}"}}
      ]
    },
    {"role":"tool","tool_call_id":"c1","content":"def login(user): ..."}
  ]
}
```

### Responses: Codex

Put native items in messages:

```json
{
  "model":"TierSense",
  "task":"Inspect report.py and add tests.",
  "messages":[
    {"role":"user","content":"Inspect report.py and add tests."},
    {"type":"custom_tool_call","call_id":"c1","name":"exec","input":"read report.py"},
    {"type":"custom_tool_call_output","call_id":"c1","output":"def report(data): return {}"}
  ]
}
```

Function calls and their outputs also use call_id. Tool inputs are scoring evidence; TierSense does not execute them.

### Anthropic: Claude Code

```json
{
  "model":"TierSense",
  "task":"Inspect app.py for race conditions.",
  "messages":[
    {"role":"user","content":"Inspect app.py for race conditions."},
    {"role":"assistant","content":[{"type":"tool_use","id":"c1","name":"Read","input":{"path":"app.py"}}]},
    {"role":"user","content":[{"type":"tool_result","tool_use_id":"c1","content":"File contents...","is_error":false}]}
  ]
}
```

The final user message contains a tool result; it is not treated as a new user task. Preserve is_error when a tool fails.

### From an existing provider request

```python
# Reuse score_difficulty.

def score_provider_request(provider_request, task):
    if "messages" in provider_request:
        history = provider_request["messages"]
    else:
        history = provider_request["input"]
    return score_difficulty(history, task=task)
```

Use this with a request containing the full visible history. When Responses uses incremental input and previous_response_id, reconstruct the history from your application's saved messages before scoring. A response ID alone does not contain the conversation.

For streaming, assemble text and tool-argument deltas into complete messages, then append tool results. Submit message objects rather than raw SSE text, log paths, or strings describing “the current context.”

## 5. Common questions

**Does a standalone question require task?**

No. Send model and a non-empty messages string.

**Can I send only task?**

The public gateway requires non-empty messages. For the first agent round, include the original user message.

**Why 422 missing_task?**

The input lacks a task, for example it contains only tool results or “continue.” Provide task and the current non-empty history.

**Should I remove all system prompts myself?**

Submit the original message history. The API prepares a separate scoring copy and handles system/developer roles and recognized framework wrappers. Capture the original task before wrappers are added.

**How do I select a model?**

Use score as an input to your own policy. Calibrate thresholds on representative tasks for your model set; the API returns scores rather than choosing a model.

**Does this compress the context?**

This endpoint scores difficulty. For compression decisions, see [TierSense-Compress](../../docs/compress/README.md).
