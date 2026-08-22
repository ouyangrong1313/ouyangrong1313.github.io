---
title: 图工程（Graph Engineering）来了？LangChain说不是新东西（速读摘要）
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Graph-Engineering
  - 主题/LangGraph
  - 主题/Harness
  - 主题/Loop
  - 主题/Agent-Topology
  - 场景/公众号长文
  - 来源/AI工程化
type: digest
date: 2026-07-27
source: 微信公众号「AI工程化」2026-07-23 推送 / winkrun
原始链接: https://mp.weixin.qq.com/s/_uUffN2JEgASnLQNfDWSDw
nodes: []
---

# 图工程（Graph Engineering）来了？LangChain说不是新东西（速读摘要）

> **一句话**：Graph Engineering 不是新物种，而是按真实数据依赖重画 Agent 拓扑：边只在真正读到上游输出时才存在；图适合可预画路径，Harness 适合开放探索。

## 8 节点速查表

| 节点 | 一句话定义 |
|---|---|
| 线性Agent是退化图 | 不读上游输出的串行链路，本质是在浪费等待时间 |
| 节点契约 | 节点必须有明确输入、输出和单一职责 |
| 数据契约边 | 边表示数据依赖，而不是“第几步” |
| 钻石拓扑 | fan-out → reduce → synthesize 是并行骨架 |
| 验证器节点 | 结果进入下游前先过对抗验证或多视角审查 |
| 有环图 | 生产 Agent 要支持重试、补问、回修和恢复 |
| 动态Send | 运行时才知道工作规模时，必须动态生成分支 |
| 图-vs-Harness | 可预画路径用图；路径需探索用 Harness |

## 3 个关键模式

- **钻石拓扑**：先拆任务，再并行执行，最后合并结论，适合研究、审查、迁移等场景。
- **验证器节点**：把 reviewer / critic / judge 做成显式节点，比最后统一返工更稳。
- **动态Send**：当输入规模或任务数运行时才确定时，不要把边提前画死。

## 3 个反直觉点

1. **生产图通常不是 DAG**：重试、追问和恢复都要求环。
2. **Loop 不是图的对立面**：一个循环本身就是一个有向有环图。
3. **路由尽量代码化**：模型负责判断，控制流尽量交给代码保证确定性。

## 5 个对 Seetong / MyAIWiki 可借鉴动作

1. **并行前先问一句**：下游是否真的读取上游输出？
2. **子 Agent 返回统一结构**：优先 schema，不要默认自由文本。
3. **把验证器做成节点**：review / critic / judge 独立复用。
4. **未知规模任务设停止条件**：例如连续 K 轮没有新发现就停。
5. **开放探索任务别强上静态 DAG**：深度研究、排障和搜索优先走 Harness。

## 关联 + 备注

**关联**：[[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] / [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]] / [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] / [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] / [[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]] / [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]]

**备注**：本文最强的部分不是“Graph Engineering”这个名词，而是那句很能落地的判定句：**只有下一步真的读取上一步输出时，边才成立。**
