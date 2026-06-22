---
title: Agent Harness 14 步路线图
category: 01-ai-agents
date: 2026-06-17
source: X (@0xCodez) - Codez 长文 2026-06-16
source_url: https://x.com/0xCodez/status/2066867539305459732
project: .claude/ harness 14 步从 0 到 self-improving
tags: [#主题/AI-Agent, #主题/AI-Coding, #主题/Harness, #主题/Loop, #主题/Self-Improving, #节点/Harness-Engineering, #节点/CLAUDE-md, #节点/settings-json, #节点/Subagent, #节点/Skill, #节点/Hooks, #节点/Memory, #节点/Loop, #节点/STATE-md, #节点/Reviewer, #节点/4件套, #节点/8反模式, #手法/反例论证, #手法/工程框架, #手法/路径指南, #场景/X长文, #场景/ClaudeCode]
nodes: [Harness-定义, 4件套, 三层关系, CLAUDE-md-500tokens, settings-json-权限, Subagent-隔离, Skill-复用, Hooks-强制, Loop-定时, Dynamic-Workflow, Memory复利, State-md三段式, Self-Improving-闭环, 8反模式-CheckList, Harness-顺序论, Reviewer-子Agent, 强制vs建议, Loop-on-Bad-Harness]
links: [[harness-engineering]], [[Harness工程AgentLoop]], [[HarnessEngineering企业级实战]], [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[APPSO-Codex-Claude-Code-Loop-Engineering]], [[陈进-读完Agent-Loop工程手册]], [[Skill-Self-Evolution]]
---

# Agent Harness 14 步路线图

> **一句话**：Harness 是 Loop 的地基。一个坏 harness 上的好 loop，是大规模生产垃圾的最快方法。14 步从单 Agent 搭到自我进化系统。

**作者**：Codez (@0xCodez) · 2026-06-16 · 原文：[X 长文](https://x.com/0xCodez/status/2066867539305459732)
**互动**：likes 564 / retweets 87 / bookmarks 993 / views 84,721
**与既存文档关系**：
- 概念体系见 [[harness-engineering]]（Rule/Skill/Subagent/Workflow/Scripts/MCP 六件套）
- 工程实现细节见 [[Harness工程AgentLoop]]（生命周期/上下文/工具/容错/调度）
- 上层 Loop 范式见 [[Addy-Osmani-Loop-Engineering]]（Loop 是 Harness 套上 timer）

本文定位：**从 0 到 self-improving 的具体路径与顺序**。

---

## 核心公式

```
Self-Improving System = Harness + Loop + Memory（且顺序不能反）
```

**关键反直觉**：
- **模型从来没变过，变的是它周围的 harness** —— "自我进化"是 harness 在累积，不是模型在学。
- **Loop 没有加 intelligence，只是把 harness 套了个定时器**。Harness 没搭好就上 loop，复利是双向腐烂。
- **Harness = 模型 + 工具 + 权限 + 上下文**。其他一切（subagents/hooks/memory）都是这四件的形状变体。

---

## 三层不要混

| 层级 | 性质 | 关键组件 | 错放代价 |
|------|------|---------|---------|
| **Harness** | 静态配置 | 模型/工具/权限/上下文 | 一切上层都崩 |
| **Loop** | 定时调起 | `/loop` + `/goal` | 烂 harness 上跑得越快越烂 |
| **Self-Improving** | 复利闭环 | Loop + Memory + Reviewer | 没有它就跑一次忘一次 |

**实操分类原则**：
- 事实 → CLAUDE.md（每 session 都要的）
- 流程 → skills（多步操作）
- 单文件夹规则 → `rules/`
- 强制约束 → hooks（不能依赖模型"听话"）
- 隔离任务 → subagents

---

## 14 步路线图（3 段）

### Part 1 · What Harness is（01-04）

| 步 | 主题 | 一句话 |
|---|------|--------|
| 01 | Harness 定义 | 单一 Agent 运行所处的环境 = 模型 + 工具 + 权限 + 上下文 |
| 02 | 目录结构 | 全部装在 `.claude/` 一个目录里，目录即文档 |
| 03 | 三层关系 | Harness/Loop/System 三层不混 |
| 04 | 默认 harness | 装好 Claude Code 就是空 harness，one-off 任务够用，重复任务必崩 |

### Part 2 · Build the foundation（05-09）

| 步 | 主题 | 一句话 |
|---|------|--------|
| 05 | **CLAUDE.md** | 限 **500 tokens** 内，只放事实；procedures 挪 skills；单文件夹规则挪 rules/ |
| 06 | **settings.json** | 预先放行安全操作、禁掉危险操作；判断标准：**弄错了多难撤销？** |
| 07 | **Subagents** | 核心价值是"反自我评分"—— reviewer 子 agent 用新 context 窗口挑刺 |
| 08 | **Skills** | 触发器 = 反复把同一段指令粘进新对话。Skills 是 harness 进化的可复用单位 |
| 09 | **Hooks** | **CLAUDE.md 是建议，hooks 是强制**（exit 2 可阻断）。两类最值钱：PreToolUse 安全门 + PostToolUse 格式化 |

### Part 3 · Make it compound（10-14）

| 步 | 主题 | 一句话 |
|---|------|--------|
| 10 | **Add a loop** | `/loop 30m /goal` + 独立 grader 判定 done |
| 11 | **Dynamic workflow** | 复杂任务用 Claude 自己写 JS harness（`agent()`/`parallel()`/`pipeline()`）；workflow 是指挥家，harness 是管弦乐队 |
| 12 | **Add memory** | `agent-memory/STATE.md` 三段式：verified facts / lessons learned / last session |
| 13 | **Close the loop** | Output → reviewer（07）→ memory（12）→ 蒸馏到 skills（08）→ 下次跑更聪明 |
| 14 | **Ship it** | 打包成 plugin 团队复用；**Ship 前要扫 secrets 和过宽权限** |

### 顺序就是教训（**重点**）

> 一次手动跑通 → 加 context/permission → 加 reviewer subagent → 加 memory → **最后才上 loop**。
>
> 错位代价：loop 跑得越勤，harness 的问题放大得越快。

---

## `.claude/` 目录速查

```
.claude/
├─ CLAUDE.md          # 事实，每次 session 必读（≤500 tokens）
├─ settings.json      # 权限、模型、hooks
├─ .mcp.json          # 外部工具连接
├─ rules/             # 路径级行为（tests.md / python-types.md）
├─ agents/            # 子 agent 定义（reviewer.md / eval-runner.md）
├─ skills/            # 可复用流程（pr-checklist/SKILL.md）
└─ agent-memory/      # 跨 run 记忆（STATE.md）
```

**判别原则**：能讲清每个文件为什么存在；讲不清的，删。

---

## settings.json 模板

```json
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "autoApprove": ["Read(*)", "Grep(*)", "Bash(npm test)", "Bash(git status)"],
    "deny": ["Bash(rm -rf*)", "Bash(git push*)", "Edit(.env*)", "Edit(secrets/*)"]
  }
}
```

**放行/禁止判断标准**：弄错了多难撤销？
- 撤销便宜（读、grep、测试）→ autoApprove
- 撤销昂贵（rm -rf、force-push、读 secrets）→ always deny or prompt
- 中间地带 → autoApprove + 记日志

---

## Hooks 模板（最值钱的两个）

```json
"hooks": {
  "PreToolUse": [{
    "matcher": "Bash",
    "command": "./.claude/hooks/block-dangerous.sh"
    // exit 2 = 阻断，模型无法"礼貌忽略"
  }],
  "PostToolUse": [{
    "matcher": "Edit|Write",
    "command": "prettier --write \"$CLAUDE_FILE_PATH\""
  }]
}
```

**反模式**：20 个 hooks。一个好 harness 只有 1-2 个锋利 hook；判断题留给模型，强制题交给 hooks。

---

## STATE.md 模板

```markdown
# Project memory

## Verified facts   # stop guessing about these
- prc is in dollars, not cents (checked via SELECT MIN/MAX)
- auth middleware order: rate_limit -> jwt -> rbac

## Lessons learned  # distill the general ones into skills
- Windows CI runners fail TLS 1.2 in PowerShell — use bash
- Migrations on tables >1M rows must batch in 10k chunks

## Last session     # resume, don't restart
2026-06-11 · 3 fixes merged, 2 escalated. Next: verify rate-limit fix.
```

**Memory 复利三动作**：
1. **Write before walking away** —— 每次跑完更新 state file
2. **Read at the start** —— 每次开局先读 state + 相关 skills
3. **Distill into skills** —— 一般化教训（"Windows runner 用 bash"）从 state 升格为 skill

---

## 8 个 Harness 反模式（check list）

| # | 反模式 | 后果 | 解药 |
|---|--------|------|------|
| 1 | **跑在默认 harness** | agent 每 session 重新猜项目 | 建 `.claude/` 基础四件 |
| 2 | **CLAUDE.md 膨胀** | 每 session 浪费 token、procedures 越改越乱 | 限 500 tokens / 拆 skills / 拆 rules/ |
| 3 | **Enforcement 放 CLAUDE.md** | 模型"礼貌忽略"建议 | 改 hooks（exit 2 阻断） |
| 4 | **单 agent 自写自评** | 自我宽容，质量崩 | 加 reviewer subagent（新 context） |
| 5 | **没有 memory** | 每次重零开始 | 建 STATE.md 三段式 |
| 6 | **loop 套在烂 harness 上** | 烂的更快更大 | 顺序：先 harness 跑通，再上 loop |
| 7 | **20 个 hooks** | 谁也搞不清在哪触发 | 1-2 个锋利的 |
| 8 | **Ship harness 不扫 secrets** | 团队级泄漏 | 打包前扫 `.env` / 过宽权限 |

---

## 对 Seetong 团队的 5 个优先动作

1. **梳理/新建 `.claude/`**：CLAUDE.md 限 500 tokens / `rules/` 按模块分 / `skills/` 装 PR checklist / `agents/` 装 reviewer
2. **加 PreToolUse 安全 hook**：挡 `rm -rf` / 改 `.env` / push 到 `master` / `main`（监控类 APP 误删代价极高）
3. **加 reviewer subagent**：让独立 context 检查主 agent 改动（Seetong 历史代码量大，主 agent 容易"自我宽容"）
4. **建 `.claude/agent-memory/STATE.md`**：每次跑完更新 verified facts（`pod install` 顺序/`pch` 路径依赖）/ lessons（push 前要 `pod repo update`）
5. **警惕"loop on bad harness"**：harness 没搭好之前不上 `/loop` 或 Routines。**复利是双向的：好 harness 复利加速，烂 harness 复利腐烂**

---

## 金句卡

> **"所有人都在聊 loop，但几乎没人聊 loop 跑在什么上面。"** —— 0xCodez

> **"Loop engineering sits one floor above the harness."** —— Addy Osmani（被 0xCodez 引用）

> **"CLAUDE.md 是建议，hooks 是强制。"** —— 区分软硬约束的本质

> **"Workflow 是指挥家，harness 是管弦乐队。"** —— workflow 与子组件的关系

> **"模型从来没变过，变的是它周围的 harness。"** —— 自我进化的真相

> **"Loop 拿走所有掌声，harness 干所有活。"** —— 哲学升华

---

## 相关链接

- 原文 raw：[../../raw/2026-06-17-0xCodez-Agent-Harness-14-Steps.md](../../raw/2026-06-17-0xCodez-Agent-Harness-14-Steps.md)
- 拆解 digest：[../../raw/2026-06-17-0xCodez-Agent-Harness-14-Steps-digest.md](../../raw/2026-06-17-0xCodez-Agent-Harness-14-Steps-digest.md)
- 同主题 wiki：[./harness-engineering.md](./harness-engineering.md)（6 核心概念体系）
- 同主题 wiki：[./Harness工程AgentLoop.md](./Harness工程AgentLoop.md)（工程实现细节）
- 同主题 wiki：[./HarnessEngineering企业级实战.md](./HarnessEngineering企业级实战.md)
- 上层 Loop 范式：[../02-ai-coding/Addy-Osmani-Loop-Engineering.md](../02-ai-coding/Addy-Osmani-Loop-Engineering.md)
- 作者 Substack：https://movez.substack.com/

标签：#主题/AIAgent #主题/AI-Coding #手法/体系框架 #手法/工程实践 #场景/X长文 #场景/ClaudeCode
