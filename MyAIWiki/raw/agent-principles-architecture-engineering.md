# 你不知道的 Agent：原理、架构与工程实践

**来源**：https://mp.weixin.qq.com/s/cIQYl9Wr1Eov4ma-_bYh-w
**作者**：侑夕（阿里云开发者）
**日期**：2026-04-28
**标签**：#主题/AI-Agent #场景/技术博客

---

## 核心结论

1. **更贵的模型带来的提升很多时候没有想象中那么大**，反而 Harness 和验证测试质量对成功率的影响更大
2. **调试 Agent 行为时，应优先检查工具定义**，因为多数工具选择错误都出在描述不准确
3. **评测系统本身的问题很多时候比 Agent 出问题更难发现**，如果一直在 Agent 代码上反复调，效果未必明显

---

## 一、Agent Loop 的基本运转方式

**核心实现逻辑**（不到20行代码）：
```javascript
const messages = [{ role: "user", content: userInput }];
while (true) {
  const response = await client.messages.create({
    model: "claude-opus-4-6",
    max_tokens: 8096,
    tools: toolDefinitions,
    messages,
  });
  if (response.stop_reason === "tool_use") {
    const toolResults = await Promise.all(
      response.content
        .filter((b) => b.type === "tool_use")
        .map(async (b) => ({
          type: "tool_result" as const,
          tool_use_id: b.id,
          content: await executeTool(b.name, b.input),
        }))
    );
    messages.push({ role: "assistant", content: response.content });
    messages.push({ role: "user", content: toolResults });
  } else {
    return response.content.find((b) => b.type === "text")?.text ?? "";
  }
}
```

**控制流**：感知 → 决策 → 行动 → 反馈，四个阶段不断循环，直到模型返回纯文本。

**新能力接入方式**：
- 扩展工具集和 handler
- 调整系统提示结构
- 把状态外化到文件或数据库

**原则**：模型负责推理，外部系统负责状态和边界。核心循环逻辑很少需要频繁调整。

### Workflow 和 Agent 的区别

| 维度 | Workflow | Agent |
|------|----------|-------|
| 控制权 | 代码预定义，同输入必走同一路径 | LLM 动态决策 |
| 执行方式 | 工具顺序固定，错误走预设分支 | 工具按需选择，模型可尝试自我修复 |
| 状态与记忆 | 显式状态机，节点跳转清晰 | 隐式上下文，状态在对话历史中累积 |
| 维护成本 | 改流程需修改代码并重新部署 | 调整系统提示即可 |
| 可观测性 | 日志定位节点，延迟可预估 | 需完整执行记录理解决策链 |
| 人机协作 | 人在预设节点介入 | 人在任意轮次介入或接管 |
| 适用场景 | 流程固定、输入边界清晰 | 需要中间推理与灵活判断 |

### 五种常见控制模式

1. **提示链 Prompt Chaining**：任务拆成顺序步骤，每步 LLM 处理上一步输出
2. **路由 Routing**：对输入分类，定向到对应的专用处理流程
3. **并行 Parallelization**：分段法（独立子任务并发）或投票法（同一任务跑多次取共识）
4. **编排器-工作者 Orchestrator-Workers**：中央 LLM 动态分解任务，委派给工作者
5. **评估器-优化器 Evaluator-Optimizer**：生成器产出，评估器给反馈，循环直到达标

---

## 二、为什么 Harness 比模型更关键

**Harness 四部分**：验收基线、执行边界、反馈信号、回退手段。

### OpenAI 的 Agent 优先开发实践

3个工程师5个月写了百万行代码，将近1500个PR，传统开发速度的10倍。背后的工程决策：

1. **Agent 看不到的内容等于不存在**：知识必须存在于代码库本身，AGENTS.md 只保留约100行作为索引
2. **约束编码化而非文档化**：架构分层靠自定义 Linter 机械强制，不靠人工 Review
3. **Agent 端到端自主完成任务**：验证→复现Bug→实现修复→驱动应用验证→开PR→处理Review反馈→自主合并
4. **最小化合并阻力**：测试偶发失败用重跑处理而不是阻塞进度

