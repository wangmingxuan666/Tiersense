# TierSense 压缩与召回 API 用户使用指南

[English](usage.en.md) | [简体中文](usage.md) · [返回首页](README.zh-CN.md) · [功能边界](method.md)

将用户的原始任务和 Agent 当前上下文传给 TierSense，获得两项建议：**现在是否需要压缩历史、是否需要召回历史信息**，以及各自的置信度。

接口只提供判断，不生成摘要、不执行检索、不修改上下文，也不返回每个历史步骤的压缩分数。是否执行及如何执行，由接入方的 Agent 决定。

## 1. 快速调用

```text
POST https://tierflow.cn/tiersense/v1/memory/decide
```

将 `YOUR_API_KEY` 换成平台提供的调用 Key：

```bash
curl 'https://tierflow.cn/tiersense/v1/memory/decide' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "TierSense",
    "task": "检查 demo_report 项目的测试，说明失败原因。",
    "messages": [
      {"role": "user", "content": "检查 demo_report 项目的测试，说明失败原因。"},
      {"role": "assistant", "content": "已阅读测试文件，正在核对失败用例。"}
    ]
  }'
```

本指南的任务、项目名和工具结果均为虚构的格式示例，不代表固定的判断结果。

## 2. 请求需要哪些字段

| 字段 | 格式 | 说明 |
| --- | --- | --- |
| `model` | 字符串 | 填写 `TierSense` |
| `task` | 字符串，推荐每次明确提供 | 本次任务的原始用户问题 |
| `messages` | 消息对象数组或字符串，必需 | Agent 当前实际使用的完整、有序上下文 |

### messages：传入当前上下文

传入本轮准备交给主模型的消息历史，包括用户补充、助手消息、工具调用及对应结果。已有摘要或召回信息，也应保留在当前实际上下文中。

- 工具调用与结果必须完整配对；并行工具应等本轮结果收齐后再调用。
- 不传流式增量、半条消息或尚未完成的工具调用。
- 标准消息可包含 `system`、`developer`、`user`、`assistant`、`tool`。
- 标准工具调用的 `function.arguments` 是表示 JSON 对象的合法 JSON 字符串；`tool_call_id` 对应调用的 `id`。
- 不需要为接入本接口而手工删除已支持的 `developer` 消息。

纯文本上下文也可以直接传字符串：

```json
{
  "model": "TierSense",
  "task": "整理会议待办。",
  "messages": "已整理三个待办，其中采购负责人尚未确认，接下来核对会议记录。"
}
```

有多轮历史或工具调用时，推荐消息对象数组，以保留消息边界。不要写成 `"messages": ["一整段历史"]`。

## 3. 四种 Agent 的输入示例

这些示例展示可接入的消息格式，不是各 Agent 的 SDK。实际使用时，替换为自己的原始任务和已完成消息，不要伪造工具结果。

### CodeBuddy / WorkBuddy：标准工具消息

```json
{
  "model": "TierSense",
  "task": "检查 demo_report 项目的测试，说明失败原因。",
  "messages": [
    {"role": "user", "content": "检查 demo_report 项目的测试，说明失败原因。"},
    {
      "role": "assistant",
      "content": "先运行现有测试。",
      "tool_calls": [
        {"id": "cb_demo_1", "type": "function", "function": {"name": "Bash", "arguments": "{\"command\":\"pytest demo_report/tests -q\"}"}}
      ]
    },
    {"role": "tool", "tool_call_id": "cb_demo_1", "content": "1 failed, 8 passed"}
  ]
}
```

### Codex：已完成的 Responses 消息和工具条目

```json
{
  "model": "TierSense",
  "task": "检查 demo_report 项目的测试，说明失败原因。",
  "messages": [
    {"role": "developer", "content": "先检查现有测试，不修改无关文件。"},
    {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "检查 demo_report 项目的测试，说明失败原因。"}]},
    {"type": "function_call", "call_id": "cx_demo_1", "name": "exec_command", "arguments": "{\"cmd\":\"pytest demo_report/tests -q\"}"},
    {"type": "function_call_output", "call_id": "cx_demo_1", "output": "1 failed, 8 passed"}
  ]
}
```

应传完整消息或已完成条目，而不是把原始流式事件逐条直接转发。

### Claude Code：tool_use 与 tool_result

```json
{
  "model": "TierSense",
  "task": "检查 demo_report 项目的测试，说明失败原因。",
  "system": "你是代码助手。",
  "messages": [
    {"role": "user", "content": "检查 demo_report 项目的测试，说明失败原因。"},
    {
      "role": "assistant",
      "content": [
        {"type": "text", "text": "先运行现有测试。"},
        {"type": "tool_use", "id": "cl_demo_1", "name": "Bash", "input": {"command": "pytest demo_report/tests -q"}}
      ]
    },
    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "cl_demo_1", "content": "1 failed, 8 passed", "is_error": true}]}
  ]
}
```

`system` 是可选字段，供系统消息位于消息数组之外的输入使用。

### DeepSeek Harness：组装完成的工具消息

