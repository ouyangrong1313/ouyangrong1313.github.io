# Claude Code 之父一周年回顾:下一年的形态,一定跟现在完全不同

- 原文链接:https://mp.weixin.qq.com/s/OXXZdKfBwFJJK14kKBJ5Kw
- 原始作者:BorisNCat(微信公众号)
- 原始视频:https://www.youtube.com/watch?v=Hth_tLaC2j8
- 来源:微信公众号 / BorisNCat
- 演示嘉宾:Boris Cherny(Anthropic,Claude Code 负责人)+ Cat Wu(Anthropic,Claude Code 产品负责人)
- 发布时间:2026-06-09 23:29
- 获取时间:2026-06-10
- 获取方式:curl + UA + 抓取 js_content 区段,Python 清洗

---

## 引子

一年前,Claude Code 在 Slack 内部演示时只收到了两个赞。一年后,PM 在写代码,工程师在手机上写代码,Agent 在自动修 bug。

昨天,Claude Code 负责人 Boris Cherny 和产品负责人 Cat Wu 录了一期回顾视频,聊了聊这一年的心路历程。

上面是两人的完整回顾视频,我也结合视频内容对 Claude Code 这一整年的进程进行了全面梳理。

## 01 两个赞的起点

Boris 在视频里回忆了 Claude Code 最早的样子:

> 我们刚发布 Claude Code 的时候就是一个小视频,我记得发到 Slack 上,大概只有两个人点了个赞。

Cat 则笑着回应:

> 我当时觉得挺酷的,特别是一些比较简单的工程任务,它做得还不错。

Boris 自我拆台道:

> 这话说得真委婉啊,其实就是说它当时不太行。

2025 年 2 月,Claude Code 以 Research Preview 的身份登场,搭配 Claude 3.7 Sonnet,就是一个能在终端里跟 Claude 聊天、编辑文件、跑 bash 的 CLI 工具。

3 个月后的 5 月 22 日,Claude 4 家族(Opus 4 和 Sonnet 4)发布,Claude Code 正式发布。

**从那天起,一切开始加速。**

## 02 验证才是关键

Boris 认为,过去一年他在 Claude Code 上学到的最重要的一个理念是:每次 Claude 犯错,不要告诉它下次怎么做,而是让它把经验写进 CLAUDE.md 或做成 Skill。

> 如果你能做到这点,Claude 就能一直跑下去。

但真正让 Agent 能长时间自主运行的,是验证。

Boris 表示,大家对验证的理解普遍有误。一提到验证,开发者想到的就是单元测试、lint 检查、类型检查。但 Agent 层面的验证完全是另一回事:**Agent 能不能自己跑起来,验证自己写的东西?**

他回忆了一个让自己震惊的瞬间:

> Opus 4 刚出的时候,我让 Claude 写一个功能然后自己测试。它打开了一个 Claude CLI,在 bash 里自己测试了自己写的功能。当时我就震惊了。

而现在,这已经是常规操作了,iOS 模拟器、Android 模拟器、桌面端的 computer use 循环跑验证,都不稀奇了。

Cat 在团队里的做法则更为实际。她主要做桌面应用开发,团队有个工程师写了一个「桌面开发 Skill」,教 Claude 怎么运行本地桌面应用。Claude 会用 computer use 在应用里点来点去,测试新 UX,发现 bug 就修,修完再验证。

遇到预发布环境的问题,Cat 甚至让 Claude 去读 Slack 看看是不是环境本身挂了。解决之后,再让 Claude 把经验更新到 Skill 里。

**一个自我进化的闭环。**

## 03 人人都在写代码

在视频里,Boris 特别兴奋地提到了一件事:**他的 PM(也就是 Cat)在写代码**。

> 我从来没在一个团队里见过 PM 会写代码,而且你的代码写得还挺好。

Cat 觉得这倒不奇怪了,因为 Claude 在写代码,人只需要有想法就行:

> 现在更重要的是你有什么 idea。如果你有产品 sense、有业务 context、懂设计和用户,你反而能做出更好的东西。

而这个现象,已经不只发生在 Claude Code 团队内部。

Boris 表示,他们在企业客户那里反复看到同一个模式:**先是工程师用上 Claude Code,然后旁边的人凑过来看了一眼,说「这东西好厉害,我也试试」。**

于是设计师开始直接在代码里改 UI,不用再找工程师排队、PM 直接在应用里改功能、财务团队在 Claude Code 里跑预测模型、数据科学家的屏幕上,也全是 Claude Code。

Boris 还记得第一次看到设计师 Megan 提 PR 时的反应:

> 我当时吓了一跳,「天哪 Megan 为什么在提 PR?」然后她说「我就是在修个按钮」。我一看代码……写得还挺好的。

**产品、工程、设计,这些角色的边界正在模糊。**

Boris 对此的判断是:未来每个人都既是 PM 又是工程师。产品团队写代码,DevRel 写代码,设计团队写代码。而工程师则越来越多地端到端交付产品,从想法到实现到发布到和法务、市场协调,一个人走完全流程。

## 04 Routines 的威力

