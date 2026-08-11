---
title: Datawhale - Claude Code 之父的老板，坦白 Agent 协作方法
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/AI-Coding
  - 场景/公众号长文
  - 节点/Agent-Loop
  - 节点/Harness
  - 节点/AI-Native
  - 节点/Claude-Code
  - 节点/Spec-Driven
nodes: [验证取代编写, spec入仓, TDD回归, 跨角色验证, Agency-Accountability, Bad-Sad分级, Motion-vs-Progress, Routines异步调度, Switching-Cost-Unresolved, IC优先]
links: [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]], [[02-ai-coding/Claude-Code首席设计师Meaghan-Choi工作流]], [[02-ai-coding/Claude-Code一周年回顾-Boris-Cat]], [[02-ai-coding/Claude-Code-主动式Agent-Routines]], [[03-productivity/WonderLearner-Alice-Claude-Code之父的新洞察-揭示AI对团队岗位的真正冲击]], [[02-ai-coding/Addy-Osmani-Loop-Engineering]], [[01-ai-agents/ThinkingAgent-Knock-AI-Native组织5级成熟度模型]], [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]], [[03-productivity/Laurel-CPO-Jiaona-Zhang-公司OS]], [[03-productivity/快刀青衣-OpenAI高管教练四层能力]]
date: 2026-07-06
source: 微信公众号 / Datawhale（编译 Lenny's Podcast 访谈 Fiona Fung）
source_url: https://mp.weixin.qq.com/s/c9Vkx_2l2PRSY__GjUlHuQ
original_source: https://www.youtube.com/watch?v=Ybrl4FYM57c
---

# Claude Code 之父的老板，坦白 Agent 协作方法：他们做对的，和还没解决的！

## 核心结论（一句话）

> **Anthropic 工程师人均代码产出涨到 8 倍，靠的不只是模型变强，还有一整套配套的协作方法论——把"什么算好"写进 spec，把自由和责任绑定，把管理者的日常判断模板化成可以自动运行的 Routine，把新晋管理者先按回 IC 的位置；但这套方法论并不完整——协作中的孤独感用结伴编程午餐缓解却没有真正解决，并行 Agent 带来的切换负荷 Fiona 自己说"还没搞定"。**

## 分类提炼

- **场景**：AI Native 团队 Agent 协作方法论（Claude Code 团队实战）
- **类型**：方法论 + 实战案例 + 自我反思（罕见的"承认没解决"诚实访谈）
- **一句话定位**：Claude Code 团队的"动作清单 + 没解决的清单"双视角

## 知识节点（10 个独立概念）

- **验证取代编写**：核心动作从"做出来"变成"判断做得对不对"，跨角色重复出现的规律
- **spec 入仓**：把"什么算好"写成 spec 检入代码仓库，Claude 做 code review 时对照 spec 校验
- **TDD 回归**：测试驱动开发因 AI 分担执行工作重新变得容易坚持（Fiona 自嘲像"先吃西兰花"）
- **跨角色验证**：PM 不再受工程带宽限制可自己实现，数据科学家从"做分析"变成"审核 AI 生成的半错分析"
- **Agency-Accountability**：高 Agency 必须绑定高 Accountability——自由不是放手，是绑定责任
- **Bad-Sad 分级**：Bad=严重不可恢复错误；Sad=可恢复但影响体验问题；定义权下放各组
- **Motion-vs-Progress**：不在衡量工具使用量，衡量的是"行动是否推动想要的结果"
- **Routines 异步调度**：Claude Code 远程会话常驻仓库/Slack/仪表盘；Routines 每天固定时间运行自动生成 PR
- **Switching-Cost-Unresolved**：并行 Agent 带来的切换负荷 Fiona 自己说"还没搞定"
- **IC 优先**：新晋管理者先以个人贡献者身份工作一段时间；她自己加入第一周改用 Claude 提问替代请工程师喝咖啡

## 关联图谱

### 上游（基于 / 来自）

- [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]]：Claude Code 团队内部使用 Skills 的经验，本文的"spec 入仓 + Claude code review"是从 Skill 心法到协作方法论的延伸
- [[02-ai-coding/Claude-Code首席设计师Meaghan-Choi工作流]]：Claude Code 团队首席设计师工作流，本文是同团队的管理者视角
- [[02-ai-coding/Claude-Code一周年回顾-Boris-Cat]]：Claude Code 之父 Boris Cherny 一周年回顾，本文是 Boris 老板 Fiona 的对应视角
- [[02-ai-coding/Claude-Code-主动式Agent-Routines]]：Claude Code 的 Routines 功能详解，本文是 Routine 在管理者工作中的具体应用

