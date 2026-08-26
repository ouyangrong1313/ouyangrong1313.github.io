---
title: WAIC 2026 圆桌：Physical AI 是 Agentic AI 之后的下一个范式吗？
subtitle: 群核/生数/银河通用 3 位 CEO：方向共识 vs 路径分歧 vs 时间表之争
author: 苏扬/徐青阳（腾讯科技）
source_roundtable: WAIC 2026「腾讯WAIC之夜」圆桌实录（2026-07-17 上海）
date: 2026-07-20
slug: WAIC之夜-Physical-AI-下一个范式
category: 06-ai-tech
tags:
  - Physical-AI
  - 具身智能
  - 世界模型
  - Harness-Model共生
  - 数据飞轮
rating: ⭐⭐⭐
source_wechat: https://mp.weixin.qq.com/s/R13v1uVIIL9HfW4r4ezDkg
digest: "[[06-ai-tech/WAIC之夜-Physical-AI-下一个范式-digest]]"
related:
  - "[[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]"
  - "[[06-ai-tech/深思圈-消费护城河不是注意力是环境]]"
  - "[[06-ai-tech/Nikesh-Arora-模型过剩与记忆护城河]]"
  - "[[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]"
  - "[[06-ai-tech/麦肯锡-AI提效只是第一波红利]]"
  - "[[06-ai-tech/OpenAI-AI原生组织-4条工作原则]]"
  - "[[06-ai-tech/傅盛-李飞飞-机器人世界模型与人的自主性]]"
nodes: []
---

# WAIC 2026 圆桌：Physical AI 是 Agentic AI 之后的下一个范式吗？

> 微信公众号「腾讯科技」2026-07 推送
> 原文链接：https://mp.weixin.qq.com/s/R13v1uVIIL9HfW4r4ezDkg
> 一手来源：2026-07-17 上海「腾讯WAIC之夜」圆桌实录
> 主持：陈昱（云启资本）；嘉宾：黄晓煌（群核科技）/骆怡航（生数科技）/张直政（北京银河通用机器人）

## 核心命题

**Agentic AI 之后，Physical AI 正在被资本 + 政策 + 巨头同步重新定价；3 位 CEO 在"方向"上达成共识（Digital AI → Physical AI），在"路径"上明显分歧（物理仿真 vs 视频 vs 融合），在"落地速度"上分歧最剧烈——张直政给出"激进判断"：物理 AI Agent 到来会比数字 AI 大大缩短周期。**

5 句核心金句：
- "纯软件、无行业沉淀的纯 Agent，护城河会越来越薄弱"——黄晓煌
- "下一代范式……我给的是：物理世界的通用模型"——骆怡航
- "先学会交互，再从交互中持续学习——交互不是目的，是数据飞轮"——张直政
- "三种能力缺一不可：建模动作 + 促进策略 + 通用评价"——张直政
- "物理 AI 的 Agent 到来，会比数字 AI 大大缩短周期"——张直政

## 8 个核心节点

### 节点 1：范式共识 — Digital AI → Physical AI

张直政凝练："过去用 offline learning 构建 GPT；如果想构建能跟物理世界可靠交互的模型，要先把 offline learning 变成 online learning。"Digital AI Agent 是起点，Physical AI Agent 是其在物理世界的延伸，不是替代。

### 节点 2：纯软件 Agent 护城河薄弱

黄晓煌观察一年多后下注："只做纯软件、没有行业沉淀的纯 Agent，护城河会越来越薄弱。大模型基本能把软件或 Agent 直接复制出来。"结论是大模型要做，但要做在大语言模型"射程之外"——可交互的世界生成。

### 节点 3：物理仿真路线（黄晓煌 · 群核）

"世界由不可见的因素组成，用纯视觉的方式不靠谱，视觉只是欺骗人类。"群核走结构化数据 + 参数化模型的偏物理仿真路径。**关键判断**：视频路线与物理仿真 80% 工作相似，最后 20% 才在收敛点分叉。

### 节点 4：融合路线（骆怡航 · 生数 Motubrain）

"单一路线必撞瓶颈。"Motubrain 走多模态融合：视频 + 物理强化 + 本体 + Ego。架构持续演进（Diffusion Transformer / MoE 混合）。已有"类似 GPT-2 → GPT-3 → GPT-3.5 的前兆"——长程任务规划与通用性开始具备可能性。

### 节点 5：世界模型三项能力（张直政 · 银河通用）

行业里很多定义不完整。三项能力缺一不可：(1) **建模动作对状态的改变**（无论像素空间还是 latent space）；(2) **以建模促进策略学习**（更快学会技能 + 更可信输出动作）；(3) **通用评价能力**（行业盲区：环境改变好不好？动作结果是不是想要的？）。

