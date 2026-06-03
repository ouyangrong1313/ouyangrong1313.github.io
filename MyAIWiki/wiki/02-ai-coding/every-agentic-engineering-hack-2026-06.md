# Matt Van Horn 的 22 个 Agentic Engineering Hacks

> 来源：Matt Van Horn @mvanhorn 2026-06-03 长文（34万 浏览 / 1,669 喜欢 / 5,144 书签）
> 原文：https://x.com/mvanhorn/status/2061877533885473181
> 关联：[[claude-code-dynamic-workflows]] · [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] · [[Codex才是最适合普通人的顶级牛马-Agent]] · [[every-agentic-engineering-hack-2026-06-digest|速读摘要]]

---

## 一句话主张

> **No IDE. Just plan.md files and voice.**

Agentic Engineering 的全部工作流是：语音输入 → plan.md 沉淀 → agent 执行。3 月那篇 91.3万 浏览的 "Every Claude Code Hack" 是 1.0 版，这是 6 月 2.0 版。

---

## 5 大核心原则

### 1. Plan 是缰绳，不是读物
- 想到 idea 立刻 `/ce-plan`，不是"想想"，不是"先写代码"
- **Make the plan. Trust the plan. Don't read the plan.**
- 读 300 行 markdown 是 agent 的作业；你 inline 问 "TLDR?" / "eli5 this plan"

### 2. 思考进计划，执行机械化
- 传统 dev = 80% 编码 + 20% 计划
- Agentic Engineering = **20% 编码 + 80% 计划**
- 这是开发者角色的根本翻转：写代码的人 → 思考的人

### 3. Research → Plan → Build 标准循环
- 任何决策前先 `/last30days <topic>` 跑研究
- 再 `/ce-plan` 落地到结构化 plan.md
- 再 `/ce-work` 执行
- **从"凭印象选库"到"凭社区共识选库"**

### 4. 多 session 并发 + Human Signal
- 4-6 个 cmux tab 并行跑不同任务
- Agent 提供体量，**人提供品味、方向、react-and-redirect loop**
- "Option two is closer but use the language from option one" 这种判断才是价值
- **Be the taste. Let them be the hands.**

### 5. 现实警告：AI Psychosis
- Agentic Engineering 是"最伟大的电子游戏"，loop 太爽
- 朋友们做了一堆项目没有用户，**消失的是 build 之外的人**
- Take breaks. Talk to loved ones. Build for someone.

---

## 22 个 Hack 速查表

| # | Hack | 工具 / 命令 | 一句话 |
|---|------|------------|--------|
| 1 | CE plan.md 第一时间 | `/ce-plan` `/ce-work` `/ce-brainstorm` | 想到 idea 立刻出 plan，**80% 计划 + 20% 编码** |
| 2 | Don't Read the plan.md | inline "TLDR?" / "eli5" | 计划是给 agent 的缰绳，**别坐下来读 300 行** |
| 3 | Plan for the Plan | `/ce-plan make a plan for the plan` | **防止 LLM 偷懒的万能招**：先 plan 再 plan |
| 4 | Get Voice-Pilled | Monologue / Wispr Flow / Apple dictation | **语音转 LLM 不需要完美转写** |
| 5 | Lots of Tabs in cmux | cmux | 4-6 tab 并行，**每个跑不同任务** |
| 6 | Terminal 默认进 Claude | Ghostty config + launcher.sh | **新 tab 直接进 Claude Code** |
| 7 | Remote Control + Email | Claude mobile + AgentMail | Claude 可以收邮件触发新 session |
| 8 | Skip Permissions YOLO | `skipDangerousModePermissionPrompt: true` + 声音 hook | **It's my computer. YOLO.** |
| 9 | Codex 不开 CLI | Codex IDE 扩展 + `/ce-work --codex` | **Claude plans, Codex builds** |
| 10 | last30days 跑研究 | `/last30days <topic>` | **决策前先跑多源新鲜研究**（26K stars） |
| 11 | Granola Raw Transcript | Granola + Claude | **整段生 transcript 丢给 LLM**，不先总结 |
| 12 | Human Signal | 你的 judgment | **你是品味、方向、react-and-redirect loop** |
| 13 | HyperFrames 做视频 | HyperFrames + agent | **视频 HTML 化，agent 写 script.md 渲染 MP4** |
| 14 | Notes as Agent KB | Bear / Obsidian / gbrain / supermemory | **选有 CLI/API 的笔记，让 agent 能读** |
| 15 | Mac mini 远程工作 | Mosh + Tmux + Hermes + OpenClaw | **Mosh 远端不卡，Tmux 飞机不掉** |
| 16 | Proof 给人看 plan | Proof | **plan.md 丢进 Proof，非终端人也能评论** |
| 17 | Write Your Own Skills | "look at CE skill and help me make one like this" | **做超过 2 次的事做成 skill** |
| 18 | Contribute to OSS | `/ce-plan` + `/ce-work` 循环 | **用同一套循环提 PR 给 Python/Go/Vercel Agent Browser** |
| 19 | M5 Max + 64GB | M5 Max 笔记本 | **6 session 起步配置**，Anker 充电宝救命 |
| 20 | Printing Press + Agent Cookie | printingpress.dev | **把现实服务包成 agent-native CLI**，自动登录 |
| 21 | AI Psychosis | mindset | **陷阱是沉迷 build 失去人，不是空 launch** |
| 22 | 本文写作方式 | cmux + Monologue + Proof | **No IDE. No typing code. Talk, plan, build.** |

