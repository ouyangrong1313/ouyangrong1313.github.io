# 从 Harness 杀到 Ontology：Graph Engineering 开始重构 Agent 系统

- 原文链接：https://mp.weixin.qq.com/s/qLlAUiVI1MFZ4PWiupXQwg
- 来源：微信公众号「DataFunTalk」
- 作者：DataFunTalk
- 发布：2026-09-04 13:00
- 获取时间：2026-09-05
- 抓取方式：`isolated-chrome-cdp`
- 抓取正文 SHA-256：`29a0f474e92c38a29986185eb25bbf924ae1eb36d0a6c8e18906dd849ba4c296`
- 清理说明：已删除文中重复出现的非正文推广与互动文本。

## 正文（去广告版）

过去两年，Agent 工程的重心持续向模型外部扩张：Prompt Engineering 组织指令，Context Engineering 决定推理时提供什么信息，Harness Engineering 把工具、Memory、Skills、执行环境和验证机制接到模型周围，Loop Engineering 再把这些能力组织为规划、行动、观察、验证和适应的循环。

当任务变成长期、并行、有依赖、需要独立验证且必须保存状态的系统问题，瓶颈不再是单个 Agent 缺少什么能力，而是多个智能组件怎样共同完成任务。Yuyuan Feng 等人在 2026 年 8 月的综述《Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence》中将这一步概括为从 Individual Intelligence 走向 System Intelligence：以显式、动态、可演化的图结构组织任务、协调 Agent、维护运行时状态。

Graph Engineering 关注 DAG 调度、并发同步、能力路由、共享状态一致性、依赖链故障定位和长程失败恢复。事务、血缘、Checkpoint、Replay、Rollback 等分布式系统概念进入 Agent 语境；但因模型输出具有概率性、任务结构会动态变化且持续与环境交互，不能将 Agent Runtime 直接等同传统数据平台。

## 01 Agent 越强，系统问题越突出

综述将能力分为三个层级。Model Intelligence 来自预训练、后训练与 Prompt/Context Engineering，关注给定上下文中的理解、推理和任务完成。Individual Intelligence 则在模型外围加入 Harness 与 Loop：Foundation Model 提供理解、推理和规划，Harness 提供知识、工具、记忆、技能和执行环境，Loop 组织感知、推理、行动、反馈与状态更新。

复杂软件工程、科学发现和企业流程同时需要异构专业能力、依赖子任务、并发执行、独立验证和长期状态维护。把它们压进一个 Agent Loop 会导致上下文争用、可并行操作被串行化、同步点不可见、状态混在同一轨迹、局部失败无法保留其他有效进度。

Graph Engineering 因而分为三块：Task Organization 回答做什么，表达任务、依赖、顺序、并发和验证约束；Agent Coordination 回答谁来做，将任务映射到 Agent、模型、工具与资源；Runtime State Management 回答实际发生了什么，记录确认状态、冲突、故障来源、有效进度和恢复路径。

## 02 DAG 回来：显式组织任务

简单任务可让模型在上下文中生成步骤并逐步执行；一旦存在前后依赖、并行分支、验证节点和动态重规划，计划就需要外化为显式图。节点表示子任务或中间目标，边表示先后、数据或逻辑依赖，计划从模型可读文本变成运行时可调度、检查和修改的结构。

文中以 LLMCompiler 为例：它将 Function Calling Plan 编译为 Dataflow DAG，上游满足后立即执行准备就绪的节点；Plan-over-Graph 从依赖图生成并行 Agent Schedule；TDAG 和 Flow 允许根据中间结果继续拆任务、调整依赖，并驱动多 Agent 的生成、分配和协作。

图工程不止于画图。语义任务需要被编译为 LLM Call、Agent、Retriever、Tool、Memory Operation、Aggregator、Verifier 等算子，并不断优化结构。GPTSwarm 将语言 Agent 表示为计算图；ADAS、AutoFlow、AFlow 搜索 Agent Workflow；DyFlow、EvoFlow、QualityFlow 用运行时反馈调整子图。较合理的形态不是人工写死 DAG，也不是任由 Prompt 自由规划，而是模型提出或修改结构，运行时负责约束、调度、验证并记录结果。

