---
title: "规范驱动开发：Notion 的 AI 工程工作流程 - Digest"
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/SDD, #主题/Harness, #主题/DevX, #节点/规范驱动开发, #节点/Codex, #节点/Boxy, #场景/编译长文]
nodes: [Spec-driven-Development, Whisper-Codex流水线, 救CI, Standup-Prep自动化, Boxy-@Codex出PR, 我不懂PR评审, Spec-Verification, 工程师角色重构]
links: [[Notion-spec-driven-AI-workflow]]
date: 2026-06-09
source: 微信公众号 / Capihom（编译自 Latent Space《How I AI》播客，嘉宾：Notion 工程师 Ryan Nystrom）
---

# 规范驱动开发：Notion 的 AI 工程工作流程 - Digest

- 原文链接：https://mp.weixin.qq.com/s/3tD61I6xLWpjoOrF6goewA
- 来源：微信公众号 / Capihom（编译自 Latent Space《How I AI》播客，嘉宾：Notion 工程师 Ryan Nystrom）
- 发布时间：2026-06-08 22:00
- 获取时间：2026-06-09

## 一句话总结

**Spec-driven development 不是给团队平白多一层负担，而是把"原本就在做但停在会议等待区的设计文档"第一次变成 agent 的施工说明书和可执行工程资产**——Ryan 在 Notion 已经跑通"Whisper 说意图 → Codex 写 spec → @Codex 出 PR + 验证截图 → spec 进仓库做 change log"的完整流水线。

## 三大主线

1. **入口范式**：先说清楚，再写代码（Whisper → Codex 写 spec → "Build it"）
2. **流水线改造**：Standup prep 自动化 / @Codex 出 PR / Spec 进仓库成为可执行资产
3. **角色重构**：工程师 = 系统思考者 + 架构师，重心从手工 plumbing 挪到验证/边界/自证工具

## 8 个知识节点速查

| 节点 | 一句话 |
|---|---|
| **Spec-driven Development** | 文档不再是会议材料，是写进仓库、带验证计划的工程资产 |
| **Whisper→Codex 流水线** | 语音说意图 → Codex 写 spec → "Build it" |
| **救 CI / DevX** | 慢 CI = 一次等待卡住整个验证回路 = AI 采用问题 |
| **Standup Prep 自动化** | Notion AI agent 拉 24h 多源信息生成 preread |
| **Boxy / @Codex 出 PR** | Notion 评论 @Codex → 10 分钟出 PR + 预览 + 验证截图 |
| **"我不懂" PR 评审** | 承认不懂发给 agent = 有效 debug；从社交阻力里拽出 code review |
| **Spec Verification** | spec 底部明确写 verification = 文档成可执行资产 |
| **工程师角色重构** | 系统思考者 + 架构师；重心在 spec/验证/边界/自证 |

## 5 个金句

- > "我真的不知道这里在干什么，你得像给 5 岁小孩讲一样解释给我听。"
- > "我不是 CI 专家，但我大概知道自己想要什么。"
- > "你的 AI、你的 agent，不会因为你在开会前 5 分钟让它做这件事而抱怨。"
- > "spec 就是事实来源。"
- > "我把我们的工作看成是在变成系统思考者和架构师。"

## 3 步可借鉴动作

1. **挑一段最重复的流程**（standup 预读 / 评论触发 PR / 老设计文档改写为可执行 spec）先打通
2. **先打通一小段，再把整条链路慢慢换掉**——阻力会小很多
3. **把 spec 放进 repo**——改功能时先改 spec，再让 agent 回头改代码

## 与已有文章的关联

- **强关联**：
  - [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]（工具/方法论对照）
  - [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]]（SDD 工具谱系坐标）
  - [[AI-Coding的顿悟时刻]]（Spec→LDD 流水线 + 工程师向两端收缩）
  - [[Claude-Code团队5条工作原则-Fiona-Fung分享]]（验证/评审/安全瓶颈转移）
  - [[Anthropic万字长文三个判断和一个阳谋]]（"验收能力"的一线落地版）
- **同级**：
  - [[Claude-Code负责人谈AI原生工程组织]]
  - [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]]
  - [[54万行代码的顿悟-Markdown才是新编程方式]]（个人层 vs 组织层）
  - [[买了一样的AI为什么别家的比你的强]]（spec 仓库 = 一种"组织级 skill"）
