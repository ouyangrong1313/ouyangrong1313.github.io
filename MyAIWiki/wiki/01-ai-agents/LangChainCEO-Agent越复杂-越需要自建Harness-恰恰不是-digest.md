---
title: LangChain CEO：Agent 越复杂，越需要自建 Harness？恰恰不是 - 速读
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Harness工程
  - 主题/可观测性
  - 场景/公众号长文
nodes: [任务分布, Context诊断, 执行轨迹, Benchmark闭环, 受控自主]
links: [[01-ai-agents/LangChainCEO-Agent越复杂-越需要自建Harness-恰恰不是]], [[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]]
date: 2026-08-22
source: 微信公众号「DataFun」整理 Harrison Chase（LangChain CEO）公开演讲
---

# LangChain CEO：Agent 越复杂，越需要自建 Harness？恰恰不是 - 速读

> 先问任务离模型熟悉的工作分布有多远，再决定 Harness 要定制到什么程度；出错时先看模型实际收到了什么 Context。

## 决策表

| 情况 | 优先动作 |
|---|---|
| 任务接近通用能力 | 复用通用 Harness，最小化增量 |
| 垂直规则或流程偏移 | 只定制业务 Context、Gate、Check 与状态 |
| 最终答案异常 | 回放 Context、工具结果、摘要与错误传播 |
| 多种改法可选 | 同任务集比较效果、时延、Token 与成本 |
| 高风险自主执行 | 加权限、审计、人工确认和可回滚边界 |

## 关键提醒

- Model、Context、Harness 是独立但耦合的诊断面；换模型不等于解决系统问题。
- Trace 是定位根因的前提，只记录最终回复无法判断问题发生在哪一步。
- Harness 不是一次性脚手架，应在真实任务、Benchmark 和反馈中持续迭代。

## 关联

- [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]：系统分层实践。
- [[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]]：Trace 与任务评测基础设施。
- [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]]：Harness 六元组工程实现。

证据边界：案例与产品细节来自 DataFun 二手演讲整理，未独立复现。
