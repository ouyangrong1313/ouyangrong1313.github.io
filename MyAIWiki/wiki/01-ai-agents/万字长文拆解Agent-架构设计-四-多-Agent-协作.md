---
title: 万字长文拆解Agent 架构设计（四）：多 Agent 协作
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
nodes: [上下文切分优于能力切分, 编排者执行者互补权限, Task工具委派接口, 子Agent定义三读者, 新桌子效应, 最后一条消息回传, 权限交集裁剪, 模型即调度器]
links: [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]], [[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]], [[01-ai-agents/未来属于垂直领域Agent]], [[02-ai-coding/多Agent使用边界与并行判定]], [[01-ai-agents/图工程-Graph-Engineering-来了-LangChain说不是新东西]], [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]], [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]
date: 2026-07-27
source: 微信公众号「架构师带你玩转AI」2026-07-22 推送 / AllenTang
---

# 万字长文拆解Agent 架构设计（四）：多 Agent 协作

- **原文标题**：万字长文拆解Agent 架构设计（四）：多 Agent 协作
- **原文链接**：https://mp.weixin.qq.com/s/CFTp_TVA8DQLFuvirkrFvQ
- **公众号**：架构师带你玩转AI
- **作者**：AllenTang
- **发布时间**：2026-07-22 23:17
- **获取时间**：2026-07-27
- **分类理由**：这篇文章虽然以 Claude Code 为例，但真正讲的是多 Agent runtime 的核心原语：角色分层、上下文隔离、权限裁剪、结果回流和调度边界。它讨论的是 Agent 架构，不是某个 AI Coding 技巧页，所以放 `01-ai-agents`。

## 核心结论

> **多 Agent 协作真正切开的不是“能力”，而是“上下文”——父 Agent 负责规划和汇总，子 Agent 在全新上下文里吃掉局部大材料，最后只把最终结论带回，从而用更干净的桌面换取更稳定的判断。**

## 分类提炼

- **场景**：Claude Code 子 Agent 设计 / 多 Agent 编排 / 上下文工程
- **标签**： #主题/AI-Agent #主题/Claude-Code #主题/多-Agent #主题/Context-Engineering #主题/Agent-Architecture #主题/Sub-Agent #场景/公众号长文 #来源/架构师带你玩转AI
- **类型**：架构拆解 / runtime 设计 / 子 Agent 原语说明
- **最强增量**：把“新桌子效应”“最后一条消息回传”“权限交集裁剪”“模型即调度器”讲成一组可以直接迁移到其他 Agent 系统里的设计规则

## 知识节点（8 个独立概念）

- **上下文切分优于能力切分**：多 Agent 的收益不来自“换一个更会做事的模型实例”，而来自给每个子任务一个更小、更干净、更聚焦的上下文窗口。
- **编排者执行者互补权限**：父 Agent 拥有规划、分解和派发能力，子 Agent 拥有具体执行能力，两者工具集互补而非重叠，用来阻止越权执行和递归失控。
- **Task工具委派接口**：派发子 Agent 在实现上就是一次普通 tool call，输入是任务描述和子类型，输出只有最终消息，这让多 Agent 不需要单独长出一套复杂的控制面。
- **子Agent定义三读者**：子 Agent markdown 定义同时面向三类读者：`description` 给父模型选人，`tools` 给权限系统裁剪白名单，正文给子 Agent 自己做 system prompt。
- **新桌子效应**：子 Agent 在全新上下文里启动，看不到父 Agent 的历史聊天和枝节噪声，等价于把大任务搬到一张新桌子上只做局部处理。
- **最后一条消息回传**：父 Agent 默认只接收子 Agent 的最终结论，不接收其中间轨迹、工具明细和弯路，从而把上下文消耗压缩在子线程内部。
- **权限交集裁剪**：子 Agent 最终可用的工具不是“定义里写了什么就有什么”，而是“子定义白名单”与“父 Agent 已拥有权限”的交集，且默认拿不到 `task`。
- **模型即调度器**：哪些任务并行、哪些串行，不靠框架层写死调度器，而是由模型在一轮里决定要发几个 task 调用；系统只提供安全原语和边界。

## 关联图谱

### 上游（基于 / 来自）

- [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]]：那篇从会话边界和进程边界解释多 Agent 架构差异，这篇补上了 Claude Code 子 Agent 在上下文边界上的 runtime 机制。
- [[01-ai-agents/未来属于垂直领域Agent]]：domain-specific 拆分强调“为什么要拆成多个小 Agent”，本文进一步解释“拆出来以后怎样靠新上下文和权限裁剪保持稳定”。
- [[01-ai-agents/图工程-Graph-Engineering-来了-LangChain说不是新东西]]：图工程讲“边为什么成立”，本文讲“子 Agent 为什么能成立”；两者都把系统收益归到上下文/依赖切分，而不是名词热度。

### 下游（应用于 / 验证于）