### Harness 的关键结论

任务按**清晰度**和**验证自动化程度**分为四种状态：
- 右上角（目标明确+结果可自动验证）= 最适合 Agent 发挥的区域
- Harness 要做的是把任务推进右上角，让对错有机器可以执行的判断标准

---

## 三、上下文工程为什么决定稳定性

**Context Rot**：Transformer 注意力复杂度 O(n²)，上下文越长，关键信号越容易被噪声稀释。

### 上下文为什么要分层

| 层级 | 内容 | 管理方式 |
|------|------|---------|
| 常驻层 | 身份定义、项目约定、绝对禁止项 | 保持短、硬、可执行 |
| 按需加载 | Skills 和领域知识 | 描述符常驻，完整内容触发时再注入 |
| 运行时注入 | 当前时间、渠道ID、用户偏好等 | 每轮按需拼入 |
| 记忆层 | 跨会话经验写入 MEMORY.md | 不直接进系统提示，需要时才读取 |
| 系统层 | Hooks 或代码规则处理确定性逻辑 | 完全不进上下文 |

**原则**：确定性逻辑放进上下文是浪费，凡是可以通过 Hooks、代码规则或工具约束表达的都应交给外部系统。

### 三种常见压缩策略

| 策略 | 成本 | 丢什么 | 适用场景 |
|------|------|--------|---------|
| 滑动窗口 | 极低 | 早期上下文 | 简短对话 |
| LLM 摘要 | 中 | 细节，保留决策 | 长任务、含关键决策 |
| 工具结果替换 | 极低 | 工具原始输出 | 工具调用密集型 |

### Prompt Caching 的原理

Key-Value 对可以缓存（精确前缀匹配），稳定的大系统提示比频繁变动的小提示实际成本更低。写入成本只付一次，后续调用读取折扣可达90%。

### Skills 按需加载

**核心思路**：系统提示只保留索引，完整知识按需加载。

```javascript
const systemPrompt = `可用 Skills：
- deploy: 部署到生产环境的完整流程
- code-review: 代码审查检查清单
- git-workflow: 分支策略和 PR 规范`;
```

**Skill 描述要足够短、足够像路由条件**。反例不是可选项，是 Skill 描述能不能起作用的关键。

数据：有反例准确率从73%到85%，响应时间降18.1%。

### 文件系统做上下文接口

工具调用返回大量 JSON，不如直接写入文件，让 Agent 通过 grep、rg 或脚本按需读取。Cursor 验证：A/B 测试中，调用 MCP 工具的任务总 token 消耗减少46.9%。

---

## 四、工具设计决定 Agent 能做什么

**工具设计三阶段**：
1. **API 封装**：每个 API Endpoint 对应一个工具，粒度过细
2. **ACI（Agent-Computer Interface）**：工具对应 Agent 的目标，而不是底层 API 操作
3. **Advanced Tool Use**：Tool Search、Programmatic Tool Calling、Tool Use Examples

### ACI 工具设计原则

| 维度 | 好工具 | 差工具 |
|------|--------|--------|
| 粒度 | 对应 Agent 要完成的目标 | 对应 API 能做的操作 |
| 示例 | update_yuque_post | get_post + update_content + update_title |
| 返回 | 与下一步决策直接相关的字段 | 完整原始数据 |
| 错误 | 结构化，含修正建议 | 通用字符串 "Error" |
| 描述 | 说明何时用、何时不用 | 只写功能说明 |

**工具设计如何演进**：
- 第一代：API 封装
- 第二代：ACI，工具应对应 Agent 的目标
- 第三代：Tool Search（动态发现）、Programmatic Tool Calling（代码编排）、Tool Use Examples（示例驱动）

**Programmatic Tool Calling**：让模型用代码编排多个工具调用，中间结果在执行环境中流转，不进入 LLM 上下文，token 可从约150,000降到约2,000。

### 为什么工具消息也要隔离

