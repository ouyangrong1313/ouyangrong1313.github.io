---
title: WorkBuddy Harness 工程复盘：从模型到可用 Agent
category: 01-ai-agents
tags:
  - 主题/WorkBuddy
  - 主题/Harness
  - 主题/Context-Engineering
  - 主题/Loop-Engineering
  - 主题/MCP
  - 主题/Skill
  - 主题/Memory
  - 主题/AI-Agent
  - 场景/微信编译
  - 场景/产品拆解
  - 作者/Anne
  - 编辑/Founder-Park
nodes: [无状态模型, 工具调用协议, MCP三原语, SkillPlugin分层, 上下文五动作, 长期记忆准入, Harness三能力, 五层Harness, Loop组件, 业务验证缺口]
links: [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]], [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]], [[01-ai-agents/HarnessEngineering企业级实战]], [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]], [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[01-ai-agents/Loop-Engineering-验证才是瓶颈]], [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]], [[01-ai-agents/AI-团队协作-Loop-SDD]], [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]], [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]], [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]
date: 2026-07-12
source: 微信公众号「Founder Park」2026-07-12 推送 / Anne（WorkBuddy 团队策略产品经理）
---

# WorkBuddy Harness 工程复盘：从模型到可用 Agent

- **原文标题**：万字复盘：从模型到可用Agent，WorkBuddy的Harness工程是怎么做的？
- **原文链接**：https://mp.weixin.qq.com/s/GkhemHUAhKWV-3Uxaa1Mqg
- **公众号**：Founder Park
- **作者**：Anne，WorkBuddy 团队策略产品经理，负责研发与办公场景 Agent 的上下文策略设计与落地
- **获取时间**：2026-07-13
- **分类理由**：这篇不是单一公司案例，也不是纯理论综述，而是少见的“产品视角一体化长文”——把 Function Call / MCP / Skill / Plugin、Context Engineering、Memory、Harness、Loop 串成一条完整产品化链路；补完 01-ai-agents 主线里“理论原典 + 工程实战 + 验证方法”之间缺的“解释层 / 产品层 / 用户-构建者双视角”。

## 核心结论

> **模型只决定能力上限，真正决定 Agent 能否稳定落地的，是外部那一层上下文组织、能力接入、长期记忆、权限边界、反馈验证和循环编排。WorkBuddy 的价值不在“会不会调模型”，而在把这些环节做成一个可运行、可纠错、可持续的 Harness 系统。**

- **场景**：Agent 产品拆解 / Harness 实战 / 产品化方法论
- **类型**：产品视角的一体化解释（不是单点案例）
- **关键定位**：把“模型 -> 能力层 -> 上下文 -> 记忆 -> Harness -> Loop -> 业务正确性边界”解释成一条连续工程链

## 10 个知识节点（独立概念）

