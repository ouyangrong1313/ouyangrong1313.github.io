---
title: 未来属于垂直领域 Agent丨AI Engineer
公众号: 晚点再听LaterCast
原始作者: Justin Schroeder(StandardAgents CEO / Dmux / ArrowJS 作者)
来源: AI Engineer 大会演讲 "The Future Is Domain-Specific Agents"
原视频: https://www.youtube.com/watch?v=spNAUEgq_A8
原文微信链接: https://mp.weixin.qq.com/s/PEoe-AuccFxXplyqoRmFNA
发布时间: 2026-07-03(微信公众号)
获取时间: 2026-07-03 10:54 Asia/Shanghai
抓取方式: curl + Chrome UA + Python 正则清洗
---

> **全文约 4000 字**

## 编辑导读

> "2027 年,基本上会是多 Agent 编排之年。"
> "Token 已经不再变便宜了。"
> "你会得到一群高效的小 Agent 协同工作,而且每个都保持很小的上下文窗口。"

企业里的 AI 项目很容易先变成一个长长的工具清单:接邮箱、接表格、接 Figma、接 Salesforce,再把权限、数据、日志和审批塞进同一个大 Agent。演示时一切顺利,进入真实办公室后,IT 团队开始盯着环境变量、运行时、观测日志和权限边界发愁。

AI Engineer 这场演讲来自 Justin Schroeder。他在 StandardAgents 做一套仍处于早期的 Agent 生态,也维护过 Dmux、ArrowJS 等面向 coding agent 的开源项目。他给出的主张很直接:未来的企业 Agent 可能不会沿着"一个大模型吃下所有工具"的路线长大,而会拆成一组更小、更专、更容易控制的 domain-specific agents。

---

## 一、企业先卡在集成,模型智商排在后面

房地产中介、私人保险经纪、Fortune 500 公司都在尝试自建 Agent。Justin 的观察来自普通公司里的需求:业务数据已经在 CRM、表格、邮件和内部数据库里,员工希望 AI 能直接进入那些地方干活。

> "Agent 是确定性软件,它把模型产生的非确定性结果,用在某个目标上。"

难点也从这里开始。一个能跑 demo 的 Agent,离稳定进入生产环境还差很远。Agentic loop 要能被编排,供应商抽象要能切换,故障后要能从中断处恢复,停止条件和验证逻辑也要清楚。到了规模化阶段,每一步到底传了什么、调用了什么、为什么偏离预期,都要被记录和诊断。

办公室里能说出 Claude 或 Codex 名字的人已经变多,能解释 Agent 到底是什么的人还很少。业务部门却已经开始动手,原因很现实:如果 AI 不能读公司自己的数据,不能操作已有软件,单纯聊天再聪明也进不了日常工作。自建 Agent 成了很多团队第一眼能想到的入口。

生产环境的麻烦会很快暴露。Justin 提到 provider abstractions、durable execution、validations、stop conditions,还点名 Vercel AI SDK 和 Eve 这类新工具。企业要的交付物包括故障后能恢复、日志能追、权限能审、同一套 Agent 换机器还能跑。

他还把 Agent 和 harness 的边界放得很松:只要一段确定性软件能拿模型输出去追逐某个目标,就已经进入 Agent 的范畴。这个定义对企业很要紧,因为多数内部项目并不会先做一个人格化助手,而是先写一套能调用模型、工具和数据的运行壳。

---

## 二、把工具全塞进去,大 Agent 会越跑越重

MCP 给企业提供了一条很顺手的路:把公司工具分发给 Claude、ChatGPT 这类通用 Agent。Justin 承认它能用,尤其适合把企业里的信息和工具接进去。但他翻到 MCP 网站上的支持矩阵后,看到真正完整的一列主要是 tools。MCP 在很多场景里变成了工具分发机制。

Skills 也类似。一个 markdown 文件能像文档一样告诉 Agent 某件复杂事怎么做。少量 skills 很好用,数量上来以后,模型每次都要背着更多说明、更多工具 schema、更多消息历史去行动。工程里有个老词叫 inheritance:给一个对象不断叠属性,让它获得更多行为。今天很多 Agent 集成,正沿着这条路膨胀。

> "我们不是靠给一个人一堆工具,把送上月球的。"

五个 skills 还能忍,五十个、一百个、一千个以后,收益会递减。Figma、Playwright、Gmail、Google Sheets、差旅、报销、React 修复器、GitHub skill 全挤在同一个上下文里,主 Agent 每次行动前都要带着一大包无关材料。对于企业团队,延迟、费用、误调用和权限风险会一起上涨。

