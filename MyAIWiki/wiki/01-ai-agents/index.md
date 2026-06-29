# AI Agents Wiki

## 核心概念

- [[agent-architecture]] - 代理架构设计
- [[tool-use]] - 工具调用机制
- [[memory-systems]] - 记忆系统
- [[workflow-vs-agent]] - Workflow 与 Agent 的区别
- [[harness-engineering]] - Harness Engineering 工程化落地指南 ⭐
- [[Harness工程AgentLoop]] - Agent Loop 从Demo到工业级：20行伪代码+5大工程决策+4大失效场景 ⭐
- [[HarnessEngineering企业级实战]] - 阿里实战：从25%到90% AI代码率，10阶段Pipeline + 四要素架构 ⭐
- [[0xCodez-Agent-Harness-14-Steps]] - X 长文 0xCodez 14 步路线图：Harness 是 Loop 地基 + 3 段 14 步 + 8 反模式 check list + 对 Seetong 5 个优先动作 ⭐⭐
- [[agent-architectures]] - Agent 架构模式（ReAct/Plan-and-Execute）⭐
- [[deep-research-stack]] - Deep Research Stack：开源深度研究方案 ⭐
- [[吴恩达提示词课-协作原则]] - AI协作核心原则：从"控制"变"一起想" ⭐

## 关键论文

- [[Skills驱动推理新范式]] - TRS：用技能卡片降低推理 Token 成本 ⭐
- [[Skill-Self-Evolution]] - 阿里妹飞樰 2026-06-09 深度综述：Agent Skill 自进化三大学派（Trace2Skill 归纳法 / EvoSkill 自验证 / SkillOpt 训练范式）+ 可验证性=飞轮 + Skill 即参数；与 [[买了一样的AI为什么别家的比你的强]] [[Agent Skills 系统性综述]] [[从Prompt-Context到Harness-工程的三次进化与终局之战]] 强关联 ⭐⭐⭐
- [[Skill-Self-Evolution-digest]] - 上一篇的速读摘要版
- [[react-paper]] - ReAct: 推理+行动
- [[autogpt-analysis]] - AutoGPT 深度分析
- [[openclaw-analysis]] - OpenClaw 分析

## 记忆系统专题

- [[记忆是-agent-基建]] - 记忆是 Agent 基建（对话 Calvin@Vida）⭐
- [[llm-agent-unified-memory-framework]] - LLM Agent 统一记忆框架综述 ⭐
- [[ai-personal-knowledge-base-problems]] - AI 个人知识库：为什么还是那么难用 ⭐

## 核心案例

- [[good-ai-pm-bad-ai-pm|Good AI PM / Bad AI PM：AI 时代，PM 藏不住了]] - AI 压缩协调成本后，真正稀缺的是客户洞察与判断力 ⭐ - 2026-05-13
- [[Agent时代架构师系统能力]] - 筛选/上下文分层/工具契约/评估/Harness/状态管理 ⭐ - 2026-05
- [[agent-era-productivity-paradox|Agent时代的生产力悖论]] - 阿里AoneCopilot：为什么换AI工具不改变研发效率？协作模式变革 ⭐ - 2026-05-08
- [[HarnessEngineering企业级实战]] - 阿里实战：从25%到90% AI代码率，10阶段Pipeline + 四要素架构 ⭐
- [[openclaw-shi-yong-an-li-ji-qiao|OpenClaw使用案例与技巧]] - 写作助理/Review/主动推送等实际场景 ⭐ - 2026-05-10
- [[garry-tan-ai-second-brain|Garry Tan的AI第二大脑]] - 薄路由/厚技能/厚数据，复利型AI系统 ⭐ - 2026-05-10
- [[OpenClaw-vs-Hermes-多-Agent-架构设计]] - 从会话边界 vs 进程边界理解多 Agent 架构差异
- [[OpenClaw-vs-Hermes-多-Agent-架构设计-digest]] - 上一篇的速读摘要版
- [[从零设计生产级-Multi-Agent-Harness]] - 从编排、工具治理、记忆、评估、预算到 MCP 接入的全景拆解
- [[从零设计生产级-Multi-Agent-Harness-digest]] - 上一篇的速读摘要版
- [[make-for-agent-qi-shi-huan-shi-make-for-human|Make for Agent，其实还是 Make for Human]] - Agent 产品设计的核心不是界面，而是责任链、身份与上下文基础设施 ⭐ - 2026-05-27
- [[AI-PM核心技能-观测评估与反馈闭环]] - AI PM 的新门槛：反馈源、Trace、Eval 与产品学习闭环 ⭐ - 2026-05-31