### 下游（应用于 / 验证于）

- [[02-ai-coding/Addy-Osmani-Loop-Engineering]]：Loop 验证视角，本文的"验证取代编写"是 Loop 验证在跨角色场景的扩展
- [[03-productivity/WonderLearner-Alice-Claude-Code之父的新洞察-揭示AI对团队岗位的真正冲击]]：Boris Cherny 视角的"AI 对团队岗位冲击"，本文是 Boris 老板 Fiona 的对应视角
- [[01-ai-agents/ThinkingAgent-Knock-AI-Native组织5级成熟度模型]]：AI Native 组织成熟度对照，本文是 L4-L5 阶段的"Claude Code 团队实证"
- [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]：同样是"人跟不上 Agent"的视角，本文是同主线不同公司样本（Anthropic vs Multica）

### 同级（横向 / 并列）

- [[03-productivity/Laurel-CPO-Jiaona-Zhang-公司OS]]：同 AI 时代团队 OS 主线（Laurel 谈"公司 OS 怎么搭"，Fiona 谈"Claude Code 团队怎么跑"）
- [[03-productivity/快刀青衣-OpenAI高管教练四层能力]]：同主线"AI 时代个人/团队能力升级"——本文给"管理者 + 团队协作"维度的具体方法论
- [[03-productivity/HBR-China-为什么越来越多顶级领导者开始认真学哲学]]：哲学决策视角，本文是同主线的"工程团队管理者"角度
- [[03-productivity/宁向东-企业家凭什么能看见别人看不见的机会]]：创新认知视角，本文是同主线的"已实现的创新协作方式"角度

## 正文要点（7 条）

### 一、验证，正在取代编写，成为核心动作

- 编码不再是瓶颈，最大变量变成"能有多大野心"——吞吐量上升带来"质量信心"的新问题
- 把"什么算好"写成 spec 检入代码仓库，Claude 做 code review 时对照 spec 校验——code review 变成"核对代码是否仍符合当初设定的目标"，不是逐行人工过
- TDD 因 AI 分担执行工作重新变得容易坚持——Fiona 自嘲"以前像必须先吃掉西兰花"，在 Claude Code 修复第一个 bug 时重启了 TDD

### 二、同一条规律，不止发生在工程师身上

- Fiona 认为 PM 是目前受 AI 冲击**第二大**的角色（仅次于工程师）——PM 不再受限于工程带宽，可自己动手实现
- 数据科学家变审核员——"现在很多人会自己用 AI 做一版数据分析，再拿给数据科学家'过目把关'，而这些分析往往有一半时候是错的"
- "验证取代编写"跨角色重复出现的规律——核心动作从"做出来"变成"判断做得对不对"

### 三、自由和责任绑在一起：Agency + Accountability + "犯新的错误"

- Agency（自主行动力）原则——遇到问题，每个人都可以有自己的解法；但高 Agency 必须绑定高 Accountability
- "犯新的错误"管理原则——允许犯错是必要的，只要每次犯的是新错误；零错误目标往往意味着团队推进得不够快或过于谨慎
- Bad/Sad 分级框架——Bad=严重不可恢复错误（CLI 崩溃、丢失工作进度）；Sad=可恢复但影响体验问题（界面闪烁）；定义权下放各小组
- "别把动作当成进步"——不在衡量工具使用量，衡量的是"行动是否推动你想要的结果"；Facebook Marketplace 时期"超级卖家"教训让她明白指标要持续追问

### 四、从手动巡查到自动调度：协作是怎么被自动化的

- Claude Code 远程会话常驻仓库/Slack/仪表盘——每月和团队成员一起打开共同回顾（聚焦做什么、上线什么、市场反馈、有没有问题）
- Routines 改变日常——过去早上喝咖啡人工浏览反馈；现在 Routine 每天固定时间运行自动扫描反馈→提炼主题→生成 PR
- 工作方式从同步（写 prompt 等结果）演进到异步（Routine 自动派发 Agent，PR 等她第二天早上醒来摆在面前）

### 五、没被解决的代价：切换负荷与新型孤独感

