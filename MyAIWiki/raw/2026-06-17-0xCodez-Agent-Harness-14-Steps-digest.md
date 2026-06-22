---
title: Agent Harness 14 步路线图 - 拆解
source: 2026-06-17-0xCodez-Agent-Harness-14-Steps.md
author: Codez (@0xCodez)
compiled: 2026-06-17
type: digest
---

# 0xCodez《Agent Harness 14 步路线图》拆解

> **一句话定位**：在 Prompt→Harness→Loop 三层架构里，**Harness 是 Loop 的地基**。本文把地基拆成 14 步，从单 Agent 一步步搭到"自我进化"系统。

---

## 一、核心观点（5 条）

1. **Loop 只是 Harness 的 timer 化**。"Loop engineering sits one floor above the harness." 上层（loop）多火，下层（harness）就多被忽视。9/10 的人跑 Claude Code 用的是默认 harness，所以 loop 出来的全是 slop。

2. **Harness 的四件套 = 模型 + 工具 + 权限 + 上下文**。其他一切（subagents/hooks/memory）都是这四件套的形状变体。抓住这四点，harness 设计就抓住了骨架。

3. **三层不要混**：Harness（静态配置）/ Loop（定时调起）/ Self-improving system（loop + memory 复利）。**事实入 context、流程入 skills、执行隔离入 subagents、强制约束入 hooks** —— 混了就是性能崩+成本炸的根源。

4. **CLAUDE.md 限 500 tokens 是死线**。Procedures 不能塞 CLAUDE.md，要塞 skills；单文件夹规则要进 `rules/`。这一条是 practitioner 共识，反直觉但实战反复验证。

5. **"自我进化"不是模型在变聪明，是 Harness 在累积**。Reviewer subagent + memory state file + skills 蒸馏三件套闭环，**让下次跑比这次跑更聪明**。模型不变，harness 越来越尖。

---

## 二、7 个分析角度

### 角度 1：层次观（Prompt → Harness → Loop → Self-Improving）

- Harness 是 Loop 的"地基"，Loop 是 Self-improving system 的"定时器"。
- 错位代价：loop 跑得越勤，harness 的问题放大得越快。
- 与 [[Addy-Osmani-Loop-Engineering]] 是同一枚硬币的两面：Osmani 讲 Loop，本文讲 Harness（Loop 的下一层）。

### 角度 2：可拆解的 14 步路线图

- **Part 1（01-04）What Harness is**：定义 → 目录结构 → 三层关系 → 默认空 harness 的局限。
- **Part 2（05-09）Build the foundation**：CLAUDE.md（事实）→ settings.json（权限）→ subagents（隔离）→ skills（流程）→ hooks（强约束）。
- **Part 3（10-14）Make it compound**：loop（定时）→ dynamic workflow（自编排）→ memory（跨 run 记忆）→ 闭环 → 打包分享。
- **顺序就是教训**：先 manual 跑通 → 加 context/permission → 加 reviewer → 加 memory → **最后才上 loop**。

### 角度 3：CLAUDE.md 的"反膨胀"实践

- 限 500 token 是死线，不是建议。
- 三分类判断标准：是否每 session 都需要（→ CLAUDE.md）/ 是否多步流程（→ skills）/ 是否单文件夹（→ rules/）。
- "读 CLAUDE.md 时大声念出来"是判别技巧：每行都该是 fact，不是 procedure。

### 角度 4：Hooks 是 CLAUDE.md 的"硬升级版"

- 关键对比：**CLAUDE.md 是建议，hooks 是强制**。模型能"礼貌忽略"前者，不能忽略 exit code 2 的后者。
- 两个最有价值的 hook：PreToolUse 安全门（挡 rm -rf/读 .env/push main）+ PostToolUse 格式化（跑 prettier）。
- 反模式：20 个 hooks。一个好 harness 只有 1-2 个锋利 hook。

### 角度 5：Subagent 的最大价值是"反自我评分"

- Subagent 不是为并行而并行，**核心价值是把"dirty work"隔离出主 context**。
- **最有价值的 subagent 是 reviewer**：让独立 context 窗口的 reviewer 检查主 agent 输出。模型自己 review 自己太宽容。
- Writer-vs-checker 分工：让 loop 上层可以放心信任输出。

### 角度 6：Memory 让"昨天的工作"成为"明天的起点"

- Agent 跑完就忘。Harness 不必。
- State file 三段式：verified facts（停猜的）/ lessons learned（要蒸馏的）/ last session（恢复的）。
- **复利三动作**：Write before walking away + Read at start + Distill general lessons into skills。
- "Windows runner 用 bash 不用 PowerShell"这种教训要从 state file 升格为 skill。

### 角度 7：错误的 8 种姿势（反向 check list）

- Default harness（无 context/规则/记忆） / 膨胀的 CLAUDE.md / 把 enforcement 放 CLAUDE.md 而非 hooks / 单 agent 自写自评 / 无 memory / 把 loop 套在烂 harness 上 / 20 个 hooks / 不扫 secrets 就 ship 插件。
- 共同模式：**把"建议"当"约束"、把"流程"当"事实"、把"加法"当"迭代"**。

---

