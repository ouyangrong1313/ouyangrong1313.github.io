# Hermes Agent Masterclass

> 作者：Akshay 🚀 @akshay_pachaar
> 发布时间：2026年5月13日 22:08
> 来源：https://x.com/akshay_pachaar/status/2054564519280804028
> 标签：#主题/AIAgent #场景/技术教程

## 核心信息

**Hermes Agent** 是 Nous Research 开发的开源 AI Agent，两个月内在 GitHub 获得 90,000+ stars。

**核心特性**：
- 跨会话记忆
- 自主编写可复用 Skills
- 后台自动修剪 Skills
- 通过 GEPA 离线优化 Skills

**与 OpenClaw 的核心区别**：
> "Hermes packages a gateway around a learning agent. OpenClaw packages an agent around a messaging gateway."

## 解决的问题

> "Every AI agent you've used has the same problem: it forgets everything the moment your session ends."

你的编码偏好、项目规范、修复过的错误——下次会话全部消失，从头开始。

## 架构概览

Hermes 核心是一个 AIAgent 类，运行 ReAct 风格同步循环：
- 构建系统提示词 → 检查是否需要压缩 → 调用 API → 执行工具调用 → 循环

**关键设计**：
1. **六种执行环境**：本地终端、Docker、SSH、Modal、Daytona、Singularity。同一套代码，换个配置就能切换。
2. **多模型支持**：翻译层将任何 provider 路由到三种 API 格式，Claude/GPT/Gemini/Ollama 切换只需一个命令。
3. **90 轮上限**：防止卡死循环造成费用燃烧。

## 身份层：SOUL.md

在记忆之前有一个身份层，决定 Agent 是谁。

`~/.hermes/SOUL.md` 位于系统提示词的 slot #1，定义：
- 个性
- 语气
- 沟通风格
- 硬性限制

示例：
```markdown
# SOUL.md
You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.
```

SOUL.md 是固定框架，Memory 和 Skills 是内部运动部件。

## 三层记忆系统

### Tier 1：两个小型 Markdown 文件

- **MEMORY.md**（最多 2200 字符）：Agent 关于环境、项目规范、工具怪癖、经验教训的笔记
- **USER.md**（最多 1375 字符）：你的 profile，包含名称、沟通偏好、技能水平、注意事项

两者在会话开始时作为冻结快照注入系统提示词。80% 容量时 Agent 必须合并整理。

### Tier 2：全文会话搜索

每个对话（CLI 和消息）存储在 SQLite 中，支持全文搜索。Agent 可搜索数周前的对话。

### Tier 3：外部记忆 providers（8 个插件）

深度持久记忆，8 个可插拔 providers，与内置记忆并行运行（不替换）。激活时 Hermes 自动：
- 每次 turn 前预取相关记忆
- 每次响应后同步对话 turn
- 会话结束时提取记忆

## 自进化 Skills：Agent 编写自己的 playbook

Skills 是带 YAML frontmatter 的 Markdown 文件，作为 Agent 的**程序性记忆**——不是知道什么，而是如何做事。

### Skill 结构

```yaml
---
name: k8s-pod-debug
description: > 
  Activate for crashing pods, CrashLoopBackOff, 
  "why is my pod restarting", container failures.
version: 1.2.0
author: agent
platforms: [linux, macos]
---
## Procedure
1. Get pod status → check events → pull logs
2. Look for OOMKilled, ImagePullBackOff, config errors
## Pitfalls
- Forgetting --previous flag on restarted containers
## Verification
- Pod stays Running with 0 restarts for 5+ minutes
```

### 渐进式披露（控制 Token 成本）

- **Level 0**：Agent 只看到名称和描述（完整目录约 3k tokens）
- **Level 1**：实际需要时加载完整 skill 内容
- **Level 2**：可深入 skill 内的特定参考文件

### 自我改进循环

Skill 创建触发条件：
1. Agent 完成复杂任务（5+ 工具调用）
2. 遇到错误或死胡同并找到可行路径
3. 用户纠正其方法
4. 发现非平凡工作流

循环：遇到问题 → 试错解决 → 保存为 SKILL.md → 下次遇到类似问题直接加载 skill

`skill_manage` 工具支持六种操作：create、patch（首选，节省 token）、edit、delete、write_file、remove_file

