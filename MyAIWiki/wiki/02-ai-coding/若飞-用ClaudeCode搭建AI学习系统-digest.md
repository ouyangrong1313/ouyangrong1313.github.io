---
title: 若飞：用 Claude Code 搭建自己的 AI 学习系统 - Digest
category: 02-ai-coding
date: 2026-06-22
source: 微信公众号 / 架构师 JiaGouX —若飞
source_url: https://mp.weixin.qq.com/s/YScRbcLfQYJWY7QLHXWp9A
main_entry: [[若飞-用ClaudeCode搭建AI学习系统]]
---

# 若飞：用 Claude Code 搭建自己的 AI 学习系统 — Digest

## 一句话总结

**AI 学习稀缺的不是答案，缺的是一个能持续暴露问题的环境。** Claude Code 维护"学习工作台" = 4 文件 + CLAUDE.md 长期陪练规则 + 3 周节奏 + 4 验收，把"答案机"升级为"能留下能力的学习系统"。

## 速查表

**核心命题**：AI 时代学习关键 = 能不能给自己搭一个"暴露问题的系统"（不是更快解释）
**核心金句**：① AI 可以提高当场完成度，不等于提高了长期学习 ② 看懂答案和自己答出来，中间隔着一道很深的沟 ③ 答案不能提前出现 ④ 能讲出来只说明理解一部分，能换题做出来才说明能力开始长出来
**4 文件** = 学习契约/资源/错题集/测试卷（30 分钟启动）
**3 周节奏** = D1 契约 / D2 资源 / 每天故障复现 / W2 错题重练 / W3 小项目
**4 个小验收** = 24h 闭卷复述 / 换题能做 / 错误数减少 / 小项目落地
**CLAUDE.md 5 条** = 先提示→再追问→再检查→最后才揭示
**学习卡 5 元素** = 1 句话解决 + 5 概念 + 5 例子 + 3 误区 + 3 速答题
**错误记录 3 段** = 错误 + 原因 + 下次动作

## 3 个最实操的 prompt 模板

**写学习契约**（先不讲解）：> 我想学习【主题】。请先帮我建立学习契约，5 个问题（水平/用途/时间/目标/本轮不学），问完后给 3-5 阶段 + 完成标准 + 一项练习。

**筛资料**（不超 5 个）：> 我要学习【主题】，目标是【用途】。请帮我筛 3-5 资源（权威/按序/明确本轮不看），设计 7 天路径。**不要超过 5 个。**

**出测验**（答案不提前）：> 我刚学完【主题】里【具体范围】。请扮演严格考官，一次 1 道，10 分制，答错先追问不急进。**不要一次性给出答案。**

## 反直觉 5 个

1. 第一天清楚解释 ≠ 第二天复述能力（理解感 ≠ 能力）
2. 无护栏 AI 访问 = 当场表现好，被拿走后独立表现可能变差
3. 资源越多 ≠ 推进（实际可能只是不断换入口）
4. 完整回答不一定是好事（默认值要调成"先提示→再追问→再检查→最后才揭示"）
5. 目标错就走错得更快（AI 会顺着目标走，目标错了它帮你更高效地走错）

## 5 个对 Seetong 团队可借鉴动作

1. **Seetong 新人 onboarding 第一周 = "Seetong 学习契约"**（不准"看完文档"，要"能独立完成 X 模块全流程"）
2. **TAPD 需求模板加"完成标准"必填字段**（模糊表述打回，可验收表述才通过）
3. **Seetong 周报加"学习卡"+"错误复盘"两版块**（学习卡 5 元素 + 错误复盘 ≤ 3 条）
4. **OpenClaw SOUL.md 加 learning-mode 配置档**（学习任务自动切陪练规则）
5. **seetong-batch-issue-rootcause-analysis 加"答错不急进"机制**（给根因前先反问 ≥ 3 个验证性问题）

## 关联

**主条目**：[[若飞-用ClaudeCode搭建AI学习系统]]
**上游**：[[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[Agentic-Engineering-AI-Workbench]] / [[Addy-Osmani-Loop-Engineering]] / [[Claude-Code-主动式Agent-Routines]] / [[Claude-Code一周年回顾-Boris-Cat]] / [[Claude-Code之父品味不是人类护城河]]
**下游**：[[seetong-daily-briefing]] / [[seetong-tapd-version-review]]
**同级**：[[APPSO-Codex-Claude-Code-Loop-Engineering]] / [[ai-learning-expert-perspective]] / [[karpathy-knowledge-system]]

## 备注

- 速读版：核心结论 + 速查表 + 3 prompt 模板 + 反直觉 + Seetong 借鉴动作 + 关联
- 完整编译页：同目录 [[若飞-用ClaudeCode搭建AI学习系统]]
- 本文是若飞 Harness/Loop 主线"个人学习场景版"——同作者 Loop-Engineering-详解、Agentic-Engineering-AI-Workbench 的"学习场景迁移"
- 学习科学背书：Karpicke & Roediger / Dunlosky / Bastani / Bloom
