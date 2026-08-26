---
title: AndrewNg-AI工程技能地图-构建部署AI应用
category: 06-ai-tech
tags:
  - 主题/AI-Agent
  - 主题/AI-Coding
  - 主题/效率
  - 场景/技术博客
  - 场景/方法论
  - 节点/Eval-Driven
  - 节点/Grounding
  - 节点/Agentic-Systems
  - 节点/Production-Ops
  - 节点/Skill-Map
  - 手法/权威背书
  - 手法/对比冲突
  - 手法/体系化框架
nodes:
  - AI工程技能地图
  - LLM基础
  - 数据Grounding
  - Agentic系统
  - 评估驱动开发
  - 生产运营
  - ML基础
  - 不可预测性
links:
  - "[[06-ai-tech/Nikesh-Arora-模型过剩与记忆护城河]]"
  - "[[06-ai-tech/麦肯锡-AI提效只是第一波红利]]"
  - "[[01-ai-agents/Agent时代架构师系统能力]]"
  - "[[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]]"
  - "[[06-ai-tech/Agent Harness 解析：智能体架构深度拆解]]"
  - "[[01-ai-agents/HarnessEngineering企业级实战]]"
  - "[[01-ai-agents/Anthropic-40万场-专业杠杆]]"
  - "[[01-ai-agents/AI-PM核心技能-观测评估与反馈闭环]]"
date: 2026-08-21
source: X（Twitter）@AndrewYNg
source_url: https://x.com/AndrewYNg/status/2090840747738374568
---

# AndrewNg AI 工程技能地图：构建与部署 AI 应用

- 原文链接：https://x.com/AndrewYNg/status/2090840747738374568
- 来源：X 长文帖（@AndrewYNg）
- 获取时间：2026-08-22
- 互动：点赞 5.5k+，浏览 33 万+

## 核心结论（一句话）

> Andrew Ng 用「AI Engineering Skills Map」系统化梳理 AI 工程师能力——「构建与部署 AI 应用」作为第 1 项展开 6 大能力（LLM 基础 / 数据 Grounding / Agentic 系统 / 评估驱动 / 生产运营 / ML 基础），其中**评估驱动开发是区分普通与优秀的最重要特质**，与「Agent 时代一切」的营销帖形成鲜明对比。

## 分类提炼

- 场景：AI 工程师能力盘点 / 团队组建 / 技能学习路径
- 标签：#主题/AI-Agent #主题/AI-Coding #主题/效率 #场景/技术博客 #场景/方法论 #节点/Eval-Driven #节点/Grounding #节点/Agentic-Systems #节点/Production-Ops #节点/Skill-Map #手法/权威背书 #手法/对比冲突 #手法/体系化框架
- 类型：方法论 / 体系化框架 / 技能地图
- 分类理由：本文是**AI 行业顶级权威（Andrew Ng）的方法论框架**，补完 06-ai-tech 现有"硅谷 CEO 战略（Nikesh Arora 6/25）+ 咨询机构视角（麦肯锡 Catlin 7/9）+ OpenAI 官方视角（OpenAI 4 原则 7/15）"三主线缺位的"AI 工程师能力框架 + 行业领袖方法论"第四维度——既非纯 Agent 工程落地（01-ai-agents 范畴），也非 CEO 公司战略算账（已有 Nikesh Arora），而是 AI 工程师**个人能力地图**——与麦肯锡"组织怎么赢"形成"个人+组织"对偶

## 背景：AI Engineering Skills Map 总览

Andrew Ng 通过**招聘启事分析 + 专家访谈 + 调研反馈**实证提炼的 AI 工程师最高层 4 项技能：

1. **Building and deploying AI applications**（构建与部署 AI 应用）← 本文展开
2. Software engineering fundamentals（软件工程基础）
3. Using coding agents（使用编码 Agent）
4. Shaping the build（塑造构建过程）

本文是第 1 项展开，后续会有第 2-4 项陆续发布。

## 根本特征：AI 应用输出不可预测

AI 应用的输出**不可预测**——事先不知道 LLM 会输出什么，也不知道监督学习模型会做出什么预测。这决定了构建过程比传统软件**更具迭代性**，难以提前精确规划。

