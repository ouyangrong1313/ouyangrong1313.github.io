# Matt Van Horn 的 22 个 Agentic Engineering Hacks - Digest

**原文：** [every-agentic-engineering-hack-2026-06.md](./every-agentic-engineering-hack-2026-06.md)
**作者：** Matt Van Horn（@mvanhorn）— last30days / Printing Press / Agent Cookie 作者，Compound Engineering #3 贡献者
**日期：** 2026-06-03
**互动：** 34万 浏览 · 1,669 喜欢 · 5,144 书签
**来源：** https://x.com/mvanhorn/status/2061877533885473181
**系列：** 3 月 "Every Claude Code Hack I Know"（91.3万 浏览）6 月升级版

---

## 核心观点（5 条）

1. **"No IDE. Just plan.md files and voice."** —— 这是整篇文章的元命题。Agentic Engineering 的工作流完全脱离了 IDE / 鼠标 / 键盘码字，而是：语音输入 → plan.md 沉淀 → agent 执行。
2. **Plan 是缰绳，不是你的读物。** 计划必须存在（让 agent 不偷懒），但人不该读它（这是 agent 的作业）。Traditional dev 是 80% 编码 + 20% 计划；Agentic Engineering 把它翻成 20% 编码 + 80% 计划——**思考进计划，执行机械化**。
3. **Research → Plan → Build 是真正的标准循环。** 任何决策前先跑 `/last30days` 收集新鲜信息，再 `/ce-plan` 落地，agent 才能给出"基于社区真实知识"的方案，不是 6 个月前的训练数据。
4. **你是品味，不是手。** 6 个 session 并行跑，agent 提供体量，**人提供判断**。Be the taste. Let them be the hands. 你的稀缺价值是"react-and-redirect loop"，不是 typing。
5. **AI 时代的隐性危机是"AI Psychosis"** —— agent 太爽了，工作狂潮变成瘾，朋友们做完项目发现没有用户，**消失的是 build 之外的人**。这是技术狂欢背后必须正视的人类问题。

---

## 7 个分析角度 + 21 个开头钩子

### 角度 1：范式跃迁 — 从 Vibe Coding 到 Agentic Engineering

> Matt 自述："This used to be called vibe coding. Around last Thanksgiving the models got good enough that the toy became real, what people now call Agentic Engineering." 这是开发者角色的彻底重写：不是"写代码的人"，是"判断 + 指挥 + 验收"的人。

**钩子：**
- "Vibe Coding 已死，Agentic Engineering 永生。"
- "去年感恩节，模型终于配得上玩具的外壳。"
- "开发者不再是写代码的人，是给品味的人。"

---

### 角度 2：Plan 哲学 — Make the plan. Trust the plan. Don't read the plan.

> 计划是给 agent 的缰绳，不是给你读的读物。强制计划存在 → agent 不偷懒 → 写完 acceptance criteria → 必须打勾。读 300 行 markdown 是 agent 的作业，不是你的；你只需要 inline 问 "TLDR?" 或 "eli5 this plan"。

**钩子：**
- "Make the plan. Trust the plan. Don't read the plan."
- "读 300 行 plan 是 agent 的作业，不是你的。"
- "Plan 是缰绳，让 agent 不偷懒的唯一办法。"

---

### 角度 3：标准循环 — Research → Plan → Build

> 任何决策前先 `/last30days <topic>`，再 `/ce-plan`，再 `/ce-work`。last30days（27K stars）做多源新鲜研究（Reddit/X/YouTube/HN/Polymarket/GitHub 并行），/ce-plan 把研究结果落地到结构化 plan.md，/ce-work 执行。**这是从"凭印象选库"到"凭社区共识选库"的分水岭。**

**钩子：**
- "从 6 个月前的训练数据，到今天的社区共识：先 last30days 再 ce-plan。"
- "Vercel agent-browser vs Playwright？我用 last30days 投了票。"
- "Research, Plan, Build. That's the real loop."

---

### 角度 4：多 Session 并发 — 4-6 个 tab，Human Signal 是指挥棒

> 日常开 4-6 个 cmux tab，每个跑不同任务（一个写 plan、一个 build、一个查 last30days、一个修 bug）。/ce-plan 在 A 窗口跑着，/ce-work 在 B 窗口干活，新 bug 塞进 C 窗口。**人是指挥棒，不是钢琴家**。"Option two is closer but use the language from option one"——这种判断才是价值。

