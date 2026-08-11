---
title: "东方屹腾：执行型 Agent 从零到稳定交付"
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/执行型Agent
  - 主题/Harness
  - 主题/企业SaaS
  - 场景/落地案例
  - 场景/企业SaaS
  - 场景/工作流自动化
  - 节点/执行型Agent分野
  - 节点/控制叙事二元论
  - 节点/机械状态平面
  - 节点/会话统一状态平面
  - 节点/锚账集与分层记忆
  - 节点/ReAct到规划执行
nodes: [执行型Agent分野, 控制叙事二元论, Orchestrator意图网关, ReAct到规划执行, HITL阻塞续作, 机械状态平面, 会话统一状态平面, 锚账集与分层记忆]
links: [[01-ai-agents/未来属于垂直领域Agent]], [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]], [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]], [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]], [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]], [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]]
date: 2026-07-17
source: ADPS 企业 Agent 系统蓝皮书 v0.2 / 梁博 / 上海东方屹腾案例
---

# 东方屹腾：执行型 Agent 从零到稳定交付

- 原文链接：https://adpsagent.com/zh/cases/liangbo-execution-agent/
- 来源：ADPS（Agent Design Patterns Society）企业 Agent 系统蓝皮书 · 案例报告 01
- 发布日期：2026-07-13
- 获取时间：2026-07-17

## 核心结论（一句话）

> **对企业 SaaS 的执行型 Agent，真正决定稳定交付的不是“工具能不能接进来”，而是能否把业务 API 的机械参数绑定从 LLM 生成里剥离出去，落成 Orchestrator + 规划执行 + 机械状态平面 + 会话统一状态平面的工程骨架。**

## 分类提炼

- **场景**：企业 SaaS 工作流自动化 / 高约束事务执行 / 生产级 Agent
- **标签**： #主题/执行型Agent #主题/Harness #场景/企业SaaS #场景/工作流自动化
- **类型**：案例蓝皮书 / 架构复盘
- **适用前提**：系统是封闭企业体系；步骤依赖明确；参数错一位就会失败或破坏数据

## 知识节点（8 个独立概念）

- **执行型Agent分野**：执行型 Agent 交付的是业务系统状态变化，而不是文本内容；它与内容生成型 Agent 的复杂度根本不在一个量级。
- **控制叙事二元论**：控制平面负责把自然语言收敛成可驱动执行流的机械信号，叙事平面负责理解目标、总结进展和支撑推理。
- **Orchestrator意图网关**：Orchestrator 是所有能力的宿主，意图网关消费控制信号并把系统路由到不同的执行链。
- **ReAct到规划执行**：ReAct 适合“干一步看一步”，但遇到严格顺序依赖的事务流时，会自然逼出任务 DAG、规划器、执行器和状态机。
- **HITL阻塞续作**：一旦任务图和状态机成为一等公民，关键节点阻塞、人工审批和恢复续作就能自然接到主干上。
- **机械状态平面**：关键参数不再混在叙事上下文里由 LLM 感知再生成，而是进入一个按坐标和 Provenance 管理的独立状态平面。
- **会话统一状态平面**：SessionNarrative、SessionState、Workspace 三个平面分别负责进展、参数和调度，构成三权分立的会话运行态。
- **锚账集与分层记忆**：锚固定原始目标，账持续记录关键里程碑，集在关键推理入口做蒸馏投影；L1/L2/L3 记忆再补上跨步骤经验召回。

## 关联图谱

### 上游（基于 / 来自）

- 东方屹腾 HR SaaS 的真实薪资、考勤、审批、报税业务流
- ADPS 模式矩阵与企业 Agent 蓝皮书体系

### 下游（应用于 / 验证于）

- [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]]：高风险业务流程里，如何把工具边界、幂等性、审批门和状态治理落到生产
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]：状态文件、DAG 编排、渐进式知识加载和脚本化执行，是“长链路状态化”的另一种企业实现
- [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]]：truth layer、eval 和组织层 AI Factory，是执行型 Agent 进入企业大规模运转后的延伸形态

### 同级（横向 / 并列）

