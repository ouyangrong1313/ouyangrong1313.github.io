---
title: Claude Code 主动式 Agent Routines — 速读摘要
slug: Claude-Code-主动式Agent-Routines-digest
date: 2026-06-17
source: 微信公众号 Capihom 2026-06-17 编译
raw: 2026-06-Claude-Code-主动式Agent-Routines.md
category: 02-ai-coding
---

# Claude Code 主动式 Agent Routines — 速读摘要

## 一句话总结

**主动式 Agent 不该等你按回车才开始工作。** Anthropic 在 Claude Code 里推出 Routines:让 Claude 按 cron / GitHub 事件 / webhook 主动启动远程会话,最小配置 = prompt + repo + connector + trigger 四样。**主动式 Agent 三大设计问题**:触发器(什么时候上班)/ 上下文(能读到哪些信息)/ 可转向性(人怎么介入和校正)—— 渐进路径 = 先让 Claude 做调查建议,再把行动权限一点点放出去。

## 核心观点 6 条

1. **AI 提效正在从"写好 prompt"走向"把稳定流程设计成可触发、可观察、可校验的系统"** — 流程一旦能写成触发器+上下文+校验方式,就不再是某人的熟练手法,而是团队可复用的生产机制
2. **主动式 Agent 三大基础设施负担**:agent 跑在哪里(本地会断,需托管)/ 什么时候触发(cron + endpoint + event 都要胶水)/ 人怎么介入(headless 会话不可见不可控)
3. **Routines 最小配置四样**:prompt + 连接的 repo + 可用连接器 + 触发器;运行在 Claude Code 托管基础设施上,笔记本开不开都不影响
4. **Claude 拥有的上下文 = 它能成功的上限** — 问题往往不在模型态度,而在流程没把必要信息接进来
5. **可转向性 Steerability = 主动式 Agent 的成熟形态** — 两种做法:agent-on-agent review / 人在中途进入会话(像终端里用 Claude Code 一样)
6. **渐进路径**:先让 Claude 做调查和建议,再把行动权限一点点放出去;**小处先赢,系统会慢慢长出来**

## 知识节点 8 个

- **主动式 Agent Proactive Agent**:不等按回车,在问题出现时自己开始调查
- **Routines**:Anthropic 在 Claude Code 里推出的"按日程/事件主动启动的远程会话"产品
- **三大基础设施负担**:跑在哪里(本地/托管/持久化/鉴权) / 什么时候触发(cron/endpoint/event 胶水) / 人怎么介入(可观察可转向可恢复)
- **Routines 最小配置**:prompt + repo + connector + trigger 四样
- **托管会话 Hosted Session**:运行在 Claude Code 托管基础设施,笔记本开不开都不影响
- **触发器 Trigger**:cron / GitHub event / webhook payload as context;越具体越能收紧任务边界
- **上下文 = 成功的上限 Context = Success Ceiling**:Claude 拥有什么上下文,就能做到哪一步
- **可转向性 Steerability**:agent-on-agent review / 人在中途进入会话;主动式 agent 不要求人消失,要求人能叫停

## 关键数字 / 事实

- **Claude Code 每周 PR 数从新年开始增长 200%**(Anthropic 内部数据)
- **Routines 最小配置**:4 样东西
- **Anthropic 内部案例**:文档同步 routine(Sarah 每周一上午 10 点跑) = 读 main 分支新变化 + 对照文档 repo + 开 PR
- **触发器类型**:时间表 / GitHub 事件 / Slack 反馈 / 部署完成 / webhook payload
- **Routine 形态**:左侧连接资源 + 右侧指令文本,session 里能看到 Claude 从源码/changelog/文档逐步查起
- **渐进路径**:deploy verifier 案例:先调查建议 rollback 决策 → 信任增加后让它参与回滚动作

## 反直觉点 5 个

1. **主动式 Agent 的成熟形态不要求人消失** — 更健康的形态是人能看到它为什么启动、读了什么、准备做什么,并且能立刻叫停
2. **AI 判断不稳定的根因往往不是模型态度,而是流程没把必要信息接进来** — 缺源码它无法判断功能变化,缺文档它开不了 PR,缺 Slack 它无法通知
3. **主动式 Agent 不是黑箱后台任务** — 可以像可打开的协作文档,记录初始指令/读取仓库/比较 changelog/最后创建 PR
4. **AI 提效正在从"写好 prompt"转向"把稳定流程设计成可触发、可观察、可校验的系统"** — 比多学十个提示词更接近组织能力
5. **proactive agents beat reactive agents** — 主动式 Agent 价值不在一次性回答更漂亮,在它能在问题出现时先开始调查