**钩子：**
- "4-6 个 session 并行跑，你是指挥棒，不是钢琴家。"
- "Be the taste. Let them be the hands."
- "Agentic Engineering 的工作日长这样：6 个 tab + 1 个麦克风 + 0 行代码。"

---

### 角度 5：Harness 配置哲学 — YOLO + 声音 Hook

> `skipDangerousModePermissionPrompt: true` + 声音 hook 是双核心。6 个 session 并行时，你没法逐个 babysit，权限弹窗会把你逼疯。`afplay /System/Library/Sounds/Blow.aiff` 结束提示音让你**听音辨窗口**——哪个 session 跑完了，听声音就知道。**Harness 是工程，不是仪式**。

**钩子：**
- "Harness 不是仪式，是工程。YOLO + 声音 hook 才是 6 session 并行的必备。"
- "It's my computer. GitHub is there if I break or ruin everything."
- "afplay Blow.aiff —— 这是 Matt Van Horn 的 Agentic Engineering 铃声。"

---

### 角度 6：知识复利 — Your Notes Are Your Agent's Knowledge Base

> Bear（10 年笔记）+ Obsidian + gbrain + supermemory —— 关键是**让 agent 能 CLI/API 读你的笔记**。一个写了 10 年的笔记 + 一个能读它的 agent = **Personal RAG**。Compounding context 是 Compound Engineering 真正的复利。

**钩子：**
- "你的笔记就是 agent 的知识库：Personal RAG without calling it that."
- "写了 10 年笔记不是为了自己读，是为了给 agent 读。"
- "Bear CLI + Claude = 十年复利的一次性解锁。"

---

### 角度 7：现实警告 — AI Psychosis

> 这是 Matt 最诚实的一段。Agentic Engineering 是"最伟大的电子游戏"，loop 太爽了。朋友们做了一堆项目没有用户，消失的是 build 之外的人。**陷阱不是空 launch，是沉迷于 build 而忘了人**。他提了一个反向问题：问自己"有没有人真的想要这个"，如果没有，那就只为自己做——这也可以。

**钩子：**
- "Agentic Engineering 的隐性代价：AI Psychosis。"
- "The trap isn't the empty launch, it's vanishing into the build and losing the people around you."
- "Building 是新时代的最大成瘾品，而家人不会等你。"

---

## 22 个 Hack 速查表

| # | Hack | 一句话 |
|---|------|--------|
| 1 | CE plan.md 第一时间 | 想到 idea 立刻 `/ce-plan`，传统 dev 80% 编码翻成 20% 编码 |
| 2 | Don't Read the plan.md | 计划是给 agent 的缰绳，inline 问 TLDR/eli5 |
| 3 | Plan for the Plan | 非工程任务（商业、策略）用 `/ce-plan make a plan for the plan` |
| 4 | Get Voice-Pilled | Mac 用 Monologue/Wispr Flow，手机用 Apple dictation |
| 5 | Lots of Tabs in cmux | 4-6 个 tab，每个跑不同任务 |
| 6 | Terminal 默认进 Claude | 改 Ghostty config，让新 tab 直接进 Claude Code |
| 7 | Remote Control + Email | Claude mobile app + AgentMail 给 Claude 一个邮箱 |
| 8 | Skip Permissions YOLO | `skipDangerousModePermissionPrompt: true` + 声音 hook |
| 9 | Codex 不开 CLI | Codex IDE 扩展 + `/ce-work --codex` + Printing Press Codex mode |
| 10 | last30days 跑研究 | 任何决策前 `/last30days <topic>`，26K stars 多源研究 |
| 11 | Granola Raw Transcript | 整段生 transcript 丢给 LLM，不先总结 |
| 12 | Human Signal | 你是品味、方向、react-and-redirect loop |
| 13 | HyperFrames 做视频 | 视频也是 HTML 化，agent 写 script.md 渲染 MP4 |
| 14 | Notes as Agent KB | Bear/Obsidian/gbrain/supermemory，选有 CLI/API 的 |
| 15 | Mac mini 远程工作 | Mosh（远程）+ Tmux（飞机）+ Hermes/OpenClaw + Agent Cookie |
| 16 | Proof 给人看 plan | plan.md 丢进 Proof 发送，非终端人也能评论 |
| 17 | Write Your Own Skills | 做超过 2 次的事做成 skill，让 agent 看现有 skill 抄结构 |
| 18 | Contribute to OSS | 用 /ce-plan + /ce-work 循环给自己用的工具提 PR |
| 19 | M5 Max + 64GB | 6 session 起步配置，Anker 充电宝救命 |
| 20 | Printing Press + Agent Cookie | 把现实生活服务包成 agent-native CLI，Agent Cookie 自动登录 |
| 21 | AI Psychosis | Take breaks. Talk to loved ones. Build for someone. |
| 22 | 本文写作方式 | cmux + Monologue 语音 + Proof 评审 + last30days 喂料 |

