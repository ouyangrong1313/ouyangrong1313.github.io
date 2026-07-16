---
title: 架构腐朽与Loop-Engineering
category: 02-ai-coding
tags:
  - "#主题/架构腐朽"
  - "#主题/Loop-Engineering"
  - "#主题/排熵"
  - "#主题/AI-Coding时代"
  - "#主题/架构约束代码化"
  - "#节点/Linux外紧内松"
  - "#节点/守卫自检"
  - "#节点/删比改"
  - "#作者/lencx"
nodes: 架构五层定义｜腐朽必然性｜重构悖论｜Linux外紧内松｜提交即重构｜守卫自检｜删比改更重要｜Loop-Engineering
links:
  - "[[Addy-Osmani-Loop-Engineering]]"
  - "[[AI循环-Claude-GPT和Mira到底什么才是真正好用的]]"
  - "[[Loop-Engineering-验证才是瓶颈]]"
  - "[[loonggg-Claude-Code-技能心法-11条建议]]"
date: 2026-07-15
source: 微信公众号「lencx」2026-07 推送 / 作者 lencx（Mark Text 等开源工具作者）/ 原文 https://mp.weixin.qq.com/s/wINKSDQCroWBvf29h567zA
---

# 架构腐朽与 Loop Engineering

- **原文链接**：https://mp.weixin.qq.com/s/wINKSDQCroWBvf29h567zA
- **原始作者**：lencx（微信公众号「lencx」，Mark Text 等开源工具作者）
- **发布时间**：2026-07（推送日未在原文标注）
- **获取时间**：2026-07-15 10:42 Asia/Shanghai

## 核心结论

> 屎山源于不敢删，架构活于持续排熵；AI Coding 时代代码生成边际成本接近 0，腐朽速率同样翻倍——唯一解药是把架构约束编码到 Loop + CI 里让机器维护。

**分类**：本文是"AI Coding 时代架构腐朽应对 + Loop Engineering 方法论"专题，主轴是代码工程实践而非 Agent 架构。放 02-ai-coding 与现有 Loop/Harness/AI Coding 主线同分类；补完现有主线偏"Loop 入门/Harness 实战"缺位的"架构腐朽 + AI Coding 时代新紧迫性"维度。

## 知识节点（8 个独立概念）

- **架构定义五层**：图（快照）/ 决策记录（ADR）/ 约束（"你不许做什么"，不是增加自由而是把危险自由收掉）/ 运行时结构（模块边界、依赖方向、并发模型、可降级）/ **"删起来贵的部分"**——第五层是工程现实最贴的工作定义
- **腐朽必然性 = 历史负担 + 失败成本不对称**：三年前的字段约定可能承载合规要求；五年前的 if 分支可能绕过了某个 SDK bug；历史负担越来越重 + 工程师越来越保守 = 系统越来越没人敢动
- **重构悖论**：立项永远漂亮（边界清晰/性能更好/风险更低），但两年后多数人选择绕道——在旧系统旁边起新服务、用适配层接上，旧系统没被替换只是被包裹，问题没消失只是多了一层壳
- **Linux 外紧内松**：稳定性预算必须花在正确的边界上——绝大多数 commit 不进稳定树，预算集中在系统调用/驱动 API/文件系统语义"对外承诺"接口；内部实现频繁重写反而是好事
- **提交即重构**：把重构分摊到每次 commit——小步前进 + 主干可编译 + 重构不动语义 + 删死代码 + 命名即文档（5 条原则）；反模式是"攒够一波再重构一次"——攒得越多越不敢动 + 重构 PR 越大越难评审 + git bisect 失效
- **守卫自检**：永远 pass 的检查器信息量为零（系统完美 OR 检查器早已失效）；每条规则配反例测试，故意写一个违反规则的 commit 让 CI 报错后回滚，证明检查器还能工作
- **删比改更重要**：祖训（那个模块别动/那张表别删字段/那段逻辑别修）是软件熵的化石；定期盘点"已知死代码" + 让删变成正常开发动作（review checklist 加"能不能删"）+ 删前加引用监控
- **Loop Engineering**：AI Coding 让代码生成边际成本接近 0（熟练工程师 + Claude Code + 良好 Harness 一周可写出以前团队一月的代码量）；腐朽速率同样翻倍（手写 bug 变成模型批量生成烂代码 + 工程师审核不过来）；架构师工作从"画图"变成"把约束编码到 Loop"——约束进 Loop，Loop 进 CI，CI 不可绕过

## 关联图谱

### 上游（基于 / 来自）

