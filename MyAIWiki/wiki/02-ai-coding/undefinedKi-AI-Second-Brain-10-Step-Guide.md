---
title: AI 第二大脑 Claude+Obsidian 10 步完整实操指南
category: 02-ai-coding
date: 2026-06-22
source: X 推文 / @undefinedKi（Yarchi）
source_url: https://x.com/undefinedKi/status/2068306794116501544
quote_source: https://x.com/ridark_eth/status/2068753952850546985
tags: [#主题/AI-Coding, #主题/效率, #主题/Claude-Code, #主题/Obsidian, #主题/第二大脑, #节点/LLM-Wiki, #节点/MCP, #节点/项目级Vault, #节点/Skill, #节点/Schedule, #节点/权限控制, #节点/keys-not-prompts, #节点/Karpathy, #手法/教程式结构, #手法/权限优先, #场景/技术博客]
nodes: [第二大脑, LLM-Wiki, MCP连接, 项目级Vault, Skill化重复任务, Schedule自动维护, 权限控制优先, Claude-Desktop配置]
links: [[karpathy-knowledge-system]], [[claude-obsidian-second-brain]], [[obsidian-claude-code-os]], [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]], [[garry-tan-ai-second-brain]], [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]], [[Claude-Code-主动式Agent-Routines]], [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[APPSO-Codex-Claude-Code-Loop-Engineering]]
---

# AI 第二大脑 Claude+Obsidian 10 步完整实操指南

- **原文**：https://x.com/undefinedKi/status/2068306794116501544 ｜ **引用推广**：https://x.com/ridark_eth/status/2068753952850546985（@ridark_eth，16M 浏览）
- **作者**：Yarchi（@undefinedKi）｜ **发布日期**：2026-06-20 ｜ **抓取**：2026-06-22
- **数据**：385.6万 查看 / 9,297 书签 / 2,044 转发

## 核心结论与分类

> **把 Karpathy 2026-04 提出的 LLM Wiki 模式，从概念压成"一个晚上能搭完"的 10 步实操**——Claude Desktop（Pro 付费）+ Obsidian + Local REST API + mcp-obsidian MCP + CLAUDE.md + 项目级 vault + Skill + Schedule，把对话型 AI 升级为"记忆永不丢失、每天自我整理"的个人第二大脑。**核心反直觉**：1）**"keys, not prompts"**——权限走只读 scoped key，不靠"别删文件"的提示词；2）**"The big vault plans. A single project ships."**——大库规划、单项目独立打开成 vault 才出活；3）**"You are not building a Claude setup. You are building your own memory."**——同订阅完全不同的机器。

- **分类**：02-ai-coding（Claude Code 工具实操 + 知识管理落地）
- **本工作区已有 6 篇相关页面**（[[karpathy-knowledge-system]] 概念原典 / [[claude-obsidian-second-brain]] 5-12 旧版 718万 / [[obsidian-claude-code-os]] / [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] / [[garry-tan-ai-second-brain]] / [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]）——本文价值在"10 步完整实操"+"Schedule"+"keys-not-prompts"，**是 2026-06 真正可以"开箱即用"的最新版实操指南**
- **节点数**：8

## 8 个知识节点

| 节点 | 一句话定义 | 关键洞察 |
|---|---|---|
| **第二大脑** | 让 Claude 持久记住你所有写过的内容 | vault = 你的记忆；Claude = 在记忆上运行的大脑 |
| **LLM-Wiki** | Karpathy 2026-04 提的"LLM 持续维护的 markdown 知识库"模式 | raw（只读素材）+ wiki（LLM 编译 + 链接）+ Schema（CLAUDE.md 维护规则） |
| **MCP连接** | `mcp-obsidian` 接 Obsidian 的 Local REST API（端口 27124） | Claude Code Tab 配合 mcp-obsidian 跨进程读写 .md 文件 |
| **项目级Vault** | "Manage vaults → Open folder as a vault" 把单项目独立打开 | Claude 只读那个项目的 CLAUDE.md，避免上下文污染 |
| **Skill化重复任务** | "I want to turn this into a reusable skill..." 一次描述、永久复用 | Inputs/Process/Outputs/Feedback 四区项目结构 |
| **Schedule自动维护** | Claude Desktop Schedule 任务，每日 7:00 自动跑"整理 + 摘要" | 你醒来时，脑已整理过一遍；OpenClaw HEARTBEAT 同方向 |
| **权限控制优先** | keys, not prompts——read-only scoped key 控制访问 | 只要技术上能删，假设终有一天会删；Gmail/Calendar 一律 read-only |
| **Claude-Desktop配置** | Pro 付费版（$20/月）才有的 Code Tab | 免费版没有 Code Tab，10 步法跑不通 |

