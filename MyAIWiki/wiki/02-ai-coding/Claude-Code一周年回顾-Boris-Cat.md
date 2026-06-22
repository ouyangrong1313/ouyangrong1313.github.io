---
title: Claude Code 一周年回顾:Agent 自主验证 / Routine 异步化 / Auto Mode 反直觉安全 / Context 极简主义
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Native, #主题/Anthropic, #主题/Harness, #主题/AI安全, #主题/供应链安全, #主题/工作流设计, #节点/Agent自主验证, #节点/角色边界模糊, #节点/Routine异步化, #节点/AutoMode反直觉安全, #节点/两次认知跃迁, #节点/手机编程, #节点/Context极简主义, #节点/源码泄露事件, #节点/KAIROS守护进程, #节点/UndercoverMode, #节点/ClaudeCode时间线, #手法/访谈实录, #手法/反例论证, #手法/历史回顾, #场景/编译长文, #场景/Anthropic一手]
nodes: [Agent自主验证, 角色边界模糊, Routine异步化, AutoMode反直觉安全, 两次认知跃迁, 手机编程, Context极简主义, 源码泄露事件, KAIROS守护进程, ClaudeCode时间线]
links: [[Claude-Code作者Boris-我已经不写prompt了我写loop]], [[Claude-Code之父品味不是人类护城河]], [[Claude-Code首席设计师Meaghan-Choi工作流]], [[Claude-Code团队5条工作原则-Fiona-Fung分享]], [[Addy-Osmani-Loop-Engineering]], [[Agentic-Engineering-AI-Workbench]], [[Anthropic万字长文三个判断和一个阳谋]], [[买了一样的AI为什么别家的比你的强]], [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]], [[多Agent使用边界与并行判定]], [[从Prompt-Context到Harness-工程的三次进化与终局之战]]
date: 2026-06-10
source: 微信公众号 / BorisNCat(编译自 Anthropic Claude Code 负责人 Boris Cherny + 产品负责人 Cat Wu 一周年回顾视频)
---

# Claude Code 一周年回顾:Agent 自主验证 / Routine 异步化 / Auto Mode 反直觉安全 / Context 极简主义

- 原文链接:https://mp.weixin.qq.com/s/OXXZdKfBwFJJK14kKBJ5Kw
- 原始作者:BorisNCat(微信公众号)
- 原始视频:https://www.youtube.com/watch?v=Hth_tLaC2j8
- 演示嘉宾:Boris Cherny(Anthropic,Claude Code 负责人)+ Cat Wu(Anthropic,Claude Code 产品负责人)
- 来源:微信公众号 / BorisNCat
- 发布时间:2026-06-09 23:29
- 获取时间:2026-06-10

## 核心结论(一句话)

> **Claude Code 用一年时间从 Slack 两个赞走到「人人写代码 / Agent 自动修 bug / 一半工作在手机上完成」。Boris Cherny + Cat Wu 一周年回顾核心 10 点:①Agent 自主验证(不是单元测试,而是 Claude 自己在 bash 里测自己写的东西)②人人写代码(PM/设计师/财务都用)③Routine 让 Claude 从同步变异步 ④Auto Mode 比手动更安全(Sonnet 4.6 分类器判断权限)⑤两次认知跃迁(写代码 → Agent → Loop)⑥一半工程工作在手机上完成 ⑦Context 极简主义(给最少 system prompt + 最少 tools)⑧源码泄露风波(59.8MB source map 暴露 51.2 万行代码 + KAIROS/Undercover/内部代号)⑨一年 9 个功能里程碑 ⑩下一年:Agent 越来越自主,跑几百几千个 Agent 早就不稀奇。**

## 分类提炼

- 场景:Anthropic 一周年回顾 / 个人 AI 工作流演化 / AI 编程基础设施
- 标签:#主题/AI-Coding #主题/Anthropic #节点/AutoMode反直觉安全 #节点/源码泄露事件
- 类型:访谈实录 / 历史回顾 / 供应链安全反例

## 知识节点(10 个独立概念)

