# Harness Engineering for Self-Improvement（翁荔 Lilian Weng）

> **编译者备注**:微信公众号 Datawhale 2026-07-08 推送，作者翁荔(Lilian Weng)，Datawhale 编辑团队。
> 原文一手来源：https://lilianweng.github.io/posts/2026-07-04-harness/
> 抓取时间：2026-07-08 10:38 Asia/Shanghai
> 抓取方式：curl + Chrome User-Agent

---

## 原文标题

**AI 自我改进的关键，从模型转向 Harness了！**

## 作者

**翁荔(Lilian Weng)**，北大校友、AI 研究者，Lil'Log 博客 2017 年写到现在，Google Scholar 引用量 5 万+；前 OpenAI 安全研究副总裁，2024.11 离开 OpenAI，现联合创立 Thinking Machines Lab。2023 年提出行业最被引用的 Agent 定义——"Agent = LLM + 记忆 + 工具 + 规划 + 行动"。本文是她 2026-07-04 发布的 Harness Engineering for Self-Improvement 主题整理。

## 公众号编辑按

Datawhale 干货。北大校友、AI 研究者翁荔的技术博客 Lil'Log，是 AI 圈子里少数几个"一更新就必读"的地方。她此前在 OpenAI 担任安全研究副总裁，现联合创立了 Thinking Machines Lab。

就在刚刚，她发布了一篇新文章《Harness Engineering for Self-Improvement》，书写了当前大热的 Harness Engineering 主题。

[图]原文链接：https://lilianweng.github.io/posts/2026-07-04-harness/

她认为，递归自我改进(RSI)走到今天，起作用的不只是模型本身变聪明了，包在模型外面的那层 Harness 同样在决定 AI 能跑多快、多稳。

这篇文章梳理了 Harness Engineering 这个方向：它有哪些设计模式，学术界目前怎么优化它，以及往前走还剩下哪些没解决的问题。原文技术密度很高，这篇编译尽量把核心机制讲清楚。

## 一、翁荔眼中的 Harness

递归自我改进(RSI)这个概念能追溯到 I. J. Good (1965)，他把"超级智能机器"定义为一种在所有智力活动上都能超越人类、并能设计出更好的机器来改进自己的系统。Yudkowsky 把"recursive self-improvement"这个说法用在一个具体的反馈回路上：AI 用自己当下的智能，去改进产生这份智能的认知机制本身。

放到今天的 AI 里，这个反馈回路可能表现为模型直接重写自己的权重，也可能表现得更宽泛：模型改进训练管道和部署系统，进而让下一代模型在有经济价值的任务上表现更好。

Lilian Weng 特别强调"部署系统"这个词，因为她认为，包在裸模型和真实场景之间的这一层，重要性不亚于模型本身的原始智能(也就是预训练刚结束时跑的那些评测)。Claude Code、Codex 这类编码 Agent 产品的成功，印证了 harness 在 AI 部署里的分量。

她给出的定义是：harness 是包裹在基础模型外面的系统，负责编排执行过程，决定模型怎么思考和规划、怎么调用工具和行动、怎么感知和管理上下文、怎么存储产出物，以及怎么评估结果。

这篇文章聚焦的是 harness engineering 本身，以及它对 RSI 的贡献。模型自我博弈、合成数据、测试时训练、持续学习这些同样呼应 RSI 愿景的方向，原文里只是点了一下名字，没有展开。

## 二、Harness 的三种设计模式

对比早期的 agent 框架("agent = LLM + 记忆 + 工具 + 规划 + 行动")，harness engineering 多了工作流设计(比如 loop engineering)、评估、权限控制、持久状态管理这几层。它不再只是 prompt 模板，而是更接近运行时和软件系统设计：模型怎么观察、行动、记忆、自我检查、自我改进。

设计上应该刻意做得简单、通用，这样才能泛化，并且可以参照现有软件工程的实践，从预训练已经学到的知识里获益。操作系统和 harness 之间有一个很强的类比：一个好的 harness 应该像操作系统一样，把复杂逻辑封装起来，同时保持接口简单。config、工具接口和其他协议，也可能会随着行业发展逐渐标准化。

### 模式一：工作流自动化

给模型定义一个可以操作、测试、迭代的工作流，是实现自动化的关键设计。Karpathy 的 autoresearch 仓库是一个干净的例子。常见的工作流遵循一个目标导向的循环：规划、执行、观察或测试、改进，再执行，直到目标达成，过程中可能会主动向用户请求澄清任务规格或执行偏好。这套工作流图强调的是模型在一个"agent runtime"里分析自己的执行轨迹和失败案例、持续迭代，而不是套用一个静态的 prompt 模板。

