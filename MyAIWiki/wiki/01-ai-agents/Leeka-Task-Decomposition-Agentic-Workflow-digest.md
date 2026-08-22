---
title: Task Decomposition - Digest
category: 01-ai-agents
date: 2026-06-29
tags:
  - 主题/未分类
nodes: []
---

# Task Decomposition - Digest

## 一句话总结

> **Task Decomposition 是 Agentic Workflow 最底层核心**——90% 的问题不是模型不够聪明，是不会拆；四步法：① 标准化（参数化 + MUST/SHOULD/MAY + Markdown）② 拆解（Pipeline + JSON 数据契约）③ 双向开发（小步快跑）④ MCP 整合（AI 世界的 Type-C）+ Human-in-the-loop Checkpoint。

## 速查表（10 节点）

| # | 节点 | 一句话定义 |
|---|---|---|
| 1 | 三层世界观 | Human SOP（写给人看）/ Skill（单点任务）/ Agentic Workflow（生产线） |
| 2 | 90% 真相 | LLM 能力已够；90% 失败是不会拆，不是模型不够聪明 |
| 3 | Mega Agent 死路 | AGI 来了也不行；黑箱=不可预测+不可观测+不可修复 |
| 4 | 分而治之 | 4 个小 Agent 各干一件边界明确的小事；哪里坏了改哪里 |
| 5 | 标准化 | 参数化 + MUST/SHOULD/MAY（RFC 2119）+ 结构化 Markdown |
| 6 | 拆解与连接 | Pipeline Steps + 严格 JSON 数据契约；上节点 Output = 下节点 Input |
| 7 | 双向开发 | 小步快跑；速度的本质不是首发多完美，而是迭代有多快 |
| 8 | MCP 整合 | MCP = AI 世界里的 Type-C 接口；统一标准调外部 Tools |
| 9 | HITL Checkpoint | 高风险节点（>5000 元/权限变更）必须人工 Approve |
| 10 | 实战案例 | 200 人公司内部请求分拣系统；20 次测试+3 轮迭代→正确率 98%+ |

## 关键金句（5 条）

1. "90% 的原因不是模型不够聪明，而是你根本不知道怎么把一个巨大的、模糊的任务，拆成 AI 真正能跑得动的小 Task。"
2. "高超的任务拆解能力是构建稳定、可观测、生产就绪（Production-ready）系统的唯一地基。"
3. "大公司绝对不敢让这种黑箱系统上 Production，因为他们无法容忍这种不可预测的崩溃。"
4. "速度的本质，不是首发多完美，而是迭代有多快。"
5. "MCP 就是 AI 世界里的 Type-C 接口。"

## 3 个反直觉

- **AGI 来了也必须拆**："这跟帮手够不够聪明没有半毛钱关系"——AI 没有读心术
- **不要等首发完美**："速度的本质不是首发多完美，而是迭代有多快"——小步快跑 + 踩坑 + 补 MUST 规则
- **大公司绝不上 Mega Agent**：黑箱不可预测 + 不可观测 + 不可修复；必须分而治之

### 6 个对 Seetong 借鉴动作

1. **不搞 Seetong "Mega Agent"**：拆成 4-5 个边界明确的小 Skill（设备分诊/反馈分诊/远程操作/添加设备/报警处理）
2. **客服 SOP 四步翻译**：把 Seetong 客服 SOP/反馈分诊 SOP 按 Leeka 四步法翻译成 Skill + Agentic Workflow
3. **MUST/SHOULD/MAY 法则引入**：Seetong AI 助手所有规则用三档标注
4. **MCP 集成规划**：Seetong AI 助手按 MCP 标准接入（设备/反馈/工单/Logan/神策/友盟）
5. **高风险节点强制 HITL**：设备添加/远程开门/解绑/超 N 元支付 → 人工 Approve
6. **双向开发节奏**：先跑粗糙版 1-2 周，踩坑→补 MUST 规则→下一轮迭代，目标正确率 98%+

## 关联 + 备注

- **关联**：`[[01-ai-agents/0xCodez-Agent-Harness-14-Steps]]` / `[[02-ai-coding/Addy-Osmani-Loop-Engineering]]` / `[[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]]` / `[[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]]` / `[[01-ai-agents/清华沈阳-自进化AI新物种]]` / `[[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]` / `[[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]`
- **分类理由**：本文是 Agent 落地方法论，与 Addy（Loop 验证）/ 0xCodez（Harness 14 步）/ 阿里妹（4 层 8 步）同主线"Agent 落地方法"
- **"拆"+"测"互补**：本文（Leeka 任务拆解）+ `[[02-ai-coding/Addy-Osmani-Loop-Engineering]]`（验证才是瓶颈）= Agent 落地完整闭环
- **透明玻璃自检**：wiki ?K（≤8K）/ digest ?K（≤4K）/ 节点 10（6-10）/ H2 ? wiki / H2 ? digest（≤5）/ 表格 ? wiki / 表格 ? digest（≤2）/ 0 陈词 ⭐⭐⭐