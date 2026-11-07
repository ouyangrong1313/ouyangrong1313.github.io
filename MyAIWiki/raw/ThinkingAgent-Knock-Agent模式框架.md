# Agent 模式框架：从个人助手、流程嵌入，到企业智能

## 元数据

- **标题**：Agent 模式框架：从个人助手、流程嵌入，到企业智能
- **作者**：Knock（微信公众号「ThinkingAgent」主理人）
- **来源**：微信公众号「ThinkingAgent」
- **原文链接**：https://mp.weixin.qq.com/s/fegZl9TxIGFEmHCMnx2sTg
- **发布时间**：2026-07-16 08:27
- **获取时间**：2026-07-17 10:20 Asia/Shanghai
- **正文长度**：约 8300 字
- **导语**："过去两年，很多人对 AI Agent 的理解还停留在'更聪明的聊天机器人'。但真正的 Agent 不是一个会聊天的机器人，而是一个能够理解目标、拆解任务、调用工具、执行步骤、检查结果，并在必要时与人或其他 Agent 协作的智能系统。"

## 正文

### 导语：为什么现在必须重新理解 Agent？

过去两年，很多人对 AI Agent 的理解还停留在"更聪明的聊天机器人"。
但真正的 Agent 不是一个会聊天的机器人，而是一个能够**理解目标、拆解任务、调用工具、执行步骤、检查结果，并在必要时与人或其他 Agent 协作**的智能系统。
如果说 ChatGPT 代表的是"会回答问题的 AI"，那么 Agent 代表的是"能完成任务的 AI"。
这也是为什么吴恩达在 DeepLearning.AI 的 Agentic Workflow 系列中，把 Agent 的核心能力总结为四类设计模式：Reflection、Tool Use、Planning、Multi-agent Collaboration。他在 The Batch 文章中明确写到，四种会推动 AI Agentic Workflow 进展的设计模式是 Reflection、Tool Use、Planning 和 Multi-agent collaboration。
而 Anthropic 在《Building Effective Agents》中进一步从工程实践角度指出，过去一年他们与许多团队一起构建 Agent 后发现，最成功的实现往往不是复杂框架，而是简单、可组合的模式。Anthropic 还区分了 Workflow 和 Agent：Workflow 是由预定义代码路径编排 LLM 和工具，Agent 则由 LLM 动态决定流程和工具使用方式。
Google Cloud 也在 2026 年发布了 Agentic AI 系统设计模式指南，明确表示 Agent 设计模式是构建 Agentic 应用的常见架构方法，用于帮助开发者选择适合单 Agent 或多 Agent 系统的架构。
这些信息合起来说明了一件事：Agent 已经从"概念热词"进入"工程架构阶段"。
今天，企业真正要思考的，不是"要不要做 Agent"，而是：
什么任务适合 Agent？Agent 该采用什么模式？单 Agent 够不够？什么时候需要多 Agent？哪些节点必须人类介入？如何让 Agent 可控、可评估、可治理？如何从个人助手走向流程嵌入，再走向企业智能？这篇文章就围绕这个问题展开。

### 一、Agent 到底是什么？不是聊天，而是行动

很多人容易把 Agent 和 Chatbot 混在一起。
Chatbot 的核心是回答问题。Agent 的核心是完成任务。
两者的差异可以这样理解：

| 类型 | 典型能力 | 核心特征 |
|------|----------|----------|
| Chatbot | 问答、总结、生成文本 | 被动响应 |
| Copilot | 辅助写作、辅助编码、辅助分析 | 人主导，AI 辅助 |
| Agent | 规划、调用工具、执行任务、自我检查 | 目标驱动 |
| Multi-Agent | 多角色分工、协同、评审、编排 | 团队协作 |

