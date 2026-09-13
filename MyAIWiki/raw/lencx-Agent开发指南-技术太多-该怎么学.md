# Agent 开发指南：技术太多，该怎么学？

**来源：** 微信公众号
**作者：** lencx
**日期：** 2026-07-28
**链接：** https://mp.weixin.qq.com/s/Mx1pclSLzkRFXKEME24TYA

---

## 正文

一份关于 Agent、Harness、浏览器、桌面宿主、Skills 与编程语言的 2026 技术趋势报告
证据边界 & 观察尺度
本文解释为什么看似分散的开源项目、收购、语言重写与浏览器能力，正在汇入同一套 Agent 基础设施，并刻意区分已发生的事实、基于事实的推断与面向未来的预测。
Vercel Labs、Cloudflare 实验项目、公司公告与收购计划只作为趋势证据，不自动构成任何公司的稳定路线图。
项目自报的性能、兼容性和成本数据均视为项目方主张，除非另有独立证据。
本文是一份独立的技术趋势研究，仅供参考。
本文观察尺度高于某一套具体框架（如 LangGraph），重点是比较跨框架长期存在的系统责任：目标、状态、身份、执行、验证、副作用与人工接管。具体框架仍应按团队语言、部署环境、故障模型、治理要求和迁移成本选择（可参考清单：
awesome-agents
[1]
、
awesome-ai-agents
[2]
）。
这篇文章有点 looooooooong，没办法，我不喜欢一件事分几次来写。大家可以收藏/转发，分多次阅读。在阅读前，也可以补充一点相关背景：
Claude Opus 5：一半 Fable 价格，解锁更强能力
编程心得：Vibe 上百亿 Token 后，我收获了什么?
TS 7：AI 生成式代码的拐点
Noi 编程实战：Fable 没那么强，GPT 也没那么弱
GPT-5.6 Sol：前沿智能不再平权
Loop 不是 Agent 架构，Harness 才是
深度思考：架构腐朽 & Loop Engineering
Claude Fable 5：最强 AI 正在变成“特权资源”
浅谈 AI 编程
浅谈 AI 超级应用
第一个 Agent 从 Pi 开始
深度解析：Codex Pet Skill
顶层思维
Agent Memory 架构本质
深度解析：Claude Code 源码
深度解析：Harness Engineering
AI 操作系统：从指令到意图
Agent 趋势浅思：原生化 & CLI 化
AI 编程生态：Anthropic 收购 Bun 意味着什么？
从 Prompt Engineering 到 Context Engineering
深度思考：聊聊 AI 发展趋势
浅谈 AI 浏览器
...
核心判断
Agent 不缺代码，缺可信完成
Vercel 与 Cloudflare 的开源和收购、Pi/OpenClaw/Hermes 的 Gateway 与 Harness、Chrome/Dia 等 AI 浏览器、Electron/Tauri 的桌面宿主，以及 Rust/Zig/TypeScript/Python 的语言重构，都只是庞大 AI 生态浮出水面的局部信号。它们不足以代表全貌，却共同指向软件基础设施的重心变化。只看表层，最容易得出的结论是：
AI 带火了 Rust、Zig、浏览器自动化和 TypeScript。
这个结论停留在表层。更深的因果来自软件成本函数和操作者模型的变化：
生成与试错成本下降
-> 同一任务产生更多代码、更多分支、更多工具调用
-> 环境、状态、权限与失败面的复杂度上升
-> 真正稀缺的东西从“代码”转向“可信结果”
当模型只回答问题时，最重要的是推理质量；当模型可以写文件、运行命令、登录网站、部署服务、花钱和修改生产数据时，最重要的开始变成：
它以谁的身份行动；
它只能触达什么；
环境是否可复现；
中断后能否恢复；
结果如何验证；
副作用如何审计；
人类何时能够接管；
“完成”到底由谁认定。
因此，Agent 原生软件的核心，是在概率性的推理核心之外建立一个确定性的执行外壳。聊天框、语言和框架只是其中的局部实现：
这里每一层都可以开源一部分，但真正能收费、能形成平台黏性的，通常是托管的执行、身份、状态、浏览器、GPU、部署和可观测性控制面。全文的核心判断是：
Agent 原生软件的终点不是“最大自治”，而是让一个不完全可靠的推理者，能够在可靠系统中持续承担责任。
一、回答不等于负责
经典 LLM 应用常被描述为：
prompt -> model -> response
Agent 环路则更接近：
observe -> plan -> act -> wait -> verify -> settle
\-> pause / approve / retry / recover
两者的差异来自状态模型。一次回答可以失败后重问；一次真实动作可能已发出邮件、已创建资源、已扣款，进程却在收到结果前崩溃。此时简单地“重试”可能造成重复副作用。生产 Agent 因而需要：
稳定的任务、步骤与动作身份；
幂等键和副作用收据；
超时、取消、预算与资源租约；
dispatch 前、dispatch 后、结果确认后的明确阶段；
对结果不确定的动作执行 reconcile，避免盲目重放；
检查点、恢复、补偿和人工接管；
以可核验的证据驱动完成判定。
模型调用到这里已经只是系统中的一步。决策循环、持久状态、能力授权、隔离执行、结果验证与业务结算必须由不同边界负责；否则一次超时究竟该重试推理、重放工具、恢复任务，还是对账外部副作用，系统根本无法判断。Agent 从“回答”走向“负责”的关键，正是为这些不确定状态建立确定的所有权。
二、Harness 持有全程
Prompt 管一次，Harness 管全程
“Prompt Engineering 已经过时”是一种过度简化。Prompt 仍决定当前一次推理收到什么指令，只是工程对象已经不断向外扩张。
Anthropic 对 Context Engineering 的定义
[3]
很准确：Prompt Engineering 组织模型指令，Context Engineering 则在每次推理前，从 system prompt、工具、MCP、外部数据、消息历史和运行状态中选择最有价值的一组有限 token。进入长任务以后，compaction、结构化笔记、按需检索和 subagent 都是在管理这份不断变化的注意力预算。
再向外一层，
OpenAI 所说的 Harness Engineering
[4]
不再只优化模型“看到什么”，而是让工程师设计环境、表达意图并建设反馈环路，使 Agent 能可靠工作。Anthropic 的
Managed Agents 架构
[5]
给出了更接近系统实现的拆分：session 是追加写的事件日志，harness 是调用模型并路由工具的循环，sandbox 是执行代码与文件动作的环境。
这些术语的区别，在于各自持有什么状态、覆盖多长时间、对哪一段执行负责：
这些概念相互嵌套，各有清晰边界：
Context 是每次采样的视野，Loop 是时间轴，Graph 是任务拓扑，Skill 是可加载的程序性模块；Harness 持有目标，并把它们组织成一次可恢复执行。
Graph Engineering
仍是观察 orchestration 拓扑的角度，行业边界尚未稳定，也无需扩张成包办一切的新学科。
Harness 还必须随模型变化而删减。Anthropic 发现，为 Sonnet 4.5 的 “context anxiety” 加入的 context reset，到 Opus 4.5 已经成为多余负担。
到了 Opus 5 一代，这种删减更加激进。
Anthropic 的 Claude 5 context engineering 复盘
[6]
披露称，Claude Code 为 Opus 5、Fable 5 等新模型删掉了超过 80% 的 system prompt，coding eval 没有出现可测量损失。团队发现，system prompt、
CLAUDE.md
与 Skills 中累积的规则不仅会过度约束模型，还可能彼此冲突，迫使模型先花推理预算解释约束，再处理用户任务。
对应的方法也从“堆更多指令”转向“设计更好的运行环境”：少写覆盖所有场景的规则，让模型结合周边上下文判断；少用示例限定工具探索空间，改为设计表达力更强的参数与状态；不再把 review、verification 等信息全部前置，而是通过 Skills、deferred tools 和 progressive disclosure 按需加载。Claude Code 还把这套检查放进
/doctor
，用于收缩过度膨胀的 Skills 与
CLAUDE.md
。
System prompt 仍有价值，但每条长期指令都应有退出条件。策略必须可替换、效果必须持续评测；模型升级时，Harness 应删除过时脚手架，避免把一代模型的缺点固化成长期负担。
Goal 定义何时停
Codex Goal
[7]
把长任务的责任边界落实为产品原语：
/goal
的文本既是第一条 prompt，也是任务的 completion criteria；一个合格目标至少应写明 outcome、constraints 和 verification。它可以被暂停、恢复、编辑或清除，并允许在同一任务中继续补充上下文，但不会因此获得更宽的 sandbox 或 approval 权限。
这比“请一直做下去，直到完成”严格得多。生产级 Goal 应当是一份可执行契约：
Intent
-> Goal { outcome, constraints, verifier, budget }
-> Plan / task graph
-> Observe -> Act -> Collect evidence
-> checkpoint + update state
-> continue / retry / needs-input / blocked / completed
完成状态应由测试、可测指标、Diff、截图、外部状态或人工验收确认，而非模型自述。持续运行同样需要边界：当 verifier 不可达、预算耗尽、权限不足或外部依赖永久失败时，Harness 必须进入
blocked
、
needs-input
、
cancelled
或
budget-exhausted
一类明确终态。缺少停止证明和资源上限的 Goal，本质上仍是无限循环。
Memory 不是向量库
Agent 的 memory 至少应拆成五类：
工作状态
：当前计划、步骤、游标、预算、等待条件；
事件历史
：观察、动作、工具结果、审批与结算记录；
领域知识
：文档、代码、业务事实及其来源和版本；
情节与偏好
：历史任务总结、用户习惯、可衰减经验；
身份与隐私
：凭据、授权、租约和人类决定。
身份与隐私需要独立于普通语义索引保存。事件历史也应保留原始记录：摘要适合压缩上下文，审计则依赖可追溯事实。成熟 memory 系统需要写入权、来源、TTL、冲突处理、删除义务、模式迁移和回放规则。能无状态完成的任务应保持短寿命，因为持久化本身会引入隐私、腐化和迁移成本。
这五类信息采用不同的一致性和恢复语义：工作状态可以被新 checkpoint 取代，事件历史应追加写，领域知识必须保留版本与来源，偏好需要衰减和纠错，凭据则应留在专用隐私边界。Memory 设计应先回答谁能写、什么是真相、何时失效，以及崩溃后以哪一份记录恢复，随后再选择存储与检索技术。
Subagent 拆上下文，Handoff 转责任
Subagent 最直接的价值在于隔离噪声并获得并行度。
Codex Subagents 文档
[8]
建议先从探索、测试、triage 和总结等 read-heavy 工作开始：每个 worker 可以消耗自己的上下文和工具输出，只把压缩结果交回主 Agent；write-heavy 并行则需要 worktree、文件所有权和合并者，否则协调成本会吞掉并行收益。
subagent
与
handoff
表达两种不同的责任关系。
OpenAI Agents SDK 的编排模型
[9]
将其区分为：
Agent as tool
：主 Agent 保留控制权，调用 specialist 完成有边界的子任务，再统一验证和交付；
Handoff
：当前 Agent 把会话控制权转给 specialist，由后者成为当前 active agent。
可靠 handoff 需要结构化移交：目标与范围、已经验证的事实、未决假设、当前 checkpoint、待确认副作用、能力与审批状态、资源租约、停止条件，以及结果应交还给谁。只传一段自然语言摘要，会把上下文丢失伪装成组织分工。
Claude Code Dynamic Workflows
[10]
则展示了更大的组合单位：Claude 动态写 orchestration script，把任务分发给数十至数百个并行 subagent，加入独立尝试、反驳、review、聚合与修复循环，并持久化进度以便中断后继续。Bun 的 Zig→Rust 迁移把几种术语同时落到了代码上：
translation rulebook 和 dependency map 是 graph；
按文件 fan-out、每个文件双 reviewer、再 fan-in 是 multi-agent orchestration；
compiler 与 test failure 不断生成下一批修复项，是 loop；
session、并发、进度、权限、成本、恢复和最终 judge 合在一起，才是 harness。
Dynamic Workflows 的发布稿与
后续迁移复盘
[11]
采用了不同时间点的代码量和测试口径，本文分别保留其原始语境。后者记录的 19 个合并后 regression 已经足够说明边界：Agent 可以把大规模机械迁移推到既有验收器覆盖的位置，测试没有表达的行为仍会逃逸。后文讨论 Bun 的重写规模时，重点也会落在这笔验证成本上。
Harness 到这里解决了“同一任务如何持续推进”。下一层问题是能力由谁托管，以及怎样进入开发者已有的工作流。Vercel 与 Cloudflare 提供了两张方向相反的系统剖面：一家从 Web 交互向下补执行，另一家从 runtime 与状态向上补体验。
三、平台争夺 Agent 全栈
两家公司的起点相反：Vercel 从表示和开发体验向执行层下探，Cloudflare 从 runtime、状态和安全控制向开发体验上探。以下项目按系统缺口排列，发布时间只作为背景。
Vercel 向下补执行
Vercel 的起点一直是 Web 开发体验。它的 Agent 路线沿着“用户意图如何变成可运行、可审阅、可部署的 Web 软件”逐层向下补齐。
UI 成为中间表示
AI SDK
[12]
先统一模型、工具调用、结构化输出和流式 UI；
AI SDK 7
[13]
又把实验性的 HarnessAgent、带签名的审批、细粒度超时与 SandboxSession 放进同一开发表面。它的职责由此从“统一模型调用”扩展到“组织一次受控执行”，浏览器、沙箱、构建与身份则由独立能力承接。
Chat SDK
[14]
用 adapter 统一 Slack、Teams、Google Chat、Discord、Telegram、GitHub、Linear、WhatsApp 等交互渠道；
Streamdown
[15]
则处理尚未闭合的流式 Markdown。
Agent UI 呈现的是一条仍在推进的执行过程：输出逐步到达，中间夹着工具状态和审批节点，界面还要保持可读、可交互、可恢复。
json-render
[16]
更进一步：模型生成受 catalog、属性 schema、action 声明约束的 JSON 规范，再交给 React、React Native、Vue、Svelte、Solid、Ink、PDF、Email 或 3D renderer。UI 由此变成 Agent 与宿主之间的中间表示：
自然语言意图
-> 受约束 UI Spec
-> 宿主验证
-> 多端渲染
-> 人类补充输入、审阅与批准
Catalog 约束“模型能说哪些 UI 词汇”，action handler 的权力仍由业务授权、无障碍规则、稳定性测试与审计约束。
执行需要沙箱和稳定地址
Vercel Sandbox
[17]
提供临时 Firecracker Linux microVM，使模型生成的代码和命令与应用宿主隔离。它负责隔离与兼容环境；任务规划、长期 memory、业务审批、网络和凭据策略由上层控制面继续承担。
agent-browser
[18]
则把浏览器动作变成面向 Agent 的 Rust CLI/daemon：直接连接 CDP，使用 accessibility snapshot 和稳定元素引用，提供批处理、截图、diff、trace、console、HAR、session/profile，以及 allowed domain、content boundary、action policy 和 confirmation 等治理能力。项目的重点是把观察—行动—再观察压缩成低 token、可追踪的机器接口，范围已经超过性能更快的 Playwright 包装。
portless
[19]
揭示了另一个真实瓶颈：并行 Agent 和多个 worktree 很难可靠判断
localhost:3000
属于谁。稳定命名的
.localhost
URL、自动端口分配和 worktree 子域，为每个开发环境提供机器可寻址的地址。它负责地址稳定性，应用状态仍需独立管理；本地 CA、443 端口和主机服务也会扩大本机信任面。
ai-cli
[20]
把图像、视频、音频、文本、语音与转录能力做成 stdin/stdout、JSON metadata、可预测文件和退出码。它位于 planner 与 memory 之下，提供 Agent 偏好的执行工具形状：非交互、可组合、结构化结果、明确失败。
底层接口走向可观察、可验证
scriptc
20c3a6c
[21]
最能体现 Vercel Labs 对可观察编译边界的探索。它从 TypeScript checker 生成 typed IR，再经 LLVM 或 C backend 产生 native executable：
TypeScript
-> 真正的 TypeScript checker
-> typed IR
-> LLVM 或 C backend
-> clang
-> native executable
它将程序分成三个明确层级：
能静态证明的部分编译为 native code；
--dynamic
才为 npm JS 或
any
代码嵌入
QuickJS-ng
[22]
，并验证静态/动态边界；
无法降低的构造显式拒绝，避免静默改变语义。
其 C runtime 包含引用计数和 cycle collector、stackful fiber、事件循环以及按需链接的功能单元；测试把同一语料分别跑在 Node 和 native binary 下，对 stdout、stderr 和退出码做差分，并提供 ASan 与引用计数审计。项目声称静态程序约 2.4ms 启动、170–200KB binary、典型 1–4MB RSS；这些应视为项目自报基准，而非对全部 TypeScript 的普遍结论。
scriptc
的启发来自它对兼容边界的处理：边界可观察、可拒绝，也能进入差分测试。限制同样明确：构建仍依赖 checker、clang 和目标 ABI，网络、文件、时间与进程仍引入外部状态，动态 tier 仍带 JS engine，npm 原生扩展和 JavaScript 的极端动态行为继续存在。它证明了更严格的编译契约；TypeScript 与 Rust 仍承担不同职责，单文件分发也只覆盖环境闭包的一部分。
Native SDK
[23]
走的是另一条路：Zig engine、自有
.native
声明式 markup、Model/Msg/pure update、参考 renderer、record/replay、state fingerprint、accessibility snapshot 和 automation server。它试图让 UI 本身可观察、可驱动、可回放，默认 native surface 可以没有浏览器、WebView 或 JS runtime。
项目也保留可选 WebView composition，且 macOS 支持最深、移动端仍实验性、整体处于 pre-1.0。参考 renderer 可以稳定自身状态转换，OS 字体、IME、GPU 和窗口系统仍会影响最终像素结果。
vgpu
[24]
自称 “agentic-first WebGPU library”，使用显式 GPU context、WGSL reflection，并提供 deterministic mock adapter，让 Agent 可以在没有真实 GPU 时检查 bind group、pipeline 与调用结构。它表明 Agent 友好的底层 API 正在强调显式状态、反射、结构化错误和可模拟性。现阶段证据只覆盖 API 设计探索，尚未延伸到 Vercel 的 GPU 云路线。
Mock 能验证调用契约；真实浏览器、Dawn、驱动、浮点与并行调度仍需独立验证。
构建图先于 Agent
Turborepo
[25]
说明这条路线早于 Agent 热潮。
Vercel 在 2021 年正式收购 Turborepo
[26]
，将 CLI 开源并让创始人 Jared Palmer 加入。它最初解决大型 JavaScript/TypeScript monorepo 的构建速度；到了 Agent 时代，同一套机制又成为一张可执行、可缓存、可检查的确定性工作图：
Package Graph + turbo.json
-> Task DAG
-> 显式 inputs / env / dependencies / outputs
-> 内容哈希
-> 本地或远程 cache
-> 日志、artifact、run summary 与退出状态
模型每修改一次代码，都需要重新回答“哪些任务受影响、先跑什么、什么已经验证过、哪些结果可以复用”。Turborepo 的价值是把这个判断从模型的自然语言猜测，降低为可执行的 DAG、哈希和缓存协议：
--affected
、filter 和
prune
缩小观察、构建与部署范围；
task graph 将依赖顺序和可并行性显式化；
task hash 把文件、依赖、配置与环境输入压缩成可比较指纹；
local/remote cache 将一次已完成的确定性工作转化为可复用 artifact；
run summary、
--graph
、
turbo query
与浏览器 devtools 让仓库结构和执行结果机器可读。
Turborepo 的 AI 指南
[27]
已经不再只是泛泛建议：它提供官方 Agent Skill，建议并行 Agent 使用 Git worktree，允许为 task 添加 description，并提供
turbo docs
、Markdown content negotiation、
.md
路由、机器可读 sitemap 和版本化文档。当前源码甚至有独立的
turborepo-ai-agents
[28]
crate，通过
AI_AGENT
、
CODEX_SANDBOX
、
CLAUDE_CODE
、Cursor、Gemini 等环境信号识别调用方，并把 agent name 纳入 telemetry。
Turborepo 自身也完成了一条典型的原生化路线。它最初选择 Go；Vercel 在 2023 年公开了渐进式
Go→Rust 迁移
[29]
，一度采用 “Rust-Go-Rust sandwich” 分阶段替换。迁移动机包括与 Turbopack 共享底层能力、细粒度内存控制、生态复用和跨平台分发；当前 README 已将其描述为 Rust 编写的构建系统。真正收益来自减少两套工具链的重复实现，并把热路径和跨语言边界统一到同一系统生态。
2026 年，Vercel 工程师又用后台 Agent 寻找优化候选：先把难读的 trace 降低为 grep-friendly Markdown profile，再由人选择方案，并在同一 Sandbox 中用
hyperfine
对照验证。项目最终报告 task graph 计算提升 81–91%，特定仓库最高 96%；
原文
[30]
也记录了无人值守循环过高的错误率，因此大型仓库基础工具仍由人筛选方案。比性能数字更可复用的是这套分工：
机器可读观测
-> Agent 提案
-> 人类筛选
-> 隔离环境中的成对基准
-> PR 与回归证据
Agent 提高了候选方案的吞吐，人类筛选与成对基准却仍决定优化能否成立。生成瓶颈已经后移到验证。
Turborepo 位于 Agent runtime 之下，提供任务图与证据压缩。它假设被缓存任务在已声明输入下是确定性的；漏掉环境变量、文件或 output 会产生错误 cache hit，部署等有副作用的任务必须
cache: false
。远程缓存的 HMAC-SHA256 artifact 签名可以校验来源，业务授权、沙箱、审批与结果正确性仍由其他边界负责。
同一条 Rust 编译路线还包括
SWC
[31]
，它与 Vercel 的关系来自作者任职和产品集成。
Next.js 11.1 公告
[32]
记录了 SWC 创建者 DongYoon Kang 加入 Vercel 的 Next.js 团队；
Next.js Compiler
[33]
则以 SWC 承担编译与压缩热路径，并在不兼容配置下保留 Babel 回退。
团队并入补齐闭环
Vercel 的收购、团队加入与已宣布交易，可以按它们补上的系统能力理解：
Turborepo（2021）补仓库任务图、增量执行、远程缓存与构建协作；
Grep
[34]
（2024）补代码搜索和真实用例检索；
Tremor
[35]
（2025）补 React、Tailwind、Radix 的数据 UI 原语，并明确服务
v0
[36]
；
NuxtLabs 团队加入 Vercel
[37]
（2025），带来 Nuxt 与跨平台 server runtime Nitro，官方直接称其可承载 API 与 AI Agents；
Vercel 宣布收购 Better Auth
[38]
（2026），把焦点推进到每个 Agent/subagent 自有、可撤销、可缩小的身份与授权。
这些动作正在拼出一条连续的开发闭环：
找到正确上下文
-> 生成受约束界面
-> 在可移植 runtime 中执行
-> 用独立身份承担副作用
这些项目共同指向一条从开发者意图到可部署 Agent 应用的默认路径。它为判断 Vercel 的战略方向提供了依据；Labs 项目的产品化与托管控制面的开放程度，仍需逐项等待交付证据。
Context 开始包管理化
vercel-labs/skills
[39]
是跨 Agent 的安装、发现与更新工具，职责区别于 Vercel 的官方 Skills 内容。Vercel CTO 将它称为 “package manager for agent context”，因为它管理的已经是来源、解析、安装范围与更新，而非简单复制
SKILL.md
。
在固定的
e173b8c
快照中，它已经支持 70 余种 Agent 配置，并提供：
add/list/find/update/remove/init
，以及无需持久安装、临时生成 prompt 或启动目标 Agent 的
use
；
GitHub shorthand/URL、GitLab、任意 Git URL、本地路径和
.well-known/agent-skills
等来源；
project/global 两种 scope；
先复制到规范化
.agents/skills
，再向 Claude Code、Codex、Cursor 等各自目录建立 symlink，或选择独立 copy；
skills.sh
[40]
API 搜索、安装计数和 owner 过滤；
source、ref、skill path、folder hash 与更新时间等 lock metadata。
项目级
skills-lock.json
[41]
对目录内所有文件按路径排序后计算 SHA-256，并刻意不写 timestamp，以减少分支合并冲突；全局 lock 则记录 source URL、ref、GitHub tree hash 与安装/更新时间。这已经出现 package manager 的三个核心属性：来源、解析和变更检测。与 npm/Cargo 相比，它的可复现解析仍较有限：普通 branch ref 会漂移，folder hash 只能发现变化，签名发布、不可变版本和作者身份还需额外机制。
开放网络来源已有一组基础防护。
well-known provider
[42]
的 v0.2 格式要求
sha256:
digest；archive 解包限制为 50MB/1000 files，并拒绝绝对路径、
..
、symlink、hard link 和加密 ZIP。installer 还做 skill name/subpath 清洗、目标目录边界检查、Git transport allowlist 和 source/destination overlap 防护。
安全边界也写在源码里：
partner audit
[43]
请求超时或失败时返回
null
，安装流程只展示风险结果，明确采用 advisory、fail-open；
-y
还能跳过最终确认。CLI 只负责复制 skill 中的脚本和资源，脚本审查与后续执行权限仍由宿主负责。
Vercel 在 2026 年 2 月公布的 “69,000+ skills、200 万 CLI installs” 属于公司自报快照；同一篇文章也承认出现过 Markdown 看似正常、附带 Python reverse shell 的 Skill，并因此引入 Gen、Socket、Snyk 审计。
Skills Night 原文
[44]
此外，CLI 默认发送 install/remove/update/find 等 telemetry；
DISABLE_TELEMETRY
或
DO_NOT_TRACK
可以关闭。安装统计驱动 skills.sh 的搜索与排行榜，也为 Vercel 提供了生态观测面：
哪些 Agent 被使用
-> 哪些 Skills 被安装
-> 哪些框架知识最缺
-> 哪些工具和部署路径值得成为默认
Vercel 尚未因此控制 Agent Skills 标准，但 Context 分发已经显现网络效应：在 Agent 真正执行之前，谁更容易被发现、安装和更新，谁就更容易成为默认路径。至于一个 Skill 怎样进入企业环境、模型会吸收哪些通用技巧，以及组织还必须保留哪些责任，第九节再集中讨论。
Cloudflare 向上补体验
Cloudflare 手里先有全球网络、隔离 runtime、状态与安全控制，缺的是把这些能力组织成连贯的 Agent 开发体验。
状态构成平台护城河
Cloudflare Agents
[45]
建在 Durable Objects 上：每个 Agent 可以拥有持久身份、SQLite/storage、生命周期、休眠唤醒、WebSocket、schedule、MCP、Workflows/HITL 与观测。它将一次性 serverless function 扩展成全球分布的 stateful actor。
它的文档把三类状态放进不同的恢复路径：需要实时同步给用户的小型进度放 Agent state；代码、依赖、日志和产物放 Sandbox filesystem；跨越单次请求、需要重试或等待外部事件的任务交给 Workflows。
Agents + Sandbox
[46]
与
Agents with Workflows
[47]
分别回答三种故障后的问题：界面进度从哪里恢复，执行产物在哪里保留，长任务由谁继续推进。
模型可以替换，平台更难复制的是运行环境及其控制面：
受控网络与存储；
长连接和调度；
可恢复工作流；
沙箱或容器；
远程浏览器；
日志、trace 与计费；
组织级身份和策略。
Cloudflare 已经拥有其中大部分。它的 Agent 战略由此围绕既有平台能力展开：把网络、状态、安全与执行环境编排成长寿、可恢复的执行单元。
托管浏览器独立成层
Browser Run
[48]
在 2026 年从 Browser Rendering 更名，官方定位是供代码与 AI 控制的 headless Chrome，支持 Puppeteer、Playwright、CDP、MCP/WebMCP、Live View、recording 和人类接管；随后又
把底层重建到 Containers
[49]
。
Cloudflare Puppeteer
[50]
与
Playwright fork
[51]
是面向这一服务的开源客户端适配层；浏览器服务控制面仍由 Cloudflare 托管。
Playwright fork 也明确列出 Test、Components、Firefox、Android、Electron、video 等未完整支持项。它实现的是有限协议兼容，托管浏览器与本地浏览器仍存在产品边界。
产品拆分也在发生。
Cloudflare 已弃用 Sandbox SDK 中的 desktop feature
[52]
，并将浏览器自动化迁往 Browser Run。代码执行环境与浏览器身份/会话宿主由此分开：前者承载不受信任计算，后者承载昂贵、长寿、带凭据的 Web 能力。二者对应不同的风险与恢复模型，统一称作 “sandbox” 会丢失这层差异。
Web 开始主动服务机器
Nimbus
[53]
是 Astro 文档栈，默认考虑
.md/.mdx
twins、
llms.txt/full
、JSON-LD 和 Agent handoff。文档由此开始同时为人类和机器提供第一方表示。
Cloudflare Skills
[54]
将 Workers、Agents、Durable Objects、Sandbox、Wrangler、Cloudflare One 的操作知识、commands 和远程 MCP server 组织成可安装资产。
Agent Readiness
[55]
则把 robots、sitemap、Markdown content negotiation、API catalog、OAuth discovery、MCP server card、Skills index 和 WebMCP 放进同一套站点机器界面。
Cloudflare 同时在塑造 Agent 读取和操作 Web 的方式。其扫描数据属于厂商自有测量，证据范围有限；“网页需要第一方机器接口”则已经成为清晰的产品方向。
Cloudflare 的 MCP 设计也体现了上下文压缩：其 API MCP 用
search()
和
execute()
两个入口渐进发现数千个端点，避免在调用开始时注入全部 schema；
Code Mode
[56]
让模型生成的组合代码运行在隔离 Worker 中，默认无法直接出网，凭据仍留在宿主 callback。这套设计把工具发现、组合执行、凭据持有和审批分配到不同信任域。
Rust 仍受 V8 能力边界约束
workers-rs
[57]
的真实链路是：
Rust
-> wasm32-unknown-unknown
-> wasm-bindgen / worker-sys JS FFI
-> index.js + wasm
-> Wrangler
-> workerd / V8
workers-rs
是通往 workerd/V8 的 Rust→Wasm 绑定层，而非 Rust-native workerd、WASI component runtime 或 Cloudflare Agents SDK 的 Rust 版本。Rust 在这里承担受控宿主中的计算内核，最终能力仍由 JavaScript/Wasm 边界和 workerd 提供。区分 Rust、Wasm、单文件与沙箱，才能看清真实隔离模型。
收购补齐平台缺口
按基础设施缺口排列，Cloudflare 近年的相关并入形成了以下链条：
PartyKit
[58]
（2024）：实时协作与 stateful serverless；
Baselime
[59]
（2024）：高基数日志、trace 与 serverless observability；
Outerbase
[60]
（2025）：数据库与 Agent 数据体验；
Replicate
[61]
（2025）：模型打包、目录与 GPU inference 服务；
Human Native
[62]
（2026）：许可数据、内容结构化与 Agent/发布者经济关系；
Astro
[63]
（2026）：内容型 Web 与文档层；
VoidZero
[64]
（2026）：Vite、Vitest、Rolldown、Oxc 与本地到部署的工具链。
这些能力分别覆盖状态、观测、数据、模型、内容、Web 框架和构建。VoidZero 把这条线进一步推到本地工具链：Cloudflare 明确提出让 Vite deploy 根据应用意图自动配置 D1/R2 等资源，并承诺 Vite、Vitest、Rolldown、Oxc、Vite+ 保持 MIT、开源和 vendor-neutral。当前证据属于公司宣布的整合方向和前瞻性陈述，具体产品仍待交付。
这些公开动作呈现出一条可能的纵向平台路径：本地项目语义由 Vite/Oxc 理解，运行在 Workers/Containers，状态落在 Durable Objects/D1/R2，需要时调用 Replicate/Workers AI 和 Browser Run，再由 Baselime/平台 observability 提供证据。它用于解释公司方向，尚不代表已经交付的统一产品架构。
Vercel 与 Cloudflare 相向而行
Vercel 与 Cloudflare 的项目表面不同，向外扩张的结构却逐渐接近：
Agent 会优先使用它能看懂、模型熟悉、安装简单、反馈清晰的工具。开源项目和 Skills 既服务开发者分发，也会进入模型上下文、代码语料与团队规范，形成“默认选择先验”。平台公司可以开放边缘的 SDK 和协议，同时在托管执行、全局状态、身份、GPU、浏览器与审计层变现。
四股力量争夺操作层
Vercel 与 Cloudflare 之外，还有两股纵向整合力量：模型公司从 inference 和 chat 向下进入文件、终端、浏览器、桌面与设计；OpenClaw、Hermes 一类开源项目则从本地 Gateway 与 IM 入口横向包住多种模型和工具。
这里的 “Operating Layer” 指一组持续责任：把意图翻译成任务，选择上下文和工具，持有身份与状态，调度执行环境，再把证据和控制权交还用户。它未必以新的操作系统品牌出现。开发平台与云厂商已经展示了底座如何纵向整合；模型公司接下来要争夺的，是这套底座与最终用户之间的完整工作流。
四、模型公司吞并数字工作
Coding 只是楔子
“模型公司试图接管一切”抓住了纵向整合动机，也容易高估当前完成度。只提供 token 的公司无法控制上下文质量、工具可靠性、执行安全、最终体验与用户关系；账户、订阅、memory、模型、harness、桌面入口和任务结果共同到位以后，完整反馈环才会闭合。
Coding 是最自然的第一块楔子，因为代码世界已经为 Agent 准备好了半套操作系统：
repository 和 filesystem 提供结构化外部记忆；
shell、Git、compiler、test runner、
rg
等提供可组合动作；
Diff、类型检查和测试提供相对客观的 judge；
branch、worktree 和 commit 让大部分动作可隔离、可回滚；
开发者愿意容忍 CLI、日志和显式权限等早期产品摩擦。
这解释了为什么 Claude Code、Codex CLI、Gemini CLI 首先在编程里证明长循环。
Coding 提供了最便宜的行动与验收环境，却只是 Agent 扩张的第一站。Harness 一旦学会读取文件、调用工具、保留状态、并行分解与验证结果，同样的骨架就可以向研究、运营、财务、文档、演示、设计和跨应用流程迁移；改变的主要是 Skills、连接器、artifact renderer、权限策略与 judge。
并购补齐闭环
纵向整合也发生在产品界面之下。模型公司开始把 Agent 执行链上的关键瓶颈纳入同一工程反馈回路：
runtime 与工具链
-> API 与工具连接
-> 评测、安全与反馈
-> GUI 与桌面行动
-> 持久执行环境
Anthropic 在 2025 年 12 月收购 Bun
[65]
，将 Claude Code 已经依赖的 JS/TS runtime、包管理、bundler、test runner 与单文件分发纳入自身基础设施，同时承诺 Bun 保持 MIT 和开放开发。随后，
Vercept 收购
[66]
补 computer use 的视觉感知与 GUI 交互，
宣布收购 Stainless
[67]
补 OpenAPI → 多语言 SDK、CLI 与 MCP server 的工具连接。三笔动作依次覆盖执行、行动与连接。
OpenAI 的链条更偏向 Codex 与企业部署：
Promptfoo 已加入 OpenAI
[68]
，为 Agent eval、red-team 和安全治理补反馈层；OpenAI 又先后
宣布拟收购 Astral
[69]
与
拟收购 Ona
[70]
，前者带来 uv、Ruff、ty 组成的 Python 高频执行与验证链，后者提供安全、持久、客户可控的云环境。两笔交易截至研究日仍受 closing 条件约束。
已经完成的 Sky 收购
[71]
则把屏幕理解、macOS 应用操作和桌面入口补到 ChatGPT 一侧。
OpenClaw 代表第三种关系。OpenAI
没有收购 OpenClaw
；创建者 Peter Steinberger 加入 OpenAI 后，项目进入独立的 501(c)(3)
OpenClaw Foundation
[72]
，继续保持 MIT、开放与多模型中立。OpenAI 是主要捐助者，并在内部成立 Peter 领导的 Claw Labs，推进共享产品改进。这种“作者加入 + 基金会资助 + 技术合作”让 OpenAI 获得 personal-agent Gateway 与长期 Harness 的一手经验，同时保留 OpenClaw 的跨模型公共位置。
因此，开源生态出现了三种不同的控制关系：Bun 代表所有权整合，OpenClaw 代表影响力合作，MCP 与 AGENTS.md
进入 Linux Foundation 旗下 AAIF
[73]
的做法则代表中立标准治理。模型公司争夺的也不只是源码；维护团队、兼容性语料、默认集成、分发渠道和生产反馈，往往更加稀缺。
Anthropic 的产品线把这条扩张路径呈现得最完整：
Claude Chat
负责对话、思考与轻量生成；
Claude Code
把模型放进 repo、shell、Git 与测试构成的工程闭环；
Claude Cowork
[74]
明确复用 Claude Code 的 agentic approach，把目标执行扩展到本地文件、Slack/Drive 等连接器、浏览器、subagent、scheduled task，以及文档、表格、演示等知识工作 artifact；
Claude Design
[75]
再提供 chat + canvas + direct manipulation 的专用创作表面，读取 codebase 和设计文件形成 design system，并把可编辑 prototype、PPTX、HTML 或 handoff bundle 交给 Claude Code。
Claude Design 与 Claude Code 的双向同步
[76]
尤其有代表性：
/design-sync
、
/design
和 design-to-code handoff 让“意图 -> 视觉探索 -> 设计约束 -> 实现 -> 部署”共享上下文与 artifact。Claude Cowork 则把同一思路推向非工程岗位；Anthropic 2026 年 7 月披露，Cowork 超过 90% 的使用量来自软件开发之外，主要集中在业务运营与内容创作。
Cowork Web/Mobile 公告
[77]
OpenAI 走的是从通用入口与 Coding 专用执行器汇合的路线：
ChatGPT
先拥有通用对话、搜索、memory、voice、文件与庞大用户入口；
Codex CLI / IDE / Cloud / App
在代码、terminal、worktree、sandbox 与并行 Agent 上构建专用执行闭环；
到 2026 年 7 月，新的 ChatGPT desktop shell 同时容纳
Chat、Work 与 Codex
，其中 Work 面向研究、分析和成品交付，Codex 保留软件开发与本地 repo 工作；内置 browser 同时服务 Work 和 Codex。
这里发生的是
桌面宿主与能力平面共享
。
OpenAI 当前说明
[78]
仍将 Codex 作为独立 view，历史也与 ChatGPT 分开；
内置浏览器
[79]
则成为两者共享的行动面。共享宿主没有抹平两个产品各自的任务状态。
越通用，越难验收
模型公司正在为不同类型的工作寻找各自的监督与 artifact 表面：
从 Coding 向上扩张会提高验收成本。编译器可以判定语法，测试可以检查一部分行为；一份董事会材料是否抓住重点、一次客户沟通是否合适、一个视觉方向是否符合品牌、一次采购是否应该发生，都没有同等便宜的 verifier。通用 Agent 因而会更依赖来源引用、领域 Skill、组织 policy、人工审批、角色分离和可逆草稿，Coding 场景的“测试绿了就合并”无法直接照搬。
权力与风险也随纵向整合一起集中：同一提供方可能同时看到用户的对话、文件、浏览历史、登录页面、组织知识和动作轨迹，又提供模型、memory、插件目录、judge 与计费。便利性越高，越需要可导出的 session/artifact、可替换模型与工具、独立审计、scoped identity、最小权限，以及把高风险 approval 放在 Agent 自身不可伪造的边界上。MCP、WebMCP、Agent Skills、开放 CLI 和本地 Gateway 为闭环保留可替换性，降低用户被单一供应商完整锁定的风险。
模型公司向更多工作扩张以后，单一聊天框已经装不下整条链路：执行需要 CLI，异步触达需要 IM，复杂监督需要桌面工作台，跨应用行动又需要浏览器。产品扩张因此会先表现为入口分化，但这些入口必须共享同一份任务状态和证据。
五、入口分化，状态合流
从界面历史看，Agent 编程先后出现聊天框、CLI/TUI、IDE、桌面 GUI 与 Browser/Computer Use。时间顺序容易制造“新界面替代旧界面”的错觉，实际发生的是入口分工：
CLI 留在行动底座，其他表面围绕异步任务、监督和接管继续生长。
CLI 是行动总线
2025 年，终端首先成为 Agent 编程的主战场：Anthropic 在 2 月将
Claude Code
[80]
作为命令行 Agent 研究预览发布，OpenAI 在 4 月推出
Codex CLI
[81]
，Google 在 6 月发布开源
Gemini CLI
[82]
；2026 年又出现 Antigravity CLI 与官方 Grok Build。
原因远超工程师对命令行的偏爱。代码仓库原本就生活在 shell、Git、package manager、compiler、test runner、
rg
、
curl
和部署 CLI 组成的世界里。终端为 Agent 提供了少见的一组共同属性：
文本输入输出紧凑，适合进入模型上下文；
stdin、stdout、stderr、退出码和文件产物易于组合；
命令可以在本机、容器、CI、SSH 与远程 sandbox 中复用；
Git diff、测试日志和构建 artifact 天然构成验证证据；
非交互模式容易设置 timeout、工作目录、环境变量与权限边界；
一次动作可以被记录、重放和比较，而不必解释整套图形界面。
Claude Code 的 CLI 参考
[83]
同时支持交互 REPL、一次性
-p
、管道输入和会话恢复；
Codex
[84]
既可交互运行，也能以
codex exec
进入脚本和 CI；
Gemini CLI
[85]
将文件、shell 与 Web search 暴露为工具。
Google 从 Gemini CLI 转向 Antigravity CLI，是界面分层的直接案例。
官方公告
[86]
先肯定终端是优秀的 Agent 界面，再指出多 Agent、异步任务和跨界面工作需要统一后端；新的 Go CLI 支持后台异步工作，并与 Antigravity 2.0 桌面应用共享 Agent harness。
同一个 core engine 因而拥有两个表面：CLI 面向键盘、SSH、低开销与脚本，桌面端面向视觉编排和项目管理，
会话还可以从终端导出到 GUI 继续
[87]
。
Gemini CLI 目前只停止了个人免费、Google AI Pro 与 Ultra 账户经 Gemini CLI/Gemini Code Assist 发起请求的入口；Standard、Enterprise、Google Cloud 和付费 Gemini API key 仍获支持，Apache-2.0 仓库也继续接收模型、bug 与安全更新。
与此同时，xAI 2026 年 5 月发布的正式名称是
Grok Build
[88]
，它同时提供
交互式 TUI、headless 脚本模式与 ACP 嵌入
[89]
。CLI 已从早期的唯一界面，演化成可被不同宿主复用的 Agent runtime 表面。
Bun 缩短执行环
Bun
[90]
位于这条链路的执行层，和 Claude Code、Codex 这类 Harness 分属不同层次。它把 JS/TS runtime、package manager、test runner、bundler、package runner 与单文件编译收进一个 executable，使 Agent 生成的临时脚本、工具 CLI 和验证命令更快启动、更少依赖额外拼装：
Agent CLI / Harness
-> shell tool call
-> Bun / Node / Python / uv / rg / Git
-> filesystem / process / network / OS
这类底座的价值是缩短
生成脚本 -> 安装依赖 -> 执行 -> 测试 -> 读取结果
的循环，并让分发形状更适合自动化。Planner、memory、approval、identity、任务恢复与 sandbox 仍由其他层负责。Anthropic 收购 Bun，正是把这条高频 JS/TS 执行链纳入 Claude Code 的反馈回路；它依然只服务采用 Bun 的工作流，尚未成为所有 Agent CLI 的共同底座。后文的 Zig→Rust 重写，则继续解释这条执行底座如何原生化。
rg
是低成本雷达
Codex 的打包脚本
[91]
把
rg
纳入运行路径，并校验下载文件的大小与 SHA-256。这个选择对应着 Agent 进入大型仓库时的第一项需求：快速获得一幅可导航的代码轮廓。
rg
启动快、只读、跨平台，无需维护常驻索引；
rg --files
可以枚举候选文件，文本搜索可以继续收窄范围，退出码和
--json
又便于接入脚本化循环。它由此成为 Harness 中低成本、可组合的词法感知原语。
ripgrep FAQ
[92]
指出，并行搜索不会保证结果顺序，稳定输出需要
--sort path
；默认规则还会跳过 ignored、hidden 和 binary 文件，并且不跟随 symlink。这些策略原本用于换取速度与低噪声，进入 Agent 回路后，也会直接影响搜索可见性和结果复现。Harness 需要显式管理搜索范围、排序与输出规模，语义索引、权限治理和安全执行再由上层承接。
CLI 与
rg
建立了高密度的本地行动—观察回路。随着任务变长，新的压力落在任务连续性上：进程如何越过当前终端继续运行，状态、审批与结果又如何抵达人所在的入口。由此，Gateway 开始成为下一层基础设施。
Gateway 让 Agent 常驻
在 CLI 成为主战场的同时，另一条分支把 Agent 接进 Telegram、Discord、Slack、WhatsApp 等日常通信入口。人可以离开工作台，在手机上继续补充目标、查询状态、接收文件、停止任务或处理审批。IM 由此成为异步任务的
interrupt、attention 与 delivery surface
，价值远高于聊天皮肤。
Gateway 决定了这种远程入口能否承载持续任务。只把 webhook 转发给模型的 bot 没有持久责任；Agent Gateway 要把渠道消息规约为带身份、会话、顺序、幂等与投递状态的事件，再把同一任务映射到持久 Harness 和执行宿主：
这一层必须处理大量模型之外的问题：同一条 inbound 是否已消费、运行中的新消息是排队还是 steer、进程崩溃时 final response 到底有没有发出、附件落在哪里、一个 channel 是否共享 memory、远程
/approve
究竟批准了哪条命令。IM 账号身份也不能自动继承本机操作权限；“能给机器人发消息”与“能批准在某台机器执行某个 argv、cwd 和 credential scope” 必须是两份契约。
Pi：小内核，大扩展
earendil-works/pi
[93]
把 Agent 的机械结构拆得足够清楚，因此适合作为从 CLI 走向可扩展 Harness 的样本：
pi-ai
-> provider、stream、tool schema 与跨供应商兼容
pi-agent-core
-> loop、event、steering、follow-up 与 tool hook
pi-coding-agent
-> CLI/TUI、session tree、compaction、Skills、extension、RPC
它选择“最小 Harness + 最大可塑性”：plan、subagent、handoff、permission gate 和产品形态可以由 extension 或 package 组合，无需全部固化进 core。现有 JSONL session tree 已支持 branch、fork 与 compaction；compaction 还要维护 tool call/result 边界、文件操作累积和超长 turn。这比“自动总结历史”更接近状态迁移。Active run 的 crash-durable resume 仍在推进，当前能力属于 durable session，尚未覆盖 durable execution。
Pi 的
packages/server
[94]
目前是 experimental 本地 RPC 进程监督器，公网与 IM Gateway 由其他组件承担。第一方聊天形态来自独立的
pi-chat
[95]
，当前源码适配 Discord 与 Telegram。它把一个 channel 映射为独立 session、JSONL log、workspace、memory、Skills、worker 与 Gondolin micro-VM；于是 channel 从消息地址变成了 Agent 的持久责任边界。
当前实现的边界同样明确：日志和渠道 cursor 可持久化，
pendingJobs
尚不会从未完成的
job_queued
记录重建，因此任务队列还未达到 crash-durable；Pi core 默认继承启动用户的文件、进程、网络与凭据权限，sandbox 和逐动作审批需要外部宿主。Project trust 只决定是否加载项目资源，真正隔离依赖 Gondolin、Docker、OpenShell。它证明了扩展性，也揭示了可插入安全接缝与默认安全闭环之间的距离。
OpenClaw 重 Gateway，Hermes 重自进化
OpenClaw
[96]
与
Hermes Agent
[97]
都把 CLI、IM、Skills、memory 与 subagent 组合起来，责任重心却不同：
这里讨论的是独立基金会治理的 OpenClaw 开源实现。创建者加入 OpenAI、OpenAI 资助基金会并成立 Claw Labs，并未改变项目的多模型定位；前文已经将这种影响力合作与直接收购分开。
核心
：OpenClaw 以长期运行的 Gateway 和 typed control plane 为中心；Hermes 以 Python
AIAgent
loop 和多 surface Harness 为中心。前者先服务化 Agent，后者先强化执行内核。
远程入口
：OpenClaw 让 IM、Web、desktop 和 nodes 接入同一 Gateway；Hermes 提供 20 多种 platform adapter、relay、CLI/TUI/API。两者都把 IM 当作远程打断、审批和交付面。
Skills 与 memory
：OpenClaw 提供分层 skill roots、proposal/scan/rollback、Markdown 与 hybrid recall；Hermes 提供
/learn
、background review、skill/memory 自改善和 FTS history。程序性记忆开始生长，也随之需要治理。
Subagent
：OpenClaw 使用 SQLite registry、yield/wake/handoff 和重启后的语义续跑；Hermes 强调 fresh child、live transcript、cost/file rollup 与 durable completion。两者首先保证子任务结果可交付，执行栈原地恢复则是更强的能力。
结果投递
：OpenClaw 能向 adapter 对账时执行 reconcile，无法证明时可以拒绝盲目重发；Hermes 使用 durable ledger，崩溃歧义时重发并显式标记“可能重复”。Exactly-once 通常不可得，关键是识别并暴露未知状态。
OpenClaw 最接近 personal-agent Gateway control plane：Gateway 统一 channel、operator client、node capability、session、approval、delivery 与 child lifecycle。它把审批做成持久、可核验的授权记录，绑定 node、argv/plan、cwd、agent/session、channel/thread 与 requester device，
allow-once
只能消费一次。这比 Telegram 中一个脱离原动作的“同意”更接近 capability authorization。
审批绑定实现
[98]
Hermes 更接近 self-improving Harness：它把 loop guardrail、context compression、超大工具输出落盘、background memory/skill review、session lineage 和 delegation observability 做进执行内核。完整输出先落到当前 local/Docker/SSH/cloud backend，再由 Agent 分页读取，避免塞满 context；这类小机制往往比增加复杂 planner 更直接地提高长任务完成率。
Agent loop
[99]
两者都迫使
durable Agent
从一个布尔标签拆成可验证的问题：
inbound message、session 与 task record 是否耐重启；
运行中的 child 是从语义 checkpoint 继续，还是只把已完成结果送回；
final delivery 能否对账，还是只能诚实地 at-least-once；
filesystem rollback、Agent computation checkpoint 与外部副作用补偿分别覆盖什么；
approval 是否绑定原动作，重启后是否仍然有效。
功能表之外还要观察默认安全：OpenClaw 的 sandbox 默认关闭，默认把个人 DM 汇入
main
session，多用户场景必须显式隔离；Hermes 常从 local backend 起步，Gateway command approval 是进程内 per-session FIFO，skill/memory write approval 默认也未采用全局保守模式。两者展示了能力上限和快速演化的执行边界，企业安全基线仍需部署者配置。
GUI 管监督
CLI 擅长串行表达“刚刚执行了什么”；多个长任务、worktree、浏览器、终端、Diff、artifact、审批、失败恢复和远程会话则需要更宽的监督界面。随着一次 Agent 任务从几十秒增长到几十分钟甚至更久，人类的工作也从“盯着 token 流”变成：
委托
-> 离开
-> 被需要时回来
-> 看证据而不是重读全过程
-> 批准、纠偏、接管或验收
桌面应用由此成为 shell、浏览器和后台 runtime 的监督层，把它们投影为持久、可切换、可通知的工作状态。它可以同时承载：
task/thread/worktree 与并行 Agent；
Diff、测试、截图、trace 和最终 artifact；
browser、terminal、filesystem 与 drag-and-drop 上下文；
细粒度 approval、暂停、恢复和人工接管；
系统通知、托盘、全局快捷键与防休眠；
本地任务和远程任务之间的连续会话。
Anthropic 在 2026 年 4 月
重做 Claude Code Desktop
[100]
时，也把变化概括为从“一次输入、等待一次结果”转向多个任务同时在途、由人坐在 orchestrator seat。新界面把并行 session、集成终端、文件编辑器、Diff、HTML/PDF preview 与可拖拽布局放进同一个工作台，并继续要求桌面端与 CLI plugins 保持能力一致。GUI 增长发生在 Agent core 上方，承担监督、证据审阅和人工接管。
Codex 当前的界面桥接非常直白：CLI 的
/app
[101]
可以在 macOS 或 Windows 上把当前会话继续到桌面应用；反过来，桌面端把并行任务、worktree、Diff review、浏览器和 Computer Use 放到同一个监督工作台。Codex 长任务文档还把
/goal
、并行 chat、worktree、暂停/恢复、系统通知和 Pets 放在同一条工作流里。GUI 因而成为 CLI 任务的监督器。
Pet 管注意力
Pet 在 vibe coding 中提供了直观的情绪价值：长时间面对编译日志、失败重试和不确定等待时，一个有性格的动画比红点和系统横幅更有温度。它更深层的作用，是把 Agent 状态从工作台内的主动查询，转化为周边视野中的被动感知。
OpenAI 的 Pets 文档
[102]
将桌面浮动宠物定义为跨应用跟随工作状态的可选伴侣，并明确说明选择宠物只改变外观，不改变 ChatGPT 完成任务的方式。它区分四个状态：
多个任务同时活跃时，Pet 按需要输入、阻塞、完成、运行的顺序争夺注意力；
通知文档
[103]
也将其定位为用户操作其他应用时的 chat 状态跟踪。它把三种需求压进一个轻量表面：用
peripheral awareness
免去持续轮询，用
interrupt routing
把人叫回需要决定或恢复的任务，再用
emotional salience
提升关键通知的可感知性。长任务由此改变人与软件的时间关系：人可以离开工作台，只在决策、恢复和验收时回来。
拟人化必须服从运行时真相。Pet 只读投影持久任务状态，并能打开对应任务与证据；
Blocked
要如实呈现，动画只传达注意力优先级，结果仍由测试、Diff、trace 或人工验收确认。Codex TUI 的
/pets
与
/pet
说明同一机制也能存在于终端；桌面形态额外提供跨窗口悬浮、跨任务排序和离开工作台后的持续可见性。无障碍、隐私、减少动画和通知节流都属于这套状态机。
当桌面工作台同时承载本地代码、网页身份、视觉结果和人工接管，浏览器随之成为核心行动面。
六、浏览器成为能力平面
网页自动化已有多年历史。Agent 浪潮重新放大浏览器，是因为它把五种通常分散的能力放进了同一个宿主：
传感器
：DOM、Accessibility Tree、网络、console、截图、性能数据；
执行器
：点击、输入、下载、上传、导航、脚本；
身份容器
：cookie、SSO、session、设备权限；
验证与接管界面
：人类能看见最终结果，并在敏感步骤接手；
本地计算
：Wasm、WebGPU、媒体与存储让部分处理贴近用户发生。
浏览器由此成为现实世界的“最后一公里适配器”，结构化接口仍应排在行动路径前端：
稳定类型化 API
-> 后端 MCP / authenticated tool
-> 页面提供的 WebMCP
-> accessibility / semantic locator
-> DOM / JavaScript
-> screenshot + vision
-> OS computer use
越往下兼容性越强，语义越弱、成本越高、风险越大。财务交易、高吞吐写入和关键生产变更应优先使用结构化 API；浏览器适合没有 API 的兼容场景、最终视觉验证和人类接管。
AI Browser 从回答走向行动
AI Browser 已经出现三条同时推进的路线：
既有浏览器把模型、搜索与 Agent 能力内置；
新浏览器围绕 AI 重新设计 tab、memory、skill 与工作流；
更大的 Agent 工作台吸收浏览器能力，独立 browser shell 反而可能消失。
Google 走第一条路线。
Gemini in Chrome
[104]
已从“总结当前页面”扩展到 side panel、多标签上下文、Gmail/Calendar/YouTube/Maps 等 Connected Apps 和
auto browse
。在用户授权后，auto browse 可以跨页面完成多步任务，甚至借助 Google Password Manager 处理登录；购买、社交发布等敏感动作会停下来要求确认。
与此同时，
AI Mode 进入 omnibox
[105]
，让复杂搜索、追问与当前页面上下文直接进入地址栏。
两者承担不同职责：AI Mode 重构搜索与答案界面，Gemini side panel 和 auto browse 则进入观察—行动循环。Google 的优势来自模型与 Chrome 分发、Google Account、Password Manager、Search、Workspace、Android 共同构成的上下文和身份闭包。
The Browser Company 则代表第二条路线。它在 Arc 之后推出
Dia
[106]
，把产品重心从“更好的 tab 管理”推进到跨 tabs、history、G Suite、Slack、Notion 等上下文的搜索、综合、memory 与可复用 Skills。这里的浏览器不再只是承载 Agent 的窗口，而开始直接保存“今天在做什么、信息散落在哪里、下一步是什么”。
Atlassian 在 2025 年
宣布收购 The Browser Company
[107]
，公开目标是把 Dia 做成 knowledge worker’s browser：连接 SaaS apps、tabs、tasks、personal work memory 与 AI Skills，并补上 enterprise security、compliance 和 admin control。
截至研究日，
Dia 已使用 Atlassian identity
[108]
。
Atlassian 2026 年进一步披露
[109]
，Dia 正把 Teamwork Graph、Morning Brief、SSO、Chromium MDM、SOC 2 与 Guard 集成带入企业场景，部分高级企业能力仍处于 closed beta。产品重心也从 Arc 式消费浏览器转向企业知识图谱和 Agent action 的前台。
OpenAI 的 Atlas 是第三条路线的过渡案例：
迁移说明
[110]
明确它将在 2026-08-09 停止工作，浏览器 Agent 能力则进入 ChatGPT 与 Codex。长期竞争单元将更接近“每个主流 Agent 宿主都具备 browser capability”，独立 AI Browser 只是其中一种产品形态。
三条路线的入口不同，却沿着同一条能力梯度前进：
page assistant
-> cross-tab context
-> browser memory + connected apps
-> multi-step web action
-> enterprise identity / policy / audit
越往后，竞争焦点越接近“谁能在用户已有登录态和组织上下文中推进工作”。浏览器也会成为 Agent 最有价值、同时最危险的入口：不可信网页内容与高权限 cookie、password、history、企业数据处在同一表面，prompt injection 可能直接诱导真实动作。AI Browser 的护城河将由上下文隔离、敏感动作确认、组织策略、可审计 trace 和可靠人工接管共同构成。
CDP 管控制，WebMCP 管语义
Chrome DevTools Protocol
[111]
能检查、调试、控制 Chromium 的大量内部域，因此成为众多 browser agent 的事实控制 ABI。
agent-browser
、Cloudflare Browser Run、Puppeteer 和 Playwright fork 都在利用它。但 CDP 官方明确说 tip-of-tree 经常变化且不保证向后兼容；Playwright 也明确说
connectOverCDP
比自己的协议连接“显著更低保真”，并只支持 Chromium。
WebDriver BiDi
[112]
正在尝试提供跨浏览器、双向事件化的标准控制协议，但截至研究日仍是 Working Draft。
CDP 提供“怎样控制浏览器”的机械接口，页面的业务语义仍要由更高层表达。WebMCP 让站点开始主动暴露这层能力。
Chrome WebMCP early preview
[113]
与
W3C Web Machine Learning Community Group 草案
[114]
允许页面把表单或 JavaScript 函数注册为带自然语言描述和 schema 的工具。它是后端 MCP 的客户端补充：
后端 MCP 适合服务器 API 和跨站能力；
WebMCP 复用当前页面、登录态、可见 UI 和人类上下文；
页面可以在工具完成前等待人类确认；
同一个业务操作既能被人点击，也能被 Agent 以结构化方式调用。
WebMCP 把网页从像素和 DOM 的被动暴露，推进到对业务能力的主动声明。它有望减少 selector 漂移、token 消耗和错误点击，也能让人机协作更自然。
WebMCP 的安全性仍取决于宿主：恶意或被攻破的网站同样可以注册误导性工具，宿主需要校验 origin、参数、身份、权限和副作用，并对高风险动作要求确认。
Cloudflare WebMCP
[115]
目前是 Browser Run 中的 beta/lab 能力，Chrome 官方称其为 early preview。实际可用性还取决于浏览器内核版本、实验开关与宿主是否暴露对应 API；内嵌 Chromium 或系统 WebView 本身并不保证可调用。现阶段它与后端 MCP、人类 UI、headless automation 形成互补。
WebGPU 把计算带进浏览器
WebGPU
[116]
截至研究日是 W3C Candidate Recommendation Draft，它不只提供图形渲染，也提供通用 GPU computation，并映射到现代原生 GPU API。WebGL 时代浏览器主要是图形输出设备；WebGPU 加入 compute shader 后，浏览器开始成为可移植的本地并行计算宿主。
对 Agent 基础设施而言，WebGPU 有四类价值：
本地推理与预处理
：embedding、小型模型、语音识别、图像分类、视觉特征提取；
隐私与离线
：敏感数据无需全部上传远端模型；
交互延迟
：UI 内的局部模型、排序、过滤和视觉处理可以贴近用户；
渲染与验证同域
：Agent 可生成、渲染并视觉检查 2D/3D、图表、视频或 UI artifact。
Transformers.js 的 WebGPU 指南
[117]
已展示 embedding、Whisper 转录和图像分类。这证明 WebGPU 能承载实际机器学习工作负载；训练集群和远端大模型仍负责超出本地模型体积、显存、功耗与量化精度上限的工作。
vgpu
的价值正好落在 WebGPU 当前最难的部分：原生 API 显式而低级，WGSL、layout、buffer 和 pipeline 很容易写错；Agent 生成代码尤其需要反射、稳定错误和无 GPU mock。未来 “Agent-friendly” 的 GPU 抽象除了缩短语法，还要提供 capability discovery、明确资源生命周期、静态/运行时 schema、可序列化命令、deterministic simulation、可比较 trace，以及真实 GPU 与 mock 之间的差异报告。
WebMCP 与 WebGPU 是正交的两条升级：前者让网页动作从 DOM 猜测升级为语义能力，后者让网页运行时从 UI 渲染升级为本地计算。再叠加 CDP、Wasm、WebRTC、Storage 与 Permissions，浏览器正在成为 Agent 的观察、行动、语义、计算、验证与人工接管复合平面。
能力越大，风险越集中
浏览器 profile、CDP WebSocket URL、session token 和下载目录都接近凭据。可靠设计至少需要：
每任务或每信任域独立 profile/context；
域名、导航、网络和下载 allowlist；
页面内容一律按不可信数据处理，与系统指令分域；
稳定的 observation epoch，动作必须绑定产生它的文档/frame；
dispatch 前审批，dispatch 后以证据 reconcile；
screenshot、network、console、trace 和 action receipt；
CAPTCHA、登录、支付、授权与高风险动作的人类接管；
会话清理、凭据撤销与可审计重放。
Sandbox 负责限制爆炸半径，业务 verifier 负责判断动作是否正确；内容边界标记降低 prompt injection 的成功率，身份、权限和人工接管继续承担纵深防御。
浏览器把高权限身份、不可信内容和真实动作放到同一个平面，也把问题推回更底层：能力究竟运行在哪里、能触达什么，中断后又从哪里恢复。
七、环境决定能力边界
长任务会反复执行相似动作。即使单次环境差异只有 1%，在数十或数百次调用中也会从偶发故障变成经常遇到的问题。因此 scriptc、uv、Bun、rg、portless、Wasm、container 和 microVM 的共同价值，是减少两种“环境泄漏”：
ambient dependency
：隐式依赖、路径、版本、端口、系统包；
ambient authority
：默认可访问的文件、网络、凭据和进程权限。
完整的环境闭包由多项条件共同构成：固定工具链、依赖和 artifact digest，声明 filesystem snapshot 与可写范围、网络和资源策略、独立身份和隐私、时间与随机性，并为 stdout/stderr、产物、checkpoint、补偿与 cleanup 提供统一契约。
不同执行形态覆盖不同的兼容性、密度与隔离需求：
workers-rs
的 Rust→Wasm→V8、Vercel Sandbox 的 Firecracker、Browser Run 的远程 Chrome 与 scriptc 的 native binary，分别选择了不同的环境闭包。评价它们的共同尺度是宿主权力、输入边界、恢复方式和证据，而非文件数量。
到了本地桌面，环境闭包会具体落到宿主拓扑：谁持有 Chromium、Node/Rust 与系统权限，网页和 UI 通过什么 IPC 调用能力，不受信任的代码又被送到哪一层执行。Electron 与 Tauri 的差异应从这里理解。
Electron 自带完整 Web Runtime
Electron
[118]
把 Chromium 与 Node.js 打包进跨平台桌面应用。
官方进程模型
[119]
将其拆为 main、renderer 和可选 utility process；
WebContentsView
[120]
可以在一个原生窗口中承载多个独立 Web 内容表面。
这与本地 Agent 工作台的需求高度重合：
Chromium 提供 Web UI、DevTools/CDP、WebGPU、媒体与最终视觉验证；WebMCP 还取决于内核版本、实验开关与宿主暴露；
Node.js 及其 npm/外部工具生态可连接文件、Git、进程、PTY 与网络；
原生桌面壳提供窗口、通知、快捷键、系统权限与长任务入口；
多进程架构允许把 UI、网页、终端和后台 runtime 分离；
同一个工作台可以让 Agent headless 工作，也能在需要时租用可见表面给人审阅。
因此，Electron 很可能继续是本地 Agent 产品的重要选型，尤其适合浏览器优先、TypeScript 团队和需要快速跨平台交付的产品。固定 Chromium、多 Web surface、Node 工具生态和原生桌面入口共同构成它的能力闭包。
但这也意味着网页漏洞可能升级为本地代码执行。Electron 官方安全指南要求远程内容禁用 Node integration、开启 context isolation 和 sandbox、限制导航与新窗口、验证 IPC sender，并只暴露按功能收窄的 preload API。
contextBridge 指南
[121]
也明确反对直接把通用
ipcRenderer.send
暴露给页面。
一个稳健的 Agent 桌面架构应当是：
renderer
只负责 UI、订阅、投影与交互状态
main
只负责生命周期、调用者准入、窗口/表面监督和能力注册
utility / capability hosts
拥有 terminal、filesystem、browser、provider 等副作用
sandbox / microVM / remote host
承载真正不受信任的代码
所有能力集中进 main、或让显示互联网内容的 renderer 直接获得 Node 权限，都会扩大攻击面。Electron 的 utility process 提供带 Node 和 MessagePort 的 Chromium service child process，适合隔离 CPU 密集或易崩溃服务；任意恶意代码仍应进入 microVM、container 或其他专门沙箱。
Tauri 用 Capability 收窄边界
Tauri
[122]
代表另一种边界选择。它让 Rust core process 持有操作系统访问权和 IPC 路由，前端运行在操作系统提供的 WebView 中：Windows 使用 WebView2、macOS 使用 WKWebView、Linux 使用 webkitgtk。
官方进程模型
[123]
明确说 WebView library 在运行时动态链接，而不随每个应用打包；这通常能显著缩小基础安装体积，却也把浏览器版本、行为和调试差异交给了目标平台。
对 Agent 产品来说，Tauri 的关键价值在于
Capabilities
[124]
：前端可调用的 core/plugin 命令按 window、webview、platform 与 remote origin 显式列出，filesystem、shell 等命令还能进一步限制 scope。“这个表面能做什么”由此成为可检查的配置。
Capability 主要约束 frontend→Rust core 的 IPC 暴露，完整的 Agent policy 还要覆盖以下边界：
同一个 WebView 命中多份 capability 时，权限会合并；
默认注册的自定义命令若不额外声明，可能对所有窗口开放；
用户身份、逐动作审批和任务预算仍需上层策略处理；
官方明确列出它无法防御恶意 Rust core、过宽 scope、错误的命令检查、WebView 0-day 与供应链攻击。
Agent 工作台还需要 npm CLI、Python、Git、PTY、浏览器 driver 和用户既有工具链。Tauri 通过
外部 binary sidecar
[125]
承接这些 runtime，官方也提供
把 Node.js 应用编译为 sidecar
[126]
的路径。
Sidecar 名称和参数可以由 shell plugin permission 约束，但每加入一个 Node/Python/browser sidecar，就增加一套下载、签名、升级、进程监督、stdout 协议和崩溃恢复边界。一个复杂 Agent 产品最终可能重新拥有接近 Electron 的运行时重量，只是被拆成了不同 artifact。
关键是能力拓扑
如果产品核心是多个一致的 Chromium surface、浏览器调试、WebGPU、Node 生态和复杂本地工具编排，Electron 的重量对应的是它提供的能力闭包；如果产品只需要少量受约束的本地能力，希望默认缩小前端权限和安装体积，Tauri 更有吸引力。反过来说，Tauri 的 system WebView 会让 WebMCP、WebGPU、CDP 和浏览器行为随平台变化；Electron 的统一 Chromium 则扩大供应链、更新和内存成本。
两种框架遵循同一个稳健原则：UI 只投影状态，特权能力由窄接口宿主持有，不可信脚本进入 container、microVM、Wasm/isolate 或远程执行环境。框架选择决定默认边界和工程摩擦，业务身份、审批、审计与恢复仍由产品系统定义。
Codex 验证桌面形态
OpenAI 官方将 Codex App 描述为管理并行 Agent、worktree、diff review、Skills、Automations 和系统级 sandbox 的桌面 “command center”，后来又加入 in-app browser、computer use、文件与终端等工作面。
官方产品介绍
[127]
足以证明“桌面工作台 + 本地能力 + 人类监督”这个产品形态。
OpenAI 虽未公开说明 macOS Codex App 是否采用 Electron（其实在安装包内可以看到 Electron 影子），公开证据支持的是产品形态：
Codex Desktop 验证了“浏览器能力 + 本地执行 host + 多任务桌面工作台”的架构价值。
因此，Codex 适合作为桌面 Agent 工作台的产品证据，Electron 与 Tauri 仍应依据公开架构、能力分层和进程边界独立比较。
环境拓扑确定以后，语言选择才有正确的问题：每一层需要什么反馈速度、故障模型、兼容面与分发形状。
八、上层求快，底层求稳
Agent 的 Harness、入口和能力宿主逐渐分层，语言选择也呈现出清晰的成本结构：TypeScript/Python 服务高频反馈、生态连接与产品表达，Rust/Go/Zig/C++ 进入热路径、CLI、runtime、隔离和分发。所谓 “Rust/Zig 成为底层、TypeScript/React/Tailwind 成为上层标配”，描述的是这种分工，而非一场全栈语言替代。
表外还有一层正在变重：规模化算力已经进入模型公司的资本结构与研究节奏。2026 年 7 月 27 日，
SSI 宣布与 NVIDIA 建立长期战略合作
[128]
，称 NVIDIA 的大额投资将使其在 12 个月内把算力扩大到十倍；SSI 给出的理由是内部研究已经到达“值得规模化”的阶段。同日，
NVIDIA AI Infrastructure
[129]
将合作落到 Vera Rubin 平台。目前公开信息确认了合作、投资与扩容目标，尚未披露 SSI 的研究结果或验收指标。
这组一手表述揭示了算力关系的变化：前沿实验室、芯片平台和资本开始共享更长的技术路线，compute 既是资源，也是研究排期、融资结构和工程反馈速度。Agent 的长推理、多模态观察、browser/computer use 与 subagent 并发会进一步放大推理负载，最终竞争指标也会从单次 token 价格，扩展到每个可验证任务的端到端成本、时延、成功率和恢复代价。模型能力因此会与 GPU 架构、编译器、推理 runtime、网络、调度和能源效率共同演进。
React 栈正在收敛
这组技术越来越像 Agent 生成 Web 产品时的默认脚手架，各自在不同层承担责任：
React——异步 UI 模型
：组件、状态、事件和单向数据流适合表达 streaming、tool call、approval、retry 等组合状态，训练语料也最充分；状态、effect、并发和 server/client 边界仍可能被生成错。
Vite——反馈与构建环
：dev server、HMR、transform、build 和插件图提供快速反馈，错误还能回流终端；浏览器运行时继续由截图、console、network 和端到端测试验证。
Tailwind CSS——视觉语法
：utility、design token 与响应式状态和组件源码共址，class diff 清晰；代价是 class 堆积、动态拼接、token 漂移和视觉同质化。
Base UI——行为原语
：无样式、可访问、可组合的 primitives 承担 focus、keyboard、ARIA 和 popup 边缘情况；错误组合和自定义样式仍会破坏无障碍。
shadcn/ui——源码分发
：registry 将预制抽象和组件源码交给项目，Agent 可以直接读取、修改、diff 和迁移；fork 以后的升级与一致性也由项目承担。
React 的优势还来自状态表达。Agent 产品需要组合 tool call、streaming、pending、approval、error、artifact 与 retry；组件和单向数据流提供了模型熟悉、可以逐文件验证的中间层。React 官方在弃用 Create React App 时，也把无需完整 framework 的项目引向
Vite 等 build tool
[130]
，进一步强化了 UI 层与构建系统独立演进的组合方式。
Vite 8
[131]
在 2026 年把开发和生产构建统一到 Rust 编写的 Rolldown，并保留 Rollup 风格 plugin compatibility。相比项目方自报的 10–30 倍 build 提升，
server.forwardConsole
对 Agent 更有指向性：浏览器 console/error 可以回传 dev server 终端，并在检测到 coding agent 时自动启用。过去模型修改 React 后只能看
vite build
是否通过；现在运行时错误可以进入 CLI 的 observation loop：
生成/修改组件
-> Vite HMR
-> 浏览器运行
-> console/error 回流终端
-> Agent 继续修复
-> 人类做视觉与交互验收
Cloudflare 收购 VoidZero 的战略意义也在这里：Vite/Oxc/Rolldown 同时是前端工具链和 Agent 高频 observe-edit-run 循环的反馈底座。Console 提供运行时观察，screenshot、a11y tree、network trace、端到端测试和人工视觉判断负责更完整的验证。
Tailwind CSS v4
[132]
又把这一循环中的样式摩擦降低了一层：first-party Vite plugin、自动内容检测、CSS-first configuration、原生 theme variables 和 data/state variants，让 design token、组件状态和源码修改处在同一份可搜索文本里。对 Agent 而言，
bg-surface text-foreground data-[open]:...
比跨多份 CSS 文件猜 selector 和级联更局部、更易 diff；受治理的 token vocabulary 则用来控制 class 堆积和视觉漂移。
Base UI
[133]
是无样式的 React primitive library，可与 Tailwind、CSS Modules 等组合；shadcn/ui 则通过 registry 把更高层组件源码和样式交给项目拥有。两者分别位于行为原语与源码分发层。截至 2026-07，
shadcn 已把 Base UI 设为新项目默认 primitive
[134]
，同时继续支持 Radix，并将
React Aria 纳入一等选项
[135]
。完整分层更接近：
Base UI / Radix / React Aria
-> 无样式行为与无障碍 primitive
-> shadcn registry 与组件抽象
-> Tailwind/token 视觉层
-> 项目自己的源码与设计系统
这套组合以强约定提供起点，又把核心 UI 保留为项目可修改的源码。Base UI 文档提供 Markdown/
llms.txt
入口，shadcn 同时发展 registry、MCP 和迁移 Skill；Agent 可以发现组件、复制源码、按项目 token 改写，并用 Git 记录变化。生成效率解决实现摩擦，信息架构、视觉层级、品牌、触屏、国际化、无障碍和长期 design-system governance 决定最终产品质量。
由此可以把 React + Vite + Tailwind + headless primitives/source-owned components 视为 Agent Web 开发的高概率默认路径。Next.js、React Router、TanStack Start、Astro、Vue/Svelte 以及原生平台仍服务各自场景；比具体 logo 更稳定的是上层技术的共同取向：
可组合、可局部替换；
文档和 schema 对机器可读；
反馈循环短且错误能回到终端；
行为 primitive 与视觉 token 分离；
源码、配置与验证证据都能进入 Git。
TypeScript 7 用原生内核提速
TypeScript 7.0
[136]
已于 2026-07-08 发布。它用 Go 原生重写 compiler，并利用 shared-memory multithreading；微软报告完整构建通常提升 8–12 倍。TypeScript 继续承担应用表达，Go 内核则降低类型检查和工具反馈成本。
这次迁移也留下了兼容窗口：7.0 暂未提供原有 compiler API，新的程序化 API 计划在 7.1；Vue、MDX、Astro、Svelte、Angular 和自定义 transformer 等嵌入式工具链仍可能需要 TypeScript 6。对 Agent 来说，更快的类型检查缩短 observe-edit-check 环路，生态则要逐步迁移既有嵌入契约。
Python 守住生态，uv 重做工具链
uv
[137]
用 Rust 实现单一、预编译的 Python package/project manager，整合 pip、pip-tools、pipx、Poetry、pyenv、virtualenv 等工作流。它负责解释器选择、依赖解析、lockfile、工具安装和启动，Python runtime 与 sandbox 继续由各自边界承接。
长期图景更接近分层共生：Python 继续拥有模型、数据、Notebook、科研和 PyTorch 生态，Rust/C++/CUDA 承担包管理、解析、tokenizer、数据路径与内核。原生工具让 Python 环境更可预测，也更适合 Agent 自动化。
Bun 转 Rust：迁移快了，验证贵了
Bun PR #30412
[138]
于 2026-05-14 合并 “Rewrite Bun in Rust”：约 100 万新增行、2188 个文件，GitHub 页面显示 6755 个 commits。作者称既有测试在各平台通过，binary 缩小 3–8MB，性能持平或更快，架构和数据结构基本不变，也没有采用 async Rust。分支和提交历史显示大量 Claude 辅助工作；更可靠的概括是“由团队与大规模 Agent workflow 共同完成的迁移”，而非一个模型独立完成。
截至研究日，main/canary 已是 Rust-first Cargo workspace，而 GitHub 标记的最新稳定版 v1.3.14 仍是迁移前的 Zig build；JavaScriptCore/C++ 与多个 C 库也继续存在于新的混合实现中。
LLM 大幅降低了机械翻译、批量修复和跨文件迁移成本，同时把瓶颈推向语义验证、unsafe 边界、性能回归和长期维护。合并后社区很快报告了
safe Rust 下的潜在 UB/Miri 问题
[139]
，表明测试通过只覆盖已有验收面，Rust 的完整安全收益还依赖 invariant、sanitizer、Miri、fuzz、review 和灰度发布。未来大型重写会更多，验证成本也会比生成速度更值钱。
终端是系统语言的压力测试场
终端同时承受 PTY、ANSI/VT、Unicode/IME、字体 shaping、GPU 渲染、shell 生命周期、SSH、multiplex、窗口系统和跨平台分发。它在本文承担一种证据角色：把 Rust、Zig 等系统语言放进真实产品的复杂边界，检验微基准以外的工程能力。
窄渲染与可编程宿主
：
Alacritty
[140]
用 Rust + OpenGL 坚持窄而可组合；
kitty
[141]
以 C/Python/Go 分层，并通过
JSON remote-control protocol
[142]
暴露按 action 授权的控制面；
WezTerm
[143]
用 Rust core 持有会话和 I/O，以 Lua 保留配置反馈，同时提供 multiplexer、SSH/domain 与
wezterm cli
[144]
。
可嵌入内核
：
Ghostty
[145]
用 Zig core 配合 macOS、Linux 原生 UI，再通过 C ABI 进入其他宿主。
libghostty-vt
[146]
已把 VT parsing、screen/scrollback state、input encoding 和 formatter 暴露为 C/Zig API，并覆盖 Wasm；Turborepo 的
turborepo-ghostty
[147]
已用它解析和渲染任务输出。
awesome-libghostty
[148]
则记录了正在生长、API 尚在变化的嵌入生态。
终端扩成工作台
：
Warp
[149]
用 Rust client、自研 GPU UI 和
block model
[150]
组织 command/output 与 rich view；
Wave
[151]
选择 Go backend + Electron/React，把 terminal、editor、browser、preview 组合成可拖拽 block，并提供 durable SSH 与
wsh
。
这些路线分别优化显示边界、协议与会话、可嵌入内核和图形工作台。Rust 已从窄渲染器延伸到长期会话、GPU UI 与跨平台产品；kitty 的多语言分层、Ghostty 的 Zig 与 Wave 的 Go/TypeScript 同时表明，清楚的模块边界比语言纯度更有解释力。
Rust 已形成一套 CLI 产品语法
终端 emulator 之上，一整套 Rust 项目又形成了相似的 CLI 产品语法：
Shell 与提示层
：
fish
[152]
4.0 从 C++ 迁到 Rust，目标是在重建实现时保持 Shell 语义；
Starship
[153]
用一个跨 Shell、跨平台 binary 统一 prompt。
搜索与只读观察
：
rg
[154]
缩小搜索范围，
bat
[155]
为文件和管道增加语法/Git 上下文，
eza
[156]
为目录增加 tree、Git、类型和时间等元数据。bat 在非交互输出时退回 plain content，说明现代 CLI 仍要保留 Unix 管道语义。
TUI 与工作区
：
Ratatui
[157]
提供 widget、layout、buffer 和 terminal backend；
Zellij
[158]
组合 pane、session 与插件；
GitUI
[159]
将 staging、diff、log 投影成键盘驱动界面。面向 Agent 时，它们仍需提供 plain output 或结构化协议。
记录与命令知识
：
asciinema
[160]
捕获、播放和流式传输轻量终端事件，并支持 headless 与退出码传播；
navi
[161]
将 cheatsheet、参数建议和可编辑命令接入 shell widget。前者保存事件，后者保存人的操作知识。
这批项目说明 Rust 已经具备一套完整的 CLI 产品化能力：跨平台 native binary、可控启动与内存、终端协议解析、并发 I/O、TUI 组件生态，以及和 stdin/stdout/退出码共存的交互设计。它们也暴露了边界：TUI、颜色、pager 和交互选择器首先服务人类；进入脚本后需要关闭装饰、保留 plain output，并避免把屏幕状态误当成结构化协议；比较、缓存或回放依赖确定性时，还应固定排序。
fish 4.0 的迁移复盘
[162]
尤其值得与 Bun 对照。fish 用约两年把 C++ 实现迁到接近全 Rust，重点是维持成熟 Shell 的既有行为；Bun 则借助大规模 Agent 工作流压缩机械迁移时间。两条路径最终都把成本落在语义兼容、平台细节、验证与长期维护上。
Wasm 只接收显式能力
Rust 官方对 WebAssembly 的定位
[163]
很克制：Rust 提供可预测性能、较小代码体积和低层控制，Wasm 用来增强 JavaScript 的处理密集型或底层任务。组件只能使用宿主显式链接的 imports，因此可移植的是计算与接口，本地文件、网络、PTY、凭据和操作系统环境仍由宿主提供。
Zellij 给出了终端生态中最直接的例子。它的
插件系统
[164]
使用 WebAssembly/WASI，运行命令、写入 stdin、读取 pane、打开文件、访问完整磁盘、拦截输入等动作则由
独立权限表
[165]
控制。Wasm 约束组件边界，用户是否同意某次命令仍由宿主策略判断。
Wasmtime 的安全文档
[166]
同样把边界写得很清楚：core Wasm 隔离线性内存和控制流，对外能力全部来自 imports；filesystem 还要由 WASI capability 授权，内存、table 与实例数量由宿主配置
ResourceLimiter
[167]
约束，CPU 与执行时间则要通过
consume_fuel
或
epoch_interruption
[168]
等机制单独限制。甚至输出到终端的 ANSI/control sequence 都可能触发文件写入、命令执行或输入注入，因此 runtime 还要做过滤。
Rust、Wasm 与宿主形成三层责任：Rust 约束实现，Wasm 约束组件边界，宿主约束权力。
workers-rs
、Zellij plugin 和
libghostty-vt
证明 Rust/Zig 内核可以进入浏览器、边缘和插件宿主；系统环境、业务身份、审批、审计与恢复继续留在宿主控制面。
Zig 的交叉编译、C ABI、显式内存和工具链控制适合小型 runtime、GUI core 和嵌入式边界；Rust 的类型系统、并发生态和内存安全适合长期维护的基础设施；Go 则擅长网络服务、并行工具和单一分发。故障模型、团队能力和生态位置共同决定选择。
原生工具把执行变得更快、更容易分发；接下来的瓶颈是 Agent 如何知道何时调用、按什么顺序调用，以及怎样验证调用结果。Skills 正在把这部分程序性知识从散落文档变成机器可加载的操作包。
九、Skills 将知识变成操作
公司真正需要的标配，是一套面向机器的正式操作面。公开
SKILL.md
仓库是当前最轻的载体之一；拥有复杂 API、开发平台或内部流程的组织，还需要把文档、schema、工具、身份、策略和评测组合起来。
完整的机器操作面至少包含：
Skills 负责“何时、为何、按什么顺序做”的程序性知识；身份、权限和运行时能力分别由相邻层提供。Vercel skills CLI 已支持 Codex、Claude Code、Cursor 等大量 Agent 的 add/use/find/update/remove；Cloudflare 也维护自己的官方 Skills。分发机制已经形成，供应链治理仍处于早期。
find-skills
本身也是一个 Skill
[169]
：当 Agent 发现能力缺口时，它可以搜索 skills.sh、建议安装，再获得新的操作规程，由此形成递归能力获取环：
识别能力缺口
-> 搜索 Skill
-> 评估来源
-> 安装
-> 获得新的发现与执行能力
Skill 安装会改变未来任务的操作规程，风险高于下载普通文档。发现、安装、激活和执行应成为四个独立的权限与审计阶段，全局安装需要显式确认。
Agent Skills specification
[170]
所强调的渐进披露——先目录 metadata，再按需读
SKILL.md
，最后才加载引用和脚本——很适合控制上下文成本。Cloudflare 甚至提出了
.well-known/agent-skills
discovery RFC
[171]
，其草案开始要求 SHA-256 与归档安全检查，并默认不执行脚本。与此同时，Cloudflare Agents 对 Skills 的运行时支持仍明确标为 experimental：格式已经快速扩散，可信执行却远未成熟。
模型吸收通用技巧，组织保留责任
Skills 的数量会增长，价值分布却会分化。稳定、通用、公开、可从大量语料学到的技巧——例如常见 Git 操作、主流框架脚手架、固定格式转换——会逐渐进入模型权重、系统 prompt、内建工具或 Harness 默认策略。它们即使继续以 Skill 存在，也会从稀缺资产退化为兼容层。
长期价值集中在需要持续更新、组织所有权或真实责任的部分：
Skills 的护城河由
procedure + current sources + tools + policy + verifier + recovery + provenance
共同构成。通用 Skill 会被模型和宿主吸收，供应商官方 Skill 会成为随产品版本发布的机器文档，企业内部 Skill 则会成为可审计、可撤销的操作资产。越深入垂直领域，价值越来自新鲜性、所有权和真实权限。
OpenClaw 与 Hermes 已开始把 Skill 当成可变的程序性记忆，并为此补上 proposal、hash、scanner、quarantine、write approval 和 rollback。Agent 可以从成功任务中归纳流程，也可能持久化错误归纳、网页污染或偶然成功；evidence、promotion 与 retirement 决定自改善最终沉淀为组织能力，还是长期污染。
一个可进入企业生产的 Skill 至少应具备：
固定版本、digest 和来源；
owner、review date、兼容矩阵与弃用策略；
所需能力、网络、文件和隐私声明；
可执行脚本的审查与签名；
trigger 和行为 eval；
失败恢复、negative path 和回滚；
变更日志与供应链扫描。
更可能成为标配的是：
“面向机器的官方操作包”会成为 Developer Platform 标配，
SKILL.md
是当前最轻、最易扩散的载体之一，完整生产面还包括身份、能力、策略、评测与恢复。
十、责任边界先标准化
Skills 的核心职责是封装规程。一旦规程开始调用真实工具，问题就会继续外溢到身份、环境、持久执行、动作证据和人工接管。格式可以先扩散，生产系统最终仍要对齐一组比
SKILL.md
更大的责任契约。
开放权重的争论提供了另一张治理剖面。开放权重通常只说明模型参数可获取，训练数据、训练代码、许可证和可复现实验仍可能保持关闭。2026 年 7 月 27 日，
Jensen Huang 以 Hugging Face 安全事件为例
[172]
，主张防守方需要开放权重与闭源模型并存的前沿生态；他称闭源模型阻碍了关键取证，而开放权重模型帮助控制了入侵。该判断来自 Jensen 对事件的公开归因。同日，
NVIDIA 宣布 Open Secure AI Alliance
[173]
，计划通过开放共享模型、工具和研究扩大软件与 Agent 的防守者社区。
Anthropic 对开放权重的正式立场
[174]
呈现了另一侧风险：尚未表现出危险能力的开放权重模型具有公共价值，类别式禁令也无法约束真正的恶意行为者；一旦高能力权重发布，移除 safeguard、私下运行、复制传播与无法撤回会形成持久风险。Anthropic 因此主张对达到足够能力的开放与闭源模型统一执行强制安全测试，同时用芯片管制和打击工业化蒸馏处理更具体的国家安全问题。
双方对攻防收益和开放程度仍有分歧，这组分歧将下一阶段的治理问题推向了能力分级与运行证据。未来的采购和部署问题会更加具体：模型具有什么危险能力，权重与数据来自哪里，在哪种环境运行，获得哪些工具和隐私，发布前经过什么评测，事件发生后还能隔离、更新、替换或撤销什么。开放权重扩大了本地检查、部署和供应商替换空间；闭源服务更容易提供集中更新、滥用监测与访问控制。成熟 Agent 系统更可能在同一策略边界后组合两者。
未来几年的标准化重心将从框架 API 外溢到以下跨框架契约：
Agent-readable surface
：结构化内容、API catalog、Skills discovery；
可调用语义
：MCP、WebMCP、schema 化 action；
独立身份
：每个 Agent/subagent 有可撤销、最小化授权；
环境描述
：版本、文件快照、网络与资源策略可声明；
持久执行
：事件、checkpoint、幂等、暂停和恢复；
动作证据
：receipt、trace、截图、diff、结果 provenance；
人类接管
：在正确时间把可见状态和控制权交还人类；
注意力协议
：统一表达 running、needs-input、blocked、ready，让 CLI、GUI、Pet 与通知投影同一份真相；
效果评测
：不仅测答案，还测副作用、恢复和长期任务。
模型与权重来源
：能力分级、版本与 digest、训练和评测声明、发布条件及事件响应边界。
这些技术会长期以互补关系共存：
协议和平台可以提供这些公共边界，却无法替一个具体业务定义完成、风险和可接受失败。最后一层仍落在人和组织身上。
十一、工程师转向结果责任
开发者的焦虑有现实基础：把清晰需求翻译成样板代码的价值正在快速贬值，工程价值则沿着代码产量向结果责任迁移。
先定义完成，再设计恢复
面对一个 Agent 任务，先回答：
什么证据能证明任务完成？
哪些副作用不可重试？
中断在每一个阶段会怎样？
失败后恢复还是补偿？
人类什么时候必须介入？
Agent 能力越强，安全越要提前进入设计。scoped identity、secret lifecycle、capability、sandbox、IPC、prompt injection、审计和事故恢复，会成为普通应用工程师的日常工作。先把不可重试的副作用、审批绑定、崩溃后的未知状态和补偿路径写清楚，再讨论更高自治。
接口同时服务人和机器
可机器操作的接口需要：
JSON Schema、稳定 ID 和版本化 contract；
幂等键、dry-run、structured error；
明确退出码、游标、artifact manifest；
可恢复状态机和可比较 trace；
让工具既适合人，也适合非交互调用。
这些接口最终仍落在
git
、
rg
、shell、测试、profiler、浏览器 DevTools、网络、数据库与日志上。理解它们的默认行为、失败语义和安全边界，会比记住某个 Agent 框架的类名更长寿。
如果你做上层产品，React/Vite/Tailwind/Base UI 之类的组合值得熟练掌握；更可迁移的能力是组件状态、设计 token、无障碍、响应式布局、浏览器运行时与视觉验证。生成页面解决实现问题，判断页面是否可用仍是产品工程能力。
双栈学习，指标决策
TypeScript 或 Python 能让你快速连接产品和生态；Rust、Go 或 Zig 能帮助你理解 runtime、并发、内存、CLI、FFI 和分发。选择一组深入即可，不需要追逐每一次重写新闻。
在把 TypeScript/Python/Zig 重写成 Rust 之前，先量化：
冷启动和常驻内存；
p95/p99 延迟与吞吐；
安装/分发失败率；
crash、泄漏与安全事故；
跨平台成本；
团队维护与招聘成本。
如果收益只是“技术上更酷”，Agent 只会更快地产生一笔更大的维护债。
守住注意力与责任
长任务越普遍，系统越要区分运行、等待输入、阻塞和完成，并让通知直接落到对应任务、证据和待决事项。CLI、桌面、移动端与 Pet 应投影同一份运行时真相；免打扰、隐私、通知节流和人工接管入口都是状态机的一部分。
人可以离开工作台，责任链仍要保持连续。模型会继续写更多代码、调用更多工具，也会让个人完成以前需要团队才能完成的工作。长期价值将集中在：
谁能把模糊问题变成正确约束；
谁理解业务和用户真正承受的风险；
谁能设计可验证、可恢复的系统；
谁愿意对生产结果负责。
对工程师而言，最稳妥的方向是定义约束、组织证据、判断取舍，并对生产结果负责。
结语：能闭环，才可托付
生成变便宜，可靠性成本随之转移。代码、分支和工具调用越多，身份混用、环境漂移、重复副作用与错误验收就越容易从偶发问题变成长任务的日常问题。本文讨论的项目和技术选型，都在为这个成本转移补基础设施。
模型能力还会继续增长，平台也会把更多环节收进默认路径。平台负责托管状态、沙箱、浏览器、身份和日志，业务负责定义可接受结果、必须阻断的风险，以及失败后的恢复或补偿。Agent 能否被托付，最后取决于系统能否回答四个具体问题：它做了什么，依据是什么，结果是否成立，失败后如何恢复。
固定研究快照
本文在 2026-07-28 固定了主要浮动仓库的 HEAD，包括：
Vercel/Vercel Labs：
turborepo ac6c28f
、
scriptc 20c3a6c
、
vgpu 23b83d2
、
ai-cli 7799606
、
native a7509a7
、
agent-browser 3cc7022
、
json-render 9d3dfc8
、
portless 15ef064
、
skills e173b8c
、
ai c1100c4
、
chat 257a32d
、
sandbox 80d9421
、
streamdown e5deed3
；
Cloudflare：
agents f089c5b
、
skills 30553f8
、
nimbus d14cddd
、
workers-rs 5f2d6c9
、
puppeteer 08707e0
、
playwright 693f8ac
；
开源 Agent：
pi c820aa2
、
pi-chat 9adbd29
、
openclaw 924004d
、
hermes-agent d83e858
；
Agent 框架与目录：
langgraph 30c4d58
、
agent-framework 7b6d257
、
awesome-agents 4ef3577
、
awesome-ai-agents 999f3c3
；
终端与 CLI：
kitty 7ed3477
、
warp a9a3122
、
ghostty 2dd79f3
、
wezterm 76b606e
、
alacritty 852e971
、
ratatui 3d8639c
、
waveterm c99022c
、
ripgrep f9c05a9
、
starship cad50cd
、
bat 7895139
、
fish 790754d
、
zellij ea07e2d
、
eza 471bfbc
、
gitui bc086cf
、
asciinema 3c61095
、
navi 1ac218c
；
其他：
swc b830786
、
bun 4eb6f99
、
uv 9ae6754
、
codex fb6aad9
、
antigravity-cli c691118
、
webmcp 5801678
、
gpuweb d390da5
、
electron d84976d
、
tauri 7164de3
。
固定 SHA 只证明本文观察的代码快照，不证明成熟度、采用率、未来路线或生产稳定性。
References
[1]
awesome-agents:
https://github.com/kyrolabs/awesome-agents
[2]
awesome-ai-agents:
https://github.com/e2b-dev/awesome-ai-agents
[3]
Anthropic 对 Context Engineering 的定义:
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[4]
OpenAI 所说的 Harness Engineering:
https://openai.com/index/harness-engineering/
[5]
Managed Agents 架构:
https://www.anthropic.com/engineering/managed-agents
[6]
Anthropic 的 Claude 5 context engineering 复盘:
https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
[7]
Codex Goal:
https://learn.chatgpt.com/docs/long-running-work
[8]
Codex Subagents 文档:
https://learn.chatgpt.com/docs/agent-configuration/subagents
[9]
OpenAI Agents SDK 的编排模型:
https://openai.github.io/openai-agents-js/guides/multi-agent/
[10]
Claude Code Dynamic Workflows:
https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
[11]
后续迁移复盘:
https://claude.com/blog/ai-code-migration
[12]
AI SDK:
https://github.com/vercel/ai/tree/c1100c45af58ebac9935d2b81354a651100b6e12
[13]
AI SDK 7:
https://vercel.com/blog/ai-sdk-7
[14]
Chat SDK:
https://github.com/vercel/chat/tree/257a32d01c41d51f3ecabb3d25944482c37ad6bc
[15]
Streamdown:
https://github.com/vercel/streamdown/tree/e5deed330aa4231751a106445d93d62e4716a22f
[16]
json-render:
https://github.com/vercel-labs/json-render/tree/9d3dfc8917c1c6aa5568acbe0969523f3307376c
[17]
Vercel Sandbox:
https://github.com/vercel/sandbox/tree/80d9421b4ef3b933b0811d1fa8f54ea67c48db5d
[18]
agent-browser:
https://github.com/vercel-labs/agent-browser/tree/3cc7022271235694b5b5ce8aaea8bbfaa66e8cd5
[19]
portless:
https://github.com/vercel-labs/portless/tree/15ef06434c81523b1b24db2d52a17caf31edecf1
[20]
ai-cli:
https://github.com/vercel-labs/ai-cli/tree/77996062324a3f971192d99681b6e5fa047a2119
[21]
scriptc
20c3a6c
:
https://github.com/vercel-labs/scriptc/blob/20c3a6c27da4807f607ebe496663842b67e87f0e/README.md
[22]
QuickJS-ng:
https://github.com/quickjs-ng/quickjs
[23]
Native SDK:
https://github.com/vercel-labs/native/tree/a7509a7fa6c467eaed021250538b482886f1c6bf
[24]
vgpu:
https://github.com/vercel-labs/vgpu/tree/23b83d27c1a5d5aec6d04a6cf33f0de043d6ae3f
[25]
Turborepo:
https://github.com/vercel/turborepo/tree/ac6c28ff6fe82aaad2ae7f1cae32a6c4d4f094f3
[26]
Vercel 在 2021 年正式收购 Turborepo:
https://vercel.com/blog/vercel-acquires-turborepo
[27]
Turborepo 的 AI 指南:
https://turborepo.dev/docs/guides/ai
[28]
turborepo-ai-agents
:
https://github.com/vercel/turborepo/blob/ac6c28ff6fe82aaad2ae7f1cae32a6c4d4f094f3/crates/turborepo-ai-agents/src/lib.rs
[29]
Go→Rust 迁移:
https://vercel.com/blog/turborepo-migration-go-rust
[30]
原文:
https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans
[31]
SWC:
https://github.com/swc-project/swc/tree/b83078644a7f0f1bbb56d6b45754ca9ed1bafc4b
[32]
Next.js 11.1 公告:
https://nextjs.org/blog/next-11-1
[33]
Next.js Compiler:
https://nextjs.org/docs/architecture/nextjs-compiler
[34]
Grep:
https://vercel.com/blog/vercel-acquires-grep
[35]
Tremor:
https://vercel.com/blog/vercel-acquires-tremor
[36]
v0:
https://v0.app
[37]
NuxtLabs 团队加入 Vercel:
https://vercel.com/blog/nuxtlabs-joins-vercel
[38]
Vercel 宣布收购 Better Auth:
https://vercel.com/blog/vercel-acquires-better-auth
[39]
vercel-labs/skills
:
https://github.com/vercel-labs/skills/tree/e173b8c88f2581cfdaa1b6767c6519a08155790e
[40]
skills.sh:
https://skills.sh/
[41]
skills-lock.json
:
https://github.com/vercel-labs/skills/blob/e173b8c88f2581cfdaa1b6767c6519a08155790e/src/local-lock.ts
[42]
well-known provider:
https://github.com/vercel-labs/skills/blob/e173b8c88f2581cfdaa1b6767c6519a08155790e/src/providers/wellknown.ts
[43]
partner audit:
https://github.com/vercel-labs/skills/blob/e173b8c88f2581cfdaa1b6767c6519a08155790e/src/telemetry.ts
[44]
Skills Night 原文:
https://vercel.com/blog/skills-night-69000-ways-agents-are-getting-smarter
[45]
Cloudflare Agents:
https://github.com/cloudflare/agents/tree/f089c5b6a13f98ad728f9c9cb9d729469b945233
[46]
Agents + Sandbox:
https://developers.cloudflare.com/agents/tools/sandbox/
[47]
Agents with Workflows:
https://developers.cloudflare.com/agents/concepts/workflows/
[48]
Browser Run:
https://blog.cloudflare.com/browser-run-for-ai-agents/
[49]
把底层重建到 Containers:
https://blog.cloudflare.com/browser-run-containers/
[50]
Cloudflare Puppeteer:
https://github.com/cloudflare/puppeteer/tree/08707e0a188f8e1ac9c038bc118be6c56c7e2973
[51]
Playwright fork:
https://github.com/cloudflare/playwright/tree/693f8ac6d9d5ac5a3496184807f8f14708ddde8b
[52]
Cloudflare 已弃用 Sandbox SDK 中的 desktop feature:
https://developers.cloudflare.com/sandbox/guides/2026-deprecation/
[53]
Nimbus:
https://github.com/cloudflare/nimbus/tree/d14cddd7db48277e3b36b11f06a888a9864454ad
[54]
Cloudflare Skills:
https://github.com/cloudflare/skills/tree/30553f89ae1ef1e3c2917cd09d72dac992bb4e9a
[55]
Agent Readiness:
https://blog.cloudflare.com/agent-readiness/
[56]
Code Mode:
https://developers.cloudflare.com/agents/model-context-protocol/codemode/
[57]
workers-rs:
https://github.com/cloudflare/workers-rs/commit/5f2d6c9192377451d43910098738624474196364
[58]
PartyKit:
https://blog.cloudflare.com/cloudflare-acquires-partykit/
[59]
Baselime:
https://blog.cloudflare.com/cloudflare-acquires-baselime-expands-observability-capabilities/
[60]
Outerbase:
https://blog.cloudflare.com/cloudflare-acquires-outerbase-database-dx/
[61]
Replicate:
https://blog.cloudflare.com/why-replicate-joining-cloudflare/
[62]
Human Native:
https://blog.cloudflare.com/human-native-joins-cloudflare/
[63]
Astro:
https://blog.cloudflare.com/astro-joins-cloudflare/
[64]
VoidZero:
https://www.cloudflare.com/press/press-releases/2026/cloudflare-acquires-voidzero-to-build-the-future-of-the-ai-native-web/
[65]
Anthropic 在 2025 年 12 月收购 Bun:
https://www.anthropic.com/news/anthropic-acquires-bun-as-claude-code-reaches-usd1b-milestone
[66]
Vercept 收购:
https://www.anthropic.com/news/acquires-vercept
[67]
宣布收购 Stainless:
https://www.anthropic.com/news/anthropic-acquires-stainless
[68]
Promptfoo 已加入 OpenAI:
https://www.promptfoo.dev/press/
[69]
宣布拟收购 Astral:
https://openai.com/index/openai-to-acquire-astral/
[70]
拟收购 Ona:
https://openai.com/index/openai-to-acquire-ona/
[71]
已经完成的 Sky 收购:
https://openai.com/index/openai-acquires-software-applications-incorporated/
[72]
OpenClaw Foundation:
https://openclaw.ai/blog/introducing-openclaw-foundation
[73]
进入 Linux Foundation 旗下 AAIF:
https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
[74]
Claude Cowork
:
https://claude.com/product/cowork
[75]
Claude Design
:
https://www.anthropic.com/news/claude-design-anthropic-labs
[76]
Claude Design 与 Claude Code 的双向同步:
https://claude.com/blog/claude-design-stays-on-brand-for-daily-work
[77]
Cowork Web/Mobile 公告:
https://claude.com/blog/cowork-web-mobile
[78]
OpenAI 当前说明:
https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
[79]
内置浏览器:
https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app
[80]
Claude Code:
https://www.anthropic.com/news/claude-3-7-sonnet
[81]
Codex CLI:
https://openai.com/index/introducing-upgrades-to-codex/
[82]
Gemini CLI:
https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-cli-open-source-ai-agent/
[83]
Claude Code 的 CLI 参考:
https://docs.anthropic.com/en/docs/claude-code/cli-usage
[84]
Codex:
https://github.com/openai/codex
[85]
Gemini CLI:
https://github.com/google-gemini/gemini-cli
[86]
官方公告:
https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/
[87]
会话还可以从终端导出到 GUI 继续:
https://github.com/google-antigravity/antigravity-cli/blob/c6911187d1db55e4ae1d5fa4b6f40f7af5af7aee/README.md
[88]
Grok Build:
https://x.ai/news/grok-build-cli
[89]
交互式 TUI、headless 脚本模式与 ACP 嵌入:
https://docs.x.ai/build/overview
[90]
Bun:
https://bun.sh/docs
[91]
Codex 的打包脚本:
https://github.com/openai/codex/blob/fb6aad9ae34116128e537696c24e35fe6548e1c2/scripts/codex_package/README.md
[92]
ripgrep FAQ:
https://github.com/BurntSushi/ripgrep/blob/f9c05a949d1a0dc8e16dee28ca9605d38611faeb/FAQ.md
[93]
earendil-works/pi
:
https://github.com/earendil-works/pi/tree/c820aa26fe0907e053e881a957722693fc094c9c
[94]
packages/server
:
https://github.com/earendil-works/pi/tree/c820aa26fe0907e053e881a957722693fc094c9c/packages/server
[95]
pi-chat
:
https://github.com/earendil-works/pi-chat/tree/9adbd29b40ee27ff1decf0fc87cbe180b40924f5
[96]
OpenClaw:
https://github.com/openclaw/openclaw/tree/924004d35c23413ddc2861f1e0a10f069046e61a
[97]
Hermes Agent:
https://github.com/NousResearch/hermes-agent/tree/d83e858507a9bdb7f96c7a163d89c34c60909dcf
[98]
审批绑定实现:
https://github.com/openclaw/openclaw/blob/924004d35c23413ddc2861f1e0a10f069046e61a/src/gateway/node-invoke-system-run-approval.ts
[99]
Agent loop:
https://github.com/NousResearch/hermes-agent/blob/d83e858507a9bdb7f96c7a163d89c34c60909dcf/website/docs/developer-guide/agent-loop.md
[100]
重做 Claude Code Desktop:
https://claude.com/blog/claude-code-desktop-redesign
[101]
/app
:
https://learn.chatgpt.com/docs/developer-commands
#built
-in-slash-commands
[102]
OpenAI 的 Pets 文档:
https://learn.chatgpt.com/docs/pets
[103]
通知文档:
https://learn.chatgpt.com/docs/notifications
#follow
-chat-activity-with-a-pet
[104]
Gemini in Chrome:
https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/
[105]
AI Mode 进入 omnibox:
https://blog.google/products-and-platforms/products/chrome/chrome-reimagined-with-ai/
[106]
Dia:
https://www.diabrowser.com/
[107]
宣布收购 The Browser Company:
https://www.atlassian.com/blog/announcements/atlassian-acquires-the-browser-company
[108]
Dia 已使用 Atlassian identity:
https://www.diabrowser.com/security
[109]
Atlassian 2026 年进一步披露:
https://www.atlassian.com/blog/company-news/founder-update-team-26
[110]
迁移说明:
https://help.openai.com/en/articles/20001371-evolving-atlas-into-chatgpt-for-browser-based-agentic-work
[111]
Chrome DevTools Protocol:
https://chromedevtools.github.io/devtools-protocol/
[112]
WebDriver BiDi:
https://www.w3.org/TR/webdriver-bidi/
[113]
Chrome WebMCP early preview:
https://developer.chrome.com/blog/webmcp-epp
[114]
W3C Web Machine Learning Community Group 草案:
https://github.com/webmachinelearning/webmcp/tree/58016782fa379c25bc9584433f29127a9855647b
[115]
Cloudflare WebMCP:
https://developers.cloudflare.com/browser-run/features/webmcp/
[116]
WebGPU:
https://www.w3.org/TR/webgpu/
[117]
Transformers.js 的 WebGPU 指南:
https://huggingface.co/docs/transformers.js/en/guides/webgpu
[118]
Electron:
https://www.electronjs.org/docs/latest/tutorial/tutorial-prerequisites
[119]
官方进程模型:
https://www.electronjs.org/docs/latest/tutorial/process-model
[120]
WebContentsView:
https://www.electronjs.org/docs/latest/api/web-contents-view
[121]
contextBridge 指南:
https://www.electronjs.org/docs/latest/tutorial/context-isolation
[122]
Tauri:
https://github.com/tauri-apps/tauri/tree/7164de39574d616b762ba658f797f9657ea03b20
[123]
官方进程模型:
https://v2.tauri.app/concept/process-model/
[124]
Capabilities:
https://v2.tauri.app/security/capabilities/
[125]
外部 binary sidecar:
https://v2.tauri.app/develop/sidecar/
[126]
把 Node.js 应用编译为 sidecar:
https://v2.tauri.app/learn/sidecar-nodejs/
[127]
官方产品介绍:
https://openai.com/index/introducing-the-codex-app/
[128]
SSI 宣布与 NVIDIA 建立长期战略合作:
https://x.com/ssi/status/2081732119194394763
[129]
NVIDIA AI Infrastructure:
https://x.com/NVIDIAAIInfra/status/2081736062154740157
[130]
Vite 等 build tool:
https://react.dev/blog/2025/02/14/sunsetting-create-react-app
[131]
Vite 8:
https://vite.dev/blog/announcing-vite8
[132]
Tailwind CSS v4:
https://tailwindcss.com/blog/tailwindcss-v4
[133]
Base UI:
https://base-ui.com/react/overview/about
[134]
shadcn 已把 Base UI 设为新项目默认 primitive:
https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default
[135]
React Aria 纳入一等选项:
https://ui.shadcn.com/docs/changelog/2026-07-react-aria
[136]
TypeScript 7.0:
https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
[137]
uv:
https://github.com/astral-sh/uv/tree/9ae67546b933ec34ae4893f9b4df5f8b43aefca0
[138]
Bun PR
#30412
:
https://github.com/oven-sh/bun/pull/30412
[139]
safe Rust 下的潜在 UB/Miri 问题:
https://github.com/oven-sh/bun/issues/30719
[140]
Alacritty:
https://github.com/alacritty/alacritty/tree/852e971cddfabe222d2d5bcda466e130f53af207
[141]
kitty:
https://github.com/kovidgoyal/kitty/tree/7ed3477d5caad50c06ea5e78777fe82241de3d5f
[142]
JSON remote-control protocol:
https://sw.kovidgoyal.net/kitty/rc_protocol/
[143]
WezTerm:
https://github.com/wezterm/wezterm/tree/76b606ec597a3c0263fa60321548637451c0a547
[144]
wezterm cli
:
https://wezterm.org/cli/cli/index.html
[145]
Ghostty:
https://github.com/ghostty-org/ghostty/tree/2dd79f3bc6af649e68422b08e21ad0300fd8b391
[146]
libghostty-vt:
https://github.com/ghostty-org/ghostty/blob/2dd79f3bc6af649e68422b08e21ad0300fd8b391/include/ghostty/vt.h
[147]
turborepo-ghostty
:
https://github.com/vercel/turborepo/tree/ac6c28ff6fe82aaad2ae7f1cae32a6c4d4f094f3/crates/turborepo-ghostty
[148]
awesome-libghostty:
https://github.com/Uzaaft/awesome-libghostty
[149]
Warp:
https://github.com/warpdotdev/warp/tree/a9a31226f3a04cf315df61aa3b8754593f869bb7
[150]
block model:
https://www.warp.dev/blog/block-model-behind-warps-agentic-development-environment
[151]
Wave:
https://github.com/wavetermdev/waveterm/tree/c99022c15bd1f17273728e728a61743e690d6423
[152]
fish:
https://github.com/fish-shell/fish-shell/tree/790754d12adad72d542fc90886ae2f1689de6610
[153]
Starship:
https://github.com/starship/starship/tree/cad50cd836533f5134b3bb75d21afa39cb024e1e
[154]
rg
:
https://github.com/BurntSushi/ripgrep/tree/f9c05a949d1a0dc8e16dee28ca9605d38611faeb
[155]
bat:
https://github.com/sharkdp/bat/tree/78951393e29bfd2f2a45f4326b9d2bb5e737dd2a
[156]
eza:
https://github.com/eza-community/eza/tree/471bfbc7b03cbac8c738e8d9050edb06ee79132a
[157]
Ratatui:
https://github.com/ratatui/ratatui/tree/3d8639cbb2f910200f30e680a8923ccaf99ba1bf
[158]
Zellij:
https://github.com/zellij-org/zellij/tree/ea07e2d5b6bbc9ea6f9c765b0838b3e91156a58d
[159]
GitUI:
https://github.com/gitui-org/gitui/tree/bc086cf2e5f32cc66627340f8642021c9bf1bc55
[160]
asciinema:
https://github.com/asciinema/asciinema/tree/3c610957c7dbbdfcb362a1cdfc39df4eb21f48ad
[161]
navi:
https://github.com/denisidoro/navi/tree/1ac218cb1e0e80649ef23c8a916e67efc3086833
[162]
fish 4.0 的迁移复盘:
https://fishshell.com/blog/rustport/
[163]
Rust 官方对 WebAssembly 的定位:
https://rust-lang.org/what/wasm/
[164]
插件系统:
https://zellij.dev/documentation/plugins.html
[165]
独立权限表:
https://zellij.dev/documentation/plugin-api-permissions
[166]
Wasmtime 的安全文档:
https://docs.wasmtime.dev/security.html
[167]
ResourceLimiter
:
https://docs.wasmtime.dev/api/wasmtime/trait.ResourceLimiter.html
[168]
consume_fuel
或
epoch_interruption
:
https://docs.wasmtime.dev/api/wasmtime/struct.Config.html
[169]
find-skills
本身也是一个 Skill:
https://github.com/vercel-labs/skills/blob/e173b8c88f2581cfdaa1b6767c6519a08155790e/skills/find-skills/SKILL.md
[170]
Agent Skills specification:
https://agentskills.io/specification
[171]
.well-known/agent-skills
discovery RFC:
https://github.com/cloudflare/agent-skills-discovery-rfc
[172]
Jensen Huang 以 Hugging Face 安全事件为例:
https://x.com/JensenHuang/status/2081698060330250294
[173]
NVIDIA 宣布 Open Secure AI Alliance:
https://x.com/nvidia/status/2081666629264449730
[174]
Anthropic 对开放权重的正式立场:
https://www.anthropic.com/news/position-open-weights-models

---

标签： #主题/AI-Agent #主题/Harness工程 #主题/Agent基础设施 #主题/Agent-Skills #主题/浏览器自动化 #主题/可信执行 #场景/公众号长文 #作者/lencx
