# Claude Code 之父一周年回顾 - Digest

- 原文链接:https://mp.weixin.qq.com/s/OXXZdKfBwFJJK14kKBJ5Kw
- 原始作者:BorisNCat(微信公众号)
- 原始视频:https://www.youtube.com/watch?v=Hth_tLaC2j8
- 演示嘉宾:Boris Cherny(Anthropic Claude Code 负责人)+ Cat Wu(Anthropic Claude Code 产品负责人)
- 来源:微信公众号 / BorisNCat
- 发布时间:2026-06-09 23:29
- 获取时间:2026-06-10

## 一句话总结

**Claude Code 用一年时间从 Slack 两个赞走到「人人写代码 / Agent 自动修 bug / 一半工作在手机上完成」。Boris Cherny + Cat Wu 一周年回顾核心 10 点:①Agent 自主验证(不是单元测试,而是 Claude 自己在 bash 里测自己写的东西)②人人写代码(PM/设计师/财务都用)③Routine 让 Claude 从同步变异步 ④Auto Mode 比手动更安全(Sonnet 4.6 分类器判断权限)⑤两次认知跃迁(写代码 → Agent → Loop)⑥一半工程工作在手机上完成 ⑦Context 极简主义(给最少 system prompt + 最少 tools)⑧源码泄露风波(59.8MB source map 暴露 51.2 万行代码 + KAIROS/Undercover/内部代号)⑨一年 9 个功能里程碑 ⑩下一年:Agent 越来越自主,跑几百几千个 Agent 早就不稀奇。**

## 核心观点(10 个)

1. **两个赞的起点** — 2025/2 Research Preview,3 个月后搭 Claude 4 正式发布;Slack 内部只有 2 个赞
2. **Agent 自主验证,不是单元测试** — 一提到验证,大家想的是单元测试/lint/类型;Agent 层面的验证是"能不能自己跑起来验证自己写的东西";Opus 4 起 Claude 在 bash 里自己测自己写的代码;iOS/Android 模拟器、computer use 循环跑验证成常规
3. **人人都在写代码** — Cat(PM)在写代码;设计师 Megan 直接提 PR 修按钮;企业客户里设计师/PM/财务/数据科学家都在用 Claude Code;**未来每个人都既是 PM 又是工程师**
4. **Routine 是异步基础设施的第一个"显而易见场景"** — Voice Mode 工程师先设一个 Routine 自动监听相关 issue/bug,提交修复 PR;扩到"所有超过 5 小时没人回应的 bug report";"另一个 Claude 已经修了" = **Claude 从同步工具变成异步基础设施**
5. **Auto Mode 比手动更安全** — 把权限判断交给 Sonnet 4.6 分类器;99% 请求人眼走神 → auto mode 只让你关注真正重要的事;Anthropic 收集成千上万条 Agent 运行轨迹训练分类器 + 红队 prompt 注入 + 内部攻击测试,所有发现变成 eval
6. **两次认知跃迁** — 第一次:写代码 → 跟 Agent 说话;第二次:跟 Agent 说话 → 跟 Loop/Routine 说话;"一年半两次大跃迁,这速度太疯狂了"
7. **一半工程工作在手机上完成** — 电脑启动 Agent → Remote Control 从手机接管 → Voice Mode 告诉 Claude 去做;Agent View 看所有后台 Agent 状态;桌面应用自动管理 worktree;以前开 6 个终端标签,现在开 1 个
8. **Context 极简主义** — "以前 Sonnet 3.5 时代做 prompt engineering,Opus 4 时代做 context engineering。但现在的模型,这些都不需要了";**给模型最少的 system prompt,最少的 tools,让它自己找 context**;Cat 自称"context minimalist";给太多 context = 微观管理
9. **源码泄露风波(2026/3/31)** — npm v2.1.88 不小心发布 59.8MB source map;**51.2 万行未混淆 TypeScript / 约 1900 个文件**;社区扒出 KAIROS(未发布守护进程 + autoDream 空闲整合记忆)、Undercover Mode(员工操作外部仓库自动去 Co-Authored-By 署名 + 禁提内部代号)、Tengu/Fennec/Capybara 内部代号、44 个隐藏功能开关;DMCA 误伤 8100 个仓库;韩国开发者"claw-code" Python 重写版 2 小时 75,000 star;meme 币;多个严重漏洞(CVE-2025-59536、CVE-2026-21852 RCE + API token 窃取)
10. **下一年** — "一年后的使用方式如果还跟现在一样,我反而会觉得奇怪";Agent 运行时间越来越长、越来越自主;一次跑几百几千个 Agent 早就不稀奇;"想法不会只从我们这里来,而是从整个社区涌现出来"

