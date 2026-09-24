# 使用指南

[English](usage.en.md) | [简体中文](usage.md) · [首页](README.zh-CN.md)

更新日期：2026-09-24。

输入一个完整问题，或 Agent 的当前消息历史，获得五路难度分数和一个综合分数。你可以得到任务难度，也可以在 Agent 每次调用模型前读取本轮分数。

两种使用方式：直接评估一个问题与在 Agent 中逐轮评估。

## 1. 请求地址与格式

请求地址：

```text
POST https://tierflow.cn/tiersense/v1/score
```

请求头：

```text
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

| 字段 | 类型 | 怎么填写 |
|---|---|---|
| model | string | 固定填写 "TierSense" |
| messages | string 或消息对象数组 | 完整问题，或当前非空消息历史 |
| task | string，可选 | Agent 入口保存的原始任务；提供后以它作为评分目标 |

当前公网要求 messages 非空。单独问题直接用字符串；Agent 首轮用包含用户问题的消息数组。

使用完整公网地址即可。

## 2. 方式一：直接给一个完整问题

```bash
export TIERSENSE_API_KEY="替换为平台提供的API_KEY"

curl 'https://tierflow.cn/tiersense/v1/score' \
  -H "Authorization: Bearer ${TIERSENSE_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "TierSense",
    "messages": "修复多分类报表，处理同分与未知标签并添加测试。"
  }'
```

问题可以是数学题、编程需求、文档任务或其他自然语言描述，直接写完整即可。

上面这个问题在 2026-09-22 公网测试中的实际返回：

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

### 返回分数怎么看

| 返回字段 | 范围 | 用法 |
|---|---|---|
| feature_scores.domain1–domain5 | 各 0–2 | 展示五路特征难度分 |
| score | 0–10 | 展示综合难度，或交给自己的选模策略 |

例如界面显示“综合难度 2.96”，同时展示五路分数。总分经过内部加权与标定，不是五路直接相加，也不是任务成功率。不同任务、措辞和执行状态都可能产生不同分数。某一路分数高不代表总分数高，还需要任务的领域特性。

### Python 调用

安装示例依赖：

```bash
python3 -m pip install requests
```

下面的函数同时适用于单问题和 Agent 历史：

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


result = score_difficulty("修复多分类报表，处理同分与未知标签并添加测试。")
print("综合难度：", result["score"])
print("五路分数：", result["feature_scores"])
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

## 3. 方式二：接入 Agent，每轮获取分数

接入位置：**每次主模型调用之前，把原始任务和当前消息历史发给 TierSense。**

```text
用户输入问题 → 接入代码保存 task
                    ↓
当前完整 messages → TierSense → 本轮五路分数和总分
                    ↓
              Agent 调用主模型
                    ↓
              执行工具、更新 messages
                    └→ 下一轮再次评分
```

### 3.1 task 自动从用户入口保存

用户只需向 Agent 提问一次。接入代码在添加框架提醒之前保存原始问题，以后每轮复用：

```python
# 复用上一节的 score_difficulty。

def on_new_task(user_question, session):
    # session 是你的应用为这个任务保存的状态。
    session["tiersense_task"] = user_question


def before_model_call(messages, session):
    scores = score_difficulty(
        messages,
        task=session["tiersense_task"],
    )
    print("本轮难度：", scores["score"])
    print("五路分数：", scores["feature_scores"])
    return scores


