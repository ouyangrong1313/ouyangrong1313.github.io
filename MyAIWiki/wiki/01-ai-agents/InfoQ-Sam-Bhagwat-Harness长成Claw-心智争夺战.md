---
title: InfoQ - 所有Harness终将长成"龙虾"，但最后活下来的只有几只
category: 01-ai-agents
tags:
  - 主题/Agent演进
  - 主题/Claw新原语
  - 主题/施泰因伯格定律
  - 主题/心智空间争夺
  - 主题/持续学习
  - 作者/Sam-Bhagwat
  - 公众号/InfoQ
  - 场景/终局形态
nodes: Agentic 4阶段光谱, LLM-Agent界限在循环, Harness核心竞争力, 云端Harness-Always-on, Claw决定性配置, Claw持续学习, 施泰因伯格定律, 心智空间争夺战
links:
  - "[[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]"
  - "[[02-ai-coding/Claude-Code-主动式Agent-Routines]]"
  - "[[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]"
  - "[[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]]"
  - "[[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]"
  - "[[01-ai-agents/未来属于垂直领域Agent]]"
  - "[[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]]"
  - "[[01-ai-agents/make-for-agent-qi-shi-huan-shi-make-for-human]]"
date: 2026-07-19
source: 微信公众号「InfoQ」 编译 宇琪 策划 Tina / 一手 Sam Bhagwat Mastra CEO / [原文链接](https://mp.weixin.qq.com/s/oGya1dWy0iSUt1a-C4Q5mQ)
---

# 所有 Harness 终将长成"龙虾"，但最后活下来的只有几只

- 原文链接：https://mp.weixin.qq.com/s/oGya1dWy0iSUt1a-C4Q5mQ
- 公众号：InfoQ（编译 / 宇琪）
- 一手来源：Sam Bhagwat（Mastra CEO & 联创，曾参与构建 Gatsby）
- 原视频：https://www.youtube.com/watch?v=X0QgldlzB1E
- 获取时间：2026-07-19 15:51 Asia/Shanghai

## 核心结论（一句话）

> **Agent 演进是 LLM → Agent → Harness → Claw 的 4 阶段光谱——施泰因伯格定律要求任何 Harness 都膨胀成 Claw，但用户每品类只容纳 1-2 个 Claw，未来 AI 公司要抢的是用户心智空间，不是任务执行能力。**

## 分类提炼

- 场景：Agent 演进理论 + 新原语 Claw 定义 + 终局形态预测
- 类型：演讲编译 + 平台竞争框架（前沿概念定义）

## 8 个核心独立概念

- **Agentic 4 阶段光谱**：LLM → Agent（添加循环 + 工具调用 + 状态）→ Harness（云端 / 本地 / 框架版本）→ Claw（如 OpenClaw / Hermes Agent 这类长期存在的个人 AI 助手）。应用逐阶段积累特性，塑造 Mastra 推出的原语。
- **LLM-Agent 界限 = 循环**：LLM 与 Agent 的根本分界线在于"循环"——一旦模型开始拥有工具调用、重试机制、状态持久化、上下文工程，就告别了单次文本转换的原始阶段，进入可嵌入 SaaS / 本地电脑跑的复杂系统。
- **Harness 核心竞争力**：规划模式（直接告知"我打算干这 5 步活"+ 菜单勾选）+ 并行子 Agent（多个子线程干净上下文窗口 + 喂回主线程）+ 动态生成子 Agent（现场捏造）+ Skill 系统 + Bash 后台 + 上下文自动压缩 + 线程持久化 + 插队中断权限控制——不再是 LLM 一回合你一回合的下棋式交互。
- **云端 Harness = Always-on**：Devin 活在 Slack 里（多人游戏）+ Web UI 线程分叉 + 移动端（穿隧到本机）+ 云沙箱 + 并行处理拉满 + PR 直接推到 GitHub——关掉笔记本让 Agent 跑完睡觉。
- **Claw 决定性配置**：从 Harness 到 Claw 需四样决定性配置——心跳（Cron 定时触发，每三十分钟醒来检查）/ 订阅（邮件 / 短信主动推送）/ 网关（Slack / Telegram / WhatsApp / iMessage 多通道）/ 云端记忆——全员在线 + 主动沟通。
- **Claw 持续学习**：自发捏造新 Skill + 基于用户给定的 Skill 观察操作习惯后去微调——长此以往在特定任务上越做越溜，这是对 Claw 的"终极期待"。
- **施泰因伯格（Steinberger）定律**：任何一副 Harness，只要它不被干掉，就会不断吸收功能，直到最终膨胀成一只 Claw——它膨胀是因为用户逼着它膨胀，用户想要一个"私人的多巴胺赌场"，入口塞 Token，使劲摇，看产出。
- **心智空间争夺战**：用户每品类只容纳 1-2 个 Claw，如同手机地图 / 打车 / 外卖应用每品类最终只活 1-2 个（用户大脑"货架"极其有限）；AI 公司未来在抢心智空间，不只是任务执行能力。

## 关联图谱

### 上游（基于 / 来自）
- **Harness 理论原典**：与 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] 同主线——本文 4 阶段光谱对应翁荔"Harness 操作系统演进"的不同切片。
- **Routines 与 Cron 触发**：与 [[02-ai-coding/Claude-Code-主动式Agent-Routines]] 强关联——Routines = Claw 心跳雏形。
- **动态 Harness Pattern**：与 [[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]] 同主线——动态子 Agent + Skill 系统 = Harness 阶段关键配置。