框架产生的内部事件（压缩、通知、工具调用被跳过）需要记在会话历史里，但不应该进 LLM。分两种消息类型：AgentMessage（应用层用）vs Message（发给 LLM 的标准类型）。

---

## 五、记忆系统如何设计

### 四种记忆分别存在哪里

| 类型 | 内容 | 持久化 |
|------|------|--------|
| 上下文窗口 | 工作记忆，当前任务所需的最小信息 | 否，会话级 |
| Skills | 程序性记忆，操作流程、领域规范 | 按需加载 |
| JSONL 会话历史 | 情景记忆，发生了什么 | 磁盘持久化 |
| MEMORY.md | 语义记忆，Agent 主动写入的重要事实 | 是，每次启动时注入 |

### OpenClaw 混合检索

```
memory/YYYY-MM-DD.md — 追加写日志，保留原始细节
MEMORY.md — 精选事实，Agent 主动维护
memory_search — 70% 向量相似度 + 30% 关键词权重
```

对大多数 Agent 来说，结构化 Markdown 加关键词搜索已经具备足够好的可调试性、可维护性和成本表现。

### 记忆整合如何触发并回退

触发阈值：`tokenUsage / maxTokens >= 0.5`

**成功路径**：待整合消息 → llmSummarize → 追加到 MEMORY.md → 只更新 lastConsolidatedIndex

**失败路径**：原始消息写入 archive/，保留完整历史

最关键的是流程本身必须可回退，系统只移动指针，不删除原始消息。

---

## 六、如何逐步放开 Agent 自主度

### 长任务跨 session 继续

**模式**：Initializer Agent + Coding Agent 协作

- **Initializer Agent**：只在第一轮运行一次，生成 feature-list.json、init.sh、初始 git commit 和 claude-progress.txt
- **Coding Agent**：循环执行，每次从 claude-progress.txt 和 git log 恢复现场

**进度放在文件里**，功能清单用 JSON 不用 Markdown。

### 任务状态要显式写出来

```json
{"tasks": [
  {"id": "1", "desc": "读取现有配置", "status": "completed"},
  {"id": "2", "desc": "修改数据库 schema", "status": "in_progress"},
  {"id": "3", "desc": "更新 API 接口", "status": "pending"}
]}
```

同一时间只能有一个 in_progress。

### 后台 I/O 如何接入

把慢速 subprocess 放到后台线程，通过通知队列在下一轮 LLM 调用前注入结果，主循环不需要感知太多并发细节。

---

## 七、多 Agent 如何组织

**两种工作模式**：
- **指挥者模式**：同步协作，人与单个 Agent 紧密互动
- **统筹者模式**：异步委派，人在开始时设定目标，中间让多个 Agent 并行工作，最后再审查产出

### 常见组织方式

主 Agent 作为 Orchestrator，下挂多个子 Agent 独立并行工作，通过 JSONL inbox 协议通信，用 Worktree 隔离文件修改，用任务图管理依赖关系。

### 协作方式要写成协议

```json
{
  "request_id, from_agent, to_agent, content, status: 'pending' | 'approved' | 'rejected', timestamp"
}
```

协议先定，隔离先做，再谈协作和并行。

### 子 Agent 两个基本限制

1. **深度限制**：防止无限递归生成孙 Agent
2. **最小系统提示**：只给 Tooling、Workspace、Runtime 三节，不带 Skills 和 Memory，避免权限外泄

### 多 Agent 下幻觉会互相放大

交叉验证能打断错误传播链：先有可持久化任务图，再引入有身份的队友，再引入结构化通信协议，最后再加交叉验证或外部反馈。

---

## 八、Agent 评测如何做

### 评测结构更复杂

传统 Single-turn 评测是一个 Prompt 进、一个 Response 出。Agent 评测要先准备好工具、运行环境和任务，Agent 在执行过程中多次调用工具、修改环境状态，最后的评分不是看它说了什么，而是跑一批测试验证环境里真正发生了什么。

### 两组核心概念

1. **task**（测什么）、**trial**（跑多少次）、**grader**（怎么打分）
2. **transcript**（完整执行记录）vs **outcome**（环境最终结果）— 两类都要覆盖

