# How to Build a Deep Researcher

原文：https://x.com/akshay_pachaar/status/2047395420935229724
作者：Akshay 🚀 (@akshay_pachaar)
平台：X/Twitter
日期：2026-04-24

---

A 100% open-source, self-hostable Deep Research Stack That Beat OpenAI, Gemini, and Perplexity

## 核心结论

用三个开源工具搭建了一个深度研究系统：
- **Onyx** — 检索层
- **CrewAI** — 编排层
- **Voxtral** — 语音层

在 DeepResearch Bench 上排名第一，超越 OpenAI Deep Research、Gemini 2.5 Pro、Perplexity Deep Research。

---

## Why Self-Hosting Matters

使用闭源云服务的真实后果：
1. 你的查询发送到他们的服务器
2. 你的内部数据在他们基础设施上被索引
3. 保留、日志和审计由他们决定
4. 配额和定价按他们的时间表变化

对于受监管行业、有 IP 敏感工作的团队或数据驻留规则下工作的人来说，这是 AI 研究仍然感觉遥不可及的原因。

---

## Why Existing Research Tools Break

大多数研究工具做一次搜索，收集返回的任何内容，然后交给 LLM 写东西。

这适用于浅层查询。但当问到需要跨源综合、矛盾检测或多跳推理的事情时，它就会崩溃。

典型失败：
- Agent 找到一个来源和一个矛盾来源，选择一个继续。矛盾从未浮出水面。
- 两个来源说同样的话但用词不同。报告将两者作为独立证据引用。
- 一个关键连接事实存在于未被检索到的文档中，因为关键词匹配不理解"云迁移"和"将 PostgreSQL 集群迁移到 AWS"是同一件事。

**根本原因：研究不是一项任务。**

---

## What Good Deep Research Requires

无论工具如何，都需要五件事：

1. **阶段分离**
   收集、分析和写作之间有硬墙。每个阶段只从前一个阶段获得干净的输出。

2. **推理检索**
   关键词搜索很脆弱。向量相似度在多跳上崩溃。你需要并行查询变体、智能重组，以及合成前的 LLM 选择步骤。跳过最后一步，幻觉就会进入。

3. **循环中反思**
   静态计划在接触发现时无法存活。当意外表面时，系统应该 pivot，同时跟踪原始计划的覆盖范围。

4. **跨公共源和内部源的统一搜索**
   研究层需要在一条管道中查询开放的 web 和内部知识，权限按文档强制执行。

5. **语音层**
   说话比打字更适合查询。听比读更适合长报告。使工具可达，而不只是可用。

---

## Onyx: 检索层

Onyx 是一个开源 AI 平台，围绕这些原则构建：
- RAG、Web 搜索、代码执行、深度研究和自定义 Agent
- 完全可自托管，因此你的数据永远不会离开你的基础设施

在 DeepResearch Bench（100 个 PhD 级研究任务、22 个领域的独立学术基准）上排名第一。

### 三阶段，不是单一循环

- **Phase 1: Clarification** — 最多 5 个针对短或模糊查询的有针对性问题。为详细查询自动跳过。
- **Phase 2: Planning** — 将查询分解为最多 6 个探索方向。关键选择：Planner 没有工具访问权限，所以它产生计划，而不是答案。
- **Phase 3: Iterative execution** — Orchestrator 和研究 Agent 交替最多 8 个周期，每个周期并行调度最多 3 个 Agent。

### 两个重要分离

- Orchestrator 从不直接搜索
- Research agents 从不看完整查询或计划

这强制自包含的任务简报并防止上下文泄漏。

### 自适应策略

Onyx 根据其发现偏离原始计划。每条调度之间的强制性反思步骤产生结构化输出：
- 覆盖了什么
- 差距是什么
- 出现了什么新方向
- 更多周期是否会产生新信息

### 6步检索管道

每个 Agent 在 LLM 综合任何东西之前运行此：

1. **Query generation** — 并行查询：语义改写、关键词变体、广泛搜索。多部分问题自动拆分。
2. **Search and recombination** — 混合索引（向量 + BM-25），通过 Reciprocal Rank Fusion 合并结果，相邻块合并。
3. **LLM selection** — LLM 审查所有块，只保留相关块。跳过这一步是幻觉进入的地方。
4. **Context expansion** — 对于每个选定的文档，LLM 读取周围块以决定上下文大小。每个文档并行。
5. **Prompt building** — 选定部分与引用和聊天历史组装。
6. **Answer synthesis** — 带内联引用的 grounded 答案，链接到来源。

### 引用完整性

- Agent 在编写中间报告时引用内联
- 来自并行 Agent 的引用合并并重新编号为一组统一集
- 每个最终声明都可以追溯到特定源文档

---

## CrewAI: 编排层

Onyx 处理检索。CrewAI 处理协调。

CrewAI 用三个原语解决阶段分离问题：

- **Flows** — 将独立的 Crew 连接在一起，每个都只从前一个阶段接收干净的输出。没有累积上下文。
- **Skills** — 通过 SKILL.md 在运行时将领域特定指令注入 Agent 的提示。在行动点进行指令。
- **MCP Integration** — 通过 mcps 字段将 MCP 服务器直接附加到 Agent。

### 三 mini-crews，不是单一crew

自然的第一设计是一个 Crew 有三个顺序任务。不要这样做。

跨阶段共享上下文会降解 ground truth。Onyx 团队称之为"deep frying"：
- 事实被重新解释
- 矛盾被平滑覆盖
- 源材料到 Writer 看到时已经无法识别

这个系统使用 Flow：三个独立的 Crew，每个都只从前一个阶段接收干净的输出。

---

## Voxtral: 语音层

每个研究工作流都有一个摩擦点：键盘。

Voxtral 是 Mistral 的原生音频模型系列，从头开始构建用于语音理解和生成，同一个家族处理两个方向：
- 转录在口音、背景噪音和领域词汇中保持准确
- 叙述听起来自然，不机器人

两个变化：
- **语音输入** — 说话提问而不是打字。成绩单直接进入管道。
- **报告叙述** — 完整的 Markdown 报告被读回为表达性语音。

---

## 完整流程

1. 键入、说话或上传 PDF 作为你的研究查询
2. Researcher Agent 通过 Onyx MCP 搜索 web 和你的文档
3. Analyst Agent 对数据进行重复删除、标记矛盾并对发现进行分组
4. Report Writer Agent 生成结构化的、带引用的 Markdown 报告
5. 点击"Play Report"通过 Voxtral TTS 进行叙述

---

## 标签

#主题/AIAgent #主题/AI Coding #手法/对比冲突 #场景/技术博客
