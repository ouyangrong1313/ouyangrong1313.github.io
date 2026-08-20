---
title: "Harness Inspector：让 Agent 交付过程可观察、可检查、可追溯"
category: 01-ai-agents
tags: [主题/AI-Agent, 主题/Harness, 主题/AI-Coding, 节点/交付证据链, 节点/可追溯交付, 节点/Skill-Discovery, 场景/开源项目, 场景/公众号长文]
nodes: [交付证据链, 意图过程产出, Workbench, Trace, Replay, 证据边界, Skill-Discovery, 稳定工作路径]
links: ["[[01-ai-agents/phodal-Better-Harness-任务级证据评估]]", "[[01-ai-agents/Loop-Engineering-验证才是瓶颈]]", "[[02-ai-coding/phodal-项目记住-Coding-Agent-5步法]]"]
date: 2026-08-17
source: "微信公众号「phodal」/ QoderAI Better Harness"
---

# Harness Inspector：让 Agent 交付过程可观察、可检查、可追溯

- 原文：https://mp.weixin.qq.com/s/1IkDdhFhpJQy3a9ABDuMsQ
- 作者：Phodal；项目：https://github.com/QoderAI/better-harness；获取时间：2026-08-17

## 核心结论（一句话）

> Skill 自动沉淀的前提不是更多会话日志，而是把需求、执行和提交连成保留证据边界的交付链，并从被产出与验证支持的稳定工作路径中筛选候选。

## 分类提炼

- 场景：Coding Agent 交付审查、会话回放、Harness 可观测性、Skill 自动沉淀
- 类型：开源工具能力说明 / Agent 工程方法论

## 知识节点（8 个独立概念）

- **交付证据链**：需求、会话、文件活动与提交需要关联，才能检查变化的缘由、过程和结果。
- **意图过程产出**：Story/Issue/Spec 是 Intent，Session 是 Process，Commit 是 Output。
- **证据图**：真实交付常为多对多映射，不应被压成单一时间线。
- **Workbench**：核对需求、Session 与 Commit 已观测关系的整体视图。
- **Trace**：以 Turn 组织输入、回复、调用与文件活动的工作轨迹视图。
- **Replay**：按已记录事件顺序回看交付的只读视图。
- **证据边界**：关系不足时保留候选或未映射，不把相邻记录推为因果。
- **稳定工作路径**：跨相似任务重复且被产出和验证支持的路径，才适合升级为 Skill 候选。

## 从会话日志到可审查交付

原文将 Session 从评估对象降为过程证据：它能记录搜索、读取、修改和验证，却不能独自回答任务为何开始，也不能证明哪些动作进入工程系统。Inspector 以 Intent、Process、Output 重新组织 Story/Issue/Spec、Session 与 Commit；审查应先核对意图和结果的映射，再读执行细节。

## 三种视图与边界

| 视图 | 回答的问题 | 约束 |
| --- | --- | --- |
| Workbench | 对象间有哪些关系 | 不补全证据不足的映射 |
| Trace | 会话活动如何组织 | 不还原未暴露的推理 |
| Replay | 事件以何种顺序发生 | 不重跑工具或恢复工作区 |

## Skill 候选的筛选规则

高频调用并不等于可复用：重复读取可能是上下文不足，失败重试可能只是噪声。候选路径至少要在相似任务中重复出现，并能说明适用场景、上下文边界、执行步骤和验证方式，且由最终产出与验证共同支持。

## 证据边界

- 原文把 Inspector 描述为本地只读工作台；本文未独立运行 CLI、公开样本或代码实现。
- 映射应理解为可观测关联，不应直接推断完整因果链。
- 缺失时间或思考记录时，应保留顺序与未知项，而非以当前状态回填历史。

## 关联图谱

### 上游（基于 / 来自）
- [[01-ai-agents/phodal-Better-Harness-任务级证据评估]]：从任务级证据评估延展到具体交付的阅读与审查。
- [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]：解释为什么重复行为必须由结果与验证约束。

### 下游（应用于 / 验证于）
- [[02-ai-coding/phodal-项目记住-Coding-Agent-5步法]]：稳定路径可进一步判断写入 AGENTS.md、Skill、CLI 或 Loop 的位置。

### 同级（横向 / 并列）
- [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]：产品化 Harness 分层视角，与本文交付证据视角互补。

## 相关链接

- [原文](https://mp.weixin.qq.com/s/1IkDdhFhpJQy3a9ABDuMsQ)
- [项目](https://github.com/QoderAI/better-harness)
- [原文归档](../../raw/phodal-Harness-Inspector-Agent交付可观察可检查可追溯.md)
- [速读摘要](../../raw/phodal-Harness-Inspector-Agent交付可观察可检查可追溯-digest.md)
