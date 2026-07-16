# AI-Native 企业：Agent 团队和 AI Factory 会怎么重写公司体系（Augmented U · 编译稿）

- **原始链接**：https://mp.weixin.qq.com/s/LkMuNLTHRHTFJUYD6iAyaA
- **公众号**：晚点再听LaterCast（og:author: Capihom）
- **作者署名**：Capihom（微信公众号，硅谷 AI 创业与科技播客总结类）
- **一手来源**：Augmented U 节目《Building the AI-Native Enterprise, Agent Crews and the AI Factory | Interview with Masha Sharma》
  - 原视频：https://www.youtube.com/watch?v=pQj8qOyan-Q
- **受访嘉宾**：Masha Sharma（Groupon VP of Engineering，工程师 + 产品 + CTO + 创始人背景；曾在 Avenue One 把公司做到 10 亿美元估值；现负责把 Groupon 商家体验改造成 AI-first growth engine）
- **发布时间**：2026-07-07
- **获取时间**：2026-07-07 11:27 Asia/Shanghai
- **全文长度**：约 4000 字（原文标注）
- **正文长度**：5735 字符（清洗后）

---

## 正文

我们每天为你更新硅谷最新的 AI 创业与科技播客总结，让你与前沿保持同频。全文约 4000 字，如果你现在没有时间，试试转成播客稍后再听晚点再听LaterCast

> "AI 原生意味着，工作由 Agent 完成，人类负责指挥和审阅。"
> "每个职能都要会构建，这是我们的要求。"
> "不要把你对 AI 的理解委托给团队。"

公司里最容易被低估的 AI 变化，常常不在模型发布会上。它发生在一个销售同事能不能自己搭 lead research 仪表盘，一个 PM 能不能直接问代码"这里有没有 hard-code"，一个小商家能不能从想法到上线活动只花几分钟。

这期 Augmented U 的嘉宾是 Masha Sharma，Groupon 的 VP。她做过工程、产品、CTO 和创始人，也曾在 Avenue One 帮公司做到超过 10 亿美元估值。现在，她的任务是把 Groupon 的商家体验改造成 AI-first growth engine。整场访谈绕着一个问题展开：组织里的工作到底由谁来做。

### AI-native 先改组织图

Groupon 给自己的时间表很硬：到 2027 年成为 AI-native 公司。在这套定义里，任务开始交给 Agent 执行，人负责指挥和审阅。产品结果可能还是那个结果，组织图已经开始变形。

> "AI 原生团队里，每个职能都要构建。工程、产品、销售、市场、运营，都要通过 Agent 来构建，然后把结果合成为共同产出。"

很多公司听到这里会不舒服。过去一个业务同事提出需求，产品写 PRD，工程排期，数据同事补口径。Groupon 想把顺序往前推：每个职能先描述循环、搭出原型、看见结果，再把工程能力接进来。人的工作从亲手完成任务，转成设计会完成任务的循环。

所有 Agent 想法、产出和 outcome 都会被记录下来，再分发给团队。如果目标是把手工流程自动化，开工前就要写清楚：从 A 到 Z 能快多少，能省多少人时，质量、收入或其他业务指标能不能移动。Agent 项目从第一天就被放在指标桌上。

这会逼团队把重复工作拆开。输入是什么，输出是什么，失败怎么算，哪些指标能证明它真的变好了。一个人提案时，最好已经带着输入样例、输出样例、失败场景和评估指标；只带一个需求标题已经不够。

### 每个职能都要能动手搭 Agent

她形容自己的工作方式像指挥一支乐队，乐手是 Agent 和 workflow。现在一个想法拿出来时，会尽量包含输入、处理、评估和上线方案，单个 spec 已经不够。别人看到的已经是可以评审的半成品。

Groupon 内部也在给非工程团队补这些能力。训练资源、模型访问、共享 connector、MCP、Claude CoWork、Claude Design、Claude Code，都被放到业务同事可以触达的位置。变化已经落到销售的 dashboard 和 lead research 上，非工程同事也开始提出 Agent 想法。

> "成为 builder，不是 vibing 一个原型然后放在那里。成为 builder，意味着你要 ship。"

一个销售代表白天还有自己的本职工作，突然要理解 staging、CI/CD、legacy infrastructure，学习曲线很陡。Groupon 把业务同事和工程同事放进两到三人的 speedboat，小队一起搭、一起集成、一起上线。她团队里的 PM 和 UX designer 现在至少都能 ship 到 staging。

build versus buy 的口径也变了。过去她倾向先买，先把流程、人员和指标跑清楚，再考虑自建。现在采购、测试、流程都要时间，自建一个小版本反而更快、更便宜。基础设施可以买，能形成 unfair advantage 的业务环节要自己建，尤其是 eval，那一层不能外包。

