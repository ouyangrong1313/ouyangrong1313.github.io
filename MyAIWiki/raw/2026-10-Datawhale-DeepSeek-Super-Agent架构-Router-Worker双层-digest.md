# DeepSeek Super-Agent 架构 - 原文摘要

## 一句话总结

DeepSeek 开源 `dsh-superagent-prototype`：用常驻 Router + 隔离 Worker 拆开「全局连续性」与「高并发干活」，再用四个计算机系统经典设计（两级过滤、订阅直通、Inline & Spill、投机执行）把事件驱动真正跑起来。

## 核心观点

- **单 Session 与多 Session 都不行**：全塞一个 Session 则串行慢、上下文互污；每事新开则互不通气。解法是分层而非折中。
- **Router 不干活**：常驻层只做协调分派，甚至不给它配 Bash。消息积压时自动合并成 Batch，积压越多单次决策越便宜（6.4 秒降到 1.6 秒）。
- **Worker 不对人说话**：只向 Router 汇报，由 Router 统一对外。用户跨飞书群与 PR 评论时面对同一个 Agent。
- **驱动不该只是 Prompt**：群消息、代码评论、CI 结果是 Trigger。而群聊高噪音低触发率，每条都调大模型必然爆炸，所以先走确定性规则 Fast Path。
- **上下文靠局部性管理**：紧邻信息 Inline，超长内容 Spill 到窗口外只留摘要与 ID，需要时顺引用图一跳一跳检索。
- **投机执行像分支预测**：看到报 Bug 先在后代复现修复，成了拿出来，没成默默丢弃。
- **Watchdog 盯「有没有进展」**：不只盯进程存活，还用模型判断 Worker 是否空转，且支持自然语言问故障、在线改提示词。

## 关键数据

| 指标 | 数值 | 说明 |
|---|---|---|
| Router 批处理耗时 | 6.4 秒 → 1.6 秒 | 消息积压时单次决策分摊耗时 |
| 订阅直通收益 | 决策次数 -30%、读缓存 Token -37% | 消融实验 |
| p95 任务完成时间 | 15.7 分钟 | 对比单 Session + Subagent 的 29.5 分钟 |
| 人类并发上限 | 3~5 个活跃 Session | 原文给出的问题起点 |

## 核心金句

- 「多任务的上限，卡在了人的注意力上。」
- 「Router 层绝不亲自下场干活，只做高层协调与任务分派。」
- 「Worker 绝不直接对人类说话，而是向 Router 汇报。」
- 「修好了就拿出来惊艳所有人，没修好就默默丢弃、绝不打扰。」
- 「Agent 跑崩了往往不是进程挂了，而是模型陷入了死循环或跑偏了。」

## 关联图谱

- **上游**：操作系统与 CPU 设计（批处理、分支预测、局部性原理、Watchdog）；ReAct Loop。
- **下游**：多任务 Agent 底座选型、团队级 AI 协作平台设计、长驻 Agent 的稳定性方案。
- **同级**：[[01-ai-agents/Harness工程AgentLoop]]、[[01-ai-agents/InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]、[[01-ai-agents/LangChainCEO-Agent越复杂-越需要自建Harness-恰恰不是]]。

## 备注与限制

- 全部性能数字均转述自 DeepSeek 官方架构长文，未给实验条件与样本量。
- 仓库名含 `prototype`，是原型而非生产级。
- 「Session 焦虑」「链式召回」等为原文用语，非官方术语。