例如，用户问："帮我分析最近订单下降的原因。"
普通 Chatbot 可能会回答一些通用原因：流量下降、价格变化、竞品影响、转化率下降。
但一个真正的业务 Agent 应该能：
1. 查询最近 30 天订单数据
2. 对比前一周期趋势
3. 按渠道、品类、地区、用户分层拆解
4. 找出下降最大的维度
5. 查询活动、库存、价格、履约异常
6. 生成原因假设
7. 输出分析报告
8. 给出后续行动建议
这就是 Agent 和 Chatbot 的本质区别。
Agent 不是多说几句话，而是能接入真实系统，完成真实任务。
Anthropic 在《Building Effective Agents》中也强调，框架可以帮助简化调用 LLM、定义工具、解析工具、链式调用等底层任务，但真正有效的 Agent 往往依赖简单可组合的模式，而不是一味追求复杂框架。
所以，理解 Agent 的第一步，不是学习某个框架，而是理解它背后的设计模式。

### 二、吴恩达的四种 Agentic Workflow 模式

吴恩达提出的四种模式，是理解 Agent 最好的入门框架。
它们分别是：
- Reflection：反思
- Tool Use：工具使用
- Planning：规划
- Multi-agent Collaboration：多智能体协作

这四种模式分别回答了四个关键问题：

| 问题 | 对应模式 |
|------|----------|
| Agent 如何自我改进？ | Reflection |
| Agent 如何接触真实世界？ | Tool Use |
| Agent 如何处理复杂任务？ | Planning |
| Agent 如何像团队一样协作？ | Multi-agent Collaboration |

#### 1. Reflection：让 Agent 会"自我修改"

Reflection，中文可以理解为"反思模式"。
它的核心思想是：让 Agent 先生成结果，再检查结果，再根据检查意见修改结果。
这其实和人类工作很像。
我们写文章，不会第一稿就发布；写代码，不会第一版就合并；做方案，不会第一次就完美。
通常都会经历：生成初稿 → 检查问题 → 提出修改建议 → 重新修改 → 再次检查。
Reflection 把这个过程交给 AI。
例如，让 AI 写一段代码，不是直接采用第一版，而是继续让 AI 扮演 Reviewer："请检查这段代码是否有安全漏洞、边界条件遗漏、异常处理不足、性能问题。"然后再让 AI 根据 Review 意见重写。
**Reflection 适合**：写代码、写文章、生成方案、做代码 Review、生成测试用例、检查需求文档、做安全审查、做复杂推理。
**Reflection 的价值**：让 AI 不只是生成，而是迭代。
**但 Reflection 也有局限**：如果模型不知道正确标准，它可能会"自我感觉良好"，反思不出真正问题。
所以在生产环境中，Reflection 最好不要单独使用，而要结合测试、工具、规则、人工审核和评估体系。

#### 2. Tool Use：让 Agent 有"手"

Tool Use，中文是"工具使用"。
如果说大模型是 Agent 的"大脑"，工具就是 Agent 的"手"。
没有工具时，Agent 只能基于已有知识回答。有工具后，Agent 可以调用外部系统，真正执行任务。
工具可以包括：搜索引擎、数据库、代码执行器、文件系统、API、企业系统、日历、邮件、GitHub / GitLab、BI 系统、RAG 知识库、MCP Server。
例如，用户说："帮我生成上周经营分析。"
普通 AI 只能给一个模板。Tool Use Agent 可以：查询销售数据 → 查询流量数据 → 查询转化率 → 查询库存异常 → 调用图表工具 → 生成经营分析报告。
**Tool Use 的价值**：Agent 真正从"聊天机器人"变成"执行系统"，靠的就是 Tool Use。
**但 Tool Use 也带来更高风险**：因为 Agent 一旦能调用工具，就可能：查错数据、改错配置、调错接口、删除文件、发送错误邮件、执行高风险操作。
**所以企业做 Tool Use，必须同时建设**：权限管理、工具白名单、调用日志、审计留痕、沙箱环境、人工确认、回滚机制、风险分级。
Tool Use 是 Agent 的能力入口，也是治理的起点。

