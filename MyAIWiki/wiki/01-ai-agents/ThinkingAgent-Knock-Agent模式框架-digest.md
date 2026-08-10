---
title: Agent 模式框架 (Digest)
category: 01-ai-agents
date: 2026-07-17
source: 微信公众号「ThinkingAgent」/ Knock
---

# Agent 模式框架 (Digest)

## 一句话 + 8 节点速查表

> Agent 的本质不是聊天，而是行动；把智能稳定、可控、可评估地嵌入企业运行——吴恩达 4 模式 + Anthropic Workflow vs Agent 区分 + 三层路径（个人助手 → 流程嵌入 → 企业智能）。

| 节点 | 一句话定义 | 关键洞察 |
|------|------------|----------|
| 4 类型分级 | Chatbot / Copilot / Agent / Multi-Agent | Agent 核心是"完成任务"不是"回答问题" |
| Reflection | 自我修改：生成→检查→修改 | 不能单独用，必须配测试/工具/评估 |
| Tool Use | 大模型是脑，工具是手 | 是能力入口，也是治理起点 |
| Planning | 先想后做：目标→拆解→步骤→执行 | 适合多步骤复杂任务 |
| Multi-Agent | 分工协作：研究员+分析师+写作者+评审员 | 通信成本高，简单任务别用 |
| Workflow vs Agent | Workflow 人定义流程，Agent LLM 决定 | Anthropic 5 种 Workflow 模式 |
| 三层路径 | 个人助手→流程嵌入→企业智能 | 常见错误：一上来就做企业智能 |
| 5 大误区 | 一步到位/过度自主/盲目多 Agent/无评估/无权限 | 7 项评估指标：完成率/准确率/正确率/成本/延迟/反馈/业务结果 |

## 6 个对 Seetong 借鉴动作

1. **4 类型分级盘点**：Seetong AI 助手所有 Skill 按 4 类重新分类
2. **Reflection 配 Reviewer 子 Skill**：写代码 Skill 必配 Reviewer 子 Skill 循环 2-3 轮（对应 [[Loop-Engineering-验证才是瓶颈]] 验证闸门）
3. **Tool Use 治理 8 项**：权限/白名单/日志/审计/沙箱/确认/回滚/分级
4. **Planning 入 Skill 模板**：多步骤任务类 Skill 必走 Planning——目标→拆解→执行→检查→调整
5. **单 Agent 优先**：1-2 个"5 步能解决"复杂任务做成单 Agent + Workflow，验证后再考虑 Multi-Agent
6. **三层路径定位**：当前在第 1 层（个人助手），6-12 个月推到第 2 层（流程嵌入），第 3 层暂不急

## 5 金句 + 3 反直觉 + 4 类型对比

**金句**："Agent 不是多说几句话，而是能接入真实系统，完成真实任务" / "大模型是脑，工具是手" / "Tool Use 是能力入口，也是治理起点" / "多 Agent 不是越多越好" / "企业不是拥有很多 Agent，而是拥有一套可学习、可执行、可优化、可治理的智能系统"。

**反直觉**：① Agent 越强越要从半自主开始 ② 简单任务用单 Agent ③ Reflection 不能单独用。

| 类型 | 典型能力 | 核心特征 | 适合场景 |
|------|----------|----------|----------|
| Chatbot | 问答、总结、生成文本 | 被动响应 | FAQ / 简单问答 |
| Copilot | 辅助写作、辅助编码、辅助分析 | 人主导 AI 辅助 | 写作 / 编程辅助 |
| Agent | 规划、调用工具、执行任务、自我检查 | 目标驱动 | 流程化任务执行 |
| Multi-Agent | 多角色分工、协同、评审、编排 | 团队协作 | 复杂任务 / 跨域任务 |

## 关联 + 备注

- **同主线** [[ThinkingAgent-Knock-AI-Native组织5级成熟度模型]]（**同作者 2 周内连发**——5 级组织维度 + 本文 5 误区 Agent 实施维度 = "AI Native 完整工程化框架"）[[Leeka-Task-Decomposition-Agentic-Workflow]] [[0xCodez-Agent-Harness-14-Steps]] [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]
- **强关联** [[Capihom-AI-Native企业-Agent团队和AI-Factory重写公司体系]]（Groupon 实证印证 5 误区第 4 条）[[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]]
- **作者** Knock = 微信公众号「ThinkingAgent」主理人　**来源** 2026-07-16 08:27 推送，约 8300 字
- **Seetong 优先级** Tool Use → Reflection → Planning → Multi-Agent　**关键区分** 现有 90% Skill 应是 Workflow 不是 Agent，避免"什么都是 Agent"陷阱