## 三、14 个开头钩子（按引用频次和反直觉度排序）

### 钩子 1（反共识开篇）

> "所有人都在聊 loop，但几乎没人聊 loop 跑在什么上面。"

适用：写"被忽视的底层"的引子。

### 钩子 2（数据冲击）

> "10 个用 Claude Code 的人里，9 个跑在默认 harness 上 —— 没规则、没子 agent、没 hooks、没记忆。"

适用：揭示现状问题的开篇。

### 钩子 3（类比金句）

> "Loop engineering sits one floor above the harness."

适用：引入层次观的引子。

### 钩子 4（结论先行）

> "一个坏 harness 上的好 loop，是大规模生产垃圾的最快方法。"

适用：写"质量与基础"的引子。

### 钩子 5（结构预告）

> "14 步，3 层，一块地基。"

适用：长文目录预告式开篇。

### 钩子 6（数字框架）

> "Harness 拆开了就是四件套：模型、工具、权限、上下文。其他一切都是这四件的形状变体。"

适用：写"复杂概念奥卡姆剃刀"的开篇。

### 钩子 7（强制 vs 建议）

> "CLAUDE.md 是建议，hooks 是强制。模型能礼貌忽略前者，不能忽略 exit code 2 的后者。"

适用：写"约束机制设计"或"硬规则 vs 软规则"。

### 钩子 8（反直觉共识）

> "跑过 Claude Code 的人都同意：CLAUDE.md 别超过 500 tokens。"

适用：写"反直觉工程实践"开篇。

### 钩子 9（reviewer 子 agent 的颠覆性）

> "任何 harness 里最值钱的 subagent，是检查主 agent 工作的那个。"

适用：写"独立 review"价值的引子。

### 钩子 10（procedures 与 facts 区分）

> "大声念一遍你的 CLAUDE.md。每行都该是 fact（"我们用 pnpm 不用 npm"）。如果是 procedure（"加功能时先..."），挪到 skill 里。"

适用：写"文档结构化"的引子。

### 钩子 11（loop 的本质）

> "Loop 没有加 intelligence，只是把 harness 套了个定时器。"

适用：写"本质 vs 表面"的开篇。

### 钩子 12（流程与管弦乐）

> "Workflow 是指挥家，harness 是管弦乐队。"

适用：写"组件与编排"或"零件与系统"。

### 钩子 13（"自我进化"的真相）

> "模型从来没变过，变的是它周围的 harness。这才是'自我进化'的诚实含义 —— 不是模型在学，是 harness 在积累。"

适用：写"进化机制"或"AI 学习"的反共识开篇。

### 钩子 14（哲学升华）

> "Loop 拿走所有掌声，harness 干所有活。"

适用：写"幕后英雄"或"被低估的基础设施"。

---

## 四、对 Seetong 团队的 5 个可借鉴动作

1. **梳理现有 `.claude/` 目录**（如果还没建）。按本文 `01-04` 步把 CLAUDE.md（事实）/`rules/`（单文件夹规则）/`skills/`（流程）/`agents/`（reviewer 等）严格分开。**第一步先瘦身 CLAUDE.md 到 500 tokens 以内**。

2. **加一个 PreToolUse 安全 hook**。挡 `rm -rf` / 改 `.env` / `git push` 到 master/main。这是"模型不能礼貌忽略"的硬约束，对 Seetong 监控类 APP 尤为重要（误删/误推代价高）。

3. **加一个 reviewer subagent**。让独立 context 的 reviewer 检查主 agent 的代码改动。Seetong 有 QMUI + Objective-C 大量历史代码，**主 agent 容易"自我宽容"**。

4. **建 STATE.md 跨 session 记忆**。每次跑完记录：verified facts（`pod install` 顺序 / `pch` 路径依赖）/ lessons learned（`git push` 要先 `pod repo update`）/ last session。放在 `.claude/agent-memory/`。

5. **警惕"loop on bad harness"**。Harness 没搭好之前，不要上 `/loop` 或 Routines。**复利是双向的：好 harness 复利加速，烂 harness 复利也加速腐烂**。

---

## 五、相关链接

- 原文 raw：[2026-06-17-0xCodez-Agent-Harness-14-Steps.md](./2026-06-17-0xCodez-Agent-Harness-14-Steps.md)
- 同主题 wiki：[../wiki/01-ai-agents/harness-engineering.md](../wiki/01-ai-agents/harness-engineering.md)
- 同主题 wiki：[../wiki/01-ai-agents/Harness工程AgentLoop.md](../wiki/01-ai-agents/Harness工程AgentLoop.md)
- 上层 Loop：[../wiki/02-ai-coding/Addy-Osmani-Loop-Engineering.md](../wiki/02-ai-coding/Addy-Osmani-Loop-Engineering.md)
- 同主题 wiki：[../wiki/01-ai-agents/HarnessEngineering企业级实战.md](../wiki/01-ai-agents/HarnessEngineering企业级实战.md)
- Substack：https://movez.substack.com/
- 推文：https://x.com/0xCodez/status/2066867539305459732

标签：#主题/AIAgent #主题/AI-Coding #手法/体系框架 #手法/工程实践 #场景/X长文 #场景/ClaudeCode