- Linux 内核稳定性分配实践
- Addy Osmani Loop Engineering 推文（参考链接 [18]）
- Sairahul1《Loops: What Every AI Engineer Needs to Know in 2026》（参考链接 [19]）

### 下游（应用于 / 验证于）

- AI Coding 时代架构腐朽应对（排熵机制）
- Loop 自动化 + CI 强制卡口（约束代码化）
- 删代码 vs 加代码的 review 标准重设

### 同级（横向 / 并列）

- [[Addy-Osmani-Loop-Engineering]]（Loop 主线原典）/ [[AI循环-Claude-GPT和Mira到底什么才是真正好用的]]（Loop 五步骨架）/ [[Loop-Engineering-验证才是瓶颈]]（验证主题）/ [[loonggg-Claude-Code-技能心法-11条建议]]（Claude Code 团队 Skill 心法）

## 正文要点 + Seetong 借鉴动作

**4 段核心论证 + 6 个对 Seetong 借鉴动作**：

| 论点 | 原文证据 | Seetong 借鉴动作 |
|---|---|---|
| **腐朽必然性 + 祖训清单** | "每个人都记得几条祖训：那个模块不要动；那张表有几个字段没人知道用途" | **动作 1**：欧阳荣+黄松佳+谭伟+张威 4 人共同列 Seetong 当前"祖训清单"（哪些模块不能动/字段不敢删/逻辑没人敢改），反思哪几条源于"不敢删"而不是"真正必要" |
| **Linux 外紧内松 + 稳定性预算** | "稳定性预算必须花在正确的边界上——系统调用边界、驱动 API、文件系统语义" | **动作 2**：做 Seetong 稳定性预算体检——80% 监控/告警预算投在哪些边界（4G IPC 设备协议/神策埋点 schema/用户 API/Logan 格式），是否对称？内部实现可激进重构 |
| **提交即重构 + 排熵机制** | "把重构分摊到每一次提交里" | **动作 3**：每 sprint 强制 1 个删废弃代码 PR；review checklist 加"能不能删"项；定期盘点 Seetong 老屎山（4G IPC 多版本兼容层/老 API 适配层/弃用 UI 组件） |
| **守卫自检 + 永远 pass** | "一个永远通过的检查，对判断当前代码是否破坏约束几乎没有信息量" | **动作 4**：找出 Seetong 自动化检查中"永远 pass"的项——神策埋点 schema 校验/反馈分类一致性/友盟崩溃字段对齐/数据清洁体检；配反例测试故意触发失败，证明检查器还在工作 |
| **删比改更重要 + 删前加监控** | "删的勇气，比改的能力更难培养" | **动作 5**：Seetong 删代码前加 1-2 周引用监控（看哪些埋点/接口/字段真没人调用），监控期内确认 0 引用再删；让"删"成为正常开发动作 |
| **Loop Engineering + AI Coding 时代** | "约束进 Loop，Loop 进 CI，CI 不可绕过" | **动作 6**：把 Seetong 重要架构约束编码到 Loop + CI——数据清洁体检/字段命名一致/反馈分类规则/报警阈值规则 → CI 卡口自动跑，与 [[seetong-feedback-radar]] skill 衔接做反馈分类 Loop 自动化 |

## 备注与相关链接

**备注与限制**：

- 作者 lencx 是 Mark Text 等开源工具作者，独立开发者视角；推送日未在原文标注，按抓取日 2026-07-15 反推归 2026-07
- "AI Coding 代码量 10x 增长"是 lencx 经验判断，非独立统计数据；"重构悖论（立项漂亮 → 两年后绕道）"是观察未给量化数据
- Linux 内核"绝大多数 commit 不进稳定树"是 lencx 简化表述，实际有 stable/longterm/mainline 三线模型

**相关链接**：

- 原文 raw/digest 见 `raw/2026-07-lencx-架构腐朽与Loop-Engineering*.md`
- Wiki digest 见 `wiki/02-ai-coding/架构腐朽与Loop-Engineering-digest.md`
- 参考 [18] Addy Osmani Loop Engineering：https://x.com/addyosmani/status/2064127981161959567
- 参考 [19] Sairahul1 Loops：https://x.com/sairahul1/status/2064277888216555684
- 同分类已挂载：[[Addy-Osmani-Loop-Engineering]] [[AI循环-Claude-GPT和Mira到底什么才是真正好用的]] [[loonggg-Claude-Code-技能心法-11条建议]] [[Code-is-cheap-AI-Native-五倍效率]]

---

*透明玻璃自检：wiki 字节 (≤8K)/ 节点 8 (6-10)/ H2 5 (≤5)/ 表格 1 (≤2)/ 0 陈词（按硬约束清单逐项核查）*
