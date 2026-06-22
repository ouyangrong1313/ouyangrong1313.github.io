---
title: Claude Code 作者 Boris：我已经不写 prompt 了，我写 loop
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Agent, #场景/公众号长文, #节点/Claude-Code, #节点/Harness, #节点/Agent-Loop, #节点/Dynamic-Workflow]
nodes: [Dynamic Workflow, Boris Chernyshev, loop 而非 prompt, agent API, parallel, pipeline, Agentic laziness, Self-preferential bias, Goal drift, Fan-out, Adversarial verification, Tournament, Generate-and-filter, Classify-and-act, Loop until done, token 预算, quarantine, bracket 排序]
links: [[claude-code-dynamic-workflows]], [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]], [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]], [[Claude-Code团队只招聘两类人-会做梦的人+懂底层的人]], [[Harness工程AgentLoop]], [[HarnessEngineering企业级实战]], [[Skills驱动推理新范式]]
date: 2026-06-04
source: 微信公众号 / winkrun（编译自 Boris Chernyshev 30 分钟演讲）
---

# Claude Code 作者 Boris：我已经不写 prompt 了，我写 loop

- 原文链接：https://mp.weixin.qq.com/s/-Mhg_EEibje5tkWlVazdMA
- 来源：微信公众号 / winkrun
- 原始内容：Boris Chernyshev（Claude Code 作者）30 分钟演讲
- 获取时间：2026-06-04

## 核心结论（一句话）

> **Boris 已经不写 prompt 了，他写 loop**——Claude Code + loops + Dynamic Workflow 让"写代码"从"一次性 prompt 拿结果"变成"养管道"；Boris 的工作从"对话者"变成"管道养作者"，核心是用 `agent() / parallel() / pipeline()` 三个 API 配合 6 种基本模式组合出 2-4 种真实 workflow。

## 分类提炼
- 场景：AI 编程实战、Dynamic Workflow 落地、Boris 工作流揭秘
- 标签：#主题/AI-Coding #主题/AI-Agent #节点/Claude-Code #节点/Harness
- 类型：实战揭秘 / API 详解 / 避坑指南

## 知识节点

- **Boris Chernyshev**：Claude Code 作者，演讲核心论断"我不写 prompt 写 loop"
- **loop 而非 prompt**：工作范式转变——从"对话者拿一次结果"变成"养管道，长期运行多个 loop"
- **Dynamic Workflow**：Anthropic 2026-05-28 上线，让 Claude 临场写 harness（JS 文件）
- **agent API**：Dynamic Workflow 的核心三件套之一——生成独立子 agent
- **parallel**：barrier 语义——扇出后等所有结果返回才继续
- **pipeline**：流式语义——每个元素独立流过每一阶段（更便宜更快）
- **Agentic laziness**：长任务做一半就宣布完成（如 50 项审计只做 20 项）
- **Self-preferential bias**：让 Claude 验证自己输出时倾向偏袒自己
- **Goal drift**：多轮后逐渐偏离目标，每次压缩都会丢信息
- **Classify-and-act**：分类路由——便宜模型分类，贵模型只用在需要的地方
- **Fan-out-and-synthesize**：扇出合并——50 个文件安全审计最适合
- **Adversarial verification**：对抗验证——验证者从没看过原始工作，没法偏袒
- **Generate-and-filter**：先生成 30 个想法，再用 rubric 筛选，逼 Claude 晚做承诺
- **Tournament**：成对比较淘汰赛——比绝对打分可靠得多
- **Loop until done**：循环 + 停止条件，配合 `/goal` 设硬性标准
- **token 预算**：必须在 prompt 里写"use 10k tokens"——不封顶能烧到预期 5-10 倍
- **quarantine**：处理用户提交内容必须隔离——读取 agent 只读，动作 agent 不接触原文
- **bracket 排序**：要排 1000 个东西搞个 tournament bracket，别想着一次性排序

## 关联图谱

### 上游（基于 / 来自）
- [[claude-code-dynamic-workflows]]：6-3 写的英文原始博客编译版（Anthropic 官方视角）
- [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]：上午写的 Feisky 编译版（侧重判断 + 取舍）
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]：Harness 思想的总论

