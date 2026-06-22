---
title: Claude Code：如何能构建主动式 Agent 工作流？
category: 02-ai-coding
date: 2026-06-17
source: 微信公众号 Capihom 2026-06-17 编译（原始来源：Anthropic applied AI 团队 Maya 的演讲"Build a proactive agent workflow with Claude Code"）
source_url: https://mp.weixin.qq.com/s/kvtDAdTe2H4hTUXc3FEaVg
youtube_url: https://www.youtube.com/watch?v=eSP7PLTXNy8
tags: [#主题/AI-Coding, #主题/Claude-Code, #主题/主动式Agent, #主题/工作流设计, #主题/Anthropic实践, #节点/Routines, #节点/主动式Agent, #节点/三大基础设施负担, #节点/最小配置, #节点/触发器, #节点/上下文=成功的上限, #节点/可转向性, #节点/渐进路径, #手法/反例论证, #手法/产品视角, #场景/AI工作流, #场景/PM工具箱]
nodes: [主动式Agent, Routines, 三大基础设施负担, Routines最小配置, 托管会话, 触发器, 上下文=成功的上限, 可转向性]
links: [[Claude-Code首席设计师Meaghan-Choi工作流]], [[Claude-Code一周年回顾-Boris-Cat]], [[Anthropic万字长文三个判断和一个阳谋]], [[claude-code-dynamic-workflows]], [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[APPSO-Codex-Claude-Code-Loop-Engineering]], [[Agentic-Engineering-AI-Workbench]], [[Claude-Code之父品味不是人类护城河]], [[Claude-Code作者Boris-28分钟教你写真正有效的Prompts]]
---

# Claude Code：如何能构建主动式 Agent 工作流？

- **原文链接**:https://mp.weixin.qq.com/s/kvtDAdTe2H4hTUXc3FEaVg
- **演讲原视频**:https://www.youtube.com/watch?v=eSP7PLTXNy8（Anthropic applied AI 团队 Maya）
- **发布渠道**:微信公众号 Capihom（编译稿）| **发布日期**:2026-06-17 | **编译时间**:2026-06-17

## 核心结论与分类

> **主动式 Agent 不该等你按回车才开始工作。** Anthropic 在 Claude Code 里推出 **Routines**:让 Claude 按 cron / GitHub 事件 / webhook 主动启动远程会话,最小配置 = prompt + repo + connector + trigger 四样。**主动式 Agent 三大设计问题**:触发器(什么时候上班) + 上下文(能读到哪些信息) + 可转向性(人怎么介入和校正) —— 渐进路径 = 先让 Claude 做调查建议,再把行动权限一点点放出去。

- **分类**:02-ai-coding（Claude Code 工具使用 + 工作流设计）
- **类型**:Anthropic 内部演讲浓缩稿（Capihom 编译）
- **位置**:Anthropic **第一次把 Routines 当作"产品定位"对外讲** — 与 [[Claude-Code首席设计师Meaghan-Choi工作流]]（同公司同系列）、[[Claude-Code一周年回顾-Boris-Cat]]（Routine 异步化的产品化落地）形成"工具使用 + 战略定位"四角
- **节点数**:8

## 8 个知识节点

| 节点 | 一句话定义 | 关键洞察 |
|---|---|---|
| **主动式 Agent Proactive Agent** | 不等你按回车,在问题出现时自己开始调查 | proactive agents beat reactive agents;价值不在回答漂亮,在能先开始调查 |
| **Routines** | Anthropic 在 Claude Code 里推出的"按日程/事件主动启动的远程会话"产品 | 最小配置 = prompt + repo + connector + trigger 四样 |
| **三大基础设施负担** | 跑在哪里(本地/托管/持久化/鉴权)+ 什么时候触发(cron/endpoint/event 胶水)+ 人怎么介入(可观察可转向可恢复) | 团队过去不愿碰的部分,自动化跑起来后变成产品设计的一部分 |
| **托管会话 Hosted Session** | 运行在 Claude Code 托管基础设施,笔记本开不开都不影响 | session 可打开、观察、跟进、转向、恢复;不是黑箱后台 |
| **触发器 Trigger** | cron / GitHub event / webhook payload as context | 越具体越能收紧任务边界;"哪件事发生时,AI 应该开始工作" |
| **上下文 = 成功的上限** | Claude 拥有什么上下文,就能做到哪一步 | AI 判断不稳定的根因往往不是模型态度,而是流程没把必要信息接进来 |
| **可转向性 Steerability** | agent-on-agent review / 人在中途进入会话 | 主动式 agent 不要求人消失,要求人能叫停 |
| **渐进路径** | 先让 Claude 做调查建议,再把行动权限一点点放出去 | 小处先赢,系统会慢慢长出来 |

## 关联图谱

### 上游(基于 / 来自)

- [[Claude-Code首席设计师Meaghan-Choi工作流]] — 同一公司同系列产品,Meaghan Choi 演示 worktree 并行 + 全链路自动化
- [[Claude-Code一周年回顾-Boris-Cat]] — Routine 异步化 + Auto Mode 反直觉安全;**Routines 是 Routine 异步化的产品化落地**
- [[Anthropic万字长文三个判断和一个阳谋]] — Anthropic 战略主线;慢变量安全垫与本文"主动式 agent"是同主线
- [[claude-code-dynamic-workflows]] — 动态工作流的具体实现

### 下游(应用于 / 验证于)

- [[Addy-Osmani-Loop-Engineering]] — 5+1 积木中的 **Automations = Routines 的方法论原典**
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] — 4 入口(触发/沙箱/验收/账本)中"触发"对应本篇触发器设计
- [[APPSO-Codex-Claude-Code-Loop-Engineering]] — 产业同向共振;4 人物(Boris/Cat Wu/Tibo/Addy)同向信号
- [[Agentic-Engineering-AI-Workbench]] — 5 层结构工作台包含这种托管会话