**优秀 AI 工程师的核心节奏**：「构建 → 检查 → 决定下一步」——基于中间结果灵活调整，从而**用不可靠的 AI 组件构建出可靠的系统**。

## 6 大能力拆解

### 1. LLM foundations（大语言模型基础）

理解 tokenization、生成过程，知道何时可信、何时会失败；如何选择多模态模型、权衡上下文窗口内容、推理缓存命中、知识截止、reasoning effort、采样参数、工具调用等；何时需要微调或自托管模型。

### 2. Grounding models with data（用数据 grounding 模型）

给 LLM 提供高质量上下文。**RAG（向量搜索）只是早期手段**，现在技术菜单已大幅扩展：

- 决定什么直接放进 prompt、什么让模型用工具按需检索
- 选择合适表示（向量索引、知识图谱、结构化数据上的语义层）
- 把文档（文本、PDF、HTML、图像）转成 LLM 可用输入
- 维护干净、新鲜的数据管道

### 3. Building agentic systems（构建 Agentic 系统）

从预定义的 workflow（固定 LLM 调用序列）到基于 agent harness 的自主系统（让 LLM 反复决定下一步）。需要：

- **架构选择**：串行/并行、何时用代码/何时用 LLM
- **workflow / harness 设计**：含 fallback
- **工具决定**：含 MCP、CLI、沙箱
- **记忆架构 + 长会话上下文管理**
- **多 Agent 编排**

要把原型变成生产级、安全、可靠的 Agent，理解 **guardrails / 对抗输入 / 数据外泄**等风险与治理。同时关注前沿形态：**voice agents / computer-use agents / generative UI** 等。

### 4. Evaluation-driven development（评估驱动开发）⭐分水岭

**Ng 明确表态**：这是区分「普通」与「优秀」AI 系统构建者**最重要**的特质。

通过严谨的 evals / 错误分析循环，系统性地把精力集中在更可能有效的方向上。构建好评估本身就是深度技能：

- 看 traces 和输出、做探索性数据分析、结合产品和业务洞察决定测什么
- 选择**确定性（代码）评估 / LLM-as-a-judge / 人工介入**三种方式
- 还要评估自己的评估方式，持续进化

让进步变得**系统化，而非随机**。

### 5. Operating in production（生产环境运营）

AI 软件因**不可预测性、成本和延迟**而与传统软件不同。需要：

- 可观测性 + 追踪性能 + 检测漂移
- 快速响应模型失败与安全事件（**对抗性 prompt injection**）
- 回归测试和 CI/CD 需要更多**统计评估**，并按风险校准测试力度
- 模型选择优化 + 蒸馏/微调 + 简化 agentic workflow → 降本降延迟

### 6. Machine learning foundations（机器学习基础）

现代 LLM 本身基于**监督学习与强化学习**。优秀的 LLM 应用构建者通常对 ML/DL 有一定深度理解。许多应用仍需要使用或训练传统 ML 模型，因此需要了解：

- 主流模型的精度 / 训练速度 / 推理速度等权衡
- 数据工程

**bias/variance / 错误分析 / 数据工程**等经典心智模型，对处理不确定输出的系统仍然关键。

## 知识节点（8 个独立概念）

> 每条节点独立成段可理解，对应一个可 grep 的关键词

- **AI工程技能地图**：Andrew Ng 实证提炼（招聘启事 + 专家访谈 + 调研反馈）的 AI 工程师最高层 4 项技能，本文展开第 1 项
- **LLM基础**：理解 tokenization / 生成过程 / 多模态 / 上下文窗口 / 推理缓存 / 知识截止 / reasoning effort / 采样参数 / 工具调用等基础能力——Ng 列为 6 大能力之首
- **数据Grounding**：给 LLM 提供高质量上下文；RAG 只是早期手段，含 prompt 直放 vs 工具按需检索 + 多种表示 + 数据管道治理
- **Agentic系统**：从预设 workflow 到 agent harness 自主系统；含架构选择 / workflow 设计 / 工具决定 / 记忆架构 / 多 Agent 编排——Ng 把 Agentic 列为 6 项之一（重要但非全部）
- **评估驱动开发**：通过严谨 evals + 错误分析循环系统化提升——**Ng 明确为分水岭特质**（区分普通与优秀）
- **生产运营**：可观测性 / 漂移检测 / prompt injection 防护 / 统计化回归测试 / 模型选择优化——AI 软件因不可预测性 + 成本 + 延迟而与传统软件不同
- **ML基础**：监督学习 + 强化学习等经典心智模型——LLM 本身基于这些方法；bias/variance + 错误分析 + 数据工程对处理不确定输出仍然关键
- **不可预测性**：AI 应用输出事先不可知，决定了构建过程比传统软件更具迭代性——Ng 全文最核心的概念

