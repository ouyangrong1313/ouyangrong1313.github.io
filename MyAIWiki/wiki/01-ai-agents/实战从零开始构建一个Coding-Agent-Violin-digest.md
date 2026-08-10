---
title: 实战从零开始构建一个Coding Agent：Violin（速查）
category: 01-ai-agents
tags: [#主题/AI-Agent, #主题/AI-Coding, #主题/Agent-Loop, #主题/Agent-架构, #主题/Skill, #主题/插件系统]
nodes: [Agent-Loop, Model-Adapter, Tool-Registry, Session, Context-Compaction, Resources, EventBus, TCP-JSON-Lines]
links: [[实战从零开始构建一个Coding-Agent-Violin]], [[Harness工程AgentLoop]], [[WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[Lilian-Weng-Harness-Engineering-自我改进]]
date: 2026-08-06
source: 微信公众号 / 得物技术
---

# 实战从零开始构建一个Coding Agent：Violin（速查）

> 原文：[[实战从零开始构建一个Coding-Agent-Violin]]；作者酒米；得物技术；发布时间 2026-08-05。

## 一句话总结

Coding Agent 的底层是一个可控循环：问模型、执行工具、把结果回写上下文、继续询问；模型适配、工具、记忆、技能、插件和协议都是围绕这个循环增加工程能力。

## 8 个节点

| 节点 | 速查定义 |
|---|---|
| Agent Loop | 无工具调用则结束，有工具调用则执行并回写结果。 |
| Model Adapter | 用 `Model.complete()` 隔离不同 LLM Provider 的 API 差异。 |
| Tool Registry | 用名称、描述、JSON Schema 和执行函数管理工具。 |
| Session | 用 JSONL 持久化消息，以 `parent_id` 组织会话树。 |
| Context Compaction | 超过 token 预算时摘要旧消息，保留近期上下文。 |
| Resources | 加载 AGENTS.md、CLAUDE.md 和 SKILL.md 注入 system prompt。 |
| EventBus | 通过 agent/session/compaction 回调槽扩展和拦截运行。 |
| TCP JSON Lines | 让 Zig 服务端与 Python TUI 客户端通过协议解耦。 |

## 架构分层

1. **模型适配层**：统一 OpenAI / Anthropic 的请求体、tool call 和 SSE 流。
2. **agent-core**：只负责模型调用、工具判断、执行和错误重试。
3. **product 层**：负责 Session、ContextOverflow、compaction 和内存管理。
4. **横向扩展**：Tool Registry 提供行动能力，Resources 提供规则与技能，EventBus + Lua 提供插件能力。
5. **客户端边界**：Zig daemon 发送握手、聊天和流式事件，Python TUI 只消费协议。

## 关键参数

- Zig 引擎 + Python TUI，TCP + JSON Lines。
- `product/agent.zig` 约 123 行。
- compaction 默认 100K token，保留最近 10 条，摘要目标约 500 token。
- token 估算为字符数 / 4。
- EventBus 有 3 个回调槽：agent、session、compaction。
- 文中列出 8 类事件，覆盖 turn、delta、tool、result、error、ping。

## 生产边界

- tools 参数尚未完整序列化，模型可能收不到工具定义。
- Lua 插件没有权限隔离，不能直接视为安全沙盒。
- ACP 尚未接入，当前使用自定义 TCP + JSON Lines。
- 架构图和工具清单部分只在图片中出现，未做 OCR，不补写图片中的未确认细节。

## 相关链接

- 原文 raw：`../../raw/2026-08-05-得物技术-实战从零开始构建一个Coding-Agent-Violin.md`
- 原文 digest：`../../raw/2026-08-05-得物技术-实战从零开始构建一个Coding-Agent-Violin-digest.md`
- [[Harness工程AgentLoop]] [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] [[Lilian-Weng-Harness-Engineering-自我改进]] [[Hermes-Agent重构得物数仓工作流]]
