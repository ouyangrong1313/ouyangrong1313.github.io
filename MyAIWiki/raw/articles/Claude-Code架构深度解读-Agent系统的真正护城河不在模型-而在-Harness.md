# Claude Code 架构深度解读：Agent 系统的真正护城河不在模型，而在 Harness

**来源：** AI 启蒙小伙伴
**作者：** 邵猛
**日期：** 2026年4月27日
**链接：** https://mp.weixin.qq.com/s/9MUOVFjaYKayjdExpXJ82g

---

## 正文

深入阅读 Claude Code 泄露源代码，结合 Anthropic 官方文档和社区分析，重建出一个生产级 Coding Agent 完整架构图谱，并以独立开源系统 OpenClaw 作为对照组！

---

### 最核心的一个数字：1.6% vs 98.4%

社区估算：Claude Code 整个代码库里，**只有约 1.6% 是"AI 决策逻辑"（提示词、模型调用、循环），其余 98.4% 是确定性的运行环境**（permission、context、tool routing、recovery）。

这个比例是全文的"灵魂"。它意味着：
- 模型几乎拥有完全自主决策权（reason 在哪做、调什么工具）
- 但模型从不直接接触文件系统、shell、网络
- **工程复杂度不是为了约束模型，而是为了让模型在一个安全富饶的环境里自由发挥**

这与 LangGraph（用状态图约束控制流）、Devin（显式 planner）走的是相反路线：**最小脚手架 + 最大化操作型 harness**。

---

### 五种人类价值驱动整套架构

论文提炼出 Anthropic 在做设计权衡时反复出现的五个底层价值观：

| 价值 | 核心命题 |
|------|----------|
| **人类决策权（Authority）** | 用户最终拥有控制权；通过原则等级（Anthropic→operators→users）形式化 |
| **安全/隐私（Safety）** | 即使用户不专心，系统也要保护代码、数据与基础设施 |
| **可靠执行（Reliability）** | 既要单轮正确，也要跨上下文窗口、跨会话、跨子 agent 保持一致 |
| **能力放大（Capability）** | 让用户做以前根本不会尝试的事（~27% 任务是"没有这工具就不会做"的） |
| **情境适配（Adaptability）** | 系统适应用户项目、习惯、技能，关系随时间演进 |

第六个是**评估视角而非设计价值**：**长期人类能力保留**——这是论文最重要的批判性观察。

---

### 十三条设计原则与架构骨架

价值通过 13 条原则落到代码：

1. **Deny-first with human escalation**（默认拒绝、不识别就升级给人）
2. **Graduated trust spectrum**（信任是渐进光谱）
3. **Defense in depth**（多重独立安全层）
4. **Externalized programmable policy**（策略外部化，可配置）
5. **Context as scarce resource**（上下文是稀缺资源）
6. **Append-only durable state**（追加式持久化）
7. **Minimal scaffolding, maximal harness**（最小脚手架 + 最大 harness）
8. **Values over rules**（重价值判断，轻硬规则）
9. **Composable multi-mechanism extensibility**（可组合的多机制扩展）
10. **Reversibility-weighted risk**（按可逆性加权评估风险）
11. **Transparent file-based config/memory**（透明文件而非黑盒数据库）
12. **Isolated subagent boundaries**（子 agent 隔离）
13. **Graceful recovery and resilience**（优雅恢复）

整体架构可以读作两层视图：
- **七组件视图**（高层）：用户 → 接口 → Agent Loop → 权限系统 → 工具 → 状态/持久化 → 执行环境
- **五层视图**（细化）：Surface 层 → Core 层 → Safety/Action 层 → State 层 → Backend 层

---

### Agent 主循环：一个朴素的 while-true

`queryLoop()` 是一个 async generator，每一轮固定走 9 步：设置解析 → 状态初始化 → 上下文装配 → 五个 pre-model shaper → 模型调用 → tool_use 派发 → 权限网关 → 工具执行 → 停止判定。

