---
title: "Loop Engineering：把 prompt agent 替换为设计循环系统"
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Agent, #节点/Agent-Loop, #节点/Codex, #节点/Skill, #节点/Harness, #节点/Memory, #手法/范式归纳, #手法/对比冲突, #手法/警示提醒, #场景/技术博客, #场景/方法论]
nodes: [Loop-Engineering, 5积木框架, Automations, Worktrees, Skills, MCP-Connectors, Sub-agents, Memory-on-Disk, Cognitive-Surrender, Harness-Loop层次]
links: [[Claude-Code作者Boris-我已经不写prompt了我写loop]], [[claude-code-dynamic-workflows]], [[Agentic-Engineering-AI-Workbench]], [[Claude-Code之父品味不是人类护城河]], [[买了一样的AI为什么别家的比你的强]], [[从Prompt-Context到Harness-工程的三次进化与终局之战]], [[AI-Coding的顿悟时刻]], [[54万行代码的顿悟-Markdown才是新编程方式]]
date: 2026-06-09
source: X / Addy Osmani (@addyosmani) — 2026-06-09 07:30（41万 查看 / 3,266 赞 / 7,605 书签）
---

# Loop Engineering：把 prompt agent 替换为设计循环系统

- 原文链接：https://x.com/addyosmani/status/2064127981161959567?s=20
- 来源：X / Addy Osmani（@addyosmani，Chrome 团队 Lead，Google 工程总监）
- 原始推文发布时间：2026-06-09 07:30
- 互动数据：41万 查看 / 3,266 赞 / 7,605 书签 / 570 转推 / 153 回复
- 获取时间：2026-06-09
- 抓取方式：CDP Proxy（X SPA）

> 速读：[[../raw/2026-06-Addy-Osmani-Loop-Engineering-digest|Raw Digest]] · 原文：[[../raw/2026-06-Addy-Osmani-Loop-Engineering|Raw 原文]]

## 核心结论（一句话）

> **Loop engineering = 用一个"会自己循环的 5+1 积木系统"替代"人按 turn 提示 agent"的新范式；Claude Code 与 Codex 已具备全部 5 个积木 + MCP 互通 = 跨工具设计 loop 成为可能；但真正的难点不是工具，是设计 loop 时的工程判断力——verification / comprehension debt / cognitive surrender 三个反噬不警惕，再好的 loop 也会变成灾难加速器。**

## 分类提炼

- **场景**：AI Coding 方法论 · 跨工具 loop 设计 · 工程师角色升级
- **类型**：跨产品方法论长文（不是单一工具教程，是"两个工具的公约数"）
- **价值层级**：⭐⭐⭐（与 [[claude-code-dynamic-workflows]] 同级但更上层：本文是**方法论层**，dynamic workflows 是**Claude Code 一侧的具体实现**）
- **关键引述两条**（背书强度高）：
  - @steipete："You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."
  - @bcherny（Anthropic Claude Code 负责人）："I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

## 知识节点（10 个独立概念）

> 每条独立成段可理解，对应一个可 grep 关键词，不与同篇其他节点重叠。

- **Loop-Engineering**：用循环系统替代"人主动 prompt agent"的工程范式；一个 loop = 一个递归目标（你给目的，AI 迭代到完成），loop engineering = 设计这种递归系统的工程实践
- **5积木框架**：loop 由 5 个积木（Automations / Worktrees / Skills / Plugins+Connectors / Sub-agents）+ 1 个状态文件（Memory）组成；可作为 loop 设计的标准 checklist
- **Automations**：定时/条件触发的发现+分诊，是 loop 的"心跳"——让它变成持续运行的 loop 而非一次性任务；Codex 的 Automations tab、Claude Code 的 `/loop` / cron / hooks / GitHub Actions 是同一能力的不同入口
- **Worktrees**：基于 git worktree 的并行 agent 隔离；解决"两个 agent 写同一文件"机械冲突，但不解决"人 review 跟不上"——**worktrees 解机械冲突，人仍是天花板**
- **Skills**：以 `SKILL.md` 文件夹格式沉淀项目 intent（约定/build 步骤/"我们不这样写因为那次事故"）；agent 冷启动时不再用自信乱猜填 intent 空洞；**Skill = 创作格式，Plugin = 分发方式**
- **MCP-Connectors**：让 loop 接触真实工具（issue tracker / DB / staging API / Slack）的协议；Codex 和 Claude Code 都说 MCP，**写一个 connector 两边都能用**；是 loop 能"开 PR + 关联 ticket + 通知频道"而不是"告诉你该改什么"的关键
- **Sub-agents**：用独立 agent 文件（Codex `.codex/agents/` TOML / Claude Code `.claude/agents/`）做 maker-checker 分离；**写代码的 agent 不该是给自己打分的人**；`/goal` 的底层实现也是这个分离——一个全新模型判断 loop 是否完成
- **Memory-on-Disk**：跨会话状态文件（markdown / Linear board）；**agent 忘，repo 不忘**——长期 loop 的唯一可信状态是"在磁盘上、不在上下文里"
- **Cognitive-Surrender**：loop 自跑时最诱惑的姿势是停止有意见、拿走什么是什么；**为不思考而设计的 loop 是毒药，为有判断地设计是解药**——同一动作，反面结果
- **Harness-Loop层次**：loop engineering 坐在 harness engineering 之上的一层楼——harness 是车间，loop 是工厂；工厂自带时间表、spawn helper、喂自己

