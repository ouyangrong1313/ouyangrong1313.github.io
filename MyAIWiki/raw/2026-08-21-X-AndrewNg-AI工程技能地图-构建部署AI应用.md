---
title: Andrew Ng AI 工程技能地图 - 构建与部署 AI 应用（X 长文解读）
author: Andrew Ng（@AndrewYNg）
url: https://x.com/AndrewYNg/status/2090840747738374568
acquired_at: 2026-08-22 14:56 Asia/Shanghai
clean_length: 约 1800 字 / 解读版正文（用户提供中文解读）
status: 已清洗（WebFetch 受限，采用用户提供的中文解读版本作为正文载体；原帖英文长文未二次抓取）
---

# Andrew Ng：AI Engineering Skills Map — 第 1 项：构建与部署 AI 应用

## 元信息

- **作者**：Andrew Ng（@AndrewYNg）
- **来源**：X（Twitter）长文帖
- **发布时间**：2026-08-21
- **互动数据**：点赞 5.5k+，浏览 33 万+
- **原文链接**：https://x.com/AndrewYNg/status/2090840747738374568
- **系列背景**：Andrew Ng 系统化的 AI Engineering Skills Map，来源于招聘启事分析、专家访谈和调研反馈。最高层技能：
  1. **Building and deploying AI applications**（构建与部署 AI 应用）← 本文展开
  2. Software engineering fundamentals（软件工程基础）
  3. Using coding agents（使用编码 Agent）
  4. Shaping the build（塑造构建过程）

## 为什么 AI 应用与传统软件不同？

AI 应用的输出**不可预测**——事先不知道 LLM 会输出什么，也不知道监督学习模型会做出什么预测。因此构建过程比传统软件**更具迭代性**，难以提前精确规划。优秀的 AI 工程师会反复「构建 → 检查 → 决定下一步」，基于中间结果灵活调整，从而用不可靠的 AI 组件构建出可靠的系统。

## 构建与部署 AI 应用需要掌握的 6 大能力

### 1. LLM foundations（大语言模型基础）

理解 tokenization、生成过程，知道何时可信、何时会失败；如何选择多模态模型、权衡上下文窗口内容、推理缓存命中、知识截止、reasoning effort、采样参数、工具调用等；何时需要微调或自托管模型。

### 2. Grounding models with data（用数据 grounding 模型）

给 LLM 提供高质量上下文。RAG（向量搜索）只是早期手段，现在技术菜单已大幅扩展：决定什么直接放进 prompt、什么让模型用工具按需检索；选择合适表示（向量索引、知识图谱、结构化数据上的语义层）；把文档（文本、PDF、HTML、图像）转成 LLM 可用输入，并维护干净、新鲜的数据管道。

### 3. Building agentic systems（构建 Agentic 系统）

从预定义的 workflow（固定 LLM 调用序列）到基于 agent harness 的自主系统（让 LLM 反复决定下一步）。需要选择架构（串行/并行、何时用代码/何时用 LLM）、设计 workflow 或 harness（含 fallback）、决定工具（含 MCP、CLI、沙箱）、记忆架构、长会话上下文管理、何时用多 Agent 编排。

还要把原型变成生产级、安全、可靠的 Agent，理解 guardrails、对抗输入、数据外泄等风险与治理。

同时关注前沿形态：voice agents、computer-use agents、generative UI 等。

### 4. Evaluation-driven development（以评估驱动的开发）

Andrew Ng 认为这是区分「普通」与「优秀」AI 系统构建者的最重要特质。通过严谨的 evals / 错误分析循环，系统性地把精力集中在更可能有效的方向上。

构建好评估本身就是深度技能：看 traces 和输出、做探索性数据分析、结合产品和业务洞察决定测什么；选择确定性（代码）评估、LLM-as-a-judge 还是人工介入；还要评估自己的评估方式，持续进化。让进步变得系统化，而非随机。

### 5. Operating in production（生产环境运营）

AI 软件因不可预测性、成本和延迟而与传统软件不同。需要建立可观测性、追踪性能、检测漂移、快速响应模型失败与安全事件（如对抗性 prompt injection）；回归测试和 CI/CD 需要更多统计评估，并按风险校准测试力度；还要会用模型选择优化、蒸馏/微调、简化 agentic workflow 等手段优化成本与延迟。

### 6. Machine learning foundations（机器学习基础）

现代 LLM 本身基于监督学习与强化学习。优秀的 LLM 应用构建者通常对 ML/DL 有一定深度理解。许多应用仍需要使用或训练传统 ML 模型，因此需要了解主流模型及其精度、训练速度、推理速度等权衡，以及数据工程。

bias/variance、错误分析、数据工程等经典心智模型，对处理不确定输出的系统仍然关键。

## 总结与意义

Andrew Ng 强调：成为优秀的 AI 工程师需要相当的技术深度，但每学一点都会让你更好地构建有意思的应用。软件工程基础是强有力的补充（他承诺后续会写）。

这与之前那些「Prompting 将在 6 个月内死亡」「Loops & Graphs 取代一切」的营销帖形成鲜明对比——Ng 本人在这里给出的是**更全面、更务实、更结构化的技能地图**，把 agentic systems 只作为其中一个重要组成部分，同时高度重视评估驱动、生产运营和底层基础。

## 备注与限制

- WebFetch 抓不到 X 直链（被网络策略拦），r.jina.ai 也被拦；正文采用用户提供的中文解读版本作为载体
- 原帖为 Andrew Ng 英文长文（含丰富论证），本存档为解读版而非逐字原文
- 6 大能力的具体表述以解读版本为准，原帖英文原话需后续二次抓取补全
- 「AI Engineering Skills Map」是 Andrew Ng 持续更新的系列，本文是第 1 项展开，后续会有第 2-4 项
- 「构建 → 检查 → 决定下一步」是 Ng 强调的 AI 工程核心节奏，与传统软件瀑布/敏捷流程形成鲜明对比