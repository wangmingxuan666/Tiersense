# API 调用示例 / API request examples

[中文首页](../README.zh-CN.md) · [English home](../README.md)

在仓库根目录运行，使用 Python 3 标准库，无需安装额外依赖。先在业务后端环境中设置 `TIERSENSE_API_KEY`，不要把真实 Key 写进仓库。

Run from the repository root with Python 3; no extra dependencies are required. Set `TIERSENSE_API_KEY` in your backend environment. Never commit a real key.

```bash
python3 examples/request.py score --input examples/score.json
python3 examples/request.py compress --input examples/compress.json
python3 examples/request.py memory-decide --input examples/memory-decide.json
```

选择需要的一个命令即可，不必同时调用三个 API。JSON 文件只是虚构的格式示例，实际使用时替换为原始 task 与真实 messages。

Choose the command you need; you do not need to call all three APIs. JSON files are fictional format examples. Replace them with your original task and actual messages.

接口返回格式各不相同。此脚本仅打印响应，不自动切换主模型、生成摘要或执行召回，也不会把失败变成“否”。调用会产生真实的 API 请求。

Response contracts differ. The script prints the response; it does not switch models, summarize, retrieve, or turn failures into negative decisions. Running it sends a real API request.

- [Score](../docs/score/README.md)
- [Compress](../docs/compress/README.md)
- [Memory-Decide](../docs/memory-decide/README.md)