组织上，她也没有把所有实验塞进一个中央 AI 小组。边缘团队先探索，找到有用模式，再沉淀成共享标准、shared framework 和 source of truth。这样既给一线足够空间，也避免每个团队各搭一套孤岛工具。要统一的是接口、数据、评估和可复用知识。

跨职能输出最后要合成到同一套业务目标里。销售看到的线索质量、产品看到的漏斗、工程看到的实现风险，不能分别停在各自文档里。Agent 只是把这些信号更快拉到同一张桌面上。

这套协作也需要底层连接。MCP、共享 connector 和数据框架的作用，是让业务同事能查到同一批数据，工程同事也能看到业务同事到底在搭什么。否则每个职能都能构建，最后只会多出更多分散的小工具。

### 先把小商家的上线路走通

Masha 加入 Groupon 后，先做了一轮商家体验 audit：商家在说什么，消费者在抱怨什么，漏斗哪里掉得最厉害，产品能力处在什么状态。她举了一个很小的场景：美国一家美甲店的老板，自己还在给客人做指甲，根本没有时间研究营销和定价。

Groupon 想帮这种商家把"我有一个活动想法"变成"活动已经上线"。流程会先扫描市场、供需两侧和商家的数字存在感，再给出一个适合该商家的 campaign。商家只需要阅读、做少量编辑，或者直接接受，onboarding 就能继续往前走。

> "如果商家材料齐全，我们能帮他们在几分钟内从想法走到上线 campaign。"

同一套思路还被用在合规上。Groupon 不能让没有资质的人上线 Botox 注射这类服务，于是他们做了 compliance crew。这个 Agent 组合会检查商家要求、所需文件、文件内容和不同维度的合规信息，再返回判断。AI 被嵌进商家上线的路线里，承担一段原本要多人来回确认的工作。

Botox 只是一个例子。平台上还有很多服务需要按州、按城市、按服务类型检查资料。过去这些判断分散在人工审核、销售提醒和运营经验里；进入 Agent crew 后，至少能先把文件、资质和缺口整理到同一个判断链路里。

Groupon 的类别很多：美容、旅行、零售、家居、汽车，本地和跨区域需求混在一起。团队排优先级时看商家规模、商家 archetype、所在地、marketplace 供需缺口和消费者需求。AI 功能只有在可证明的业务杠杆上才会进入路线图。

小商家的耐心更少。大商家后台复杂一点，还能靠运营团队补；一个本地商家多填几轮表格、多等几封邮件，就可能直接放弃。AI 在这里要做的事很朴素：把市场研究、活动文案、定价提示和资质检查合到一条更短的上线路里。

### Truth layer 决定 Agent 能不能进生产

很多企业卡在 pilot 到 production。demo 能跑以后，Agent 还要知道该按哪套知识行动。Groupon 把这层基础叫 truth layer。公司里关于"一个好 deal 长什么样"的知识原本很分散：标题、选项结构、影响指标、细则、类别差异，都在不同人的经验里。

> "我们为每个类别建立了权威 source of truth，比如激光脱毛或按摩，由对应服务领域的专家来维护。"

Category playbooks 后来被做成 AI-readable manifests。类别经理负责 truth，也负责规则来源。这些规则要接真实数据、真实表现、市场研究和搜索词，不能只来自某个经验丰富的人。比如用户点进按摩 deal 前到底搜了什么，某个类别最近有什么需求趋势，都要进入 playbook。

这层知识稳定以后，就能被多条流程复用。Agent 可以用它生成 deal，也可以用它给商家建议。商家自己编辑 deal 时，可能无意中降低转化，因为他不了解 marketplace 的规则和需求信号。Groupon 让同一个 truth layer 同时服务生成、推荐和质控。

Product 团队现在负责 eval suite 和整体 build out，还做了一个内容管理系统，帮助类别经理维护 playbooks。接下来，deal 表现会被追到 playbook 里的某次具体编辑。如果某条规则改坏了转化，团队不需要猜，可以回到源头改。

这套机制也把责任分清了：谁拥有真相，谁维护真相。类别经理不能只把经验讲给产品团队听一次，就等 Agent 自己变聪明；产品团队也不能只做界面和 prompt。一个能上线的 AI Factory，需要业务专家持续写规则，产品团队持续把规则变成可调用资产。

### Eval 把每条生成结果接回业务规则

传统软件测试看输入输出。AI 系统同样输入，下一次输出可能不同。Groupon 把 eval 做成 AI Factory 的第二层：每段 pipeline 都要被评估，评估里有确定性规则，也有概率性判断，还有能回流到 prompt 和 playbook 的学习循环。

