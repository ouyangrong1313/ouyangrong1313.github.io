---
title: Claude Code 之父的老板，坦白 Agent 协作方法（Digest）
date: 2026-07-06
source: 微信公众号 / Datawhale（编译 Lenny's Podcast 访谈 Fiona Fung）
source_url: https://mp.weixin.qq.com/s/c9Vkx_2l2PRSY__GjUlHuQ
original_source: https://www.youtube.com/watch?v=Ybrl4FYM57c
tags: [#主题/AI-Agent, #主题/AI-Coding, #节点/Agent-Loop, #节点/Claude-Code]
status: digest
---

# Digest：Claude Code 之父的老板，坦白 Agent 协作方法

## 5 句话讲完

1. **8 倍产出是真的，但支撑它的不是模型**——Anthropic 工程师人均每季度代码产出 8 倍于 2025 同期，关键是把"什么算好"写进仓库里的 spec、Claude code review 对照 spec、TDD 因 AI 分担执行工作重新变得可坚持
2. **验证取代编写，是跨角色规律**——不只是工程师要"判断做得对不对"，PM 现在能自己动手实现，数据科学家变成"审核别人用 AI 生成的半错分析"，核心动作从"做出来"变成"判断做得对不对"
3. **自由和责任必须绑在一起**——Agency 高意味着 Accountability 必须高；"犯新的错误"比"零错误"更好；Bad/Sad 分级 + 定义权下放；别把动作当成进步（"行动是否推动想要的结果"）
4. **Routine 让管理者变成"异步调度员"**——Claude Code 远程会话常驻仓库/Slack/仪表盘，每月自动回顾；Routines 每天固定时间扫描反馈→提炼主题→生成 PR，等她第二天早上醒来成果已经摆在面前
5. **没解决的代价同样诚实**——协作孤独感用"结伴编程午餐+黑客马拉松"缓解但没真正解决；并行 Agent 切换负荷 Fiona 自己说"还没搞定"；新晋管理者先按回 IC 位置才能与团队建立信任

## 关键数字

- **8 倍**：Anthropic 工程师人均每季度代码产出相比 2025 同期
- **20 个**：Fiona 团队成员同时运行的 Agent 数量（部分人）
- **一半时候是错的**：AI 生成数据分析里被数据科学家否决的比例
- **10 个**：并行运行的 Claude 实例数量（典型）
- **1 个月**：Claude Code 远程会话月度回顾周期
- **0 个**：Fiona 团队关于"切换负荷"的解决方案数（"还没搞定"）

## 5 句金句

1. **"允许犯错是必要的，只要每次犯的是新错误，因为如果目标是零错误，往往意味着团队推进得不够快，或者过于谨慎。"**——Fiona 关于"犯新的错误"
2. **"不要把动作误当成进步。如果只是在衡量工具的使用量，衡量的是'行动'，但这真的在推动你想要的结果吗？"**——Fiona 关于别把动作当成进步
3. **"以前可能还会自己生成一些 prompt，但现在有了 Routines，几乎是在让一个 Agent 帮她生成 prompt 和 PR。"**——Fiona 关于 Routine 异步化
4. **"如果一个管理者一上来就急着打开管理工具箱、做管理该做的事，反而容易造成过多的审批层级；而如果先花时间深入代码库和产品本身，往往能和团队建立起真正的信任关系。"**——Fiona 关于 IC 优先
5. **"哪怕模型再强，工程师依然要花时间'双击'自己所依赖的那一层。因为只有理解依赖关系，才能真正意识到底层发生了什么变化。"**——Fiona 关于双击依赖层

## 3 个反直觉点

1. **快不等于好**——8 倍产出背后最关键的不是模型变强，是 spec 写进仓库、TDD 重新变得可坚持、Claude code review 对照 spec 这些"慢方法论"的回归
2. **自由必须配责任**——高 Agency 必须绑定高 Accountability，否则团队就只是"动作量"而不是"结果量"；这与"低 Agency + 高 Accountability"的传统管理逻辑相反
3. **管理者要先做 IC**——新晋管理者先以个人贡献者身份工作一段时间，才能与团队建立信任关系；这与"管理者应该尽早转型"的传统管理路径相反

## 7 个分析角度 + 14-21 个开头钩子

### 角度 1：8 倍产出背后真正的胜负手（写作角度：反差冲击）

1. "Anthropic 工程师人均代码产出涨到 8 倍——但他们的经理说，最大变量不是模型。"
2. "模型变强是表象，协作方式重塑才是这轮变化的真正内核。"
3. "8 倍产出不是靠更努力，是靠'动作是不是结果'这套新纪律。"

### 角度 2：验证取代编写的跨角色规律（写作角度：跨角色对照）

4. "工程师不再是'写代码的人'——验证取代编写，正在跨角色重复出现。"
5. "PM 现在能自己动手实现，数据科学家变成审核员——AI 时代的岗位本质都在迁移。"
6. "不再问'谁做出来'，而是问'谁判断做得对不对'——这是新协作的核心问题。"

### 角度 3：Agency 与 Accountability 的捆绑（写作角度：自由悖论）

7. "她允许团队'犯新的错误'——但零错误的目标，反而说明团队推进得不够快。"
8. "自由不是放手，是绑定责任——Anthropic Claude Code 团队的 Agency 文化。"
9. "如果一个管理者一上来就急着打开管理工具箱，往往容易造成过多的审批层级。"

### 角度 4：Bad/Sad 分级与定义权下放（写作角度：颗粒度治理）

10. "严重不可恢复的错误叫 Bad，可恢复但影响体验的叫 Sad——定义权下放各小组。"
11. "为什么 Anthropic 不追求全公司统一质量标准？因为不同产品面的仪表盘数字很难直接比较。"
12. "质量管理最反常识的一招：把'什么算好'的定义权交给最接近问题的人。"

### 角度 5：Routines 让管理者变成异步调度员（写作角度：工作方式颠覆）

13. "她现在让一个 Agent 帮她生成 prompt 和 PR——异步化是这轮工作方式的核心。"
14. "以前早上喝咖啡人工浏览反馈，现在 Routine 自动扫描反馈→提炼主题→生成 PR。"
15. "管理者的工作方式被颠覆性转变：从手动巡查到自动调度，Routine 是分水岭。"

### 角度 6：没解决的代价（写作角度：诚实即专业）

16. "并行 Agent 太多带来的切换负荷，Fiona 自己说'还没搞定'——这才是 AI 协作的真实样子。"
17. "孤独感、切换负荷、平行游戏——Anthropic Claude Code 团队也没解决的三个问题。"
18. "承认哪些地方暂时没有答案，比假装一切都已搞定，更接近这轮变化的真实。"

### 角度 7：管理者先做 IC 再谈管理（写作角度：身份回归）

19. "新晋管理者在正式承担管理职责之前，先以个人贡献者身份工作一段时间。"
20. "她加入 Claude Code 团队的第一周，请工程师喝咖啡改成向 Claude 提问了解代码库。"
21. "哪怕模型再强，工程师依然要花时间'双击'自己所依赖的那一层。"

## 关键事实清单

- 一手来源：Lenny's Podcast 访谈 Fiona Fung：https://www.youtube.com/watch?v=Ybrl4FYM57c
- Fiona Fung 管理 Anthropic Claude Code 与 Cowork 团队
- Boris Cherny（Claude Code 之父）与 Catherine Wu 都向 Fiona 汇报
- Routines 是 Claude Code 2025-2026 上线的新功能（每天固定时间运行）
- spec 入仓 + Claude code review 对照 spec 的方法论
- TDD 在 Claude Code 修复第一个 bug 时被 Fiona 重启使用
- PM 受 AI 冲击第二大（第一大是工程师）
- 数据科学家从"做分析"变成"审核 AI 生成的半错分析"
- Bad/Sad 分级框架下放各小组定义权
- 犯新的错误管理原则
- Claude Code 远程会话常驻仓库/Slack/仪表盘
- 结伴编程午餐 + 黑客马拉松作为孤独感缓解手段
- 切换负荷问题 Fiona 本人坦诚未解决
- 新晋管理者先做 IC 一段时间再谈管理
- 加入 Claude Code 团队第一周 Fiona 用 Claude 提问替代请工程师喝咖啡

## 关联链接（待办）

- [[loonggg-Claude-Code-技能心法-11条建议]] — Claude Code 团队内部使用 Skills 的经验（同主线）
- [[Claude-Code首席设计师Meaghan-Choi工作流]] — Claude Code 团队首席设计师（同主线）
- [[Claude-Code一周年回顾-Boris-Cat]] — Claude Code 之父 Boris Cherny 视角
- [[Claude-Code-主动式Agent-Routines]] — Routines 功能详解
- [[Addy-Osmani-Loop-Engineering]] — Loop 验证视角
- [[ThinkingAgent-Knock-AI-Native组织5级成熟度模型]] — AI Native 组织成熟度对照
- [[Multica-AI-Native-组织-人是最慢的节点]] — 同样是"人跟不上 Agent"的视角
- [[Laurel-CPO-Jiaona-Zhang-公司OS]] — 同 AI 时代团队 OS 主线
- [[WonderLearner-Alice-Claude-Code之父的新洞察]] — Boris Cherny 视角的"AI 对团队岗位冲击"
- [[快刀青衣-OpenAI高管教练四层能力]] — AI 时代内在能力升级
- [[HBR-China-为什么越来越多顶级领导者开始认真学哲学]] — 哲学决策视角
- [[宁向东-企业家凭什么能看见别人看不见的机会]] — 创新认知视角

## 标签

- #主题/AI-Agent
- #主题/AI-Coding
- #场景/公众号长文
- #节点/Agent-Loop
- #节点/Harness
- #节点/AI-Native
- #节点/Claude-Code
- #节点/Spec-Driven