- **Agent自主验证**:不是单元测试 / lint / 类型检查,而是"Agent 能不能自己跑起来,验证自己写的东西";Opus 4 起 Claude 在 bash 里自己测自己写的代码;iOS 模拟器、Android 模拟器、桌面端 computer use 循环跑验证成常规
- **角色边界模糊**:Cat(PM)在写代码,设计师 Megan 直接提 PR 修按钮,企业客户里设计师/PM/财务/数据科学家都在用;**未来每个人都既是 PM 又是工程师**
- **Routine异步化**:Voice Mode 工程师先设一个 Routine 自动监听相关 issue/bug 提交修复 PR;扩到"所有超过 5 小时没人回应的 bug report";**Routine 是 Claude 从同步工具变成异步基础设施的第一个"显而易见场景"**
- **AutoMode反直觉安全**:把权限判断交给 Sonnet 4.6 分类器;99% 请求人眼走神 → auto mode 让你只关注真正重要的事;**auto mode 比手动审核每一条权限提示更安全**;训练数据来自成千上万条 Agent 运行轨迹 + 红队 prompt 注入 + 内部攻击测试
- **两次认知跃迁**:①写代码 → 跟 Agent 说话 → Agent 写代码 ②跟 Agent 说话 → 跟 Loop/Routine 说话 → Loop 调度 Agent;"一年半就经历了两次大跃迁,这速度太疯狂了"
- **手机编程**:电脑启动 Agent → Remote Control 从手机接管 → Voice Mode 告诉 Claude 去做;**大概一半的工程工作是在手机上完成的**;Agent View 看后台 Agent 状态;桌面应用自动管理 worktree
- **Context极简主义**:"Sonnet 3.5 时代做 prompt engineering,Opus 4 时代做 context engineering,但现在的模型都不需要了";**给最少 system prompt + 最少 tools,让模型自己找 context**;Cat 自称"context minimalist";给太多 context = 微观管理
- **源码泄露事件**:2026/3/31 npm v2.1.88 不小心发布 59.8MB source map;**51.2 万行未混淆 TypeScript / 1900 个文件**;KAIROS 守护进程、Undercover Mode、Tengu/Fennec/Capybara 内部代号、44 个隐藏功能开关;DMCA 误伤 8100 仓库;**claw-code Python 重写版 2 小时 75,000 star**
- **KAIROS守护进程**:未发布的自主守护进程(后台 daemon,源码引用 150+ 次);自动监听 GitHub webhook、推送通知;**autoDream 功能在空闲时自动整合记忆**;**这是 Claude Code 的"后台灵魂"**
- **ClaudeCode时间线**:2025/5 正式发布 → 2025/9 v2.0(Checkpoints/VS Code/Hooks/GitHub Actions/Agent SDK)→ 2025/10 网页端+沙箱+Skills → 2025/11 Opus 4.5 降价 67%+compaction → 2026/1 v2.1.0(1096 commit)+ /teleport → 2026/2 Opus 4.6+Agent Teams+Remote Control → 2026/3 Voice Mode+/loop+auto mode → 2026/4 桌面应用+Routines+worktree+Opus 4.7 → 2026/5 Agent View+Opus 4.8+Dynamic Workflows

## 关联图谱

### 上游(基于 / 来自)

- [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - 同一作者多次访谈反复强调"写 loop",本篇第一次给出"两次认知跃迁"明确时间锚点
- [[Claude-Code之父品味不是人类护城河]] - Boris 谈品味被模型侵蚀,本篇 Boris 谈 AI 怎么自己验证自己写的代码;两者互补 = "品味边界"+"验证边界"
- [[Claude-Code首席设计师Meaghan-Choi工作流]] - Meaghan 谈"auto + loop",本篇 Boris 说最爱 auto mode;"AI 自动巡逻产品质量"是 Routine 的早期形态
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]] - "Trust but verify" → 本篇给出"验证 = Agent 自己跑起来"的 Anthropic 内部实践

### 下游(应用于 / 验证于)

- [[Agentic-Engineering-AI-Workbench]] - "AI 工作台"五层结构的"验证"层 = 本篇"Agent 自己跑起来验证"的工程化版本
- [[Addy-Osmani-Loop-Engineering]] - 5+1 积木 vs Boris 两次认知跃迁 = 同一信号的两种切面
- [[Anthropic万字长文三个判断和一个阳谋]] - "AI 审 AI"是同主线,但本篇更进一步 = "AI 当默认安全官"
- [[买了一样的AI为什么别家的比你的强]] - "模型是商品,判断是资产";本篇"Claude 在 bash 里自己测自己写的代码"是"判断力外包到验证环节"的具体实现

### 同级(横向 / 并列)

- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - "KAIROS + autoDream"是 Harness 的"持久化运行"维度
- [[多Agent使用边界与并行判定]] - "Agent View + 桌面应用自动管理 worktree"是"并行判定"的工具化形态
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] - "Context 极简主义"是 Harness 阶段的"约束观"具体表达

## 正文要点(10 条)

### 一、两个赞的起点 → 一年走完产品一辈子

