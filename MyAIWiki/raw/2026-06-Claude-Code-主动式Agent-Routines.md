---
title: Claude Code：如何能构建主动式 Agent 工作流？
slug: Claude-Code-主动式Agent-Routines
date: 2026-06-17
obtain_date: 2026-06-17
author_team: Anthropic applied AI 团队(Maya)
source: 微信公众号 Capihom
source_url: https://mp.weixin.qq.com/s/kvtDAdTe2H4hTUXc3FEaVg
youtube_url: https://www.youtube.com/watch?v=eSP7PLTXNy8
event: Anthropic 内部演讲"Build a proactive agent workflow with Claude Code"
extraction: 微信 HTML 抽取 (id="js_content" 区段) ;清洗:去除头部字段/导语/公众号页脚/JS 代码
word_count_chars: 5605
paragraphs: 33
category: 02-ai-coding
tags: [主题/AI-Coding, 主题/Claude-Code, 主题/主动式Agent, 主题/工作流设计, 主题/Anthropic实践, 节点/Routines, 节点/主动式Agent, 节点/三大基础设施负担, 节点/最小配置, 节点/触发器, 节点/上下文=成功的上限, 节点/可转向性, 节点/渐进路径, 手法/反例论证, 手法/产品视角, 手法/工程框架, 场景/AI工作流, 场景/PM工具箱, 场景/Anthropic内部]
---

# Claude Code：如何能构建主动式 Agent 工作流？

> 原始来源:微信公众号 Capihom 2026-06-17 编译自 Anthropic applied AI 团队 Maya 的演讲"Build a proactive agent workflow with Claude Code"。
> 原文链接:https://mp.weixin.qq.com/s/kvtDAdTe2H4hTUXc3FEaVg
> 演讲原视频:https://www.youtube.com/watch?v=eSP7PLTXNy8
> 全文约 3900 字(微信公众号 Capihom 编译稿)。

"编码 agent 不该等你按下回车才开始工作。"

"我们想把 Claude Code 从今天的工具，变成明天的队友。"

"Claude 拥有的上下文，就是它能成功的上限。"

Maya 是 Anthropic applied AI 团队成员，一半时间做 Anthropic 自己的一方产品和功能，一半时间帮客户基于模型开发产品、功能和 agent。她讲的是 Anthropic 自己在 Claude Code 里推出的 routines：让 Claude Code 可以按日程、GitHub 事件或 webhook 主动启动远程会话，读 repo、接工具、开 PR、发 Slack 通知。产品负责人和 PM 能从这里看到一条清晰变化：AI 提效正在从“我会不会写好 prompt”，走向“我能不能把稳定流程设计成可触发、可观察、可校验的系统”。当一个流程能被写成触发器、上下文和校验方式，它就不再只是某个人的熟练手法，而会变成团队可以复用的生产机制。Maya 没有把 routines 描述成单点功能，她反复把它放在团队协作里：谁有权限、读哪些 repo、什么事件触发、结果发到哪里、人在什么时刻介入。对正在搭 AI 工作台的团队，这比多学十个提示词更接近组织能力。

从按下回车，到任务自己启动

Maya 开场问台下有多少人把 Claude Code 跑在 cron 上，很多人举手；再问有多少人享受维护那套基础设施，只有后排一位还举着手。Anthropic 内部也遇到过同样的痛点：Claude Code 已经能写代码、查文件、改 PR，但很多团队想要的下一步，是让它在合适的时间自己开始工作。工具等待人输入，队友会在问题出现时先动起来。 routines 就是围绕这个差别设计的：你定义 prompt、repo、连接器和触发器，剩下的远程会话由 Claude Code 承担。Maya 用一句话把产品目标说得很清楚：Claude Code 今天是强大的 coding tool，团队希望把它变成明天的 coding teammate。这个转变落到产品工作里，意味着 AI 的入口会从聊天框扩展到日历、GitHub、Slack、发布流水线和客户反馈渠道。PM 过去常把“自动化”理解成一段脚本或一套运营 SOP，现在要学会把任务启动条件也设计进去。谁来触发、触发后读什么、做完后通知谁，都会影响最后的产品体验。

"编码 agent 不该等你按下回车才开始工作。"

产品团队要先拆掉三层基础设施负担

Maya 把主动式 agent 的难点拆成三件事。第一，agent 跑在哪里。放在本地电脑上，合上笔记本或者电量耗尽，会话就断了；团队还得处理托管、持久化和鉴权。第二，什么时候触发。cron、endpoint、事件监听都能做，但每一种都要搭一圈胶水代码。第三，人怎样介入。很多 headless Claude Code 会话跑起来以后，很难实时看到它在做什么，也不方便观察、转向、设边界或恢复。产品经理如果只把 AI 当成一次性输入框，最后会把大量时间花在工作流外围。 她提到的 hosting、data persistence、authentication，其实都是产品团队过去不太愿意碰的部分；可一旦工作流要自动运行，谁负责鉴权、谁保存会话状态、谁在异常时接手，就会变成产品设计的一部分。一个能跑起来的 agent，需要产品、工程和运维一起确认边界。否则团队会得到一个会启动的自动化，却得不到一个能放心交接的流程。