1. **无状态模型**：对产品来说，模型可以先被抽象成“根据输入生成后续文字的函数”。它天然无状态、知识有截止日期，所以产品必须在模型外部维护对话历史、工作进度、记忆和实时信息。这个抽象解释了为什么 Agent 产品一定会长出工具、状态和上下文管理，而不是只靠 prompt。
2. **工具调用协议**：Function Call 的本质是“模型负责提出结构化请求，Agent 负责真正执行”。持有 API Key、发请求、改数据的不是模型，而是 Agent / 宿主系统。因此参数校验、权限审批、审计留痕必须落在模型外部，不能指望 system prompt 自己兜住高风险动作。
3. **MCP 三原语**：MCP 解决的是外部能力怎么标准化接入 Agent。它不只提供工具，还同时提供 `Resources`（读给模型看的材料）、`Tools`（模型触发的动作）、`Prompts`（用户触发的模板消息）。关键不是“多一个协议”，而是把外部系统的读、写、模板调用统一成标准接口。
4. **SkillPlugin 分层**：Tool 回答“一个动作怎么做”，Skill 回答“一类任务按什么流程做”，Plugin 回答“一组连接 + 流程 + 规则 + Hooks 怎么安装和分发”。这是很多团队容易混淆的三层：把流程写成 Skill，才有版本化、可评审、可回滚的空间；把整套能力打包成 Plugin，才适合团队级复用。
5. **上下文五动作**：Context Engineering 不是“把信息塞满窗口”，而是围绕五个动作组织信息：写入（Write）、选择（Select）、检索（Retrieve）、压缩（Compress）、隔离（Isolate）。这套五动作把“模型这一刻该看到什么”从经验判断变成工程动作，是本文最适合抄回自己产品里的框架。
6. **长期记忆准入**：Memory 的核心不是“记住越多越好”，而是决定哪些过去有资格影响未来。WorkBuddy 把长期记忆限定为稳定事实、知识背景、行为信号、表达偏好和会话延续信息五类，并明确排除 Procedural Memory：做事方法不放进长期记忆，而是沉淀为 Skill。这样才能避免一次偶然有效的流程被误升级成长期规则。
7. **Harness 三能力**：从词源拆，Harness 解决三件事：驾驭（Steer）、约束（Constrain）、整合（Integrate）。驾驭负责方向和节奏，约束负责权限与安全，整合负责把 tools / memory / hooks / agents / automation 组装成系统。三者缺一不可：只有引导没有约束，会越跑越偏；只有约束没有反馈，会卡死在错误里；能力很多但没有整合，长任务仍然不稳定。
8. **五层 Harness**：WorkBuddy 把 Harness 落成五层：运行环境层、引导层、反馈层、编排层、迭代层。最有价值的不是层次本身，而是“前馈 + 反馈”的控制系统视角：前馈提高第一次做对的概率，反馈让错误尽量在进入人工审查前被系统自己发现和纠正。
9. **Loop 组件**：Loop Engineering 不是“给任务加个定时器”，而是把任务放进时间维度持续运行。一个完整 Loop 至少需要触发器、独立执行环境、Skill、Tool/MCP、Sub-agent、持久产物、Sensors/Evals、停止条件/预算。特别关键的一句是：**Goal 不是 Loop**。保存目标只是状态组件，距离可运行闭环还差触发、验证、重试和停止。
10. **业务验证缺口**：文章最后最重要的警示不是“AI 多强”，而是“业务正确性仍然缺验证器”。实现和测试可能共享同一个误解，PRD 也常常只覆盖单功能不覆盖组合行为。结论非常实用：当业务正确性缺少可靠验证时，AI 自治度必须随风险提高而下降，支付、风控、订单这类路径仍然要有人类承担最终责任。

## 关联图谱

### 上游（基于 / 来自）
- OpenAI / Anthropic / LangChain 对 Harness 的公开讨论：提供了模型外部系统设计的共识基础
- MCP 标准化趋势：把外部系统接入从“一堆私有集成”拉回到统一协议
- Addy / Lilian / Leeka 这条主线：分别从 Loop、Harness 学术定义、任务拆解补足方法论底座

### 下游（应用于 / 验证于）
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]：印证“状态文件 + 分层知识 + DAG 编排”这条工程路径
- [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]]：印证高风险生产场景里权限、校验、幂等和信任度闭环的重要性
- [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]：印证“没有验证器，Agent 不能从 Demo 走到生产”
- [[01-ai-agents/AI-团队协作-Loop-SDD]]：把本文的产品层解释继续推进到组织协作层和规格层
- [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]：与本文“业务验证缺口”直接形成前后呼应

### 同级（横向 / 并列）
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]：理论原典，提供 Harness 的学术定义和 RSI 视角
- [[01-ai-agents/HarnessEngineering企业级实战]]：企业侧落地，强调 Pipeline、门禁和角色分离
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]]：路线图视角，适合做落地 checklist
- [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]]：从 Anthropic 团队组织协作视角补完“人怎么和 Agent 共事”
- [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]]：Truth Layer + Eval + 组织图重写，是本文在企业级场景的延展

