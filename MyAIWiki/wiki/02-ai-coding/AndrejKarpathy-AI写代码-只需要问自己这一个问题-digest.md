---
title: Andrej Karpathy：AI写代码，只需要问自己这一个问题 - Digest
date: 2026-07-15
slug: AndrejKarpathy-AI写代码-只需要问自己这一个问题-digest
category: 02-ai-coding
tags:
  - Karpathy
  - AI-Coding
  - Skill
  - GitHub工作流
  - 判断执行分界
rating: ⭐⭐
source: "[[02-ai-coding/AndrejKarpathy-AI写代码-只需要问自己这一个问题]]"
nodes: []
---

# Andrej Karpathy：AI写代码，只需要问自己这一个问题 - Digest

## 一句话总结

**先问“思考到底发生在哪一步”再决定要不要交给 AI**。Karpathy 用一句话给 AI Coding 任务分流，rvaniaaa 用 8 段 GitHub 技能蒸馏流水线把“人做判断，AI 做执行”做成了会持续长技能的 Agent 机制。

## 8 节点速查表

| # | 节点 | 一句话 |
|---|---|---|
| 1 | 思考发生点 | AI Coding 先问“思考到底发生在哪一步” |
| 2 | 判断执行分界 | 判断没完成的任务留给人，执行型任务交给 AI |
| 3 | 双资深一致 | 两个资深工程师会写出近似实现的活，通常适合 AI |
| 4 | 工作流档位切换 | 自己写 / 补全 / 全代理只是同一问题的三档模式 |
| 5 | Scout-Filter-Reader | 搜仓库、去噪、文档优先读取，最后才进源码 |
| 6 | Workflow-Extractor | 真正要沉淀的是可复用 workflow，不是整仓库 |
| 7 | Skill-Score | 是否变成 Skill，优先用确定性规则打分 |
| 8 | Reviewer-Publisher | 生成与审核分离，自动化提议，人类批准 |

## 5 句核心金句 + 3 个反直觉点

1. “思考到底发生在哪一步？”
2. 判断没完成的任务，不要假装能外包给 AI。
3. 两个资深工程师会收敛到近似实现的活，通常才适合 Agent 接管。
4. 不是每个环节都该交给 LLM，能写成确定性规则的地方越多越稳。
5. 自动化负责提议，人类负责批准。

**3 个反直觉点**

- 争论“自己写 / 补全 / 全代理谁更先进”没意义，它们只是不同判断密度下的三档工作模式。
- Agent 不会自己变聪明，真正缺的不是模型能力，而是“发现 Skill → 抽 workflow → 审核发布”的外循环。
- 读仓库最省 token 的方式不是更短摘要，而是先读 README / docs / examples，很多时候根本不用进源码。

## 5 个对 Seetong / MyAIWiki 可借鉴动作

1. 所有 AI Coding 任务先加一个“判断密度”分流：需求 / 架构类默认人主导，执行类默认 AI 主导。
2. 把“双资深一致”写进 Skill / 任务模板：若实现分歧仍大，就别直接交给 Agent。
3. Reader 默认按 README → docs → examples → 依赖 → 源码顺序读取，先省 token 再省误判。
4. Skill 入库前把生成、评分、审核拆开，避免“自己写自己批”。
5. MyAIWiki 后续可把高质量 GitHub workflow 当成候选源，定期编译成知识页或 Skill 草稿。

## 关联 + 备注

**关联**：AI Coding 边界 [[02-ai-coding/AI-Coding的顿悟时刻]] / [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]] | Skill 工程 [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]] / [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]] / [[01-ai-agents/Skill-Self-Evolution]] | 验证 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]

**备注**：本文前半段是 Karpathy 判断框架，后半段是 rvaniaaa 项目拆解；公众号末尾引流、小程序、点赞分享等交互噪声已剔除。
