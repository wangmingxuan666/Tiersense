# Quick start

[简体中文](quickstart.md) · [Home](../README.md)

Replace YOUR_API_KEY with the key provided by the platform. These are fictional format examples, not predetermined predictions.

## 1. TierSense-Score

```bash
curl 'https://tierflow.cn/tiersense/v1/score' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"model":"TierSense","messages":"Fix CSV export encoding and add tests."}'
```

Read feature_scores.domain1–domain5 and score. Model selection belongs to your application; the API does not switch the main model.

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

Read should_compress, confidence, and message_indices in steps. Configure options as documented in the child project if you need span execution policies; this minimal example does not enable one. Your application generates summaries and replaces history.

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

Read compression.predicted, recall.predicted, and their respective confidence values. It returns no per-step indices and performs no summarization or retrieval. Skip an operation if eligible history or stored memory does not exist.

See the child-project guides for complete fields and agent examples.