### 常用指标

| 指标 | 含义 | 场景 |
|------|------|------|
| Pass@k | k 次至少一次正确 | 探索能力上限 |
| Pass^k | k 次全部正确 | 上线回归 |

### 三类评分器

| 类型 | 典型做法 | 确定性 | 适用场景 |
|------|---------|--------|---------|
| 代码评分器 | 字符串匹配、单元测试 pass/fail | 最高 | 有明确正确答案的任务 |
| 模型评分器 | 按评分标准打分、投票取共识 | 中 | 语义质量、风格 |
| 人工评分器 | 专家抽样审查、标注队列校准 | 可靠但慢 | 建立基准、校准自动 judge |

### 如何从零搭起评测体系

1. 20到50个真实失败案例就够启动
2. 环境隔离：每次运行都要从干净状态开始
3. 正例反例都要测
4. 评分器选择：有明确正确答案优先用代码评分器
5. 定期读完整执行记录，不要只看聚合分数

### 先修评测，再改 Agent

评测系统出问题会导致失真信号，基于它改 Agent 可能从一开始方向就错了。评测系统常见的出错来源：运行环境资源不足、评分器本身有 bug、测试用例和生产场景脱节、只看聚合分数漏掉某一类任务系统性变差。

---

## 九、如何追踪 Agent 的执行过程

### Trace 里需要记录什么

每次 Agent 运行：
- 完整 Prompt，含系统提示
- 多轮交互的完整 messages[]
- 每次工具调用 + 参数 + 返回值
- 推理链，如有 thinking 模式
- 最终输出
- token 消耗 + 延迟

### 两层可观测性分工

**第一层**：人工抽样标注，基于规则采样错误案例，由人工判断执行质量和失败原因
**第二层**：LLM 自动评估，对更大范围的 Trace 做全量覆盖

### 在线评测采样规则

- **负反馈触发**：用户明确表示不满意的 Trace，100% 进队列
- **高成本对话**：token 消耗超过阈值的优先审查
- **时间窗口采样**：每天固定时间段随机采
- **模型或 Prompt 变更后**：头 48 小时全量审查

### 事件流做底座

Agent Loop 在 tool_start、tool_end、turn_end 三个节点发出事件，完整 Trace 同步落盘，再分发给日志系统、UI 更新、在线评测、人工审查队列这些下游。事件一次发布，多路消费，主循环不需要为了任何下游改代码。

---

## 十、用 OpenClaw 看 Agent 如何落地

### 整体架构：五层解耦

| 层 | 实现 | 主要职责 |
|---|------|---------|
| Gateway | WebSocket 服务，端口 18789 | 接住外部连接，统一路由消息和系统控制信号 |
| Channel 适配器 | 23+ 渠道，统一 adapter 接口 | 对接不同渠道，负责消息收发和格式适配 |
| Pi Agent | 对外像一个可调用服务 | 维护 Agent 主循环、会话状态、调度和工具调用 |
| 工具集 | shell / fs / web / browser / MCP | 提供 Agent 可以调用的外部能力 |
| 上下文 + 记忆 | Skills 延迟加载 + MEMORY.md 整合 | 管理系统提示、运行时上下文和跨会话记忆 |

### 消息总线如何把渠道和 Agent 隔开

```javascript
// 入站消息结构，Agent 不知道来自哪个平台
const inbound = { channel, session_key, content };

// MessageBus：渠道和 Agent 之间的解耦层
class MessageBus {
  async consumeInbound() { /* 从队列取下一条消息 */ }
  async publishOutbound(msg) { /* 路由到对应渠道发出 */ }
}
```

### 系统提示按层叠加

顺序从下到上：平台与运行时信息 → 身份层 → 记忆层 → Skills 层 → 运行时注入

对应文件：SOUL.md、AGENTS.md、TOOLS.md、USER.md、MEMORY.md 和 Skills 索引。

### 三种触发模式的加载范围

- **普通会话**：加载完整系统提示
- **子 Agent**：只加载最基础的运行时信息，不带记忆和 Skills
- **heartbeat 模式**：单独加载 HEARTBEAT.md，由系统按固定节奏唤起 Agent 检查是否有任务