### 同级(横向 / 并列)

- [[Claude-Code之父品味不是人类护城河]] — Anthropic 战略主线另一视角
- [[Claude-Code作者Boris-28分钟教你写真正有效的Prompts]] — Boris Cherny 工作流方法论

## 正文要点(主张 + 案例 + 操作)

**1. AI 提效正在从"写好 prompt"转向"把稳定流程设计成可触发、可观察、可校验的系统"。** 流程一旦能写成触发器+上下文+校验方式,就不再是某人的熟练手法,而是团队可复用的生产机制。PM 过去常把"自动化"理解成一段脚本或一套运营 SOP,现在要学会把任务启动条件也设计进去。**Seetong 借鉴**:seetong-daily-briefing 现在是 cron 触发 + 简报输出,但没有"可观察可校验"机制 —— 加结果校验(网络 -102 反馈量、登录成功率)和差异告警。

**2. 主动式 Agent 三大基础设施负担。** Maya 把主动式 agent 难点拆成三件事:(1) agent 跑在哪里(本地会断,需托管/持久化/鉴权);(2) 什么时候触发(cron/endpoint/event 都要胶水);(3) 人怎么介入(headless 会话不可见不可控)。**Maya 原话**:"你需要在 prompt 之外搭出一整套基础设施,这当然能做,但工作量很大。"**Seetong 借鉴**:Seetong 现有 cron(HEARTBEAT / 简报 / 神策友盟反馈 dry-run)解决了 1 + 2,但 3(人怎么介入)还很弱 —— 需要加可观察面板。

**3. Routines 最小配置只有四样东西。** prompt + 连接的 repo + 可用连接器 + 触发器。运行在 Claude Code 托管基础设施,笔记本开不开都不影响。**Anthropic 内部案例**:Sarah 文档同步 routine(每周一上午 10 点跑) = 读 main 分支新变化 + 对照文档 repo + 开 PR。Claude Code 每周 PR 数从新年开始增长 **200%**。**Seetong 借鉴**:seetong 内部 SDK changelog 同步、Seetong-tps 跨端版本说明同步,设个每周 routine 自动对照并开 PR。

