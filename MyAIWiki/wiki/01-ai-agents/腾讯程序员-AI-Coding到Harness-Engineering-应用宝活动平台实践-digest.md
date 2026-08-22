---
title: 从 AI Coding 到 Harness Engineering 应用宝活动平台端到端实践(速读摘要)
category: 01-ai-agents
tags:
  - 主题/Harness
  - 主题/AI-Agent
  - 主题/知识库
  - 主题/端到端开发
  - 主题/多Agent
  - 主题/工程实践
  - 主题/腾讯
  - 场景/活动平台
type: digest
date: 2026-07-05
source: 微信公众号 / 腾讯程序员 2026-07-05(腾讯应用宝活动平台团队 / zimingxing、kinglongli、yifhao)
原始链接: https://mp.weixin.qq.com/s/UE-RZH9hnbBd06CVapFGrA
nodes: []
---

# 从 AI Coding 到 Harness Engineering 应用宝活动平台端到端实践(速读摘要)

> **一句话**:**Harness = 知识库底座 + 状态文件驱动 + 12 专家 Agent + DAG 并行 + 脚本化执行 + DevOps 集成**——不是给 AI Coding 加规则,而是把对话窗口升级为工程系统。

## 速查表

| 维度 | 核心命题 | 关键数字/设计 |
|---|---|---|
| 整体架构 | 知识库工程 ✖️ 端到端开发工程 | 800+ 文档 / 90+ 微服务 / 12 Agent / 30+ Skill / 10+ 脚本 |
| 知识库结构 | 3 层(总览/域/服务)+ 2 类(自动/手工)+ 8 类自动文档 | meta.yaml 注册 + git_hash 检测 |
| 知识加载 | 渐进式 3 层(关键词→grep→按模式)+ 4 查询模式(PRD/方案/接口/问答) | 替代 RAG 的 4 个优势 |
| 文档保鲜 | git_hash 增量模式 + log.md 不可覆盖 + 人工批注保留 | "过期知识比没知识危险" |
| 状态文件 | 2 类 JSON(product-state / e2e-state)+ 3 个 hook(Stop/SessionStart/SessionEnd) | 流程可中断/可恢复/可观测 |
| 专家 Agent | 5 项原则(单一职责/上下文隔离/工具最小权限/确定性输入输出/模型可插拔) | 沉淀 12 个专家 |
| 并行编排 | Worktree 隔离(同需求多任务) + Fork-Join(多 Story) | DAG 拓扑分层 + worktree merge |
| 冲突治理 | 4 类(Merge/Shared file/Proto/DB&配置)+ 核心思路"事前隔离 + 串行收口" | 4 种策略 |
| 脚本化 | 15 个脚本(e2e-dev.py / worktree.sh / build-and-publish.sh / kb-init.sh) | "AI 负责认知,脚本负责执行" |
| DevOps 集成 | TAPD/Rick/123/七彩石/伽利略 MCP + Skill | tRPC-Gateway + Codar CR |
| 调度架构 | 弃主子 Agent / 弃 Shell 改 Go / 禁项目 Memory | 强类型控制流 |
| 核心原则 | 7 条(认知归 AI/长链路状态化/知识结构化/Agent 隔离/执行脚本化/Workflow > Prompt/工程系统思维) | 沉淀式抽象 |
| Vibe Coding 边界 | 看板类(结果导向+容错高)黑盒化;核心在线业务仍需人守架构 | With 平台 100% AI 看板案例 |

**3 个反直觉点**:① **不是"加规则"而是"分层独立演化"**(知识自动生成 + 人工沉淀互不替代)② **不是"AI 越强越可靠"而是"AI 越强越要流程约束"**(整套 Harness 设计都假设模型是概率的、会漂移的)③ **不是"Workflow 越复杂越好"而是"确定性归脚本,认知归 AI"**(AI 写 Shell 脚本常潜藏语法错误,长链路末端才暴露)。

## 5 个对 Seetong 团队可借鉴动作

1. **状态文件先于多 Agent**:把 Seetong AI 助手每个长流程(版本回顾 / 简报生成 / Bug 修复)的状态写 JSON 盘——当前 Phase / 已完成步骤 / 下一步动作。会话中断能续上是关键,优先 MVP,不要等数据库。
2. **知识库按"3 层加载 + 4 查询模式"重构**:MyAIWiki 已经是结构化,但 Seetong AI 助手用的项目级知识库(seetong-iOS / seetong-android / Seetong-cli)还要按"3 层加载"重构——meta.yaml 注册 + 关键词缩域 + grep 精确筛选 + 按模式按需加载,避免一次塞全文。
3. **冲突治理入版本流程**:Seetong 多版本分支(8.3.x / 8.4.x)合并时按"4 类冲突"映射——Merge Conflict / Shared file(Info.plist)/ Proto 协议 / DB&配置,各对应一个收口负责人或脚本。
4. **沉淀 15 个流程脚本 + 调度架构转 Go 强类型**:Git worktree 操作 / TAPD 工时填写 / 反馈分诊 SOP / 简报模板渲染等重复操作改为 shell 或 Python 脚本;主调度器如果未来要做,优先 Go 而非 Shell(大模型生成的 Shell 脚本常潜藏隐性错误)。
5. **Vibe Coding 边界体检**:Seetong 后台运营看板 / 内部工具 / Demo 类需求,可放开让 AI 100% 生成不 CR;4G IPC / 4G 远程开门 / 支付 / 安全 / 数据删除等路径,严守 review + 测试 + 灰度——分清"结果导向+容错高"与"核心在线业务"两类系统的不同治理策略。

## 关联 + 备注

**关联**:Harness 主线 [[01-ai-agents/Harness工程AgentLoop]] / [[01-ai-agents/HarnessEngineering企业级实战]] / [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]] / [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] / [[01-ai-agents/harness-engineering]] | 端到端 [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]] / [[01-ai-agents/Hermes-Agent重构得物数仓工作流]] | Loop [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] / [[02-ai-coding/Addy-Osmani-Loop-Engineering]] | 任务拆解 [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]] | AI Coding 范式 [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]] / [[02-ai-coding/字节跳动洪定坤-AI-Coding的实践与探索]] | 多 Agent [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]] / [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]]

**备注**:作者 zimingxing / kinglongli / yifhao 腾讯应用宝活动平台团队 | 仅覆盖 Go 后台业务 | 整套体系重度依赖 codebuddy cli | 团队自评"刚起步能跑,缺自进化/评估/工具解耦" | 7 条核心原则是沉淀式非实证 | 文末附 Mac 应用宝推广与正文无关