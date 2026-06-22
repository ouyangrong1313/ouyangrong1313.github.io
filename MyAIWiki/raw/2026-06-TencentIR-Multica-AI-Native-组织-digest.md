# 人是最慢的节点，还怎么管AI Agent？ - Digest

> 来源：https://mp.weixin.qq.com/s/tIx02ra7Y58xdchsTtzZtw
> 公众号：腾讯研究院
> 发布时间：2026-06-11
> 采访对象：张佳圆（Multica 创始人）
> 原文：[[../2026-06-TencentIR-Multica-AI-Native-组织]]

## 一句话总结

4 人 + 几十个 Agent 的 Multica 团队用一句话回答"AI Native 组织长什么样"：**人是瓶颈，去掉中间层，让一个人端到端负责从 PRD 到部署；Agent 协作只需三类角色（Orchestrator/Worker/Validator）、最多两层、多余的层级是对人类低效组织的拙劣模仿**。

## 核心观点（5 条）

1. **人是组织的瓶颈，不是 Agent**。Agent 智能已足够强，能完成复杂工作；人最多并行 3-5 件事，Agent 可并行几十件。组织效率的天花板在人的注意力带宽。
2. **Multica = Agent 的协作层，不是 Agent 本身**。模型/平台中立（Claude Code/Codex/Manus 都能跑），三个核心概念：Runtime（运行的机器）/ Agent（AI 员工）/ Agent Team（小队）+ 任务在 inbox 里等 review。
3. **Agent 设计：三类角色 + 最多两层**。Orchestrator 做任务拆分，Worker 干活，Validator 验证；层级超过两层是"对人类低效组织的拙劣模仿"。同一个 Agent 可以既是 Orchestrator 又是 Worker。
4. **组织去中间层，一个人端到端**。从 PRD → 研发 → 测试验收，整条链路同一人 handle。以前"share context → 人演绎 → share 给 AI"的中间人本质上在做低价值信息传递。
5. **核心指标是 Agent idle 率**。大部分人 Agent 每天满载 2-3 小时，闲置 20 小时；AI Native 程度 = 让 Agent 满载时间尽量接近 24 小时。

## 关键论点（按角色展开）

- **Multica 团队的"工作日"**：周一 weekly planning（Agent 准备会议和数据）+ 每天 6 点 demo 站会（review 产出，直接部署，不再 review 代码）+ 其余时间自己 + 自己的 Agent
- **人的边界**：只剩"需要和人沟通的工作"（用户运营、用户访谈），其他都是"给 Agent 配一个人做 review/监督"
- **招人标准**：**high agency**（自主主观能动性）> 背景/专业/经验。"你怎么强，能够强过 Agent 吗？"
- **多 Agent vs 单 Agent**：单 Agent 三大问题——session 长后漂移、上下文超载偏航、同一 Agent 既做裁判又做运动员的 bias
- **Agent 信息交接**：不设显式 handoff，Agent 自己去发现需要的内容（类比让人自己查 wiki 找资料，避免浓缩过程信息丢失）
- **Token 消耗**：张佳圆平均每天 2-3 亿 token，coding 多时 10 亿；Multica 平台一周消耗约 3000 亿 token
- **开源 + 商业化**：代码不是壁垒（竞品几天抄完），真正的壁垒是网络效应——用的人越多协作层价值越大

## 7 角度 × 3 钩子

### 1. 组织架构角度
- **重构**：当 Agent 能 handle 端到端链路，"人 → 中间传递人 → AI" 的模式就过时了。一个人 handle 一件事 = 去掉 context 损耗 = AI Coding 时代最经济的组织单元
- **边界**：人是 bottleneck 的判断和张瑞敏"长坂坡新解"、YC Garry Tan 的"Egalitarian + Trust by default"是同一脉络，但 Multica 把"去中间层"做到了极致（4 人+几十 Agent）
- **实验**：可以问自己——你今天做的哪件事，本质上是"context 搬运"而非"context 创造"？这件事能不能直接由你 + Agent 端到端完成？

### 2. Agent 工程角度
- **重构**：三类角色（Orchestrator/Worker/Validator）+ 最多两层 = 多 Agent 协作的"最小可用架构"。任何超过这个的都是过度设计
- **边界**：和 [[OpenClaw-vs-Hermes-多-Agent-架构设计]] 互为镜像——OpenClaw/Hermes 是"会话边界 vs 进程边界"，Multica 是"角色边界 + 层级最小化"
- **实验**：下次你设计多 Agent 系统时，先问：真的需要单独一个 Orchestrator Agent 吗？它和 Worker 是不是同一个 Agent 就够了？

