---
title: Task Decomposition：Agentic Workflow 最底层的核心观念
category: 01-ai-agents
tags:
  - 主题/任务拆解
  - 主题/Agentic-Workflow
  - 主题/Agent落地
  - 主题/MCP
  - 主题/Human-in-the-loop
  - 主题/Leeka
  - 节点/三层世界观
  - 节点/90%真相
  - 节点/Mega-Agent死路
  - 节点/分而治之
  - 节点/四步法
  - 节点/MUST-SHOULD-MAY
  - 节点/MCP-Type-C
  - 节点/HITL-Checkpoint
nodes: [三层世界观, 90%真相-不会拆, Mega-Agent死路, 分而治之-Divide-and-Conquer, 四步方法论标准化, MUST-SHOULD-MAY法则, JSON数据契约, MCP-AI世界Type-C, Human-in-the-loop-Checkpoint, 双向开发小步快跑]
links: [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[02-ai-coding/Addy-Osmani-Loop-Engineering]], [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]], [[01-ai-agents/清华沈阳-自进化AI新物种]], [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]], [[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]
date: 2026-06-29
source: 微信公众号(RPA/AI 教程类)2026-06-29 推送 作者 Leeka（影刀 RPA 高级工程师 + 生财有术航海教练）
---

# Task Decomposition：Agentic Workflow 最底层的核心

- 原文链接：https://mp.weixin.qq.com/s/dFZDxPH7HjKV46mE8w1hww
- 作者：Leeka（影刀 RPA 高级工程师 / 生财有术 RPA 航海教练 / 专攻 AI 编程 + AI 写作）
- 公众号定位：RPA / AI 教程类
- 发布时间：2026-06-29

## 核心结论（一句话）

> **Task Decomposition 是 Agentic Workflow 最底层核心**——**90% 的问题不是模型不够聪明，是不会拆**；四步法：① 标准化（参数化 + MUST/SHOULD/MAY + Markdown）② 拆解（Pipeline + JSON 数据契约）③ 双向开发（小步快跑）④ MCP 整合（AI 世界的 Type-C）+ Human-in-the-loop Checkpoint。

### 分类提炼

- 场景：Agent 落地方法论 / 任务拆解 / Workflow 编排
- 标签： #主题/任务拆解 #主题/Agentic-Workflow #主题/Agent落地 #主题/MCP #主题/Human-in-the-loop
- 类型：实操方法论（4 步法 + 实战案例 + 7 个 Seetong 借鉴动作）

## 知识节点（10 个独立概念）

- **三层世界观**：Human SOP（写给人看，含默会知识）/ Skill（单点任务执行单元）/ Agentic Workflow（串联多个 Agents/Tools/Skills/数据源的全自动生产线）
- **90% 真相**：LLM 底层能力已足够强，**90% 的失败不是模型不够聪明，是不会把大任务拆成 AI 真正能跑得动的小 Task**
- **Mega Agent 死路**：AGI 来了也不行——AI 没有读心术；黑箱 = 不可预测 + 不可观测 + 不可修复；大公司绝不敢让黑箱上 Production
- **分而治之（Divide and Conquer）**：4 个小 Agent 各干一件边界明确的小事；哪里坏了改哪里，对症下药——可预测性 + 可观测性 + 可修复性 = 自动化工作流在生产环境活下去的铁律
- **四步法·标准化**：参数化（Temperature 模板化）+ MUST/SHOULD/MAY 法则（RFC 2119）+ 结构化 Markdown（Parameters/Steps/Error Handling 三段式）
- **四步法·拆解与连接**：Pipeline Steps + 严格 JSON 数据契约（Artifact）；上一节点 Output = 下一节点 Input
- **四步法·双向开发**：小步快跑——首发粗糙 SOP + 跑一轮 + 踩坑 + 补 MUST 规则 + 下一轮迭代；**速度的本质不是首发多完美，而是迭代有多快**
- **四步法·MCP 整合**：**MCP = AI 世界里的 Type-C 接口**；Claude/ChatGPT/Cursor 都可用同一套标准调外部 Tools/Resources
- **Human-in-the-loop Checkpoint**：高风险节点（财务支出 > 5000 元 / 权限变更 / 设备解绑 / 远程开门）必须人工 Approve
- **实战案例**：200 人公司"内部请求分拣系统"——20 次测试 + 3 轮迭代 → 正确率 98%+

## 关联图谱

### 上游（基于 / 来自）
- 斯坦福 AI 系统构建教学影片（2026）/ Leeka 个人 AI 落地咨询案例 / RFC 2119 网络协议规范

### 下游（应用于 / 验证于）
- **Seetong AI 助手**：如何拆成多个边界明确的小 Skill（避免 Mega Agent）
- **Seetong 客服 SOP 翻译**：Human SOP → Skill + Agentic Workflow
- **Seetong 高风险节点**：设备添加/远程开门/解绑/支付 → Human-in-the-loop Checkpoint

### 同级（横向 / 并列）
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] - Agent Harness 14 步法（工程框架）
- [[02-ai-coding/Addy-Osmani-Loop-Engineering]] - Loop Engineering 验证才是瓶颈（**本文是"拆"，Addy 是"测"，互补**）
- [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]] - 4 层架构 8 步流程（业务端）
- [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]] - 阿里淘宝 Agent 工程实战
- [[01-ai-agents/清华沈阳-自进化AI新物种]] - 自进化 AI 新物种
- [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]] - Multica AI Native 组织
- [[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]] - Harness vs 知识护城河