## 03 Runtime State 比 Memory 更关键

任务图和团队图只能描述预期结构；运行中还会产生任务进度、角色绑定、共享事实、资源变化、外部副作用和中间承诺。进入多 Agent 与长程执行后，若状态没有一致且可追溯的表示，不同 Agent 会读取到不同事实，故障难以定位，已完成工作也难以恢复。

综述把 Runtime State Management 拆成 State Recording、Fault Localization 和 Failure Recovery。State Recording 不等于记忆：每次状态转换需要记录 evidence、provenance 和 version。Magentic-One 的 Task Ledger 与 Progress Ledger、Graph of States 的结构化 Belief State、PatchBoard 的 Schema/权限/不变量校验、MemTX 的 tentative writes 与 transactional belief commits，分别说明“提议 -> 验证 -> 提交”应成为状态边界。并发写入还需考虑隔离、因果顺序和冲突解决；append-only history 与 Event Sourcing 用于重建、回放和分支。

最终错误往往不是首次错误的位置。系统需保留 Actor、Transition、Dependency 与 Validation Evidence，将根因作为待验证假设。恢复时必须划定边界：哪些状态撤销、哪些内部计算重放、哪些外部副作用只能补偿。Event Sourcing、AgentGit、Shepherd 支持 replay、rollback、branching；DART 强调恢复到语义有效边界；SagaLLM、RAC 和 Atomix 将 checkpoint、补偿与可逆/不可逆操作结合。恢复后模型仍可能需要重新规划，而非机械重走原路径。

## 04 多 Agent 需要 Control Plane

Agent Coordination 包括 Capability Modeling、Team Organization 和 Multi-agent Communication。能力建模不能只写角色提示词，而要显式表示技能、资源、模型、权限、可靠性与任务适配度，使运行时在工具权限或资源变化时能寻找兼容替代者。

文中提到 DyLAN 估计候选 Agent 的任务贡献，MasRouter 按任务难度和成本选择协作模式、角色和模型，SkillGraph 用技能关系指导通信拓扑，MaAS 在 Agentic Supernet 中搜索多 Agent 结构。真正的调度依据应是能力、成本、权限、资源和可靠性，而非 Researcher、Coder、Reviewer 等静态名称。

团队结构可为链式、路由式、Fan-out/Fan-in 或动态重构。MetaGPT、ChatDev 使用链式分工；Magentic-One 由 Orchestrator 规划、委派、监控和重规划；Mixture-of-Agents、MacNet 并行生成再聚合；Puppeteer、AgentNet 根据运行状态调整连接。更多通信不必然更好，通信图仍需权衡信息价值、调用成本和错误传播。

综述提出 Graph-Native Agent Operating Systems：将 Task、Agent、Capability、Runtime State 都提升为一等系统对象，以类型化、版本化图统一表示。共享 Runtime 可提供调度、能力发现、状态存储、事件与溯源日志、结构化事务、权限执行、Checkpoint、Replay、Rollback 与图级可观测性。MCP、LangGraph、AIOS 分别提供能力接入、显式工作流/状态和操作系统视角的前置形态，但尚缺统一的 Agent System 结构底座。

## 05 Agent 的下一步回到系统工程

Agent 越自主，外围基础设施越需要确定性。若依赖、状态、权限、错误传播和恢复都藏在上下文里，生产系统难以稳定可控。Graph Engineering 的变化是从能力增强转向系统组织：模型负责产生智能，系统负责调度、验证、恢复和治理这些智能组件。

综述还讨论 System Evolution 与 Ontology Engineering。运行时的成功、失败和结构调整可反哺任务图、团队结构、能力关系和状态图，但必须受 provenance、versioning、validation、replay、rollback 约束；Ontology Engineering 为任务完成、证据充分、状态有效、权限合法等概念建立共享实体、关系、类型与约束语义，避免各 Agent 自行解释系统状态。

## 资料来源

Yuyuan Feng et al., “Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence”, arXiv:2608.21156v2, 2026-08-26。

标签： #主题/AI-Agent #主题/Graph-Engineering #主题/Harness工程 #主题/运行时状态 #主题/Agent-OS #主题/本体工程 #场景/公众号长文