Cat 分享了一个让她印象深刻的故事。

团队有个工程师负责 Voice Mode,在所有产品线上线了语音功能。他设了一个 Routine,自动监听所有关于 Voice Mode 的 GitHub issue 和 bug report。他的 Claude 会主动捡起这些问题,提交修复 PR,然后 ping 他去 review。

然后他想到:不只是 Voice Mode 的反馈需要回应,其他反馈也是。于是他又设了一个 Routine:**监控所有超过 5 小时没人回应的 bug report,自动提交修复。**

Cat 亲身体验了这件事的威力:

> 我发了一个小功能,有个边界情况我没注意到。有人报了 bug,我打算晚上去修。结果我的 Claude 告诉我:「等等,另一个 Claude 已经修了。」

她去找那个工程师问:「你怎么修这么快?」结果人家根本没手动修,是 Routine 自动处理的。

Boris 也说,Claude 现在经常告诉他:「别人的 Claude 已经修过了。」

> 回想一下以前,你得自己回复 code review 评论,自己修 CI,自己 rebase。这些我已经很久很久没做过了。

而 Routine 的意义不止于此。Boris 认为,Agent SDK 是让 Claude Code 可编程化的第一步,但一开始大家不知道拿它干什么。**Routine 是第一个「显而易见的应用场景」,它让 Claude 从同步工具变成了异步基础设施。**

## 05 最爱 Auto Mode

聊到最爱的功能,Boris 的回答有点出乎我的意料:**不是 plan mode,是 auto mode**。

> 更新的模型其实已经不需要 planning 步骤了。Opus 4 到 4.5 时期还需要,但从 4.6 开始,尤其是 4.7,模型直接就能干活。

Auto mode 的逻辑是:把权限判断交给另一个模型(Sonnet 4.6)去做安全审查,而不是让用户逐条点同意。

这个方案听着有些冒险。Boris 自己也说,第一次听到这个方案时他觉得不靠谱:

> 「把 prompt 路由给一个模型来判断安全性?不可能行的。」结果实际一试,效果出奇的好。

他们的安全论点其实很反直觉:**auto mode 比手动审核每一条权限提示更安全。**

> 人的本性就是这样,当你 99% 的请求都点同意时,眼睛就走神了。Auto mode 让你只关注真正重要的事情,而不是被一堆本来就该放行的请求淹没。

为了上线 auto mode,Anthropic 内部做了大量工作:收集成千上万条 Agent 运行轨迹,让 auto mode 分类器判断安全性;请红队人员做 prompt 注入攻击;让内部团队亲自尝试攻击 Claude Code 的 auto mode。

所有发现的问题都变成了 eval,用来持续提升安全性。

Cat 表示:

> 这不只是防范已知漏洞,而是防范我们能构造出的最聪明的攻击。

## 06 Loop 和手机编程

Boris 说,过去一年半经历了两次大的认知跃迁。

- 第一次:从「我写代码」变成「我跟 Agent 说话,Agent 写代码」。
- 第二次:从「我跟 Agent 说话」变成「我跟 Loop 或 Routine 说话,它来调度 Agent」。

> 我不再跟 Agent 直接对话了,我跟 Loop 对话,Loop 替我调度 Claude。一年半就经历了两次大跃迁,这速度太疯狂了。

现在 Boris 的日常工作方式也变了。以前他开 6 个终端标签,6 个 git checkout 同一个仓库,来回切换。

现在他就开一个标签,用 Agent View 看所有后台 Agent 的状态,用桌面应用,因为它会自动管理 worktree。

而最让他自己意外的是,**现在大概一半的工程工作是在手机上完成的。**

> 我会在电脑上启动一些 Agent,然后用 Remote Control 从手机接管。出去买杯咖啡,看看 Agent 的进展,可能再启动一个新 Agent。有时候跟人聊天聊出了一个 idea,直接用 Voice Mode 告诉 Claude 去做,都不用回电脑了。

Cat 记得 Boris 开始这么干的时候:

> 你会把电脑留在办公室,屏幕锁着,插着电,然后就走了。一开始我以为你忘拿了,第二天又这样,第三天还这样。但你一直在提 PR……后来你回复我说:「我在沙发上写代码呢。」

Boris 回应:那是 Remote Control 刚好用的那一周。

## 07 Context 极简主义

Cat 在视频里,问了一个企业用户经常问的问题:怎么做 context engineering?

Boris 的回答,有点点颠覆:

> 以前 Sonnet 3.5 时代你得做 prompt engineering,Opus 4 时代你得做 context engineering。但现在的模型,这些都不需要了。

他现在的做法是:**给模型最少的 system prompt,最少的 tools,然后让模型自己去找需要的 context。**

Cat 也持相同观点,她自称「context minimalist」:

> 告诉模型它需要知道的,剩下的让它自己搞定。给模型太多 context,就像在微观管理它。有时候模型知道更好的方法来达到同一个目标。

Boris 总结了几个正在发生的大趋势:Agent 运行时间越来越长,越来越自主,一次跑几十个、几百个甚至几千个 Agent 早就不稀奇了。

