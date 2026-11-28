# “薄 Agent Loop，厚 Control Plane”：TiDB 用数据库思维重做 Harness - 拆解

- 对应原文：[[InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]
- 来源：微信公众号「InfoQ」；作者：Tina；受访者：TiDB 唐刘；发布：2026-09-06
- 文章性质：访谈与团队实践分享；系统规模、实现细节与效果均以受访方表述为准。

## 一句话

把会快速变化的 Agent Loop 交给可替换的开源核心，把状态、权限、副作用、证据、隔离、失败传播与恢复放进稳定的 Control Plane，才能让 Agent 在生产系统中持续行动而不把模型错误扩散为系统故障。

## 五个核心观点

1. **厚控制面**：Agent Loop、模型与工具协议可替换，稳定投资应放在 Workspace、Sandbox、权限、状态、审计与恢复。
2. **验证即 Harness**：测试、故障注入、随机测试、兼容性测试、性能测试与线上案例不是附属物，而是 Mission Critical 系统敢上线的理由。
3. **目标取代细排程**：模型增强使部分命令式编排转为声明式目标，但 Context、持久状态和失败恢复仍需要上层任务边界。
4. **通信即复杂度**：多 Agent 更适合以隔离 Workspace、清晰 Input/Output 与共享状态协作，而非高频消息广播和角色群聊。
5. **失败是默认前提**：应尽早发现错误、阻断错误事实传播、从最近可信状态 Failover；盲目 Retry 会将局部失误放大。

## 七个分析角度与开头钩子

### 1. 为什么 Agent Loop 要薄
- 模型和 Agent Core 天天变，团队该把工程能力押在哪一层？
- 换一个 Agent Core，为什么不该连 Sandbox 和权限一起重做？
- Agent 越聪明，哪几条边界反而越不能放松？

### 2. Harness 的真正护城河是什么
- 为什么数据库的测试体系可能比核心代码更难复制？
- Agent 说“修好了”，为什么不是完成证据？
- 哪些测试与线上案例，才构成系统敢上线的理由？

### 3. 从命令式到声明式编排
- Agent 变强后，流程图和角色 Prompt 会怎样被淘汰？
- “告诉它要什么结果”之后，哪些任务边界仍必须保留？
- Agent 编排为什么像数据库 Optimizer 的演进？

### 4. Workspace 为什么比 Session 更重要
- Sandbox 被回收后，任务状态为什么不能一起消失？
- 为什么让 Agent 看见 File、底层拥有 Database 能力？
- Version、Branch、Rollback 如何支撑并行探索？

### 5. 多 Agent 为什么要安静
- 为什么十个 Agent 互相聊天，往往比一个 Agent 更难排查？
- 状态共享和消息广播，分别适合解决什么问题？
- 什么时候真的需要五个 Agent，什么时候一个就够？

### 6. Fail Fast 为什么胜过 Retry
- Retry 在什么条件下会从恢复手段变成故障放大器？
- 错误如何在 Context 中从推断变成后续步骤的“事实”？
- 哪些检查点能让系统换 Agent、换路径仍能继续？

### 7. 人的责任为何仍在
- 模型能写代码后，为什么上线、停止和回滚仍需人签字？
- AI 遮蔽枯燥工程实践，会让新工程师失去什么？
- 未来工程师应从“写一行代码”转向定义哪些系统性质？

## 最小实践

1. 将 Agent Core 与 Control Plane 解耦：模型、Loop、工具适配可换；身份、权限、Workspace、状态、审计和副作用策略保持稳定。
2. 对每个高风险动作定义外部不变量、验证证据、幂等/补偿策略与人工升级条件，不接受 Agent 自报完成。
3. 将任务 Workspace 持久化并支持版本、分支、回滚和 Executor 接管，避免 Session 或 Sandbox 回收即丢失工作现场。
4. 多 Agent 默认使用隔离输入输出和状态合流；仅在信息增益大于通信成本时引入同步协作。
5. 为错误建立早期探针、可信 Checkpoint、传播阻断规则和 Failover 路径；在未对账的外部结果上禁止无界 Retry。

## 关联

- [[01-ai-agents/DataFunTalk-Graph-Engineering-从Harness到Ontology]]：该页从任务图、运行时状态、能力路由和恢复描述 Agent 控制面；本文以数据库实践补充为何将可变 Loop 与稳定状态/权限边界分离。
- [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]]：该页给出 Goal 契约、动作回执、可信完成与状态合流；本文补充 Workspace、版本与 Failover 的数据库类比。
- [[01-ai-agents/2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]]：该页列举会话快照、异步任务、多 Agent 隔离和全链路追踪；本文说明这些设施怎样由 Control Plane 组织。
- [[01-ai-agents/源泉TheFountainhead-从GUI到AI-Native-产品接目标界面换职责]]：该页从用户侧解释控制面为何需要承载授权、状态、审查与接管；本文从运行时基础设施解释其实现边界。

## 证据边界

TiDB Cloud Filesystem 的 Workspace 数量、采用 Pi/OpenCode 的迁移、当前架构与多 Agent 探索均为 InfoQ 访谈中的受访方自述，未独立复现或审计。数据库可靠性原则不能直接替代不同业务的安全、合规、性能、成本与可用性验证。

标签： #主题/AI-Agent #主题/Harness工程 #主题/Control-Plane #主题/Agent运行时 #主题/可靠性工程 #主题/多Agent协作 #场景/公众号长文