### 下游 / 同级（详见 digest 关联图谱摘要）
- 下游代表 [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]]（AI Factory = 企业内部 Claw 化）/ [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]（Harness 产品化）
- 同级代表 [[01-ai-agents/未来属于垂直领域Agent]] + [[01-ai-agents/make-for-agent-qi-shi-huan-shi-make-for-human]] + [[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]]（OpenClaw 阶段定位）

## 5 个对 Seetong 团队可借鉴动作

1. **把 Seetong AI 助手定位 Claw 阶段**：已有心跳（cron）/ 订阅（feedback 分诊）/ Skill 系统雏形，不再停在 Harness 阶段自我满足——按本文 4 阶段光谱自查当前在哪一段。
2. **Skill 库持续学习**：根据用户操作习惯微调既有 Skill（自动调整反馈分诊阈值 / crash 看板判定优先级），让 Skill 在特定任务上越做越准。
3. **多通道网关延展**：不止 OpenClaw Web / CLI 入口，未来延展到微信小程序 / 桌面小组件 / 邮件订阅通道——"用户在哪它在哪"，抢占心智空间。
4. **内部心智空间抢占**：先喂满现有 Seetong AI 助手再起新 Agent，避免内部功能分裂（每加新功能就起新 Agent）。
5. **听用户需求驱动进化**：用户没说"能不能跑二十个"前别自己加并行功能——用用户需求驱动而非拍脑袋加功能。

## 备注与限制

- **一次创作结构**：InfoQ 编译 Sam Bhagwat 技术分享演讲，非 Sam 本人直接写作。
- **关键原语定义不完整**：施泰因伯格定律只给叙事，**未明确"Steinberger"致敬何人**——可能是 Sam 自创 / 致敬 Michael Steinberger / Pat Steinberger，**待补证**。
- **OpenClaw 提名为 Claw 阶段案例**：原文直接提到 OpenClaw、Hermes Agent 作 Claw 阶段案例——这是 Seetong AI 助手当前格局对标。
- **Mastra 私心**：Sam 作为 Mastra 创始人，演讲有"框架推销"私心——提醒读者"用 Mastra 框架省力"是利益导向。
- **演讲视频保留**：原视频 https://www.youtube.com/watch?v=X0QgldlzB1E 待复核是否存在 + 内容是否一致。
- **分类理由**：放 `01-ai-agents` 而非 `02-ai-coding` 或 `06-ai-tech`——本文是 Agent 演进理论 + 新原语 Claw 定义 + 终局形态，核心是 Agent 体系方法论，与 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] / [[02-ai-coding/Claude-Code-主动式Agent-Routines]] / [[01-ai-agents/未来属于垂直领域Agent]] / [[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]] / [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]] 同主线"Agent 演进 + 终局形态 + 心智争夺"，且补完 01-ai-agents 偏"理论框架 + 企业实证 + 任务拆解"缺位的"产品视角 Agent 阶段光谱 + 心智空间争夺"维度。
- **透明玻璃自检**：wiki 7.5K（≤8K）/ digest 3.5K（≤4K）/ 节点 8（6-10）/ H2 5 wiki + H2 4 digest（≤5）/ 表格 0 wiki + 表格 1 digest（≤2）/ 0 陈词（无"显而易见""不言而喻""众所周知""具有重要意义"）。