**4. 触发器决定 agent 什么时候上班。** Maya 强调"第一项决定,是你的 routine 应该在什么时候触发"。**好的触发器**:文档同步每周一上午十点 / release branch 与文档 diff / 带 need docs 标签的 PR 合并 / 高优先级 issue 创建 / 用户反馈进 Slack 频道 / 一次 CD pipeline post。**反问**:"哪件事发生时,AI 应该开始工作?" — 触发器越具体,任务边界越能收紧。**Seetong 借鉴**:Seetong Bug 反馈自动归类可设"App 崩溃/ANR"事件作为 trigger,而不是简单的每天跑一次。

**5. 上下文 = 成功的上限。** "无论 Claude 拥有什么上下文,那就是 Claude 能成功的上限。" 缺源码它无法判断功能变化;缺文档 repo 它开不了 PR;缺 Slack 它无法通知。**Maya 这段给了一个更工程化的解释**:AI 判断不稳定的根因往往不在模型态度,而在流程没把必要信息接进来。**Seetong 借鉴**:为 seetong-daily-briefing 列出"输入源清单"(神策数据 / 友盟崩溃 / Tapd 任务 / 用户反馈 / 内部 changelog),缺哪一块就补哪一块。

**6. 可转向性 Steerability = 主动式 Agent 成熟形态。** 两种做法:(1) agent-on-agent review — 一个 routine 创建文档 PR,另一个 routine 在 PR 创建后做 reviewer,先留评论再交给人;(2) 人在中途进入会话,像使用终端里 Claude Code 一样查看当前分析、提出问题、把方向推回正确轨道。**Seetong 借鉴**:seetong-batch-issue-rootcause-analysis 设"分析 routine + 验证 routine"两阶段,人最后只看差异和证据。

**7. 主动式 Agent 不要求人消失,要求人能叫停。** Maya 现场演示了 GitHub issue 触发的文档 routine,发现自己已有另一个 PR 处理同样问题,直接让 Claude 停止会话。**Maya 原话**:"你可以在实时会话里问它问题,把它推向另一个方向。" **Anthropic 在文档场景里还会渲染 Claude 修改过的页面,确认输出符合预期** —— 把"相信模型"变成"检查结果"。**Seetong 借鉴**:每个 Seetong Skill 都要有"暂停 / 转向 / 恢复"入口,不能跑起来后只能等结束。

**8. 渐进路径 + 小处先赢。** Maya 现场案例:deploy verifier 案例 —— CD pipeline 每次部署后向 webhook 发请求,Claude 读服务源码 + DataDog + Grafana,先给出 no-go / go 决策;**当团队信任增加,再让它参与回滚动作**。**Maya 原文**:"先别急着设计宏大的 agent 系统。挑一个每周都重复、输入来源稳定、结果需要人确认的流程:文档同步、issue 分拣、发布检查、用户反馈归类。" **Seetong 借鉴**:不要一次设计十个自动化,挑一个 Seetong 流程跑顺后再加下一个。

## 备注与限制

- **本演讲的特殊价值**:这是 Anthropic **第一次把 Routines 当作"产品定位"对外讲**——从"工具使用"升级到"产品定位",意味着 AI 工作流设计进入"团队能力建设"阶段
- **本次编译的限制**:Capihom 是浓缩稿,完整演讲含 Maya 现场演示和问答环节,本文未覆盖;**部分操作细节(如 routine 在 web/CLI/desktop 的具体界面)未在文中展开**
- **本次未在文中出现但 Maya 反复强调的反问句**:"你的 routine 应该在什么时候触发?Claude 拥有什么上下文?人怎样介入?"
- **与本工作区 Seetong 主线的强关联**:
  - Seetong OpenClaw HEARTBEAT / 简报 cron / 神策友盟反馈 dry-run / Login 成功率每日巡检 — 都是 Seetong 现有"主动式 agent"雏形
  - 5+1 积木的 Automations = Routines 的方法论抽象
  - 本文与 [[APPSO-Codex-Claude-Code-Loop-Engineering]] 的"4 个对 Seetong 可借鉴动作"高度对应
  - Maya 三大基础设施负担 = seetong-execute / seetong-plan / seetong-finish 等 Skill 设计的 checklist
- **速读摘要**:见同目录 [[Claude-Code-主动式Agent-Routines-digest]]