Justin 把一个基础 Agent 拆成几层:底部是模型,上面有 system prompt,随后是工具、skills、MCP,最上方还有整段对话消息。几乎每一层都会进入上下文。团队以为自己在"接入能力",运行时看到的却是一份越来越长的随身包袱。

一个普通员工的桌面就能把这件事讲清:差旅 MCP、Figma、Playwright、Gmail、Google Sheets、报销表、React lint、GitHub skill,全都进入同一个执行环境。用户只问"帮我安排洛杉矶行程",Agent 却背着设计、代码和报销的说明上路。

这也是很多内部 Agent 停在 demo 的原因。开发者把大学聊天机器人做出来以后,很难把它复用到另一个任务上;本机跑通的 Agent,交给同事时又卡在环境变量、运行时和系统依赖。可移植性和可组合性没有解决,工具清单越长,维护的人越累。

Skills 带来的副作用也在这里。Justin 提到已有研究显示,装太多 skills 会让 Agent 明显变差。原因不难理解:文档越多,模型越容易在不相干规则之间来回切换;每次任务只需要一个窄工具,却要先读完整个杂货架。

---

## 三、组合路线:让每个小 Agent 只懂一件事

Justin 借用了软件工程里的另一句老话:composition over inheritance。放到 Agent 上,就是别再给同一个 Agent 继续加说明书和工具箱,而是拆出一个 Figma Agent、一个 Gmail Agent、一个 Travel Agent、一个 Sheets Agent。每个小 Agent 都有自己的 system prompt、工具、消息历史和 agentic loop。

> "组合是继承的替代方案。"

Figma Agent 只需要知道 Figma 的 API、点击位置、鼠标动作和必要上下文。Gmail Agent 只处理邮件。Travel Agent 只处理行程。上面再放一个 coordinator,像团队主管一样分派任务。主 Agent 想查周末去洛杉矶的邮件,就把问题交给 Gmail Agent;确认有行程后,再叫 Travel Agent 做预订。

沟通方式也不神秘。小 Agent 和大 Agent 之间用自然语言传递结果,像人类团队开口协作。Justin 用阿波罗登月打比方:NASA 让一组专家各自掌握有限工具,再通过消息协同。某个人的大脑像 LLM,面板上的按钮像 tools,嘴巴负责 messages。

这个类比很适合企业落地。一个财务 Agent 不必懂设计稿,一个 Figma Agent 不必保留整段销售邮件,一个旅行 Agent 也不该拿到法务材料。角色切小之后,每个执行单元能用更短的提示、更少的工具、更干净的消息历史完成自己的那一步。

Justin 特别强调,小 Agent 不是一个只暴露工具的服务器。它是完整 Agent,有自己的消息历史和循环。这个差异会影响产品设计:调用 Figma Agent 时,主 Agent 不需要知道所有按钮细节,只需要把目标说清楚,再接收完成后的结果。

消息历史也会随之变短。Gmail Agent 处理邮件时,只保留邮件任务有关的对话;Figma Agent 处理画布时,只保留设计操作有关的上下文。主 Agent 得到的是结果摘要,像同事回话一样,而不是每个子任务的全部中间噪音。

---

## 四、小而专,先省下上下文和权限焦虑

StandardAgents 内部已经在使用这套形态。Justin 给出的一个数字很具体:在定义好任务边界后,单个任务经常能看到超过 80% 的 token efficiency。原因很朴素:Gmail Agent 接到"取 Debbie 最近那封邮件"时,不需要整段对话历史,也不需要 Figma、报销和代码工具的全部说明。

成本账也会改变。他拿 DeepSeek V4 Flash 和 Fable 5 作对比,前者单任务便宜 137 倍。小模型无法胜任所有任务,可是一个被限定在窄域里的 Agent,只要完成被挑选过的动作。图像生成、扩散模型、非语言模型也能被放进更细的任务单元里。

> "对于任意给定任务,我们经常看到超过 80% 的 token efficiency。"

IT 团队在意的权限边界也更清楚。一个大 coding agent 理论上什么都能做,员工只能靠弹窗和审批兜底。窄域 Agent 只能做已经被批准的一组动作。它可以并行跑在云上,在不同区域开成千上万个实例,也不必把整家公司的上下文塞进同一个执行环境。

