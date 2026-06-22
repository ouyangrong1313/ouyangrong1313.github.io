---
title: Claude Code 动态工作流：让 AI 自己写 Harness，这事靠谱吗
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Agent, #场景/公众号长文, #节点/Claude-Code, #节点/Harness, #节点/Context-Engineering, #节点/Multi-Agent]
nodes: [动态工作流, 静态工作流, 偷懒, 自我偏爱, 目标漂移, 扇出合并, 对抗验证, 锦标赛模式, 隔离区, Harness 自我内化, Opus 4.8, ultracode]
links: [[claude-code-dynamic-workflows]], [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]], [[从Prompt-Context到Harness-工程的三次进化与终局之战]], [[AI-Coding的顿悟时刻]], [[HarnessEngineering企业级实战]], [[Harness工程AgentLoop]], [[Claude-Code在大代码库中的最佳实践]]
date: 2026-06-04
source: 微信公众号 / Feisky（编译自 Anthropic 官方博客）
---

# Claude Code 动态工作流：让 AI 自己写 Harness，这事靠谱吗

- 原文链接：https://mp.weixin.qq.com/s/gSwA5Y2Alyf9fu9mmn-32Q
- 原始博客：https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code
- 动态工作流文档：https://code.claude.com/docs/en/workflows
- 作者：Anthropic 工程师 Thariq Shihipar 和 Sid Bidasaria
- 编译：Feisky
- 获取时间：2026-06-04

## 核心结论（一句话）

> **Claude Code 的动态工作流（Dynamic Workflows）** 把"搭建 Harness"这件事也交给 Claude 自己——不再需要预先写好调度脚本，Claude 看任务后自己写确定性 JS 脚本来调度独立子 Agent；适合"不知道最优拆分方式"的探索性任务，但对已有经验的任务静态工作流仍更可控。

## 分类提炼
- 场景：复杂任务自动化、Agent 工程化、AI Coding 进阶
- 标签：#主题/AI-Coding #主题/AI-Agent #节点/Claude-Code #节点/Harness
- 类型：技术解读 / 范式跃迁 / 案例分析

## 知识节点

- **动态工作流**：让 Claude Code 现场根据任务自动写调度脚本，而不是用预先写好的静态 harness
- **静态工作流**：用 Claude Agent SDK 或 claude -p 预先编排好，需要提前考虑各种边界
- **偷懒**：单 Agent 在长上下文里的退化模式——做 50 个检查只查 20 个就宣布完成
- **自我偏爱**：Agent 评判自己产出时天然倾向给好评，对抗性验证场景致命
- **目标漂移**：上下文压缩是有损的，长任务后 Agent 优化的目标已偏离原始需求
- **扇出合并**：最常用的调度模式——拆成多个独立小步，每步一个 Agent，最后合并
- **对抗验证**：每个生成 Agent 配一个独立验证 Agent，专门挑毛病
- **锦标赛模式**：N 个 Agent 两两比较淘汰，留下赢家
- **隔离区**：读不可信外部内容的 Agent 不允许执行高权限操作，避免 prompt injection
- **Harness 自我内化**：Harness 可能像 prompt engineering 一样是模型不够强时的中间状态，未来会被内化
- **Opus 4.8**：足够强到能自己写出高质量 Harness 的模型能力门槛
- **ultracode**：Claude Code 的动态工作流触发词

## 关联图谱

### 上游（基于 / 来自）
- [[claude-code-dynamic-workflows]]：6-3 写的同主题英文原始博客编译版（侧重六种模式 + Prompt 示例）
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]：Harness 是 Agent 系统护城河的总论
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]]：从 Prompt 到 Context 到 Harness 的工程化路径

### 下游（应用于 / 验证于）
- [[HarnessEngineering企业级实战]]：动态工作流是 Harness 落地的最新形态
- [[Harness工程AgentLoop]]：动态工作流 + Agent Loop 的结合
- [[Claude-Code在大代码库中的最佳实践]]：大代码库任务正好命中动态工作流的强项

### 同级（横向 / 并列）
- [[AI-Coding的顿悟时刻]]：AI Coding 整体演化的判断
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]：另一支团队对 Claude Code 用法的判断

## 正文要点

### 单 Agent 的三大退化模式

Claude Code 默认模式是单 Agent 一个上下文窗口搞定规划和执行，**大多数编程任务这就够用**。但有些场景单 Agent 怎么优化都跑不好——三个已知的退化模式：

1. **偷懒**：让它做一轮安全审查，50 个检查项查到 20 个就宣布完成（长上下文行为退化）
2. **自我偏爱**：让它评判自己产出，天然倾向给好评
3. **目标漂移**：上下文压缩是有损的，每压缩一次，原始需求的边缘条件、约束细节丢一点

> 这三个问题不是模型能力问题，是单上下文窗口同时承担规划和执行带来的**架构局限**。

### Dynamic Workflows 工作原理

用独立的子 Agent 各自占一个干净的上下文窗口，每个子 Agent 只干一件事，由**确定性的 JavaScript 脚本**调度它们的执行顺序和依赖关系。

**核心区别**：

