---
title: 一文搞懂 YC-QM：面向企业的多人智能体平台（multiplayer agent harness）
category: 01-ai-agents
tags:
  - 主题/Multiplayer-Agent
  - 主题/Scope隔离
  - 主题/Harness适配器
  - 主题/持久电脑
  - 主题/Durable-by-default
  - 主题/安全Posture
  - 主题/工程文化
  - 主题/Seetong借鉴
  - 作者/AllenTang
  - 项目/QM
nodes: [Scope隔离7项资源, 持久电脑Durable-Computer, 4个Harness适配器, Durable-by-default, 智能体等于你本人, 3种安全Posture, 收文字不收代码, 多租户底座定位]
links: [[01-ai-agents/万字长文拆解Agent-架构设计-四-多-Agent-协作]], [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[01-ai-agents/HarnessEngineering企业级实战]], [[01-ai-agents/Harness工程AgentLoop]], [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]], [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[01-ai-agents/agent-architecture]], [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]], [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]], [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]], [[01-ai-agents/cases/liangbo-execution-agent]], [[01-ai-agents/OpenClaw-vs-Hermes-多-Agent-架构设计]], [[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]], [[06-ai-tech/企业知识库认知底座]], [[06-ai-tech/Agent Harness 与 OpenClaw：从工具到系统的中文解读]], [[01-ai-agents/未来属于垂直领域Agent]], [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]], [[01-ai-agents/Agent时代架构师系统能力]], [[02-ai-coding/phodal-项目记住-Coding-Agent-5步法]]
date: 2026-08-03
source: 微信公众号「架构师带你玩转AI」AllenTang 编译（原文 https://mp.weixin.qq.com/s/O8O6ttb-z9KmwjG4C9fe-Q）
---

# 一文搞懂 YC-QM：面向企业的多人智能体平台

- 原文：https://mp.weixin.qq.com/s/O8O6ttb-z9KmwjG4C9fe-Q
- 一手仓库：https://github.com/yc-software/qm（MIT 协议 / YC 开源）
- 作者：AllenTang（与 7/22 [[01-ai-agents/万字长文拆解Agent-架构设计-四-多-Agent-协作]] 同公众号同编辑）
- 发布时间：推断 2026-07 末至 2026-08 / 获取时间：2026-08-03 14:41 Asia/Shanghai / 原文约 3424 字

## 核心结论与分类

> QM 是 YC 开源的多人智能体协作平台——从"个人助理"到"多人协作"靠 scope 隔离；6 大特性：无头核心 + 持久电脑 + 4 个 Harness 适配器 + Durable by default + 智能体=你本人 + 3 种安全 posture + 5 条工程文化铁律。

- 场景：企业级 Agent 平台 / 多人协作 / 多租户 / 安全治理 / 类型：开源项目深度解读 + 工程方法论
- 主线：01-ai-agents / Agent 平台架构 + Harness 工程化
- 同作者姊妹篇：[[01-ai-agents/万字长文拆解Agent-架构设计-四-多-Agent-协作]]（7/22）——"多 Agent 编排 / 多租户底座"对偶
- 同日姊妹篇：[[02-ai-coding/phodal-项目记住-Coding-Agent-5步法]]（8/3）——"治理 / 落地"对偶

## 知识节点（8 个）+ 正文要点（6 节）

- **节点 1 Scope 隔离 7 项资源：** 每个员工/Slack 频道/群组/项目 = 独立 scope；记忆/文件/凭据视图/权限/cron/Web/沙箱——个人定制与团队共享兼得。
- **节点 2 持久电脑 Durable Computer：** execute 工具把命令送进 scope 自己的隔离沙箱——装过的工具不丢、重启重部署都在，不是一次性容器。
- **节点 3 4 个 Harness 适配器：** Pi / OpenCode / Codex / Claude Code 跑同一套核心；每种 substrate 躲在接口后面，换 wiring file 整体替换——QM 想做"智能体平台的操作系统层"。
- **节点 4 Durable by default：** 状态不落内存，落 Postgres；蓝绿部署多实例运行——进程内 Map/环形缓冲会被部署抹掉，凡以后还要读回的东西必须进持久存储。
- **节点 5 智能体 = 你本人：** 以所服务那个人的身份行动，持其凭据守其权限全程审计——与 OpenCode/Codex/Claude Code 本地编码智能体一脉相承。
- **节点 6 3 种安全 Posture + 命令策略：** Strict（每次工具调用暂停等批准）/ Auto（数据抵达模型前分类器来源标记）/ Dangerous（不筛查不暂停自负后果）+ 递归删除/破坏性 SQL 硬性拒绝在所有 posture 下生效 + 供应链 7 天静置。
- **节点 7 收文字不收代码 + 5 条工程文化：** AGENTS.md 5 条铁律（修每一处/让系统更简单/独立审查/不留注释）+ 贡献政策收 .txt/.md 提案不收代码——提案/实现解耦。
- **节点 8 多租户底座定位：** QM 不是聊天机器人，是让"每人一个智能体 + 团队协作"成立的多租户底座；core 无头、界面/模型/框架都可换。

