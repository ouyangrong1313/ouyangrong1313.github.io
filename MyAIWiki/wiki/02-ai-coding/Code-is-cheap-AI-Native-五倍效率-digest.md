---
title: Code is cheap - Digest
category: 02-ai-coding
type: digest
date: 2026-07-03
source: 微信公众号「无岳」2026-07-03 推送(阿里妹导读)
tags:
  - 主题/未分类
nodes: []
---

# Code is cheap - Digest

> 代码正从稀缺资源变成可快速生成 / 验证 / 丢弃的过程产物——**Harness(人定方向,模型推进)** 是 AI Native 研发的核心工程化范式。

## 8 节点速查表 + 5 句金句

**8 节点**:
- **code-is-cheap** —— 20 天 70 万行 10 项目,代码从稀缺资源变过程产物(卫生纸)
- **harness 定义** —— 人定方向,模型推进;控制点从代码细节上移到边界/checkpoint/风险通道
- **水流理论** —— 边界(堤坝)+ checkpoint(水闸)+ 风险通道(安全通道);漫溢 vs 溃堤
- **最小混沌单元** —— 小到可检查,大到可自治;spec/codemap/new-chat 三件上下文设施
- **6 种 checkpoint 动作** —— 放行 9% / 追问 25% / **加料 47%(最高频)** / 绕道 5% / 回炉 2% / 阻止 <1%
- **5 层 safety net** —— 自验 → 自测 → 他测 → 自动化回归+巡检 → 灰度+金丝雀+一键回滚
- **复述机制** —— 实施前反 slop 收搜索空间;实施中对抗 lost-in-the-middle(recency bias 反用)
- **代码廉价化 4 层级** —— 现象(可抛弃性)→ 工作方式(高速迭代)→ 实践姿态(不看代码)→ 身份(价值迁移)

**5 句核心金句**:"代码本身,正在变得非常便宜。"/ "如果代码贵,节俭代码;如果代码廉价,节俭时间。代码是过程,不是资产。"/ "代码不再是瓷器,也不再是一次性消耗品——它是卫生纸。"/ "Harness 的粗糙定义:人定方向,模型推进。"/ "未来真正稀缺的,不是写代码的人,而是能让大模型在正确边界里大胆流动,并且把端到端结果安全收回来的人。"

## 关键数字 + 反直觉

**关键数字**:70 万行 / 20 天 / 10 项目 / 6 种 checkpoint 动作(加料 47% / 追问 25% / 放行 9%)/ 5 层 safety net / 4 层工程师迁移

**3 个反直觉点**:① 真正贵的不是代码本身,而是**写代码之前**的"读地形 + 收边界 + 反 slop" ② AI 越强,质量控制来源越靠后——从"亲手写优雅代码"迁移到"任务包 + checkpoint + 多层 safety net" ③ **加料是最高频(47%),不是放行**——人更多时候是补约束 + 追问,不是裁判

## 6 个对 Seetong 借鉴动作

1. **Harness 工程实战库**:边界+checkpoint+验证 作为新员工入职和 Tapd 任务评审 checklist
2. **水流理论用在 Seetong AI 助手**:6 种 checkpoint 动作比例透明化;模型复述目标放在尾段对抗 lost-in-the-middle
3. **最小混沌单元用在 1007107 修复**:每个 commit 一个可验单元;spec 沉淀到 docs/specs/<日期>_<功能>.md
4. **spec 持久化建仓**:TAPD 需求关联的 spec 落本地文件,跨 session 接得上;new-chat 是 clean restart 关键
5. **多层 safety net 应用到 iOS release**:5 层(单测/UI 自动化+Hooks/巡检+Crash 监控/灰度+金丝雀+一键回滚);8.3.13.4 灰度前夜清单
6. **代码作为卫生纸的边界判断**:权限/支付/安全/数据删除路径不在范围内(严格 review),其他按可抛弃处理(灰度兜底)

## 关联 + 备注

**关联**:同主线(Harness 落地)[[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]] [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] / 同主线(AI Coding 范式)[[02-ai-coding/AI-Coding的顿悟时刻]] [[02-ai-coding/54万行代码的顿悟-Markdown才是新编程方式]] / 同主线(SDD / Skill / Loop / Skills)[[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] [[01-ai-agents/Skill-Self-Evolution]] [[02-ai-coding/Addy-Osmani-Loop-Engineering]] [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]]

**备注**:70 万行 / 6 种动作占比是作者自报口径未独立验证;"代码是卫生纸" + "不看代码"都有硬边界(权限/支付/安全/数据删除路径、基础库/SDK/infra 核心、隐式 contract 多的老系统、没有灰度和回滚机制的线上改动);本文补完已有 02-ai-coding 主线缺位的"AI Native 研发范式完整方法论"维度