# Harness Engineering 实战：从 25% 到 90% AI 代码率

## 一句话

通过 Harness Engineering 体系，让企业级 Java 应用（10万行代码）的 AI 代码率从 24.86% 提升至 90.54%。

## 三次范式跃迁

| 阶段 | 时间 | 核心 | 隐喻 |
|------|------|------|------|
| **Prompt Engineering** | 2022-2024 | 单次交互优化 | 写好一封邮件 |
| **Context Engineering** | 2025 | 给 Agent 看什么 | 给邮件附上正确附件 |
| **Harness Engineering** | 2026 | 完整系统架构 | 设计多人协作流程 |

## Anthropic 4 种失败模式

| 模式 | 描述 | 解决方案 |
|------|------|---------|
| **One-shot Syndrome** | 上下文超过 40% 填充率后质量衰退 | 分层加载，按需获取 |
| **Premature Victory** | 部分完成就宣布结束 | 结构化执行，Quality Gate |
| **Premature Feature Complete** | 未做端到端验证 | Browser Automation (Puppeteer MCP) |
| **Cold Start Problem** | 多次会话缺乏持久化记忆 | 进度写文件系统，非上下文窗口 |

**核心缺陷**："Agents are incapable of accurately evaluating their own work"

## 四根支柱

1. **上下文架构**：L1 常驻 / L2 阶段触发 / L3 按需查询
2. **Agent 专业化**：Planner / Generator / Evaluator 分离
3. **持久化记忆**：进度在文件系统，不在上下文窗口
4. **结构化执行**：未经批准不得写代码

## 10 阶段 Pipeline

```
需求分析 → 需求评审 → 编码实现 → 编码评审 → 单元测试编写
    → 单元测试评审 → 代码推送 → CI验证 → 部署验证 → 用户确认
```

关键设计：
- 回退路径：CI失败→阶段5，编译错误→阶段3
- 评审上限：需求3轮，编码/测试各2轮
- 5个 Human-in-the-Loop 确认点

## 四要素架构

```
.harness/
├── agents/          # Application Owner (~420行)
├── rules/           # 工程结构/开发流程/编码规范
├── skills/          # 9个Skill（request-analysis/coding-skill/expert-reviewer/...）
├── changes/         # 变更管理（每需求一个目录）
├── mcp/             # MCP Server配置
└── wiki/            # 知识库
```

## 效果数据

| 维度 | 无 Harness | 有 Harness |
|------|-----------|-----------|
| 项目 AI 代码率 | 24.86% | **90.54%** |
| 个人 AI 代码率 | 14.24% | **87.85%** |

## 关键工程经验

1. **Harness 本身需要 Dry Run** - 用虚拟需求走一遍全流程
2. **质量门禁必须可程序化验证** - "If it can't be mechanically enforced, the agent will drift"
3. **分离执行与评判是关键杠杆** - 编码 Agent + 评审 Agent
4. **流程一致性优先于流程效率** - 简单需求也要走完完整流程
5. **规范是活文档** - 每行对应一个历史失败案例

## 核心法则

> **"Agents aren't hard; the Harness is hard."** — Ryan Lopopolo, OpenAI

> **"Every time you discover an agent has made a mistake, you take the time to engineer a solution so that it can never make that mistake again."** — Mitchell Hashimoto

## 开发者角色转变

| 传统模式 | Agent-First 模式 |
|---------|-----------------|
| 写代码 | 设计 Agent 的工作环境 |
| 调 Bug | 编写规范文档 |
| Code Review | 管理任务拆分与验收 |

**核心竞争力从"写代码"转向"设计 Agent 的工作环境"**

---

## 相关资源

- 原文：[[2026-05-07-阿里HarnessEngineering企业级实战]]
- 相关：[[Harness工程AgentLoop]] / [[harness-engineering]]
- Anthropic: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- OpenAI: https://openai.com/index/harness-engineering/