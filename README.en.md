<p align="center"><a href="https://tierflow.cn/tiersense"><img src="assets/tiersense-logo.png" alt="TierSense" width="500"></a></p>

<h1 align="center">TierSense</h1>

<p align="center"><strong>Understand difficulty. Decide when to compress and recall.</strong></p>

<p align="center">
<a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
<a href="AUTHORS_STATEMENT.en.md"><img src="https://img.shields.io/badge/Authors-Statement-0969da" alt="Authors' statement"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a></p>

> **The TierSense project hub**: use the three modules independently or combine them for your application. Find project navigation, integration guidance, and the centralized [authors' statements](AUTHORS_STATEMENT.en.md) here.

## Three modules, one entry point

| Module | Question | Output | Guide |
| --- | --- | --- | --- |
| [TierSense-Score](https://github.com/wangmingxuan666/Tiersense-score) | How difficult is the current task? | Five feature scores and an overall score | [Difficulty scoring](https://github.com/wangmingxuan666/Tiersense-score/blob/main/docs/usage.en.md) |
| [TierSense-Compress](https://github.com/wangmingxuan666/Tiersense-Compress) | Which historical steps are ready for compression? | Per-step recommendations and span selection | [History compression](https://github.com/wangmingxuan666/Tiersense-Compress/blob/main/docs/usage.en.md) |
| [TierSense-Memory-Decide](https://github.com/wangmingxuan666/Tiersense-memory-decide) | Should history be compressed or recalled now? | Two decisions and their confidence values | [Memory decisions](https://github.com/wangmingxuan666/Tiersense-memory-decide/blob/main/docs/usage.en.md) |

These modules provide decision signals. Your application switches models, generates summaries, and retrieves memories. See each project's documentation for its complete contract and latest capabilities.

## Choose a module

- **Difficulty display or a signal for model routing**: use Score and define your own score-to-model mapping.
- **Selecting history to compress**: use Compress, then your own summarizer.
- **Deciding when to use an existing memory system**: use Memory-Decide and check execution preconditions.
- **Combining modules**: read the [integration guide](docs/agent-integration.en.md). You do not need all three APIs on every request.

## Quick start

Get an API key from the [TierSense platform](https://tierflow.cn/tiersense). These endpoints follow the current child-project documentation; creating this hub does not change them.

| Capability | POST endpoint |
| --- | --- |
| Difficulty scoring | `https://tierflow.cn/tiersense/v1/score` |
| History compression selection | `https://tierflow.cn/tiersense/v1/compress` |
| Compression / recall decisions | `https://demo.tierflow.cn:1443/tiersense/v1/memory/decide` |

[Minimal request examples for all three APIs](docs/quickstart.en.md). Request and response contracts differ; fields are not interchangeable.

## Documentation

- [Quick start](docs/quickstart.en.md): minimal requests for the three APIs.
- [Agent integration](docs/agent-integration.en.md): invocation points, application responsibilities, and limitations.
- [Authors' statements](AUTHORS_STATEMENT.en.md): centralized statements and research timeline material.

This is a documentation and navigation hub, not a merged inference service. It does not include model weights, production configuration, or a new unified SDK. The original repositories and their histories remain independent. The Memory Control paper is not uploaded in this update.

## Join the community

<p align="center"><a href="https://tierflow.cn"><img src="assets/tierflow-logo.png" alt="TierFlow" width="240"></a></p>

We welcome you to use our work and share your valuable feedback. Questions, reproduction efforts, and open discussion are all welcome.

<img src="assets/community-qr.png" alt="TierFlow official discussion group QR code and contact information" width="640">