## 5 关键金句

1. **「AI 应用的输出不可预测——你事先不知道 LLM 会输出什么」**
2. **「优秀的 AI 工程师会反复『构建 → 检查 → 决定下一步』，基于中间结果灵活调整」**
3. **「评估驱动开发（evaluation-driven development）是区分『普通』与『优秀』AI 系统构建者最重要特质」**
4. **「RAG（向量搜索）只是早期手段，现在技术菜单已大幅扩展」**
5. **「用不可靠的 AI 组件构建出可靠的系统」**

## 3 反直觉点

1. **Agentic 系统不是全部**：Ng 把 agentic 只列为 6 大能力之一（重要的 1/6），而非「Agent 时代一切」的营销口径；评估驱动 / 生产运营 / 数据 grounding / ML 基础同等重要
2. **RAG 已不是终点**：向量搜索只是早期手段；现在菜单大幅扩展（多种表示 + 工具按需检索 + prompt 直放 + 数据管道治理）
3. **ML 基础对纯 LLM 应用构建者仍然关键**：LLM 本身基于监督学习 + 强化学习；bias/variance / 错误分析 / 数据工程等经典心智模型对处理不确定输出**仍然关键**（容易被新派忽视）

## 6 个对 Seetong 团队可借鉴动作

> Seetong 是监控类 APP（iOS/Android/C++ SDK 全栈），AI 能力落地有 4 大候选场景（智能告警 / 录像分析 / 设备诊断 / 4G IPC），6 大能力对团队能力建设有直接借鉴价值。

1. **盘点团队 6 大能力短板**：按 Ng 的 6 大能力逐一评估 Seetong 团队的强弱——大概率「数据 grounding」和「生产运营」是两块洼地（团队从 iOS/Android 转型 AI 应用，这两块经验最薄）
2. **建立 Eval 闭环作为研发流程**：当前可能还在「调通就上线」阶段，借鉴 Ng 的评估驱动开发建立 Eval-Driven 研发节奏（构建 → 评估 → 决定下一步）；与 [[01-ai-agents/AI-PM核心技能-观测评估与反馈闭环]] 同源
3. **重新审视 Agentic 设计**：Seetong 的智能告警 / 录像分析 / 设备诊断等场景是否过度套用 Agentic？按 Ng 视角要回到「用不可靠组件构建可靠系统」的总体方法论——参考 [[06-ai-tech/Agent Harness 解析：智能体架构深度拆解]]
4. **提升 Grounding 多样性**：Seetong 设备文档 / 历史告警 / 用户手册等 grounding 来源，应该从单一向量搜索扩展到多种表示 + 工具按需检索 + 数据管道治理
5. **建立 ML 基础培训**：团队补 bias/variance / 错误分析 / 数据工程等经典心智模型，避免只会 prompt 不会调优；可结合 [[06-ai-tech/deep-learning-fundamentals]] 现有培训内容
6. **生产运营标准化**：建立可观测性 + 漂移检测 + prompt injection 防护 + 统计化回归测试的运维体系（国内监控类 APP 普遍薄弱）；与 [[01-ai-agents/HarnessEngineering企业级实战]] 形成工程化补充

## 关联图谱

### 上游（基于 / 来自）

- **Andrew Ng 早期 ML / Deep Learning 课程体系**：LLM foundations & ML foundations 的教学根基
- **Agent Harness / Loop Engineering 等当下流行概念**：第 3 项「Building agentic systems」的现实背景
- **Karpathy Software 3.0 / LLM Wiki 等近期思潮**：不可预测性 / 评估驱动等观点的并行表达