- [[AI时代给人类留了最后一份工作-是农民]] - AMC 与 Context Farmer：人类最后的工作 ⭐
- [[agent-principles-architecture-engineering]] - Agent 原理、架构与工程实践 ⭐

## AI Native 组织专题

- [[Multica-AI-Native-组织-人是最慢的节点]] - 腾讯研究院 2026-06-11 张佳圆（Multica 创始人）访谈：4 人 + 几十 Agent 的极端样本 + "人是组织瓶颈，不是 Agent" + 三类角色（Orchestrator/Worker/Validator）+ 最多两层 + 去中间层 + 端到端负责 + Agent idle 率 + 网络效应壁垒 + 思考退化对抗；与 [[Claude-Code一周年回顾-Boris-Cat]] [[OpenClaw-vs-Hermes-多-Agent-架构设计]] [[从零设计生产级-Multi-Agent-Harness]] [[make-for-agent-qi-shi-huan-shi-make-for-human]] [[AI-Coding的顿悟时刻]] [[54万行代码的顿悟]] [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]] [[AI-PM核心技能-观测评估与反馈闭环]] 强关联 ⭐⭐⭐
- [[Multica-AI-Native-组织-人是最慢的节点-digest]] - 上一篇的速读摘要版

## 业务需求 Agent 落地专题

- [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] - 阿里妹 2026-06-15 森叶：业务需求专家 Agent 的 4 层横向架构（上下文输入 / 业务专家编排 / 工具执行 / 反馈学习）+ 8 步纵向流程（需求进入→澄清→方案→实现→CR 协同→验收→发布→结项）+ 3 个关键设计（不直接升级 / 质量门禁硬规则化 / 反馈留痕到平台）+ 3 大现有问题（接入成本 / 效果度量 / 单 Agent→Team）；与 [[APPSO-Codex-Claude-Code-Loop-Engineering]] [[Addy-Osmani-Loop-Engineering]] [[Loop-Engineering-详解-把反馈循环放进工程现场]] [[Addy-Osmani-agent-skills-设计哲学]] [[Multica-AI-Native-组织-人是最慢的节点]] 强关联 ⭐⭐⭐
- [[阿里妹-端到端业务需求专家Agent-4层架构8步流程-digest]] - 上一篇的速读摘要版
- [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] - 陈进/腾讯云开发者 2026-06-16：Agent Loop 范式跃迁 + 8 个真痛点没标准答案（软目标停止 / Maker-Checker 同病 / 护栏分层 / 记忆失焦 / 理解力腐蚀 / 拓扑选型 / AI 胡说 / 多 Agent 成本）+ SELF Protocol 治理薄壳草稿（~1500 行 Python + Markdown 约定 / Knot Skill 33837 v1.6.7 / 30 天单 Agent 单样本 / 拦下编造 1 次 / 4 档入口）⭐⭐⭐
- [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题-digest]] - 上一篇的速读摘要版

## Harness 工程实战专题(高风险生产场景)

