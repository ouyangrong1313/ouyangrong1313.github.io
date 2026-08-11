---
title: 实战从零开始构建一个Coding Agent：Violin（原文摘要）
slug: 实战从零开始构建一个Coding-Agent-Violin-digest
source: 微信公众号 / 得物技术
url: https://mp.weixin.qq.com/s/yFHRoAi6fe2dduXXlM8Tzw
pub_date: 2026-08-05
fetch_date: 2026-08-06
作者: 酒米
类型: 原文摘要
---

# 实战从零开始构建一个Coding Agent：Violin - Digest

## 一句话总结

coding agent 没有神秘魔法，核心是「问模型 → 执行工具 → 把结果写回上下文 → 再问模型」的 Agent Loop；模型适配、工具注册、会话持久化、上下文压缩、技能加载、插件扩展和客户端协议，都是围绕这个循环补齐可用性、可扩展性与安全边界。

## 核心观点

1. **理解 Coding Agent 的入口**：客服、数据分析和工作流 Agent 都可以看成 coding agent 核心循环在不同场景中的变形。
2. **三层架构降低耦合**：模型适配层把 Provider 差异拍平，agent-core 只管运行时，product 层负责会话、压缩和产品化；EventBus、工具注册表和插件系统横向扩展能力。
3. **Agent Loop 是最小内核**：模型没有工具调用就结束，有工具调用就执行并把结果追加回消息；`max_turns` 是防止无限循环的安全阀。
4. **适配层隔离供应商变化**：OpenAI 与 Anthropic 在请求体、tool call 结构和 SSE 事件格式上都不同，统一接口让上层只处理规范化消息。
5. **工具系统让模型能够行动**：工具描述使用 JSON Schema，注册表负责定义下发、名称查找和执行分派。
6. **记忆不等于把历史全塞进上下文**：Session 用 JSONL + 树结构持久化，compaction 在预算超限时摘要旧消息并保留近期消息。
7. **资源和插件是系统能力层**：AGENTS.md / CLAUDE.md 提供项目规则，SKILL.md 提供可选技能，Lua hook 可以拦截工具、修改上下文和控制生命周期。
8. **跨语言客户端需要稳定协议**：Violin 用 Zig 服务端 + Python TUI，通过 TCP + JSON Lines 传输握手、聊天请求和流式事件。

## 关键架构

| 层/组件 | 解决的问题 | 文中实现 |
|---|---|---|
| Agent Loop | 模型和工具如何反复协作 | while 循环、`max_turns`、重试 |
| Model Adapter | 不同 Provider API 如何统一 | `Model.complete()`、函数指针表、SSE |
| Tool Registry | 模型能调用哪些动作 | Tool + JSON Schema + HashMap |
| Product | 会话、上下文和内存如何产品化 | `agent.zig`、Session、compaction |
| Resources | 规则和技能如何注入 | AGENTS.md、CLAUDE.md、SKILL.md |
| EventBus / Lua | 如何扩展、拦截和观察运行 | agent/session/compaction hooks |
| TCP / JSON Lines | 客户端如何与引擎解耦 | Zig daemon + Python TUI |

## 7 个分析角度

### 1. Agent Loop 是最小可解释内核

Agent 的复杂能力最终收敛为模型调用、工具执行和结果回写三个动作。

- **钩子 1**：把 UI 拆掉之后，coding agent 还剩下什么？
- **钩子 2**：一个 while 循环为什么能撑起复杂 Agent？
- **钩子 3**：Agent 的关键不是会不会回答，而是能不能继续行动。

### 2. 工程价值来自循环之外的补齐

真正难的不是写出第一版 loop，而是处理会话、超长上下文、错误、配置、资源和客户端体验。

- **钩子 1**：为什么 Demo 能跑，产品却总在边界条件上崩？
- **钩子 2**：Agent 的大部分工程量，其实不在那段 while 循环里。
- **钩子 3**：把模型接上工具，只完成了 Agent 的起点。

### 3. Provider 适配是变化隔离层

模型供应商持续变化时，统一 `Model.complete()` 接口可以把请求格式、工具调用和流式协议差异隔离在适配器内部。

- **钩子 1**：OpenAI 和 Anthropic 的 tool call 为什么不能直接互换？
- **钩子 2**：模型越多，上层越需要一个被拍平的接口。
- **钩子 3**：多模型不是多写几个 if，而是建立可替换的适配边界。

### 4. 工具定义是模型行动的契约

工具不仅是函数，还要有名字、描述、参数 Schema 和执行函数；注册表同时承担可发现性和分派职责。

- **钩子 1**：模型不是因为聪明才会调用工具，而是因为看到了工具契约。
- **钩子 2**：没有 JSON Schema，工具调用就没有稳定边界。
- **钩子 3**：工具系统的第一性问题是“模型能看见什么、系统允许做什么”。

### 5. Session 与 compaction 是外部记忆

持久化会话让 Agent 不再每次失忆，压缩机制让长对话在上下文窗口内继续运行；二者共同管理记忆的时间范围与预算。

- **钩子 1**：上下文窗口有限，Agent 的记忆应该如何留下？
- **钩子 2**：把历史全部塞给模型，为什么不等于让它记住？
- **钩子 3**：压缩不是删历史，而是把旧过程重写成可继续工作的摘要。

### 6. Skill 与插件把规则变成运行时能力

规则文件和技能文件通过资源加载注入 system prompt，Lua 插件通过事件 hook 在工具、上下文和生命周期上实现扩展。

- **钩子 1**：Agent 如何知道一个项目的规矩，而不靠每次重新解释？
- **钩子 2**：Skill 是提示词文件，还是可复用的能力模块？
- **钩子 3**：插件真正改变的不是界面，而是 Agent 的行动边界。

### 7. 客户端协议决定系统能否演化

TCP + JSON Lines 让引擎与 UI 解耦，握手、请求和事件流形成稳定边界，Python 只是一个客户端实现而不是系统本体。

- **钩子 1**：为什么把 Agent 引擎和 UI 拆开，反而更容易扩展？
- **钩子 2**：一个稳定协议能不能让不同语言共享同一个 Agent？
- **钩子 3**：当客户端只是协议消费者，Agent 才真正拥有多种入口。

## 关键参数与事实

- 底层引擎使用 Zig，Python 负责 TUI 客户端。
- `product/agent.zig` 约 123 行，负责把 loop、Session 和 compaction 粘合起来。
- Session 使用 JSONL，消息通过 `parent_id` 形成树结构，支持分支和回滚思路。
- compaction 默认阈值 100K token，保留最近 10 条消息，摘要目标约 500 token。
- token 预算用字符数除以 4 近似，不引入 tokenizer。
- 事件 Bus 有 `agent`、`session`、`compaction` 三个回调槽。
- Lua 运行时约 500KB，作为插件语言嵌入 Zig。
- 客户端协议包含 `handshake`、`chat` 和流式事件；文中列出 8 类事件。

## 工程边界与未完成项

1. `buildJson` 中 tools 参数尚未序列化，模型可能收不到工具定义。
2. Lua 插件没有权限隔离，插件理论上可以执行任意能力。
3. ACP 尚未接入，当前客户端只能使用自定义 TCP + JSON Lines 协议。
4. 文中部分架构图、工具清单和实现代码只以图片呈现，未做 OCR 转写。

## 适合继续追踪的主题

- Agent Loop 与 Graph / Harness 的边界。
- Skill 注入和项目规则的优先级治理。
- 工具权限隔离、沙盒与插件安全。
- Session 树结构、compaction 和长期记忆的关系。
- Agent 引擎协议化后如何接入 IDE、CLI 和远程客户端。