### 下游（应用于 / 验证于）
- [[Harness工程AgentLoop]]：本篇的 agent/parallel/pipeline API 是 Agent Loop 的具体实现
- [[HarnessEngineering企业级实战]]：Dynamic Workflow 是 Harness 落地的最新形态
- [[Skills驱动推理新范式]]：保存的 workflow 脚本可作为 Skill 分发

### 同级（横向 / 并列）
- [[Claude-Code团队只招聘两类人-会做梦的人+懂底层的人]]：同一团队的组织方法论
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]：同一团队的工作原则

## 正文要点

### 一、核心论断

> 我现在不再给 Claude 写 prompt 了，我有一堆 loop 在跑。**我的工作是写 loop**。

Boris 30 分钟演讲把自己的 Claude 配置摊开讲：**Claude Code + loops + Dynamic Workflow**。

### 二、Dynamic Workflow 是什么

Anthropic 2026-05-28 上线 Dynamic Workflows。默认 Claude Code 把规划和执行塞进同一个上下文窗口，**大多数写代码的活够用**——但碰到长任务、大规模并行、强结构化、对抗性任务就崩。

以前 Anthropic 内部要靠工程师手搓 harness（Research、Code Review、agent 团队都是这么来的）。**Dynamic Workflows 让 Claude 自己临场写这个 harness**——一个 JavaScript 文件，里面用几个特殊函数 spawn 子 agent，再用标准 JS 处理数据。

**相比默认 harness，多了三件事**：

| 维度 | 默认 | Dynamic Workflow |
|------|------|-----------------|
| 上下文 | 共享 | 每个子 agent 独立窗口 |
| 模型 | 单一 | 每个子 agent 可指定（Opus/Sonnet/Haiku） |
| 隔离 | 无 | worktree（独立 git checkout）或 remote |

**启动方式**：跟 Claude 说"给我做一个 workflow……"，或触发词 `ultracode`。**中途被打断也能恢复**。

### 三、结构性解决三个老毛病

Anthropic 发布文档点了三个失败模式：

1. **Agentic laziness**：复杂多步任务做一半宣布完成（50 项审计做了 20 项）
2. **Self-preferential bias**：让 Claude 验证自己时倾向偏袒自己
3. **Goal drift**：多轮后逐渐偏离目标，第 47 轮时"不要做 X"这条约束悄悄消失

**Workflow 用结构来解**：不同 Claude / 各自上下文 / 目标聚焦 / 状态隔离。

### 四、静态 vs 动态

| 维度 | 静态 workflow | 动态 workflow |
|------|--------------|--------------|
| 写法 | 提前写好 | Claude 临场写 |
| 边界 | 保守，兼顾所有 | 量身定制 |
| 适用 | 已知任务 | 探索性任务 |
| 优势 | 稳定 | **贴着你的上下文塑形**：读你的代码 / 对照新供应商真实文档 / 按你的数据定价 / 用对抗 pass 攻击自己的初步答案 |

> 动态版本赢的不是搜索，是它能**贴着你的上下文塑形**。

### 五、核心 API 三件套

| API | 语义 | 适用 |
|-----|------|------|
| `agent()` | 生成独立子 agent | 通用 |
| `parallel()` | **barrier**——扇出后等所有结果回来才返回 | 下一步必须等全部结果 |
| `pipeline()` | 流式——每个元素独立流过每一阶段 | 不需要等全部，更便宜更快 |

**选哪个就看一个问题**：下一步是不是必须等全部结果？是就 parallel，不是就 pipeline（更便宜更快）。

### 六、6 个常用模式

| 模式 | 核心思想 | 适用 |
|------|---------|------|
| **Classify-and-act** | 便宜模型分类，贵模型只用在需要的地方 | 异构任务批处理 |
| **Fan-out-and-synthesize** | 拆成多个独立小任务并行跑，再合并 | 50 个文件安全审计 |
| **Adversarial verification** | 验证者没看过原始工作，没法偏袒 | 专治 self-preferential bias |
| **Generate-and-filter** | 30 个想法 + rubric 筛掉一批 | 逼 Claude 晚做承诺 |
| **Tournament** | 成对比较，淘汰赛 | 排序/品味判断（1000 个东西排个 bracket）|
| **Loop until done** | 循环 + 停止条件 + /goal 硬性标准 | 开放式目标 |

