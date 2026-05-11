# Agent 原理、架构与工程实践

## 核心结论

1. **Harness 比模型更关键** — 更贵的模型带来的提升很多时候没有想象中那么大，Harness 和验证测试质量对成功率的影响更大
2. **调试 Agent 优先检查工具定义** — 多数工具选择错误都出在描述不准确，不在模型能力
3. **评测系统本身的问题比 Agent 出问题更难发现** — 如果一直在 Agent 代码上反复调，效果未必明显

---

## Agent Loop 基本运转方式

**核心实现**（不到20行代码）：while 循环 + tool_use 判断 + executeTool + 消息追加

**控制流**：感知 → 决策 → 行动 → 反馈，不断循环直到模型返回纯文本

**接入新能力的三种方式**：扩展工具集、调整系统提示、状态外化到文件

> 模型负责推理，外部系统负责状态和边界。核心循环逻辑很少需要频繁调整。

### Workflow vs Agent

| 维度 | Workflow | Agent |
|------|----------|-------|
| 控制权 | 代码预定义 | LLM 动态决策 |
| 维护成本 | 改流程需重新部署 | 调系统提示即可 |
| 适用场景 | 流程固定 | 需要灵活判断 |

### 五种常见控制模式

1. **提示链 Prompt Chaining** — 任务拆成顺序步骤
2. **路由 Routing** — 输入分类，定向到对应处理流程
3. **并行 Parallelization** — 分段法（独立子任务并发）或投票法（取共识）
4. **编排器-工作者 Orchestrator-Workers** — 中央 LLM 动态分解委派
5. **评估器-优化器 Evaluator-Optimizer** — 循环直到达标

---

## 为什么 Harness 比模型更关键

**Harness 四部分**：验收基线、执行边界、反馈信号、回退手段

### OpenAI Agent 开发实践

3个工程师5个月写百万行代码，1500个PR，开发速度10倍：

1. **Agent 看不到的内容等于不存在** — 知识必须存在于代码库本身，AGENTS.md 只保留约100行索引
2. **约束编码化而非文档化** — 自定义 Linter 机械强制，不靠人工 Review
3. **Agent 端到端自主完成任务** — 验证→复现Bug→实现修复→应用验证→开PR→自主合并
4. **最小化合并阻力** — 测试偶发失败用重跑处理而不是阻塞进度

### Harness 关键结论

任务按**清晰度**和**验证自动化程度**分四种状态，右上角（目标明确+可自动验证）= 最适合 Agent 发挥的区域。

---

## 上下文工程为什么决定稳定性

**Context Rot**：O(n²) 注意力复杂度，上下文越长关键信号越容易被噪声稀释。

### 上下文分层

| 层级 | 内容 | 策略 |
|------|------|------|
| 常驻层 | 身份定义、项目约定、绝对禁止项 | 短、硬、可执行 |
| 按需加载 | Skills 和领域知识 | 描述符常驻，触发时再注入 |
| 运行时注入 | 当前时间、渠道ID、用户偏好 | 每轮按需拼入 |
| 记忆层 | 跨会话经验写入 MEMORY.md | 需要时才读取 |
| 系统层 | Hooks/代码规则处理确定性逻辑 | 完全不进上下文 |

> 确定性逻辑放进上下文是浪费。

### 三种压缩策略

| 策略 | 成本 | 丢什么 |
|------|------|--------|
| 滑动窗口 | 极低 | 早期上下文 |
| LLM 摘要 | 中 | 细节，保留决策 |
| 工具结果替换 | 极低 | 工具原始输出 |

### Skills 按需加载

系统提示只保留索引，完整知识按需加载。描述要足够短、足够像路由条件。**反例不是可选项，是 Skill 描述能不能起作用的关键。**

### 文件系统做上下文接口

工具返回大量 JSON → 直接写入文件 → Agent 按需 grep 读取。Cursor 验证：MCP 工具任务 token 消耗减少46.9%。

---

## 工具设计决定 Agent 能做什么

### 工具设计三阶段

1. **API 封装** — 每个 Endpoint 对应一个工具，粒度过细
2. **ACI（Agent-Computer Interface）** — 工具对应 Agent 目标，不是底层 API
3. **Advanced Tool Use** — Tool Search、Programmatic Tool Calling、Tool Use Examples

### ACI 设计原则

| 维度 | 好工具 | 差工具 |
|------|--------|--------|
| 粒度 | 对应 Agent 目标 | 对应 API 操作 |
| 示例 | update_yuque_post（一次完成目标） | get_post + update_content + update_title |
| 返回 | 与下一步决策直接相关 | 完整原始数据 |
| 错误 | 结构化，含修正建议 | 通用字符串 "Error" |
| 描述 | 说明何时用、何时不用 | 只写功能说明 |

### Programmatic Tool Calling

让模型用代码编排多个工具调用，中间结果在执行环境中流转，不进入 LLM 上下文。Token 可从约150,000降到约2,000。

---

## 记忆系统如何设计

### 四种记忆

| 类型 | 内容 | 持久化 |
|------|------|--------|
| 上下文窗口 | 工作记忆，当前任务最小信息 | 否 |
| Skills | 程序性记忆，操作流程、领域规范 | 按需加载 |
| JSONL 会话历史 | 情景记忆，发生了什么 | 磁盘持久化 |
| MEMORY.md | 语义记忆，Agent 主动写入的重要事实 | 是 |

