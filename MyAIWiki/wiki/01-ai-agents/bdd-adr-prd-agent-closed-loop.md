---
title: BDD+ADR+PRD：让 Agent 遵守规范的闭环方法
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/AI-Coding
  - 场景/技术博客
  - 场景/公众号长文
  - 节点/Harness
  - 节点/Context-Engineering
  - 节点/Agent-Loop
  - 节点/Memory
  - 节点/Spec-Driven
  - 手法/焦虑共鸣
  - 手法/对比冲突
  - 手法/权威背书
nodes: [ADR架构决策记录, PRD三件事, BDD-Cucumber双轨, 闭环执行, Linter强制, 知识资产化, Context-Compaction, Spec-Driven, Agent-Governance]
links: [[01-ai-agents/AI-团队协作-Loop-SDD-digest]], [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[01-ai-agents/agent-skills-systematic-survey]]
date: 2026-07-01
source: 微信公众号（编译自 Michal Cichra AI Engineer 大会演讲）
source_url: https://mp.weixin.qq.com/s/QT71-f3OZ067XhDwrbrAtQ
---

# BDD+ADR+PRD：让 Agent 遵守规范的闭环方法

- 原文链接：https://mp.weixin.qq.com/s/QT71-f3OZ067XhDwrbrAtQ
- 一手来源：Michal Cichra（Safe Intelligence）· AI Engineer 大会演讲 "BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike"
- 作者背景：微软 / Red Hat 十年老兵
- 抓取时间：2026-07-01

## 核心结论（一句话）

> **当 AI Agent 越来越像团队成员，"为什么"必须从模型记忆里搬进 linter / CI / 文档契约——只有"可被静态检查的规范"才能跨 20-50 次 context compaction 存活下来。**

## 分类提炼

- **场景**：AI Agent 工程治理 / 团队 AI Coding 规范
- **类型**：方法论 + 实操框架
- **受众**：技术负责人、AI Coding 重度用户、Agent 团队管理者

## 知识节点（9 个核心概念）

- **ADR 架构决策记录**：记录"为什么做这个决定"的轻量文档（Cichra 团队 50+ 条）。
- **PRD 三件事**：极简 PRD 只写"为什么存在/解决什么问题/用户怎么走"——给 Agent 看而不是给人看。
- **BDD + Cucumber 双轨**：用人类语言（Gherkin）写的产品规范同时是可执行测试，闭合"spec 写但没人验证"的循环。
- **Linter 强制执行**：把 ADR 翻译成 ESLint 规则，违规时自动指向文档——从"Wiki 范式"升级为"Compiler 范式"。
- **闭环执行**：Git Hook → CI → Linter，Agent 提交 → 拒绝 → 收到反馈+文档链接 → 自修 → 重提的飞轮。
- **Context Compaction**：单个 session 经历 20-50 次压缩，关键信息必须靠系统级文档（不是模型记忆）保活。
- **知识资产化**：把"为什么"从人脑/模型记忆里搬进 linter/文档/合同——是 Agent 时代唯一对冲知识失忆的手段。
- **Spec-Driven**：文档不只是参考资料，是 Agent 必须消费、必须遵守、必须验证的契约。
- **Agent Governance**：让"问题不可能发生"（compile-time 拦截）而不是"问题被发现"（runtime 巡检）。

## 关联图谱

### 上游（基于 / 来自）
- [[01-ai-agents/agent-skills-systematic-survey]]：本文的"技能契约化"思路与 Agent Skills 系统的"技能生命周期"互补
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]]：本文的 Linter/闭环执行可视为 Harness 工程中的 Hooks/Loop 节点在规范治理维度的具体落地

### 下游（应用于 / 验证于）
- 暂无（待 Seetong 三端 SDK 实践后补充具体落地页）

### 同级（横向 / 并列）
- [[01-ai-agents/AI-团队协作-Loop-SDD-digest]]：**最相关的同级文章**——叶小钗的 SDD（Spec-Driven Development）"6 段式 Spec 骨架"与本文的"PRD 三件事 + ADR + BDD"同源异流，前者强调组织级协作契约，后者强调工程级 Linter 强校验

## 正文要点

### 1. 5 只猴子隐喻：AI 编码是"无主规则"的复刻

经典心理学实验（Stephenson 1967）：原始猴子被替换光后，规矩依然被执行但没人能解释为什么。**AI 写代码迭代 5 轮后，处于完全一样的状态**——继承了大量"不能这么写"的反射式约束，但每条约束的"原始理由"已在 context compaction 中蒸发。

