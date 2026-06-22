---
title: "Multica：人是最慢的节点，4 人 + 几十个 Agent 的 AI Native 组织长什么样"
category: 01-ai-agents
tags: [#主题/AI-Native, #主题/AI-Agent, #主题/多Agent协作, #主题/组织变革, #主题/人机协作, #主题/认知衰减, #公司/Multica, #场景/Agent平台, #场景/小团队]
nodes: [Agent协作层, 三类角色, 最多两层, 去中间层, 端到端负责, AgentIdle率, 人是瓶颈, 信任未建立, 思考退化, 网络效应壁垒]
links: [[Claude-Code一周年回顾-Boris-Cat]], [[AI-PM核心技能-观测评估与反馈闭环]], [[OpenClaw-vs-Hermes-多-Agent-架构设计]], [[从零设计生产级-Multi-Agent-Harness]], [[make-for-agent-qi-shi-huan-shi-make-for-human]], [[54万行代码的顿悟]], [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]], [[AI-Coding的顿悟时刻]]
date: 2026-06-11
source: 微信公众号 / 腾讯研究院
---

# Multica：人是最慢的节点，4 人 + 几十个 Agent 的 AI Native 组织长什么样

> **核心命题**：AI Native 组织的产出效率瓶颈已经**不是** AI 或 Agent，而是**人**。Multica（4 人 + 几十 Agent 的开源 Agent 协作平台）通过"去中间层 + 三类角色 + Agent idle 率"三个抓手给出了一个极端样本。
>
> 本文是腾讯研究院"AI 跃迁者调研"第四期对张佳圆（Multica 创始人，前 TikTok 工程师）的访谈整理。

## 关联图谱

### 上游（基于 / 来自）
- [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]]：YC 视角的 Agent 能力开放与 Egalitarian 思想
- [[AI-PM核心技能-观测评估与反馈闭环]]：AI 时代稀缺的不是产能而是判断力（上游共识）
- [[Claude-Code一周年回顾-Boris-Cat]]：Boris + Cat 一周年回顾里"不再 review 代码 / Agent 自主验证"同源
- [[54万行代码的顿悟]]：未来瓶颈在需求定义和架构设计

### 下游（应用于 / 验证于）
- [[OpenClaw-vs-Hermes-多-Agent-架构设计]]：用 Multica 案例验证多 Agent 架构的"角色边界 + 层级最小化"路径
- [[从零设计生产级-Multi-Agent-Harness]]：为多 Agent Harness 的"角色定义 / 信任建立 / idle 率监控"提供实战输入
- [[make-for-agent-qi-shi-huan-shi-make-for-human|Make for Agent]]：Multica 是"Make for Agent"理念的协作层落地

### 同级（横向 / 并列）
- [[AI-Coding的顿悟时刻]]：工程师个人范式 vs 团队流程（个人 ↔ 组织的同一主题）
- [[如何更科学、方向可控的实现 Skill 的「自进化」？|Skill-Self-Evolution]]：单 Agent Skill 进化（聚焦 Agent 本身能力）vs Multica 聚焦多 Agent 协作层

## 核心论点

### 1. Multica 是什么：Agent 的协作层（不是 Agent 本身）

- **定位**：模型/平台中立（Claude Code/Codex/Manus 都能跑），处于"Agent 与人之间"的中间层
- **三个核心概念**：
  - **Runtime（运行时）**：Agent 运行的机器（本地 MacBook / Mac Mini / 服务器），统一注册到 workspace
  - **Agent（智能体）**：相当于 AI 员工，可分配任务、设置角色
  - **Agent Team（小队）**：多个 Agent 组成的小队，有自己的工作流程
- **日常模式**：创建任务 → 分配给 Agent/Agent Team → 人做最终 review → Agent 需要介入时出现在 inbox

### 2. 人的角色：人是组织瓶颈，Agent 不是

> "整个组织的产出效率瓶颈，其实现在已经是人了，而非 AI 或者 Agent。"

- **瓶颈对比**：
  - Agent：智能已足够强，token 给够可并行 10 / 100+ 任务
  - 人：注意力带宽有限，并行 3-5 件事已到极限
- **人的剩余价值**：用户运营、用户访谈（对方期待和人沟通）+ 上层目标制定 + 结果 review
- **招人标准**："high agency"（自主主观能动性）> 背景/专业/经验

### 3. 组织架构：去中间层，一个人端到端

- **变革核心**：去掉"人 → 传递人 → AI"中间层
- **原模式损耗**：大脑中 context → share 给人 → 演绎 → share 给 AI，每一步都有信息损耗
- **新模式**：**一件事由一个人主要 handle，从 PRD 到研发到测试验收，整条链路同一人负责**
- **效果**：4 人 + 几十 Agent，平台一周 3000 亿 token，同时并行 100+ 任务

### 4. Agent 设计：三类角色，最多两层

| 角色 | 职责 | 备注 |
|---|---|---|
| **Orchestrator（协调者）** | 高层次任务拆分和分配 | 类似项目经理 |
| **Worker（执行者）** | 接到 task 就开始干活 | 可泛化，既做 orchestrator 又做 worker |
| **Validator（验证者）** | 对执行结果做验证 | 避免"既做裁判又做运动员" |

- **层级建议**：**最多两层**
- **理由**："人需要多层级本质是做信息聚合，因为带宽有限没法同时管 1000 人。Agent 没这个限制，建太多层级是对人类低效组织的一个拙劣模仿。"