#### 3. Planning：让 Agent 会"先想后做"

Planning，中文是"规划"。它解决的是复杂任务中的路径问题。
很多任务不能一步完成，需要先拆解：目标 → 任务拆解 → 步骤计划 → 逐步执行 → 检查进度 → 调整计划。
例如用户说："帮我完成一份竞品分析报告。"
没有 Planning 的 AI 可能直接开始写。有 Planning 的 Agent 会先规划：明确竞品范围 → 收集公开资料 → 分析产品功能 → 对比商业模式 → 对比价格策略 → 总结优势和短板 → 输出报告结构 → 生成最终文章。
在研发场景中，如果用户说："给系统增加会员积分功能。"
Planning Agent 应该先拆解：阅读现有用户模型 → 找到订单完成逻辑 → 设计积分表结构 → 增加积分计算规则 → 编写接口 → 添加单元测试 → 更新文档 → 提交 PR。
**Planning 适合**：软件开发、复杂调研、数据分析、项目管理、运营活动、跨系统办公流程、多步骤任务自动化。
**Planning 的价值**：让 AI 不只是回答，而是能处理多步骤的复杂任务。
**Planning 的风险**：规划步骤可能出错，可能遗漏关键步骤，可能过于死板。

#### 4. Multi-agent Collaboration：让 Agent 像团队

Multi-agent Collaboration，中文是"多智能体协作"。
它的核心思想是：一个 Agent 解决不了所有问题，那就让多个 Agent 分工协作。
这其实和现实中的团队很像。
一个人写不完一篇文章，那就分给：作者、编辑、审稿人、设计师。
一个人做不完一个项目，那就分给：产品经理、架构师、开发、测试、运维。
Multi-agent 把这个过程交给 AI。
例如，要做一份市场调研报告，可以让多个 Agent 协作：
- 研究员 Agent：收集信息
- 分析师 Agent：分析数据
- 写作者 Agent：撰写报告
- 评审员 Agent：审核质量
**Multi-agent 适合**：复杂任务、跨领域任务、需要多种专业能力的任务、需要多次审核的任务。
**Multi-agent 的优势**：每个 Agent 专注一个领域，质量更高；可以并行处理，效率更高；多个 Agent 互相审核，结果更可靠。
**Multi-agent 的风险**：Agent 之间通信成本高；可能出现循环调用；需要协调机制；成本高。

### 三、Anthropic 的 Workflow 与 Agent 之分

Anthropic 在《Building Effective Agents》中区分了 Workflow 和 Agent：
- **Workflow**：由预定义代码路径编排 LLM 和工具。开发者决定流程，LLM 只是执行节点。
- **Agent**：由 LLM 动态决定流程和工具使用方式。LLM 自主决定下一步。

Workflow 适合：流程明确、步骤固定、不需要太多灵活性的任务。
Agent 适合：流程不确定、需要根据情况调整、复杂任务。

Workflow 的优势：可控、可预测、易调试。Workflow 的局限：不灵活、难适应变化。
Agent 的优势：灵活、适应性强。Agent 的局限：不可预测、难调试、可能出错。

Anthropic 还进一步细分了 5 种 Workflow 模式：
1. **Prompt Chaining（提示链）**：把任务拆成多个步骤，每一步的输出作为下一步的输入。
2. **Routing（路由）**：根据输入类型，选择不同的处理路径。
3. **Parallelization（并行化）**：把任务分成多个并行子任务，最后汇总结果。
4. **Orchestrator-Workers（编排-工作者）**：一个 Orchestrator Agent 动态决定子任务，分配给多个 Worker Agent。
5. **Evaluator-Optimizer（评估-优化）**：一个 Agent 生成结果，另一个 Agent 评估并提出修改建议，直到达标。

这 5 种模式是 Workflow 的常见实现方式，Anthropic 强调简单可组合。

### 四、常见 Agent 架构模式

