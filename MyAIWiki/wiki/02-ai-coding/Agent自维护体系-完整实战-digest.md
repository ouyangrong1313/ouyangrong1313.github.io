---
title: Soyoger Agent 自维护体系 - Digest
date: 2026-07-20
slug: Agent自维护体系-完整实战-digest
category: 02-ai-coding
tags:
  - Loop-Engineering
  - Agent自维护
  - Skill设计
rating: ⭐⭐
source: "[[02-ai-coding/Agent自维护体系-完整实战]]"
---

# Soyoger Agent 自维护体系 - Digest

## 一句话总结与关键数字

**AI 写代码只是开始，维护循环才是真正的战场**——"5 动作 + 6 零件"改造人工维护循环。诊断/修复/发布三套 Skill + Sub Agents 独立裁判 + Token 分级 + 知识库复利飞轮：40 分/人次 → 48 分全量扫描 + 1 分人工审批，月省 20+ 人天，成本降 80%。

数字：40→48 分 / 334 测试 / 80% 降本 / 20+ 人天/月 / 5 条起步告警 / 6 层验证 / 8 Phase+6 Step+11 步 Skill。

## 8 节点速查表

| # | 节点 | 核心 |
|---|---|---|
| 1 | 三个断裂点 | 看不见 / 记不住 / 没闭环 |
| 2 | 四层进化 | Prompt→Context→Harness→Loop（AutoGPT 跳级必翻车） |
| 3 | 5 动作 | 发现→交付→验证→持久化→调度（缺一不可） |
| 4 | 实施顺序 | Connectors→Automations→Skills→Worktrees→Sub Agents→State |
| 5 | 三套 Skill | 诊断 8 Phase / 修复 6 Step（知识库复利）/ 发布 11 步（4 道熔断） |
| 6 | Sub Agents 独立裁判 | 6 层验证，check_log_level_not_downgraded 拦日志降级 |
| 7 | 真实数据 | 月省 20+ 人天，成本降 80% |
| 8 | 4 教训 | 工期翻倍 / 告警 5 条内 / Token 分级 / 数据类不自动化 |

## 关键提炼（5 金句 + 3 反直觉 + 4 教训）

**5 句金句**：(1) "AI 写代码只是开始，维护循环才是真正的战场"；(2) "跳级必翻车。Loop 不是买一个产品就有的，是在前三层地基上垒出来的"；(3) "SKILL.md 是操作手册，规则不写死 Agent 一定偷懒"；(4) "掩盖故障和合理降级，只有独立验证才能区分"；(5) "知道什么不该自动化，和知道什么该自动化一样重要"。

**3 反直觉**：(1) 修复者永远不应给自己打分（验证权给独立 Sub Agents）；(2) 诊断报告 = Skill 之间的接口，避免人传话；(3) Token 必须分级（小模型 5K 初筛 + 大模型按需）。

**4 教训速览**：(1) Connectors 工期翻倍；(2) 告警 5 条内；(3) Token 分级降 80%；(4) 数据/安全/核心业务修 = 转人工。

## 6 个 Seetong 借鉴动作

1. **工具链工期翻倍自评**：神策/友盟/TAPD/GitHub/反馈平台连接完整度——哪些 Agent 仍需人切控制台
2. **三套 Skill 模板**：诊断 8 Phase + 修复 6 Step + 发布 11 步入 Seetong Skill；先在 `seetong-team-daily-recap` 试点
3. **6 层验证闸门**：每 Skill 完成判定由独立 Agent 给出？先用 `seetong-feedback-radar` 日报做 Sub Agent 复审试点
4. **Token 分级熔断**：每 cron 加 token 上限 + 月度预算；月度预算 = 当前消耗 × 2
5. **诊断报告 = 接口**：让"反馈分诊日报"以结构化 MD 输出，作为下一个 Skill 的输入
6. **不该自动化的边界**：列 5 个不该自动化的场景（数据/客户隐私/核心业务/法务/付费）

## 关联与限制

**关联**：方法论同主线 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] / [[02-ai-coding/Addy-Osmani-Loop-Engineering]] / [[02-ai-coding/架构腐朽与Loop-Engineering]] / [[02-ai-coding/AI循环-Claude-GPT和Mira到底什么才是真正好用的]]；前置层 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]；同主线 [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]] / [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] / [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]。

**待补证**：月 20 人天 / 80% 降本 / 6 零件顺序均为 Soyoger 单团队经验，无行业基准；工具链 30% 占比也是经验值。

**已知限制**：单一团队案例、特定技术栈（MCP/SLS/Langfuse/Playwright）；Seetong 适配需映射等价工具（SLS → 神策、Langfuse → 友盟 APM、Playwright → 自研）。
