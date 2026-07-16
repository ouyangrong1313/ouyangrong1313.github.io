---
title: 小龙虾 OpenClaw - Digest
category: 01-ai-agents
date: 2026-06-29
---

# 小龙虾 OpenClaw - Digest

## 一句话总结

> **Agent 没那么玄乎——"把程序员写死在代码里的 if-else，挪到了运行时让模型现挂"**;3 大结论:① 不存在通用 Agent(特定场景做深)② 受控的自由(明确边界下的受控智能)③ Agent 价值在于智能(用不稳定性换泛化能力);**"老板要 Agent ≠ 真要 Agent"**——翻译 3 类真实需求:**API+RAG**(提效)/ **Workflow+SOP**(替代人工)/ **Agent+受控**(高价值决策)。

## 速查表(10 节点)

| # | 节点 | 一句话定义 |
|---|---|---|
| 1 | 不存在通用 Agent | 专注特定场景,不解决通用 |
| 2 | 受控的自由 | Agent=明确边界下的受控智能;无稳定性难上线 |
| 3 | Agent 价值在于智能 | 用不稳定+高成本换泛化;复杂度转移非消失 |
| 4 | 代码 BUG 确定 vs Prompt BUG 随机 | 维护 if-else 痛 vs 维护 ReAct 循环痛,**只是疼法不同** |
| 5 | Workflow+Agent 融合 | Workflow 确定性主干+Agent 不确定性局部——融合非替代 |
| 6 | 翻译 3 类真实需求 | API+RAG(提效)/Workflow+SOP(替代人工)/Agent+受控(决策) |
| 7 | 老板要的不是 Agent | 降本提效、少出错、看起来先进可以吹牛 |
| 8 | 业务分支有限 vs 用户表达无限 | Agent 出现的本质原因 |
| 9 | Agent 本质=生成工作流的工作流 | "将问题编译为可执行计划"的框架 |
| 10 | 5 类已落地 Agent | Coding/客服/法律/医疗/企业流程 |

## 关键金句(5 条)

1. "不存在通用 Agent——当前跑出来的 Agent 不解决通用问题,反而更专注特定场景下的连续性工作。"
2. "Agent 是在有明确边界下的受控智能,也就是让模型在可控范围内处理不确定性。"
3. "代码 BUG 是确定的,Prompt BUG 是随机的。"
4. "大多数老板要的根本不是 Agent,他要的是:降本提效、少出错、看起来先进可以吹牛。"
5. "用 AI 的泛化能力去解决确定流程里的不确定部分。"

## 3 个反直觉

- **Agent 不取代 Workflow**:Workflow 确定性主干+Agent 不确定性局部——**融合非替代**
- **Agent 不降低复杂度**:代码复杂度→数据+Prompt 复杂度——**转移非消失**
- **老板要的不是 Agent**:接到"要 AI"必须先翻译 3 类,不能直接上 Agent

### 6 个对 Seetong 借鉴动作

1. **老板要 Agent ≠ 真要 Agent**:先做"翻译对照"(降本/提效/看起来先进/少出错)
2. **Seetong 三类需求分类**:① 提效已知(API+RAG)② 替代人工(先 SOP)③ 高价值决策(Agent+受控)
3. **不存在通用 Agent——按场景拆**:5 类(设备分诊/反馈分诊/远程操作/添加设备/报警处理)
4. **Workflow 确定性主干 + Agent 局部不确定**:客服分诊 = Workflow+Agent
5. **业务分支有限 vs 用户表达无限**:反馈"七大症状"按"原话分类+意图识别"拆
6. **代码 BUG 确定 vs Prompt BUG 随机**:AI 助手所有 Agent Skill 必须配 Eval Gate

## 关联 + 备注

- **关联**:`[[Leeka-Task-Decomposition-Agentic-Workflow]]` `[[Addy-Osmani-Loop-Engineering]]` `[[0xCodez-Agent-Harness-14-Steps]]` `[[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]` `[[阿里云开发者-淘宝主播Agent的Harness工程实战]]` `[[清华沈阳-自进化AI新物种]]` `[[Multica-AI-Native-组织-人是最慢的节点]]`
- **互补关系**:本文"该不该拆/什么时候选 Agent" + `[[Leeka-Task-Decomposition-Agentic-Workflow]]`"怎么拆" = 完整闭环("选"+"拆"互补)
- **反向参考**:`[[Harness不是目的-知识才是护城河]]`(知识护城河比 Harness 重要);本文"翻译 3 类"也是"业务架构比 Agent 重要"
- **特别发现**:作者用"小龙虾 OpenClaw"做反面案例——本机 OpenClaw 是 gateway 平台,不是单一 Agent 用途
- **透明玻璃自检**:wiki 7.8K(≤8K)/ digest 3.7K(≤4K)/ 节点 10(6-10)/ H2 3 wiki / H2 5 digest(≤5)/ 表格 0 wiki / 表格 1 digest(≤2)/ 0 陈词 ⭐⭐⭐