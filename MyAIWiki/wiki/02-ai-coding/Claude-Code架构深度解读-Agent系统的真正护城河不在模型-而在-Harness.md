# Claude Code 架构深度解读：Agent 系统的真正护城河不在模型，而在 Harness

## 核心结论

Claude Code 代码库只有 **1.6% 是 AI 决策逻辑**，其余 98.4% 是确定性运行环境（permission、context、tool routing、recovery）。

**工程复杂度不是为了限制模型，而是为了让模型在一个安全富饶的环境里自由发挥。**

这与 LangGraph（状态图约束）、Devin（显式 planner）走的是相反路线：**最小脚手架 + 最大化 harness**。

## 五种人类价值

| 价值 | 核心命题 |
|------|----------|
| 人类决策权（Authority） | 用户最终拥有控制权 |
| 安全/隐私（Safety） | 即使用户不专心，系统也要保护代码、数据 |
| 可靠执行（Reliability） | 跨上下文窗口、跨会话、跨子 agent 保持一致 |
| 能力放大（Capability） | 让用户做以前根本不会尝试的事 |
| 情境适配（Adaptability） | 系统适应用户项目、习惯、技能 |

**第六视角（评估而非设计）**：长期人类能力保留

## 十三条设计原则

1. Deny-first with human escalation（默认拒绝，升级给人）
2. Graduated trust spectrum（信任是渐进光谱）
3. Defense in depth（多重独立安全层）
4. Externalized programmable policy（策略外部化）
5. Context as scarce resource（上下文是稀缺资源）
6. Append-only durable state（追加式持久化）
7. Minimal scaffolding, maximal harness（最小脚手架 + 最大 harness）
8. Values over rules（重价值判断，轻硬规则）
9. Composable multi-mechanism extensibility（可组合扩展）
10. Reversibility-weighted risk（按可逆性加权评估风险）
11. Transparent file-based config/memory（透明文件）
12. Isolated subagent boundaries（子 agent 隔离）
13. Graceful recovery and resilience（优雅恢复）

## 安全七层防御

任何工具调用必须穿过七层，**任何一层都可以否决**：

1. Tool 预过滤
2. Deny-first 规则
3. Permission Mode 约束（7 模式）
4. Auto-mode ML 分类器
5. Shell sandbox
6. Resume 不恢复 session 级权限
7. Hook 拦截

**关键发现**：用户对权限提示批准率高达 93%，所以架构选择用 sandbox + 分类器把**需要人决策的次数压低 84%**。

## 上下文管理：五层渐进式压缩

| 层级 | 类型 | 说明 |
|------|------|------|
| 1 | Budget reduction | 单条 tool 结果超尺寸就替换为引用 |
| 2 | Snip | 删掉旧历史段 |
| 3 | Microcompact | 缓存友好的细粒度压缩 |
| 4 | Context collapse | read-time projection，投影视图 |
| 5 | Auto-compact | 兜底的全模型生成式摘要 |

**为什么 5 层**：每层成本不同，先做便宜的轻压缩，不行才升级。lazy-degradation 思想。

## 四扩展机制按上下文成本分层

| 机制 | 上下文开销 | 注入点 |
|------|------------|--------|
| MCP servers | 高（tool schema） | model() 工具池 |
| Plugins | 中等 | 三处都可以 |
| Skills | 低（仅描述） | assemble() 上下文注入 |
| Hooks | 零 | execute() 前/后 |

## 子 Agent：隔离而非共享

三种隔离模式：Worktree（文件系统隔离）、Remote（远端 Claude Code）、In-process（默认，共享 FS）

**关键约束**：子 agent 只把最终摘要文本回传给父级，完整 transcript 走 sidechain 存独立 .jsonl 文件。

**token 开销**：agent teams 模式约为普通 session 的 **7×**

## 与 OpenClaw 对照

| 维度 | Claude Code | OpenClaw |
|------|-------------|----------|
| 系统形态 | 临时 CLI 进程 | 持久化网关 daemon |
| 信任边界 | 模型与执行环境之间 | 网关周界 |

**核心洞察**：两者可组合，agent 设计空间是**层级式**的。

## 关键判断

> 模型推理在哪里、harness 执行在哪里——是整个 agent 系统设计的根问题。

> 95% 单步准确率下，100 步任务成功率只有 0.6%。

> 前沿模型在编码任务上的能力正在收敛，harness 的质量正在成为主要差异化因素。

> 工程复杂度不是为了限制模型决策，而是为了让模型能更好地决策。

## 标签

#主题/AI-Coding #手法/权威背书