## 10 步流程（精简）

| # | 阶段 | 核心动作 |
|---|---|---|
| 1 | 装 Claude Desktop | 必须 Pro 付费，启用 Code Tab |
| 2 | 装 Obsidian 建 vault | 文件夹即第二大脑；用 `[[链接]]` 体会 wikilink |
| 3 | 装 Local REST API 插件 | 复制 API Key（不包含 "Bearer" 前缀） |
| 4 | `claude mcp add-json obsidian-vault` | 把 key 写进环境变量（端口 27124） |
| 5 | 让 Claude 面试你写 CLAUDE.md | 一次性建好"我是谁"，不再重复解释 |
| 6 | 建项目文件夹（Inputs/Process/Outputs/Feedback） | 每个项目自带一个 CLAUDE.md |
| 7 | "Open folder as a vault" | 单项目隔离上下文（避免大库污染） |
| 8 | 重复任务做成 Skill | "I want to turn this into a reusable skill..." |
| 9 | 接实时数据（Calendar/Gmail/Slack） | `mcp add google-workspace`，只读权限 |
| 10 | Schedule 任务 | 每天 7:00 自动整理 vault |

**详细命令与提示词模板见 raw 原文**：`raw/2026-06-22-undefinedKi-AI-Second-Brain-10-Step-Guide.md`

## 5 个对 Seetong / MyAIWiki 可借鉴动作

1. **MyAIWiki 本库是 Karpathy Wiki 模式的实操实例**——raw/articles/notes/ + wiki/ + log.md + index.md + CLAUDE.md + scripts/，跑通 4 月以来；可对外做"现成 demo"案例
2. **晨间简报升级为 Schedule 任务**——把 [[MyAIWiki写入规范与验证模板]] 的"晨间简报"做成 Claude Desktop Schedule 任务，升级为"自动 ingest + 跨节点碰撞 + 3 行变化摘要"
3. **每个 Seetong 项目独立 vault**——`/Volumes/work/sdks/seetong-tps/CLAUDE.md` 单独写角色，全局 CLAUDE.md 不污染；学 Step 7 "Open folder as a vault" 的隔离
4. **重复任务做 Skill 而非提示词**——seetong-bug-triage / seetong-prd-review / seetong-weekly-report 补统一骨架"何时触发 + 输入输出 + 验证方式 + 反合理化"
5. **权限走 Key 不走 prompt**——Seetong-TAPD 工具接 read-only scope；OpenClaw 所有 agent 工具默认只读，删除/推送走人工审批

## 关联图谱

### 上游（基于 / 来自）

- [[karpathy-knowledge-system]] — Karpathy 2026-04 原始概念
- [[claude-obsidian-second-brain]] — 5/12 旧版翻译（718万 查看），本文是"6/20 实操升级版"
- [[obsidian-claude-code-os]] / [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] / [[garry-tan-ai-second-brain]] / [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]

### 下游（应用于 / 验证于）

- **MyAIWiki 本库** — 这套模式的自运行实例
- **三个开源 ready-made 仓库**：claude-obsidian（AgriciDaniel，4 角色预设）/ obsidian-second-brain（eugeniughelbur，43 命令，跨 Claude/Codex/Gemini）/ second-brain-starter（coleam00）
- **Claude Desktop Schedule** — Schedule 任务的产品化形式

### 同级（横向 / 并列）

- [[Claude-Code-主动式Agent-Routines]] — Anthropic Routines 是"主动式 Agent"产品化形式，Schedule 任务是其子集
- [[Addy-Osmani-Loop-Engineering]] — 5+1 积木的 Automations = 本文 Schedule 任务的方法论原典
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]]

## 备注与限制

- **本文的特殊价值**：把 Karpathy 4 月的"概念"压成"6/20 的实操"——一个晚上能搭完；这是 2026-06 真正可以"开箱即用"的最新版实操指南
- **关键工具栈**：Claude Desktop（Pro $20/月）+ Obsidian（免费）+ Local REST API 插件（端口 27124）+ `mcp-obsidian` MCP 工具 + `claude mcp add google-workspace` 实时数据 + Claude Desktop Schedule 任务
- **ridark_eth 短推文**（https://x.com/ridark_eth/status/2068753952850546985，16M 浏览）是本文的引用推广，作为"舆论扩散信号"存档
- **本工作区 SEETONG 主线强关联**：MyAIWiki 本库结构 = 论文 Step 1-4 实操实例；现有 cron = Step 10 Schedule 早一代形态；Seetong 项目级 CLAUDE.md 实践 = Step 6-7 项目 vault 隔离中国版
- **速读摘要**：见同目录 [[undefinedKi-AI-Second-Brain-10-Step-Guide-digest]]