## 关键金句 6 条

- "编码 agent 不该等你按下回车才开始工作"
- "我们想把 Claude Code 从今天的工具,变成明天的队友"
- "Claude 拥有的上下文,就是它能成功的上限"
- "无论 Claude 拥有什么上下文,那就是 Claude 能成功的上限"
- "你可以在实时会话里问它问题,把它推向另一个方向"
- "proactive agents beat reactive agents"

## 对 Seetong 团队可借鉴动作 5 个

1. **把 Seetong 现有 cron 流程(seetong-daily-briefing / 周报)从"写好 prompt 跑一次"升级为"Routines 思路"** — 加托管会话 + 触发器配置表 + 上下文声明 + 可转向入口
2. **设 Seetong Agent 三大设计问题 checklist** — 触发器(什么时候开始) + 上下文(读哪些信息) + 可转向性(人怎么介入) — 每个新 Skill 上线前必填
3. **建立"上下文=成功的上限"作为 Seetong Agent 设计原则** — 列出每个 Skill 的输入源清单(GitHub issues? Slack 反馈? 数据看板? 已有 roadmaps?),缺哪一块就补
4. **设"小处先赢"渐进路径** — Seetong 不要一次设计十个自动化,挑一个每周重复 + 输入稳定 + 需人确认的流程(用户反馈归类 / Tapd 过期迭代关闭 / Crash 归类),跑顺后再加下一个
5. **借鉴 Anthropic 内部 Sarah 文档同步 routine 模式** — Seetong-tps 跨端版本说明 / Seetong 内部 SDK changelog 同步,设个每周 routine 自动对照文档并开 PR

## 关联图谱(只画三段)

**上游(基于 / 来自)**:
- [[Claude-Code首席设计师Meaghan-Choi工作流]] — 同一公司同系列产品,Meaghan Choi 演示 worktree 并行 + 全链路自动化
- [[Claude-Code一周年回顾-Boris-Cat]] — Routine 异步化 + Auto Mode 反直觉安全,Routines 是 Routine 异步化的产品化落地
- [[Anthropic万字长文三个判断和一个阳谋]] — Anthropic 战略主线,慢变量安全垫与本文"主动式 agent"是同主线
- [[claude-code-dynamic-workflows]] — 动态工作流的具体实现

**下游(应用于 / 验证于)**:
- [[Addy-Osmani-Loop-Engineering]] — 5+1 积木中的 Automations 就是 Routines 的方法论原典
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] — 4 入口(触发/沙箱/验收/账本)中"触发"对应本篇触发器设计
- [[APPSO-Codex-Claude-Code-Loop-Engineering]] — 产业同向共振,4 人物(Boris/Cat Wu/Tibo/Addy)同向信号
- [[Agentic-Engineering-AI-Workbench]] — 5 层结构工作台包含这种托管会话

**同级(横向 / 并列)**:
- [[Claude-Code之父品味不是人类护城河]] — Anthropic 战略主线另一视角
- [[Claude-Code作者Boris-28分钟教你写真正有效的Prompts]] — Boris Cherny 工作流方法论

## 备注

- **本演讲的特殊价值**:这是 Anthropic **第一次把 Routines 当作"产品定位"对外讲**——不只是"我会写 prompt",而是"我能不能把稳定流程设计成可触发、可观察、可校验的系统"
- **与本工作区主线强关联**:
  - Seetong OpenClaw HEARTBEAT / 简报 cron / 神策友盟反馈 dry-run / Login 成功率每日巡检 — 都是 Seetong 现有"主动式 agent"雏形
  - 5+1 积木的 Automations = Routines 的方法论抽象
  - 本文与 [[APPSO-Codex-Claude-Code-Loop-Engineering]] 的"4 个对 Seetong 可借鉴动作"高度对应
- **本演讲对 Seetong 团队的最大价值**:不是技术方案,而是"主动式 agent 三大设计问题(触发器/上下文/可转向性)"框架 — 直接可用作 Seetong Skill 设计 checklist
- **未在文中出现但 Maya 反复强调的反问句**:"你的 routine 应该在什么时候触发?Claude 拥有什么上下文?人怎样介入?"
