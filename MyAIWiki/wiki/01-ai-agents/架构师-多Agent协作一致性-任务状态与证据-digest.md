---
title: 多 Agent 协作一致性 - 速读
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/多Agent
  - 主题/一致性
  - 主题/Harness
nodes: [一致性三件事, 可执行交接状态, 权威事实, 结果契约, 局部重试与幂等]
links: [[01-ai-agents/架构师-多Agent协作一致性-任务状态与证据]], [[01-ai-agents/Loop-Engineering-验证才是瓶颈]], [[01-ai-agents/phodal-Better-Harness-任务级证据评估]]
date: 2026-09-14
source: 微信公众号 / 架构师（若飞）
status: published
---

# 多 Agent 协作一致性 - 速读

> 多 Agent 一致性不是让答案一样，而是让任务、事实和状态一致；模型负责判断，运行时负责版本、证据、副作用和完成证明。

- **一致性三件事**：同一任务、同一事实、同一状态；推理可以保留分歧。
- **可执行交接状态**：传递 snapshot、evidence、assumptions、constraints、artifacts 和 acceptance。
- **权威事实**：聊天是历史，摘要是工作集，代码、测试、部署和业务库才是事实来源。
- **结果契约**：保留来源、版本和状态，区分候选、已验证、冲突、否决。
- **局部重试与幂等**：失败按子任务恢复，副作用先查状态，再用幂等键安全重放。
- **完成证据**：commit、命令、退出码、报告和 Reviewer 结果共同定义“完成”。

最小实践：先为一个窄任务建立 `global_task_id / sub_task_id / version / attempt / lease_until / result_ref`，再补结构化 handoff 和局部重试。

证据边界：Google 研究数字为特定实验口径，本文架构建议来自公众号作者与参考资料综合解读。

关联：[[01-ai-agents/架构师-多Agent协作一致性-任务状态与证据]]、[[01-ai-agents/Loop-Engineering-验证才是瓶颈]]、[[01-ai-agents/phodal-Better-Harness-任务级证据评估]]。