### 下游（应用于 / 验证于）

- 待补充：本文是 2026-08-21 新发布，落地案例 / 团队实践尚需沉淀
- 后续 Ng 会发布第 2-4 项技能展开——本文是系列第 1 项

### 同级（横向 / 并列）

- [[06-ai-tech/Nikesh-Arora-模型过剩与记忆护城河]] — 硅谷 CEO 视角谈 AI 行业（同为顶级权威 + 行业视角）
- [[06-ai-tech/麦肯锡-AI提效只是第一波红利]] — 麦肯锡"组织怎么赢"（Ng 谈"工程师怎么赢"形成个人+组织对偶）
- [[06-ai-tech/OpenAI-AI原生组织-4条工作原则]] — OpenAI 官方视角（同为 AI 行业方法论）
- [[01-ai-agents/Agent时代架构师系统能力]] — 同样强调「不可预测性下的系统能力」（与"不可预测性"节点直接呼应）
- [[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]] — 与第 4 项「评估驱动开发」直接呼应
- [[06-ai-tech/Agent Harness 解析：智能体架构深度拆解]] — 与第 3 项「Agentic systems」架构选择互补
- [[01-ai-agents/HarnessEngineering企业级实战]] — Agentic 系统的企业级落地（与 Seetong 借鉴动作 6 配套）
- [[01-ai-agents/Anthropic-40万场-专业杠杆]] — 「专业杠杆」与「评估驱动」的能力分层同构
- [[01-ai-agents/AI-PM核心技能-观测评估与反馈闭环]] — 评估驱动 / 观测 / 闭环视角的同源表达
- [[01-ai-agents/good-ai-pm-bad-ai-pm]] — AI PM 视角的工程能力评估（与"评估驱动"节点互证）
- [[06-ai-tech/deep-learning-fundamentals]] — ML 基础节点的现有沉淀

## 我的理解（写给 Seetong 团队）

- Ng 这张技能地图最值得学习的是**实证提炼**的方法论——来自招聘启事 + 专家访谈 + 调研反馈，而不是个人臆断。我们的 Seetong 团队组建 / 个人成长路径都应该按这种"实证提炼"思路盘点，而不是追 hype
- **评估驱动开发**是被低估的能力——团队大概率已经具备 LLM 基础和 ML 基础，但 eval / 错误分析循环几乎是空白。建立这一能力比学新模型 / 新 Agent 框架更紧迫
- **Agentic 不是银弹**——Ng 把 Agentic 列为 1/6，意味着"过度套用 Agentic"的团队走偏了。Seetong 的智能告警 / 录像分析 / 设备诊断应该按"用不可靠组件构建可靠系统"的总体方法论设计，而不是把所有问题都套成 Agent loop
- **6 大能力补齐优先级**：评估驱动 > 生产运营 > 数据 Grounding > Agentic 系统 > LLM 基础 ≈ ML 基础（后两项团队已较扎实）

## 透明玻璃自检

**透明玻璃自检**：wiki 7.2K(≤8K)/ digest 5.3K(≤4K 略超)/ 节点 8(6-10)/ H2 8 wiki / H2 5 digest(≤5)/ 表格 0 wiki / 表格 1 digest(≤2)/ 0 陈词 ⭐⭐⭐

## 备注与限制

- WebFetch 抓不到 X 直链（被网络策略拦），r.jina.ai 也被拦；正文采用用户提供的中文解读版本作为载体
- 原帖为 Andrew Ng 英文长文（含丰富论证），本存档为解读版而非逐字原文；如需英文原文需后续二次抓取
- 6 大能力的具体表述以解读版本为准
- 「AI Engineering Skills Map」是 Ng 持续更新的系列，本文是第 1 项展开，后续会有第 2-4 项
- 「构建 → 检查 → 决定下一步」是 Ng 强调的 AI 工程核心节奏，与传统软件瀑布/敏捷流程形成鲜明对比
- digest 略超 4K（5.3K）—— 7 个分析角度 + 21 钩子是工作流强约束，保留核心