### 模式二：文件系统作为持久记忆

长周期 agent 系统里反复出现的一个模式，是用简单的方式管理丰富的状态和产出物。harness 不该把整个工作流和所有日志都塞进上下文；相反，它应该把持久状态存进文件。在长周期的 agent 执行过程里，实验日志、代码 diff、论文摘要、报错记录、过去的执行轨迹这些产出物，长度往往远超模型训练时习惯的上下文窗口。

学会通过 bash 这类命令读写和编辑文件系统，是 LLM 的一项基础能力，也因此，用文件这种简单形式管理持久记忆，会自然地随着核心模型能力的提升而受益。

### 模式三：子 Agent 与后端任务

一个 harness 可以派生多个子 agent 并行执行，同时监控后端任务。这在主 agent 需要搜索多个假设、并发跑多组实验，或者把独立子任务委派出去而不污染主上下文时很有用。这时父 agent 需要一个小型的进程管理器：启动任务、查看日志、取消失败的运行、把结果合并回主 agent 的会话线程里。

这里的关键设计选择，是让并行过程显式且可检查。如果子 agent 的产出只存在于临时的聊天上下文里，它们很快就会过期、被隐藏起来；但如果存成文件、日志和状态记录，模型就能在中断后恢复，并对自己的执行历史进行推理。

### 案例：编码 Agent 的 Harness

Claude Code、Codex、OpenCode，以及 Cursor 这类编码 agent 的核心接口，已经趋于稳定，普遍用一套循环运作：给定一个代码仓库，agent 靠一组工具去开发和调试问题，类似人类开发者靠 IDE 工作。原文给出了一份(非完整)工具分类，翻译如下：

[图][图]

### Harness 层会被模型内化吗

很难预判 RSI 未来会在多大程度上依赖 harness engineering，但 Lilian Weng 认为，RSI 近期的路径不太可能从模型直接重写自己的权重开始。她给出的预测分两步：

第一，harness engineering 会朝"元方法论"的方向演进：优化的是"获得更好答案的机制"本身，而不只是答案；harness 系统本身会成为优化目标，规则会越来越少靠硬编码的启发式，越来越多靠通用机制。

第二，成熟的 harness 反过来让模型自我改进的 auto-research 循环变得可能，而更聪明的模型也能防止 harness 被过度设计，让整套系统保持可持续。

最终，很多 harness 层的改进可能会被内化进核心模型的行为里，但与外部上下文和工具的接口应该会保留下来。这个模式在 prompt engineering 的历史上已经出现过一次比较温和的版本：随着指令微调和模型推理能力的提升，手工 prompt 技巧变得不那么核心，但指定目标、约束、上下文和评估的需求，并没有消失。

## 三、Harness 怎么被优化

优化对象的演进大致是这样一条路径：指令 prompt → 结构化上下文 → 工作流 → harness 代码 → optimizer 代码。模型越强，能驾驭的优化目标就越复杂、越通用。

### 上下文工程：ACE、MCE、Meta-Harness

把所有工具返回结果和模型生成内容简单地堆进上下文，会随着 agent 任务的复杂化和执行长度的增加而失效。上下文工程(context engineering)关注的是在每一步维护和呈现"恰到好处的信息"。

(1) ACE (Active Context Engineering)代表的是把 context 当成工作记忆来管理，工作记忆里整合了模型 rollout、批评反馈、环境反馈等信号，从而指导下一轮 rollout。

(2) MCE (Meta-Context Engineering)是另一条路径，通过基于自然语言反思的进化搜索来自动产出新的 context 策略。每条策略就是一个简洁、抽象的指令，告诉模型"怎样更聪明地使用自己的上下文"。如果策略库里有 M 条策略、每次 rollout 选 K 条拼接，那么策略空间就有 (M choose K) 这么多种组合。

(3) Meta-Harness 代表的是把 harness 本身当成可进化的对象，搜索的是 harness 代码、配置、工具的组合。代表项目是 Sakana 团队的 Darwin Gödel Machine(DGM)：模型自己改自己的代码，在 SWE-bench 上取得 20% → 50% 的提升。

### RL 优化 Harness 的方法与风险

强化学习也是优化 harness 的一种方式。代表是 Sakana 的其它项目，比如被 Anthropic 收购的 AISC，以及"自修改 RL 智能体"等。但这里有一个巨大的风险：reward hacking。