正文 6 节：① 核心命题 Scope 隔离（个人定制 + 团队共享兼得）② 落地场景（统一搜索/邮件分身/代码仓库作业/项目跟踪 + 种子技能 GitHub/Google Workspace/Linear）③ 架构无头核心 + 持久电脑 + Durable by default + TypeScript+Node/Fastify/Vite+Lit ④ 不绑模型不绑框架（4 个 Harness 适配器 substrate 接口化）⑤ 安全 = 你本人 + 3 posture + 命令策略 + 7 天 npm 静置 + 坦诚披露已知局限 ⑥ 工程文化 5 条铁律 + 收文字不收代码。

## 关联图谱

- **上游：** [[01-ai-agents/万字长文拆解Agent-架构设计-四-多-Agent-协作]]（7/22 同作者）+ [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] [[01-ai-agents/HarnessEngineering企业级实战]] [[01-ai-agents/Harness工程AgentLoop]] [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] [[01-ai-agents/agent-architecture]]
- **下游：** [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]] [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]] [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]] [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]] [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] [[01-ai-agents/cases/liangbo-execution-agent]]
- **同级：** [[06-ai-tech/Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]] [[06-ai-tech/企业知识库认知底座]] [[06-ai-tech/Agent Harness 与 OpenClaw：从工具到系统的中文解读]] [[01-ai-agents/未来属于垂直领域Agent]] [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]] [[01-ai-agents/Agent时代架构师系统能力]] [[02-ai-coding/phodal-项目记住-Coding-Agent-5步法]]（8/3 同日）

## 6 个对 Seetong 借鉴动作

1. **Scope 体检：** 识别 Seetong 4 类隔离场景（客户工单/SDK 仓库/Harmony 设备/4G IPC 监控）按"人/项目/设备"切 scope。
2. **持久电脑类比：** Seetong AI 助手每个 Skill 工具链（神策/TAPD/Git）按"工具已装、状态在册"原则改造。
3. **Durable by default：** Seetong AI 助手 cron/Skill 状态/客户工单升级全进 Postgres——避免部署丢任务。
4. **4 Harness 适配器思路：** Seetong AI 助手不绑死单一模型/框架——OpenClaw 已支持多 Agent runtime 切换，方向正确。
5. **3 种 Posture + 命令策略：** Seetong AI 助手对生产/凭据/不可逆操作分级（Strict/Auto/Dangerous）+ 递归删除/破坏性 SQL 硬性拒绝。
6. **5 条工程文化铁律入 SKILL.md：** 修每一处/让系统更简单/独立审查/不留注释/收文字不收代码——前 4 条做编码规则，第 5 条改提案/实现解耦流程。

## 备注与限制

1. 作者：AllenTang（`og:article:author=AllenTang`，公众号名未暴露，按内容定位「架构师带你玩转AI」）；一手 https://github.com/yc-software/qm（MIT）。
2. 发布：推断 2026-07 末至 2026-08。
3. 可证伪："4 个 Harness 适配器"是文章快照主分支可能更新；"7 项 scope 资源"是归纳非官方完整列表。
4. 不适用：1 人小工具/单人项目——scope 隔离价值在多租户，单人是 overhead。
5. 关联首选：与 [[01-ai-agents/万字长文拆解Agent-架构设计-四-多-Agent-协作]]（7/22 同作者）+ [[02-ai-coding/phodal-项目记住-Coding-Agent-5步法]]（8/3 同日）形成"多 Agent 编排 / 多租户底座 / 治理落地"三连。