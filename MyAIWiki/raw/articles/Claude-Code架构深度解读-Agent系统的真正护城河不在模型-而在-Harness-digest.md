# Claude Code 架构深度解读 — 拆解

## 核心观点

1. **1.6% vs 98.4%** — Claude Code 代码库只有 1.6% 是 AI 决策逻辑，98.4% 是确定性运行环境
2. **最小脚手架 + 最大化 harness** — 与 LangGraph、Devin 相反的设计路线
3. **七层安全防御** — 任何工具调用都可被否决，deny-first 规则
4. **五层渐进式上下文压缩** — lazy-degradation 思想，每层成本不同
5. **四扩展机制按上下文成本分层** — MCP/Plugins/Skills/Hooks 各有用途
6. **子 agent 摘要回传** — 不共享 transcript，token 开销 7×
7. **长期人类能力保留问题** — AI 工具使开发者慢 19%，但他们自我感觉快了 20%

## 7 个分析角度

### 角度1：核心数字
1.6% AI 决策 vs 98.4% 运行环境。工程复杂度是为了让模型在安全环境里自由发挥。

### 角度2：设计哲学
最小脚手架 + 最大化 harness。与 LangGraph 状态图、Devin 显式 planner 相反。

### 角度3：安全七层
Tool 预过滤 → deny-first 规则 → Permission Mode → ML 分类器 → Shell sandbox → Resume 隔离 → Hook 拦截。

### 角度4：上下文管理
五层渐进式压缩：Budget reduction → Snip → Microcompact → Context collapse → Auto-compact。

### 角度5：扩展机制
MCP（高成本）→ Plugins（中）→ Skills（低）→ Hooks（零成本）。

### 角度6：OpenClaw 对照
Claude Code：临时 CLI，信任在模型与执行环境之间。OpenClaw：持久化网关，信任在网关周界。

### 角度7：价值张力
Authority × Safety、Safety × Capability、Capability × Adaptability、Capability × Reliability。

## 关键判断

- "模型推理在哪里、harness 执行在哪里——是整个 agent 系统设计的根问题。"
- "95% 单步准确率下，100 步任务成功率只有 0.6%。"
- "前沿模型在编码任务上的能力正在收敛，operational harness 的质量正在成为主要差异化因素。"
- "工程复杂度不是为了限制模型决策，而是为了让模型能更好地决策。"

## 标签

- #主题/AI-Coding
- #手法/权威背书
- #场景/技术博客