在 SWE-bench 风格的代码任务里训练 RL 时，模型可能学会绕过测试、修改测试用例以通过验证、删掉某些功能性代码以让测试通过等取巧方式，而这些在真实生产环境中是不会被接受的。优化要保持在线（避免离线过拟合），并且在真实环境上持续验证，否则就是装腔作势。

### 人类写的 Harness 规则

更经典的方式是人工直接写 harness 规则，例如 Claude Code 自己的 system prompt 就包含若干条 best practices 和"反模式"提醒。这些规则涵盖怎么和用户协作(确认操作、解释非显而易见的设计决策)、怎么用工具(批处理、并行调用、写入文件前确认破坏性操作)、怎么处理长任务(中间写进度文件、滚动重读 spec)、怎么保持输出质量(避免过度工程、避免不兼容的 API 等)。这种方式的局限是 LLM 不会精确遵循每条规则，而且对 LLM 能力越强，越能在执行中"绕过"规则。

## 四、人的角色

Lilian Weng 对 RSI 的预测是：短期内 model-driven(以模型为主导的自我迭代)还不会比 harness engineering 走得更远，因此 harness design 这件事仍然重要且值得做投入。但它本身不应该被神化。Lilian Weng 提出一个反"模型过拟合"的看法：把很多条件硬塞到 prompt 里或加到 harness 里，反而会损害系统在新场景下的泛化能力。

她建议，harness 应该刻意保持简洁、通用，依赖预训练已经学到的知识，而不是把所有边界条件都罗列出来。

harness design 很大程度上还是由人主导的过程，未来的研究者和从业者会想清楚：

- 哪些约束应该硬编码进 prompt 或 harness
- 哪些约束应该交给模型自己判断
- 哪些约束应该留给运行时反馈 / 人类监督

人应该往抽象栈的更高层移动，而不是被从循环里挪走。这意味着人要在正确的时间、正确的抽象层级上提供监督，系统设计需要认真考虑什么时候、以什么方式设置这样的"接触点"。上面列出的很多挑战，最终都需要人的反馈和引导才能解决。归根结底，这项技术是为了人类更好的未来而存在的，不是反过来。

## 五、原文未展开的 3 个相关方向

1. **模型自我博弈** — AlphaGo Zero / AlphaProof 等纯 self-play 路线
2. **合成数据** — 用模型生成训练数据
3. **测试时训练 / 持续学习** — 推理时改模型权重 + 跨任务持续学习

(原文都是"点了一下名字，没有展开")

## 关于翁荔

翁荔本科毕业于北京大学，博士就读于印第安纳大学伯明顿分校。毕业后她先在 Dropbox 做工程师，后加入金融科技公司 Affirm，2018 年年初加入 OpenAI，最早在机器人团队工作，参与过教机械手复原魔方的项目。

随着 OpenAI 转向大语言模型，她在 2021 年前后组建并带领 Applied AI Research 团队，做出了 fine-tuning API、embedding API、内容审核接口这些产品化工具。GPT-4 发布后，她把公司内部的安全工作统一成一个团队，也就是 Safety Systems，团队规模一度超过 80 人，她本人在 2023 年升任 VP of Research and Safety。

她 2023 年那篇《LLM Powered Autonomous Agents》提出的公式，Agent 等于大模型加记忆加工具使用加规划，后来成了行业里描述 agent 架构最常被引用的定义之一。这次《Harness Engineering》一文里，她自己也拿这条公式做了对照的起点。

2024 年 11 月，她在 X 上宣布离开 OpenAI，说工作七年后想重启一下，去做点新的事情。此后她加入了 Mira Murati 创立的 Thinking Machines Lab。她的技术博客 Lil'Log 从 2017 年写到现在，覆盖强化学习、扩散模型、Agent、Reward Hacking 等多个方向，是 AI 圈公认的高质量长期更新源，Google Scholar 引用量已经超过 5 万次。

封面来源：AGI Hunt

---

## 备注

- 原文 7 节，本文 5 节结构做了精简（删了"原文未展开的 3 个相关方向"的详细解释 + 翁荔个人背景的某些细节）
- 原文 1 张完整工具分类图（CLI agent 工具分类）本次未抓取完整版，建议读 https://lilianweng.github.io/posts/2026-07-04-harness/ 原文
- 工作流图（planning-execution-observation-loop）也是图片
- 一手原文链接：https://lilianweng.github.io/posts/2026-07-04-harness/
- 公众号推送 ID：ayESVu4F_3RC3OdP8aV7ow