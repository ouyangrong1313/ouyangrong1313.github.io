# Harness Engineering 实战：企业级 Java 应用 AI Coding 落地

## 基础信息

- **来源**: 微信公众号 - 阿里云开发者
- **原文链接**: https://mp.weixin.qq.com/s/rlIyIIZOXFObNIXbPI7gDg
- **抓取时间**: 2026-05-07
- **主题标签**: AI Coding, Harness Engineering, 企业级落地, Prompt→Context→Harness 三次跃迁

---

## 核心内容

### 一、三次范式跃迁

| 阶段 | 时间 | 核心关注 | 隐喻 |
|------|------|---------|------|
| Prompt Engineering | 2022-2024 | 单次交互优化 | 写好一封邮件 |
| Context Engineering | 2025 | 给 Agent 看什么 | 给邮件附上正确附件 |
| Harness Engineering | 2026 | 完整系统架构 | 设计多人协作流程 |

### 二、Anthropic 4 种典型失败模式

1. **One-shot Syndrome**：试图一步到位，上下文超过 40% 填充率后质量快速衰退
2. **Premature Victory Declaration**：部分完成就宣布结束，编译都无法通过
3. **Premature Feature Completion**：功能未做端到端验证，部署后才发现问题
4. **Cold Start Problem**：多次会话缺乏持久化记忆，Token Budget 被严重消耗

**核心缺陷**："Agents are incapable of accurately evaluating their own work" —— 无法准确评估自身产出质量。

### 三、Harness 四根支柱

1. **上下文架构**：分层加载，按需获取（L1 会话常驻 / L2 阶段触发 / L3 按需查询）
2. **Agent 专业化**：Planner / Generator / Evaluator 分离，"将做事 Agent 和评判 Agent 分开是强有力的杠杆"
3. **持久化记忆**：进度写在文件系统而非上下文窗口
4. **结构化执行**：未经书面计划批准不得写代码，10 阶段 Pipeline

### 四、真实项目实战（10万行 Java 代码）

#### 四要素架构

```
.harness/
├── agents/          # Agent 角色定义
├── rules/           # 规则体系（工程结构/开发流程/编码规范）
├── skills/          # 技能体系（9个Skill）
├── changes/         # 变更管理
├── mcp/             # MCP Server配置
└── wiki/            # 知识库
```

#### Application Owner Agent

- 约 420 行，承担"Index & Map"职责
- 5 个核心模块：角色背景 / 配置索引 / 核心职责 / 工作流程 / 沟通约束
- 7 项核心职责：需求理解、任务拆解、任务分发、验收、质量把关、文档管理、知识问答

#### 10 阶段开发流程

```
需求分析 → 需求评审 → 编码实现 → 编码评审 → 单元测试编写
    → 单元测试评审 → 代码推送 → CI验证 → 部署验证 → 用户确认
```

每阶段三要素：触发条件 / Skill 加载 / 质量门禁

关键设计：
- 精确的回退路径（CI 失败 → 阶段5，编译错误 → 阶段3）
- 评审循环上限（需求评审最多3轮，编码/测试评审最多2轮）
- 5 个 Human-in-the-Loop 确认点

#### Skill 体系示例

- **coding-skill**：8份分层编码规范（Controller → Service → Domain → DAO → Adapter）
- **expert-reviewer**：Plan Review + Execution Review
- **unit-test-write**：改动驱动测试，优先查线上真实请求出入参

### 五、关键工程经验

1. **Harness 本身需要 Dry Run**：用虚拟需求完整走一遍流程，提前发现缺陷
2. **质量门禁必须可程序化验证**："If it can't be mechanically enforced, the agent will drift"
3. **分离执行与评判是关键杠杆**：编码 Agent + 评审 Agent 分离
4. **流程一致性优先于流程效率**：简单需求也要走完完整流程
5. **规范是活文档**：每行对应一个历史失败案例

### 六、效果数据

| 维度 | 无 Harness | 有 Harness |
|------|-----------|-----------|
| 项目 AI 代码率 | 24.86% | **90.54%** |
| 个人 AI 代码率 | 14.24% | **87.85%** |

关键收益：
- 返工大幅减少（Agent-to-Agent 评审闭环内部完成质量纠偏）
- 交付质量可预期
- 知识沉淀为活的开发手册

### 七、未来展望

- **Self-evolving Harness**：Agent 自动分析失败案例并提出规范改进
- **跨项目 Harness Template**：抽象为可参数化模板，新项目快速复用
- **更精细的 Agent 角色矩阵**：Performance Auditor / Security Scanner / Documentation Sync Agent
- **存量代码库渐进式引入**：模块化引入策略

### 八、核心法则

> **"Agents aren't hard; the Harness is hard."** — Ryan Lopopolo (OpenAI)

> **"Every time you discover an agent has made a mistake, you take the time to engineer a solution so that it can never make that mistake again."** — Mitchell Hashimoto

### 九、开发者角色转变

| 传统模式 | Agent-First 模式 |
|---------|-----------------|
| 写代码 | 设计 Agent 的工作环境 |
| 调 Bug | 编写规范文档 |
| Code Review | 管理任务拆分与验收 |

**核心竞争力从"写代码"转向"设计 Agent 的工作环境"**

---

## 参考资源

- Anthropic: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic: 2026 Agentic Coding Trends Report
- OpenAI: https://openai.com/index/harness-engineering/