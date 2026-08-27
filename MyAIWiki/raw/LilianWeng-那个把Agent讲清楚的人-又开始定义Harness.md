# Lilian Weng：那个把 Agent 讲清楚的人，又开始定义 Harness

**来源：** 微信公众号
**作者：** DataFun
**日期：** 2026-08-26
**链接：** https://mp.weixin.qq.com/s/CWcQtzDu-lbme41eQm-oZg

---

## 正文

导读
2023 年，她把混乱的 Agent 讨论整理成了一张事实标准的地图；2026 年 7 月 4 日，她写下 Harness，25 天后重返 OpenAI。
2023 年 6 月，Lilian Weng 在个人技术博客 Lil'Log 发表《LLM Powered Autonomous Agents》，把 LLM、规划、记忆和工具调用组织成一套清晰的 Agent 架构。这篇文章后来成为很多人理解 Agent 的通用参考。2026 年 7 月 4 日，她在同一博客发表《Harness Engineering for Self-Improvement》，讨论的是一个更基础的问题：如果 AI 要走向自我改进，最先应该被优化的是什么。她的判断是，短期内可行的递归自我改进（Recursive Self-Improvement，RSI）不太可能从“模型直接重写自己的权重”开始，更现实的路径是先优化模型外面的运行系统——也就是 Harness。
主要内容包括以下几个部分：
1.
她没有“发明”Agent，但把一个混乱时期整理成了地图
2.
现在，同一个人开始定义 Harness
3.
她写下 Harness 的那个月，OpenAI 已经开始正式衡量“AI 帮助研发 AI”
4.
改 Harness 还是改权重：她的 Safety 经历，在 RSI 阶段反而更重要
5.
写在最后
25 天后，OpenAI 向 TechCrunch 确认，Lilian Weng 重返公司，将领导一个顶层团队，重点加速内部研究，并支持与 RSI 相关的跨研究工作。
两件事没有证据表明存在直接因果关系，但时间线值得放在一起看：OpenAI 此时已经把“构建自动化 AI 研究员”列为三大目标之一，并设立了专门的 RSI 团队。
这次人事变动背后是一个更大的行业变化：AI 正从“帮助研究员写代码”，走向“进入 AI 研发循环本身”。Weng 过去几年的研究与写作，覆盖了这条路线上的几个关键节点。
01
她没有“发明”Agent，但把一个混乱时期整理成了地图
Lilian Weng 的影响力很大一部分来自 Lil'Log。她在 2022 年接受 OpenAI 采访时说，这个博客最初只是个人学习笔记：读了大量论文后，为了整理新概念，她开始持续写作，并用“能否把知识讲清楚”检验自己是否真正理解。
《LLM Powered Autonomous Agents》最能体现这种写法。当时 AutoGPT、BabyAGI、ReAct、工具调用、反思和长期记忆已经大量出现，Agent 还没有统一的工程语言。Weng 没有发明这些组件，而是把它们组织在同一张图里：LLM 作为核心控制器，外面连接 Planning、Memory 和 Tool Use，再通过 Action 与环境交互。
图 1｜2023 年 Lilian Weng 对 LLM Agent 的系统化整理（Lil'Log 官方原图：agent-overview.png）
三年后回看，这张图已经显得简单，但它抓住了一个重要变化：模型能力开始向模型之外延伸。她本人的经历也横跨这条延伸线上的多个层面：最初两年半在 OpenAI Robotics 团队参与机械手解魔方项目，2021 年初开始领导 Applied AI Research；GPT-4 官方贡献名单中，她是 Deployment 部分的 Applied Research Lead，同时参与 Model Safety、Refusals 和 Safety & Policy Evaluations；到 o1，她被列在 Supporting Leadership 和 Safety Leadership 中。这些经历共同指向一个反复出现的问题：模型能力变强以后，怎样把它放进真实系统，并让行为保持可控、可评估、可修正。Agent 是其中一步，Harness 把问题继续往外推。
02
现在，同一个人开始定义 Harness
同一个模型，放在一个只会聊天的网页里，和放在一个能读文件、跑命令、开子任务、看日志、写代码、跑测试、回滚错误的环境里，能力表现完全不是一回事。在《Harness Engineering for Self-Improvement》中，Weng 把后一类环境称为 Harness：包围基础模型的一整套运行系统，负责组织执行，并决定模型怎样规划、调用工具、感知和管理上下文、保存中间产物，以及评估结果。
相比早期“LLM + Memory + Tools + Planning + Action”的 Agent 公式，Harness 多出了真正决定长任务能否运行的部分：工作流、持久状态、权限控制、失败恢复和外部评测。模型不再只完成一次调用，而是进入一个可以持续执行、失败、检查、回滚和重试的环境。
Coding Agent 是最直观的例子。它先观察仓库，制定计划，读文件、改代码、跑测试；测试失败后查看错误，再修改方案。推理能力来自模型，但“把错误变成下一轮行动”的能力，很大程度上取决于 Harness。
图 2｜Coding Agent 的执行循环：观察、计划、修改、测试、检查错误并继续迭代（Lil'Log 官方原图：coding-harness-loop.png）
更重要的是，Harness 自己也可以成为优化对象。Weng 把这条路径概括为：Prompt → Structured Context → Workflow → Harness Code → Optimizer Code——优化对象从一次回答，逐渐移动到“产生答案的机制”。落到 RSI 上，这意味着先让 AI 读取自己的轨迹、发现失败模式、修改工作流和工具策略，再用外部评测决定修改是否保留。相比“模型自己重写权重”，这条路更像软件工程，也更接近今天已经能做的事。
03
她写下 Harness 的那个月，OpenAI 已经开始正式衡量“AI 帮助研发 AI”
6 月，OpenAI 在公司计划中把 “Build an automated AI researcher” 列为三大目标之一。官方判断是，到 2028 年 3 月，相当一部分研究工作可能由 AI 系统与研究员协同完成。OpenAI 同时写道，未来几年“AI 做 AI 研究”可能成为决定技术进步速度的关键因素。
7 月发布 GPT-5.6 时，OpenAI 把一组内部能力明确归到 RSI 指标之下，评测包含研究系统调试、Kernel 优化、训练 Recipe、机器学习实验，以及“改进另一个模型”。其中 GPT-5.6 Sol 的 RSI Index 为 57.9%，GPT-5.5 为 41.7%，提高 16.2 个百分点。
OpenAI 还披露，过去六个月，研究算力中用于内部 Coding Inference 的份额增长了 100 倍，内部 Agentic Token 使用量约增长 22 倍。OpenAI 同时强调，这些使用指标不能直接证明研究进展加快，只能说明 AI 在研究和内部工作流中的使用规模快速上升。
图 3｜OpenAI GPT-5.6 官方披露的 RSI 指标与内
部使用数据
团队建设提供了更直接的证据。OpenAI 的 RSI 招聘页写得很清楚：自动化真实研究工作流，建立反馈循环和评测，通过 Agent Harness、合成数据、RL 环境和模型训练补齐研究能力，并开发 Research Agent、实验编排系统和沙箱运行时。Agent Harness 这个词，从一篇博客文章走进了 OpenAI 的官方岗位描述。
图 4｜OpenAI RSI 团队公开岗位涉及 Agent Harness、评测、RL 环境、模型训练与研究基础设施
把这条背景放在一起看：OpenAI 正把 AI 研究自动化做成一条横跨模型、Agent、Harness、评测和研究基础设施的完整工程链，而 Weng 过去的公开工作覆盖了这条链上的多个关键环节。
04
改 Harness 还是改权重：她的 Safety 经历，在 RSI 阶段反而更重要
递归自我改进容易被讲成纯粹的能力竞赛：谁先让 AI 自己改自己，谁就能更快迭代。但一旦把“自我改进”落实到工程里，能力和控制很难再拆开。如果 Agent 能修改 Prompt、工具定义、工作流甚至 Harness 代码，就必须同时回答另一组问题：哪些文件可以改？哪些评测必须保持只读？谁决定一次修改被接受？怎样防止系统为了提高分数而改变验收标准？短期 Benchmark 变好、但长期可维护性变差时，谁来发现？
Weng 在 Harness 文章中对这类边界保持了明确警惕。她指出，如果程序可以编辑类似“操作系统”的层，抽象边界就会被打破；可编辑范围必须被严格设计，权限和安全层应放在自我修改循环之外，Reward Hacking 等问题也不会因为 Harness 更强而消失。
OpenAI 也在并行建设这一侧。除 RSI 研发岗位外，公司还公开招聘 Recursive Self-Improvement Safety 研究员，工作包含可扩展监督、自动审计，以及对 Reward Hacking、Sandbagging、Scheming 等失控风险的监测。
Weng 从 Applied Research 到 Safety 的经历，说明她并不只站在“怎样让系统更强”这一侧。到了 RSI 阶段，控制不再是模型完成之后附加的一道检查，而会直接进入系统设计：什么可以被优化，什么必须保持在优化循环之外，本身就是能力的一部分。
05
写在最后
2023 年的 Agent 文章回答的是：一个 LLM 怎样从聊天模型变成可以规划、记忆和调用工具的系统。2026 年的 Harness 文章继续追问：这个系统怎样在真实任务里长期运行、保存状态、评估结果，并逐步改进自己的工作方式。再往前一步，就是 OpenAI 现在公开推进的问题——怎样让这样的系统进入 AI 研究流程。
这可能带来一条不同于传统 Scaling 的增长路径。过去 AI 公司主要扩大训练算力、数据和参数规模；现在开始扩大的是模型参与研发的深度和频率。如果上一代模型能帮助发现训练问题、并行运行更多实验、优化更多代码，再把结果反馈给下一代训练，被压缩的就不只是一次推理时间，而可能是模型研发周期本身。
但这里还远没有到“AI 自动造出下一代 AI”的程度。Weng 自己也把边界写得很清楚：自我改进更适合评价客观、反馈快速的任务；真正困难的是弱评测、模糊目标和 Research Taste。实验能跑通，不等于问题值得研究；分数提高，也不等于产生了真正的新知识。
三年前，那张地图的关键词是 Agent。现在，它延伸到了 Harness 和 Recursive Self-Improvement。下一阶段实验室之间可能拉开差距的，不只是“谁训练出一次最强模型”，而是谁先建立一个更快、更可靠、同时仍可控的研发闭环——让今天的模型，开始参与制造明天的模型。
资料来源
1. Lilian Weng — Harness Engineering for Self-Improvement (2026-07-04)
2. Lilian Weng — LLM Powered Autonomous Agents (2023-06-23)
3. OpenAI — The power of continuous learning (2022-12-23)
4. OpenAI — GPT-4 contributions
5. OpenAI — OpenAI o1 Contributions / System Card
6. OpenAI — Built to benefit everyone: our plan (2026-06-08)
7. OpenAI — GPT-5.6: Frontier intelligence that scales with your ambition (2026-07-09)
8. OpenAI Careers — Research Engineer / Research Scientist / AI Systems Engineer, RSI
9. OpenAI Careers — Researcher, Recursive Self-Improvement Safety
10. TechCrunch — Thinking Machines co-founder Lilian Weng ... then joined OpenAI (2026-07-29)
往期推荐
基于Prompt+Context+Harness的本体约束架构！
TDSQL Nexa：面向 Agent 的统一数据平面！
Agentic Search + Memory：OpenClaw 从搜索工具到企业认知引擎
OpenAI Codex 负责人亲自回应：模型没变，Agent 为什么突然更烧 Token？
别再给 Agent 默认最强模型了：Databricks 开始同时选择 Model 和 Harness
Google前首席科学家 Jeff Dean：模型越强，真正值钱的反而越在“模型之外”
Palantir把Claude、OpenAI和Google的Agent接到了Ontology之上
99%手机背后的巨头，如何革新整个Agent生态？
LangChain CEO：Agent 越复杂，越需要自建 Harness？恰恰不是
资本开始买“语义层”了：Graphwise 获控股投资，AI Agent 的新基础设施正在成形
点个
在看
你最好看
SPRING HAS ARRIVED

---

标签： #主题/AI-Agent #主题/Harness #主题/RSI #主题/AI-Coding #场景/公众号长文