- **孤独感**——过去"N 个人一起搭一套系统"（后端、前端、iOS 自然互动）；现在一个人同时跑十个并行 Claude 实例独自推进，团队互动反而变少
- **缓解而非解决**——团队组织"结伴编程午餐"+ 保留黑客马拉松；Fiona 把这种状态形容为"类似孩子'平行游戏'"（各自在做自己的项目，却因并肩工作而彼此受益）
- **切换负荷未解决**——Fiona 自己说"还没搞定"——这是访谈里少有的没有给出解决方案的坦诚时刻

### 六、管理者怎么参与 AI 协作：先做 IC，再谈管理

- IC 优先制度——新晋管理者在正式承担管理职责之前，先以个人贡献者（IC）身份工作一段时间，此后持续保持部分 IC 工作
- 内部倾听巡回触发——"审批层级太多""希望有更清晰的优先级"的真实反馈推动制度调整
- Fiona 自己延续——加入 Claude Code 团队第一周，原准备请每位工程师喝咖啡聊需求；后改成向 Claude 提问了解代码库
- "双击依赖层"——哪怕模型再强，工程师依然要花时间深入理解所依赖的代码层

## Seetong 借鉴动作（6 个）

1. **spec 入仓 + AI 评审 Seetong 化**：把"什么算好"写成 spec 检入 Seetong 代码仓库，Codex/Claude 做 code review 时对照 spec 校验（与 [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]] 的"渐进式披露 + Claude 有记忆"互补）
2. **Bad/Sad 分级入 Seetong 质量体系**：CLI 崩溃、丢失工作进度 = Bad（必查）；界面闪烁、可恢复 UI 问题 = Sad（低优先级）；分级定义权下放各端（iOS/Android/SDK）自行判断
3. **"别把动作当成进步"入 Seetong AI 助手评估**：不衡量 Codex 调用次数/Token 用量，衡量"采纳率"——采纳修改数/总修改数 = 行动是否推动结果；这与 [[01-ai-agents/Anthropic-40万场-专业杠杆]] 的"专家 5 动作 3200 词 vs 新手 600 词"数据呼应
4. **"结伴编程午餐"试 Seetong**：每周三中午 1 小时，Seetong 三端工程师 + AI 助手项目组同时开 Codex 任务，互相可见进度——缓解"和 Agent 工作的多、和人工作的少"的孤独感
5. **"IC 优先"试 Seetong 新晋管理**：黄松佳+谭伟+张威 担任管理职责前先以 IC 身份工作一段时间（1-2 个月）；保留每周 30% 时间做 IC 工作（写代码、评审 PR、处理客户问题）
6. **承认"还没解决"作为 Seetong AI 助手路线图诚实信号**：明确"切换负荷""多 Agent 协作上下文污染"等问题当前没解决方案；路线图分"已搞定 / 试点中 / 未解决"三档公示（与 [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]] 的"4 人+几十 Agent 极端样本"形成对照）

## 关键人物

- **Fiona Fung**：Anthropic Claude Code 与 Cowork 工程与产品团队负责人；Boris Cherny 与 Catherine Wu 都向她汇报
- **Boris Cherny**：Claude Code 之父，向 Fiona 汇报
- **Catherine Wu**：Claude Code 团队成员，向 Fiona 汇报
- **Lenny Rachitsky**：Lenny's Podcast 主持人
- **Datawhale**：公众号编辑团队

## 关键术语

- **验证取代编写 / Verification-Replaces-Writing**：核心动作从"做出来"变成"判断做得对不对"，跨角色重复出现的规律
- **spec 入仓 / Spec-as-Repo-Artifact**：把"什么算好"写成 spec 检入代码仓库，Claude 做 code review 时对照 spec 校验
- **TDD 回归 / TDD-Resurgence**：测试驱动开发因 AI 分担执行工作重新变得容易坚持
- **跨角色验证 / Cross-Role-Verification**：PM 不再受工程带宽限制可自己实现，数据科学家变审核员
- **Agency-Accountability 捆绑**：高 Agency 必须绑定高 Accountability
- **犯新的错误 / Make-New-Mistakes**：允许犯错，但每次必须犯的是新错误
- **Bad/Sad 分级 / Bad-Sad-Classification**：Bad=严重不可恢复错误；Sad=可恢复但影响体验问题
- **Motion-vs-Progress**：不在衡量工具使用量，衡量的是"行动是否推动想要的结果"
- **Routines 异步调度 / Routines-Async-Orchestration**：Claude Code 远程会话常驻仓库/Slack/仪表盘；Routines 每天固定时间运行自动生成 PR
- **切换负荷未解决 / Switching-Cost-Unresolved**：并行 Agent 带来的切换负荷 Fiona 自己说"还没搞定"
- **协作孤独感 / Collaboration-Loneliness**：和 Agent 工作的多、和人工作的少，类似孩子"平行游戏"
- **IC 优先 / IC-First-Management**：新晋管理者先以个人贡献者身份工作一段时间

