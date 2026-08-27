---
title: Anthropic AI-Native SDLC：用版本化产物重构软件开发流程
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 主题/AI-Native研发
  - 主题/SDLC
  - 主题/Spec驱动
  - 主题/验证驱动
  - 主题/Harness
  - 场景/公众号长文
nodes: [代码两侧瓶颈, 提交产物, 产物触发器, 意图规格计划, 策略分层, 受保护验证, CI-Eval, 人类门禁]
links: [[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]], [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]], [[02-ai-coding/宝玉AI-我的AI原生开发流程-真实案例复盘]], [[02-ai-coding/研发工程化升级-Coding-Agent-AI-Testing与Verification-First]], [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]]
date: 2026-08-26
source: 微信公众号「Founder Park」对 Anthropic 手册的编译
---

# Anthropic AI-Native SDLC：用版本化产物重构软件开发流程

- 原文链接：https://mp.weixin.qq.com/s/YeAL7XBmltR4n3rUnz3Pag
- 来源：Founder Park；文中称编译 Anthropic《The AI-Native SDLC Playbook》
- 获取时间：2026-08-27

## 核心结论（一句话）

> 当代码生成不再是主要约束，研发流程应围绕可提交、可审查、可消费的产物重构：人类在意图、规格、计划与高风险门禁上决策，Agent 在受控范围内实施、验证和回流证据。

## 分类提炼

- 场景：AI-Native 软件研发、SDLC 重构、Agentic Coding 治理
- 类型：流程手册 / 研发治理 / Anthropic 实践二手解读
- 标签： #主题/AI-Coding #主题/AI-Native研发 #主题/SDLC #主题/Spec驱动 #主题/验证驱动 #主题/Harness #场景/公众号长文

## 知识节点

- **代码两侧瓶颈**：Agent 加速构建后，规划、测试、审查、部署和运维仍按人速运行，会决定整体吞吐。
- **提交产物**：`intent.md`、`spec.md`、`plan.md`、代码/测试、PR 与事故记录既是阶段输出，也是下游可执行输入和审计依据。
- **产物触发器**：通过审核的产物自动启动下一阶段，使流程从人工转交的线性链改为可回流的循环。
- **意图规格计划**：Intent 固定问题和约束，Spec 固定需求与设计，Plan 固定改动、顺序、风险和验证方式，错方向尽量在代码前暴露。
- **策略分层**：Skill 用于可变的组织知识和一致性；Hook/CI 用于必须确定执行的限制，避免把安全边界只寄托在提示词上。
- **受保护验证**：Agent 需要可执行的构建、测试或行为检查；修复任务中测试不可被同一执行者弱化，否则通过不构成证据。
- **CI-Eval**：近期真实任务和生产事故应沉淀为 Eval，在模型、Prompt、Skill 或 Agent 配置变化时持续检查工作标准。
- **人类门禁**：人类保留意图、风险、策略冲突、代码所有权和上线决定；注意力从逐次编辑确认转移到审查被标注的关键产物。

## 关联图谱

### 上游（基于 / 来自）

- [[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]：讨论 Spec、Plan 和圆桌审查怎样把 AI 研发从单次生成变为可审查流程。
- [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]]：将代码廉价化后的控制点定位在边界、checkpoint 与多层安全网。

### 下游（应用于 / 验证于）

- [[02-ai-coding/研发工程化升级-Coding-Agent-AI-Testing与Verification-First]]：把受保护验证和 CI-Eval 落到 Agent 研发的测试/验证体系。
- [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]]：用 Skills 将机构知识作为可分发、可版本化的执行约束。

### 同级（横向 / 并列）

- [[02-ai-coding/宝玉AI-我的AI原生开发流程-真实案例复盘]]：本文是组织级 SDLC Playbook，宝玉文章是个人 App 功能从可行性到黑盒验收的同构流程。

## 正文要点

1. 传统 SDLC 的控制目标仍然成立，但逐行审查、人工交接和低频委员会是为人类编码速度设计的。Agent 加快实现后，若不改造两侧流程，只会堆积审查与合规队列。
2. 每一个阶段的结尾应提交一份事实产物。下一阶段与 Agent 从产物读取，而不是从口头背景或临时聊天继续；这条提交链同时保留谁提出、谁生成、谁批准的证据。
3. 规划阶段从自然语言想法形成 `intent.md`；设计阶段根据现行策略生成 `spec.md`；构建阶段先在 Plan Mode 形成 `plan.md`，再授权执行。人不替 Agent 写这些产物，但要审查其中的判断。
4. `CLAUDE.md`、Skill、Hook 和子 Agent 不是堆配置：前两者承载新人需要的知识和可变策略，Hook 承担确定性禁止项，子 Agent/工作树用于边界清晰的并行任务。
5. 测试阶段将真实任务和事故做成持续 Eval，PR 审查聚焦行为与风险。发布和运维的线上信号应重新成为下一份 intent 的输入，形成从事故到流程改进的闭环。
6. 最小落地顺序是先选一个痛点明显的阶段，建立模板、验证和人工门禁；手动跑通“产物通过 → 下一阶段启动”后，再自动化触发器与 Agent 自主度。

## 备注

- 原文所称 Anthropic Playbook 的发布日期、内部实践和示例没有在本次归档中逐项对照一手材料。
- 版本化产物和分层治理可跨工具迁移；文中的 Claude Code、`.claude`、GitHub Actions 仅代表一种实现，不是架构前提。
- AI-Native 不表示取消人类审查，而是将人的注意力移到更高杠杆、更难自动验证的判断上。

## 相关链接

- [[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]
- [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]]
- [[02-ai-coding/宝玉AI-我的AI原生开发流程-真实案例复盘]]
- [[02-ai-coding/研发工程化升级-Coding-Agent-AI-Testing与Verification-First]]
