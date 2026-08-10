---
title: "通用 AI Agent 平台 Harness 技术底座 - Digest"
category: 01-ai-agents
tags: ["#主题/AI-Agent", "#主题/Harness", "#主题/Agent平台", "#主题/Context-Engineering", "#主题/MCP", "#节点/分层记忆", "#节点/安全沙箱"]
nodes: ["分层记忆", "上下文调度", "MCP运行时", "安全沙箱", "全链路追踪"]
links: ["[[2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]]", "[[储旭-从Prompt到Harness-企业级Agent工程的完整演进之路]]", "[[WorkBuddy-Harness工程复盘-从模型到可用Agent]]"]
date: 2026-07-30
source: "微信公众号「人月聊IT」/ 何明璐"
---

# 通用 AI Agent 平台 Harness 技术底座 - Digest

- 原文：https://mp.weixin.qq.com/s/g9gsWggIqMqQtlU4jeBUKA
- 作者：何明璐；文章称基于 Abu-Cowork 源码逆向整理。

## 一句话

Harness 是 Agent 平台的执行底盘：它用状态、能力、控制和证据，让模型从单次回答变成可维护的系统行为。

## 四层速查

| 层面 | 最小能力 |
| --- | --- |
| 状态 | 分层记忆、逐条持久化、Checkpoint、压缩、缓存 |
| 能力 | Skill 生命周期、MCP 运行时、调度、浏览器、Computer Use、多 Agent |
| 控制 | 工作区绑定、权限分级、路径/命令防护、Stop、白黑名单 |
| 证据 | Trace、Token、成本、工具成功率、用户中断与隐私策略 |

## 建设顺序

1. 先做会话持久化、工作区边界、权限与 Trace。
2. 再接 Skills、MCP、外部工具与异步任务。
3. 最后扩大浏览器、桌面操作和多 Agent 的自治范围，并保留审批与中断。

## 关键分层

- 可变记忆按相关性召回并能老化；不可变项目规则随 Git 版本化。
- Skill 封装任务流程；MCP 标准化外部工具、资源和 Prompt；平台统一管理其运行时与权限。
- “能调用”不是“能安全完成”，每个动作都应留下可追溯状态和可恢复边界。

## 关联与边界

- [[储旭-从Prompt到Harness-企业级Agent工程的完整演进之路]]：Agent OS 的演进框架。
- [[WorkBuddy-Harness工程复盘-从模型到可用Agent]]：Context、Memory、Skill、MCP 的产品层解释。
- [[若飞-Agent-记忆与可验证自我改进怎么设计]]：记忆的准入、失效和晋升治理。
- 文章未给出 Abu-Cowork 各能力的逐项源码与测试证据；清单应按具体风险分阶段采纳。
