---
title: "Addy Osmani agent-skills 设计哲学 - Digest"
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/Skill, #节点/反合理化, #节点/统一骨架, #场景/方法论]
date: 2026-06-15
source: 微信公众号 / ColaAI
---

# agent-skills 设计哲学 — Digest

## 一句话总结

Chrome 团队 Lead 把"资深工程师工作流"打包成 **23 技能 + 7 命令**,治的是 AI 写代码"能跑但上生产就崩"的抄近路病;真正值钱的是 **4 个设计哲学 + 7 块统一骨架**,不是技能数量。

## 速查表

| 项 | 数字 | 含义 |
|---|---|---|
| Star | 58.9k | 4-27 时 23k → 6-15 时 58.9k |
| 技能 | 23 | 22 生命周期 + 1 元 |
| 命令 | 7 | `/spec /plan /build /test /review /code-simplify /ship` |
| 角色 | 3 | 评审员 / 测试 / 安全 |
| 清单 | 4 | 测试 / 安全 / 性能 / 无障碍 |
| 工具 | 8+ | Claude Code / Cursor / Codex 等 |

## 4 个杀手锏(设计哲学)

1. **流程而非文档** —— 技能=有步骤+检查点+退出条件的工作流
2. **反合理化** —— 每技能内置"借口→反驳"表,堵死 agent 跳步退路
3. **验证不可妥协** —— 每技能以"拿证据"收尾
4. **渐进式披露** —— SKILL.md 入口 + 引用按需加载

## 7 块统一骨架(每 SKILL.md 都有)

`名称+描述` → `概述` → `何时使用` → `流程` → `反合理化` → `危险信号` → `验证`

## 关键金句

- "AI agent 默认走最短路径——而最短路径,往往跳过了让软件可靠的所有步骤"
- "它的价值不在'让 AI 更聪明',而在'让 AI 更靠谱'"
- "靠谱比聪明值钱得多"

## 反直觉点

- 技能多不稀奇,**难的是让 agent 真的照做** —— 4 个设计哲学才是壁垒
- 验证是**拿证据**(测试/构建/运行数据),不是"看起来对"
- 23 技能不散架,靠的是**死板的模板化**

## 对 Seetong / OpenClaw 3 个可借鉴动作

1. **Skill 7 块骨架审计** —— 检查 30+ 现 Skill 是否都有"反合理化""危险信号"两节;缺的优先补
2. **`反合理化` 列入团队 SKILL.md 必填项** —— 写 5 个偷懒借口 + 团队标准反驳话术
3. **复用 7 命令到 Seetong 三端** —— `/spec /plan /build /test /review /ship` 接 TAPD 流转

## 关联

- 旧版(4-27):[[谷歌开源agent-skills]] 20 skills / 23k star
- 同主线:[[Addy-Osmani-Loop-Engineering]] | [[Loop-Engineering-详解-把反馈循环放进工程现场]] | [[APPSO-Codex-Claude-Code-Loop-Engineering]]
- 同形态:[[PM-Skills-Marketplace-产品经理必备skill]] | [[Agentic-Engineering-AI-Workbench]]
- 团队沉淀:[[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]]

## 备注

- 项目仓库:https://github.com/addyosmani/agent-skills
- 原文:https://mp.weixin.qq.com/s/ZU81MGzo5j0bwd6i7CfZCw
- 缺口:无真实团队 7 命令完整落地数据,Seetong 可作首批样板