---

## 关键配置代码（开箱即用）

### ~/.claude/settings.json — YOLO + 声音 hook

```json
{
  "permissions": {
    "allow": ["WebSearch", "WebFetch", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "TodoWrite"],
    "deny": [],
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true,
  "remoteControlAtStartup": true
}
```

```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Blow.aiff" }] }]
  }
}
```

### ~/.codex/config.toml — Codex YOLO
```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

### Ghostty + Claude launcher
```bash
# ~/.local/bin/claude-launcher.sh
claude --dangerously-skip-permissions
# when Claude exits: print short note, drop into login zsh
```

---

## 工具栈生态速查

| 工具 | 角色 | 关键能力 | Stars |
|------|------|----------|-------|
| **Compound Engineering** | 工作流核心 | `/ce-plan` `/ce-work` `/ce-brainstorm` | – |
| **last30days** | 研究前置 | 多源并行抓 30 天新鲜内容 | 27K |
| **Printing Press** | CLI 工厂 | 任意服务 → agent-native CLI | 3.7K |
| **Agent Cookie** | 浏览器 session 同步 | 免密码登录，CLIs 直接以你身份行事 | – |
| **AgentMail** | Claude 收件箱 | email → 新 session（WebSocket + DKIM/SPF） | – |
| **cmux** | 终端多 tab | 4-6 个独立 session | – |
| **Monologue / Wispr Flow** | 语音转 LLM | Mac 端语音输入任意 app | – |
| **Proof** | 计划评审 | plan.md → 可分享可评论的文档 | – |
| **HyperFrames** | 视频生成 | 视频 HTML 化，agent 渲染 MP4 | – |
| **Hermes / OpenClaw** | 自主 agent 生态 | 远程自主工作 | – |
| **Mosh + Tmux** | 远程连接 | 飞机/差旅不掉 session | – |

---

## 反直觉的金句

> "It's also the single best trick I know for making an LLM not lazy. Ask for the deliverable directly and it cuts corners. Ask it to first plan how it will produce the deliverable, then execute that plan, and it does the deep version every time."
>
> —— 防止 LLM 偷懒的万能招：Plan for the Plan

> "The reason a plan gets better every time is that Claude has access to every prior plan I've written. Compounding context."
>
> —— 计划 + 笔记 = Compounding context

> "Not 'AI writes my code.' Agentic Engineering does the errands, watches the game, warms the car, and books the trip, while I'm doing something else."
>
> —— AI Coding 的下一站：AI Errands

> "The trap isn't the empty launch, it's vanishing into the build and losing the people around you."
>
> —— AI Psychosis 的真正危险

---

## 关联阅读

- [[claude-code-dynamic-workflows]] — Anthropic 官方 dynamic workflow，与本文形成"官方 vs 一线用户"互文
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] — Harness 哲学的基础理论
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] — 三层框架
- [[Codex才是最适合普通人的顶级牛马-Agent]] — Codex 工作台视角
- [[ClaudeCode用到这个程度-我算是开眼了]] — Claude Code 实战汇编
- [[vibe-coding]] — Vibe Coding 基础概念
- [[oh-my-codex]] — Codex 30 个专家团队
- [[来自Codex官方团队的分享-如何把Codex用到极致]] — Codex 官方用法
- [[Codex配置优化清单-从Harness视角]] — Codex harness 改造
- [[claude-code-large-codebase-best-practices]] — 大型代码库实践
- [[谷歌开源agent-skills]] — Agent Skills 纪律包

---

## 标签

#主题/AI-Coding #主题/AI-Agent #主题/效率 #主题/APP研发
#场景/技术博客 #场景/落地案例
#手法/案例驱动 #手法/权威背书 #手法/对比冲突 #手法/焦虑共鸣