```json
{
  "model": "TierSense",
  "task": "检查 demo_report 项目的测试，说明失败原因。",
  "messages": [
    {"role": "user", "content": [{"type": "text", "text": "检查 demo_report 项目的测试，说明失败原因。"}]},
    {"role": "assistant", "content": [{"type": "tool-call", "id": "ds_demo_1", "name": "bash", "arguments": "{\"command\":\"pytest demo_report/tests -q\"}"}]},
    {"role": "tool", "toolCallId": "ds_demo_1", "isError": true, "content": [{"type": "text", "text": "1 failed, 8 passed"}]}
  ]
}
```

其他 Agent 也可使用受支持的标准消息格式。

## 4. 如何理解返回结果

```json
{
  "compression": {"predicted": true, "confidence": 0.8, "positive_votes": 4},
  "recall": {"predicted": false, "confidence": 0.6, "positive_votes": 2},
  "confidence_type": "ensemble_agreement"
}
```

| 业务字段 | 含义 |
| --- | --- |
| `compression.predicted` | `true`：建议考虑压缩历史；`false`：当前不建议 |
| `recall.predicted` | `true`：建议考虑召回历史信息；`false`：当前不建议 |
| 两项结果中的 `confidence` | 对该项最终判断的置信度，范围 0–1；不是经过校准的正确概率 |

例如 `predicted: false, confidence: 0.8` 表示对“否”这一判断的置信度为 0.8，不是“有 80% 概率需要压缩”。不要对 `confidence` 再做一次正反判断，应直接读取 `predicted`。

`positive_votes`、`confidence_type` 是兼容附加字段。业务逻辑只需依赖 `predicted` 和 `confidence`，无需解析附加字段。

“建议压缩”不代表服务已经生成摘要；“建议召回”也不代表服务已经找到内容。返回结果不包含逐步分数、摘要或检索文本。

## 5. Python 接入示例

安装 `requests` 后，将调用 Key 保存在环境变量 `TIERSENSE_API_KEY` 中：

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

question = "检查 demo_report 项目的测试，说明失败原因。"
messages = [
    {"role": "user", "content": question},
    {"role": "assistant", "content": "已读取测试文件，正在核对失败用例。"},
]
result = decide_memory(question, messages)
print("压缩建议：", result["compression"]["predicted"])
print("召回建议：", result["recall"]["predicted"])
```

### JavaScript（服务端）

将 API Key 保存在服务端环境变量 `TIERSENSE_API_KEY` 中，不放进浏览器前端代码。以下代码适用于支持 fetch 的服务端 JavaScript 环境。

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
      task: "检查 demo_report 项目的测试，说明失败原因。",
      messages: [
        {role: "user", content: "检查 demo_report 项目的测试，说明失败原因。"},
        {role: "assistant", content: "已阅读测试文件，正在核对失败用例。"}
      ]
    })
  }
);
if (!response.ok) throw new Error(`Memory decision failed: HTTP ${response.status}`);
const result = await response.json();
console.log(result);
```

## 6. 放在 Agent 的哪个位置

推荐在**本轮工具结果收齐后、下一次主模型请求前**调用。接入流程如下：

```text
用户提交问题 → 接入代码保存 task → Agent 正常执行
准备下一次主模型请求：
    获取当前完整 messages，确认工具调用与结果已配对
    若既没有可压缩旧历史，也没有可召回记忆：直接继续
    否则调用 TierSense(task, messages)
        请求成功：按 predicted 和业务条件决定是否执行
        请求失败：保留当前上下文，记录失败，不伪造“否”结果
    将执行后的真实 messages 交给主模型，继续任务
```

只有确实存在可压缩旧历史时才执行压缩；只有确实保存了可召回信息时才执行召回。没有历史或记忆时，即使返回“是”，也不能执行不存在的操作。

摘要生成、历史选择、检索与去重由应用实现。执行失败时保留原上下文；不要拆散工具调用与结果。两项都为“是”时，由业务决定顺序，避免操作互相抵消。

## 7. task 获取与常见问题

首选在用户问题进入 Agent 前保存原始 question，之后由接入代码自动作为 `task` 传入，用户无需重复输入。不提供 task 时，可从支持的原始 user 文本或已识别的 CodeBuddy `user_query` 包装中提取；中途接入、原问题已不在历史中或提取失败时，请明确提供 task，不拿 assistant 输出、工具结果或后续“继续”冒充原任务。

| 情况 | 处理方式 |
| --- | --- |
| 中途接入，原问题已不可见 | 通过 task 提供保存的原始问题 |
| task 为空或无法解析 | 明确提供 task，不使用助手输出替代 |
| 输入格式错误／HTTP 422 | 检查消息格式、内容类型和工具配对；网关可能简化错误详情 |
| HTTP 401／403 | 检查平台 Key 和访问权限 |
| 超时或服务错误 | 保留上下文、记录失败，不把错误转成“否” |
| 想获得历史消息索引 | 本接口不返回索引，历史选择由应用实现 |
| 没有历史却返回压缩建议 | 没有可压缩旧历史时不执行 |

其他 Agent 可使用受支持的标准消息格式，但这不保证任意 Agent 版本、任意多模态或事件类型均可直接接入。示例是公开接口用法，不是新增跑分结果，也不保证每项任务均能受益。