- [[阿里云开发者-淘宝主播Agent的Harness工程实战]] - 阿里云开发者/阿里妹 2026-06-17：**Harness 从"个人助手"推到"淘宝直播"高风险生产场景的工程骨架**（操作不可撤回 + 主播注意力稀缺 + 多话题高频交织 + 长程可中断）；**业务/框架彻底分层**（业务方写 Skill,框架兜底）+ **物理存储分治**（MySQL 会话/ Hologres 记忆/ GitLab Skill）+ **纵深防御 5 层**（Prompt→Schema→Approval→验证→审计）+ **记忆对账信任度闭环**（L1 主观/ L2 事实/ L3 行为 + 矛盾累积 ≥ 3 次才覆盖 + trust 非对称更新 +0.05/-0.10/-0.05/+0.03 + trust 决定输出形态 ≥0.7 recommend/0.4-0.7 弱参考/<0.4 仅 evidence）；**Harness 六元组** (E, T, C, S, L, V) + **Reducer 上下文模式** + **工具三件套**（边界+Schema+幂等,写操作必带 UUID 幂等键防"双切品/双改价"）+ **结构化错误码 3xxx/4xxx/5xxx/9xxx** + **Hook 5 时机**（PreReasoning/PreToolCall/PostToolCall/PostReasoning/SessionEnd）+ **Approval 4 档**（auto/soft-gate/hard-gate/block）+ **DAG 替代 ReAct**（PlanEngine 成功率 0.847 vs 0.737, 子任务覆盖率 0.976 vs 0.883, 工具执行冗余率 0.587 vs 0.727, 迭代轮次 5.440 vs 8.020）；**8 节点 + 5 个对 Seetong 借鉴动作**（六元组体检/业务框架分层重写 Skill 库/记忆三层对账用到简报/Approval 4 档作为操作硬规则/写 Seetong PlanEngine 7 天小试点）；与 [[Harness工程AgentLoop]] [[HarnessEngineering企业级实战]] [[0xCodez-Agent-Harness-14-Steps]] [[harness-engineering]] [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] [[腾讯-AI-Agent-Skill-测评方案落地]] 强关联 ⭐⭐
- [[阿里云开发者-淘宝主播Agent的Harness工程实战-digest]] - 上一篇的速读摘要版

## Loop 主题专题(补完:验证才是瓶颈)

- [[Loop-Engineering-验证才是瓶颈]] - 深思 SenseAI 2026-06-17 翻译/编译自 Samuel McDonnell(@samueljmcd) 英文原文《My Thoughts on Loop Engineering》：**Loop 工程的真正瓶颈不是生成器(编排),而是验证器(闸门)**;**一个 loop = 生成器 + 验证器,瓶颈从来在验证器一侧**;**开放循环易变废料机 / 今天真正出活的是带评估闸门的封闭循环**;**"那个框(验证),才是产品,其余的都是管道"**;**内循环成熟(任务内:改→测→修→全绿,大多数 agent 都会) / 外循环还半残**(跨会话 SKILL.md/AGENTS.md 持久化教训只搭了一半,大量价值正摊在桌子上没人捡);**"先仪表化闸门再去扩大循环"**(无法改进一个没在测量的循环);**Bun 75 万行 Zig→Rust 移植案例**(Jarred Sumner 2026-06:11 天合并/99.8% 测试/Anthropic 自家公告附注"未上生产" = "整个发布里最诚实的一句话");**"产出的质量被验证器的质量封顶,一分都高不上去"**(99.8% 跑分 ≠ 生产正确);**降维边界**(写作/策略/设计/品味验证者无法降维成自动闸门,"你以为在搭循环,其实只是把'自己看一眼'换了名字");深思圈**补刀**(外循环的"教训持久化"判断哪条对也是验证问题,一条错的教训会毒化之后每次运行);**"别再设计提示词,去设计验证者"**;**8 节点 + 5 个对 Seetong 借鉴动作**(5 步 SOP 加评估闸门层 / Bun 案例思维实验 Seetong 代码移植 3 层 agent / 先仪表化再去扩循环作为前置条件 / 拆 Seetong 哪些任务"有验证器"vs"没验证器" / 写"Seetong 外循环持久化教训"原则 + 教训准入 Gate);**本文是现有 Loop 主线 3 篇(Addy-Osmani / Loop-Engineering-详解 / APPSO)偏编排的"补完篇"——本文讲验证**,与 [[Harness工程AgentLoop]] [[HarnessEngineering企业级实战]] [[0xCodez-Agent-Harness-14-Steps]] [[阿里云开发者-淘宝主播Agent的Harness工程实战]] 形成"**Harness=骨架 / Loop=循环 / 闸门=验证**"完整主线三角;与 [[腾讯-AI-Agent-Skill-测评方案落地]] "测评是 Demo→生产必须跨过的门槛"同主线;与 [[Skill-Self-Evolution]] "外循环的持久化教训"与 EvoSkill/SkillOpt 三大学派直接对话;与 [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] [[Claude-Code一周年回顾-Boris-Cat]] [[Claude-Code首席设计师Meaghan-Choi工作流]] 强关联 ⭐⭐
- [[Loop-Engineering-验证才是瓶颈-digest]] - 上一篇的速读摘要版

## Loop 主题专题(补完:大众教育版)

