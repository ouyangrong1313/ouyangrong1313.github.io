---
title: AI 第二大脑 Claude+Obsidian 10 步完整实操指南 - Digest
slug: undefinedKi-AI-Second-Brain-10-Step-Guide-digest
source: X 推文 / @undefinedKi
url: https://x.com/undefinedKi/status/2068306794116501544
pub_date: 2026-06-20
fetch_date: 2026-06-22
类型: 原文摘要
---

# AI 第二大脑 Claude+Obsidian 10 步完整实操指南 - Digest

## 一句话总结

把 Karpathy 2026-04 提出的 LLM Wiki 模式，**从概念落地为"一个晚上能搭完"的 10 步实操**——Claude Desktop + Obsidian + Local REST API + mcp-obsidian + CLAUDE.md + 项目级 vault + Skill + Schedule，把对话型 AI 升级为"记忆永不丢失、每天自我整理"的个人第二大脑。

## 5 条核心观点

1. **关键拼图是 MCP + Local REST API**——Claude 桌面版用 `mcp-obsidian` 走 stdio 接 Obsidian 本地 REST API（端口 27124），从此 Claude 不再只是聊天框，而是能读写你 vault 里的每个 .md 文件。**Claude 必须是 Pro 付费版**（$20/月），免费版没有 Code Tab。

2. **CLAUDE.md 是策略层，项目文件夹是执行层**——根目录的 CLAUDE.md 写"我是谁、目标、风格"（让 Claude 面试你生成），每个项目文件夹自带一个 CLAUDE.md 写"这一个项目的目标和你扮演的角色"。**大库规划、单项目交付**。

3. **Inputs/Process/Outputs/Feedback 四区项目结构**——所有项目统一这套文件夹：原始素材进 Inputs，Claude 在 Process 工作，产出到 Outputs，结果反馈到 Feedback。**任何重复任务做成 Skill**：下次说一句"跑 xxx skill"就执行。

4. **把"vault 维护"做成 Schedule 任务**——每天 7:00 让 Claude 自动跑："检查 vault，把 Inputs 里的新东西归类、链接、过时标注、写 3 行变化摘要"。**你醒来时，脑已经整理过一遍**。

5. **keys, not prompts**——权限控制走"只读 scoped key"，不靠"请别删文件"的提示词。**只要技术上能删，就假设终有一天会删**。Gmail/Google Calendar 接 read-only scope 是底线。

## 关键参数/数字

| 项 | 数字/范围 | 用途 |
|---|---|---|
| Claude 订阅 | Pro $20/月（必须付费） | 启用 Code Tab 写文件能力 |
| Obsidian | 免费 | 本地 .md 存储 |
| Local REST API 端口 | 27124 | Claude 接入 vault 的入口 |
| MCP 协议 | stdio + mcp-obsidian | Claude 与 Obsidian 的标准连接 |
| Schedule 频率 | Daily 7:00am | 自动维护 vault |
| 三个 ready-made 仓库 | claude-obsidian / obsidian-second-brain / second-brain-starter | 跳过手搭 |
| obsidian-second-brain | 43 个命令 | /obsidian-save、/obsidian-daily、/obsidian-find |
| 原文热度 | 385.6万 查看 / 9,297 书签 | 2026-06-20 发布 |

## 10 步流程（精简）

| # | 阶段 | 核心动作 |
|---|---|---|
| 1 | 装 Claude Desktop | 启用 Code Tab；必须 Pro 付费 |
| 2 | 装 Obsidian 建 vault | 文件夹即"第二大脑"；用 `[[链接]]` 体会 wikilink |
| 3 | 装 Local REST API 插件 | 复制 API Key |
| 4 | `claude mcp add-json obsidian-vault` | 把 key 写进环境变量 |
| 5 | 让 Claude 面试你写 CLAUDE.md | 一次性建好"我是谁" |
| 6 | 建项目文件夹（Inputs/Process/Outputs/Feedback） | 每个项目自带一个 CLAUDE.md |
| 7 | "Open folder as a vault" | 单项目隔离上下文 |
| 8 | 重复任务做成 Skill | "I want to turn this into a reusable skill..." |
| 9 | 接实时数据（Calendar/Gmail/Slack） | MCP `mcp add google-workspace`，只读权限 |
| 10 | Schedule 任务 | 每天 7:00 自动整理 vault |

## 5 句核心金句

1. **"You are not building a Claude setup. You are building your own memory, and it gets smarter every day you feed it."**（你不是在搭一个 Claude 配置，你是在建自己的记忆，它会越喂越聪明）
2. **"An empty brain is useless. Fix that first, and don't type it all out by hand. Make Claude interview you."**（空脑无用，先让 Claude 面试你，别自己手敲）
3. **"The big vault plans. A single project ships."**（大库做规划，单项目出活）
4. **"Always grant read-only where you can, the brain should read your data, not delete it."**（能只读就只读，脑是读你数据的，不是删你数据的）
5. **"Same subscription. Completely different machine."**（同一个订阅，完全不同的机器——把对话 AI 变成持久记忆系统）

## 5 个反直觉点