**不再做的事**：没有显式 planner，没有状态图，没有 tree search。这是 ReAct 的最简实现。

工具执行用 `StreamingToolExecutor`：模型一边流式输出 tool_use，一边并行执行只读工具，写操作串行。结果按收到顺序回填，**保证模型看到的工具结果顺序与它发起请求时的顺序一致**。

恢复机制有五种（输出 token 升级、reactive compact、prompt-too-long 处理、流式回退、fallback model），全部是"先静默自救、不行才告诉人"。

---

### 安全的"七层防御"

任何工具调用都要穿过这七层，**任何一层都可以否决**：

1. Tool 预过滤（被全局拒绝的工具甚至不会出现在模型视野里）
2. Deny-first 规则（deny 永远压制 allow，即使 allow 更具体）
3. Permission Mode 约束（plan / default / acceptEdits / auto / dontAsk / bypassPermissions / bubble 共七模式）
4. Auto-mode ML 分类器（yoloClassifier.ts，独立 LLM 调用判定安全性）
5. Shell sandbox（独立于权限系统的文件系统/网络隔离）
6. Resume 不恢复 session 级权限（强制重新授权）
7. Hook 拦截（PreToolUse 可阻断/重写/异步审批）

**最关键的设计哲学**：Anthropic 自己的研究发现 **用户对权限提示的批准率高达 93%**——这意味着交互式确认在行为上不可靠。所以架构选择是"不靠人盯着"，而是用 sandbox + 分类器把 **需要人决策的次数压低 84%**。

---

### 上下文管理：五层渐进式压缩

模型的上下文窗口是**整套系统的瓶颈资源**。每次模型调用前依次跑 5 个 shaper：

1. **Budget reduction**（始终生效）：单条 tool 结果超尺寸就替换为引用
2. **Snip**：删掉旧历史段
3. **Microcompact**：缓存友好的细粒度压缩
4. **Context collapse**：read-time projection——存储不动，模型看到的是投影视图
5. **Auto-compact**：兜底的全模型生成式摘要

**为什么要 5 层而不是 1 层**：每层成本不同，先做便宜的轻压缩，不行才升级。这是 lazy-degradation 思想。

CLAUDE.md 的四级层次（managed → user → project → local）是**文件型记忆**——刻意拒绝向量数据库，代价是检索粒度只能到文件级。

**重要洞察**：CLAUDE.md 是以"用户消息"形式注入而非 system prompt，因此对模型的约束是**概率性的**。真正的强制力来自 deny-first 的权限规则。这是一个刻意的"指引层（概率） vs 执行层（确定）"分离。

---

### 扩展机制：四个、不是一个

为什么 Claude Code 既有 MCP，又有 plugins、skills、hooks？

答案是这四者**承担的上下文成本不同**：

| 机制 | 独特能力 | 上下文开销 | 注入点 |
|------|----------|------------|--------|
| MCP servers | 外部服务集成 | 高（tool schema） | model() 工具池 |
| Plugins | 多组件打包分发 | 中等 | 三处都可以 |
| Skills | 领域指令 + 元工具 | 低（仅描述） | assemble() 上下文注入 |
| Hooks | 生命周期拦截 | 默认零 | execute() 前/后 |

**梯度上下文成本**意味着便宜的扩展（hooks）可以大量铺开，昂贵的（MCP）保留给真正需要新工具的场景。

---

### 子 Agent：隔离而非共享

通过 `AgentTool`（`Task` 是它的 legacy alias）派遣。子 agent 有三种隔离模式：

1. **Worktree**：临时 git worktree，文件系统隔离
2. **Remote**（仅内部）：远端 Claude Code 运行
3. **In-process**（默认）：共享 FS，隔离上下文

**关键约束**：子 agent **只把最终摘要文本回传给父级**，完整 transcript 走 sidechain 存独立 .jsonl 文件——既保留可审计性，又不污染父上下文。

**代价**：每次调用基本都得自包含 prompt。Anthropic 自己披露 agent teams 模式 **token 开销约为普通 session 的 7×**。