价格曲线也给了这条路线更强的压力。Justin 说,很多人还相信 intelligence cost 会继续下降,但他们跟踪的数据在 2026 年出现反转:按 IQ 调整后,token 今年已经上涨 29%;不按 IQ 调整,涨幅达到 76%。当企业想把 AI 放到客户面前,巨型模型的单次费用会把很多场景挡在门外。

前台场景对这笔账更敏感。内部员工每天少跑几次还可以忍,客户对话一旦规模化,单次调用费用、响应时间和失败重试都会被放大。窄域拆分让团队可以把高价模型留给少数难题。

预算讨论因此会从模型排行榜回到任务清单。哪些步骤需要强推理,哪些步骤只是在读写文件、查邮件、生成表格,拆清楚以后,工程团队才有机会把体验和费用同时压住。

客户生命周期金额足够高时,昂贵模型还能被摊薄;普通客服、销售跟进、内部审批和资料生成没有这么宽的预算。窄域 Agent 的意义就在这里:把好模型留给需要推理的环节,把确定动作交给小模型、工具函数或专门子 Agent,少花钱也少暴露权限。

权限部分也更像企业能接受的控制面。今天很多人为了让 coding agent 顺利干活,会连续放过权限弹窗,像 Justin 说的那样"飞得离太阳很近"。窄域 Agent 的动作少,凭证少,失败面也小,审批策略可以按任务拆开,而不是围着一个全能助手打补丁。

---

## 五、2027 年,企业会开始谈多 Agent 编排

Justin 的判断很明确:2026 年下半年,围绕 domain-specific agents 的框架、讨论和产品会快速增多;2027 年会成为 multi-agent orchestration 被频繁提起的一年。Vercel 发布 Eve 时,他看到官网文案里出现了 company brain、personal assistant、domain-specific agent,觉得这个词终于从自己的演讲里走进了更大的开发者语境。

> "2027 年,我会说基本上是多 Agent 编排之年。"

他还补了一张更底层的理想结构图:每个 Agent 都该有自己的文件系统和沙盒代码执行位置。工具层里可以有函数、prompt、完整的子 Agent;hooks 可以注入时间、触发副作用;rules 负责限制回合数、验证要求和停止条件。这样打包起来,才像一个可迁移的小执行环境。

文件系统和沙盒执行不是装饰。用户让 ChatGPT、Claude 或 Codex 做一份生日派对 PDF 时,它们都会在自己的小文件区里生成、运行和保存。企业版的窄域 Agent 也需要同样的原语,只是边界更清楚、权限更窄、产物更容易审计。

销售团队的例子最容易理解:顶层 coordinator 下方有 Salesforce Agent、Google Workspace Agent、素材生成 Agent、法务 Agent。法务 Agent 下面还能再拆 GDPR 合规 Agent、OSHA 合规 Agent。每个小 Agent 保持短上下文,只拿自己需要的凭证和工具,在协作链条里交付一个清晰结果。

素材生成 Agent 可以拥有 Nano Banana、SVG generator 和自己的 QA 逻辑;Salesforce Agent 拿销售数据;Google Workspace Agent 生成表格;法务 Agent 只检查输出里的合规风险。递归子 Agent 继续向下拆,直到 GDPR 或 OSHA 这样的窄任务拥有自己的小执行单元。

企业如果现在开始试,不必先等一个完整平台成熟。更实际的做法是挑一条高频链路,列出每一步需要的数据、凭证、工具和验证规则,再判断哪些步骤应该独立成小 Agent。拆得足够窄,失败位置才会清楚;边界足够明确,IT 才敢让它靠近真实业务。

hooks 和 rules 也是这张图里容易被忽略的部分。模型不知道当前时间,就用 hook 注入一条人工消息;一次工具调用后是否必须验证、一个回合能跑多少步,则交给 rules。企业 Agent 真正进入生产时,这些小开关往往比模型名更决定稳定性。

---

## 写在最后

下一次设计企业 Agent,可以先画一张任务拆分图:哪些动作只需要邮件,哪些只需要 CRM,哪些必须走法务。别急着给一个大 Agent 继续加工具。把边界缩小,很多成本、权限和稳定性问题会提前浮出来。

---

**内容来源**:"The Future Is Domain-Specific Agents - Justin Schroeder, StandardAgents"丨AI Engineer
**原视频**:https://www.youtube.com/watch?v=spNAUEgq_A8
