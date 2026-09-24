<p align="center"><a href="https://tierflow.cn/tiersense"><img src="assets/tiersense-logo.png" alt="TierSense" width="500"></a></p>

<h1 align="center">TierSense</h1>

<p align="center"><strong>Understand difficulty. Decide when to compress and recall.</strong></p>

<p align="center">
<a href="https://tierflow.cn/tiersense"><img src="https://img.shields.io/badge/API-TierSense-6856E8" alt="TierSense API"></a>
  <a href="https://github.com/wangmingxuan666/Tiersense-memory-decide/blob/main/paper/Memory_Control.pdf"><img src="https://img.shields.io/badge/Paper-Memory_Control-b31b1b" alt="Memory Control PDF"></a>
<a href="AUTHORS_STATEMENT.en.md"><img src="https://img.shields.io/badge/Authors-Statement-0969da" alt="Authors' statement"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a></p>

> **The TierSense project hub**: use the three modules independently or combine them for your application. Find project navigation, integration guidance, and the centralized [authors' statements](AUTHORS_STATEMENT.en.md) here.

> [!IMPORTANT]
> **Authors' statement | Independent technical approach and research timeline**
>
> We deeply regret that, in this day and age, publishing our work requires us to clarify when we began it. Nevertheless, we will do so.
>
> We solemnly state that the three methods and two manuscripts were completed **before September 14, 2026, Beijing time (UTC+8), with their actual completion dates being earlier still (supported by the WeChat screenshot at the end of this page)**. Jev appeared on **September 15, 2026**. This work represents approximately six months of effort before its public release. These were not papers hastily assembled with AI within a few days of Jev's appearance. The two papers emerged as branches of the research process; both are complete studies developed through validation and released recently after repeated refinement. For the detailed timeline, please contact the account holder directly.
>
> **This method follows a completely different technical approach from Jev and includes our own mechanistic findings. We regard it as an advance beyond Jev through an independent technical direction—not a reproduction or a rushed follow-up.** This is the authors' assessment of originality and technical direction, not a claim that a universal performance advantage across all tasks has already been demonstrated in published comparisons.
>
> We oppose hastily assembled work lacking substantive research presented under the label “auto research,” and we disagree with applying that label to carefully developed work based solely on publication timing. We want to make a genuine contribution to the community and recognize that AI-assisted research can produce high-quality results. We ask that the effort behind this method and manuscript not be dismissed as automatically generated filler without a fair examination.
>
> At the same time, we understand the concerns about research quality and appreciate those who speak up for meaningful scholarly discussion. We hope to work alongside you to produce and publish genuinely valuable research, so that sustained effort receives thoughtful consideration rather than being dismissed overnight as filler. If this resonates with you, please join our official discussion group to exchange ideas, explore new directions, and pursue more interesting and rigorous research together.
>
> We welcome you to use our work and share your valuable feedback. Questions, reproduction efforts, and open discussion are all welcome.

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
| Compression / recall decisions | `https://tierflow.cn/tiersense/v1/memory/decide` |

[Minimal request examples for all three APIs](docs/quickstart.en.md). Request and response contracts differ; fields are not interchangeable.

## Paper

[Memory Control Signals Emerge Before Action in Long Horizon Agents](https://github.com/wangmingxuan666/Tiersense-memory-decide/blob/main/paper/Memory_Control.pdf)

Read or download the full author-provided PDF (35 pages). The research system described in the paper and the hosted decision API have different scopes; see the usage guide for the API contract.

## Documentation

- [Quick start](docs/quickstart.en.md): minimal requests for the three APIs.
- [Agent integration](docs/agent-integration.en.md): invocation points, application responsibilities, and limitations.
- [Authors' statements](AUTHORS_STATEMENT.en.md): centralized statements and research timeline material.

This is a documentation and navigation hub, not a merged inference service. It does not include model weights, production configuration, or a new unified SDK. The original repositories and their histories remain independent. Read the Memory Control paper using the link above.

## Join the community

<p align="center"><a href="https://tierflow.cn"><img src="assets/tierflow-logo.png" alt="TierFlow" width="240"></a></p>

We welcome you to use our work and share your valuable feedback. Questions, reproduction efforts, and open discussion are all welcome.

<img src="assets/community-qr.png" alt="TierFlow official discussion group QR code and contact information" width="640">

## Research timeline screenshot

<img src="assets/wechat-timeline.png" alt="Author-provided research timeline screenshot" width="600">