多 agent 协调用**文件锁**而不是 message broker——零依赖、可调试，但牺牲吞吐。

---

### 持久化：append-only JSONL

Session 存为**几乎只追加的 JSONL**。三条独立持久化通道：
- Session transcript（项目级，每 session 一文件）
- 全局 prompt history（仅用户输入）
- 子 agent sidechain（独立 .jsonl + .meta.json）

`--resume` 重放 transcript 重建会话，**但刻意不恢复 session 级权限**——这是把"信任"作为**会话隔离的安全不变量**。

---

### 与 OpenClaw 的对照：同样的问题，不同的答案

OpenClaw 是一个 WebSocket 网关守护进程，连接 WhatsApp / Telegram / Slack 等几十个消息渠道。它和 Claude Code 都要回答同样的设计问题，但答案截然相反：

| 维度 | Claude Code | OpenClaw |
|------|-------------|-----------|
| 系统形态 | 临时 CLI 进程 | 持久化网关 daemon |
| 信任模型 | 每动作 deny-first 评估 + 7 模式 | 网关边界鉴权 |
| Agent runtime | queryLoop() 是系统中心 | Pi-agent 嵌入网关 RPC |
| 扩展架构 | 4 机制按上下文成本梯度 | manifest-first 插件，12 种能力 |
| 内存 | CLAUDE.md 4 级 + 5 层压缩 | 工作区引导文件 + dreaming |
| 多 agent | 父-子任务委派 | 路由 + 委派两层分离 |

**核心洞察**：两者可组合——OpenClaw 可以通过 ACP 把 Claude Code 当作外部 coding harness 托管。agent 设计空间是**层级式**的——网关层和任务层可以叠在一起。

**一句话**：Claude Code 把信任边界放在模型与执行环境之间；OpenClaw 把它放在网关周界。

---

### 五大价值张力

| 张力 | 表现 |
|------|------|
| **Authority × Safety** | 93% 批准率证明人类督查不可靠，安全要靠分类器/sandbox 补 |
| **Safety × Capability** | >50 子命令的 bash 会跳过 per-subcommand 检查——defense-in-depth 的层共享性能瓶颈 |
| **Adaptability × Safety** | 多个 CVE 利用"信任对话框出现前"的 hook / MCP 初始化窗口攻击 |
| **Capability × Adaptability** | 主动式提示让任务完成率 +12-18%，但高频时用户偏好骤降 |
| **Capability × Reliability** | 上下文有界 + 子 agent 隔离 → 局部好决策 ≠ 全局好结果 |

---

### 第六视角：长期人类能力保留

外部经验证据汇总：
- **Becker et al. 2025**（16 名经验丰富开发者 RCT）：AI 工具使开发者**慢 19%**，但他们自我感觉快了 20%
- **Shen & Tamkin 2026**：AI 辅助组**理解力测试低 17%**
- **He et al. 2025**（Cursor 在 807 个仓库的因果分析）：代码复杂度 **+40.7%**，初期速度增益三个月内消散
- **Liu et al. 2026**：30.4 万 AI 提交审计，约 1/4 引入的问题持续到最新版本
- **Kosmyna et al. 2025**（54 人 EEG 研究）：LLM 用户神经连接性减弱，且**移除 AI 后仍持续**
- **Rak 2025**：2023 → 2024 入门级技术岗招聘下降 **25%**

**论文的判断**：Claude Code 显著放大短期能力，但提供的支持长期人类成长、深度理解、代码库连贯性的机制非常有限。

---

### 值得记住的几个判断

> 模型推理在哪里、harness 执行在哪里——是整个 agent 系统设计的根问题。

> 95% 单步准确率下，100 步任务成功率只有 0.6%。——这是为什么每一步都要验证。

> 前沿模型在编码任务上的能力正在收敛，operational harness 的质量正在成为主要差异化因素。

> 工程复杂度不是为了限制模型决策，而是为了让模型能更好地决策。

---

标签：#主题/AI-Coding #手法/权威背书 #场景/技术博客
