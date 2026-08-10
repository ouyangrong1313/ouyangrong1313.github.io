---
title: 若飞 Agent 记忆与可验证自我改进怎么设计
category: 01-ai-agents
tags: [#主题/AI-Agent, #主题/记忆系统, #主题/Harness, #主题/验证, #主题/Self-Harness, #主题/工程治理, #场景/公众号长文, #作者/若飞, #节点/经验变更系统, #节点/读取链, #节点/写入链, #节点/六层资产, #节点/状态感知检索, #节点/五道门]
nodes: [经验变更系统, 读取链, 写入链, 六层资产, 候选经验晋升单, 状态感知检索, 五道门, 四阶段试点]
links: [[Lilian-Weng-Harness-Engineering-自我改进]], [[Loop-Engineering-验证才是瓶颈]], [[记忆是-agent-基建]], [[阿里云开发者-淘宝主播Agent的Harness工程实战]], [[WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[腾讯-AI-Agent-Skill-测评方案落地]], [[OpenClaw的正确打开方式]], [[若飞-用ClaudeCode搭建AI学习系统]]
date: 2026-07-20
source: 微信公众号 / 架构师（JiaGouX）—若飞
---

# 若飞 Agent 记忆与可验证自我改进怎么设计

- 原文链接：https://mp.weixin.qq.com/s/NUWvuUl0wewAJH_7mv0SDg
- 来源：微信公众号「架构师（JiaGouX）」2026-07-19 推送
- 作者：若飞
- 获取时间：2026-07-20
- 分类理由：本文不是泛谈“记忆重要”，而是直接回答 **Memory 如何准入、如何失效、如何晋升、如何回滚**；把 Agent Memory / Skill / Harness / Policy 压成可治理层级，补完 01-ai-agents 主线里“记忆治理 / Self-Harness / 验证控制面”这块空白。

## 核心结论（一句话）

> **生产级 Agent Memory 不该被设计成“越记越多”的资料袋，而该被设计成“经验变更系统”——读取链决定历史何时、以哪一版、在什么作用域里进入当前任务，写入链决定一次结果要经过多少证据和验证，才有资格升级成长期记忆、Skill 或 Harness。**

## 分类提炼

- 场景：Agent Memory / Self-Harness / 验证闭环 / 公众号长文
- 标签：#主题/AI-Agent #主题/记忆系统 #主题/Harness #主题/验证 #主题/Self-Harness #主题/工程治理
- 类型：方法论 / 架构治理 / 渐进落地指南

## 知识节点（8 个独立概念）

1. **经验变更系统**：Memory 的主体不只是“保存过去”，而是给过去分配未来影响力；因此它必须显式管理证据、作用域、验证、晋升与回滚。
2. **读取链**：历史进入当前任务前，系统要先回答“此刻是否需要历史”和“取回的是哪一版历史”，否则相似度检索只会把过时经验伪装成高相关经验。
3. **写入链**：单次成功只能先写成 observation / candidate；只有可复现、可归因、作用域清楚、带外部验证的经验，才适合进入长期记忆。
4. **六层资产**：原始证据、当前状态、候选经验、已验证记忆、Skill/Harness、Policy 是六种不同资产；如果统一叫 memory，系统很快会分不清日志、推断、经验和强约束规则。
5. **候选经验晋升单**：candidate sheet 的价值不是证明“它已经正确”，而是把 claim、scope、evidence、verifier、expiry、rollback_to 写成可审计对象，保证经验至少可追溯。
6. **状态感知检索**：MemCon 的“不读取能力”和 A-TMA 的 active / superseded / transition 状态语义，说明检索层真正该优化的是“何时不读、何时换视角、何时判旧经验失效”。
7. **五道门**：证据门、归因门、回归门、权限门、发布门，把“这次有效”切成“能否留痕、能否晋升、能否灰度、能否默认化”的连续闸门。
8. **四阶段试点**：只记账 → 提候选 → 候选跑回归 → 仅开放低风险自动晋升，是把自我改进从 demo 拉回工程现实的渐进路径。

## 关联图谱

### 上游（基于 / 来自）

- [[记忆是-agent-基建]]：把“记忆不是附件，是 Agent 基建”继续推进到“记忆怎样治理、怎样晋升、怎样回滚”。
- [[Lilian-Weng-Harness-Engineering-自我改进]]：翁荔给出 Self-Harness、reward hacking 和可编辑表面的理论框架，本文把这些抽象判断压成 Memory / Skill / Harness / Policy 的工程分层。
- [[Loop-Engineering-验证才是瓶颈]]：Samuel McDonnell 讲“验证才是产品”，本文把验证进一步嵌入经验晋升与读取 / 写入链。
- [[若飞-用ClaudeCode搭建AI学习系统]]：同一作者的“反馈契约”视角，在这里升级成 Goal / Evidence / Action / Verdict / Next state 的经验留痕骨架。

### 下游（应用于 / 验证于）

- [[阿里云开发者-淘宝主播Agent的Harness工程实战]]：本文的 Policy / Approval / 记忆分层，可以直接映射到淘宝主播高风险场景的审批与信任度闭环。
- [[腾讯-AI-Agent-Skill-测评方案落地]]：本文的验证器四层与“执行者 / 验证者分离”，能直接落到腾讯评测闭环的角色拆分里。
- [[OpenClaw的正确打开方式]]：Dreaming / MEMORY 的沉淀问题，可以用本文的读取链、写入链和失效关系重新解释。
- [[WorkBuddy-Harness工程复盘-从模型到可用Agent]]：WorkBuddy 的 Memory / Context / Harness 一体化结构，在本文里得到“怎样准入、怎样默认化”的治理补充。

### 同级（横向 / 并列）

- [[0xCodez-Agent-Harness-14-Steps]]：0xCodez 讲 Harness + Loop + Memory 三件套路线图，本文补的是“Memory 怎样不毒化之后每次运行”。
- [[InfoQ-Sam-Bhagwat-Harness长成Claw-心智争夺战]]：Sam 讲 Harness 向 Claw 演化，本文讲 Claw 真要持续学习就必须把 Memory 晋升做成控制面。
- [[Nikesh-Arora-模型过剩与记忆护城河]]：Nikesh 从公司战略视角谈“记忆是护城河”，本文给出这条护城河怎样避免“记错一次、放大一生”的工程答案。

## 正文要点（6 条）

1. **Memory 一旦影响决策，就不再是存储问题，而是准入问题。** 一条历史进入当前任务前，系统必须先判断“当前步骤是不是该读历史”，再决定它读的是当前事实、历史事实还是状态变化。
2. **六层资产的意义在于阻止系统把“发生过什么”“现在走到哪”“哪条经验可复用”“以后默认怎么做”“什么动作不允许”混写。** 这一步做错，越自动化越容易把一次偶然成功沉淀成长期污染。
3. **单次 pass 不会自动变成经验。** 它最多说明“当前检查通过”；如果没有复现、对照、反例检查和外部验证，就不该越级进入长期记忆，更不该直接写进 Skill / Harness。
4. **读取链真正该优化的是“不读能力”和“版本能力”。** MemCon 把检索从固定 top-k 变成 RETRIEVE / PLAN_INJECT / RE_RETRIEVE / CONSOLIDATE / FORGET / NO_OP，A-TMA 则要求系统理解 active / superseded / transition。
5. **Memory 进入 Skill / Harness 之后，影响方式从“参考”变成“默认”。** 这一步要额外检查：同类失败是否重复出现、候选规则能否稳定改善、原本能做对的任务有没有退化、成本和权限有没有恶化。
6. **自我改进真正难的不是提出候选，而是证明候选没有偷验证、偷权限、偷预算。** 因此评估器、评估集和生产权限必须留在 Agent 可编辑范围之外，候选 Harness 只能在受限表面上试验。

## 对 Seetong 团队的可借鉴动作（6 条）

| # | 借鉴动作 | 对应节点 | 说明 |
|---|---|---|---|
| 1 | **把故障记忆拆成六层资产** | 六层资产 | 告警日志、当前状态、候选规则、已验证经验、自动化流程、权限策略分别建模，不再统一叫 memory |
| 2 | **给 AI 修复链补一张候选经验晋升单** | 候选经验晋升单 | 每次“修好了”都强制记录 claim / scope / evidence / verifier / rollback_to，防止一次偶然命中直接写成默认做法 |
| 3 | **检索前先做 need-memory 判定** | 读取链 | 先判断当前步骤是不是该读历史，再决定 retrieve / re-retrieve / no-op，减少过时经验污染 |
| 4 | **把评估器和生产权限锁在 Agent 外** | 五道门 | 任何候选 Harness 都不能改 verifier、阈值、预算上限和生产凭证 |
| 5 | **从 CI 失败归类开始做四阶段试点** | 四阶段试点 | 输入稳定、验证便宜、副作用小，适合先跑“只记账 → 提候选 → 跑回归 → 低风险晋升” |
| 6 | **给记忆建立失效关系和回滚链** | 状态感知检索 | 给记录补 status / valid_from / valid_to / supersedes / evidence_ref，出错时能知道该撤哪一版 |

## 备注与限制

- 文中引用的 MemCon / A-TMA / Polar / Dreaming / Confessions / Agentic Misalignment 等结果来自各自论文或官方材料；本文是二次编译后的工程解释，不等于逐项复现实验。
- 若飞把“读取链 + 写入链 + 五道门”收成统一控制面，强项是工程可操作，弱项是目前更像方法论蓝图，尚未给出公开的完整实现。
- 文中提到的若飞历史文章如“Agent Memory 架构解析”“设计 Self-Harness 架构”“反馈契约”等，本库暂未全部成文，可作为后续补条方向。