- [[01-ai-agents/未来属于垂直领域Agent]]：提供“企业 Agent 应拆成更小、更专、更可控的 domain-specific agents”视角
- [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]]：补上任务拆解、数据契约、MUST/SHOULD/MAY 和 HITL checkpoint 的方法论
- [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]：从产品视角解释 Tool / Skill / Plugin / Context / Harness / Loop 如何分层
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]：给出 Harness 的理论原典和“模型重要性 = Harness 重要性”的学术视角

## 正文要点（6 条）

### 一、先分清：执行型 Agent 不是内容生成型 Agent

这篇案例的第一刀切得很准。MCP 在“搜资料 -> 写报告 -> 做 PPT”这类内容型任务里很好用，因为主链上传递的是文本结果，语义有偏差也未必致命；但在报销、薪资组搭建、入职办理这类事务流里，步骤之间传递的是机械参数，错一位就不是“内容不够好”，而是业务失败甚至脏写数据。

### 二、真正的痛点不在“看起来像 AI”，而在“第一次配置太难”

东方屹腾没有把精力放在分析报表、经营建议这类更容易展示智能感的场景，而是锁定了薪资组快速搭建这个冷启动痛点。这个锚点非常关键：它决定系统必须解决事务流程、状态依赖、参数绑定和回滚，而不是仅仅生成一份漂亮的解释文本。

### 三、从起步开始就把前端和可观测性做成底座

作者强调的“前端尽早做精美”和“把 Agent 的意识和行为对开发者可观测”很务实。企业里，展示层不是装饰；可观测性也不是附属功能。对执行型 Agent 来说，看得到每一步 Thought / Action / Observation / LLM 调用 / 成本 / 工具动作，是压住复杂度的基础设施。

### 四、控制 / 叙事二元论让系统第一次真正可控

在意图识别阶段，团队就识别出运行态里有两种不同的平面：一种是控制信号，一种是叙事上下文。前者要机械、稳定、能驱动程序；后者要承载理解、总结、压缩和推理。这条二元论很重要，因为它把“Agent 很智能”的模糊直觉拆成了“程序控制什么，LLM 理解什么”。

### 五、ReAct 足够灵活，但严格事务流最终会逼出规划执行和 HITL

ReAct 适合“干一步看一步”，但当薪资组搭建这种流程要求“先匹配模板、再建快照、再导入、失败则回滚”时，靠 ReAct 临场决定步骤顺序就会跨步或漏步。于是系统自然长出任务 DAG、规划器、执行器和状态机，随后又顺理成章接上 HITL 阻塞审批和恢复续作。

### 六、真正把系统从“会跑”变成“稳定交付”的，是机械状态平面和三权分立

全文最值钱的部分，是作者直面了一个行业里常被含糊带过的问题：**LLM 不适合承担确定性参数复制。**  
`template_id`、申请 id、审批单 id 这类东西不能混在上下文里让模型“生成出来”，必须进入一个独立的机械状态平面；而整个会话运行态也要分成叙事状态平面、机械状态平面、任务调度状态平面三部分。再叠加锚、账、集和 L1/L2/L3 记忆，系统才有机会在长链路里保持稳定。

## 5 个可借鉴动作

1. **不要把 LLM 当参数复制器。**  
   只要步骤之间传递的是确定性 id、状态码、版本号、资源句柄，就应该把它们外化成独立状态，而不是塞进上下文让模型去猜。
2. **先选一个真实锚点场景，而不是做“最像 AI”的 demo。**  
   执行型 Agent 的工程骨架，不会从花哨的分析报告里长出来，只会从刚需事务流里长出来。
3. **把可观测性和审批门做进主干，而不是后补。**  
   执行型 Agent 的失败不是“答得不够好”，而是会直接写系统、调工具、跑任务；调试和治理必须一开始就有。
4. **当 ReAct 开始漏步时，别继续硬调 prompt。**  
   这是进入规划执行、任务 DAG 和状态机的时候，不是再多加几条提示词的时候。
5. **迁移前先问自己是不是封闭企业体系。**  
   机械状态平面之所以能成立，前提正是工具注册和状态键字典都由你自己控制。

## 相关链接

- [[01-ai-agents/cases/liangbo-execution-agent-digest]]
- [[01-ai-agents/未来属于垂直领域Agent]]
- [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]]
- [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]]
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]