### 节点 6：Harness-Model 共生与 One Model One System

"Harness 是数据飞轮，Model 是能力支撑，二者不可分。"与 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] "5 段优化路径 prompt→上下文→工作流→harness 代码→optimizer 代码"在终局判断上同主线。**激进结论**："One Model One System"——Harness 最终被内化进模型，Digital AI 与 Physical AI 会大一统（"空间智能是 Physical AI 的一个子集"）。

### 节点 7：数据难题 = 物理世界数字化

"Coding 落地好 = 数字化高；自动驾驶落地好 = 在行驶中自动采集数据。"要解决物理 AI，最首要的是让物理世界信息尽可能进入数字世界——怎样规模化、低成本、批量把整个"宇宙"采集起来。**类比反向适用于 Seetong**（设备现场报警/录像的数字化程度 = 物理 AI 落地效果的卡点）。

### 节点 8：激进判断 — limited space + 全面通用

张直政的"激进乐观"：物理 AI 落地逻辑 ≠ "像人什么都能干"，而是"在有限范围里追求全面通用"——自动驾驶（驾驶场景里的通用）/ 银河通用"太空舱"（特定工厂产线）/ 特殊空间技能（落地的通用）。**结论**：物理 AI 落地门槛没那么高，Agent 到来会比数字 AI 大大缩短周期。

## 关联图谱

**上游**：黄仁勋 CES 2026-01（"物理 AI 的 ChatGPT 时刻即将到来"是引子）；WEF 2026 初 + 德勤《2026 技术趋势》（物理 AI 已准备好主流部署的外部印证）；李飞飞 World Labs Marble 估值 10 亿→50 亿（圆桌对照案例）；市场规模（全球具身智能 2025 ~44.4 亿 → 2030 230 亿美元；中国 2035 突破万亿元）。

**下游**：机器人企业落地节奏；Three capability world model 工程化；One Model One System 终局进度。

**同级**：方法论对偶 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]；战略对偶 [[06-ai-tech/Nikesh-Arora-模型过剩与记忆护城河]]；样本对偶 [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]；数据洞察对偶 [[06-ai-tech/深思圈-消费护城河不是注意力是环境]]；组织战略对偶 [[06-ai-tech/麦肯锡-AI提效只是第一波红利]] / [[06-ai-tech/OpenAI-AI原生组织-4条工作原则]]；机制补充 [[06-ai-tech/傅盛-李飞飞-机器人世界模型与人的自主性]]（物理数据、世界模拟、行动规划与反馈闭环）。

补充视角：[[06-ai-tech/腾讯科技-席宁-机器人学习物理世界数据与模型融合]] 将圆桌中的“仿真 vs 视频 vs 融合”路线讨论，落到数据学习与有限状态机、动力学、运动学等物理先验的知识融合问题。

## 6 个对 Seetong 团队可借鉴动作

1. **设备协同 4 维体检**：iOS/Android/Harmony/云端 + Seetong AI 助手 + SDK 六维是否真协同？每月 4 人共识检视
2. **数据难题**：神策 `AlarmMessage` 是否覆盖"现场物理状态"？不补永远卡在屏幕里看图
3. **Harness-Model 检查**：Seetong AI 助手每个 Skill 是否配 Harness（批准/分流/协调/限定动作 4 种最小 Agent 模式）？
4. **Three capability 体检**：最缺"通用评价能力"（多数 Skill 是生成类而非评价类）
5. **limited space 借鉴**：挑 1 个场景（4G IPC 多分屏/报警消息列表/配网失败处理）半年内 AI 化
6. **季度复盘 Physical AI 在监控/对讲/报警小场景的渗透**

## 备注与限制

- 数据时效：嘉宾路径分歧仅代表 2026-07-17 时点观点
- 二手报道：腾讯科技为公众号，非嘉宾本人书面确认
- 3 类二手数字待独立验证：44.4 亿 / 万亿元 / Marble 10 亿→50 亿——嘉宾口播未给具体出处
- 3 家"准上市或上市"具体进度未在原文展开
- 圆桌实录有删减，可能漏掉具体案例与反驳
- 透明玻璃自检：wiki ≤ 8K / digest ≤ 4K / 节点 8 / H2 5 / 表格 0 + 1 / 0 陈词 / 0 称呼违规 / 全角标点
- 标签 #主题/Physical-AI #主题/具身智能 #主题/世界模型 #主题/空间智能 #主题/Harness-Model共生 #主题/数据飞轮 #主题/limited-space-通用 #主题/One-Model-One-System #主题/中国AI战略 #手法/圆桌访谈 #场景/WAIC-2026 #公众号/腾讯科技 #公司/群核科技 #公司/生数科技 #公司/银河通用
