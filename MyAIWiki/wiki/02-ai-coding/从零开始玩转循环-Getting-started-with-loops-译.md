---
title: 从零开始玩转循环 (Getting started with loops)【译】
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/Claude-Code, #主题/Loop, #主题/工作流设计, #主题/验证, #节点/回合制循环, #节点/目标导向循环, #节点/时间基循环, #节点/主动式循环, #节点/停止条件, #节点/验证技能, #节点/Token边界, #场景/公众号长文]
nodes: [回合制循环, 目标导向循环, 时间基循环, 主动式循环, 停止条件, 验证技能, 触发器设计, Token边界]
links: [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[Claude-Code-主动式Agent-Routines]], [[claude-code-dynamic-workflows]], [[Agentic-Engineering-AI-Workbench]], [[Claude-Code一周年回顾-Boris-Cat]], [[Claude-Code作者Boris-我已经不写prompt了我写loop]], [[APPSO-Codex-Claude-Code-Loop-Engineering]], [[AI循环-Claude-GPT和Mira到底什么才是真正好用的]]
date: 2026-07-08
source: 微信公众号 / 宝玉AI（宝玉翻译 @delba_oliveira 原文）
---

# 从零开始玩转循环 (Getting started with loops)【译】

- 原文链接：https://mp.weixin.qq.com/s/lG4WU5sSykOVu4XMHtWq1g
- 原始来源：https://x.com/ClaudeDevs/status/2074208949205881033
- 来源：微信公众号 / 宝玉AI
- 发布日期：2026-07-07 12:26
- 编译时间：2026-07-08

## 核心结论（一句话）

Loop 不是“多问几轮 AI”，而是先定义触发器、停止条件、验证方式和成本边界，再按任务强度从 turn-based、`/goal`、`/loop` / `/schedule` 到 proactive 逐级升级。

## 分类提炼

- 场景：Claude Code / Loop 工程 / 工作流设计 / 公众号长文
- 标签：#主题/AI-Coding #主题/Claude-Code #主题/Loop #主题/工作流设计 #主题/验证 #场景/公众号长文
- 类型：Claude Code loop 入门分类法 / 官方工作流心法翻译稿

## 知识节点（5-10 个独立概念）

- **回合制循环**：每条 prompt 本质上都在触发一个 loop，适合短任务与探索性问题，核心是把人工检查尽量前移进 verifier。
- **目标导向循环**：`/goal` 的价值不在“多跑几轮”，而在于把完成定义外显，避免模型凭感觉过早收工。
- **时间基循环**：`/loop` 适合本地按时间轮询，`/schedule` 适合云端长期例行程序，关键在任务是否会持续接收外部输入。
- **主动式循环**：当 `schedule + goal + skills + dynamic workflows + auto mode` 被组合起来，AI 才像一个持续上班的岗位，而不是一次性对话。
- **停止条件**：没有 stop condition 的 loop 会退化成乐观的 while 循环，成本和漂移都会失控。
- **验证技能**：把人工验收步骤写进 `SKILL.md`，让 Claude 能看页面、点按钮、查控制台、跑性能指标，才算真正的闭环。
- **触发器设计**：事件触发通常优于盲目定时轮询，因为它更贴近外部世界的变化频率，也更省 token。
- **Token边界**：小任务用小模型、确定性工作用脚本、高频任务先试水再扩容，这是 loop 成本治理的基本盘。

## 关联图谱

### 上游（基于 / 来自）

- [[Addy-Osmani-Loop-Engineering]]：给出了 Loop Engineering 的 5+1 积木总框架，本文把它落成 Claude Code 视角下的 4 类 loop 分类法。
- [[Claude-Code一周年回顾-Boris-Cat]]：Boris / Cat 把“我不写 prompt，我写 loop”讲成产品心智，本文提供的是可执行的分类入口。
- [[Claude-Code作者Boris-我已经不写prompt了我写loop]]：同一主线下的作者视角补充，解释为什么 loop 会替代单轮 prompt 成为新默认。

### 下游（应用于 / 验证于）

- [[Claude-Code-主动式Agent-Routines]]：把本文的 time-based / proactive loop 继续产品化为 Routines。
- [[claude-code-dynamic-workflows]]：说明 proactive loop 里多 agent 编排、并行 worktree 和 reviewer judge 是怎么落地的。
- [[Loop-Engineering-详解-把反馈循环放进工程现场]]：把本文的 trigger / stop / verifier 思路扩展成中文工程实践中的任务卡、准入表和 7 天试点。

### 同级（横向 / 并列）

- [[Agentic-Engineering-AI-Workbench]]：从工作台 5 层结构看 loop 的上下文、执行、验证与治理控制面。
- [[APPSO-Codex-Claude-Code-Loop-Engineering]]：从产业视角解释为什么 2026 年大家都开始从 prompt 迁移到 loop。
- [[AI循环-Claude-GPT和Mira到底什么才是真正好用的]]：给出 loop 五步骨架与五个积木的轻量版入门表述，可与本文的 4 类分类法对照看。

## 正文要点（3-7 条）

1. **这篇文章把“loop 是什么”讲成了一个四维选择题。** 不要先问“要不要上自动化”，先问触发方式、停止条件、调用原语和任务类型是否匹配。这样 loop 不是玄学，而是控制面设计。

2. **Turn-based loop 不是低级版，而是默认版。** 你每次发 prompt，本来就在做 loop。它真正的升级点不是把 prompt 写得更复杂，而是把人工验收翻译成可执行的 skill 和 verifier，让 Claude 自己把检查跑完。

3. **`/goal` 的核心是防止“差不多就停”。** 对复杂任务，模型最常见的问题不是完全不会做，而是太早宣布完成。`/goal` 把成功标准和最大尝试次数都显式化，让 loop 在明确门槛前继续迭代。

4. **`/loop` / `/schedule` 解决的是“外部世界还在变”这件事。** 当任务是 PR 审查、CI 失败、Slack 汇总、用户反馈分诊这类持续流入输入的工作时，单轮对话已经不够。此时重点不是“能不能定时跑”，而是频率是否和输入变化速度一致。

5. **Proactive loop 不是单指令，而是组合系统。** `schedule + goal + skills + dynamic workflows + auto mode` 一起用，才接近“长期工作岗位”的形态。其难点从来不在“让 AI 去做”，而在“让它知道何时开始、何时停、如何自证、何时升级给人”。

6. **质量和成本的边界必须前置。** 干净代码库、第二个 reviewer agent、文档可达、失败教训回写规则、用脚本替代确定性推理、按任务匹配模型，这些都不是附属建议，而是 loop 能否进生产的前置条件。

## 相关链接

- [[Addy-Osmani-Loop-Engineering]]
- [[Loop-Engineering-详解-把反馈循环放进工程现场]]
- [[Claude-Code-主动式Agent-Routines]]
- [[claude-code-dynamic-workflows]]
- [[Agentic-Engineering-AI-Workbench]]
- [[Claude-Code一周年回顾-Boris-Cat]]
- [[Claude-Code作者Boris-我已经不写prompt了我写loop]]