1. **"提示词"不是护城河，"权限"才是**——"don't delete this" 是建议不是安全机制；要靠 read-only key
2. **空 vault 没有价值**——先建 CLAUDE.md 让 Claude 知道自己是谁，否则它什么都不懂
3. **别从大 vault 入口工作**——每个项目独立打开成 vault，Claude 只读那个项目的 CLAUDE.md（避免上下文污染）
4. **三个开源 ready-made 仓库就够了**——claude-obsidian / obsidian-second-brain / second-brain-starter 任何一个都能跳过手搭；社区已经把 Karpathy Wiki 模式打包好
5. **跨模型不锁定**——vault 是纯文本 .md，明年换 Gemini/Codex 依然能用（"你拥有脑，不是工具"）

## 5 个对 Seetong / MyAIWiki 可借鉴动作

1. **本工作区 MyAIWiki 已经是 Karpathy Wiki 模式的实操实例**——本知识库用 raw/articles/notes/ + wiki/ + prompts/ + scripts/ + CLAUDE.md 五层结构，跑通 4 月以来；可对外做"现成 demo"案例
2. **Schedule 7:00 自动整理**——把 [[MyAIWiki写入规范与验证模板]] 的"晨间简报"做成 Claude Desktop Schedule 任务（已有 cron 雏形），升级为"自动 ingest + 跨节点碰撞 + 3 行变化摘要"
3. **每个 Seetong 项目独立 vault**——`/Volumes/work/sdks/seetong-tps/CLAUDE.md` 单独写角色，全局 CLAUDE.md 不污染；学 Step 7 "Open folder as a vault" 的隔离
4. **重复任务做 Skill 而非提示词**——seetong-bug-triage / seetong-prd-review / seetong-weekly-report 已经是 Skill 雏形；可补统一骨架"何时触发 + 输入输出 + 验证方式 + 反合理化"
5. **权限走 Key 不走 prompt**——Seetong-TAPD 工具接 read-only scope；OpenClaw 所有 agent 工具默认只读，删除/推送走人工审批

## 关联图谱

### 上游（基于 / 来自）

- [[karpathy-knowledge-system]] — Karpathy 2026-04 提出的 LLM Wiki 原始概念（raw/wiki 双层 + Claude 维护）
- [[claude-obsidian-second-brain]] — 5/12 旧版翻译（718万 查看 7 大架构模式 + 4 个 prompt 模板）
- [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] — LLM Wiki 的深度分析视角
- [[garry-tan-ai-second-brain]] — Garry Tan "AI second brain" 早期提法
- [[obsidian-claude-code-os]] — Obsidian + Claude Code 工作流总览

### 下游（应用于 / 验证于）

- **MyAIWiki 本库** — 是这整套模式的自运行实例（raw/articles + wiki/ + log.md + index.md + CLAUDE.md）
- **三个开源 ready-made 仓库** — claude-obsidian（AgriciDaniel）/ obsidian-second-brain（eugeniughelbur 43 命令）/ second-brain-starter（coleam00）
- **Claude Desktop Schedule 功能** — 把日常维护变成 cron 任务

### 同级（横向 / 并列）

- [[LLM-Wiki-详解]] — LLM Wiki 模式详解
- [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]] — 07-rag-systems 中 Wiki 写作工作流
- [[Claude-Code主动式Agent-Routines]] — Schedule 任务的产品化形式（Anthropic 同方向）
- [[Addy-Osmani-Loop-Engineering]] — 5+1 积木系统，Loop 主题的姊妹视角

## 备注与限制

- **本文的特殊价值**：把 Karpathy 4 月的"概念"压成"6/20 的实操"——5 分钟 setup vs 5 个月沉淀的差距，这是 2026-06 真正可以"开箱即用"的实操指南
- **本工作区已有 6 篇相关页面**（[[karpathy-knowledge-system]] / [[claude-obsidian-second-brain]] / [[obsidian-claude-code-os]] / [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] / [[garry-tan-ai-second-brain]] / [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]），本文价值在"10 步完整实操"+"Schedule 自动维护"+"keys-not-prompts 权限观"，不重复架构论述
- **关键工具栈**：Claude Desktop（Pro $20/月）+ Obsidian（免费）+ Local REST API 插件 + `mcp-obsidian` MCP 工具 + `claude mcp add google-workspace` 实时数据 + Claude Desktop Schedule 任务
- **ridark_eth 短推文**（https://x.com/ridark_eth/status/2068753952850546985）是本文的引用推广（16M 浏览），核心观点与本文一致但短 10 倍，作为"舆论扩散信号"存档
- **本次抓取的限制**：原文为英文长推文（385.6万 浏览），本 digest 用中文重写关键步骤，命令部分保留英文原文以保准确
- **本工作区 SEETONG 主线强关联**：
  - MyAIWiki 本库结构（raw + wiki + log + index + CLAUDE.md）= 论文 Step 1-4 的实操实例
  - 现有 cron（OpenClaw HEARTBEAT / 简报 / 神策友盟反馈 dry-run）= Step 10 Schedule 的早一代形态
  - Seetong 项目级 CLAUDE.md 实践 = Step 6-7 项目 vault 隔离的中国版
  - 现有 Skill 雏形（seetong-bug-triage / seetong-prd-review）= Step 8 的 Skill 化路径
- **标签**：`#主题/AI-Coding` `#主题/效率` `#节点/LLM-Wiki` `#节点/第二大脑` `#节点/MCP` `#节点/Skill` `#节点/Schedule` `#节点/权限控制` `#节点/Claude-Desktop` `#节点/项目级Vault` `#场景/技术博客` `#手法/教程式结构` `#手法/权限优先`
