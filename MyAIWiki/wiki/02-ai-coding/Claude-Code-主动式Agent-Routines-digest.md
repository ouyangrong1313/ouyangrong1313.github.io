---
title: Claude Code 主动式 Agent Routines - Digest
category: 02-ai-coding
date: 2026-06-17
source: 微信公众号 Capihom 2026-06-17 编译
source_url: https://mp.weixin.qq.com/s/kvtDAdTe2H4hTUXc3FEaVg
main_entry: [[Claude-Code-主动式Agent-Routines]]
---

# Claude Code 主动式 Agent Routines — Digest

## 一句话总结

**主动式 Agent 不该等你按回车才开始工作。** Anthropic Routines 最小配置 = prompt + repo + connector + trigger 四样;**主动式 Agent 三大设计问题**:触发器 + 上下文 + 可转向性;**渐进路径**:先调查建议,再放行动权限。

## 速查表

**核心命题**:AI 提效从"写好 prompt"转向"把稳定流程设计成可触发、可观察、可校验的系统"
**核心金句 4 条**:① 编码 agent 不该等你按回车 ② Claude 拥有什么上下文,就能做到哪一步 ③ 主动式 agent 不要求人消失,要求人能叫停 ④ proactive agents beat reactive agents
**关键数字**:Routines 最小配置 4 样 / Claude Code 每周 PR 增 200% / 内部文档 routine 每周一上午 10 点跑

## 反直觉 5 个

1. 主动式 agent 成熟形态不要求人消失,要求人能叫停
2. AI 判断不稳定根因往往不是模型态度,是流程没把信息接进来
3. 主动式 agent 不是黑箱后台,是可打开的协作文档
4. AI 提效从"写好 prompt"转向"流程可触发/可观察/可校验"
5. proactive agents beat reactive agents(问题出现时先开始调查)

## 5 个对 Seetong 团队可借鉴动作

1. **Seetong 现有 cron 流程从"写好 prompt 跑一次"升级为"Routines 思路"** — 加托管 + 触发器 + 上下文声明 + 可转向入口
2. **设 Seetong Agent 三大设计问题 checklist** — 触发器 + 上下文 + 可转向性,每个新 Skill 上线前必填
3. **建立"上下文=成功的上限"作为 Seetong Agent 设计原则** — 列每个 Skill 的输入源清单
4. **设"小处先赢"渐进路径** — 挑每周重复 + 输入稳定 + 需人确认的流程,跑顺后再加下一个
5. **借鉴 Anthropic 内部 Sarah 文档同步 routine 模式** — Seetong-tps 跨端版本说明 / 内部 SDK changelog 同步

## 关联

**主条目**:[[Claude-Code-主动式Agent-Routines]]
**上游**:[[Claude-Code首席设计师Meaghan-Choi工作流]] / [[Claude-Code一周年回顾-Boris-Cat]] / [[Anthropic万字长文三个判断和一个阳谋]] / [[claude-code-dynamic-workflows]]
**下游**:[[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]] / [[Agentic-Engineering-AI-Workbench]]
**同级**:[[Claude-Code之父品味不是人类护城河]] / [[Claude-Code作者Boris-28分钟教你写真正有效的Prompts]]

## 备注

- 速读版:核心结论 + 反直觉 + Seetong 借鉴动作 + 关联指针
- 完整编译页:同目录 [[Claude-Code-主动式Agent-Routines]]
- 演讲原视频:https://www.youtube.com/watch?v=eSP7PLTXNy8 (比浓缩稿更完整,含 Maya 现场演示和问答)