## 分类理由

本文是 **AI Native 团队 Agent 协作方法论 + Claude Code 团队实战反思**——一手来源是 Lenny's Podcast 访谈 Fiona Fung（Anthropic Claude Code 与 Cowork 负责人）；核心命题"8 倍产出靠的不是模型，是配套协作方法论"，包含 5 大方法论（spec 入仓 / 跨角色验证 / Agency-Accountability / Bad-Sad 分级 / Routines 异步调度）+ 2 大未解决问题（孤独感 / 切换负荷）+ 1 大管理原则（IC 优先）；放 **01-ai-agents** 比 02-ai-coding 更贴切——核心是 Agent 协作与团队工作方式（不是 AI Coding 工具方法论）；且补完现有 Claude Code 团队主线（[[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]] / [[02-ai-coding/Claude-Code首席设计师Meaghan-Choi工作流]] / [[02-ai-coding/Claude-Code-主动式Agent-Routines]] / [[03-productivity/WonderLearner-Alice-Claude-Code之父的新洞察-揭示AI对团队岗位的真正冲击]]）偏"工程师视角"+"首席设计师视角"+"Boris 视角"缺位的"Fiona 视角 + 管理者视角 + 协作反思视角"维度；与 [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]（极端样本）形成"主流大厂样本 vs 极端样本"对照。

## 透明玻璃自检

- wiki 6.8K(≤8K) / digest 3.5K(≤4K)
- 节点 10 wiki / 节点 10 digest(6-10)
- H2 5 wiki / H2 5 digest(≤5)
- 表格 0 wiki / 表格 0 digest(≤2)
- 0 陈词 ⭐⭐⭐

## 适合关联的主题

- [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]]：Claude Code 团队内部使用 Skills 的经验——本文"spec 入仓 + Claude code review"是 Skill 心法到协作方法论的延伸
- [[02-ai-coding/Claude-Code首席设计师Meaghan-Choi工作流]]：Claude Code 团队首席设计师工作流——本文是同团队的管理者视角
- [[02-ai-coding/Claude-Code一周年回顾-Boris-Cat]]：Claude Code 之父 Boris Cherny 一周年回顾——本文是 Boris 老板 Fiona 的对应视角
- [[02-ai-coding/Claude-Code-主动式Agent-Routines]]：Claude Code 的 Routines 功能详解——本文是 Routine 在管理者工作中的具体应用
- [[03-productivity/WonderLearner-Alice-Claude-Code之父的新洞察-揭示AI对团队岗位的真正冲击]]：Boris Cherny 视角的"AI 对团队岗位冲击"——本文是 Boris 老板 Fiona 的对应视角
- [[02-ai-coding/Addy-Osmani-Loop-Engineering]]：Loop 验证视角——本文的"验证取代编写"是 Loop 验证在跨角色场景的扩展
- [[01-ai-agents/ThinkingAgent-Knock-AI-Native组织5级成熟度模型]]：AI Native 组织成熟度对照——本文是 L4-L5 阶段的"Claude Code 团队实证"
- [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]：同样是"人跟不上 Agent"的视角——本文是同主线不同公司样本（Anthropic vs Multica）
- [[03-productivity/Laurel-CPO-Jiaona-Zhang-公司OS]]：同 AI 时代团队 OS 主线——Laurel 谈"公司 OS 怎么搭"，Fiona 谈"Claude Code 团队怎么跑"
- [[03-productivity/快刀青衣-OpenAI高管教练四层能力]]：同主线"AI 时代个人/团队能力升级"——本文给"管理者 + 团队协作"维度的具体方法论
- [[03-productivity/HBR-China-为什么越来越多顶级领导者开始认真学哲学]]：哲学决策视角——本文是同主线的"工程团队管理者"角度
- [[03-productivity/宁向东-企业家凭什么能看见别人看不见的机会]]：创新认知视角——本文是同主线的"已实现的创新协作方式"角度