"你需要在 prompt 之外搭出一整套基础设施，这当然能做，但工作量很大。"

Routine 的最小配置只有四样东西

routines 的配置故意压得很低：prompt、连接的 repo、可用连接器、触发器。会话运行在 Claude Code 的托管基础设施上，笔记本开不开都不影响它继续干活；触发方式可以是时间表，也可以是 GitHub 事件，甚至可以通过团队自己的 webhook 把事件 payload 作为上下文传进去。更重要的是，每个 routine 底层仍是一段 Claude Code session。团队可以在 web、CLI 或 desktop 打开它，看它正在读哪些文件、怎么判断，还能继续追问或把会话恢复到新的方向。这里的产品含义很直接：AI 自动化不必做成黑箱后台任务。它可以像一个可打开的协作文档，记录自己接到的初始指令、读取过的仓库、比较过的 changelog，以及最后创建的 PR。Maya 展示的页面里，routine 左侧列出连接资源，右侧保留指令文本，session 里能看到 Claude 从源码仓库、变更记录和文档仓库逐步查起。可观察性留在产品里，团队才敢把更多重复任务交给它。

"每个 routine 其实都是底层的一段 Claude Code 会话，你可以打开、观察、跟进、转向和恢复。"

Anthropic 先拿文档同步开刀

Maya 给出的内部案例很具体：Claude Code 的每周 PR 数从年初以来增长了 200%。新功能来得更快，用户当然开心，工程团队也开心；压力落到了负责维护 Claude Code 和 agent SDK 文档的工程师 Sarah 身上。Sarah 设置了一个每周 routine：每周读取 main 分支的新变化，对照文档 repo，如果发现文档需要更新，就开一个 PR。她在终端里输入 `/schedule`，再写下“每周审查 main 上的新变化，对照文档 repo，如有变化就创建文档更新 PR”。Claude 接着追问运行时间、PR 创建后是否通知 Slack，回答完，routine 就生成了。Maya 在网页端展示这个 routine 时，左侧能看到它连接了两个 repo，运行时间是每周一上午十点，并且接入 GitHub 和 Slack；右侧指令则由 Claude 根据初始 prompt 和后续回答生成。进入某次 session 后，Claude 已经读完指令，开始查看 source code repo 最近合并的 PR 和 changelog，并和 documentation repo 里的内容做比较。最后它发现了需要补充的文档变化，并打开了一个 PR。

"Claude Code 的每周 PR 数从新年开始已经增长了 200%。"

触发器决定 agent 什么时候上班

Maya 要求团队在创建 routine 时先回答第一个问题：什么时候触发。文档同步可以每周一上午十点跑一次；发版时也可以在 release branch 与文档之间做 diff；工程师合并带有 `need docs` 标签的 PR 时，也能让 GitHub 事件启动 Claude Code。把这套思路放到产品团队，触发器可以是每周 backlog review，可以是高优先级 issue 创建，可以是用户反馈进入 Slack 频道，也可以是一次部署完成后的健康检查。好 workflow 的第一步，往往在于定义“哪件事发生时，AI 应该开始工作”。 触发器越具体，越容易把任务边界收紧：一条 issue 打开、一个 label 合并、一次 release cut、一次 CD pipeline post，这些事件都比“帮我看看最近有什么要做”更适合交给 agent。Maya 现场还创建了一个 GitHub issue trigger：只要文档 repo 里有新 issue 打开，Claude 就拿着 issue 里的上下文启动调查。这个用法很适合需求池：当客户反馈被打上某个标签，routine 先读相关 issue、历史 PR 和当前文档，给 PM 一份可追溯的初步判断。

"第一项决定，是你的 routine 应该在什么时候触发。"

上下文决定 agent 能做到哪一步

第二个问题是上下文。Sarah 的文档 routine 需要同时读 Claude Code 源码 repo 和文档 repo，才能知道哪些功能已经改了，哪些页面需要跟着改。Maya 还提到另一种情况：如果希望 Claude 沿用 Anthropic 对外营销材料里的语言，就可以接 Google Drive；如果 PR 创建后要提醒人，就接 Slack。PM 做需求分拣时也是同一套逻辑：GitHub issues、Slack 用户反馈、已有 roadmaps、客户访谈纪要、数据看板，缺哪一块，Claude 的判断就会卡在哪一块。Claude 拥有的上下文，就是它能成功的上限。 很多团队觉得 AI 判断不稳定，Maya 这一段给了一个更工程化的解释：问题可能不在模型态度，而在流程没有把必要信息接进来。缺少源码，它无法判断功能变化；缺少文档 repo，它开不了 PR；缺少 Slack 或邮件，它无法把结果送到人手里。PM 在设计 agent 工作流时，也要像写需求一样列清楚输入源、权限、输出位置和通知对象。比如一次用户反馈归类，需要反馈原文、账号信息、历史工单、相关功能代码和当前 roadmap 同时在场。

