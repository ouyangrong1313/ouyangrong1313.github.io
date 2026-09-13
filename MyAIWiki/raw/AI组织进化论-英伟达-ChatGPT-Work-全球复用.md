# 英伟达最新团队AI实践：搭工作流、全球复用，每周省出16小时

**来源：** 微信公众号
**作者：** AI组织进化论
**日期：** 2026-08-20
**链接：** https://mp.weixin.qq.com/s/2q72atboegdmWIyCMl4xdA

---

## 正文

英伟达这次案例的经验核心已经是把 AI
嵌进工作流
本身：自动化重复劳动、跨团队共享流程、持续迭代。
8月18日，OpenAI在官方最新放出英伟达采用GPT应用案例，值得看看。
案例提到，在英伟达（NVIDIA），ChatGPT 正在帮知识型员工把"整理信息"的时间，换成"采取行动"的时间。
对于 GTM（Go-To-Market，市场拓展）和解决方案架构师（Solutions Architect）团队来说，ChatGPT 已经深度嵌入工作流的组织、自动化与规模化——GTM 团队用它改造重复性运营流程，解决方案架构师则用它把快速变化的外部动态，和英伟达的内部优先级连接起来。
这不是我们经常谈的"试点"，而是一个
已经跑通、正在扩散
的故事：一个工作流每周自动运行两次，在 12 周的筹备周期里省下上百小时；另一套工作流每周把 25–40 条外部 AI 更新蒸馏成 5–8 条可行动信号。更重要的是，这些流程正在被复制到全球其他区域的团队里。
下面我们拆开来看：英伟达到底是怎么用 ChatGPT Work 的，以及这背后的方法论，对你我有什么参考价值。
先搞懂背景：ChatGPT Work 是什么
简单说，ChatGPT Work 是面向企业团队的工作场景——它不只是一个"聊天窗口"，而是可以把重复性任务固化成
可复用、可共享、可自动运行的工作流（Workflow）
：定期抓取数据、按规则分析、产出结构化结论、推送给对应的人。员工自己就能搭建和修改，不需要专门等 IT 部门开发工具。
英伟达案例里的两位主角，恰好代表了两种典型用法：
一种是把"苦活累活"自动化（运营提效），一种是把"海量信息"变成情报（决策提效）
。我们用一张图先看全貌。
一、把时间还给客户：一场 12 周的"省时实验"
Will Daney 负责支持英伟达全球销售、业务拓展与产品负责人执行和衡量战略。他的一项常规工作是服务 GTC（NVIDIA 的全球 AI 大会）背后的一线团队（field team）。
过去，筹备 GTC 需要在电子表格里做大量手工活：整理客户名单、跟踪报名进度、帮团队梳理为客户和伙伴创造优质体验所需采取的动作。大会筹备期间，Will 估计
手动分析约占他 40% 的时间
——这意味着大量本该用来理解客户的时间，被消耗在了搬数据上。
如今，他把大部分工作变成了一套
每周自动运行两次的 ChatGPT Work 流程
。在长达 12 周的 GTC 筹备周期里，这套工作流帮他
每周省下约 16 小时
，相当于每个工作日多出 3 个多小时。
"我能把时间还给真正的一线团队，更了解他们，帮他们想清楚如何让客户更成功。"Will 说。
更关键的是：因为他自己拥有这套工作流，活动需求一变，他就能随时调整，
不用等公司采购、上线、维护一个新工具
。他还能把底层流程分享给其他地区的团队——支持圣何塞、台北、欧洲和华盛顿特区的同事，都已拿到他的 ChatGPT 工作流，并按本地需求做了定制（customized for their local needs）。
"用 ChatGPT，我觉得真正的关键是：我能把一个已经开发好的工作流，一场活动接一场活动地自动化复用，几乎零额外成本。"
"With ChatGPT, I think the real key is that I'm able to take a workflow I've already developed and automate it event over event with little to no overhead."
—— Will Daney，英伟达 Go-To-Market 策略师
二、在快速变化的行业里捕捉信号：从"阅读"到"情报"
Rachita Jain 在英伟达市场部的 AI 运营（AI Operations）团队工作，负责搭建 AI 工作流、帮团队采用新工具。她的挑战是：这个行业每天都有新模型、新基准、新研究冒出来，怎么跟得上？
信息本身唾手可得，难的是判断
哪些动态对英伟达真正重要
，并把它们与内部项目、讨论和优先级联系起来——这正是她口中"信息过载"（information overload）问题的核心。
Rachita 用 ChatGPT Work 搭建了一套工作流：
审阅可信外部信源（trusted external sources）+ 内部上下文（internal context），识别有意义的交集，输出可供行动的洞察。
"ChatGPT 帮我把被动阅读，变成了主动情报。"她说。这句话值得划重点：
同样的信息，以前是"看"，现在是"用"
——信息不再是负担，而是决策的输入。
同一个环境还支撑着完整的构建过程：从一个想法出发，探索可行方案、跑通代码库（codebase）、调试问题、打磨结果，全程不用在彼此割裂的工具之间来回切换。那些曾经只能停留在"side project"的想法，如今几天内就能长成能用的产品。她有一个案例：
从想法到可用原型只用了 3–5 天
，而如果手动跨工具搭建，估计要 2–3 周——效率提升约 4 倍。
"我想解决的最大问题是信息过载——一切都在飞速变化，跟踪所有更新一天比一天难。有了 ChatGPT，这件事变得简单多了。"
"I think the biggest problem I'm trying to solve is information overload, because everything is moving so fast. It's getting harder by the day to keep track of all the changes. And with ChatGPT, it becomes much simpler."
—— Rachita Jain，英伟达解决方案架构师
三、下一步：把已经跑通的，规模化复制
接下来的机会，是把已经验证有效的打法规模化。把专业知识沉淀成可复用工作流，让英伟达各个团队能在不同职能、不同活动、不同地区之间复用成熟流程——同时把流程演进的掌控权，留给最贴近业务的人（keeping the people closest to the work in control）。
随着 AI 版图不断变化，这些共享工作流能帮英伟达更快地把外部动态与内部优先级连起来，让更多员工用上 AI 驱动的工作方式（AI-enabled ways of working）。最终目标很朴素：给团队更多时间去解读发现、协作，专注在真正服务客户的事情上。
这种潜力在 Will 身上已经显现：
"ChatGPT 对我来说真的是一个乘数效应（force multiplier），"他说，"
感觉就像有一支团队在替我干活。
它帮我跳出琐碎的泥潭（get out of the weeds），专注在真正重要的工作上。"
"ChatGPT has really been a force multiplier for me personally. It feels like I have a team working for me. It's helped me get out of the weeds and focus more on the work that matters."
—— Will Daney 原话
四、案例三条可执行启示
1️⃣
盘点你或团队的"40%"
：找出每周最耗时、最重复的任务，试试把它变成一条自动运行的 prompt 工作流，而不是只问一次。
2️⃣
给信息装一个"漏斗"
：如果你每天被迫阅读大量行业信息，试着让 AI 先做交叉比对和筛选，你只看最终的"可行动信号"。
3️⃣
把流程"送出去"
：你搭好的工作流，同事能不能直接用？分享 + 定制，才能把个人效率变成团队能力。
英伟达这次案例的经验核心已经是把 AI
嵌进工作流
本身：自动化重复劳动、跨团队共享流程、持续迭代。
ChatGPT 的价值，最终体现在
人省出来的时间上
——省下来的每一小时，都在流向更接近客户、更有创造力的工作。就像 Will 说的：
"It feels like I have a team working for me."
OpenAI原文链接：
https://openai.com/index/nvidia/chatgpt-work/
📍关注AI组织进化论｜赋能AI组织转型
AI转型升级中，我们也坚信人是终极变量，而管理者则是关键杠杆。因此我们设计了一门面向AI时代管理者的
《极简AI领导力-成为AI原生管理者》
课程，聚焦
如何领导AI，而不仅仅个人使用AI
，帮助管理者快速掌握推动团队AI落地的核心框架、方法与工具，推动团队AI升级。
适合管理者、技术负责人、产品负责人、HR、OD 及数字化转型相关伙伴，欢迎私信交流。
其他推荐阅读：
案例PPT｜谷歌最新六大机制：AI时代如何对抗大公司病，重塑产品力
AI重写组织：一种新形态正在出现——认知型组织（含PPT）
如何领导AI和人？一文说透人机协同五种模式及应用流程（含PPT）
如何打造AI原生团队？以技术研发为例（含PPT）
人机协同下，如何培养人才？一文讲透AI时代能力发展新范式（含PPT）
从个人提效到团队提效，要迈过三道门槛（含PPT）

---

标签： #主题/AI工作流 #主题/组织提效 #主题/ChatGPT-Work #主题/信息情报 #主题/流程复用 #场景/公众号长文