### 2. ADR 的真正革命：写可被静态检查的合同

Cichra 团队 50+ 条 ADR 定义整个产品架构。**关键不是写了多少条，而是每条都配一条 linter 规则**——违规时 ESLint 直接报"ADR-007 violated, see ..."，把治理从"Wiki 软规范"升级为"Compiler 硬约束"。

### 3. PRD 极简三件事：受众变了，文档形态必须变

受众从人扩展到 Agent 那一刻，背景故事就成了反模式。Agent 不需要 why-you-decide，只需要 what-to-build。**10 页 PRD 写得很完整但 6 周后没人会读；3 句话 PRD 才是 Agent 时代的工程交付物**。

### 4. BDD 解决"AI 写的测试读不懂"

比 AI 写代码更难的是读 AI 写的测试——前者起码能跑，后者连"测的是啥"都得猜。**Gherkin 把测试代码本身变成产品规范**，60 年软件工程最大的浪费（spec 一份、test 一份、对不上没人发现）就此闭合。

### 5. 闭环执行：让"问题不可能发生"

```
Git Hook → CI → Linter → Agent 自修 → 重提
   ↑                              ↓
   └────── 收到反馈+文档链接 ←─────┘
```

不是"发现问题"，是"让问题不可能发生"——把治理从"事后巡检"升级为"提交即拦截"。

### 6. 20-50 次压缩是知识资产化的核心动机

模型越来越强 ≠ 知识越来越稳。**压缩次数只增不减**，模型记忆注定不可靠；唯一对冲是把"为什么"放在模型之外（ADR/PRD/BDD），让系统在压缩中保活关键信息。

## 表格：四件套 + 闭环执行的依赖关系

| 层 | 工具 | 解决的问题 | 失败代价 |
|----|------|----------|---------|
| 目标 | PRD 三件事 | Agent 不知道"为谁做" | 做出技术正确但产品错位的东西 |
| 历史 | ADR + Linter | Agent 推翻历史决策 | 重新踩已知的坑 |
| 验证 | BDD + Cucumber | 测试代码变黑盒 | 测试通过 ≠ 产品正确 |
| 强制 | Git Hook → CI | 规范沦为"建议" | 47 轮压缩后规范荡然无存 |

## 案例：最小可用版本（今晚就能动手）

### 背景
新接手的 Seetong 三端 + 2 个 C/C++ SDK 团队，想给 AI Agent 写"入职文档"，但不知道从哪开始。

### 做法（4 步）
1. **新建 `docs/adr/`** — 每条决策一个 markdown，固定字段：Context / Decision / Consequences / Date
2. **新建 `docs/prd-mini.md`** — 只写 3 段：为什么存在 / 解决什么问题 / 用户怎么走
3. **挑 3 条最重要的 ADR，配 3 条 linter 规则** — 违规时报错并指向 ADR 编号
4. **BDD 暂缓** — 等团队里 Agent 写的测试越来越难读时再引入 Cucumber

### 结果
一周内能跑通"违规可被静态检查"的最小闭环；ADR 数量会自然增长，但治理负担可控。

## 我的理解

这套方法论击中了我最焦虑的问题：**知识在模型与团队之间不断蒸发**。Seetong 三端的"为什么这么写"已经没人记得清，AI Agent 接手后会更糟。

最值得抄的不是 50 条 ADR 的规模，而是 **"linter 强制" 这一招**——它把"软规范"升级为"硬约束"，从"靠人自觉"变成"靠编译器"。可以立刻用：在 Seetong iOS 项目里给"为什么不用宏""为什么 QMUI 组件统一前缀"这两条历史决策，配 clang-tidy 静态检查规则，违规直接报"ADR-XYZ violated"。

## 适合关联的主题

- [[01-ai-agents/AI-团队协作-Loop-SDD-digest]]：SDD 6 段式 Spec 骨架 + 本文的 ADR/PRD/BDD 是"组织级 + 工程级"两条 spec-driven 路径
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]]：本文的 Linter/Loop 是 Harness 工程 Hooks/Loop 节点在规范治理维度的细化
- [[01-ai-agents/agent-skills-systematic-survey]]：技能契约化的思路互补——Skill 是"怎么做"的契约，ADR/PRD/BDD 是"为什么 + 做什么 + 怎么验"的契约
