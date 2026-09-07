---
title: “薄 Agent Loop，厚 Control Plane”：TiDB 用数据库思维重做 Harness
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Harness工程
  - 主题/Control-Plane
  - 主题/Agent运行时
  - 主题/可靠性工程
  - 主题/多Agent协作
  - 场景/公众号长文
nodes: [薄Agent-Loop, 厚Control-Plane, 持久Workspace, 外部不变量, 声明式目标, 版本化并行探索, 通信即复杂度, Fail-Fast, 可信恢复]
links: [[01-ai-agents/DataFunTalk-Graph-Engineering-从Harness到Ontology]], [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]], [[01-ai-agents/2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]], [[01-ai-agents/源泉TheFountainhead-从GUI到AI-Native-产品接目标界面换职责]]
date: 2026-09-07
source: 微信公众号「InfoQ」/ Tina 对话 TiDB 唐刘
---

# “薄 Agent Loop，厚 Control Plane”：TiDB 用数据库思维重做 Harness

- 原文链接：https://mp.weixin.qq.com/s/XwdD9d6jFbRFwMWhr5a7JA
- 作者：Tina
- 受访者：TiDB 唐刘
- 发布：2026-09-06 12:30
- 获取时间：2026-09-07

## 核心结论（一句话）

> Agent Core、模型与工具协议可以快速替换，但持久 Workspace、权限、外部副作用、验证证据、隔离、错误传播控制与 Failover 应由稳定的 Control Plane 负责，才能让会犯错的 Agent 持续参与生产任务。

## 分类提炼

- 场景：生产级 Coding Agent、分布式系统、云服务升级、多 Agent Runtime
- 类型：Harness 基础设施访谈 / 数据库可靠性向 Agent 运行时迁移
- 标签： #主题/AI-Agent #主题/Harness工程 #主题/Control-Plane #主题/Agent运行时 #主题/可靠性工程 #主题/多Agent协作 #场景/公众号长文

## 知识节点

- **薄Agent-Loop**：模型协议、工具调用与 Agent Core 变化快且可替换，不应成为系统稳定性的唯一承载层。
- **厚Control-Plane**：状态、权限、Sandbox、副作用边界、审计和恢复属于跨模型的稳定基础设施，应独立治理。
- **持久Workspace**：Agent 的工作现场应脱离 Session/Sandbox 生命周期，以便 Executor 更替后继续访问同一文件和任务状态。
- **外部不变量**：关键任务用测试、输入、故障条件、外部状态和可重现实验验证，而非采信 Agent 的完成声明。
- **声明式目标**：模型变强后，用户可更多声明结果而非逐步指定内部协作，但高层任务边界、状态与恢复仍不可省略。
- **版本化并行探索**：多个 Agent 分别在隔离 Workspace/Version 中尝试方案，再 Merge 或淘汰，避免争抢同一共享世界。
- **通信即复杂度**：高频消息广播扩大同步、性能和调试成本；明确 Input/Output 与状态共享通常比 Agent 群聊更稳。
- **Fail-Fast**：失败应尽早暴露并停止错误路径，不能用无界 Retry 把局部故障扩散为后续 Context 的权威事实。
- **可信恢复**：Checkpoint、持久状态、路径切换和 Executor 接管使系统能从最近可信状态 Failover，而非在错误前提上继续执行。

## 关联图谱

### 上游（基于 / 来自）

- [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]]：该页的可信完成、动作回执、Goal 契约与状态合流，为本文的外部不变量、持久 Workspace 和恢复路径提供通用 Agent 基础。
- [[01-ai-agents/2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]]：该页的会话快照、异步任务、沙箱、多 Agent 隔离和追踪，构成本文 Control Plane 所要统一的底座能力。

### 下游（应用于 / 验证于）

- [[01-ai-agents/DataFunTalk-Graph-Engineering-从Harness到Ontology]]：该页将任务、能力、运行时状态、证据、权限与恢复组织为图；本文用数据库的版本、事务、检查点和 Failover 类比强化其运行时实现边界。

### 同级（横向 / 并列）

- [[01-ai-agents/源泉TheFountainhead-从GUI到AI-Native-产品接目标界面换职责]]：该页解释用户侧控制面如何承担授权、状态、审查与接管；本文从系统侧说明这些体验依赖哪些稳定基础设施。
- [[01-ai-agents/phodal-面向人机交互设计Harness-产物中心Agent-Loop]]：该页强调产物版本、操作回执与领域运行时；本文扩展到跨 Session 的 Workspace、权限和 Failover。

## 正文要点

1. **将 Agent Loop 与 Control Plane 解耦。** TiDB 的实践不是从零重写 Loop，而是让开源 Agent Core 承担最内层能力；状态、权限、Sandbox、任务编排和失败恢复独立演进，从而支持换模型或 Agent Core 而不破坏生产边界。
2. **数据库的验证观可迁移到 Agent。** Mission Critical 系统靠测试、故障注入、随机/兼容/性能测试和线上 Case 积累建立可信度。Agent 的“已修好”必须被 Commit、输入、测试、故障条件、外部 Evidence 与可复现性验证。
3. **编排会由步骤说明转向结果声明。** 模型能处理更多内部计划时，命令式角色流程和 Prompt 会减少；但 Context 上限、持久状态和错误恢复仍要求上层定义任务边界与控制规则。
4. **版本化 Workspace 支持并行探索。** Agent 可继续以 File 操作理解环境，但底层需提供数据库式检索、事务、版本、分支、回滚与查询。隔离 Version 让多个 Agent 先独立尝试，再合并或舍弃。
5. **多 Agent 的默认策略应是降通信。** Agent 间以清晰 I/O 与共享状态解耦，上层再按需分配与汇总；高频聊天、同步通知和复杂拓扑只有在信息收益大于协调成本时才值得引入。
6. **长程可靠性的关键是控制错误传播。** 不应把连续步数当作核心指标。系统应尽早发现错误，禁止未证实输出自动沉淀为后续事实，并通过 Checkpoint、持久状态和替代执行者回到最近可信状态。
7. **责任边界仍属人类治理。** 模型在通用 Coding 上趋同不等于能承担云服务升级、客户风险和回滚后果；工程师的职责会上移到定义系统性质、风险取舍、验收与最终决策。

## 备注

- 本文是 InfoQ 对 TiDB 团队实践的访谈，涉及架构、规模、实现迁移与效果的说法均来自受访方，未独立复现或审计。
- 数据库的 Transaction、Privilege、Durability、MVCC、Checkpoint 与 Failover 仅用于提供可靠性类比；落地 Agent 系统仍需按业务风险和外部系统语义具体设计。
- “更少编排”不是没有编排，而是把可由模型内部完成的步骤隐藏在声明式目标之后，同时保留状态、权限、验证与恢复控制。

## 相关链接

- [[01-ai-agents/DataFunTalk-Graph-Engineering-从Harness到Ontology]]
- [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]]
- [[01-ai-agents/2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]]
- [[01-ai-agents/源泉TheFountainhead-从GUI到AI-Native-产品接目标界面换职责]]