- [[530万人-自循环-提示词]] - 深思圈 2026-06-22 编译/解读自 Anatoli Kopadze(@AnatoliKopadze) 英文爆款《Loops explained: Claude, GPT, Mira and what actually works》（**X 平台 530 万浏览**）：**530 万浏览讲清一件事——大多数人用 AI 还是手动循环（"你就是那台引擎"）；真循环 = 五步（发现→计划→做→验证→决定）+ 三关键（验证是心脏 / 状态是学习 / 停止条件不烧账户）**；**"验证是心脏"**——没真检查 = 看 AI 反复同意自己("干活的那个模型给自己打分时太仁慈了")；**四条门槛**判断要不要上重型循环(任务每周重复 / 有自动判错 / 端到端能自己干 / 完成客观非品味,少一条就用手动提示词)；**可粘贴的自检循环提示词模板**(目标+3条严标准+循环协议+8分门槛+每轮先修最弱项+**你只是触发器**——关掉标签页它就没了)；**Mira 案例**——Telegram 内无代码 agent,接 500+ app,跨会话长期记忆,模型无关(GPT/Claude/Gemini 按任务切),**"ChatGPT 回答,Mira 动手"**——让 agent 把邮件发出去,不是写邮件；**深思圈两个关键提醒**①530 万爆款 = 病毒发布 playbook(巨大承诺+免费赠品+CTA,深思圈评价"这套打法跑通了")②**大众版"无闸门 agent"风险**——工程师版强调"验证器+急停开关",Mira 把刹车悄悄拿掉只剩油门,递给不会设 gate 的普通用户；**8 节点 + 5 个对 Seetong 借鉴动作**(提示词模板入 Seetong Prompt 库 / 四条门槛做 Loop 候选评估 checklist / "验证是心脏"补 Seetong Skill 的 Validation Gate / cron run ack timeout = "无停止条件" 加 maxRunningMs+onTimeout 双闸门 / 警惕 Mira 类"无闸门 agent" Seetong 默认 Approval=hard-gate)；**Loop 主题第 6 视角"大众教育版"**——补完现有 5 篇(Addy-Osmani / 若飞详解 / APPSO / 陈进 / Samuel McDonnell)偏工程师视角,本文把循环讲给普通人听;**与 [[Loop-Engineering-验证才是瓶颈]] 核心互补**——本文 prompt-level("对标准 1-10 分"),Samuel 那篇 system-level("评估闸门才是产品,其余的都是管道"),同一硬币的正反面 ⭐⭐⭐
- [[530万人-自循环-提示词-digest]] - 上一篇的速读摘要版

## Loop 主题专题(补完:团队协作/组织治理)

- [[AI-团队协作-Loop-SDD]] - 叶小钗 2026-06-22：**"个人提效 ≠ 团队提效"核心命题**；**Loop Engineering 最大的问题是"只说结果，不说前提"**——隐藏三个前提：①**Skill 从哪来**（谁来写/评审/更新）②**谁做最终验证**（Addy 承认"验证在你身上"但几十个 Loop 并行时人类审阅带宽怎么跟上）③**Token 成本谁买单**（总 token 消耗是手动 Prompt 的 3-8 倍）；**金句**："方向正确和实现简单之间，隔着大量的工程细节，每个细节都能让你在错误的方向上耗几个月"；**组织级补丁是 SDD（Spec-Driven Development）**——不是"先写文档让 AI 写代码"那么粗暴，是构建"共享上下文/规则/边界/验收标准"的方法论；**Spec 三核心角色** = ①上下文 ②协作契约（避免"产品说一套/研发理解一套/AI 生成一套/测试验另一套"）③质量基准；**vs TDD/BDD**：TDD 偏实现/BDD 偏场景/SDD 偏上游；**六段式 Spec 骨架** = 目标→范围→约束→决策→任务→验收；**SDD 三层次** = Spec First（规格先行，起手式）/ Spec-Anchored（规格锚定，长期资产）/ Spec as Source（规格即源码，终极形态）；**任务复杂度 3 分级** = 小改动 Prompt / 中等需求 轻量规格 / 大型任务 完整规格（避免"所有需求都套完整规格 → AI 提效变文档负担"）；**SDD 落地四步路径** = ①选高价值场景切入点（新模块/遗留迁移/外部接入）②定义轻量 Spec 模板 ③建立项目级上下文（架构约束/目录规范/接口规范/权限模型/状态机/错误码/数据字典）④把 Spec 纳入研发流程明确人工卡点；**AI 进入组织 4 层爬坡** = 个人工具→流程标准→组织协作→评价体系（上一层问题解决后会把下一层问题推出来），关键判断：这些问题不是 AI 带来的，组织原本就存在——只是过去被低效率掩盖；**8 节点 + 5 个对 Seetong 借鉴动作**（SDD 入 TAPD PRD 模板/客服反馈→Spec 链路入 Seetong Bug Triage/项目级上下文建 Seetong 项目知识库/Spec 6 段式入 Seetong Bug 描述模板/AI 进入组织 4 层爬坡做 Seetong AI 落地 roadmap）；**Loop 主题第 7 视角"团队协作/组织治理"**——补完现有 6 篇(Addy-Osmani / 若飞详解 / APPSO / 陈进 / Samuel McDonnell / Anatoli深思圈)偏单人/偏工程师视角的"组织落地"维度；**与 [[Multica-AI-Native-组织-人是最慢的节点]] 镜像**——本文"个人提效 ≠ 团队提效" vs Multica"人是组织瓶颈不是 Agent"；**与 [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] 强关联**——本文 SDD "规格+边界+验收" ≈ 那篇 3 关键设计"不直接升级/质量门禁硬规则化/反馈留痕到平台" ⭐⭐⭐
- [[AI-团队协作-Loop-SDD-digest]] - 上一篇的速读摘要版