## 7 个分析角度 × 3 个开头钩子

### 角度 1:现象 / 反常识

- 钩子 1:"Slack 两个赞"到"人人写代码"只用了一年
- 钩子 2:"Claude Code 负责人最爱的功能不是 plan mode,是 auto mode"
- 钩子 3:把权限判断交给另一个模型,比让用户点同意更安全(反直觉)

### 角度 2:痛点 / 矛盾

- 钩子 1:99% 的权限请求人眼走神 — auto mode 反而是更安全的选择
- 钩子 2:Context 越多越好?Anthropic 内部答案是最少 system prompt + 最少 tools
- 钩子 3:源码泄露 51.2 万行 = "另一种方式的开源"

### 角度 3:原因 / 为什么

- 钩子 1:为什么 Opus 4.6/4.7 之后不再需要 plan 步骤?
- 钩子 2:为什么 Routine 是 Claude 从同步变异步的"第一个显而易见场景"?
- 钩子 3:为什么 Context 极简主义(给最少)比 Context 工程(给一堆)更有效?

### 角度 4:方法 / 怎么做

- 钩子 1:Agent 自主验证 = Claude 在 bash 里自己测自己写的代码(不靠单元测试)
- 钩子 2:Auto Mode = Sonnet 4.6 分类器判断 + 训练数据来自成千上万 Agent 运行轨迹
- 钩子 3:从终端 6 标签 → Agent View 1 标签 + 桌面应用自动管理 worktree

### 角度 5:流程 / 迭代

- 钩子 1:一年 9 个时间锚点(2025/5 → 2026/5) = 完整功能演化时间线
- 钩子 2:两次认知跃迁(写代码 → Agent → Loop) = 一段 1.5 年走完两层抽象跃迁
- 钩子 3:验证 = 写完 → bash 自己测 → Skill 沉淀 → 下次直接用 = 自我进化闭环

### 角度 6:类比 / 跨域

- 钩子 1:Auto Mode = "用另一个模型当你的安全顾问",但你不需要听他长篇大论,只看结论
- 钩子 2:Routine = "长期挂着永不关机的 cron + 决策权",从"我做" → "我设个规矩,让 Claude 自动跑"
- 钩子 3:源码泄露 = 一次失败的 DMCA = 反向公开了 Claude Code 内部 40+ 工具/5 种压缩策略/23 个 bash 安全检查

### 角度 7:行动 / 启示

- 钩子 1:你的 AI 工作流里哪些权限提示你每天点同意点到手软?试试 auto mode / 二级确认
- 钩子 2:你的 Routine / cron 是不是只有"查"没有"修"?学 Voice Mode 工程师设个"5 小时没人响应自动修"的
- 钩子 3:你的 context 是不是给得太多?试试 context minimalist 思路,给最少的 system prompt

## 我的理解