# 放进 Agent 已有的用户输入入口：
# on_new_task(user_question, session)
#
# 放进每一轮模型调用之前：
# scores = before_model_call(messages, session)
# response = existing_model_call(messages=messages)
```

这两处函数接到你已有的 Agent 生命周期中即可。分数单独记录；主模型继续使用自己的原始 messages。

task 按任务或会话保存，不同用户不共用。子 Agent 保存自己收到的委派任务。用户提出新目标时替换 task；补充关键约束时，将约束合并进当前任务描述。“继续”和工具返回不覆盖原目标。

例如原任务是“修复登录接口”，用户补充“不得改变返回 JSON 格式”，下一轮可传 `task="修复登录接口；不得改变返回 JSON 格式。"`。

### 3.2 一份完整 Agent 请求示例

```json
{
  "model": "TierSense",
  "task": "修复登录接口的并发问题，并补充回归测试。",
  "messages": [
    {"role": "system", "content": "你是一个代码助手。"},
    {"role": "user", "content": "修复登录接口的并发问题，并补充回归测试。"},
    {
      "role": "assistant",
      "content": "先读取登录接口实现。",
      "tool_calls": [
        {
          "id": "call_1",
          "type": "function",
          "function": {
            "name": "Read",
            "arguments": "{\"path\":\"app.py\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_1",
      "content": "def login(user): ..."
    }
  ]
}
```

messages 应是实际消息对象数组，不是 ["当前第20步的完整上下文"] 这样的文字占位符。保留工具调用 ID 及对应结果，服务会按 ID 关联它们。

### 3.3 如果没有在入口保存 task

可以只提交从首轮开始的完整历史：

```json
{
  "model": "TierSense",
  "messages": [
    {
      "role": "user",
      "content": "<system-reminder>框架环境提醒</system-reminder><user_query>修复登录接口并补测试。</user_query>"
    }
  ]
}
```

服务从首轮 user 任务块提取目标。

## 4. 不同 Agent 怎么接

优先接到用户输入入口；其次才从首轮请求消息提取。

| Agent / 协议 | task 从哪里保存 | messages 放什么 |
|---|---|---|
| CodeBuddy / CBC | 向 Agent 提交的原始问题 | 当前 Chat 或 Anthropic 消息；已知 CBC 提醒由服务识别 |
| Codex | 提交给 CLI / SDK 的任务文本 | 已组装的 Responses 消息 items，包括 function/custom 工具调用及结果 |
| DeepSeek Harness | harness 接收的原始用户文本 | 当前有效的消息历史；包括原生 `tool-call` / `toolCallId` 等字段 |
| Claude Code | 用户提交入口；使用 hook 时取 UserPromptSubmit.prompt | 当前 Anthropic 消息历史 |
| OpenClaw | 收到用户消息的入口内容 | 当前已支持的消息记录；内部 message:received 事件可取 context.content 保存 task |
| 自建 Agent | 应用自己的用户输入函数 | 当前 Chat、Responses 或 Anthropic 消息列表 |

表中入口字段用于**接入代码保存 task**，不需要把整个 hook 事件或日志文件当成评分 messages。TierSense 不会自行读取其他 Agent 进程的输入。

接入优先级是：入口保存原始问题 → 从首轮真实 user 任务块提取 → 明确补传 task。无论 Agent 品牌是什么，都使用实际发送给主模型的完整消息快照；不要把日志文件路径、SSE 文本、只有请求 ID 的对象当作消息历史。

### Codex / Responses 原生工具格式

把原生消息 items 放进评分请求的 messages，工具调用与返回保留同一个 call_id：

```json
{
  "model": "TierSense",
  "task": "检查报表脚本并补充测试。",
  "messages": [
    {"role": "user", "content": "检查报表脚本并补充测试。"},
    {
      "type": "custom_tool_call",
      "call_id": "c1",
      "name": "exec",
      "input": "read report.py"
    },
    {
      "type": "custom_tool_call_output",
      "call_id": "c1",
      "output": "def report(data): return {}"
    }
  ]
}
```

同类 function_call / function_call_output 也按 call_id 关联。工具输入是评分证据，TierSense 不执行这些工具。

### Anthropic 工具格式

```json
{
  "model": "TierSense",
  "task": "检查 app.py 的并发问题。",
  "messages": [
    {"role": "user", "content": "检查 app.py 的并发问题。"},
    {
      "role": "assistant",
      "content": [
        {"type": "tool_use", "id": "c1", "name": "Read", "input": {"path": "app.py"}}
      ]
    },
    {
      "role": "user",
      "content": [
        {"type": "tool_result", "tool_use_id": "c1", "content": "文件内容……"}
      ]
    }
  ]
}
```

这里最后一条 user 是工具结果，不会被当成新任务。

### 已经拿到主模型请求体时

另建评分请求，复制消息内容即可。评分请求的 model 始终是 TierSense，不要直接把主模型的 GPT / DeepSeek 等 model 值发给评分网关：

```python
# provider_request 是准备交给主模型的原始请求。
def score_provider_request(provider_request, task):
    if "messages" in provider_request:
        history = provider_request["messages"]
    else:
        history = provider_request["input"]
    return score_difficulty(history, task=task)

# scores = score_provider_request(provider_request, saved_task)
# 随后仍把原 provider_request 交给主模型。
```

该例适用于请求中已有完整历史的情况。若 Responses 请求只带增量和 previous_response_id，先在自己的 Agent 中补齐保存的历史，再提交 messages；仅有 ID 不能代替历史正文。

流式调用也一样：先将文本和工具参数的 delta 组装成完整消息，等工具结果返回后放回同一份历史。保留 `call_id` / `tool_call_id` / `tool_use_id` 等对应字段，不把调用 ID 换成工具名；并行出现两个 `Read` 时，它们仍是两次不同调用。







## 5. 常见问题

**只传一个问题，还需要 task 吗？**

不用。发送 {"model":"TierSense","messages":"完整问题"} 即可。

**只有 task，messages 可以为空吗？**

当前公网会返回 400，提示 messages must not be empty。单独问题用 messages 字符串；Agent 首轮传包含用户问题的消息列表。

**为什么返回 422 missing_task？**

输入中没有真实任务，例如只传 assistant 输出、工具结果或“继续”。补传明确的 task 和非空历史即可。

**用户说“继续”怎么办？**

继续使用已经保存的 task，并提交更新后的消息历史。用户改变目标时，再更新 task。