## Harness 工程实战专题(数仓场景补完)

- [[Hermes-Agent重构得物数仓工作流]] - 得物技术(小诘、博温)2026-06-17:**数仓埋点承接最消耗的不是"生成 SQL"而是"把分散信息重新拼起来"**;得物选 **Hermes Agent 而非 OpenClaw** 重构数仓工作流(核心 4 项原生能力:**分层持久记忆 SQLite+FTS5 + 技能自动沉淀 + 多平台统一网关 + 工具与扩展生态 MCP**);**4 个工程构件**(工作区独立空间 + 看板状态机进入→设计→预演→评审→交付每步责任人 + 规则+长期记忆"老同学才知道"沉淀可执行检查清单 + 结构化工具接口+预演+人工确认点);**4 类资产化能力底座**(规则包答判断 / 工作区答依据 / 看板答卡 / 结构化接口答验证);**上线前 3 道门**(事实源门/预演门/责任门,**任何缺证据 Hermes 只能停在候选/待确认状态,不能继续生产写入**);**能力边界划分**——**Hermes 是"流程编排者"不是"埋点生成器"**,Hermes 做"判断前工程化准备"(材料/历史/候选方案/系统预演/风险证据),**人聚焦口径裁决 + 生产放行**;**单 Agent 编排 + 多能力模块**(固化 5 项流程契约:输入/动作边界/输出产物/失败处理/经验回写);**规模化落地路径**——用 4 个量化指标(准备时间/交付周期/评审通过率/返工原因)对齐看板/日志/确认记录;**8 节点 + 5 个对 Seetong 借鉴动作**(Seetong 需求承接 4 工程构件 TAPD 端到端试点/3 道门建 Seetong 自动化 SOP/4 资产化能力底座重写 Seetong Skill 库/能力边界划 Seetong AI 助手定位 AI 做判断前准备/人做真判断/4 量化指标评估 Seetong 自动化效果);与 [[阿里云开发者-淘宝主播Agent的Harness工程实战]] [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] Harness 主题互补(主播=实时交互高风险/得物=承接流程标准化);与 [[Skill-Self-Evolution]] [[用 LLM Agent 重构告警排查流程]] [[Claude Code Harness 工程:数仓侧落地方案]] 同作者团队 Skill 主线;与 [[Loop-Engineering-验证才是瓶颈]] 互补(本文"3 道门"硬证据 vs 那篇 Loop 验证闸门);与 [[腾讯-AI-Agent-Skill-测评方案落地]] "测评是 Demo→生产必须跨过的门槛"同主线;与 [[阿里云开发者-淘宝主播Agent的Harness工程实战]] 5 层纵深防御 + 记忆对账信任度闭环风险治理同主线 ⭐⭐
- [[Hermes-Agent重构得物数仓工作流-digest]] - 上一篇的速读摘要版