"无论 Claude 拥有什么上下文，那就是 Claude 能成功的上限。"

可转向，才敢让 agent 多跑几步

第三个问题是 steerability，也就是如何让 Claude 保持诚实。Maya 提到两种做法。第一种是 agent-on-agent review：一个 routine 创建文档 PR，另一个 routine 在 PR 创建后做 reviewer，先留下评论，再交给人看。第二种是人在中途进入会话，像使用终端里的 Claude Code 一样查看当前分析，提出问题，把方向推回正确轨道。她现场演示了一个 GitHub issue 触发的文档 routine：issue 一创建，新 run 被拾取，issue 内容自动进入初始上下文。Maya 发现自己已经有另一个 PR 处理了同样问题，就直接让 Claude 停止会话。这个细节很重要：主动式 agent 的成熟形态并不要求人消失。更健康的形态是人能看到它为什么启动、读了什么、准备做什么，并且能在它开错路时立刻叫停。Anthropic 在文档场景里还会渲染 Claude 修改过的页面，确认输出符合预期；这一步把“相信模型”变成了“检查结果”。产品团队也可以照着做：让一个 routine 起草变更，让另一个 routine 按验收标准挑问题，人最后只看差异和证据。

"你可以在实时会话里问它问题，把它推向另一个方向。"

PM 可以先把 backlog 变成 routine

Maya 在结尾把 routines 推到更宽的团队场景：部署验证、on-call 调查、backlog 分拣。她举了一个 PM 场景：如果工作里要反复翻很多 GitHub issues 或 Slack 帖子，可以设置一个每周 job，让 Claude 读取这些问题，帮助排序，必要时为最重要的问题打开 PR。产品团队可以把这件事拆成三步：触发器是每周固定时间；上下文是 GitHub、Slack 和问题所在系统；转向方式是先让 Claude 给出调查和优先级，再由人决定是否进入执行。产品视角里的提效，是把重复收集、对照、起草和通知交给会按时出现的 agent，同时保留最终取舍。 她还举了 deploy verifier：CD pipeline 每次部署后向 webhook 发请求，Claude 读取服务源码和 DataDog、Grafana 等监控工具，先给出是否 rollback 的 no-go / go decision；当团队信任增加，再让它参与回滚动作。这里的渐进路径很务实：先让 Claude 做调查和建议，再把行动权限一点点放出去。Maya 说得很直白：proactive agents beat reactive agents。主动式 agent 的价值，不在一次性回答更漂亮，而在它能在问题出现时先开始调查。一个 PM 每周少翻几十条 issue，省下来的注意力才会回到排序和取舍。

"也许你是一名 PM，你的工作是处理 backlog 里的大量 issue。"

写在最后

如果你想把这期的方法带回团队，先别急着设计宏大的 agent 系统。挑一个每周都重复、输入来源稳定、结果需要人确认的流程：文档同步、issue 分拣、发布检查、用户反馈归类。先写清楚触发器，再补齐上下文，最后保留一个能看见、能追问、能暂停的入口。Claude Code routines 的启发就在这里：主动式 agent 不一定要替你做最终判断，它可以先替你把该开始的工作准时启动。流程先跑起来，团队再逐步决定哪些地方继续让人把关，哪些地方可以交给 agent 多走一步。Maya 最后的提醒很朴素：一条 `/schedule` 命令，就能开始创建第一个 routine。真正难的部分，仍然是团队对自身流程的清楚理解。先把一个小流程跑顺，比一次设计十个自动化更稳。下周一让它先读 backlog、列证据、开草稿 PR，就已经能改变团队节奏。小处先赢，系统会慢慢长出来。先试试。

内容来源："Build a proactive agent workflow with Claude Code"丨Claude

原视频：https://www.youtube.com/watch?v=eSP7PLTXNy8

⇣ 关注我，每天为你更新硅谷最新的 AI 创业／科技播客总结，让你与前沿保持同频 ⇣

---

## 备注

- 本次抓取清洗范围:id="js_content" 区段到 var first_sceen 标记之间(425217 偏移前)
- 已去除:头部字段(作者/导语/推广)、公众号页脚推广语、嵌入的 JS 段
- 原始内容:Anthropic 演讲浓缩稿,Capihom 编译,含 8 章 + 引言 + 写在最后
- 段落编号:1-33 段,共 5605 字符
- 标签:#主题/AI-Coding #主题/Claude-Code #主题/主动式Agent #主题/工作流设计 #主题/Anthropic实践 #节点/Routines #节点/主动式Agent #节点/三大基础设施负担 #节点/最小配置 #节点/触发器 #节点/上下文=成功的上限 #节点/可转向性 #节点/渐进路径 #手法/反例论证 #手法/产品视角 #手法/工程框架 #场景/AI工作流 #场景/PM工具箱 #场景/Anthropic内部