### 5. 核心指标：Agent idle 率

> "判断一个组织 AI Native 的程度够不够彻底，就看 Agent 的产出占工作时间的比例。"

- **现状**：大部分人 Agent 每天满载 2-3 小时，闲置 20 小时
- **目标**：让 Agent 满载时间尽量接近 24 小时
- **意义**：当生产侧变得无限，决定**不去做什么**比决定做什么更重要

### 6. 代价与未解张力

- **信任问题未解决**：1000+ 已完成任务，还有很多等 review；现在主要靠"AI 做完我看一遍"维持底线
- **思考退化**：使用 AI 越多，思考过程越少；可能未来几年思维模式会改变
- **张佳圆的对抗方式**：每天刻意写 journal；决策前先自己思考一版再和 AI 讨论
- **余一的对抗方式**：每天强制 30 分钟"忍受慢和无聊"听播客，训练专注度

## 关键事实卡

### Multica 团队构成

| 维度 | 数据 |
|---|---|
| 人数 | 4 人 |
| Agent 数 | 几十个，常用 10+ |
| Token 消耗 | 平台一周 ~3000 亿 token；张佳圆个人日均 2-3 亿（coding 多时 10 亿）|
| 工作模式 | 线下办公 + 周一 planning + 每天 6 点 demo 站会 |
| 任务并发 | 同时 100+ 任务；已完成 1000+ 任务 |
| GitHub Star | 访谈时 27,500；一周涨 12,000 |

### 典型 Agent 岗位

- 每人本地 coding agent
- 团队公共 24h coding agent（部署 Mac Mini）
- 数据分析师 Agent（接 PostHog，比传统数据分析师更强）
- 部署运维 Agent
- Go-to-market Agent（分析热点 / 联系 KOL）
- 写 deck（PPT）的 Agent
- **淘汰制**：一键淘汰不再需要的 Agent

## 与其他 AI Native 主张的差异

| 主张方 | 核心观点 | 与 Multica 的差异 |
|---|---|---|
| **YC Garry Tan** | 350+ 工具注册表 + Dream Cycle + Egalitarian + Trust by default | 思路一致（AI Native 组织），但 Multica 更激进：4 人 + 几十 Agent，**真正去掉了中间人** |
| **Claude Code 团队 Fiona Fung** | JIT 规划 + 自动化肌肉记忆 + Taste is scarce | 互补——Fiona 强调"人和 AI 协作的具体技巧"，Multica 强调"组织层的人和 Agent 协作" |
| **Boris Cherny 28 分钟** | Prompt 升级为 Loop / Harness | Multica 是 Loop 哲学的**组织层落地**（多 Agent Loop 而非单 Agent）|
| **Matt Van Horn 22 Hacks** | Agentic Engineering 实操 | Multica 是 22 Hacks 的**极端样本**（22 Hacks 偏"个人 + 工具"，Multica 偏"组织 + 协作层"）|

## 可直接复用的判断框架

### 框架 1：瓶颈识别

> 当你团队产出停滞时，先问——**是人不够多 / 人不够强，还是 Agent idle 率太高？**

- 答案 A（人不够强）→ 招 high agency 的人，让 AI 当杠杆
- 答案 B（Agent idle 率高）→ 给 Agent 派更多任务，让人从低价值 review 中解放
- 大多数 AI 团队现状是 **B**：Agent 满载 2-3h / 24h

### 框架 2：三层决策（Orchestrator/Worker/Validator）

> 任何多 Agent 协作问题，先问——**任务能不能拆成 O/W/V 三类？层级是否超过两层？**

- 是 → 用三类角色 + 最多两层建模
- 否 → 大概率是过度设计，回到单 Agent 或纯工作流

### 框架 3：人/Agent 分配

> 任务是人做还是 Agent 做？标准是——**对方期待和人沟通吗？**

- 是（用户运营 / 访谈 / 关键决策沟通）→ 人做
- 否（数据查询 / 代码 review / 文档生成 / 部署运维）→ Agent 做 + 人 review

### 框架 4：思考退化对抗

> 今天我自己想清楚了一件事吗（不借助 AI）？

- 每天 15 分钟 journal 或 30 分钟"无 AI 时间"
- 决策前先自己思考一版，再和 AI 讨论（不让 AI 取代你的判断）

## 待补证 / 局限

- **1000+ 任务完成质量**：未披露"review 通过率"和"rework 率"，无法判断 Agent 实际产出质量
- **trust 阈值未量化**："100% 信任还需要建立"是定性描述，无具体信任曲线
- **小团队适用性**：4 人 + 几十 Agent 的模式**未必能直接扩展到 20 / 50 / 200 人规模**——50 人以上的协调成本可能需要新的组织设计
- **单点风险**：4 人团队对单一个体的依赖度极高，创始人一旦离岗组织稳定性存疑

## 标签与分类

- 主题：AI-Native / AI-Agent / 多 Agent 协作 / 组织变革 / 人机协作 / 认知衰减
- 手法：范式反思 / 经济反转 / 极端样本
- 场景：Agent 平台 / 小团队 / 开源 + 商业化
- 公司：Multica / 腾讯研究院

---

*完整访谈快问快答与产品演示细节见 [[../../raw/2026-06-TencentIR-Multica-AI-Native-组织]] 原文。*
*速读摘要见 [[Multica-AI-Native-组织-人是最慢的节点-digest]]。*