> 这 6 个模式很少单独出现，**一个真实 workflow 通常组合 2-4 个**。

**真实案例**：Anthropic 把 Bun 从 Zig 重写到 Rust 用的就是"**Fan-out（一个 agent 一个 callsite）→ 对抗验证 → loop until done**"。

### 七、容易踩的坑（Claude Code 团队自己的提醒）

1. ❌ **该用普通 session 解决的事别上 workflow**——大多数日常编码任务不需要 5 个评审
2. ❌ **不设 token 预算**——一个野心大的 workflow 不封顶能烧到预期的 **5 到 10 倍**；直接在 prompt 里写 `"use 10k tokens"`
3. ❌ **让同一个 agent 既干活又验证**——self-preference 让验证形同虚设
4. ❌ **把 parallel() 和 pipeline() 当一回事**——barrier 差别很关键
5. ❌ **loop 模式不配 /goal**——它会在第一个软完成点停下
6. ❌ **让不可信内容直达执行 agent**——处理用户提交内容必须 **quarantine**——读取 agent 只读，动作 agent 不接触原文
7. ❌ **排序用绝对打分**——换成 tournament 配对比较
8. ❌ **跑通的 workflow 不保存**——在 workflow 菜单按 `s` 存到 `~/.claude/workflows`，或打包成 Skill 分发

### 八、旁观者视角

网友总结：

> Boris 不小心把 n8n 整套 UX 哲学说了一遍——一个 loop 看 webhook，一个 loop 看 schedule，一个 loop 盯队列。**你不再跑任务，你在养管道**。

> 但编排层得先稳，再上动态路由，不然会被自己绕死。

## 表格：parallel vs pipeline 决策

| 场景 | 应该用 | 理由 |
|------|--------|------|
| 50 个文件安全审计，最后给一份报告 | `parallel()` | 必须等所有审计结果 |
| 1000 条 ticket 批量分类，按类型路由到不同处理 | `pipeline()` | 元素独立流过分类→处理 |
| Bun 重写：callsite 改完 + 跑测试 + 改下一个 | `pipeline()` | 元素间有依赖但不需要 barrier |
| 多角度撕商业计划，最后合并 | `parallel()` | 必须等所有视角回来 |
| 实时数据流处理 | `pipeline()` | 元素独立流过 |

## 我的理解

- **这是 Dynamic Workflow 主题的"第 3 篇"**——6-3 英文官方版、上午 Feisky 编译版、本篇作者亲述实战版。**三篇配套看最完整**：
  - 6-3 英文版侧重**六种模式 + Prompt 示例**
  - 上午 Feisky 版侧重**判断 + 取舍**（什么时候不用）
  - 本篇 Boris 实战版侧重**API 三件套 + 避坑指南**

- **"我写 loop 不写 prompt" 是 2026 年最值得记住的范式转变**——跟 [[Claude-Code团队只招聘两类人]] 是同一团队在**两个层面**的呼应：
  - 组织层：写 prompt 的人才画像 → 写 loop 的人才画像
  - 个人层：执行者 → 管道养作者

- **token 预算是真实坑**——`"use 10k tokens"` 这种 prompt 限制**必须成习惯**，否则一个 workflow 能烧掉 5-10 倍预算

- **quarantine 模式**是最有防御价值的工程实践——跟 [[陈春花-AI时代管理者重建判断权]] 的"隔离区"判断是同一回事：**读和写分离，避免 prompt injection 导致的越权**

- **"你不再跑任务，你在养管道"**——这个比喻对 Seetong 团队很有启发：核心问题不是"AI 能不能做这个 task"，而是"我能不能维护一个长期跑的管道"

## 适合关联的主题

- [[claude-code-dynamic-workflows]]
- [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- [[Claude-Code团队只招聘两类人-会做梦的人+懂底层的人]]
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]
- [[Harness工程AgentLoop]]
- [[HarnessEngineering企业级实战]]
- [[Skills驱动推理新范式]]
- [[陈春花-AI时代管理者重建判断权]]
