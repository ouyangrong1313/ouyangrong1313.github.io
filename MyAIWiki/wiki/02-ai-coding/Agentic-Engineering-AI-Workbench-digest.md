---
title: "Agentic Engineering 实战 - Digest"
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Native, #主题/工作台, #主题/Harness, #主题/权限治理, #节点/AI工作台五层, #节点/plan-md, #节点/CLAUDE-md, #节点/Skill过程资产, #场景/编译长文, #场景/工程团队]
nodes: [AI-工作台五层, 可控并行, plan-md任务协议, 5层上下文3档载入, CLAUDE-md三段式, Skill-过程资产, Subagents-隔离原则, 团队3层权限]
links: [[Agentic-Engineering-AI-Workbench]]
date: 2026-06-09
source: 微信公众号 / 架构师 JiaGouX（若飞）—— 编译自 Matt Van Horn、John Kim、Kaxil Naik、Simon Willison、Addy Osmani 等多篇
---

# Agentic Engineering 实战 - Digest

- 原文链接：https://mp.weixin.qq.com/s/TTLaGn28owLQSy-cvEgPWw
- 来源：微信公众号 / 架构师 JiaGouX（若飞，编译）
- 发布时间：2026-06-08 23:20
- 获取时间：2026-06-09

## 一句话总结

**"Agent 面前摆着一张工作台"**——AI 工作台 = **计划 / 上下文 / 执行 / 验证 / 治理** 五层；个人可以 YOLO，团队必须把"任务卡 + 工作区隔离 + 可验证结果 + 合并规则"四件事说清楚后再多开 Agent；**CLAUDE.md 三段式、plan.md 任务协议、Skill = 过程资产、Subagents = 隔离、团队 3 层权限渐进**构成可落地的最小工作台。

## 8 个知识节点速查

| 节点 | 一句话 |
|---|---|
| **AI-工作台五层** | 计划 / 上下文 / 执行 / 验证 / 治理；每层"最小交付物"+"用来解决什么" |
| **可控并行** | 多开 Agent 之前的 5 问 + 每开一个 Agent 先写"任务卡" |
| **plan-md 任务协议** | 8 段核心 + 2 段进阶（证据要求/合并条件） |
| **5层上下文 × 3档载入** | 5 层分类 × 3 档投放；CLAUDE.md 重 Validation |
| **CLAUDE-md 三段式** | What / Domain / Validation（最值得花时间） |
| **Skill = 过程资产** | 不是最佳实践文档，是可执行流程；6+ 段式 |
| **Subagents = 隔离** | 独立可验型才拆；强耦合型留在主线 |
| **团队3层权限** | 只读 → 半自动 → 受控写入；接入真实系统前 5 行威胁模型 |

## 5 个金句

- > **"工作台搭得越清楚，Agent 干活越有边界。"**
- > **"上下文不是越多越好，更重要的是放对位置。"**
- > **"Agent 正在从代码助手变成执行层。"**
- > **"代码生成几乎免费以后，review 变成瓶颈。"**
- > **"Agent 会静默失败——错误输出经常看起来很合理。"**

## 4 个核心交付物（团队可直接抄）

1. **plan.md 8 段模板**（目标/不做什么/背景/可能涉及文件/实施步骤/验收标准/验证命令/当前状态）
2. **CLAUDE.md 三段式**（What / Domain / Validation，重 Validation）
3. **PR 模板**（目标/改动范围/验证证据/风险）
4. **权限表 + 5 行威胁模型**（按"读代码/跑测试/写本地/发 PR/访问 Slack/改生产/登录态网页"分级）

## 5 个最小行动（行动笔记）

1. 复杂任务留 `plan.md` 文件出口
2. `CLAUDE.md` 三段式，重 Validation
3. 把团队最容易漏掉的验证流程写成 Skill
4. hooks 第一版：挡一类危险命令 + 整理一类失败日志
5. Subagents：能独立探索/独立验证/只返回高密度结果的任务才拆

## 7 天小试点（中等复杂度 bug 修复）

| 天 | 动作 |
|---|---|
| 1 | 选任务 |
| 2 | 最小 `plan.md` |
| 3 | 一小段 `CLAUDE.md` |
| 4 | 隔离环境实现 |
| 5 | 认真做人工 review |
| 6 | 失败写回 gotchas |
| 7 | 看 4 问 + 5 指标 |

## 与已有文章的关联

- **强关联**（本篇是它们的"团队工程化版"）：
  - [[every-agentic-engineering-hack-2026-06]]（Matt Van Horn 个人 YOLO 母本）
  - [[claude-code-dynamic-workflows]]（plan = 动态可执行）
  - [[从Prompt-Context到Harness-工程的三次进化与终局之战]]（"上下文不是越多越好" = Harness 思想具体化）
  - [[Notion-spec-driven-AI-workflow]]（plan.md 的一种更严格形式：spec 进仓库 + verification）
  - [[AI-Coding的顿悟时刻]]（Spec→LDD + 工程师向两端收缩）
  - [[多Agent使用边界与并行判定]]（"可控并行 5 问"是更具体的可执行版）
  - [[任务类型到验证模板]]（PR 模板 = 验证证据前置）
  - [[买了一样的AI为什么别家的比你的强]]（Skill = 过程资产 = 组织内 skill 沉淀）
  - [[Claude-Code团队5条工作原则-Fiona-Fung分享]]（Trust but verify + 团队级 harness）
- **同级**：
  - [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]（plan.md 8 段结构可与 Spec-Kit spec.md 对照）
  - [[Claude-Code负责人谈AI原生工程组织]]
  - [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]]
  - [[54万行代码的顿悟-Markdown才是新编程方式]]（个人层 vs 团队层）
  - [[Anthropic万字长文三个判断和一个阳谋]]（"验收能力"主线，本篇是工程化落地版）
- **原始素材延伸**：
  - Matt Van Horn《Every Agentic Engineering Hack I Know》
  - John Kim《How I use Claude Code》(Meta Staff Engineer)
  - Kaxil Naik《I Haven't Written a Line of Code in 4 Months》
  - Simon Willison《Context engineering》
  - Addy Osmani《Agent Skills》（O'Reilly Radar）
