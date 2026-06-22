---
title: Loop Engineering 的另一半:验证才是瓶颈
category: 01-ai-agents
tags: [#主题/Loop-Engineering, #主题/AI-Agent, #主题/工程实践, #主题/AI评测, #主题/AI安全, #主题/Agent-Loop, #场景/方法论, #场景/补完]
nodes: [Loop-生成器-验证器二分, 开放循环-封闭循环, 评估闸门才是产品, 内循环-外循环分层, 仪表化前置原则, Bun-75万行-移植案例, 跑分-生产鸿沟, 验证者-降维边界]
links: [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[APPSO-Codex-Claude-Code-Loop-Engineering]], [[Harness工程AgentLoop]], [[HarnessEngineering企业级实战]], [[0xCodez-Agent-Harness-14-Steps]], [[阿里云开发者-淘宝主播Agent的Harness工程实战]], [[腾讯-AI-Agent-Skill-测评方案落地]], [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]], [[Skill-Self-Evolution]]
date: 2026-06-18
source: 微信公众号 / 深思 SenseAI(翻译/编译) 2026-06-17 13:25
原始作者: Samuel McDonnell(@samueljmcd)
原始链接: https://mp.weixin.qq.com/s/xo6oA8gnihPG2ERGV9l4Sw
---

# Loop Engineering 的另一半:验证才是瓶颈

> **核心结论**:Loop 工程的真正瓶颈不是生成器(编排),而是验证器(闸门)。**一个 loop = 生成器 + 验证器,瓶颈从来在验证器这一侧**——设计编排现在简单,工具基本替你做了;还难、还得手动、还真正决定结果的是评估闸门。
>
> agent 时代的管理 = 设计约束(验证闸门),和管人是同一件事。**别再设计提示词,去设计验证者**。

## 8 个知识节点

- **Loop 二分 = 生成器 + 验证器**:一个 loop 由生成器(generator)和验证器(verifier)组成,**生成器从来不是瓶颈,验证器才是**。这是被 2026 年所有 loop engineering 叙事藏起来的那一半。
- **开放循环 vs 封闭循环**:开放循环给大片探索空间(真正新颖的产出来自这里,但烧 token + 评判一松变废料机);封闭循环钉死步骤/评估/停止条件,能在正常预算下跑完。**今天真正能出活的是封闭循环**——评估闸门挡住"自信的错误答案"传下一轮。
- **"那个框,才是产品"**:大部分讲循环画"发现-规划-执行-验证"图,但没人对"验证"框说具体。**验证框才是产品,其余的都是管道**。
- **内循环 vs 外循环**:内循环(任务内:改完→写测试→跑→修边界→全绿)大多数 agent 都会做;外循环(跨会话:失败教训持久化到 SKILL.md/AGENTS.md,下次会话读到从一开始做对)**只搭了一半**——把对的教训、用对的颗粒度、写到对的地方,比听起来难得多,大量价值正摊在这块桌子上没人捡。
- **"先仪表化闸门再去扩大循环"**:你没法改进一个你没在测量的循环。**先把闸门仪表化(可观测、可量化),再去扩大循环**——否则你只是在更快地生成错误答案。
- **Bun 75 万行 Zig → Rust 移植案例**:Jarred Sumner 用 Claude Code 动态工作流移植,11 天合并(Anthropic 数据)/ 6 天(Sumner 自述),**99.8% 现有测试通过**;每个文件配两个审查 agent + 独立"反驳层"agent + 修复循环驱动编译测试。**验证不是最后一步,验证就是整个架构**。
- **跑分 ≠ 生产的鸿沟**:Anthropic 自家公告附注"这个移植还没上生产"——Samuel 说"这是整个发布里最诚实的一句话"。**产出的质量被验证器的质量封顶,一分都高不上去**——99.8% 通过跑分 = 复现旧测试,生产 = 没人写过测试的行为。
- **验证者的降维边界**:"设计验证者"在你能写出验证者的地方是金科玉律(代码有测试/编译能过/lint 能跑);但在写作/策略/设计/品味这些"验证者无法降维成自动闸门"的领域,**你以为在搭循环,其实只是把"自己看一眼"换了个名字**;外循环的"持久化教训"判断哪条对也是验证问题——一条错的教训被持久化下来,会毒化之后每一次运行。

## 关联图谱

