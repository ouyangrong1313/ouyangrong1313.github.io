---
title: 图工程（Graph Engineering）来了？LangChain说不是新东西
category: 01-ai-agents
tags: [#主题/AI-Agent, #主题/Graph-Engineering, #主题/LangGraph, #主题/Harness, #主题/Loop, #主题/Agent-Topology, #场景/公众号长文, #来源/AI工程化]
nodes: [线性Agent是退化图, 节点契约, 数据契约边, 钻石拓扑, 验证器节点, 有环图, 动态Send, 图-vs-Harness]
links: [[0xCodez-Agent-Harness-14-Steps]], [[WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[Lilian-Weng-Harness-Engineering-自我改进]], [[Loop-Engineering-验证才是瓶颈]], [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]], [[从零设计生产级-Multi-Agent-Harness]]
date: 2026-07-27
source: 微信公众号「AI工程化」/ winkrun
---

# 图工程（Graph Engineering）来了？LangChain说不是新东西

- 原文链接：https://mp.weixin.qq.com/s/_uUffN2JEgASnLQNfDWSDw
- 来源：微信公众号「AI工程化」2026-07-23 18:39 推送 / 作者 winkrun
- 获取时间：2026-07-27 Asia/Shanghai

## 核心结论（一句话）

> **Graph Engineering 不是比 Prompt / Loop / Harness 更“新”的东西，它只是把 Agent 的真实依赖关系显式画出来：只有下一步真的读取上一步输出时才保留边；能预画路径的任务用图，路径本身需要探索的任务用 Harness。**

## 分类提炼
- 场景：Agent 拓扑设计 / 多步骤编排 / LangGraph 方法论
- 标签：#主题/AI-Agent #主题/Graph-Engineering #主题/LangGraph #主题/Harness #主题/Loop #主题/Agent-Topology #场景/公众号长文 #来源/AI工程化
- 类型：方法论拆解 / 拓扑选型 / 图编排解释层

## 知识节点（8 个独立概念）

- **线性Agent是退化图**：如果下游并不读取上游结果，串行链路只是把等待硬编码进流程。
- **节点契约**：每个节点都应有明确输入、输出和单一职责，最好用 schema 约束结构化返回。
- **数据契约边**：边应表达数据依赖而不是步骤顺序，命名要说明传递的是什么数据。
- **钻石拓扑**：fan-out → reduce → synthesize 是并行子任务最常见也最稳的图骨架。
- **验证器节点**：在结果进入下游前安排对抗验证、多视角审查或评委团打分，避免坏结果扩散。
- **有环图**：生产 Agent 很少是 DAG；重试、补问、验证回修和人工中断恢复都要求循环。
- **动态Send**：当工作项数量运行时才知道时，图必须能动态创建下游分支，而不是提前写死所有边。
- **图-vs-Harness**：路径可提前画出的任务适合图；路径本身需要探索的任务更适合 Harness 或 Deep Agent。

## 关联图谱

### 上游（基于 / 来自）
- [[0xCodez-Agent-Harness-14-Steps]]：把 Harness / Loop / Memory 的组合关系讲清，本文在此基础上把“拓扑”单独显化。
- [[Lilian-Weng-Harness-Engineering-自我改进]]：本文“节点里能装完整 Agent、图通常带环”的判断，可视为翁荔 5 段优化路径里的 workflow / harness 视角延伸。
- [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]：本文最后一段“让 Claude 自己画图”与动态 workflow 是同一条主线。

### 下游（应用于 / 验证于）
- [[从零设计生产级-Multi-Agent-Harness]]：把图拓扑落到多 Agent 编排、工具治理和状态管理的工程骨架。
- [[WorkBuddy-Harness工程复盘-从模型到可用Agent]]：把“图 / Context / Harness / Loop”进一步整合成产品级解释层。
- [[阿里云开发者-淘宝主播Agent的Harness工程实战]]：用 DAG / Reducer / Approval / Hook 等生产机制验证“图不是只画流程图”。

### 同级（横向 / 并列）
- [[Loop-Engineering-验证才是瓶颈]]：本文讲拓扑，Samuel 那篇讲验证闸门；两者拼起来才是闭环。
- [[未来属于垂直领域Agent]]：两篇都在回答“什么时候拆图、什么时候拆 Agent、什么时候别再堆一个大 Agent”。
- [[多Agent使用边界与并行判定]]：把本文“下一步是否真的读上一步输出？”收束成更日常的并行判定规则。

## 正文要点（6 条）

- **图工程的真正对象不是“图”，而是依赖关系**：Graph Engineering 只是把 Prompt / Context / Harness / Loop 背后的控制流问题显式化；新词不是重点，重点是把“哪一步真的依赖哪一步”画清楚。
- **设计边的第一问是“有没有真实读取”**：很多多步 Agent 被误画成 A→B→C→D，只因为人习惯顺序思考；如果 B 不消费 A 的结果，就不应该为它们保留边和等待。
- **稳定图靠契约，不靠更多 prompt**：节点要有输入/输出/单一职责，边要表达数据类型而不是先后顺序；路由用代码保证确定性，判断可用模型但控制流不要完全交给模型自由发挥。
- **生产图往往是有环的**：真实系统要重试失败工具、向用户补问、验证后回修、等待人工干预再恢复，这决定了生产 Agent 更像状态机而不是一次性的 DAG。
- **图的常用骨架可以直接复用**：并行适合独立任务；钻石拓扑适合 fan-out / fan-in；验证器节点适合在结果下游前设闸门；未知规模任务要配动态 Send 和“连续 K 轮无新发现”的停止条件。
- **Graph 不是 Harness 的替代物**：如果任务路径能提前画出来，用图最稳；如果路径本身需要探索，例如通用深度研究、开放式搜索或高度不确定的多轮委派，更合适的入口是 Harness / Deep Agent，而不是把探索硬塞进静态图里。

## 相关链接

- 原文：图工程（Graph Engineering）来了？LangChain说不是新东西
- LangChain 官方：3 Years of Graph Engineering with LangGraph
- [[0xCodez-Agent-Harness-14-Steps]]
- [[WorkBuddy-Harness工程复盘-从模型到可用Agent]]
- [[Loop-Engineering-验证才是瓶颈]]
- [[从零设计生产级-Multi-Agent-Harness]]

## 备注与限制

- **文章来源结构**：这是公众号解读稿，正文把 LangChain 官方博文、Codez 图工作流文章和作者个人评论揉在一起，不是单一一手原文直译。
- **最有价值的增量**：不是“图工程是新概念”，而是给出一套很实用的拓扑判定句和“图 vs Harness”分界线。
- **分类理由**：放 `01-ai-agents` 而不是 `02-ai-coding`，因为核心不是某个 coding 工具，而是 Agent 编排、状态机、图拓扑和任务选型。
