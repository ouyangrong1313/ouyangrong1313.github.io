---
title: AI 第二大脑 Claude+Obsidian 10 步完整实操指南 - Digest
category: 02-ai-coding
date: 2026-06-22
source: X 推文 / @undefinedKi
---

# AI 第二大脑 Claude+Obsidian 10 步完整实操指南 - Digest

## 一句话总结

把 Karpathy 2026-04 提出的 LLM Wiki 模式，**从概念落地为"一个晚上能搭完"的 10 步实操**——Claude Desktop + Obsidian + Local REST API + mcp-obsidian + CLAUDE.md + 项目级 vault + Skill + Schedule，把对话型 AI 升级为"记忆永不丢失、每天自我整理"的个人第二大脑。

## 5 条核心观点

1. **MCP + Local REST API 是关键拼图**——Claude 用 `mcp-obsidian` 接 Obsidian 本地 REST API（端口 27124），从此 Claude 能读写 vault 里每个 .md 文件；**必须 Pro 付费版**才有 Code Tab
2. **CLAUDE.md = 策略层，项目文件夹 = 执行层**——根 CLAUDE.md 写"我是谁"，项目 CLAUDE.md 写"这一项目的目标"；**大库规划、单项目出活**
3. **Inputs/Process/Outputs/Feedback 四区项目结构**——所有项目统一这套文件夹；**重复任务做成 Skill**：下次一句"跑 xxx skill"就执行
4. **vault 维护做成 Schedule 任务**——每天 7:00 让 Claude 自动跑"整理 + 链接 + 过时标注 + 3 行变化摘要"；**你醒来时，脑已整理过**
5. **keys, not prompts**——权限控制走只读 scoped key，不靠"别删文件"的提示词；**只要技术上能删，假设终有一天会删**

## 10 步流程（精简）

| # | 阶段 | 核心动作 |
|---|---|---|
| 1 | 装 Claude Desktop | 必须 Pro 付费，启用 Code Tab |
| 2 | 装 Obsidian 建 vault | 文件夹即第二大脑；用 `[[链接]]` 体会 wikilink |
| 3 | 装 Local REST API 插件 | 复制 API Key |
| 4 | `claude mcp add-json obsidian-vault` | 把 key 写进环境变量 |
| 5 | 让 Claude 面试你写 CLAUDE.md | 一次性建好"我是谁" |
| 6 | 建项目文件夹（Inputs/Process/Outputs/Feedback） | 每个项目自带一个 CLAUDE.md |
| 7 | "Open folder as a vault" | 单项目隔离上下文 |
| 8 | 重复任务做成 Skill | "I want to turn this into a reusable skill..." |
| 9 | 接实时数据（Calendar/Gmail/Slack） | MCP `mcp add google-workspace`，只读权限 |
| 10 | Schedule 任务 | 每天 7:00 自动整理 vault |

## 5 句核心金句

1. **"You are not building a Claude setup. You are building your own memory, and it gets smarter every day you feed it."**
2. **"An empty brain is useless. Fix that first, and don't type it all out by hand. Make Claude interview you."**
3. **"The big vault plans. A single project ships."**
4. **"Always grant read-only where you can, the brain should read your data, not delete it."**
5. **"Same subscription. Completely different machine."**

## 5 个对 Seetong / MyAIWiki 可借鉴动作

1. **MyAIWiki 本库是 Karpathy Wiki 模式的实操实例**——raw + wiki + log + index + CLAUDE.md 五层结构，跑通 4 月以来
2. **晨间简报升级为 Schedule 任务**——把 [[MyAIWiki写入规范与验证模板]] 的"晨间简报"做成 Claude Desktop Schedule 任务
3. **每个 Seetong 项目独立 vault**——`/Volumes/work/sdks/seetong-tps/CLAUDE.md` 单独写角色，全局 CLAUDE.md 不污染
4. **重复任务做 Skill 而非提示词**——seetong-bug-triage / seetong-prd-review / seetong-weekly-report 补统一骨架
5. **权限走 Key 不走 prompt**——Seetong-TAPD 工具接 read-only scope；OpenClaw 默认只读，删除/推送走人工审批

## 关联图谱（精简）

- **上游**：[[karpathy-knowledge-system]] / [[claude-obsidian-second-brain]]（5/12 旧版）/ [[obsidian-claude-code-os]] / [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] / [[garry-tan-ai-second-brain]] / [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]
- **下游**：MyAIWiki 本库 + 三个开源 ready-made 仓库（claude-obsidian / obsidian-second-brain / second-brain-starter）+ Claude Desktop Schedule
- **同级**：[[Claude-Code-主动式Agent-Routines]] / [[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]]

## 备注与限制

- 原文 6/20 发布，385.6万 浏览；**本工作区已有 6 篇相关页面**，本文价值在"10 步完整实操"+"Schedule"+"keys-not-prompts"
- 关键工具栈：Claude Desktop（Pro $20/月）+ Obsidian（免费）+ Local REST API 插件 + mcp-obsidian + Schedule
- **ridark_eth 短推文**（16M 浏览）是本文的引用推广，作为"舆论扩散信号"存档
- 详细版本：见同目录 [[undefinedKi-AI-Second-Brain-10-Step-Guide]]