### 上游(基于 / 来自)
- **Boris Cherny 2026 六月大会讲话**:Claude Code 负责人 Boris 自述已不写提示词,管理几百到上千 agent——loop engineering 叙事引爆点
- **Addy Osmani Loop Engineering 5+1 积木**:工具链已基本覆盖编排(简单的那半)
- **Claude Code 动态工作流 / Meaghan Choi worktree 并行 + 自动巡逻**:Loop 工程实现

### 下游(应用于 / 验证于)
- **Bun 75 万行 Zig→Rust 移植案例**(Jarred Sumner 2026-06):11 天 / 99.8% 测试通过 / 仍未上生产——验证"评估闸门封顶产出"主张

### 同级(横向 / 并列)
- 既有 Loop 主线(本文是"**补完篇**",它们讲编排,我讲验证):[[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]]
- 既有 Harness 主线(**Harness=骨架 / Loop=循环 / 闸门=验证**,本文补完"闸门"侧):[[Harness工程AgentLoop]] / [[HarnessEngineering企业级实战]] / [[0xCodez-Agent-Harness-14-Steps]] / [[harness-engineering]] / [[阿里云开发者-淘宝主播Agent的Harness工程实战]]
- 评测主线:[[腾讯-AI-Agent-Skill-测评方案落地]] 测评是 Demo→生产必须跨过的门槛
- 治理薄壳:[[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] Loop 范式 8 个真痛点
- 自进化:[[Skill-Self-Evolution]] 外循环的持久化教训与 EvoSkill/SkillOpt 三大学派直接对话
- Claude Code 一手 + 阿里业务:[[Claude-Code一周年回顾-Boris-Cat]] / [[Claude-Code首席设计师Meaghan-Choi工作流]] / [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]

## 5 个对 Seetong 团队可借鉴动作

1. **Seetong 现有 5 步 SOP 加"评估闸门"层**:`seetong-bug-triage` / `seetong-tapd-version-review` / `seetong-daily-briefing` / `seetong-prd` 每个 step 末尾加"这一步的验证器是什么"——**没有验证器的 step 不是 step,是喷废料机**。
2. **Bun 案例思维实验 → Seetong 代码移植**:iOS OC→Swift / Android Java→Kotlin 迁移用 3 层 agent(写代码 / 2 审查 / 1 反驳 / 修复循环),**但把"99.8% 通过"作为启动条件,不是完成条件**;必须补 5-10 个"生产场景测试"(真实崩溃堆栈/慢启动场景)才算跑通。
3. **"先仪表化再去扩循环"作为前置条件**:`seetong-batch-issue-rootcause-analysis` / `seetong-daily-briefing` 加 4 项指标(分群准确率/根因命中率/小时级延迟/人工二次确认率),先跑 7 天收集 baseline,再去扩量。**没有 baseline 的循环是赌博**。
4. **拆 Seetong 哪些任务"有验证器"vs"没验证器"**:① 编译/单测/lint = 有客观验证器,扩 loop 价值高(参考 Bun) ② UI/策略/PRD 文档 = 没验证器,扩之前先想"是不是把'自己看一眼'换名字" ③ Bug 严重度/反馈归类 = 灰区,需先小批量人工标 baseline,跑通评测后再扩 loop。
5. **写 Seetong "外循环持久化教训"原则**:`seetong-bug-triage` 跑出的"3 天内复现 2 次根因 X"等 Lesson 自动写进 `seetong-knowledge-base`(对应 [[ai-personal-knowledge-base-problems]]),但**先做"教训准入 Gate"**(2 次人工确认 + 1 次自动复现)才准持久化,避免毒化之后运行。

## 备注与限制

- 原文英文,深思 SenseAI 翻译+补刀,核心 90% 来自 Samuel McDonnell
- 深思圈"补刀"价值极高(写作/策略/品味 + 外循环"教训持久化"递归)
- "外循环还半残"经验判断,未给"还差多少"度量
- "99.8% 通过"是跑分,Anthropic 未给"生产测试覆盖率"对比
- Bun "独立反驳层 agent"实际起多大作用未给拆解
- "内循环成熟"未给跨模型对比
- 原文:https://mp.weixin.qq.com/s/xo6oA8gnihPG2ERGV9l4Sw
- raw:[../../raw/2026-06-17-深思SenseAI-Loop-Engineering-验证才是瓶颈.md](../../raw/2026-06-17-深思SenseAI-Loop-Engineering-验证才是瓶颈.md) | digest:[./Loop-Engineering-验证才是瓶颈-digest.md](./Loop-Engineering-验证才是瓶颈-digest.md)