> 一年后的使用方式肯定跟现在完全不一样。如果一年后还是这些东西,我反而会觉得奇怪。

## 08 源码泄露风波

当然,还有个视频里没有聊到的 Claude Code 这一年经历的另一件大事。

2026 年 3 月 31 日,Anthropic 通过 npm 包 @anthropic-ai/claude-code v2.1.88 不小心发布了一个 59.8MB 的 JavaScript source map 文件。

安全研究员 Chaofan Shou 在 X 上公开了这个发现,瞬间引爆了整个开发者社区。

泄露的根本原因有点搞笑:Claude Code 基于 Bun 构建(Anthropic 在 2025 年底收购了 Bun),Bun 默认会生成 source map,但……没人在 .npmignore 里排除它。

**51.2 万行未混淆的 TypeScript 代码,约 1900 个文件,就这样暴露了。**

社区从中扒出了不少料:

- 一个叫 **KAIROS** 的未发布自主守护进程,源码中被引用了 150 多次。它能以后台 daemon 的方式持续运行,自动监听 GitHub webhook、发送推送通知,甚至有一个叫 **autoDream** 的功能,在空闲时自动整合记忆。
- 一个叫 **Undercover Mode** 的功能,约 90 行代码。它会在 Anthropic 员工操作非内部仓库时自动激活,去掉 commit 里的 Co-Authored-By 署名,禁止提及内部代号和未发布模型。
- ……这甚至还引发了关于 AI 匿名贡献开源代码的伦理讨论。
- 还有内部模型代号:**Tengu** 是 Claude Code 项目代号,**Fennec** 是 Opus 4.6,**Capybara** 疑似 Mythos 模型。
- 更有 **44 个隐藏功能开关,20 多个未发布功能**。

Boris Cherny 对此的回应是:

> 这是一个人为错误。没有人因此被开除,犯错的人仍然拥有公司的完全信任。这是一个流程漏洞,任何人都可能犯。

Anthropic 随后发了 DMCA 取消通知,但误伤了约 **8100 个仓库**,包括自家开源仓库的合法 fork。

后来不得不撤回大部分通知。

一个 mirror 仓库在被下架前积累了 **41,500 个 fork**,一个韩国开发者做了个叫「claw-code」的 Python 重写版,**2 小时内拿到了 75,000 个 GitHub star**,甚至还有人根据源码中一个稀有的 Claude Buddy 变体发了个 meme 币。

泄露之后,安全研究人员从中发现了多个严重漏洞(CVE-2025-59536、CVE-2026-21852 等),涉及 RCE 和 API token 窃取。这些在后续版本中被修复。

不过从另一个角度看,这次泄露也让社区第一次看到了 Claude Code 内部的工程复杂度:**40 多个注册工具,5 种 context 压缩策略,23 个 bash 安全检查,14 个缓存破坏向量。**

也算是另一种方式的开源了。

## 09 一年功能速览

最后,让我们快速过一遍这一年的功能里程碑:

| 时间 | 里程碑 |
|---|---|
| 2025 年 5 月 | 正式发布,搭配 Opus 4 |
| 2025 年 9 月 | Claude Code 2.0 发布(Checkpoints / VS Code 扩展 / Hooks 系统 / GitHub Actions 集成 / Agent SDK) |
| 2025 年 10 月 | 登陆网页端(claude.ai/code)+ 沙箱隔离 + Skills 系统 |
| 2025 年 11 月 | Opus 4.5 带来 67% 降价 + context compaction |
| 2026 年 1 月 | v2.1.0,1096 个 commit 合入,Skills 增强 + /teleport + 多语言 |
| 2026 年 2 月 | Opus 4.6 + Agent Teams + Remote Control |
| 2026 年 3 月 | Voice Mode + /loop + auto mode 登场;Routine 让 Agent 从同步变异步 |
| 2026 年 4 月 | 桌面应用重新设计 + Routines 正式发布 + worktree 隔离;Opus 4.7 默认模型 + push notifications |
| 2026 年 5 月 | Agent View 上线 + Opus 4.8 + Dynamic Workflows(可编排成百上千子 Agent 并行) |

**一年之内,从一个终端聊天工具变成了一个可以自主运行、自我验证、多实例协作的 AI 编程基础设施。**

## 10 下一年

在视频最后,Boris 说道:

> 一年后的使用方式如果还跟现在一样,我反而会觉得奇怪。Agent 运行时间越来越长,越来越自主,同时跑几百上千个 Agent 早就不稀奇了。下一年的形态,一定跟现在完全不同。

Cat 补充道:

> 这些想法不会只从我们这里来,而是会从整个社区里涌现出来。

从两个 Slack 点赞到人人写代码,Claude Code 用一年时间走完了大多数产品一辈子都走不完的路。

**Claude Code 对这个世界的改变,还在继续发生。**

## 相关链接(原文)

- YouTube 视频原片:https://www.youtube.com/watch?v=Hth_tLaC2j8
- Claude Code 官方文档:https://code.claude.com/docs/en/overview
- ClaudeDevs 推文:https://x.com/ClaudeDevs/status/2064032814392352816