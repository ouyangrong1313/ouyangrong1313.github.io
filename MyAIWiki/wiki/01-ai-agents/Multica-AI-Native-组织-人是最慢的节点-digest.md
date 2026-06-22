# Multica：人是最慢的节点 - Digest

> 来源：https://mp.weixin.qq.com/s/tIx02ra7Y58xdchsTtzZtw
> 公众号：腾讯研究院
> 发布时间：2026-06-11
> 完整版：[[Multica-AI-Native-组织-人是最慢的节点]]
> 原文：[[../../raw/2026-06-TencentIR-Multica-AI-Native-组织]]

## 一句话总结

**人是组织的瓶颈，不是 Agent。** Multica（4 人 + 几十 Agent）用"去中间层 + 三类角色 + Agent idle 率"三个抓手，给出了 AI Native 组织的一个极端样本。

## 三个核心抓手

### 抓手 1：去中间层，一个人端到端

- **原模式损耗**：大脑中 context → share 给人 → 演绎 → share 给 AI，每一步信息损耗
- **新模式**：一件事由一个人主要 handle，从 PRD 到研发到测试验收，整条链路同一人负责
- **效果**：4 人 + 几十 Agent，同时并行 100+ 任务

### 抓手 2：三类角色，最多两层

| 角色 | 职责 |
|---|---|
| Orchestrator | 任务拆分、分配 |
| Worker | 接到 task 就干活 |
| Validator | 验证执行结果 |

- **层级上限**：**两层**，超过两层是"对人类低效组织的拙劣模仿"
- **同一 Agent 可兼任**：Orchestrator 和 Worker 不必是不同 Agent

### 抓手 3：Agent idle 率

- **定义**：Agent 满载时间 / 24 小时
- **现状**：大部分团队 Agent 满载 2-3h / 24h（idle 20h）
- **意义**：当生产侧变得无限，**决定不去做什么**比决定做什么更重要

## 4 个可复用判断框架

### 框架 1：瓶颈识别
> 产出停滞时，先问：人是瓶颈还是 Agent idle 率高？

### 框架 2：三层决策（O/W/V）
> 任何多 Agent 协作，先问：能否拆成 Orchestrator/Worker/Validator？层级是否超过两层？

### 框架 3：人/Agent 分配
> 任务是人做还是 Agent 做？**对方期待和人沟通吗？** 是 → 人；否 → Agent + 人 review

### 框架 4：思考退化对抗
> 每天 15 分钟 journal / 30 分钟"无 AI 时间"；决策前先自己思考一版再和 AI 讨论

## 一句话金句

- "人是组织的瓶颈，不是 Agent。"
- "建太多层级是对人类低效组织的一个拙劣模仿。"
- "供给侧生产侧变得无限之后，决定不去做什么事情更重要。"
- "快速做错误决策 > 缓慢做正确决策。"
- "只要活得足够久，就是壁垒。"
- "AI 给你吐出来的是 P50（中位数）。"

## 关键事实卡

- **4 人 + 几十 Agent**，平台一周 3000 亿 token
- **张佳圆日均 2-3 亿 token**（coding 多时 10 亿）
- **同时并行 100+ 任务**，已完成 1000+ 任务
- **三类典型 Agent 岗位**：coding / 数据分析 / 部署运维 / GTM
- **招人标准**：high agency > 背景 / 经验
- **代码不是壁垒**，网络效应（用的人越多越好用）才是

## 关联阅读

- [[Claude-Code一周年回顾-Boris-Cat]] — "不再 review 代码"同源
- [[AI-PM核心技能-观测评估与反馈闭环]] — AI 时代稀缺的是判断力
- [[OpenClaw-vs-Hermes-多-Agent-架构设计]] — 多 Agent 架构的另一条主线
- [[从零设计生产级-Multi-Agent-Harness]] — 多 Agent Harness 工程化
- [[make-for-agent-qi-shi-huan-shi-make-for-human]] — Agent 协作层的产品设计
- [[54万行代码的顿悟]] — 未来瓶颈 = 需求定义 + 架构设计
- [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]] — 同一 AI Native 组织主题的另一视角
- [[AI-Coding的顿悟时刻]] — 工程师个人范式

## 标签

#主题/AI-Native #主题/AI-Agent #主题/多Agent协作 #主题/组织变革 #主题/人机协作 #主题/认知衰减 #公司/Multica #场景/Agent平台 #场景/小团队