### 3. 效率与瓶颈角度
- **重构**：当生产侧变得无限（Agent 可 24×7 满载），决策侧反而成为瓶颈——"决定不去做什么事情"比"决定做什么"更重要
- **边界**：呼应 [[AI-PM核心技能-观测评估与反馈闭环]] 的判断——AI 时代稀缺的是判断力，不是产能
- **实验**：用 Agent idle 率作为你的"AI Native 程度"指标——你今天为 Agent 分配的任务让它跑了几小时？如果 < 8 小时，你还没有榨干杠杆

### 4. 信任与人机协作角度
- **重构**：人和 Agent 之间的"信任"和"review" 是 AI Native 组织里**未解决的核心矛盾**。当前主流是"AI 干完我必须看一遍"——本质是 100% 信任还未建立
- **边界**：和张佳圆的"Maker Mode → Manager Mode"切换同源——人越来越多时间在 review 而非 build
- **实验**：可以刻意做一个"信任实验"——对一类低风险任务（数据查询/简单 refactor）让 Agent 直接 merge，统计 review 通过率，看看你真实的不放心阈值在哪里

### 5. 个人认知角度
- **重构**：**人的思考在 AI 时代是被低估的**——AI 给的是 P50（中位数），要 P90/P99 需要人提供独特 context；但同时人必须警惕"思考退化"——使用 AI 越多，自己的思考过程越少
- **边界**：张佳圆每天刻意写 journal，余一每天强制 30 分钟"忍受慢和无聊"——同一结论：对抗 AI 时代认知衰减的"反 AI 时刻"是必要的
- **实验**：设一个 daily journal 闹钟——每天 15 分钟写"今天我自己想清楚的一件事是什么（不借助 AI）"

### 6. 创业与产品战略角度
- **重构**：**速度本身已不再是壁垒**——所有团队都在高速迭代，慢了就没上牌桌。真正的壁垒是网络效应和"活得久"
- **边界**：呼应 [[Claude-Code一周年回顾-Boris-Cat]] 里"Agent 自主验证"——验证环节会从"人 review 代码" 变成"系统自动验证 + 人看业务结果"
- **实验**：把"速度"和"壁垒"两个词从你的 OKR 里删掉，换成"Agent idle 率"和"网络效应密度"

### 7. 决策与认知角度
- **重构**：**快速做错误决策 > 缓慢做正确决策**——犹豫导致整个组织 block，错误可以修复
- **边界**：呼应 [[54万行代码的顿悟]] 的"未来瓶颈=需求定义+架构设计"——决策速度和需求定义质量是 AI 时代创业者的两个核心能力
- **实验**：用 24 小时决策 deadline 替代"再想想"——超过 24 小时没决的事，强制先选一个方向开干，下周复盘

## 一句话金句（适合贴工作群）

- "人是组织的瓶颈，不是 Agent。"
- "建太多层级是对人类低效组织的一个拙劣模仿。"
- "供给侧生产侧变得无限之后，决定不去做什么事情更重要。"
- "快速做错误决策 > 缓慢做正确决策。"
- "只要活得足够久，就是壁垒。"
- "AI 给你吐出来的是 P50（中位数）。"

## 关联阅读

- [[../2026-06-BorisNCat-Claude-Code一周年回顾-Boris-Cat]] — Claude Code 一周年"Agent 自主验证 / Routine 异步化"，与 Multica "不再 review 代码" 同源
- [[AI-PM核心技能-观测评估与反馈闭环]] — 决策和判断力是 AI 时代稀缺资源
- [[OpenClaw-vs-Hermes-多-Agent-架构设计]] — 多 Agent 架构对比的另一条主线（会话边界 vs 进程边界）
- [[从零设计生产级-Multi-Agent-Harness]] — 多 Agent Harness 工程化全景
- [[make-for-agent-qi-shi-huan-shi-make-for-human|Make for Agent]] — Agent 产品设计的责任链、身份与上下文
- [[54万行代码的顿悟]] — 未来瓶颈 = 需求定义 + 架构设计
- [[54万行代码的顿悟-Markdown才是新编程方式]] — 范式/组织/实操三层合并
- [[AI-Coding的顿悟时刻]] — 工程师个人范式 vs 团队流程
- [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]] — 同一 AI Native 组织变革主题的另一视角

## 标签

#主题/AI-Native #主题/AI-Agent #主题/多Agent协作 #主题/组织变革 #主题/人机协作 #主题/认知衰减 #主题/创业战略 #手法/范式反思 #手法/经济反转 #公司/Multica #公司/腾讯研究院 #场景/Agent平台 #场景/小团队