| 维度 | 静态工作流 | 动态工作流 |
|------|----------|----------|
| 调度脚本 | 提前写好，考虑各种边界 | Claude 看任务后自己写 |
| 适用 | 已知拆分方式的任务 | 探索性任务 |
| 稳定性 | 可控 | 灵活但需要 Prompt 引导 |

### 六种调度模式

1. **分类路由**：一个分类 Agent 判断任务类型，分发给不同处理 Agent
2. **扇出合并**（最常用）：拆成很多小步，每步一个独立 Agent，最后合并
3. **对抗验证**：每个生成 Agent 配独立验证 Agent 专门挑毛病
4. **生成过滤**：先大量生成，再按标准筛选去重
5. **锦标赛模式**：N 个 Agent 不同策略做同一件事，两两淘汰留赢家
6. **循环到完成**：不设固定轮次，跑满足停止条件

> 这些模式可组合：先扇出，每个分支内部做对抗验证，合并时再跑一轮锦标赛。

### 实际应用场景

| 场景 | 模式 | 关键价值 |
|------|------|---------|
| **大规模迁移和重构** | 扇出 + 对抗验证 | Bun Zig→Rust 重写；每个修改点一个独立 Agent，天然避免交叉污染 |
| **深度验证** | 分类 + 扇出 | 提取文章里的事实性声明，每个声明派 Agent 核实，验证信息源是否可靠 |
| **排序** | 锦标赛 | 按 Bug 严重程度排 1000 条工单；比较判断比绝对评分可靠 |
| **规则遵守** | 分类 + 验证 | CLAUDE.md 规则一条 Agent 验证一条；反向扫日志提炼新规则 |
| **根因分析** | 扇出 + 对抗 | 不锁定单一假设，分别从日志/文件/数据生成假设，每个假设面对验证者和反驳者 |
| **大规模分流** | 分类 + 隔离区 | 工单队列分类、去重、自动修复；读不可信内容的 Agent 不可执行高权限操作 |

### 什么时候不需要工作流

> 动态工作流消耗的 token 显著更多，适合复杂、高价值的任务。

**判断标准**：
- ❌ 不需要：能用一句话说清楚要做什么 + 做完能快速验证
- ✅ 需要：任务可拆成独立并行单元，或验证成本高到不想自己一个个检查

### 用法和技巧

```bash
# 两种开启方式
ultracode  # 触发词
# 或在 Prompt 里要求 "用工作流做这件事"

# 配合 /loop 定期执行
/loop "用工作流扫最近 50 个 session..."

# 配合 /goal 硬性完成条件
/goal "不找到根因不许停"

# 限制 token 消耗
"用 10k token 解决"  # 大概一两轮对话
```

**Prompt 模板示例**：
- `这个测试大概 50 次跑挂一次。用工作流复现它，形成竞争性假设，不找到经得起验证的根因不许停。`
- `用工作流扫我最近 50 个 session，找到我反复在纠正的模式，把重复出现的提炼成 CLAUDE.md 规则。`
- `拿我的商业计划，用工作流让不同 Agent 分别从投资人、客户、竞争对手的视角撕它。`
- `这个文件夹有 80 份简历，用工作流按后端岗位排名，前 10 名交叉验证一遍。先用 AskUserQuestion 问我评分标准。`

**保存工作流**：按 s 可保存脚本到 `~/.claude/workflows`，或通过 Skill 分发给团队。

## 表格：六种调度模式对比

| 模式 | 核心思想 | 适用场景 | 关键风险 |
|------|---------|---------|---------|
| 分类路由 | 任务类型分发 | 异构任务批处理 | 分类器本身的准确性 |
| 扇出合并 | 拆小步并行 | 大规模可拆解任务 | 合并 Agent 的归纳能力 |
| 对抗验证 | 配独立验证 | 需要质量保证的生成 | 验证 Agent 也要强 |
| 生成过滤 | 大量生成+筛选 | 创意/方案探索 | 筛选标准的可定义性 |
| 锦标赛 | 两两淘汰 | 排序/评选 | N 较大时 token 成本 |
| 循环到完成 | 跑到满足 | 开放式目标 | 难以停止 / token 爆炸 |

## 我的理解

- **Harness 也可能是中间状态**——这是这篇文章最有哲学意味的判断。"Harness 可能像 prompt engineering 一样，是大模型发展过程中的一个中间状态……下一代模型根本不需要外部编排，自己就能在内部完成任务分解和对抗验证"
- **动态 vs 静态不是替代关系**——文章明确说"两者不矛盾，动态工作流可以保存下来变成静态的"
- **对 MyAIWiki 的启发**：**这跟 [[Harness不是目的，知识才是护城河]] 是同一判断的两个侧面**——工程化重要但不是终局，知识沉淀和判断力才是
- **实战判断**（按 80/20）：日常工作流**别上动态工作流**（成本不划算），只在"知道这件事复杂 + 验证成本高"时才用

## 适合关联的主题

- [[claude-code-dynamic-workflows]]
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]]
- [[HarnessEngineering企业级实战]]
- [[Harness工程AgentLoop]]
- [[Claude-Code在大代码库中的最佳实践]]
- [[Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]
- [[AI-Coding的顿悟时刻]]
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]
