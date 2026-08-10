---
title: 实战从零开始构建一个Coding Agent：Violin
category: 01-ai-agents
tags: [#主题/AI-Agent, #主题/AI-Coding, #主题/Agent-Loop, #主题/Agent-架构, #主题/Skill, #主题/插件系统, #场景/公众号长文]
nodes: [Agent-Loop, 模型适配层, Tool-System, Session树, Context-Compaction, Resources注入, EventBus插件, TCP-JSON-Lines, Zig-Python分层, Agent安全边界]
links: [[Harness工程AgentLoop]], [[WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]], [[Lilian-Weng-Harness-Engineering-自我改进]], [[若飞-Agent-记忆与可验证自我改进怎么设计]], [[Hermes-Agent重构得物数仓工作流]]
date: 2026-08-06
source: 微信公众号 / 得物技术
source_wechat: https://mp.weixin.qq.com/s/yFHRoAi6fe2dduXXlM8Tzw
---

# 实战从零开始构建一个Coding Agent：Violin

- 原文链接：https://mp.weixin.qq.com/s/yFHRoAi6fe2dduXXlM8Tzw
- 来源：微信公众号「得物技术」
- 作者：酒米
- 发布时间：2026-08-05 18:30（页面时间戳）
- 获取时间：2026-08-06

## 核心结论（一句话）

> **Coding Agent 的最小内核是一个可控的 Agent Loop：问模型、执行工具、把结果写回上下文、继续询问，直到完成或触发边界。** 模型适配、工具注册、Session、compaction、Skill 注入、插件和客户端协议，都是围绕这个循环补齐可用性、可扩展性和安全边界。

## 分类提炼

- 场景：Coding Agent 学习、Agent Runtime 设计、个人 Agent 工程实践
- 标签：#主题/AI-Agent #主题/AI-Coding #主题/Agent-Loop #主题/Agent-架构 #主题/Skill #主题/插件系统
- 类型：源码/架构拆解 + toy project 实战 + 协议设计
- 项目：Violin；Zig 服务端 / Python TUI 客户端；TCP + JSON Lines
- 证据等级：作者项目实践与设计说明；不是成熟商用系统的性能或安全验证报告

## 知识节点（10 个独立概念）

- **Agent Loop**：模型无工具调用就结束，有工具调用就执行并把结果追加回消息，再进入下一轮。
- **三层 Agent 架构**：模型适配层拍平供应商差异，agent-core 只管运行时，product 层承接会话和产品化逻辑。
- **Model Adapter**：通过统一的 `Model.complete()` 隔离 OpenAI、Anthropic 等 Provider 的请求、tool call 和流式协议差异。
- **Tool Registry**：用名称、描述、JSON Schema 参数和执行函数定义工具，并通过注册表完成发现、下发和分派。
- **Session 树**：用 JSONL 持久化会话，以 `parent_id` 组织消息树，支持恢复、分支和回滚。
- **Context Compaction**：上下文超过预算时，把旧消息摘要化，保留近期消息，使 Agent 能在有限窗口内继续工作。
- **Resources 注入**：从 AGENTS.md、CLAUDE.md 和 SKILL.md 加载项目规则与技能，并格式化成 system prompt。
- **EventBus 插件**：通过 `agent`、`session`、`compaction` 回调槽，把观察、拦截、修改和阻止能力交给 Lua 插件。
- **TCP JSON Lines**：用握手、聊天请求和流式事件定义引擎与客户端边界，让 Zig 服务端和 Python TUI 解耦。
- **Toy Agent 边界**：工具参数尚未完整序列化、插件没有权限隔离、ACP 未接入，说明“能跑通”不等于生产可靠。

## 关联图谱

### 上游（基于 / 来自）

- **Pi / how-pi-agent-works**：Violin 借鉴三层分离、EventBus、工具注册表、插件系统和 JSONL Session 的设计思路。
- [[Harness工程AgentLoop]]：提供 Agent Loop 与 Harness 工程的概念背景，本文将其落到 Zig toy project 的模块边界。
- [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]]：同一 Agent Loop 主题的工程问题清单，补充本文未展开的治理与边界问题。

