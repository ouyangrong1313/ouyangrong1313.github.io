# Claude Code 动态工作流 - Digest

**原文：** [claude-code-dynamic-workflows.md](./claude-code-dynamic-workflows.md)
**作者：** Thariq Shihipar & Sid Bidasaria（Anthropic Claude Code 团队）
**日期：** 2026-06-03
**互动：** 132万 浏览 · 6,210 喜欢 · 1.4万 引用
**来源：** https://x.com/trq212/status/2061907337154367865

---

## 核心观点（5 条）

1. **动态工作流 = 让 Claude 现写 Harness**：Claude Code 新功能 Dynamic Workflows 让 Claude 在执行任务时**自己写**一套适合该任务的 harness（脚手架），不再依赖统一的默认 harness。这是 Agent 工程范式的一次跃迁。
2. **解决单上下文窗口的三大失败模式**：Agentic laziness（偷懒早停）、Self-preferential bias（自我偏好偏差）、Goal drift（目标漂移）—— 多 subagent + 独立 context window 是结构性的解药。
3. **六种可组合的工作流模式**：Classify-and-act、Fan-out-and-synthesize、Adversarial verification、Generate-and-filter、Tournament、Loop until done。这是 Agent 工程"乐高积木"。
4. **不是所有任务都该用 Workflow**：常规编码任务不需要 5 个 reviewer 一起来评。Workflow 烧 token，要用在"现写法子能跑出新水平"的地方。
5. **可分享、可版本化的工作流**：保存到 `~/.claude/workflows` 或打包成 Skill，团队复用。这意味着 harness 工程从一次性脚本变成**可积累的工程资产**。

---

## 7 个分析角度 + 14-21 个开头钩子

### 角度 1：范式跃迁 — 从"通用 harness"到"任务现写 harness"

> Dynamic workflow 本质是：**让模型自己设计自己的工作环境**。以前的 prompt 是"问问题"，workflow 是"让 Claude 先造一套专用工具再来回答"。这是 Agent 工程的元能力。

**钩子：**
- "通用 Agent 框架已死，专用 Workflow 永生。"
- "Claude Code 的下一站：让 Claude **自己写自己的脚手架**。"
- "Anthropic 终于承认：没有一套 harness 能搞定所有任务。"

---

### 角度 2：单 Context Window 的三重原罪

> 当 Claude 在一个 context 里既要规划又要执行时，会出现三种典型失败：偷懒、自我偏好、目标漂移。Workflow 用**多独立 context + 聚焦子目标**来结构性地规避这些问题。

**钩子：**
- "你的 Claude 偷懒、偏心、走神？问题不在模型，在 context。"
- "Agentic laziness、Self-preferential bias、Goal drift —— 一个 context window 里的三宗罪。"
- "Context window 不是越大越好，独立 context 才是工程的关键。"

---

### 角度 3：六种乐高积木 — Agent Workflow 的基本模式

> Classify-and-act、Fan-out-and-synthesize、Adversarial verification、Generate-and-filter、Tournament、Loop until done —— 这六种模式可以独立使用、可以组合拼装。Thariq 把它们叫做"common patterns that Claude might use and compose together"。

**钩子：**
- "Agent 工程师的乐高积木：6 种 pattern，组合出无限种 workflow。"
- "Tournament 模式：让 N 个 agent 同台竞技，judge agent 决出胜负。"
- "Fan-out-and-synthesize：拆任务 → 多个 subagent 并行 → barrier 合成。Agent 并发的标准模板。"

---

### 角度 4：从 Coding 到非 Coding — Workflow 是通用工作流引擎

> 默认 Claude Code harness 写代码，但**很多任务长得像写代码**。Research、security analysis、agent teams、code review 这些都要专门的 harness。Workflow 让 Claude Code 变通用引擎。

**钩子：**
- "Claude Code 不只是写代码的，它正在变成通用工作流引擎。"
- "Research、Code Review、Incident 复盘 —— 都能用 workflow 模式重写。"
- "营销方案、招聘筛选、商业计划书批判：dynamic workflow 接管一切非技术工作。"

---

### 角度 5：反直觉的工程哲学 — 越通用的 harness 越弱

> 静态 workflow（用 Agent SDK 或 `claude -p`）必须覆盖所有 edge case，**只能做得更通用、更平庸**。Opus 4.8 + dynamic workflow 的关键变化是：**模型变聪明到能针对单次任务写专用 harness**。

**钩子：**
- "通用 framework 输给专用 workflow，这是 AI 工程的新分水岭。"
- "静态 workflow 输给动态 workflow，模型能力是分水岭。"
- "Opus 4.8 真正的杀手锏：它能**现场造工具**。"

---

### 角度 6：工程债视角 — Workflow 是可分享、可版本化的工作流资产

> Workflow 可以保存为 JS 文件、存到 `~/.claude/workflows`、打包成 Skill、提交到 git。**harness 工程从一次性脚本变成可积累的工程资产**，这是 Agent 工程进入"软件工程时代"的标志。

