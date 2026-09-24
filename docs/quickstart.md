# 快速调用

[English](quickstart.en.md) · [首页](../README.zh-CN.md)

将 YOUR_API_KEY 换成平台提供的 Key。以下为虚构的格式示例，不预设模型结果。

## 1. TierSense-Score

```bash
curl 'https://tierflow.cn/tiersense/v1/score' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"model":"TierSense","messages":"Fix CSV export encoding and add tests."}'
```

读取 feature_scores.domain1–domain5 与 score。模型选择由应用完成，接口不会替你切换主模型。

## 2. TierSense-Compress

```bash
curl 'https://tierflow.cn/tiersense/v1/compress' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model":"TierSense",
    "task":"Fix CSV export encoding and add tests.",
    "messages":[
      {"role":"user","content":"Fix CSV export encoding and add tests."},
      {"role":"assistant","content":"Located an encoding mismatch; preparing a fix."}
    ]
  }'
```

读取 steps 中的 should_compress、confidence 与 message_indices。需要连续片段执行策略时，按子项目文档配置 options；本最小示例不启用该策略。摘要生成与历史替换由应用执行。

## 3. TierSense-Memory-Decide

```bash
curl 'https://tierflow.cn/tiersense/v1/memory/decide' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "model":"TierSense",
    "task":"Fix CSV export encoding and add tests.",
    "messages":[
      {"role":"user","content":"Fix CSV export encoding and add tests."},
      {"role":"assistant","content":"Located an encoding mismatch; preparing a fix."}
    ]
  }'
```

读取 compression.predicted、recall.predicted 及各自 confidence。它不返回逐步索引，不执行摘要或检索；没有旧历史／可召回记忆时，不执行对应动作。

完整字段和 Agent 示例见各子项目使用指南。