- **"Agent 自主验证"是 Claude Code 一年里最被低估的能力升级** — 不是"单元测试",而是"Claude 自己在 bash 里跑自己写的代码";这跟 [[Agentic-Engineering-AI-Workbench]] 中"AI 工作台 = 5 层结构(计划/上下文/执行/验证/治理)"的"验证"层是同一思路,但 Claude Code 把"验证"层做成了"Agent 自己在 iOS 模拟器/桌面应用里点来点去";**这意味着:对 Seetong 来说,验证不再是"测试工程师写测试用例",而是"AI 自己在 Xcode/真机里跑"**
- **"Auto Mode 比手动更安全"是反直觉但有数据的安全设计模式** — Anthropic 用 Sonnet 4.6 做权限分类器,99% 人眼走神反而是漏洞;这与 [[Anthropic万字长文三个判断和一个阳谋]] 提到的"AI 审 AI"同主线,但更进一步 = **不只 AI 审 AI,而是 AI 当默认安全官,人只介入真正高风险事件**;对 Seetong:**当前 Seetong 的多级确认(开发/测试/PM)可能有"99% 走过场"的隐患,值得调研 auto 化的权限分层**
- **"Routine 是 Claude 从同步变异步的第一个显而易见场景"** — 跟 [[Claude-Code首席设计师Meaghan-Choi工作流]] 的"AI 自动巡逻产品质量"是同一信号的反复印证;但 Meaghan 那篇是 Anthropic 内部自用,本篇给了具体配置:**5 小时没人响应的 bug report 自动提交修复**;**对 Seetong 可立刻抄作业**:Seetong 当前 Bug/需求响应周期长,可设个"3 天测试未响应 + 1 天开发未响应"的自动催办或自动升优先级 Routine
- **"两次认知跃迁(写代码 → Agent → Loop)"** — 这是 2026 年 AI Coding 范式的最清晰总结;跟 [[Claude-Code作者Boris-我已经不写prompt了我写loop]] [[Addy-Osmani-Loop-Engineering]] [[Claude-Code之父品味不是人类护城河]] 是同一主线,**但本篇第一次给出了"两次跃迁"的明确时间锚点(1.5 年)**
- **"Context 极简主义"是 Anthropic 内部对"Context Engineering"反思** — Cat 自称"context minimalist",Boris 说"给最少 system prompt + 最少 tools";**这跟 [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] 中"Harness 是约束,不是堆 context"是同一立场**;**对 Seetong 团队**:当前如果每个项目的 AGENTS.md/CLAUDE.md 都写了一大堆"上下文",可能需要反向瘦身,只留关键约束
- **"源码泄露风波"是教科书级的供应链安全反例** — 51.2 万行 / KAIROS / Undercover Mode / 内部代号 / 44 隐藏开关 / DMCA 误伤 8100 仓库 / 韩国开发者 2 小时 75,000 star / meme 币;**对 Seetong 团队**:①发布 npm 包时一定要确认 .npmignore 排除 source map ②任何"小疏忽"都可能成为产品级公关危机 ③AI 匿名贡献开源的伦理问题(Undercover Mode)是新兴领域,值得团队提前讨论立场
- **"KAIROS + autoDream"是 AI Agent 的"后台灵魂"** — 源码泄露暴露 Claude Code 内部有"自主守护进程 + 空闲时自动整合记忆" = **AI 越来越有"持续存在"的本体论意义**;与 [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] 的"AI 持久化运行"同主线;**未来 Seetong 自研 AI 助手时,要考虑"AI 也有后台(daemon + 自动记忆)"的架构设计**
- **"下一年:Agent 越来越自主,跑几百几千个"** — Boris 公开说"下一年的形态,一定跟现在完全不同";**给团队的最重要提醒**:**今天搭的所有 AI 工作流都是"过渡版"**,不用追求一步到位,关键是要**保留架构弹性**让下一代模型/Agent 直接接上(呼应 Meaghan 那篇的"先把流程搭好等模型升级")

## 关联文章

- [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - 同一作者多次访谈反复强调"写 loop",本篇第一次给出"两次认知跃迁"明确时间锚点
- [[Claude-Code之父品味不是人类护城河]] - Boris 谈品味被模型侵蚀,本篇 Boris 谈 AI 怎么自己验证自己写的代码;两者互补 = "品味边界"+"验证边界"
- [[Claude-Code首席设计师Meaghan-Choi工作流]] - Meaghan 谈"auto + loop",本篇 Boris 说最爱 auto mode;"AI 自动巡逻产品质量"是 Routine 的早期形态
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]] - "Trust but verify" → 本篇给出"验证 = Agent 自己跑起来"的 Anthropic 内部实践
- [[Addy-Osmani-Loop-Engineering]] - 5+1 积木 vs Boris 两次认知跃迁 = 同一信号的两种切面
- [[Agentic-Engineering-AI-Workbench]] - "AI 工作台"五层结构的"验证"层 = 本篇"Agent 自己跑起来验证"的工程化版本
- [[Anthropic万字长文三个判断和一个阳谋]] - "AI 审 AI"是同主线,但本篇更进一步 = "AI 当默认安全官"
- [[买了一样的AI为什么别家的比你的强]] - "模型是商品,判断是资产";本篇"Claude 在 bash 里自己测自己写的代码"是"判断力外包到验证环节"的具体实现
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - "KAIROS + autoDream"是 Harness 的"持久化运行"维度
- [[多Agent使用边界与并行判定]] - "Agent View + 桌面应用自动管理 worktree"是"并行判定"的工具化形态
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] - "Context 极简主义"是 Harness 阶段的"约束观"具体表达