**钩子：**
- "Workflow 不只是运行一次，你可以 `~/.claude/workflows` 里把它版本化。"
- "Agent 时代的第一批工程债：workflow 文件夹管理。"
- "把动态 workflow 打包成 Skill 分享给团队：Agent 工程的 GitHub 时刻。"

---

### 角度 7：节制使用 — Token 经济学警告

> Thariq 明确警告：**Dynamic workflows 烧 token**。常规编码任务不要硬上 5 个 reviewer 一起来评。**判断标准是"这个任务用 workflow 能不能跑出现有方案跑不出的新水平"**，否则就是浪费。

**钩子：**
- "Anthropic 工程师亲自警告：workflow 烧 token，节制使用。"
- "你的任务值得 5 个 reviewer 吗？想清楚再开 workflow。"
- "Token 经济学：workflow 的 ROI 计算器比你想的更重要。"

---

## 7 种 Useful Patterns 速查表

| 模式 | 一句话定义 | 适用场景 |
|------|-----------|----------|
| **Classify-and-act** | 用分类 agent 决定走哪条分支 | 任务类型多样、需差异化处理 |
| **Fan-out-and-synthesize** | 拆任务 → 多个 subagent 并行 → barrier 合成 | 大量小步骤、需要隔离 context |
| **Adversarial verification** | 跑一个 agent 再跑一个 agent 来反对它 | 关键输出、需 rubric 验证 |
| **Generate-and-filter** | 大量生成 → 用 rubric 过滤去重 | 头脑风暴、命名、点子生成 |
| **Tournament** | N 个 agent 同台竞技，judge agent 决出胜负 | 排序、择优、评选 |
| **Loop until done** | 循环 spawn 直到 stop condition 满足 | 工作量未知（debug、triage） |
| **Quarantine（triage 特化）** | 读外部内容的 agent 不能做高权限动作 | 不可信输入 + 高权限操作的隔离 |

---

## 10 个 Use Case 速查表

| 场景 | Workflow 模式组合 | 真实案例 |
|------|----------------|----------|
| Migrations / refactors | Fan-out + adversarial review | Bun 从 Zig 重写到 Rust |
| Deep research | Fan-out + adversarial verify | `/deep-research` skill |
| Deep verification | Identify claims → 子 agent 逐条核对 | 报告/博客文事实核查 |
| Sorting | Tournament / pairwise compare | 80 份简历排序、1000+ 工单分桶 |
| Memory / rule adherence | Verifier agent per rule | 把 50 次会话的修正蒸馏成 CLAUDE.md |
| Root-cause investigation | 多独立假设 + verifiers+refuters | 排查故障、销售下滑、数据管道失败 |
| Triaging at scale | Classifier + quarantine + 修复 agent | 长期 bug 队列、support queue |
| Exploration and taste | Generate + rubric-based review | 设计方案、命名、Tournament 选优 |
| Evals | 子 agent + comparison agent | Skill 评估与精炼 |
| Model routing | Classifier 决定 Sonnet / Opus | 任务复杂度自适应模型选择 |

---

## 与已有知识库的关系

### 互为镜像 / 延伸阅读

- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] — 解读 1.6% / 98.4% 的工程比例，论证 harness 才是护城河
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] — 三层框架理解 AI 工程演进
- [[Codex才是最适合普通人的顶级牛马-Agent]] — Codex 工作台的整体视角
- [[54万行代码的顿悟-Markdown才是新编程方式]] — Tokenmaxxing 经济学
- [[Claude-Code负责人谈AI原生工程组织]] — 组织层面对 AI 编码的调整
- [[claude-code-large-codebase-best-practices]] — 大型代码库的 Claude Code 最佳实践

### 关键概念串联

- **Harness 哲学** → 进一步被 Anthropic 官方工程师"任务现写 harness"观点加强
- **多 Agent 并发** → 给出 6 种可组合的具体模式
- **Skill 系统** → 给出 workflow 如何打包成 Skill 分发的具体路径
- **Token 经济学** → 明确警告 dynamic workflow 烧 token

---

## 关键金句

- "Claude can now write its own harness on the fly, custom-built for the task at hand."
- "Workflows allow you to dynamically create harnesses that enable Claude to solve all of those problems and more natively inside of Claude Code."
- "Creating a workflow helps combat these by orchestrating separate Claudes with their own context windows and focused, isolated goals."
- "The synthesize step is a barrier — it waits for all the fan-out agents, then merges their structured outputs into one result."
- "A useful pattern for triage workflows is quarantine. This involves barring the agents that read untrusted public content from taking high-privilege actions."

---

## 标签

#主题/AI-Coding #主题/AI-Agent #主题/AI-Tech
#场景/技术博客 #场景/产品介绍
#手法/权威背书 #手法/案例驱动 #手法/对比冲突