| 维度 | 数据 |
|---|---|
| 2025/2 | Research Preview,搭配 Claude 3.7 Sonnet |
| 2025/5/22 | Claude 4 家族发布,Claude Code 正式发布 |
| 初始反馈 | Slack 内部只有 2 个赞 |
| Cat 当时评价 | "做得还挺不错"(委婉版 = "不太行") |

> "从那天起,一切开始加速。"

### 二、Agent 自主验证,不是单元测试

**常见误解**:单元测试 / lint / 类型检查
**Agent 层面的验证**:能不能自己跑起来,验证自己写的东西

| 阶段 | 验证能力 |
|---|---|
| Opus 4 | Claude 打开一个 Claude CLI,在 bash 里自己测自己写的功能 |
| 现在 | iOS 模拟器 / Android 模拟器 / 桌面端 computer use 循环跑验证成常规 |
| Cat 团队实践 | 桌面开发 Skill,computer use 在应用里点来点去,发现 bug 就修,修完再验证 |

> "如果 Claude 能把经验写进 CLAUDE.md 或做成 Skill,Claude 就能一直跑下去。"

**自我进化的闭环**:
```
发现 bug → 修复 → 验证 → 把经验更新到 Skill → 下次直接用
```

### 三、人人都在写代码

| 角色 | 写代码状态 |
|---|---|
| Cat(PM) | 写代码 |
| 设计师 Megan | 直接提 PR 修按钮("写得还挺好的") |
| 企业客户的 PM | 直接在应用里改功能 |
| 企业客户的财务 | 在 Claude Code 里跑预测模型 |
| 企业客户的数据科学家 | 屏幕上全是 Claude Code |

**Boris 的判断**:未来每个人都既是 PM 又是工程师。工程师越来越多地端到端交付产品,从想法到实现到发布到和法务、市场协调,一个人走完全流程。

### 四、Routine 的威力:Claude 从同步变异步

**Voice Mode 工程师的两个 Routine**:
1. 自动监听所有关于 Voice Mode 的 GitHub issue 和 bug report → 提交修复 PR → ping 他 review
2. 监控所有**超过 5 小时没人回应**的 bug report → 自动提交修复

> "我发了一个小功能,有个边界情况我没注意到。有人报了 bug,我打算晚上去修。结果我的 Claude 告诉我:「等等,另一个 Claude 已经修了。」"

> "回想一下以前,你得自己回复 code review 评论,自己修 CI,自己 rebase。这些我已经很久很久没做过了。"

**关键定位**:Routine 是 Agent SDK 之后第一个"显而易见的应用场景",让 Claude **从同步工具变成异步基础设施**。

### 五、最爱 Auto Mode(反直觉安全设计)

**Auto Mode 的核心设计**:把权限判断交给另一个模型(Sonnet 4.6)做安全审查。

**反直觉论点**:auto mode 比手动审核每一条权限提示更安全。
- 当你 99% 的请求都点同意时,眼睛就走神了
- Auto mode 让你只关注真正重要的事

**Anthropic 上线前的安全工程**:
- 收集成千上万条 Agent 运行轨迹 → 训练 auto mode 分类器
- 请红队人员做 prompt 注入攻击
- 让内部团队亲自尝试攻击 Claude Code 的 auto mode
- 所有发现的问题都变成 eval,持续提升安全性

> "这不只是防范已知漏洞,而是防范我们能构造出的最聪明的攻击。"

### 六、两次认知跃迁 + 一半工作在手机上

**两次认知跃迁**:
```
跃迁 1:写代码 → 跟 Agent 说话(Agent 写代码)
跃迁 2:跟 Agent 说话 → 跟 Loop/Routine 说话(Loop 调度 Agent)
```

**手机编程**:
- 电脑启动 Agent → Remote Control 从手机接管
- 出去买杯咖啡,看看 Agent 进展,启动新 Agent
- 跟人聊天聊出 idea → Voice Mode 告诉 Claude 去做
- **大概一半的工程工作是在手机上完成的**

**终端标签对比**:
| 维度 | 一年前 | 现在 |
|---|---|---|
| 终端标签 | 6 个 | 1 个 |
| git checkout | 6 个同一仓库切换 | 桌面应用自动管理 worktree |
| 状态监控 | 来回切换 | Agent View 一屏全看 |

### 七、Context 极简主义

> "以前 Sonnet 3.5 时代你得做 prompt engineering,Opus 4 时代你得做 context engineering。但现在的模型,这些都不需要了。"

**Cat 的实践**:告诉模型它需要知道的,剩下的让它自己搞定。

> "给模型太多 context,就像在微观管理它。有时候模型知道更好的方法来达到同一个目标。"

### 八、源码泄露风波(2026/3/31)

