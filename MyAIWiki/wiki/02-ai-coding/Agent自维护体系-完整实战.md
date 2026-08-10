---
title: Soyoger：Agent 自维护体系完整实战（5 动作 6 零件）
subtitle: 40 分钟排查→48 分钟扫描 + 1 分钟审批，334 测试 + 6 层验证 + 三套 Skill
author: Soyoger
source_wechat: 微信公众号「Soyoger」2026-07-20 推送
date: 2026-07-20
slug: Agent自维护体系-完整实战
category: 02-ai-coding
tags: [Loop-Engineering, Agent自维护, Skill设计, Sub-Agents]
rating: ⭐⭐⭐
source: https://mp.weixin.qq.com/s/mxCEO3NxwBrOEsTfAzyzQQ
digest: "[[Agent自维护体系-完整实战-digest]]"
related:
  - "[[Loop-Engineering-验证才是瓶颈]]"
  - "[[Addy-Osmani-Loop-Engineering]]"
  - "[[架构腐朽与Loop-Engineering]]"
  - "[[Lilian-Weng-Harness-Engineering-自我改进]]"
  - "[[loonggg-Claude-Code-技能心法-11条建议]]"
  - "[[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]"
  - "[[WorkBuddy-Harness工程复盘-从模型到可用Agent]]"
---

# Soyoger：Agent 自维护体系完整实战（5 动作 6 零件）

> 微信公众号「Soyoger」2026-07-20 推送
> 原文链接：https://mp.weixin.qq.com/s/mxCEO3NxwBrOEsTfAzyzQQ

## 核心命题

**AI 写代码只是开始，维护循环才是真正的战场**——本文复盘"5 动作 + 6 零件"改造人工维护循环。诊断/修复/发布三套 Skill + Sub Agents 独立裁判 + Token 分级控制 + 知识库复利飞轮：40 分钟/人次 → 48 分钟全量扫描 + 1 分钟人工审批，月省 20+ 人天，成本降 80%。

5 句核心金句：(1) "AI 写代码只是开始，维护循环才是真正的战场"；(2) "跳级必翻车。Loop 不是买一个产品就有的，是在前三层地基上垒出来的"（AutoGPT 反例）；(3) "SKILL.md 是一份严格的操作手册，不是一段描述；规则不写死，Agent 一定偷懒"；(4) "掩盖故障和合理降级，只有独立验证才能区分，不能让修复者自证"；(5) "知道什么不该自动化，和知道什么该自动化一样重要"。

## 8 个核心节点

### 节点 1：三个断裂点（维护循环卡在哪里）

- **看不见**：错误散落——一周 1000+ ERROR 散在 3 个 Logstore，每天 50→350 翻 7 倍晚 24 小时才发现
- **记不住**：经验锁死在 AI 对话里——同类问题第二次修同样慢
- **没闭环**：修复者给自己打分——logger.error 改 logger.warning = "已修复"（错误还在，只是不喊）

### 节点 2：四层进化（AI 工程化位置）

| 层级 | 时间 | 能力 | 局限 |
|---|---|---|---|
| Prompt | 2022 | 单次问答 | 失忆 |
| Context | 2025 | 喂日志/代码库/文档 | 你问一句答一句 |
| Harness | 2026 初 | Shell + MCP + Git | 每次都要按启动键 |
| **Loop** | **2026.06** | **规则写死、自动跑** | **人只在关键节点批准** |

**跳级必翻车**（2023 AutoGPT = 循环空转烧钱）；Loop 是前三层地基垒出来的。

### 节点 3：5 动作 + 6 零件

**5 动作**：发现 → 交付 → 验证 → 持久化 → 调度。少"验证"= 批量假修复；少"调度"= 退回一次性操作。

**6 零件**：Connectors → Automations → Skills → Worktrees → Sub Agents → State。**跳层必踩坑**。

### 节点 4：Connectors——打通 6 层数据接口

最易被低估的一步。Agent 默认只见本地文件，没打通 MCP/SLS/Langfuse/Git/Playwright/通知 = 后续 Skill 全是空中楼阁。

**验收标准**：一条命令查日志 + 串 trace + 触发预发部署，中间不切任何控制台。

### 节点 5：三套 Skill（核心设计）

**诊断 Skill（8 Phase）**：Phase 2 git log 交叉验证判断标准写死（7 天新问题 / 14 天长期 / 突变 / 回归）；**Phase 6 证据链格式**（[事实+证据来源+推理+结论]，无证据打回重做）；**数据类不让 Agent 修，转人工**。