- [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]]：把本文的上下文隔离、权限边界和子 Agent 返回契约推进成生产级多 Agent Harness 骨架。
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]：用 12 专家并行、DAG 协作和评审节点验证“模型决定并行，系统兜住边界”这条工程路线。
- [[02-ai-coding/多Agent使用边界与并行判定]]：把本文的 runtime 机制收束成日常可执行判定句：不是任务一复杂就该多 Agent，而是要先看上下文负载和边界清晰度。

### 同级（横向 / 并列）

- [[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]：动态工作流强调让模型临场画图，本文解释 Claude Code 最底层能支撑这件事的子 Agent 原语是什么。
- [[01-ai-agents/图工程-Graph-Engineering-来了-LangChain说不是新东西]]：一篇讲拓扑，一篇讲子 Agent 运行时；合起来才完整回答“多 Agent 到底怎么拆、怎么跑”。
- [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]]：一篇讲架构形态，一篇讲运行机制；同属多 Agent 基础理解层。

## 正文要点（6 条）

1. **Claude Code 对多 Agent 的回答，不是把同一个模型硬拆成不同职能，而是把大任务拆成多个干净上下文。**  
   文章最重要的反直觉点是：子 Agent 并不因为“角色名不同”就更强，它之所以值钱，是因为只拿到一段任务描述和有限材料，能在更小上下文里集中注意力。

2. **父 Agent 和子 Agent 的核心分工不是“谁更聪明”，而是“谁负责规划，谁负责执行”。**  
   父 Agent 有 `task`、只读工具和汇总责任；子 Agent 拥有 `bash`、`write_file` 之类副作用工具，但默认不能再派子 Agent。这样既防父线程绕过规划直接动环境，也防子线程无限递归。

3. **Task 是一个很薄的委派接口，真正的复杂度不在“调用方式”，而在“契约设计”。**  
   `prompt` 是唯一输入，子 Agent 定义文件则决定角色边界和权限。换句话说，多 Agent 的稳定性主要取决于你是否把任务说明、工具白名单和 system prompt 写成了清晰接口。

4. **“只交最后一条消息”是整个设计里最关键的压缩动作。**  
   子 Agent 的中间轨迹、工具详情和试错过程不自动回流父上下文，这个设计直接决定了父线程还能继续保持“桌面干净”，否则多 Agent 只会把多个长轨迹重新塞回同一窗口。

5. **权限与预算的默认策略都是收缩，而不是扩张。**  
   子 Agent 的工具权限来源于交集裁剪，预算是从父线程继承后再向下分配，默认不能无限生长。这说明多 Agent 体系要先设计“怎么收口”，再设计“怎么变强”。

6. **并行并不是框架层写死的 scheduler，而是模型利用 `task` 原语做出来的运行时选择。**  
   Claude Code 没有专门写一层显式并发调度器，哪些任务该并行、哪些该串行，仍然由模型根据上下文判断；框架真正提供的是安全护栏、权限边界和返回格式。

## 6 个对 Seetong / APP AI 开发流程可借鉴动作

1. **把多 Agent 触发条件从“任务复杂”改成“上下文过载”**：只有单个上下文已经吃不下、记不牢、聚不焦的任务，才值得拆子 Agent。
2. **让主线程默认做编排，不直接拿高风险副作用工具**：研究、排障、方案生成、知识库编译这类任务里，主线程优先负责拆解、指派和收束。
3. **为每类子 Agent 固化三段定义**：一句角色说明给父模型选人、一组工具白名单给权限系统、一段 system prompt 给子 Agent；不要混成一坨长说明。
4. **子 Agent 强制只回传结构化结论**：例如“结论 + 证据 + 风险 + 建议动作”，不要把整个思维轨迹和原始材料直接回灌父上下文。
5. **所有子 Agent 权限走交集裁剪，默认禁递归派发**：先把系统做成收敛的，再按需放开，而不是先给全权限再靠 prompt 劝它克制。
6. **并行决策交给模型，但审计与预算交给系统**：让模型判断读多个模块、查多份资料时是否要并行；系统负责记录预算、限制工具和收敛输出。

## 备注与限制

- 文章是 Claude Code 架构拆解系列中的一篇，重点在 runtime 原语，不是完整官方源码逐行注释。
- 文中的 TypeScript 代码是概念化复写，更适合帮助建立心智模型，而不是作为现成框架直接照搬。
- 这篇文章最适合和 [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]]、[[01-ai-agents/图工程-Graph-Engineering-来了-LangChain说不是新东西]]、[[01-ai-agents/从零设计生产级-Multi-Agent-Harness]] 连读，分别补“形态”“拓扑”“工程骨架”三块。

## 相关链接

- [[01-ai-agents/万字长文拆解Agent-架构设计-四-多-Agent-协作-digest]]
- [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]]
- [[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]
- [[01-ai-agents/图工程-Graph-Engineering-来了-LangChain说不是新东西]]
- [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]]
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]