**事件**:
- Anthropic 通过 npm 包 @anthropic-ai/claude-code v2.1.88 不小心发布 59.8MB JavaScript source map
- 51.2 万行未混淆 TypeScript / 约 1900 个文件
- 根本原因:Claude Code 基于 Bun 构建,Bun 默认生成 source map,但没人在 .npmignore 里排除

**社区扒出的料**:

| 内部代号 | 含义 |
|---|---|
| Tengu | Claude Code 项目代号 |
| Fennec | Opus 4.6 |
| Capybara | 疑似 Mythos 模型 |

**未发布功能**:

| 功能 | 描述 |
|---|---|
| KAIROS | 自主守护进程(后台 daemon),源码引用 150+ 次;监听 GitHub webhook、推送通知 |
| autoDream | KAIROS 内置,空闲时自动整合记忆 |
| Undercover Mode | ~90 行代码;员工操作非内部仓库时自动激活,去掉 Co-Authored-By 署名,禁止提及内部代号 |
| 隐藏功能开关 | 44 个 |
| 未发布功能 | 20 多个 |

**社区反应**:
- 安全研究员 Chaofan Shou 在 X 公开 → 引发开发者社区爆炸
- Anthropic DMCA 误伤 8100 个仓库(包括自家开源仓库的合法 fork)→ 撤回大部分
- Mirror 仓库被下架前 41,500 个 fork
- **韩国开发者"claw-code" Python 重写版 2 小时 75,000 GitHub star**
- 有人根据 Claude Buddy 变体发 meme 币

**漏洞暴露**:
- CVE-2025-59536、CVE-2026-21852 等
- RCE + API token 窃取

**正面影响**:也让社区第一次看到 Claude Code 内部复杂度 — 40+ 注册工具 / 5 种 context 压缩策略 / 23 个 bash 安全检查 / 14 个缓存破坏向量。

> Boris:"这是一个人为错误。没有人因此被开除,犯错的人仍然拥有公司的完全信任。这是一个流程漏洞,任何人都可能犯。"

### 九、一年功能时间线(9 个里程碑)

| 时间 | 里程碑 |
|---|---|
| 2025/5 | 正式发布,搭配 Opus 4 |
| 2025/9 | **Claude Code 2.0**(Checkpoints / VS Code 扩展 / Hooks 系统 / GitHub Actions 集成 / Agent SDK) |
| 2025/10 | 网页端(claude.ai/code)+ 沙箱隔离 + Skills 系统 |
| 2025/11 | Opus 4.5 + 67% 降价 + context compaction |
| 2026/1 | v2.1.0(1096 commit)+ /teleport + 多语言 |
| 2026/2 | Opus 4.6 + **Agent Teams** + **Remote Control** |
| 2026/3 | Voice Mode + /loop + **auto mode** |
| 2026/4 | 桌面应用重设计 + **Routines 正式发布** + worktree 隔离 + Opus 4.7 + push notifications |
| 2026/5 | **Agent View** + Opus 4.8 + **Dynamic Workflows** |

> "一年之内,从一个终端聊天工具变成了一个可以自主运行、自我验证、多实例协作的 AI 编程基础设施。"

### 十、下一年

> Boris:"一年后的使用方式如果还跟现在一样,我反而会觉得奇怪。Agent 运行时间越来越长,越来越自主,同时跑几百上千个 Agent 早就不稀奇了。下一年的形态,一定跟现在完全不同。"

> Cat:"这些想法不会只从我们这里来,而是会从整个社区里涌现出来。"

## 我的理解

