---
title: 万字长文拆解Agent 架构设计（四）：多 Agent 协作（速读摘要）
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Claude-Code
  - 主题/多-Agent
  - 主题/Context-Engineering
  - 主题/Agent-Architecture
  - 主题/Sub-Agent
  - 场景/公众号长文
  - 来源/架构师带你玩转AI
type: digest
date: 2026-07-27
source: 微信公众号「架构师带你玩转AI」2026-07-22 推送 / AllenTang
原始链接: https://mp.weixin.qq.com/s/CFTp_TVA8DQLFuvirkrFvQ
nodes: []
---

# 万字长文拆解Agent 架构设计（四）：多 Agent 协作（速读摘要）

> **一句话**：Claude Code 的多 Agent 机制并不是“给同一个模型分不同脑区”，而是把大任务拆到多个干净上下文里去做，让子 Agent 吃掉大材料，最后只交回一页结论。

## 8 节点速查表

| 节点 | 一句话定义 |
|---|---|
| 上下文切分优于能力切分 | 多 Agent 的收益主要来自干净窗口，而不是角色名不同 |
| 编排者执行者互补权限 | 父 Agent 负责规划和派发，子 Agent 负责具体执行 |
| Task工具委派接口 | 子 Agent 派发本质上就是一次普通工具调用 |
| 子Agent定义三读者 | `description` 给模型选人，`tools` 给权限系统，正文给子 Agent |
| 新桌子效应 | 子 Agent 在全新上下文里处理局部材料，更容易聚焦 |
| 最后一条消息回传 | 父线程只收最终结论，不收中间轨迹 |
| 权限交集裁剪 | 子 Agent 权限 = 父权限与子定义白名单的交集 |
| 模型即调度器 | 并行和串行由模型决定，系统只提供原语和护栏 |

## 4 条设计规则

1. **父线程默认做编排，不直接做高风险执行。**
2. **子线程默认不开递归派发，防止调度树膨胀。**
3. **任务描述是唯一输入，任务结果只回最终消息。**
4. **系统负责权限、预算和上下文边界，模型负责判断何时并行。**

## 3 个最值钱的反直觉点

- **多 Agent 不等于更多能力**：最核心的收益其实是“桌面更干净”。
- **并行不需要重型调度器**：模型在一轮里多发几个 task，本来就能并行。
- **子 Agent 定义不是注释，而是接口**：描述写不清，派工就会错误。

## 6 个对 Seetong / APP AI 开发流程可借鉴动作

1. **只有上下文过载才拆子 Agent**，不要把“任务一复杂”误当成并行信号。
2. **主线程保留拆解和汇总职责**，尽量不直接持有高风险副作用工具。
3. **每类子 Agent 写成三段定义**：角色说明、工具白名单、system prompt。
4. **子 Agent 统一返回结构化短结论**，不要把长轨迹直接塞回父线程。
5. **工具权限默认做交集裁剪**，高风险工具和递归派发都默认关闭。
6. **让模型负责是否并行，让系统负责预算和审计**。

## 关联 + 备注

**关联**：[[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]] / [[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]] / [[01-ai-agents/未来属于垂直领域Agent]] / [[02-ai-coding/多Agent使用边界与并行判定]] / [[01-ai-agents/图工程-Graph-Engineering-来了-LangChain说不是新东西]] / [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]] / [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]

**备注**：这篇文章补的是多 Agent runtime 机制这一层，不是“为什么需要多 Agent”的宏观论证，也不是“如何落成生产系统”的完整工程手册。