### The Curator：Skills 的垃圾回收

后台维护系统，处理 Skills 堆积问题。

**触发条件**：7 天未运行且 Agent 空闲 2+ 小时

**两阶段操作**：
1. **自动转换**（确定性，无 LLM）：
   - 30 天未使用 → stale
   - 90 天未使用 → archived
2. **LLM 审查**（最多 8 次迭代）：调查所有 Agent 创建的 skills，决定 keep/patch/consolidate/archive

**重要约束**：
- Curator 从不触碰捆绑或 hub 安装的 skills
- 永不自动删除，最坏情况是归档到 `~/.hermes/skills/.archive/`，可恢复
- 每次 Curator 运行前，Hermes 拍摄整个 skills 目录的 tar.gz 快照
- 可用 `hermes curator pin <skill>` 保护关键 skills

## GEPA：离线进化 Skills

**背景**：in-agent 学习循环有已知弱点：
1. Agent 倾向于自我庆祝，即使表现不好也认为自己做得很好
2. 自动生成 skills 的同一系统可能用更差版本覆盖手动定制

**GEPA（Genetic-Pareto Prompt Evolution）**：
- 不内置于 Hermes 运行时，而是位于 companion 仓库
- ICLR 2026 Oral paper，MIT 许可
- 核心思想：读取执行 traces 理解为什么失败，通过进化搜索提出有针对性的改进

**流程**：
1. 从 Hermes repo 读取当前 skill
2. 生成评估数据集（Claude Opus 的合成测试用例、SQLite 的真实会话历史、手工策划的金色集合）
3. 运行 GEPA optimizer：读取执行 traces → 理解失败点 → 生成候选变体
4. 使用 LLM-as-judge 评分（不是二元通过/失败）
5. 应用约束门：完整测试套件必须 100% 通过、skills 保持在 15KB 以下、缓存兼容性保留、语义目的不漂移
6. 最佳变体作为 PR 提交到 Hermes repo，从不直接 commit

**成本**：约 $2-10 每次优化运行，无需 GPU，可在 finetuning/RL 之前作为有效替代方案

## 安装和运行

**环境**：Linux、macOS、WSL2，Python 3.11+，8GB RAM 足够 API 使用