- **"Agent 自主验证"是 Claude Code 一年里最被低估的能力升级** — 不是"单元测试",而是"Claude 自己在 bash 里跑自己写的代码";跟 [[Agentic-Engineering-AI-Workbench]] 中"AI 工作台 = 5 层结构(计划/上下文/执行/验证/治理)"的"验证"层是同一思路,但 Claude Code 把"验证"做成了"Agent 自己在 iOS 模拟器/桌面应用里点来点去";**对 Seetong**:验证不再是"测试工程师写测试用例",而是"AI 自己在 Xcode/真机里跑"
- **"Auto Mode 比手动更安全"是反直觉但有数据的安全设计模式** — Anthropic 用 Sonnet 4.6 做权限分类器,99% 人眼走神反而是漏洞;与 [[Anthropic万字长文三个判断和一个阳谋]] 提到的"AI 审 AI"同主线,但更进一步 = **AI 当默认安全官,人只介入真正高风险事件**;**对 Seetong**:当前 Seetong 多级确认(开发/测试/PM)可能有"99% 走过场"的隐患,值得调研 auto 化权限分层
- **"Routine 是 Claude 从同步变异步的第一个显而易见场景"** — 跟 [[Claude-Code首席设计师Meaghan-Choi工作流]] 的"AI 自动巡逻产品质量"是同一信号的反复印证;但本篇给了**具体配置:5 小时没人响应的 bug report 自动提交修复**;**对 Seetong 可立刻抄作业**:Seetong 当前 Bug/需求响应周期长,可设个"3 天测试未响应 + 1 天开发未响应"的自动催办或自动升优先级 Routine
- **"两次认知跃迁(写代码 → Agent → Loop)"** — 这是 2026 年 AI Coding 范式的最清晰总结;跟 [[Claude-Code作者Boris-我已经不写prompt了我写loop]] [[Addy-Osmani-Loop-Engineering]] [[Claude-Code之父品味不是人类护城河]] 是同一主线,**但本篇第一次给出了"两次跃迁"的明确时间锚点(1.5 年)**
- **"Context 极简主义"是 Anthropic 内部对 Context Engineering 的反思** — Cat 自称"context minimalist",Boris 说"给最少 system prompt + 最少 tools";跟 [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] 中"Harness 是约束,不是堆 context"是同一立场;**对 Seetong 团队**:当前如果每个项目的 AGENTS.md/CLAUDE.md 都写了一大堆"上下文",可能需要反向瘦身,只留关键约束
- **"源码泄露风波"是教科书级的供应链安全反例** — 51.2 万行 / KAIROS / Undercover Mode / 内部代号 / 44 隐藏开关 / DMCA 误伤 8100 仓库 / 韩国开发者 2 小时 75,000 star / meme 币;**对 Seetong 团队**:①发布 npm 包时一定要确认 .npmignore 排除 source map ②任何"小疏忽"都可能成为产品级公关危机 ③AI 匿名贡献开源的伦理问题(Undercover Mode)是新兴领域,值得团队提前讨论立场
- **"KAIROS + autoDream"是 AI Agent 的"后台灵魂"** — 源码泄露暴露 Claude Code 内部有"自主守护进程 + 空闲时自动整合记忆" = **AI 越来越有"持续存在"的本体论意义**;与 [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] "AI 持久化运行"同主线;**未来 Seetong 自研 AI 助手时,要考虑"AI 也有后台(daemon + 自动记忆)"的架构设计**
- **"下一年:Agent 越来越自主,跑几百几千个"** — Boris 公开说"下一年的形态,一定跟现在完全不同";**给团队的最重要提醒**:**今天搭的所有 AI 工作流都是"过渡版"**,不用追求一步到位,关键是要**保留架构弹性**让下一代模型/Agent 直接接上(呼应 Meaghan 那篇的"先把流程搭好等模型升级")

## 相关链接

- 原文:https://mp.weixin.qq.com/s/OXXZdKfBwFJJK14kKBJ5Kw
- 原始视频:https://www.youtube.com/watch?v=Hth_tLaC2j8
- Claude Code 官方文档:https://code.claude.com/docs/en/overview
- ClaudeDevs 推文:https://x.com/ClaudeDevs/status/2064032814392352816
- 关联 wiki:
  - [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - 同一作者多次访谈反复强调"写 loop",本篇第一次给出"两次认知跃迁"明确时间锚点
  - [[Claude-Code之父品味不是人类护城河]] - Boris 谈品味被模型侵蚀,本篇谈 AI 怎么自己验证自己写的代码
  - [[Claude-Code首席设计师Meaghan-Choi工作流]] - Meaghan 谈"auto + loop",Boris 说最爱 auto mode
  - [[Claude-Code团队5条工作原则-Fiona-Fung分享]] - "Trust but verify" → "Agent 自己跑起来验证"
  - [[Addy-Osmani-Loop-Engineering]] - 5+1 积木 vs Boris 两次认知跃迁
  - [[Agentic-Engineering-AI-Workbench]] - "AI 工作台"五层结构的"验证"层
  - [[Anthropic万字长文三个判断和一个阳谋]] - "AI 审 AI"主线,本篇更进一步 = "AI 当默认安全官"
  - [[买了一样的AI为什么别家的比你的强]] - "Claude 在 bash 里自己测自己写的代码"是"判断力外包到验证环节"
  - [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - "KAIROS + autoDream"是 Harness 的"持久化运行"维度
  - [[多Agent使用边界与并行判定]] - "Agent View + 桌面应用自动管理 worktree"是并行判定的工具化形态
  - [[从Prompt-Context到Harness-工程的三次进化与终局之战]] - "Context 极简主义"是 Harness 阶段的"约束观"具体表达