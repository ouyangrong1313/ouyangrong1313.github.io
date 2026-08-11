---
title: Agent评测漫谈 —— 由浅入深讲解Agent评测（速查）
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Agent评测
  - 主题/长程Agent
  - 主题/可观测性
  - 主题/评测基础设施
nodes: [Response-Evaluation, Trajectory-Evaluation, Rubric二元化, Good-Bad-Case飞轮, Task评测, Evaluation-Harness, 长程评测基础设施]
links: [[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]], [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]], [[02-ai-coding/用Agent评测思路管理AI-Coding-31万行代码重构实践]], [[02-ai-coding/研发工程化升级-Coding-Agent-AI-Testing与Verification-First]]
date: 2026-08-06
source: 微信公众号「美团技术团队」/ 图灵Agent评测
---

# Agent评测漫谈 —— 由浅入深讲解Agent评测（速查）

> 原文：[[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]]；作者图灵Agent评测；来源「美团技术团队」；发布时间 2026-08-06。

## 一句话总结

Agent 评测从“回答是否正确”升级为“任务是否完成、过程是否可靠、结果是否可解释且可回归”。

## 8 个节点

| 节点 | 一句话 |
|---|---|
| Response Evaluation | 看最终回复、产物和任务结果。 |
| Trajectory Evaluation | 看规划、工具调用和中间状态。 |
| 评测搭桥 | 连接模型能力、任务系统和业务结果。 |
| Rubric 二元化 | 把模糊标准拆成是/否/未知规则。 |
| Good/Bad Case 飞轮 | 让线上样本持续修正评测体系。 |
| Task 评测 | 用输入、成功标准和 Trace 定义测试。 |
| Evaluation Harness | 运行、记录、评分并汇总评测任务。 |
| 长程评测基建 | 回放、Case、沙箱、归因、回归、门禁。 |

## 核心方法

1. **先观测再评测**：没有 Trace 就无法还原现场，无法区分偶然成功和稳定能力。
2. **先搭桥再堆指标**：业务关心 DAU、留存和点击，系统关心召回和点击率，Agent 层要补齐意图、检索和结果整合指标。
3. **人人一致 + 人机一致**：指标下钻、Rubric 二元化，用一致率和 unknown 占比持续校准。
4. **实践科学**：从高频场景和少量指标开始，用 Good Case 定义范式，用 Bad Case 暴露边界。
5. **人机分工**：人负责高价值标准设计和 Rubric 对齐，AI 负责规模化运行、初筛和回归，平台负责沉淀、回放、告警和归因。

## 长程 Agent 评测清单

- **Task**：明确输入和成功标准的单个测试。
- **Trace / Trajectory**：包含输出、工具调用、推理、中间结果和交互的完整记录。
- **Outcome**：环境最终状态，不等同于 Agent 的口头回复。
- **Evaluation Harness**：并发运行任务、记录步骤、评分和汇总结果。
- **基础设施能力**：全链路回放、Case 管理、执行沙箱、AI 评测引擎、报告归因、历史回归、准入准出门禁。

## 关键提醒

- ChatAgent 评测关心“说得好不好”；长程 Agent 评测关心“事情做成没有，以及是怎么做成的”。
- Skill 越容易由 AI 生成，评测越需要简单、标准化、自动化并接入发布流程。
- 评测真正放大的不是机器打分，而是核心评测员已经对齐的判断标准。
- 配图中的流程图、对比表和开源项目表未做 OCR；原文数字按经验案例保留，不作为通用基准。

## 关联

- [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]：评分器、五维指标、用例基线和 Trace。
- [[02-ai-coding/用Agent评测思路管理AI-Coding-31万行代码重构实践]]：评测驱动工程改造。
- [[02-ai-coding/研发工程化升级-Coding-Agent-AI-Testing与Verification-First]]：测试、验证前移和分层信任。
