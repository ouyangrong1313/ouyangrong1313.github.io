---
title: AI 原生工作法：Codex 负责人谈团队新的工作模式
category: 03-productivity
tags:
  - 主题/AI时代工作方法
  - 主题/AI原生团队
  - 主题/Codex-OpenAI
  - 主题/Agent优先
  - 主题/工作方法论
  - 主题/多线程任务管理
  - 主题/工程师新角色
  - 场景/Seetong借鉴
  - 作者/AI组织进化论
nodes: [十个要点短规格, Codex参与思考, 多线程管理任务, 工程师建设环境, AGENTS.md是地图, 计划只做两种, 角色边界模糊责任不模糊, 用户是开发系统一部分, 招聘看做过什么]
links: [[06-ai-tech/OpenAI-AI原生组织-4条工作原则]], [[03-productivity/LaterCast-Netflix产品技术负责人-AI时代更需要系统型人才]], [[03-productivity/LaterCast-YC设计负责人-AI重写设计师工作流]], [[03-productivity/笔记侠-十布-这-是以后的工作方式]], [[03-productivity/笔记侠-苏姿丰-MIT演讲-工程师本能]], [[03-productivity/WonderLearner-Alice-Claude-Code之父的新洞察-揭示AI对团队岗位的真正冲击]], [[01-ai-agents/harness-engineering]], loop-engineering
date: 2026-07-21
source: 微信公众号「AI组织进化论」2026-07-21（一手 Peter Yang 访谈 OpenAI Codex 负责人 Alex + 开发者体验负责人 Romain / 原文 https://mp.weixin.qq.com/s/5EMMIaXwJm6SL7nYcCoi0g）
---

# AI 原生工作法：Codex 负责人谈团队新的工作模式

- **原文链接**：https://mp.weixin.qq.com/s/5EMMIaXwJm6SL7nYcCoi0g
- **来源**：AI组织进化论 / 2026-07-21

## 核心结论

> **Codex 团队围绕 Agent 重新设计工作：少写长文档 + AI 参与思考准备 + 多线程管理任务 + 工程师建设环境 + AGENTS.md 是地图 + 招聘看作品**——从"写代码"变成"管理数字同事的工作台"。

## 知识节点

### 1. 十个要点短规格
- 复杂项目说明通常只写十来个要点，文档不像描述执行步骤，而是澄清意图 + 验收标准

### 2. 先让 Codex 参与思考，再让它执行
- 先让 Codex 读项目、提选项、问目标用户/优先级；AI 负责读取/补充/暴露遗漏，人负责判断真正问题与取舍

### 3. 多线程管理任务
- 1 人可以让 1 个 Agent 实现功能、1 个检查代码、1 个排查安全，同时再启动 1 个线程理解陌生模块

### 4. 工程师建设环境
- Agent 缺工具/抽象/内部结构就无法从高层目标推进到可靠结果；失败时要追问"Agent 缺少什么能力"而不是只返工

### 5. AGENTS.md 是地图
- 巨大文档会挤占上下文并迅速过时；AGENTS.md 改成目录，知识分层放在架构/设计/计划/质量/安全等文档

### 6. 计划只做两种
- 短期最长约 8 周，长期看模型能力可能走到哪里，不写死中期——中间要给团队留下调整空间

### 7. 角色边界模糊，责任不能模糊
- 设计师写代码、PM 做原型、工程师做产品判断；**AI 削弱的是"这不是我的工作"，不是"这件事没人负责"**

### 8. 用户是开发系统的一部分
- 团队自己用 → 用户深度用 → 新用法出现 → 产品吸收 → 再次交付，开源进一步缩短反馈距离

### 9. 招聘看"你做过什么"
- 先看作品链接与主动性；技术正在从职业边界，变成实现想法的公共能力

## 关联图谱

### 上游
- Peter Yang 访谈（OpenAI Codex 团队 Alex + Romain）
- OpenAI 内部"Agent 优先工程"复盘：Harness Engineering

### 下游
- 企业级 Agent 团队组织设计 / AI 原生团队工作流 / Agent 工程化

### 同级（横向）
- [[06-ai-tech/OpenAI-AI原生组织-4条工作原则]] 同主线 AI 原生组织
- [[03-productivity/LaterCast-Netflix产品技术负责人-AI时代更需要系统型人才]] 系统型人才 + 平台 80%
- [[03-productivity/LaterCast-YC设计负责人-AI重写设计师工作流]] 设计师 AI 工作流
- [[03-productivity/笔记侠-十布-这-是以后的工作方式]] AI 原生组织实战（影刀）
- [[03-productivity/笔记侠-苏姿丰-MIT演讲-工程师本能]] 工程师本能 4 关键词
- [[03-productivity/WonderLearner-Alice-Claude-Code之父的新洞察-揭示AI对团队岗位的真正冲击]] 5 类角色原型
- [[01-ai-agents/harness-engineering]] 工程化主线 / loop-engineering 验证主线

## 6 个对 Seetong 借鉴动作

1. **短规格替代长文档**：SKILL.md 强制 ≤ 200 行 + 关键节点 bullets 表达
2. **AI 参与思考准备**：加 1 个"探索模式"，用户输入模糊想法时 AI 先提问题澄清
3. **多线程管理任务**：6 个 cron 评估互不依赖的并行可能
4. **工程师新工作 = 建设环境**：70/30 写代码 vs 维护环境 → 6 个月内调整到 50/50
5. **AGENTS.md 是地图不是百科全书**：大块内容迁到 skill 目录，AGENTS.md 只保留"目录 + 入口"
6. **4 条普通团队可复制原则**：任务说明 / Agent 可找系统 / 反馈回路 / 围绕问题任务而非职能

## 备注与相关链接

- **一手**：Peter Yang 访谈 OpenAI Codex 产品负责人 Alex + 开发者体验负责人 Romain
- **未独立验证**：4 条普通团队原则未在 Codex 之外团队验证；"短期 8 周 + 长期判断"是 Codex 内部节奏未给公开依据
- **本批对比**：与 [[06-ai-tech/OpenAI-AI原生组织-4条工作原则]] 形成"宏观原则 + 具体执行"对偶；与 [[03-productivity/LaterCast-Netflix产品技术负责人-AI时代更需要系统型人才]] 同"AI 原生团队"主线

- [原文链接](https://mp.weixin.qq.com/s/5EMMIaXwJm6SL7nYcCoi0g)
- [How OpenAI's Codex Team Builds with Codex](https://www.youtube.com/watch?v=9qXc-THAvc0)
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
- [[06-ai-tech/OpenAI-AI原生组织-4条工作原则]] / [[01-ai-agents/harness-engineering]] / loop-engineering