## 关联图谱

### 上游（基于 / 来自）

- [[Claude-Code作者Boris-我已经不写prompt了我写loop]]：Boris 在 30 分钟演讲里展开 "我的工作 = 写 loop"，本文是**该金句的跨工具方法论化**（Boris 偏 Claude Code dynamic workflows 实现，本文是双工具的公约数）
- [[claude-code-dynamic-workflows]]：本文"Codex 也有 `/goal`、也用 `SKILL.md`、也走 MCP"的跨工具对称论断，与 Thariq 的 Claude Code Dynamic Workflows 互为镜像——**dynamic workflows 是 Claude Code 一侧的工程实现，loop engineering 是跨产品的设计框架**
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]]：本文"loop engineering 坐在 harness 之上的一层楼"是 Harness 哲学的延伸——Harness 是车间，loop 是工厂
- [[Agentic-Engineering-AI-Workbench]]：若飞 2026-06-08 编译长文，Addy Osmani 是其编译来源之一（《Agent Skills》那篇），本篇是 Addy 在 loop 这一相邻主题的独立方法论；两篇互为佐证
- [[买了一样的AI为什么别家的比你的强]]：Hiten Shah "Skill 是资产"——本文"Skill 是 loop 复利的关键"是同一信号在 loop 场景的落地
- [[54万行代码的顿悟-Markdown才是新编程方式]]：Garry Tan 的 Skillify 循环与本文 "Memory on disk = 复利" 是同一思想的另一表达

### 下游（应用于 / 验证于）

- [[Claude-Code之父品味不是人类护城河]]：Boris Cherny 访谈里"我的工作已经变成写 Loops"的金句，本文是该金句的系统化展开
- [[AI-Coding的顿悟时刻]]："未来瓶颈 = 需求定义 + 架构设计"——本文"build the loop, stay the engineer"是同主线的工程化版本
- [[多Agent使用边界与并行判定]]：本文"worktrees 解机械冲突，人仍是天花板"是该主线在 loop 自动化场景的强化

### 同级（横向 / 并列 / 镜像）

- [[Claude-Code作者Boris-我已经不写prompt了我写loop]]：同一金句的姊妹篇——Boris 偏 Anthropic 一侧，Addy 跨工具框架
- [[claude-code-dynamic-workflows]]：同主题不同层面——动态工作流是单工具实现，loop engineering 是跨工具框架
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]]：同层级——Harness / Loop / Factory 三层抽象的另一视角

## 正文要点（7 条）

### 一、范式跃迁：从"你按 turn 提示 agent"到"你设计系统调 agent"

过去两年用 coding agent 的方式是：你写 prompt → 看输出 → 写下一个 prompt → 重复。**agent 是工具，你全程握着**。这件事正在结束。新范式是：你建一个小型系统，**让系统去找工作、分派工作、验收、记下结果、决定下一步**——系统替你戳 agent。

### 二、Loop = 递归目标：定义目的，AI 迭代到完成

一个 loop = 一个递归目标（你给目的，AI 迭代到完成）。这是对 loop 的最简定义。Loop engineering = 设计这种递归系统。**Loop engineering 之于 harness，等于工厂之于车间**——harness 是车间，loop 是工厂。

### 三、5+1 积木框架（一张可以照搬的设计 checklist）