### 下游（应用于 / 验证于）

- [[WorkBuddy-Harness工程复盘-从模型到可用Agent]]：把模型、上下文、工具、记忆、Harness 和 Loop 组合成更接近生产的 Agent 系统。
- [[Lilian-Weng-Harness-Engineering-自我改进]]：将工具、状态、反馈和自我改进放进可持续运行的 Harness。
- [[Hermes-Agent重构得物数仓工作流]]：把同一类 Agent 构件用于真实数仓流程，增加工作区、状态机、预演和人工确认门。

### 同级（横向 / 并列）

- [[若飞-Agent-记忆与可验证自我改进怎么设计]]：从记忆准入、验证和自我改进角度补充 Session/compaction。
- [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]：从业务 Agent 的分层与流程编排角度对照 Violin 的运行时分层。
- [[Loop-Engineering-验证才是瓶颈]]：补充“循环能够运行”之后，如何通过反馈与验证把 Agent 推向可靠交付。

## 正文要点

1. **Agent Loop 是所有上层能力的汇聚点**：最简形式是 `while (turn < max_turns)`，调用模型、检查 tool call、执行工具、把结果回写消息；`max_turns` 防止无限循环，错误分类决定重试策略。
2. **三层边界控制变化传播**：模型适配层不让 Provider 差异污染 loop；agent-core 不管理持久化；product/agent.zig 把历史加载、ContextOverflow 重试和新消息保存接起来。
3. **模型的“能力”必须转成契约**：Tool 不只是函数，还要给出可供模型理解的名称、描述和 JSON Schema；注册表负责工具可见性与执行分派。
4. **上下文治理是长期运行的前提**：Session 用 JSONL 保留可恢复历史，compaction 用字符数/4 估算 token，在默认 100K 预算下保留最近 10 条消息并生成约 500 token 摘要。
5. **规则和 Skill 是外部记忆与行为约束**：Resources 按项目优先、全局兜底的路径加载 AGENTS.md / CLAUDE.md / SKILL.md，将可复用规范注入每次模型调用。
6. **插件系统把事件变成控制面**：Lua 可以在工具开始前阻止危险命令、修改参数，在工具结束后修改结果，在上下文阶段注入规则，也可以拦截 Agent 启动或会话压缩。
7. **协议化让 Agent 入口可替换**：Zig daemon 不绑定 Python UI，TCP + JSON Lines 通过 `handshake`、`chat`、`turn_start`、`delta`、`tool_start`、`tool_end`、`turn_end`、`result` 等消息承载运行状态。
8. **作者主动标出生产缺口**：tools 参数未序列化会导致模型收不到工具定义；Lua 没有权限隔离；ACP 尚未接入。toy project 的价值是验证架构假设，而不是宣称已经生产就绪。

### 对 Seetong / Agent 工程的借鉴

- 把 Agent 实现拆成“模型适配 / Loop / 工具注册 / Product / 资源 / 事件 / 协议”七个可审计边界，先定义每层输入输出再扩展功能。
- 将 AGENTS.md、SKILL.md、Session 和 compaction 看成不同生命周期的外部记忆：规则常驻、技能按需、会话可恢复、摘要受预算约束。
- 任何带写权限的工具都应有 JSON Schema、参数校验、执行前拦截、执行后结果和审计记录；不能把 Lua hook 直接当作安全边界。
- 用事件流把模型增量、工具开始/结束、错误和最终结果暴露给 UI、日志和评测系统，才能验证 Agent 是否真的推进了任务。

### 相关链接

- 原文 raw：`../../raw/2026-08-05-得物技术-实战从零开始构建一个Coding-Agent-Violin.md`
- 原文 digest：`../../raw/2026-08-05-得物技术-实战从零开始构建一个Coding-Agent-Violin-digest.md`
- 同主题：[[Harness工程AgentLoop]] [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] [[Lilian-Weng-Harness-Engineering-自我改进]]

> 透明玻璃自检：wiki 10 节点；digest 8 个核心观点 + 7 个分析角度、21 个钩子；原文图片资源已保留，图片文字未 OCR；文章中的工具清单只确认“6 个基本工具”，未凭空补写名称。