---

## 十一、安全边界

### 安全边界三件事

1. **谁能用**：白名单授权，只有授权用户可以触发 Agent
2. **能在哪用**：工作空间隔离，shell 工具需要强制进行路径检查
3. **做了什么可以追踪**：操作审计日志，每次执行都记一笔

### Prompt Injection 防护

- 最小权限：不给 Agent 不需要的工具
- 敏感操作显式确认：向第三方传信息、调用写操作执行前必须让用户确认
- 标注外部内容边界：外部拉取的内容进入上下文时显式标注来源
- 关键路径加独立 LLM 验证

### Provider 故障切换

```javascript
const providers = ["Anthropic", "OpenAI", "Anthropic Sonnet"];
async function runWithFallback(task) {
  for (const provider of providers) {
    try {
      return await runTask(provider, task);
    } catch {
      continue;
    }
  }
  throw new Error("所有 Provider 均不可用");
}
```

---

## 十二、工程实现遵循顺序

1. 单渠道先跑通，Telegram -> Agent -> Telegram 完整链路
2. 安全边界先于功能
3. 记忆整合要早做
4. Skills 先于新工具
5. 第一个失败就建评测

---

## 十三、常见反模式

| 反模式 | 问题 | 怎么修 |
|--------|------|--------|
| 系统提示当知识库 | 越来越长，关键规则被忽略 | 领域知识移到 Skills |
| 工具数量失控 | Agent 频繁选错工具 | 合并重叠工具，明确命名空间 |
| 缺少验证机制 | Agent 说完成了，但没法验证 | 每类任务绑定可执行的验收标准 |
| 多 Agent 无边界 | 状态漂移，故障归因困难 | 明确角色和权限，worktree 隔离 |
| 记忆不整合 | 长对话第20轮后决策质量下降 | 监控 token 占用，超阈值自动触发整合 |
| 没有评测 | 改了一个地方不知道有没有引入回归 | 每个真实失败案例立刻转成测试用例 |
| 过早引入多 Agent | 协调开销超过并行收益 | 先建任务图，验证单 Agent 上限后再扩展 |
| 约束靠期望不靠机制 | 规则在文档里，Agent 选择性遵守 | 期望 -> 工具验证 / Linter / Hook |

---

## 十四、划重点

1. **Agent 核心是感知、决策、行动、反馈的稳定循环**，控制流基本不变，新能力主要通过工具扩展、提示结构调整和状态外化实现
2. **Harness 比模型更关键**，高质量自动化验证和清晰目标缺一不可
3. **上下文工程的重点是防 Context Rot**，分层管理 + 配合压缩策略
4. **工具设计按 ACI 原则**：面向 Agent 目标，边界明确，定义里直接给示例
5. **记忆分四种**：工作记忆、程序性记忆、情景记忆、语义记忆
6. **长任务稳定运行靠状态外化**：进度通过文件传递，不依赖上下文窗口
7. **多 Agent 先有任务图和隔离边界再引入并行**
8. **评测上 Pass@k 验证能力边界，Pass^k 保证上线质量**
9. **可观测性 Trace 是排查的前提，两层要一起用**
10. **真正让 Agent 跑稳，靠的是消息解耦、状态外化、分层提示、记忆整合和安全边界这些工程细节**

---

## 参考资料

1. [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI
2. [Cloudflare, How we rebuilt Next.js with AI in one week](https://blog.cloudflare.com/vinext/) — Cloudflare
3. [Anthropic, Introducing Agent Skills](https://claude.com/blog/skills) — Anthropic
4. [Anthropic, Managing context on the Claude Developer Platform](https://claude.com/blog/context-management) — Anthropic
5. [Anthropic, Measuring AI agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — Anthropic
6. [OpenAI, Designing AI agents to resist prompt injection](https://openai.com/index/designing-agents-to-resist-prompt-injection/) — OpenAI
7. [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic

## 标签

#主题/AI-Agent #场景/技术博客