---

## 工具栈生态速查

| 工具 | 角色 | 关键能力 |
|------|------|----------|
| **Compound Engineering** | 工作流核心 | `/ce-plan` `/ce-work` `/ce-brainstorm`，plan 强约束 |
| **last30days** | 研究前置 | 多源并行抓 30 天新鲜内容（26K stars） |
| **Printing Press** | CLI 工厂 | 把任意服务生成 agent-native CLI（3.7K stars） |
| **Agent Cookie** | 浏览器 session 同步 | 免密码登录，CLIs 直接以你身份行事 |
| **AgentMail** | Claude 收件箱 | email → 新 session 启动（WebSocket + DKIM/SPF 验证） |
| **cmux** | 终端多 tab | 4-6 个 tab，每个跑独立 session |
| **Monologue / Wispr Flow** | 语音转 LLM | Mac 端语音输入到任意 app |
| **Proof** | 计划评审 | 把 plan.md 变成可分享可评论的文档 |
| **HyperFrames** | 视频生成 | 把视频 HTML 化，agent 写 script.md 渲染 MP4 |
| **Hermes / OpenClaw** | 自主 agent 生态 | 远程自主工作 |
| **Mosh + Tmux** | 远程连接 | 飞机/差旅网络下保持 session |

---

## 与已有知识库的关系

### 互为镜像 / 延伸阅读

- [[claude-code-dynamic-workflows]] — Anthropic 官方 dynamic workflow：6 种 Pattern + 10 个 Use Case
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] — Harness 是护城河
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] — 三层框架
- [[Codex才是最适合普通人的顶级牛马-Agent]] — Codex 工作台视角
- [[ClaudeCode用到这个程度-我算是开眼了]] — Claude Code 实战汇编
- [[vibe-coding]] — Vibe Coding 基础概念
- [[oh-my-codex]] — Codex 30 个专家团队
- [[来自Codex官方团队的分享-如何把Codex用到极致]] — Codex 官方用法
- [[Codex配置优化清单-从Harness视角]] — Codex harness 改造
- [[Codex配置原则总览]] — Codex 配置入口
- [[claude-code-large-codebase-best-practices]] — 大型代码库实践
- [[谷歌开源agent-skills]] — Agent Skills 纪律包

### 关键概念串联

- **Vibe Coding → Agentic Engineering 命名进化**：Matt 的亲口命名
- **Harness 哲学实证**：YOLO 模式、声音 hook、remote control 全部是 harness 层
- **Compound Engineering (CE) 范式**：plan.md 强约束 + fan-out research + acceptance criteria
- **Skills 编程**：做超过 2 次的事 → skill
- **Human-in-the-Loop 商业化**：Proof 工具让人能在 plan.md 上评论
- **多 Agent 并发配置**：4-6 tabs + 声音 hook + YOLO 权限

---

## 关键金句

- "No IDE. Just plan.md files and voice."
- "The moment I have an idea, it's /ce-plan to make a plan.md. Not 'let me think about this,' not 'let me start coding.'"
- "Make the plan. Trust the plan. Don't read the plan."
- "Traditional dev is 80% coding, 20% planning. This flips it."
- "It's also the single best trick I know for making an LLM not lazy. Ask for the deliverable directly and it cuts corners. Ask it to first plan how it will produce the deliverable, then execute that plan, and it does the deep version every time."
- "Be the taste. Let them be the hands."
- "It's my computer. GitHub is there if I break or ruin everything."
- "Research, plan, build. That's the real loop."
- "Compounding context. So I pointed it at my whole brain."
- "Write the skill once. Every session after is faster. That's the compounding part of Compound Engineering."
- "The trap isn't the empty launch, it's vanishing into the build and losing the people around you."

---

## 标签

#主题/AI-Coding #主题/AI-Agent #主题/效率 #主题/APP研发
#场景/技术博客 #场景/落地案例
#手法/案例驱动 #手法/权威背书 #手法/对比冲突 #手法/焦虑共鸣