## 正文要点（5 条）

1. **从“模型够强 + prompt 足够好”退回到“模型只是其中一层”**  
   这篇文章最先纠偏的是认知：模型不是产品本身。只要任务涉及外部系统、跨会话延续、权限边界、结果验证和反馈纠正，真正决定可用性的就是模型外部那层工程系统。
2. **把四个常被混用的概念拆干净：Function Call / MCP / Skill / Plugin**  
   很多团队做 Agent 时卡在“工具很多但任务还是不稳定”。这篇文章的价值在于把“动作协议 / 外部接入 / 任务流程 / 能力分发”分层说明，给后续架构设计一个清晰词汇表。
3. **Context Engineering 不是堆 token，而是做信息调度**  
   五动作框架、Prompt Cache 前缀稳定、渐进式加载、工具结果截断策略，说明上下文工程本质上是成本、相关性和正确率之间的调度问题。
4. **Memory 必须有准入机制，且要和 Skill 分开**  
   这篇文章少见地把“陈述性记忆”和“程序性记忆”分开。用户事实与历史状态进 Memory，稳定做法进 Skill。这个分层很重要，它决定系统是在积累经验，还是在积累偏见。
5. **Harness / Loop 的终点不是完全自动，而是把自治度和可验证性对齐**  
   文章最后没有乐观地说“以后都能自动化”，反而强调业务验证缺口、代码库 Harnessability、案例适用边界和持续投入成本。这使它比很多“AI 工程万能论”文章更可信。

## 6 个对 Seetong 团队可借鉴动作

1. **先把 Seetong AI 助手的词汇表统一**：把 Tool / MCP / Skill / Plugin 的边界写成一页规则，避免不同人把“流程”“工具”“插件”混着用，导致能力越积越乱。
2. **把 Context Engineering 的五动作直接变成检查表**：每个新 Skill 都过一遍 Write / Select / Retrieve / Compress / Isolate，尤其检查“哪些信息应该压缩到文件、哪些旁支任务应该隔离给子 Agent”。
3. **Memory 和 Skill 做硬切分**：用户偏好、设备环境、项目背景进 Memory；调试流程、发布流程、反馈分诊 SOP 一律进 Skill。不要让“上次凑巧有效的步骤”长期污染系统行为。
4. **Harness 先补反馈层，再谈更强自治**：对 Seetong 现有 AI 助手，优先补 lint / build / test / review / E2E / rollback / audit 这类反馈信号，让 Agent 每次失败都能拿到可纠正的信息，而不是只收到一句“失败了”。
5. **Loop 必须和验证器绑在一起**：版本回顾、依赖升级、报警汇总、文案生成这类长期任务，如果没有明确的 eval、停止条件和预算，就不要用“自动循环”包装成高级能力。
6. **先挑高 Harnessability 模块试点**：选择结构清晰、边界明确、验证信号足、回滚成本低的模块做 Agent 试点。不要一上来就把最老、最脏、最核心的系统交给 AI 自治。

## 备注与限制

- 这篇文章最大价值是“解释层”和“结构层”，不是给出一套可直接复制的代码实现
- WorkBuddy 的很多具体机制没有公开完整细节，例如内部 Tool/Skill 清单、审批策略、评测指标
- 文中引用 OpenAI / Anthropic / LangChain 的实践，更多是方法论对照，不是可直接迁移的模板
- 对业务正确性的验证缺口，文章指出了问题，但没有给出成熟的通用解法
- 适合和 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]、[[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]、[[01-ai-agents/Loop-Engineering-验证才是瓶颈]] 连读，能形成“理论定义 -> 工程机制 -> 验证边界”的三段理解链

## 相关链接

- [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent-digest]]
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]
- [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]
