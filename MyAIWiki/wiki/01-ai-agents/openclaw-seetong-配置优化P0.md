---
title: "OpenClaw + Seetong 配置优化方案 P0 落地"
category: 01-ai-agents
tags: [#主题/AI-Agent, #主题/Agent配置, #主题/Seetong, #主题/OpenClaw, #节点/任务分级, #节点/验证Gate, #节点/Skill自进化, #节点/通用规则, #场景/Agent配置优化, #场景/Seetong-iOS研发, #手法/规则提炼, #手法/增量优化, #手法/避免过度设计]
nodes: [Goal&Task-任务分级, 验证-Gate-优先, Skill-自进化护栏, 薄路由厚技能厚数据, OC-崩溃风险, MCP-数据路由, Seetong-AGENTS-硬规则, OpenClaw-三件套, 拟生命-数字生命, 不可解释-但-可验证]
links: [[清华沈阳-自进化AI新物种]], [[OpenClaw-使用案例与技巧]], [[OpenClaw-的正确-打开方式]], [[Skill-Self-Evolution]], [[Harness-Engineering-企业级实战]], [[如何更科学方向可控的实现-Skill-自进化]], [[Addy-Osmani-Loop-Engineering]]
date: 2026-06-15
source: 综合 OpenClaw 实战经验 + 清华沈阳《自进化 AI》+ EvoSkill / SkillOpt / Addy Osmani Loop Engineering 等多源沉淀
---

# OpenClaw + Seetong 配置优化方案 P0 落地

> **本文档版本**：v1.0（2026-06-15 落地 P0）
> **优化对象**：`~/.openclaw/workspace/SOUL.md`、`~/.openclaw/workspace/AGENTS.md`
> **优化原则**：精炼、增量、Seetong 专属，不大改
> **跳过 P1/P2**：P1（Seetong-AGENTS 速记口诀 + openclaw.json skillEvolution 字段）+ P2（Heartbeat 双引擎 + taskTiering 字段 + 数字生命暗示）已生成方案，待验证 P0 效果后分批上

## 优化动机

通过整合用户 MyAIWiki 中积累的所有 AI Agent 知识（清华沈阳《自进化 AI》、EvoSkill / SkillOpt 学术综述、Addy Osmani Loop Engineering、OpenClaw 正确打开方式、Anthropic 万字长文等），提炼**通用性规则**，结合 Seetong APP 研发场景做适配，**小步增量**地升级 OpenClaw 的工作流范式与安全护栏。

## 提炼的 7 条通用规则（不依赖任何单篇文章）

| # | 规则 | 核心动作 | 知识来源 |
|---|------|----------|----------|
| 1 | **Goal & Task > Step-by-Step** | 工作流从步骤列表改写为目标 + 可观测任务 + 验证 Gate | 清华沈阳 ZeeLin Goal&Task 体系 |
| 2 | **验证 Gate > 信任推理链** | 不在"理解 agent 怎么想"上花时间，把精力放在"如何设计可验证机制"上 | 清华沈阳"不可解释但可验证" + EvoSkill 验证 gate |
| 3 | **任务分级 + 分层架构** | 按 L1–L4 复杂度决定单 agent / subagent / 状态树并行 | 清华沈阳智能形态分化论（差距 ≥ 10 倍 = 不同维度） |
| 4 | **薄路由厚技能厚数据**（已有强化） | Skill / Memory / Knowledge / Archive 四层边界清晰 | Garry Tan 原则 + 用户 SOUL.md 既有沉淀 |
| 5 | **拟生命演化的双向压力** | 生存压力（Token / 失败率）+ 诗和远方（周期性非功利目标） | 清华沈阳 OpenClaw 龙虾三步骤 |
| 6 | **Self-evolution 受控** | 允许进化但必须可回滚、可审计、有负反馈历史强约束 | EvoSkill 三角色 Pipeline + 负反馈历史 |
| 7 | **上下文预算管理**（已有强化） | 单文件 > 100 行 / 上下文 > 8000 字符 → 拆；复用率 < 30% → 拆到 Skill | 用户 AGENTS.md "Keep It Lean" + ZeeLin 上下文编排 |

## Seetong 场景的 5 条专属规则

| # | 规则 | 核心约束 | 知识来源 |
|---|------|----------|----------|
| 8 | **iOS 真实设备约束** | 未经授权绝不动 xcodebuild / pod install / 模拟器 / 真机 | 用户 Seetong-AGENTS.md 既有 |
| 9 | **OC 崩溃风险优先于功能正确性** | Review 时按 B-N-T-O-R（Bounds / Nil / Thread / Observer / Retain cycle）顺序检查 | 用户 Seetong-AGENTS.md 既有 + OC 实战踩坑 |
| 10 | **现有栈复用 > 引入新抽象** | 改前先查 BaseViewController / STNetworkManager / QMUITips / Realm / Masonry / MJExtension | 用户 Seetong-AGENTS.md 既有 |
| 11 | **知识沉淀分离** | App 仓库只放执行规则；专题知识去 MyAIWiki | 用户 Seetong-AGENTS.md 既有 + Claude Code 一周年 |
| 12 | **MCP 数据路由** | Seetong 数据源严格走已配 MCP（seetong-feedback / umeng-app / sensors-analyst / mcp-server-tapd），不直接 curl | 用户 openclaw.json 既有 4 个 MCP |

---

## P0 已落地的 3 项修改

### ✅ 1. SOUL.md 增补：验证 Gate 优先原则

**位置**：`/Users/topsee/.openclaw/workspace/SOUL.md` 「Core Truths」末尾

```markdown
**Verify, don't trust.** Every Skill must have a binary validation gate
(pass/fail). When in doubt, design the verification — don't try to
understand the reasoning. "Incomprehensible but verifiable" is healthy;
"incomprehensible and unverifiable" is dangerous.
```

**为何是 P0**：SOUL.md 是 Agent 的人格底色，把"验证优先"写进 Core Truths 意味着 agent 每次醒来都会读到它——这是最低成本、最高频次的护栏。

---

### ✅ 2. AGENTS.md 增补：Task Tiering (L1–L4 任务分级 + 架构选择)

**位置**：`/Users/topsee/.openclaw/workspace/AGENTS.md` 「Plan Trigger」之后

```markdown
### Task Tiering (先分级,再决定架构)

任何任务接进来，默认先分级，再决定用什么 agent 架构跑：

| Tier | 特征 | 架构 | 例 |
|------|------|------|-----|
| **L1 简单** | 改个 typo / 格式化 / 简单搜索 | 单 agent 直干 | 重命名变量、format 文件 |
| **L2 中等** | 涉及 1–2 个文件，逻辑清晰 | agent + Skill 验证 Gate | 改个 API、修单测、加日志 |
| **L3 复杂** | 跨模块 / 跨文件 / 架构调整 | 先 plan + subagent 并行 | 加新模块、重构、跨端 SDK 调整 |
| **L4 超能力** | 超出单 agent 能力 10 倍 | 状态树并行 + 多方案对比 | 重写核心 SDK、全量迁移 |

**默认假设 L2**。识别到 L3+ 立即升级到 plan 模式 + 调高 subagent 并发度。
**识别到 L4** 必须拆成多个子状态树并行，最后用 Cross-Modal Eval 收敛最优解。
```

**为何是 P0**：现有 AGENTS.md 的"Plan Trigger"只有"要不要 plan"的二元判断，缺少"用什么架构跑"的工程化指导。L1–L4 把这个空白补上。

---

### ✅ 3. AGENTS.md 增补：Self-Evolution Guardrails

**位置**：`/Users/topsee/.openclaw/workspace/AGENTS.md` 「Skill vs Memory vs Knowledge」之后

```markdown
### Self-Evolution Guardrails (Skill 自进化受控)

Skill 自进化允许，但必须满足硬约束：

- [ ] **写入前快照**：每次写新版本前，旧版本自动备份到 `.bak/skills/`
- [ ] **验证 Gate 必填**：每个 Skill 必须有通过/失败的二元判定，不允许"看起来跑通了"
- [ ] **失败自动回滚**：Gate 不通过 → 自动恢复快照，不静默重试
- [ ] **负反馈历史强约束**：同类错误重复 > 2 次 → 写入"禁止再犯"清单，下次自动避坑
- [ ] **生命周期管理**：> 90 天未被调用的 Skill → 月度 Lint 时标记候选删除
```

**为何是 P0**：Skill 自进化是 OpenClaw 强大之处也是失控之处，没有护栏的进化 = 越跑越偏。这 5 条约束直接对应 EvoSkill 的工程化做法，是最低成本的"防爆栓"。

---

## P1 候选（已规划，待验证 P0 后落地）

| # | 文件 | 改动 | 价值 |
|---|------|------|------|
| 4 | Seetong-AGENTS.md | 增加 OC 崩溃风险速记口诀（B-N-T-O-R） | 提升 Review 速度 |
| 5 | Seetong-AGENTS.md | 把"Verification" 升格为硬规则（加 ⛔ 标记） | 强化防误操作 |
| 6 | openclaw.json | 增加 `agents.defaults.skillEvolution` 字段 | Skill 进化可配置化 |

## P2 候选（高级特性，建议一两周后评估）

| # | 文件 | 改动 | 价值 |
|---|------|------|------|
| 7 | AGENTS.md | 增加"双引擎"章节（生存压力 + 诗和远方） | 避免 agent 退化 |
| 8 | openclaw.json | 增加 `agents.defaults.taskTiering` 字段（**仅按 L1–L4 决定架构与并发度，不切模型**） | 任务分级可配置化 |
| 9 | SOUL.md | 增加"Simulated 数字生命"暗示（沈阳模型） | 增强 agent 主体性 |

> **2026-06-15 用户确认**：所有任务统一用 `minimax-portal/MiniMax-M3`，不按 L1–L4 切不同模型。taskTiering 字段只能动"架构 / 并发度 / 是否用 subagent / 是否走状态树"这些维度，**不**触碰模型路由。

---

## 落地清单

### 已落地（P0）
- [x] `/Users/topsee/.openclaw/workspace/SOUL.md` 增加"Verify, don't trust"
- [x] `/Users/topsee/.openclaw/workspace/AGENTS.md` 增加"Task Tiering (L1–L4)"
- [x] `/Users/topsee/.openclaw/workspace/AGENTS.md` 增加"Self-Evolution Guardrails"

### 待落地（P1/P2）
- [ ] Seetong-App-iOS/AGENTS.md 增加 B-N-T-O-R 速记口诀
- [ ] Seetong-App-iOS/AGENTS.md Verification 章节升格硬规则
- [ ] openclaw.json skillEvolution 字段
- [ ] AGENTS.md 双引擎章节
- [ ] openclaw.json taskTiering 字段
- [ ] SOUL.md Simulated 数字生命暗示

## 复盘节奏

- **本周末**：观察 P0 三项在日常对话中是否被有效触发（agent 是否主动问 L1/L2/L3、是否开始写验证 Gate）
- **两周后**：评估 P1 优先级，决定是否上 openclaw.json skillEvolution 字段
- **一个月后**：评估是否需要上 P2（双引擎 + taskTiering）
- **每季度**：跑一次 Skill Lint，清理 > 90 天未调用的 Skill