| 积木 | Codex | Claude Code |
|------|-------|-------------|
| **Automations** | Automations tab | `/loop` / cron / hooks / GitHub Actions |
| **Worktrees** | 内建多线程 worktree | `git worktree` + `--worktree` flag + subagent `isolation: worktree` |
| **Skills** | `SKILL.md`（$ 或 /skills 或自动匹配） | 同 `SKILL.md` 格式 |
| **Plugins + Connectors** | MCP | MCP（互通） |
| **Sub-agents** | `.codex/agents/` TOML | `.claude/agents/` + agent teams |
| **Memory（第 6 块）** | markdown / Linear board | 同 |

**关键洞察：跨产品形状完全一致——别再争哪个工具好，直接设计一个在两边都能跑的 loop**。

### 四、5 积木详解（每一块都讲 Codex 和 Claude Code 双实现）

- **Automations（心跳）**：让 loop 持续跑而非一次性。Codex 的 Triage inbox 把"找到东西的 run"和"没找到东西的 run"分开，**archive 自跑结果**很关键。Automation 可以 call skill，让循环任务可维护。Claude Code 同能力：`/loop` 周期、cron 时间表、hooks 在 lifecycle 触发、GitHub Actions 在你关电脑后继续跑
- **Worktrees（隔离）**：解"两个 agent 写同一文件"的机械冲突；**worktrees take away the mechanical collision but YOU are still the ceiling**——你 review 的带宽决定最多能跑几个 agent
- **Skills（intent 沉淀）**：让 agent 冷启动时不再用自信乱猜填 intent 洞；**没有 skill 的 loop 每轮从零重推项目，有 skill 的 loop 复利累积**；Skill = 创作格式，Plugin = 分发方式
- **Connectors（手脚）**：MCP 让 loop 接触真实工具；**这是 agent 说"这是 fix"和 loop "开 PR + 关联 ticket + 通知频道"的区别**
- **Sub-agents（制衡）**：**写代码的不该是给自己打分的人**；经典三件套：探索 / 实现 / 验证；`/goal` 在底层就是这个分离——独立模型判断 loop 是否完成

### 五、最值得知道的原语：`/loop` + `/goal`

`/loop` 按周期重跑。**`/goal` 跑到你写的条件真正成立**——每轮之后用独立小模型验是否 done。**Codex 也有 `/goal`，同名同行为**——这是跨工具统一的原语。给个条件如"test/auth 全过 + lint 干净"然后走开。

### 六、一个 loop 长什么样（Addy 自用模板）

```
每天早上 9 点在仓库跑 automation
  ↓
prompt 调起 triage skill：读昨日 CI failures / open issues / recent commits
  ↓
findings 写进 markdown 或 Linear board
  ↓
对每个值得做的 finding：在独立 worktree 开新线程
  ↓
sub-agent 写 fix，第二个 sub-agent 对照项目 skills + 现有 tests review
  ↓
connector 让 loop 自动开 PR + 更新 ticket
  ↓
loop 处理不了的东西进 triage inbox 等人
  ↓
state file 是整个系统的脊椎——明天的运行从今天停的地方继续
```

**关键认知：你只设计一次。其余步骤你一个都没 prompt。**

### 七、三个反噬（loop 越强越尖锐，不是更简单）

1. **Verification 还是你的**。无人值守的 loop = 无人值守地犯错。"完成了"是声明不是证明——**your job is to ship code you confirmed works**
2. **理解会腐烂**。loop 越快产你没写的代码，"存在"和"你懂"之间的 gap 越大。**Comprehension debt**——一个顺滑的 loop 让它长得更快
3. **认知投降是最舒服的姿势**。loop 自跑时最诱惑的就是停止有意见。**Cognitive surrender**——设计 loop 是药（有判断地设计）也是毒（为不思考而设计）

## 结尾金句

> **Build the loop. Stay the engineer.**

> Two people can build the exact same loop and get completely opposite results. One uses it to move faster on work they understand deeply. The other uses it to avoid understanding the work at all. **The loop doesn't know the difference. You do.**

> That's what makes **loop design harder than prompt engineering**, not easier. Cherny's point isn't that the work got easier. **It's that the leverage point moved.**

> Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go.

## 标签

#主题/AI-Coding
#主题/AI-Agent
#节点/Agent-Loop
#节点/Codex
#节点/Skill
#节点/Harness
#节点/Memory
#场景/技术博客
#场景/方法论
#手法/范式归纳
#手法/对比冲突
#手法/警示提醒