按摩类别可能有 20 种服务，他们会生成 60 个 deal 来看上下文捕捉得怎样。评估会问：是否对齐原始 truth？有没有违反关键规则？这个 deal 是否可转化？人会不会购买？语义上有没有前后矛盾？搜索引擎能不能发现？每个 eval 都会产出 insight。

> "我们把 insight 按服务层级聚合和量化，然后就能看到：Reiki massage 这里我们偏得很厉害。"

牙齿美白这类边界条件最容易出错。有的服务在诊所现场做，有的带回家自己做，两种交付方式完全不同。早期 playbook 只覆盖了一种方式，eval 把缺口暴露出来。修的是源头，后面生成、推荐、质控才会一起对齐。

上线节奏也靠 eval 控制。早期系统保持开放，让团队学习和 pattern match。学到足够多以后，第二阶段才开始划门槛：什么指标触发 human review，什么指标允许 deal 直接走完全自动。Groupon 还会用小比例 customer rollout 控制 blast radius，换学习速度，也守住客户信任。

自主 Agent 的吸引力来自规模，风险也来自规模。一个后台建议错了，可能只是内部返工；一个面向商家或消费者的自动决策错了，就会影响收入、信任和合规。所以 Groupon 的路线会先让系统暴露错误，再用门槛决定什么时候放手，最后才扩大自动化比例。

Groupon 还跑 weekly quality control agents，看已经生成的内容是否对齐、哪里出错、哪些洞察要回到下一轮优化。AI Factory 在她嘴里更接近一套生产线：truth layer 供料，Agent 生成，eval 挑错，insight 回流，再进入下一版 prompt 和 playbook。

生成只是前半段，费工的是回流。一个 eval 暴露出 Reiki massage 偏得厉害，团队要知道是 prompt 问错了、playbook 漏了规则，还是原始 truth 就不够清楚。没有这条回路，Agent 生成得越快，后面的返工也越快。

### 领导者先搭自己的工作操作台

企业 leader 可以先从自己开始。Masha 一年前还很保守，尤其讨厌经验不足的人把 thinking 外包给 AI。现在她更开放，因为她先搭了自己的 operating system：stakeholder、strategy、vision、metrics、source of truth、direct reports、决策记录，都持续进入她自己的知识库。

> "它不是替我思考。AI 的思考已经被我的知识和专业经验 grounding。"

她现在不逐封读邮件，不逐条读 Asana，也不一条条看聊天。信息先进入 Agent，再按当月、当周策略和优先级排序。外部知识也一样：过去她手动把阅读材料丢进 Apple Notes；现在新工具、Claude 变化、GitHub trending repo 会先被 Agent 带回来，再判断能不能用于她正在做的事。

可执行的动作很小：先设自己的 operating system，再挑一个高痛点、高收益、从第一天就可衡量的 workflow，端到端 ship 一个小版本。不要在 research 里等完整方案。只有真实运行，团队才能看见规则、边界和信任门槛。

产品和业务负责人可以直接照这个用。过去想知道一个功能怎么工作，要翻产品文档；文档和代码经常不同步，PRD 事后更新又很痛。现在她直接问代码：这里怎么运行，两个系统有没有 drift，某个值是不是应该从 hard-code 挪到 config。最近四周，她自己就写过两三张 code audit tickets。

最后那句话更直：不要把理解 AI 的责任交给 AI 团队。高管、PM、运营、销售如果只等别人做培训，很快会看不懂自己公司的新生产方式。最好的训练方式，是自己搭一个小系统，让 Agent 读你的材料、理解你的目标、帮你完成一个真实任务。

写在最后

如果团队还没想清楚 AI-native 从哪里开始，可以先别开大项目。挑一个每天重复、能衡量、出错半径小的工作流，给它配 source of truth、eval 和人审门槛。先让一个小循环跑起来，组织会比在会议里更快学会新分工。

---

## 备注

- 原文 4000 字，本文保留全部正文（5735 字符清洗后）
- 内容来源标注的链接已被原作者压缩到一句话：内容来源："Building the AI-Native Enterprise, Agent Crews and the AI Factory | Interview with Masha Sharma"丨Augmented U，原视频 https://www.youtube.com/watch?v=pQj8qOyan-Q
- 公众号"晚点再听LaterCast"正文未提供日期时间（og:description 中包含"全文约 4000 字"），但微信公众号典型推送格式与发布日的 2026-07-07 一致
- 文末"如果你喜欢深度好文，试试用小程序将不方便立刻阅读的文章转成播客"为公众号常规收尾语，已保留