### 记忆整合触发

**阈值**：`tokenUsage / maxTokens >= 0.5`

**可回退**：系统只移动指针，不删除原始消息。失败时原始消息写入 archive/，保留完整历史。

---

## 如何逐步放开 Agent 自主度

### 长任务跨 session

**模式**：Initializer Agent + Coding Agent

- **Initializer Agent**：第一轮运行一次，生成 feature-list.json、init.sh、claude-progress.txt
- **Coding Agent**：循环执行，每次从文件系统恢复现场

> 进度放在文件里，用 JSON 不用 Markdown。

### 任务状态显式化

同一时间只能有一个 in_progress，每完成一步先更新状态再继续下一步。

---

## 多 Agent 如何组织

### 两种工作模式

- **指挥者模式**：同步协作，人与单个 Agent 紧密互动
- **统筹者模式**：异步委派，人只在起点和终点出现

### 协作协议先于协作

```json
{ request_id, from_agent, to_agent, content, status, timestamp }
```

**顺序**：协议先定，隔离先做，再谈协作和并行。

### 子 Agent 两个限制

1. **深度限制**：防止无限递归生成孙 Agent
2. **最小系统提示**：只给 Tooling、Workspace、Runtime 三节

---

## Agent 评测如何做

### Pass@k vs Pass^k

| 指标 | 含义 | 场景 |
|------|------|------|
| Pass@k | k 次至少一次正确 | 探索能力上限 |
| Pass^k | k 次全部正确 | 上线回归 |

### 两类都要覆盖

- **transcript**：看 Agent 怎么说（执行记录）
- **outcome**：看系统最后变成什么样（环境最终结果）

> "看 Agent 怎么说"和"看系统最后变成什么样"是两件事，两类都要覆盖才能看清楚。

### 先修评测再改 Agent

评测系统出问题会导致失真信号，基于它改 Agent 可能从一开始方向就错了。

---

## 追踪 Agent 执行过程

### Trace 记录内容

- 完整 Prompt（含系统提示）
- 多轮交互完整 messages[]
- 每次工具调用 + 参数 + 返回值
- 推理链（thinking 模式）
- 最终输出
- token 消耗 + 延迟

### 在线评测采样规则

- **负反馈触发**：用户明确表示不满意的 Trace，100% 进队列
- **高成本对话**：token 消耗超过阈值的优先审查
- **模型或 Prompt 变更后**：头48小时全量审查

---

## OpenClaw 架构落地

### 五层解耦

| 层 | 实现 | 职责 |
|---|------|------|
| Gateway | WebSocket 服务，端口 18789 | 接住外部连接，统一路由 |
| Channel 适配器 | 23+ 渠道 | 消息收发和格式适配 |
| Pi Agent | 对外可调用服务 | 维护主循环、会话状态、工具调用 |
| 工具集 | shell/fs/web/browser/MCP | 提供外部能力 |
| 上下文+记忆 | Skills 延迟加载 + MEMORY.md | 管理提示和跨会话记忆 |

### 安全边界三件事

1. **谁能用**：白名单授权
2. **能在哪用**：工作空间隔离，路径检查
3. **做了什么可以追踪**：操作审计日志

---

## 常见反模式

| 反模式 | 问题 | 怎么修 |
|--------|------|--------|
| 系统提示当知识库 | 越来越长，关键规则被忽略 | 领域知识移到 Skills |
| 工具数量失控 | 频繁选错工具 | 合并重叠工具 |
| 缺少验证机制 | 说完成了但没法验证 | 每类任务绑定验收标准 |
| 记忆不整合 | 第20轮后决策质量下降 | 超阈值自动触发整合 |
| 没有评测 | 改了一个地方不知道有没有引入回归 | 真实失败案例立刻转测试用例 |
| 过早引入多 Agent | 协调开销超过并行收益 | 先验证单 Agent 上限 |

---

## 划重点

1. Agent 核心是感知→决策→行动→反馈的稳定循环
2. **Harness 比模型更关键**
3. 上下文工程的重点是防 Context Rot
4. 工具设计按 ACI 原则
5. 记忆分四种，跨会话一致性靠 MEMORY.md + 可回退整合
6. 长任务靠状态外化（文件系统）而非上下文窗口
7. 多 Agent 先有任务图和隔离边界再并行
8. Pass@k 验证上限，Pass^k 保证上线质量
9. Trace 是排查前提，两层可观测性一起用
10. 真正让 Agent 跑稳靠的是**消息解耦、状态外化、分层提示、记忆整合、安全边界**

---

## 参考资料

- [Harness engineering](https://openai.com/index/harness-engineering/) — OpenAI
- [Anthropic, Introducing Agent Skills](https://claude.com/blog/skills) — Anthropic
- [Anthropic, Managing context](https://claude.com/blog/context-management) — Anthropic
- [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic

## 相关链接

- [[ai-personal-knowledge-base-problems|AI 个人知识库：为什么还是那么难用]] — 知识系统需要权威负责
- [[llm-agent-unified-memory-framework|LLM Agent 统一记忆框架综述]] — 记忆系统对比

## 标签

#主题/AI-Agent #场景/技术博客