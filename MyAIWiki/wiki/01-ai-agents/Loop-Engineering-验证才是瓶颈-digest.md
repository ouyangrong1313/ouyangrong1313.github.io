---
title: Loop Engineering 的另一半:验证才是瓶颈(速读摘要)
category: 01-ai-agents
tags: [#主题/Loop-Engineering, #主题/AI-Agent, #主题/工程实践, #主题/AI评测, #主题/Agent-Loop, #主题/补完]
type: digest
date: 2026-06-18
source: 微信公众号 / 深思 SenseAI(翻译/编译) 2026-06-17
原始作者: Samuel McDonnell(@samueljmcd)
原始链接: https://mp.weixin.qq.com/s/xo6oA8gnihPG2ERGV9l4Sw
---

# Loop Engineering 的另一半:验证才是瓶颈(速读摘要)

> **一句话**:Loop 工程真正瓶颈不是生成器(编排)而是验证器(闸门)——**一个 loop = 生成器 + 验证器**;今天真正出活的是带评估闸门的封闭循环,而不是烧 token 的开放循环。

## 速查表

| 维度 | 核心命题 | 关键数字/设计 |
|---|---|---|
| Loop 二分 | 生成器 + 验证器 | 瓶颈在验证器 |
| 开放循环 | 大片探索空间 | 易变废料机,烧 token |
| 封闭循环 | 钉死步骤/评估/停止 | 今天真正出活 |
| 评估闸门 | "那个框,才是产品" | 其余都是管道 |
| 内循环 | 任务内(改→测→修→全绿) | 大多数 agent 都会 |
| 外循环 | 跨会话(SKILL.md/AGENTS.md 持久化教训) | **只搭了一半**,价值未释放 |
| 仪表化前置 | "先仪表化闸门再去扩大循环" | 否则更快生成错误答案 |
| Bun 案例 | 75 万行 Zig→Rust,11 天,99.8% 测试 | 仍未上生产(最诚实的一句话) |
| 跑分 ≠ 生产 | 验证器质量封顶产出 | 绿色 ≠ 正确 |
| 降维边界 | 写作/策略/设计/品味 验证者无法降维 | "把'自己看一眼'换了个名字" |
| 教训持久化 | 错的教训毒化之后每次运行 | 验证问题在记忆层又长出来 |

**5 个反直觉点**:① Loop 瓶颈在验证器(工具已做编排) ② 开放循环烧 token,封闭循环才出活 ③ 验证框才是产品 ④ 99.8% 跑分通过 ≠ 生产正确 ⑤ 自动化不是产出,是更快的错。

## 5 个对 Seetong 团队可借鉴动作

1. **Seetong 现有 5 步 SOP 加"评估闸门"层**:每个 step 末尾问"这一步的验证器是什么"——**没有验证器的 step 不是 step,是喷废料机**
2. **Bun 案例 → Seetong 代码移植**:iOS OC→Swift / Android Java→Kotlin 迁移用 3 层 agent(写代码/2 审查/1 反驳/修复循环),**把"99.8% 通过"作为启动条件,不是完成条件**
3. **"先仪表化再去扩循环"作为前置条件**:加 4 项指标 baseline,跑 7 天再扩量——**没有 baseline 的循环是赌博**
4. **拆 Seetong 哪些任务"有验证器"vs"没验证器"**:① 编译/单测/lint=有验证器,扩 loop 高 ② UI/策略/PRD=没验证器,扩之前先想"是不是把'自己看一眼'换名字" ③ Bug 严重度/反馈归类=灰区,需人工标 baseline
5. **写 Seetong "外循环持久化教训"原则**:Lesson 自动写进 `seetong-knowledge-base`,但**先做"教训准入 Gate"**(2 次人工确认+1 次自动复现)才准持久化,避免毒化

## 关联 + 备注

**关联**:Harness=骨架 / Loop=循环 / 闸门=验证三角 — 与 [[Harness工程AgentLoop]] [[HarnessEngineering企业级实战]] [[0xCodez-Agent-Harness-14-Steps]] [[阿里云开发者-淘宝主播Agent的Harness工程实战]] 形成完整主线 | Loop 补完篇 — [[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]] 偏编排,本文偏验证 | 评测 [[腾讯-AI-Agent-Skill-测评方案落地]] | 治理 [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] | 自进化 [[Skill-Self-Evolution]] 与 EvoSkill/SkillOpt 三学派对话 | 阿里 [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] | Claude Code [[Claude-Code一周年回顾-Boris-Cat]] / [[Claude-Code首席设计师Meaghan-Choi工作流]]

**备注**:原文英文,深思 SenseAI 翻译+补刀 | "外循环还半残"经验判断无度量 | "99.8% 通过"跑分无生产对比 | Bun "反驳层 agent"作用未拆解 | "内循环成熟"无跨模型对比
