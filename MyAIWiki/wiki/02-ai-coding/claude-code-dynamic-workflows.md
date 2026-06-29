# Claude Code 动态工作流：让 Claude 现写 Harness 解决任何任务

> 来源：Anthropic 工程师 Thariq Shihipar & Sid Bidasaria 2026-06-03 长文（132万 浏览 · 6,210 喜欢 · 1.4万 引用）
> 原文：https://x.com/trq212/status/2061907337154367865
> 关联：[[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] · [[从Prompt-Context到Harness-工程的三次进化与终局之战]] · [[claude-code-dynamic-workflows-digest|速读摘要]]

---

## 核心结论

**Dynamic Workflows** 是 Claude Code 的新能力：让 Claude 在执行任务时**现场写一套适合该任务的 harness（脚手架）**，不再依赖统一的默认 harness。这是 Agent 工程范式的一次跃迁——从"通用 harness 框架"走向"任务现写专用 harness"。

---

## 一句话价值主张

> "Claude can now write its own harness on the fly, custom-built for the task at hand."

把 Agent 工程的"造工具"权力下放给模型本身，Opus 4.8 之后的 Claude 才有这个智能水平。

---

## 为什么需要 Dynamic Workflow

**默认 Claude Code harness 在单 context window 里既要规划又要执行**，长任务会出现三种失败模式：

| 失败模式 | 表现 | 触发场景 |
|----------|------|----------|
| **Agentic laziness**（偷懒） | 复杂多步任务中途停下，宣布"完成"，但只做了一半（如 50 项安全审计只审了 20 项） | 多步骤审查、批量处理 |
| **Self-preferential bias**（自我偏好） | 验证自己产出时倾向放水 | 自我评审、对照 rubric 自评 |
| **Goal drift**（目标漂移） | 长时间对话后，原始目标被逐渐稀释，约束条件（特别是"别做 X"）丢失 | 跨多轮、经过 compaction 后 |

**Workflow 的解药**：让每个 subagent 拥有**独立 context window + 聚焦子目标**，结构性规避上述问题。

---

## Dynamic vs Static Workflow

| 维度 | 静态 Workflow（旧的） | 动态 Workflow（新的） |
|------|----------------------|----------------------|
| 实现方式 | Claude Agent SDK / `claude -p` 拼装 | Claude 现场写 JS 文件 |
| 通用性 | 必须覆盖所有 edge case，**通用平庸** | 量身定做 |
| 前提 | 不依赖模型智能 | 需要 Opus 4.8 这种"能造工具"的智能 |
| 维护成本 | 高 | 低（Claude 自己生成） |

**关键论点**：静态 workflow 输给动态 workflow，**模型能力是分水岭**。Opus 4.8 的真正杀手锏是它能现场造工具。

---

## 六种可组合的工作流 Pattern（乐高积木）

| 模式 | 定义 | 适用场景 |
|------|------|----------|
| **Classify-and-act** | 用分类 agent 决定走哪条分支 | 任务类型多样、需差异化处理 |
| **Fan-out-and-synthesize** | 拆任务 → 多个 subagent 并行 → barrier 合成 | 大量小步骤、需要隔离 context |
| **Adversarial verification** | 跑一个 agent 再跑一个 agent 来反对它 | 关键输出、需 rubric 验证 |
| **Generate-and-filter** | 大量生成 → 用 rubric 过滤去重 | 头脑风暴、命名、点子生成 |
| **Tournament** | N 个 agent 同台竞技，judge agent 决出胜负 | 排序、择优、评选 |
| **Loop until done** | 循环 spawn 直到 stop condition 满足 | 工作量未知（debug、triage） |

> **Fan-out 的关键细节**：synthesize 步骤是 **barrier**——它等待所有 fan-out agent 完成后，再合并结构化输出。这种"屏障"是并发控制的标准做法。

---

## 10 个真实 Use Case

### 1. Migrations / Refactors（迁移与重构）
- **真实案例**：Bun 从 Zig 重写到 Rust，用 workflow 完成
- **做法**：把任务拆成 callsites、failing tests、modules 等子步骤；每个子任务 spin 一个 subagent 在独立 worktree 改；另一个 agent 做 adversarial review；最后合并
- **关键提示**：告诉 agent **别用资源密集型命令**（如全量构建），避免机器被打爆

### 2. Deep Research（深度研究）
- Anthropic 自家 `/deep-research` skill 就是 dynamic workflow
- 模式：fan-out web searches → fetch sources → adversarial verify claims → synthesize cited report

### 3. Deep Verification（深度核查）
- 适用：长报告/博客的事实核查
- 做法：让一个 agent 识别所有 factual claims，再 spin subagent 逐条核对；还可用 verification agent 反查 source 质量

### 4. Sorting（排序）
- **关键洞察**：1000+ 行用单 prompt 排序质量会崩、塞不进 context
- 解法：tournament、或 pairwise comparison 流水线（**比较判断比绝对评分更可靠**）、或 bucket-rank 并行后 merge
- 例子：80 份简历排序、1000+ 工单按严重度分桶

### 5. Memory & Rule Adherence（规则遵循）
- 痛点：CLAUDE.md 写了但 Claude 还是漏
- 做法：每个规则配一个 verifier agent
- **反向用法**：挖最近 50 次会话的共同修正 → 聚类 → adversarial 验证（"这条规则能不能阻止一个真实错误？"）→ 把幸存者蒸馏回 CLAUDE.md

### 6. Root-cause Investigation（根因调查）
- 单 context 调查容易 self-preferential bias
- 做法：spin 多个独立 agent 从不同证据（logs、files、data）生成假设；每个假设面对 verifiers + refuters 评审组
- **非技术也能用**：销售下滑、数据管道失败、任何 post-mortem

### 7. Triaging at Scale（大规模分诊）
- 每个团队都有无法全人工处理的 support queue
- 模式：classify → dedupe → 修复或升级到人
- **关键模式 = Quarantine**：禁止读外部不可信内容的 agent 做高权限操作，权限操作由另一组 agent 负责（隔离原则）
- 配合 `/loop` 持续运行

### 8. Exploration and Taste（探索与品味）
- 设计、命名这种"靠品味"的任务
- 让 Claude 探索多方案 → review agent 用 rubric 评 → 满足条件即完成；或用 tournament 选优

### 9. Evals（评测）
- 跑轻量级 eval：worktree 跑子 agent → comparison agent 评分 → 对照 rubric 迭代
- 例子：评估并精炼一个 skill

### 10. Model and Intelligence Routing（模型路由）
- 任务复杂度差异大时，用 classifier agent 提前判断 → 路由到 Sonnet 或 Opus
- **例子**："解释 auth 模块怎么工作" 用哪个模型，取决于 auth 模块有多少文件、代码库结构
- 适合工具调用密集、需要执行前先研究场景

---

## 怎么用 Dynamic Workflow

### 触发方式
1. 直接告诉 Claude "use a workflow" / "set up a workflow" / "use ultracode"
2. 用触发词 `ultracode` 强制让 Claude 写 workflow

### 关键参数 / 工具
- **模型选择**：workflow 内部可决定 subagent 用 Sonnet 还是 Opus
- **隔离级别**：subagent 可在独立 worktree 运行
- **可恢复**：中断后恢复会话，workflow 会从断点继续
- **Token 预算**："use 10k tokens" 这种预算提示可限制烧 token
- **配合指令**：`/goal`（硬性完成条件）+ `/loop`（定期跑）

### 保存与分享
- workflow menu 按 `s` 保存到 `~/.claude/workflows`
- 可打包成 Skill：把 JS workflow 文件放到 skill 目录，SKILL.MD 里引用
- **分发建议**：把 skill 里的 workflow 当**模板**而不是**逐字脚本**，给 Claude 留灵活度

---

## 什么时候**不要**用 Dynamic Workflow

**反直觉提醒**（Anthropic 工程师自己警告）：
- 常规编码任务不要硬上 workflow
- 多数传统编码任务**不需要 5 个 reviewer** 一起来评
- **判断标准**：用 workflow 能不能跑出现有方案跑不出的新水平？不能就别用
- Workflow 烧 token，要算 ROI

---

## 三大 Tips

1. **Prompting 要细**：直接套用 6 种 pattern 的描述给 Claude
2. **小任务也能用**：可以 prompt "quick workflow" 做一次轻量对抗性审查
3. **Token 预算要显式**：用 "use 10k tokens" 这种预算提示设上限

---

## 工程意义

### 从一次性脚本到可积累资产
- 旧：每次跑都重新设计 agent
- 新：workflow 沉淀到 `~/.claude/workflows`，**git 化、Skill 化、团队化**

### Quarantine 模式是安全新基线
- 读不可信内容 ≠ 能做高权限操作
- 这是 Agent 工程的权限分层新思路

### Harness 哲学被官方背书
- 印证 [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] 的判断
- 印证 [[从Prompt-Context到Harness-工程的三次进化与终局之战]] 的框架
- Anthropic 自家工程师"现写 harness"是 harness 哲学的延伸——**harness 应该被动态构造**

---

## 标签

#主题/AI-Coding #主题/AI-Agent #主题/AI-Tech
#场景/技术博客 #场景/产品介绍
#手法/权威背书 #手法/案例驱动 #手法/对比冲突