**一键安装**：
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc  # 或 ~/.zshrc
```

**设置向导**：
```bash
hermes setup
```

**开始对话**：
```bash
hermes
```

**连接 Telegram**：
1. 从 @BotFather 获取 bot token（/newbot）
2. 从 @userinfobot 获取 Telegram user ID
3. 运行 gateway wizard

## ~/.hermes/ 目录结构

```
~/.hermes/
├── config.yaml          # 主要配置
├── .env                 # API keys 和 secrets
├── auth.json            # OAuth provider credentials
├── SOUL.md              # Agent 身份（slot #1）
│   ├── memories/
│   │   ├── MEMORY.md    # 持久 Agent 事实
│   │   └── USER.md      # 用户模型
├── skills/              # 所有 skills（捆绑、hub、Agent 创建）
├── mlops/
│   ├── axolotl/
│   └── vllm/
├── devops/
├── .hub/                # Skills Hub 状态
├── sessions/            # 每个平台的会话元数据
├── state.db             # SQLite 会话存储（FTS5）
├── cron/
│   ├── jobs.json        # 定时任务
│   └── output/          # Cron 运行输出
├── plugins/             # 自定义插件
├── hooks/               # 生命周期钩子
├── skins/               # CLI 主题
└── logs/                # agent.log, gateway.log, errors.log
```

**关键文件说明**：
- `config.yaml`：所有非秘密配置的中心，模型选择、终端后端、工具启用、MCP servers
- `.env`： secrets，API keys、bot tokens、passwords
- `skills/`：整个学习循环所在
- `state.db`：SQLite 数据库，支持 WAL 模式、FTS5 索引

## Skills Hub

687 个 skills，18 个类别：
- 87 个内置 skills
- 79 个可选 skills
- 16 个来自 Anthropic（frontend-design、pdf、pptx、docx、mcp-builder 等）
- 505 个来自 LobeHub（更广泛的社区贡献）

**添加自定义 GitHub repo**：
```bash
hermes skills tap add yourname/your-skills-repo
hermes skills install yourname/your-skills-repo/<skill-name>
```

## 多 Agent 配置：从 1 到 10

Hermes 通过 profiles 支持多 Agent，每个 profile 是完全隔离的 Hermes 实例，有自己的 config、memory、skills、sessions、SOUL.md。

### 创建团队

```bash
hermes profile create designer --clone
hermes profile create programmer --clone
hermes profile create researcher --clone
hermes profile list
```

`--clone` 复制默认 profile 的 config 和 .env 作为起点。

### 每个 Agent 独立 Telegram bot

每个 profile 需要自己的 bot（@BotFather），Telegram 每个 token 只允许一个连接。

### SOUL.md 定制示例

**Designer**（~/.hermes/profiles/designer/SOUL.md）：
```markdown
# Soul
You are an expert at creating hand-drawn illustrations that explain AI, machine learning, and software engineering concepts.
Think whiteboard sketches, not polished marketing art.
Every illustration should make a technical idea click.
```

**Programmer**（~/.hermes/profiles/programmer/SOUL.md）：
```markdown
# Soul
You are my staff engineer. Terse, direct, pragmatic.
You read code before you write code.
You write the smallest change that solves the problem.
You prefer standard library over dependencies, boring tech over shiny tech, and explicit over clever.
Always check: does this already exist in the codebase? Are there tests? What breaks if this fails?
Run the tests before saying "done."
```

**Researcher**（~/.hermes/profiles/researcher/SOUL.md）：
```markdown
# Soul
You are my deep researcher for the AI and machine learning space.
Your main job is a daily Telegram digest of what's new and what matters.
Cover four streams: trending GitHub repos, big tech and lab announcements, fresh research papers, and the social pulse.
Lead with what changed since yesterday. Cite every claim with a URL.
```

### Programmer 集成 Claude Code

Programmer 更强大的是不自己写代码，而是委托给 Claude Code CLI 执行。Hermes 编排，Claude Code 执行文件编辑、运行命令、管理 git。

**激活提示**：
```
I already have a Claude Max subscription. You are my staff engineer who helps me with my day-to-day coding tasks, and under the hood you use Claude Code for all the executions. Set yourself up accordingly.
```

Programmer 会自动安装 autonomous-ai-agents/claude-code skill，验证 claude 在 PATH 上。

### Designer 学习视觉风格

模式：提供参考设计 → 让 Agent 学习 → 要求创建 skill 生成相同风格的内容

```markdown
Carefully study these reference illustrations. Note the color palette, line weight, level of detail, composition, and overall aesthetic. I want you to create a new skill called "my-design-style" that captures this visual style.
```

### 定时任务：Cron  plain English

Hermes 内置调度器，gateway daemon 每 60 秒 tick 一次，在隔离的 Agent 会话中运行任何到期的 job，结果传递到指定的消息平台。Jobs 持久化，重启后依然存在。

**研究者的每日简报设置**：
```markdown
Every weekday at 8am India time, prepare a deep digest of what's new in the AI and machine learning space over the last 24 hours.
Cover four streams in this order:
1. Trending GitHub repos
2. Big tech and lab announcements
3. Fresh research papers worth reading
4. Social pulse from X, Reddit, and Hacker News
Lead with what changed since yesterday. Cite every claim with a URL. Keep it under 800 words. Deliver to Telegram. Set this up as a recurring cron job.
```

**验证**：
```bash
hermes -p researcher cron list
```

**Cron 语法变体**：
- 一次性延迟：`/cron add 30m "Remind me to check the build"`
- 重复间隔：`/cron add "every 2h" "Check server status"`
- 标准 cron 表达式：`/cron add "0 9 * * 1-5" "..."` 工作日 9am
- Skill 附件：`/cron add "every 1h" "Summarize new feed items" --skill blogwatcher`

可用 `context_from` 链接 jobs，一个 cron 的输出成为下一个 cron 的输入。

## 总结

- **SOUL.md** 设置身份
- **运行时循环** 捕获经验
- **Curator** 保持 skill 库清洁
- **GEPA** 确保 skill 库中的内容真正有效

完整理论 + 实践：从 0 到 3 个完全隔离的 agents（programmer、deep researcher、designer），每个有自己的人格、记忆、skills、Telegram bot。