### 正文要点（5 条）

1. **三层世界观**（Human SOP / Skill / Agentic Workflow）——Human SOP 靠默会知识补全，AI 缺这能力；Skill = 单点任务执行单元；Agentic Workflow = 整条现代化生产线
2. **Mega Agent 死路**——AGI 来了也不行（"这跟帮手够不够聪明没有半毛钱关系"）；黑箱不可预测 + 不可观测 + 不可修复；大公司绝不敢上 Production
3. **四步法·标准化**——参数化 + MUST/SHOULD/MAY + 结构化 Markdown；MUST 是铁律（不能跳过），SHOULD 是强烈建议（特殊情况可跳过但必须 Log），MAY 是可选
4. **四步法·拆解 + 双向开发 + MCP 整合**——Pipeline Steps + JSON 数据契约 + 首发粗糙小步快跑 + MCP 整合外部工具
5. **Human-in-the-loop Checkpoint**——高风险节点（>5000 元/权限变更）必须人工 Approve；AI 是执行者，人是方向盘

### 6 个对 Seetong 团队可借鉴动作

1. **不搞 Seetong "Mega Agent"**：按 Divide and Conquer 拆成 4-5 个边界明确的小 Skill（设备分诊/反馈分诊/远程操作/添加设备/报警处理）
2. **客服 SOP 四步翻译**：把 Seetong 客服 SOP/反馈分诊 SOP 按 Leeka 四步法翻译成 Skill + Agentic Workflow
3. **MUST/SHOULD/MAY 法则引入**：Seetong AI 助手所有规则用三档标注；写进 `seetong-knowledge-system/SKILL.md`
4. **MCP 集成规划**：Seetong AI 助手按 MCP 标准接入内部系统（设备/反馈/工单/Logan/神策/友盟）
5. **高风险节点强制 HITL**：设备添加/远程开门/解绑/超 N 元支付 → 人工 Approve
6. **双向开发节奏**：先跑粗糙版 1-2 周，踩坑→补 MUST 规则→下一轮迭代，目标正确率 98%+

### 备注与限制

- 本文是 RPA/AI 教程类公众号推送，核心是 Agent 落地的"任务拆解"方法论
- 与 [[02-ai-coding/Addy-Osmani-Loop-Engineering]] 区别：Addy 关注"Loop 验证"，本文关注"任务拆解"——**"测"+"拆"互补**
- 与 [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] 区别：0xCodez 是 14 步 Harness 框架，本文是 4 步 SOP 翻译法
- 与 [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]] 区别：阿里妹 4 层 8 步（业务端），本文 4 步翻译（Human SOP → Workflow）
- **核心反直觉**：AGI 来了也必须拆——"这跟帮手够不够聪明没有半毛钱关系"
- **未展开**：MCP 协议具体技术细节（Leeka 假设读者已了解）；Skill 文件夹具体结构

### 相关链接

- 原文：https://mp.weixin.qq.com/s/dFZDxPH7HjKV46mE8w1hww
- 同主线 [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] / [[02-ai-coding/Addy-Osmani-Loop-Engineering]] / [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]] / [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]] / [[01-ai-agents/清华沈阳-自进化AI新物种]] / [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]] / [[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]
- 反向参考：[[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]（知识护城河比 Harness 重要；本文"任务拆解"也是"比 Harness 更底层的地基"）