## 自进化 AI 与 FDE 专题

- [[清华沈阳-自进化AI新物种]] - 新智元 2026-06-15 对话清华沈阳：自进化 AI 5 条产品线（ZeeLin 框架 / AutoResearch / Story / 元相 / Knover）+ 三个原创概念（不可解释但可验证 / Token 稀缺性拟生命 / 智能形态维度差）+ FDE 组织进化协议 30%–50% 岗位重构空间；与 [[Skill-Self-Evolution]] [[Harness-Engineering-企业级实战]] [[OpenClaw-使用案例与技巧]] [[Agent-时代-架构师系统能力]] 强关联 ⭐⭐⭐
- [清华沈阳 - Digest](../../raw/2026-06-15-清华沈阳-自进化AI新物种-digest.md) - 上一篇的速读摘要版（7 角度 + 21 钩子）

- [[腾讯-AI-Agent-Skill-测评方案落地]] - 腾讯程序员 2026-06-17(TEG 云架构平台部网关测试团队 martinskxu):**"测评是 Agent 从 Demo 可用走向生产可靠必须跨过的门槛"**——Agent 三大独有痛点(非确定性/黑盒化/错误级联放大)+ **3 类评分器**(确定性 > Rubric > 人工;"能用代码判断的绝不用模型")+ **5 大评测维度**(功能正确性/过程质量/效率成本/鲁棒性安全/体验对齐)+ **3 类 Agent 侧重**(知识库问答/功能工具/Skill)+ **5 步闭环 SOP**(设计→评分→基线→执行→维护)+ **用例基线 Baseline**(1 次人工确认的预期快照)+ **负向触发用例**("过度触发比不触发难发现"反直觉)+ **多轮稳定性评估**(N 次 1 次不通过即标风险);**落地项目 TPerf 性能平台智能分析 Agent** 已在生产跑通;**8 个独立知识节点**;与 [[Skill-Self-Evolution]] [[陈进-读完Agent-Loop工程手册]] [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] **上游强关联**,与 [[用Agent评测思路管理AI-Coding-31万行代码AI重构实践]] [[如何构建一个更"好"的知识库：RAGAS 三维度评估 + 8 步构建流程 + 前沿架构选型]] [[seetong-batch-issue-rootcause-analysis]] [[seetong-daily-briefing]] **下游强关联**;**5 个对 Seetong 借鉴动作**(建"Seetong Agent 评测集"/Trace 输出作为 Skill 设计标准能力/"过度触发比不触发难发现"作为新 Skill 设计硬规则/5 步闭环作为 Seetong 内部 Agent SOP/TPerf 项目作为基准参考);**这是 01-ai-agents 在 2026-06 第一个完整的"评测工程实践"落地参考** ⭐⭐⭐
- [[腾讯-AI-Agent-Skill-测评方案落地-digest]] - 上一篇的速读摘要版(1 句话 + 4 金句 + 5 反直觉 + 5 Seetong 借鉴动作 + 关联指针)

## 行业落地案例

- [一个农民，用 Codex 管理了 1500 亩地](./cases/farmer-Codex-1500-mu.md) - AI小范儿 2026-06-08 转载自 OpenAI 官方案例：北海道农民 Hiroki Tomiyasu 用 Codex 改造 4 个工作流 + "ChatGPT 学习 + Codex 落地" 普通人 AI 路径 + 工具低估反思
- [一个农民 - Digest](./cases/farmer-Codex-1500-mu-digest.md) - 上一篇的速读摘要版
- 完整案例列表：[./cases/index.md](./cases/index.md)

## 相关标签

#主题/AI-Agent
- [深度解析 LLM Wiki / Obsidian-Wiki / GBrain：Agent 时代知识的”自组织”与”自进化”](./deep-analysis-llm-wiki-obsidian-wiki-gbrain.md)
- [[hermes-obsidian-llm-wiki-knowledge-base]] - Hermes+Obsidian+LLM Wiki 本地知识库：三个工具协作自动化 ⭐ - 2026-05-14
- [[hermes-agent-masterclass]] - Hermes Agent Masterclass：Akshay 深度教程，90K stars 的技术细节 ⭐ - 2026-05-14