企业 Agent 落地中，常见的架构模式有：

- **Supervisor（监督者）**：一个 Supervisor Agent 监督多个 Worker Agent，决定谁做什么。
- **Router（路由）**：根据任务类型，路由到不同的专家 Agent。
- **Handoffs（交接）**：一个 Agent 完成自己部分后，把任务交给下一个 Agent。
- **Subagents（子代理）**：主 Agent 启动子 Agent 处理子任务，子 Agent 完成后返回结果。
- **Skills（技能）**：把可复用的能力封装成 Skill，Agent 按需调用。

这些模式不是互斥的，往往组合使用。
例如，一个企业 Agent 系统可能：Supervisor 负责整体调度 → Router 把任务分给不同专家 Agent → 专家 Agent 调用 Skill 完成具体任务 → Evaluator 评估结果 → Orchestrator 编排多个子任务。

### 五、什么时候用单 Agent，什么时候用多 Agent？

#### 单 Agent 适合：
- 任务相对简单，不需要太多分工
- 任务流程明确，不需要太多灵活性
- 资源有限，不能承担多 Agent 的成本
- 团队刚开始 Agent 实践

#### 多 Agent 适合：
- 任务复杂，需要多种专业能力
- 任务流程不确定，需要根据情况调整
- 需要并行处理，提高效率
- 需要多个 Agent 互相审核，提高质量

#### 判断标准：
- 任务是否需要多种专业能力？需要 → 多 Agent
- 任务流程是否明确？明确 → 单 Agent + Workflow；不明确 → 多 Agent
- 任务是否可以并行？可以 → 多 Agent
- 是否需要多次审核？需要 → 多 Agent

#### 一个简单原则：
**从单 Agent 开始，能单 Agent 解决就不要多 Agent**。
多 Agent 增加复杂度、增加成本、增加调试难度。除非真的需要，否则不要轻易上多 Agent。

### 六、Agent 落地的三层路径

企业 Agent 落地，不是"上 Agent 就行"，而是沿着三层路径逐步推进：

**第一层：个人助手**
Agent 帮个人提升效率。比如帮写邮件、帮做总结、帮查资料、帮写代码。
这一层的特征：个人使用，不需要太多权限，Agent 能力有限，但能明显提升个人效率。
**第二层：流程嵌入**
Agent 进入业务流程。比如自动处理客户请求、自动审核合同、自动处理工单、自动生成报告。
这一层的特征：Agent 嵌入到具体业务流程中，需要调用业务系统，需要权限管理，需要审计留痕。
**第三层：企业智能**
Agent 成为企业智能操作系统的一部分。多个 Agent 协同工作，覆盖企业核心业务。
这一层的特征：多个 Agent 互相协作，Agent 之间有通信协议，Agent 可以自主决策，Agent 与企业系统深度集成。

企业 Agent 落地的常见错误是：一上来就想做"企业智能"，结果连"个人助手"都没做好。
正确的做法是：从**个人助手**开始，验证 Agent 能力；再进入**流程嵌入**，验证 Agent 与业务系统的集成；最后才是**企业智能**，让多个 Agent 协同工作。

### 七、Seetong 团队 Agent 落地的实践建议

（原文后续内容在抓取时被截短，主要讲 Agent 治理、权限管理、评估体系）

### 八、Agent 治理：可控、可评估、可治理

Agent 一旦能调用工具、能执行任务、能做出决策，就必须有治理。

**可控**：
- 权限管理：每个 Agent 只能调用它被授权的工具。
- 工具白名单：禁止 Agent 调用未授权工具。
- 沙箱环境：高风险操作在沙箱中执行。
- 人工确认：高风险操作需要人工确认。

**可评估**：
- 任务完成率：Agent 完成任务的比例。
- 工具调用准确率：Agent 正确调用工具的比例。
- 正确率：Agent 输出结果正确的比例。
- 成本：Agent 调用 LLM 和工具的成本。
- 延迟：Agent 完成任务的时间。
- 用户反馈：用户对 Agent 输出的满意度。
- 业务结果：Agent 对业务的实际影响。