**修复 Skill（6 Step）**：解析报告 → **grep 知识库（30+ 条 YAML 修复方案，连接池超时 48 分钟→15 分钟 = 复利飞轮）** → 生成补丁 → 跑测试（受影响 + 全量 334） → 提 feature 分支 → 触发部署。**3 轮限制**：超自动升级人工。

**发布 Skill（11 步）**：Step ⚠0 三重安全校验 → Step ⚠4 必须指定 skill_names（不指定 = 测试失焦）→ Langfuse Trace 0 ERROR → 推审批卡片。**人工介入 0 次**。

### 节点 6：Sub Agents 独立裁判——堵死假修复

修复者永远不应给自己打分。验证 Agent 必须是新启动的独立 Sub Agent。

**6 层验证**（validate_fix）：(1) 单元测试全绿 / (2) 预发无新增 ERROR / (3) Langfuse Trace 0 ERROR / (4) **拦截日志降级假修复（check_log_level_not_downgraded）**——直接命名出的具体检查项 / (5) 向后兼容 / (6) 预发 vs 线上行为一致。

### 节点 7：真实数据

旧流程 40 分钟/排查（Top 3-5 类覆盖）→ 新流程 48 分钟全量扫描 + 1 分钟审批。月省 **20+ 人天**，成本降 **80%**（小模型 5K 初筛 + 大模型按需 + 双熔断）。

### 节点 8：4 个教训

- **教训一**：Connectors 工期翻倍估算——工具链占 30%，"先跑起来再说"心态导致后面花 1 倍时间补
- **教训二**：告警宁缺勿滥，5 条以内起步——配 15 条 IM 群消息刷屏没人看
- **教训三**：Token 分级——小模型 5K 初筛 + 大模型按需 + 单次/月度双熔断 → 成本降 80%
- **教训四**：**不是所有问题都该自动化**——数据/安全/核心业务一律转人工，**"知道边界才能放心开放权限"**

## 关联图谱

**方法论同主线 Loop**：[[Loop-Engineering-验证才是瓶颈]] / [[Addy-Osmani-Loop-Engineering]] / [[架构腐朽与Loop-Engineering]] / [[AI循环-Claude-GPT和Mira到底什么才是真正好用的]]。

**方法论对偶**：[[Lilian-Weng-Harness-Engineering-自我改进]]（Harness 是 Loop 前置层）/ [[loonggg-Claude-Code-技能心法-11条建议]]（"SKILL.md 是操作手册"）/ [[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]（状态文件驱动同主线）/ [[WorkBuddy-Harness工程复盘-从模型到可用Agent]]（Context Engineering + 验证闸门工程化）。

## 6 个对 Seetong 团队可借鉴动作

1. **工具链工期翻倍自评**：神策/友盟/TAPD/GitHub/反馈平台连接完整度——哪些 Agent 仍需人切控制台？
2. **三套 Skill 模板**：诊断 8 Phase 入 `seetong-feedback-radar`；修复 6 Step 入 Skill 模板；发布 11 步先用 `seetong-team-daily-recap` 试点
3. **6 层验证闸门**：每 Skill 完成判定由独立 Agent 给出？先用 `seetong-feedback-radar` 日报做 Sub Agent 复审试点
4. **Token 分级熔断**：每 cron 加 token 上限 + 月度预算；月度预算 = 当前消耗 × 2
5. **诊断报告 = 接口**：让"反馈分诊日报"以结构化 MD 输出，作为下一个 Skill 的输入
6. **不该自动化的 5 个边界**：列清单（数据/客户隐私/核心业务/法务/付费），明确不交 Agent 自动修

## 备注与限制

- 单一团队经验、特定技术栈（MCP/SLS/Langfuse/Playwright）；Seetong 适配需映射（SLS → 神策、Langfuse → 友盟 APM、Playwright → 自研）
- 月 20 人天 / 80% 降本 / 6 零件顺序 均为 Soyoger 单团队经验，无行业基准
- 标签 #主题/Loop-Engineering #主题/Agent自维护 #主题/Skill设计 #主题/Sub-Agents #主题/验证闸门 #主题/Token-分级 #主题/MCP #主题/Seetong借鉴 #公众号/Soyoger #节点/三个断裂点 #节点/四层进化 #节点/5个动作 #节点/6个零件 #节点/三套Skill #节点/Sub-Agents独立裁判 #节点/6层验证 #节点/4个教训