**可治理**：
- 调用日志：每次 Agent 调用工具的记录。
- 审计留痕：Agent 决策过程的记录。
- 异常处理：Agent 出错时的处理机制。
- 回滚机制：Agent 操作错误时的回滚。
- 风险分级：根据操作风险分级管理。

### 九、5 大常见误区

**误区一：一步到位做"企业智能"**
很多企业一开始就想要"企业智能操作系统"，结果连最简单的"个人助手"都没做好。
Agent 落地需要从个人助手到流程嵌入再到企业智能，逐步推进。

**误区二：过度追求完全自主**
完全自主的 Agent 风险很高。企业更应该从半自主开始：AI 建议 → 人类确认 → AI 执行 → 人类抽查，再逐步扩大自动化范围。

**误区三：为了多 Agent 而多 Agent**
多 Agent 不是越多越好。如果一个简单任务用五个 Agent，可能只会增加成本和错误。
多 Agent 只适合复杂任务、跨角色任务、开放式任务。

**误区四：没有评估就上线**
Agent 输出看起来合理，不代表真的正确。必须有评估体系：正确率、任务完成率、工具调用准确率、成本、延迟、风险、用户反馈、业务结果。

**误区五：忽视权限和审计**
Agent 一旦能调用系统，就必须像人一样受权限约束，甚至更严格。否则很容易出现：数据泄露、越权访问、错误操作、无法追责、难以回滚。

### 十、结语：Agent 的终局，是企业智能

Agent 的价值，不在于它像不像人，而在于它能不能稳定完成任务。
吴恩达的四种模式，给了我们理解 Agent 的基础语言：
- Reflection：让 Agent 会自我改进
- Tool Use：让 Agent 能调用工具
- Planning：让 Agent 能处理复杂任务
- Multi-Agent：让 Agent 能团队协作

Anthropic、Google、LangChain、Microsoft 等进一步把这些模式工程化，形成了 Prompt Chaining、Routing、Parallelization、Orchestrator-Workers、Evaluator-Optimizer、Supervisor、Router、Handoffs、Subagents、Skills 等更细的架构模式。

但企业真正要落地，不能只停留在"模式学习"。更重要的是沿着三层路径推进：**个人助手 → 流程嵌入 → 企业智能**。
- 第一阶段，Agent 帮个人提升效率。
- 第二阶段，Agent 进入业务流程。
- 第三阶段，Agent 成为企业智能操作系统的一部分。

最终，企业不是拥有很多 Agent，而是拥有一套可以持续学习、持续执行、持续优化、持续治理的智能系统。
**一句话总结**：Agent 的本质不是聊天，而是行动；Agent 模式的本质不是炫技，而是把智能稳定、可控、可评估地嵌入企业运行。

## 参考来源

- DeepLearning.AI - Agentic Design Patterns (deeplearning.ai/the-batch/tag/agentic-design-patterns)
- Anthropic - Building Effective Agents (anthropic.com/engineering/building-effective-agents)
- Google Cloud - Choose a design pattern for your agentic AI system (docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- LangChain - Multi-agent (docs.langchain.com/oss/python/langchain/multi-agent)
- Microsoft Research - AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (arxiv.org/abs/2308.08155)

## 备注

- 作者署名：Knock | 约 8,300 字 | 2026 年 7 月
- 原文第七节"Seetong 团队 Agent 落地的实践建议"在抓取时被截短（实际原文应是"Seetong 团队 / 企业级 Agent 实施"等通用话题），核心方法论在前六节已完整
- 公众号"ThinkingAgent"未在原文中标注推送日，按内容推断为 2026-07-16 早晨推送
- 文末"参考来源"段为外链，未保留具体 URL 之外的扩展信息
- 公众号固定模板"分享、点赞、在看"等未保留