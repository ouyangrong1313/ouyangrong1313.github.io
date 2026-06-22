# AI Coding

## 主题说明

AI 辅助编程的实战经验、提示词模板、工作流总结。

## 核心资源

### Skills 命令
- [[skills]] - Skills 命令手册（/compile /lint /summary /weekly）⭐

### 提示词模板
- [[prompt-engineering]] - Prompt Engineering 指南 ⭐
- [[prompts/function-implementation]] - 功能实现提示词
- [[prompts/code-review]] - 代码审查提示词
- [[prompts/refactoring]] - 重构提示词
- [[prompts/bug-fix]] - Bug 排查提示词

### 工作流模板
- [[workflows/full-feature]] - 完整功能开发流程
- [[workflows/debugging]] - 调试排查流程
- [[workflows/code-migration]] - 代码迁移流程
- [[Codex配置原则总览]] - 当前 Codex 配置的总入口与阅读顺序 ⭐
- [[MyAIWiki写入规范与验证模板]] - 正式知识落盘路径、最小文件集合与验证模板 ⭐
- [[知识卡片编译模板-长文如何压成raw-digest-wiki三层]] - 长文进入知识库时的三层卡片化模板 ⭐
- [[任务类型到验证模板]] - 给知识库、文档、脚本、代码、配置任务定义最小 verifier ⭐
- [[Codex任务交接与new模板]] - 任务结束后如何写交接摘要并安全切到 `/new` ⭐
- [[Codex长期线程设计草案]] - 为高频长任务定义固定线程容器与 stop condition ⭐
- [[Codex工具入口与能力边界]] - 给 shell / webfetch / playwright / MCP / GUI 明确适用面和边界 ⭐
- [[多Agent使用边界与并行判定]] - 定义什么时候该单 agent，什么时候值得并行 ⭐

### 实战案例
- [[ClaudeCode用到这个程度-我算是开眼了]] - 自动编译草稿：Claude Code 用到这个程度，我算是开眼了
- [[我用Codex做研究后-总结出6条有用经验]] - 自动编译草稿：我用 Codex 做研究后，总结出 6 条有用经验
- [[Codex「自我蒸馏」提示词进化版-官方团队给出更强方案-一键打包你的专属工作流]] - 自动编译草稿：Codex「自我蒸馏」提示词进化版
- [[vibe-coding]] - Vibe Coding：用 AI 写代码的正确姿势 ⭐
- [[oh-my-codex]] - oh-my-codex：让 Codex CLI 拥有 30 个专家团队 ⭐
- [[来自Codex官方团队的分享-如何把Codex用到极致]] - 用 durable threads / tools / automations / goals / shared memory 搭完整 Codex 工作台 ⭐
- [[Codex配置下一步改造-从规则层走向线程工具目标与共享记忆]] - 下一阶段优先补线程、工具面、目标模板和共享记忆 ⭐
- [[Codex配置优化清单-从Harness视角]] - 从 AGENTS、skills、知识库和验证闭环四层重构 Codex 配置 ⭐
- [[cases/ai-customer-service]] - AI 客服实战
- [[cat-wu-interview]] - Cat Wu 访谈：AI时代PM的唯一护城河 ⭐
- [[ai给自己出题]] - 聪明人用AI做的，是给自己出题
- [[谷歌开源agent-skills]] - 谷歌 Agent Skills：23000+ Stars 的 AI 编程纪律包 ⭐
- [[你在用AI-AI也在悄悄引导你的选择]] - Linear CEO：AI 编程六个月的真实观察 ⭐
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - Claude Code 架构深度解读 ⭐
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] - 用 Prompt / Context / Harness 三层框架理解 AI 工程演进 ⭐
- [[用Agent评测思路管理AI-Coding-31万行代码重构实践]] - 用Agent评测思路管理AI Coding：31万行代码重构实践 ⭐
- [[吴恩达AI提示词课]] - 吴恩达 AI Prompting 课程精华：三层搜索模型、Sycophancy 对抗 ⭐
- [[软件工程的功底是智能时代生死攸关的要素]] - AI 时代软件工程基本功的系统性提醒：复杂性、技术债、理解债与工程治理
- [[Claude-Code首席设计师Meaghan-Choi工作流]] - loonggg 2026-06-09 编译自 Anthropic Claude Code 首席设计师 Meaghan Choi 演示:worktree 并行 + AI 自决给理由 + 全链路自动化 + 定时巡逻产品质量 + Opus+1M+auto+loop,"能自动化的全自动化,人只在判断环节介入"
- [[Claude-Code一周年回顾-Boris-Cat]] - BorisNCat 2026-06-09 编译自 Boris Cherny + Cat Wu 一周年回顾:Agent 自主验证 + Routine 异步化 + Auto Mode 反直觉安全(Sonnet 4.6 分类器)+ 两次认知跃迁 + 一半工作在手机上 + Context 极简主义 + 2026/3/31 源码泄露风波(51.2 万行 / KAIROS / Undercover Mode)+ 一年 9 个功能里程碑 ⭐⭐⭐
- [[为什么说React是比HTML更合适的AI设计稿格式]] - 宝玉 2026-06-08：React 的组件化、树形结构、数据驱动、文本化交付，比巨大 HTML 更适合 AI 时代的设计稿协作 ⭐
- [[买了一样的AI为什么别家的比你的强]] - Hiten Shah 2026-06-06：模型是商品，skill 才是资产——AI 公司的竞争优势来自把"最厉害的人的判断"打包成可被 agent 复用的 skill ⭐⭐
- [[Anthropic万字长文三个判断和一个阳谋]] - 快刀青衣 2026-06-07：拆解 Anthropic《When AI builds itself》— 执行力零价格 + 验收能力 + 慢变量安全垫 + 巴鲁克计划阳谋 ⭐⭐⭐
- [[Claude-Code之父品味不是人类护城河]] - 机器之心 2026-06-07：编译自 Boris Cherny 访谈 — Claude Code 起源 / 编程=AI Safety 实验场 / "我的工作已经变成写 Loops" / Generalist 黄金时代 / MTS 文化 / 少招人多给 tokens / 价值观护城河 ⭐⭐⭐
- [[problem-first把方案翻转回问题]] - 深思圈 2026-06-07：编译自 George @nurijanian 69.8K 浏览 — 每个"需要做 XX" = 没被说清的问题压缩版 / 8 个部分 90 秒 / 三个替代框架 / 假设挑战带验证 / 50 个想法 90% 死于证据状态 / 协议优于提示词 ⭐⭐⭐
- [[软件工程的功底是智能时代生死攸关的要素-digest]] - 上一篇的速读摘要版
- [[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]] - 把软件工程基本功映射到 Agent / Skill / 知识库 / 验证闭环的实践理解
- [[Codex才是最适合普通人的顶级牛马-Agent]] - 从聊天框到 Agent 工作台：项目目录、Skill、Computer Use 与多线程调度
- [[Codex才是最适合普通人的顶级牛马-Agent-digest]] - 上一篇的速读摘要版
- [[大家都在说软件工厂-但90的CEO不知道自己公司在第几级]] - Alex Lieberman 的软件工厂五级阶梯（Level 0-4）与自测 6 问，分水岭是"拿走 AI 工具后流程会不会崩" ⭐
- [[大家都在说软件工厂-但90的CEO不知道自己公司在第几级-digest]] - 上一篇的速读摘要版
- [[54万行代码的顿悟-Markdown才是新编程方式]] - Garry Tan 的"代码/模型经济方程反转 + Markdown 是新编程方式 + Skillify 循环 + Tokenmaxxing"，与 [[Claude-Code负责人谈AI原生工程组织]] 互为镜像 ⭐
- [[54万行代码的顿悟-Markdown才是新编程方式-digest]] - 上一篇的速读摘要版
- [[AI-Coding的顿悟时刻]] - 工厂模式半年标配 + Spec→LDD 流水线 + Scrum 失效论 + 未来瓶颈=需求定义+架构设计 + 4%成本换100%产出+组织向两端收缩，与 [[54万行代码的顿悟]] 互为镜像（团队流程+组织重构 vs 工程师个人范式） ⭐
- [[AI-Coding的顿悟时刻-digest]] - 上一篇的速读摘要版
- [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]] - Pete Koomen + Gary (Garry Tan) 对谈：350+ 工具注册表 + Dream Cycle + Skillify/check resolvable + Egalitarian + Trust by default + Horseless Carriages 批评，**与 [[54万行代码的顿悟]] 是同一个人同一时间的不同侧面表达**（组织层 vs 工程师个人层） ⭐
- [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放-digest]] - 上一篇的速读摘要版
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]] - Fiona Fung 一手经验：瓶颈转移到验证/评审/安全 + JIT 规划 + 自动化肌肉记忆 + Trust but verify + Taste is scarce + 团队级 harness + 3 个没答案的问题（iOS/Android 团队、自动化 review 边界、模糊角色信心），范式→组织→实操三层合并 = 完整 AI-native 蓝图 ⭐
- [[Claude-Code团队5条工作原则-Fiona-Fung分享-digest]] - 上一篇的速读摘要版
- [[claude-code-dynamic-workflows]] - Claude Code 动态工作流：让 Claude 现写 Harness 解决任何任务，Anthropic 官方 6 种 Pattern + 10 个真实 Use Case ⭐
- [[claude-code-dynamic-workflows-digest]] - 上一篇的速读摘要版
- [[every-agentic-engineering-hack-2026-06]] - Matt Van Horn 的 22 个 Agentic Engineering Hacks："No IDE. Just plan.md and voice." + YOLO + 多 session 并发 + 工具栈生态 ⭐
- [[every-agentic-engineering-hack-2026-06-digest]] - 上一篇的速读摘要版
- [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] - "在线系统重构迁移"项目真跑过 Spec-Kit + BMAD：**AI 原生 ≠ 人人用 AI 工具 = 让 AI 进入协作流程（AI 依据什么写代码）** + Spec-Kit 拉上限(强秩序) vs BMAD 拉下限(角色化+圆桌) + "没有基线不切换" + 砍需求分阶段持续砍 + BMAD 心智负担是真实成本；与 [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]] [[AI-Coding的顿悟时刻]] [[Claude-Code负责人谈AI原生工程组织]] [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]] 同主线 ⭐
- [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD-digest]] - 上一篇的速读摘要版
- [[Notion-spec-driven-AI-workflow]] - Capihom 2026-06-08 编译自 Latent Space《How I AI》嘉宾 Ryan Nystrom：Notion AI 核心建设者亲自拆解 spec-driven 完整流水线（Whisper→Codex→Spec→@Codex 出 PR → Spec 进仓库做 change log）+ 救 CI / Standup Prep 自动化 / "我不懂"PR 评审 / 工程师=系统思考者+架构师；与 [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]] [[AI-Coding的顿悟时刻]] [[Claude-Code团队5条工作原则-Fiona-Fung分享]] 强关联 ⭐⭐
- [[Notion-spec-driven-AI-workflow-digest]] - 上一篇的速读摘要版
- [[Agentic-Engineering-AI-Workbench]] - 若飞（架构师 JiaGouX）2026-06-08 编译自 Matt Van Horn / John Kim / Kaxil Naik / Addy Osmani：**"Agent 面前摆着一张工作台"——AI 工作台 5 层结构（计划/上下文/执行/验证/治理）+ 可控并行 5 问 + plan.md 8 段任务协议 + 5层上下文×3档载入 + CLAUDE.md 三段式 + Skill=过程资产 + Subagents=隔离 + 团队 3 层权限渐进 + 5 行威胁模型 + PR 模板 + 7 天小试点**；是 [[every-agentic-engineering-hack-2026-06]]（个人 YOLO 版）的"团队工程化版"，与 [[claude-code-dynamic-workflows]] [[从Prompt-Context到Harness-工程的三次进化与终局之战]] [[Notion-spec-driven-AI-workflow]] [[AI-Coding的顿悟时刻]] [[多Agent使用边界与并行判定]] [[任务类型到验证模板]] [[买了一样的AI为什么别家的比你的强]] 强关联 ⭐⭐⭐
- [[Agentic-Engineering-AI-Workbench-digest]] - 上一篇的速读摘要版
- [[Addy-Osmani-Loop-Engineering]] - Addy Osmani 2026-06-09 跨产品方法论长文（**41万 查看 / 3,266 赞 / 7,605 书签**）：**Loop engineering = 用一个会自己循环的 5+1 积木系统替代"人按 turn 提示 agent"的新范式**——5 积木（Automations/Worktrees/Skills/Plugins+Connectors/Sub-agents）+ 1 状态文件（Memory），Codex 与 Claude Code 都已具备；`/loop` + `/goal` 是跨工具统一原语；3 个反噬警示（Verification/Comprehension-Debt/Cognitive-Surrender）+ "Build the loop. Stay the engineer."；与 [[Claude-Code作者Boris-我已经不写prompt了我写loop]] 同主线姊妹篇（本文偏跨工具方法论，Boris 偏 Claude Code dynamic workflow 实现），与 [[claude-code-dynamic-workflows]] [[Agentic-Engineering-AI-Workbench]] [[Claude-Code之父品味不是人类护城河]] [[买了一样的AI为什么别家的比你的强]] [[从Prompt-Context到Harness-工程的三次进化与终局之战]] [[AI-Coding的顿悟时刻]] [[54万行代码的顿悟-Markdown才是新编程方式]] 强关联 ⭐⭐⭐
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] - 若飞（架构师 JiaGouX）2026-06-11 中文工程化深度解读 + 7 天试点：**Prompt → Harness → Loop 层次关系 + 6 工程问题 + 4 入口（触发/沙箱/验收/账本）+ 闭环 vs 开环 + 4 条件准入 + 5 项准入小表（输入/输出/验证/权限/停止）+ 6 类试点场景（技术稿事实核验/CI 分流/文档漂移/重复故障归类/陈旧 feature flag/依赖升级）+ 任务卡预算 + 状态记忆 5 段式 plan.md + 5 条保守原则（先写停止条件再写继续条件）+ 7 天试点路径（D1-D7）+ 复盘 5 指标（命中率/误报率/回滚率/成本/证据）+ "momentum ≠ progress" + "循环越自动，人的判断越要在场"**；是 [[Addy-Osmani-Loop-Engineering]] 的中文工程社区实操版 + [[Agentic-Engineering-AI-Workbench]] 7 天试点的具体落地，与 [[Claude-Code作者Boris-我已经不写prompt了我写loop]] [[Claude-Code一周年回顾-Boris-Cat]] [[Claude-Code之父品味不是人类护城河]] [[从Prompt-Context到Harness-工程的三次进化与终局之战]] [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]] [[多Agent使用边界与并行判定]] [[Codex配置原则总览]] [[Claude-Code团队5条工作原则-Fiona-Fung分享]] 强关联 ⭐⭐⭐
- [[Loop-Engineering-详解-把反馈循环放进工程现场-digest]] - 上一篇的速读摘要版
- [[PM-Skills-Marketplace-产品经理必备skill]] - 开源日记 2026-06-13:phuryn/pm-skills 3 个月 16k Star,9 插件 68 技能 42 命令,把 OST/Lean Canvas/JTBD/Pre-mortem 等产品方法论编入 Skill —— **"通用 AI 给文字模板,PM Skills 给结构化执行路径"** + Skill(独立方法论)=积木 vs Command(组合流程)=流水线 + AI 提问/用户决定 + 方法论壁垒被抬高 + Skill 生态仍在 jQuery 插件时代;与 [[mattpocock-skills]] [[Skill-Self-Evolution]] [[claude-code-large-codebase-best-practices]] [[与AI一起做产品的六条原则]] [[AI-PM核心技能-观测评估与反馈闭环]] 强关联 ⭐⭐
- [[PM-Skills-Marketplace-产品经理必备skill-digest]] - 上一篇的速读摘要版(7 角度 + 21 钩子 + 6 类手法)
- [[APPSO-Codex-Claude-Code-Loop-Engineering]] - APPSO 2026-06-14 产业视角入门:Prompt→Harness→Loop 时代迁移 + 5 个必答问题 + 5+1 积木(Codex Automations / OpenClaw HEARTBEAT)+ 4 类场景(内容/客服/产品运营/研究)+ 3 上手前提(Token/重复/验证)+ 成本转移 + **Boris/Cat Wu/Tibo/Addy 4 产业人物同向信号** + 分界线>术语;**Loop 主题第三视角**:[[Addy-Osmani-Loop-Engineering]] 方法论原典(跨产品 5+1)+ [[Loop-Engineering-详解-把反馈循环放进工程现场]] 中文工程实操(7 天试点)+ 本文产业信号(4 人同向),形成"方法论→实操→产业"三视角闭环;**对 Seetong 4 个可借鉴动作**:盘点已是 loop 的(OpenClaw HEARTBEAT / Seetong 日报周报简报 cron / 神策友盟反馈 dry-run / Login 成功率每日巡检)/ 选 1 个"高 ROI + 验证便宜"场景试 7 天(神策崩溃堆栈归类 / TAPD 过期迭代关闭 / 用户反馈去重)/ 写 Loop 任务卡 8 项必填(循环名称/触发频率/输入范围/最大运行/权限/验证/停止/交付物)/ 拒绝为 loop 而 loop(一次性需求继续用好提示词+Plan 模式);与 [[Addy-Osmani-Loop-Engineering]] [[Loop-Engineering-详解-把反馈循环放进工程现场]] [[Claude-Code一周年回顾-Boris-Cat]] [[Claude-Code之父品味不是人类护城河]] [[从Prompt-Context到Harness-工程的三次进化与终局之战]] [[claude-code-dynamic-workflows]] [[Claude-Code首席设计师Meaghan-Choi工作流]] [[Anthropic万字长文三个判断和一个阳谋]] 强关联 ⭐⭐
- [[APPSO-Codex-Claude-Code-Loop-Engineering-digest]] - 上一篇的速读摘要版(8 节点 + 1 表 + 4 人物同向 + 4 借鉴动作)
- [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] - ColaAI 2026-06-15 整理自 Chrome 团队 Lead Addy Osmani 开源项目（**58.9k Star / 23 技能 / 7 命令 / 3 角色 / 4 清单**）：**agent-skills = 把资深工程师工作流打包,治 AI 写代码"能跑但上生产就崩"**；4 个设计哲学（①流程而非文档 ②**反合理化**-每技能内置"借口→反驳"表 ③验证不可妥协 ④渐进式披露）+ 7 块统一骨架（名称+描述/概述/何时使用/流程/反合理化/危险信号/验证）+ Google 工程文化内嵌（Hyrum定律 / Beyoncé规则 + 测试金字塔 80/15/5 / 变更规模 ~100 行 / Chesterton栅栏 / 主干开发+功能开关）；**3 个对 Seetong 可借鉴动作**：Skill 7 块骨架审计（重点补"反合理化""危险信号"两节）/ 反合理化列入团队 SKILL.md 必填项（写 5 个偷懒借口+标准反驳）/ 复用 7 命令流水线到 Seetong 三端（/spec /plan /build /test /review /code-simplify /ship）接 [[seetong-tapd-version-review]]；与 [[谷歌开源agent-skills]] 同项目 4-27 旧版（20 skills/23k star）配对看、与 [[Addy-Osmani-Loop-Engineering]] [[Loop-Engineering-详解-把反馈循环放进工程现场]] [[APPSO-Codex-Claude-Code-Loop-Engineering]] [[PM-Skills-Marketplace-产品经理必备skill]] [[Agentic-Engineering-AI-Workbench]] [[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]] [[从Prompt-Context到Harness-工程的三次进化与终局之战]] 强关联 ⭐⭐⭐
- [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架-digest]] - 上一篇速读摘要版（1 表 + 4 哲学 + 7 骨架 + 3 借鉴动作 + 8 关联）

- [[InfoQ-Adam-Bender-软件生态学-10倍时刻]] - InfoQ 2026-06-17 编译自 Google 首席软件工程师 Adam Bender (Google I/O 2026 主题演讲):**"软件生态学"整体性学科**(对生产软件的社会技术生态系统进行研究)+ **10 倍代码时刻** 5 个容量型瓶颈(编译/代码审查/Token经济学/测试计算资源/版本控制)必先崩 + **依赖图二次方增长**(10x 代码 → 100-1000x 测试) + **工程是积分编程**(编程可加速,工程是慢变量) + Google 文化 8 特质 + 大规模变更(10 行代码修补 100 亿行应用);**8 个独立知识节点**(软件生态学/社会技术系统/共享命运/大规模变更/10倍代码时刻/工程是积分编程/依赖图二次方增长/智识掌控);与 [[Addy-Osmani-Loop-Engineering]] [[APPSO-Codex-Claude-Code-Loop-Engineering]] [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] [[软件工程的功底是智能时代生死攸关的要素]] **上游强关联**(同一硬币的另一面:Loop 跑起来后 5 个节点会被 10x 撑爆),与 [[Claude-Code一周年回顾-Boris-Cat]] [[Anthropic万字长文三个判断和一个阳谋]] [[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]] **下游强关联**;**5 个对 Seetong 团队可借鉴动作**(画 Seetong 开发者生态图 / 回答"10x 代码量,什么先崩"4 候选 / "工程是积分编程"作为 Seetong 内部 Code Review checklist 第一条 / "代码审查=指导"文化对照 / "小仓库不是救世主"做新模块拆分的反问句,Seetong-KMP 跨平台是反例) ⭐⭐
- [[InfoQ-Adam-Bender-软件生态学-10倍时刻-digest]] - 上一篇的速读摘要版(1 句话 + 4 金句 + 4 反直觉 + 5 Seetong 借鉴动作 + 关联指针)

- [[Claude-Code-主动式Agent-Routines]] - Capihom 2026-06-17 编译自 Anthropic applied AI 团队 Maya 演讲"Build a proactive agent workflow with Claude Code":**"主动式 Agent 不该等你按回车才开始工作"** — Anthropic 在 Claude Code 里推出 **Routines**(按 cron/GitHub 事件/webhook 主动启动远程会话),**最小配置 4 样**(prompt+repo+connector+trigger),**三大基础设施负担**(跑在哪里/什么时候触发/人怎么介入),**主动式 Agent 三大设计问题**(触发器 + 上下文 + 可转向性 Steerability),**渐进路径**(先调查建议,再放行动权限),**Anthropic 内部案例**(Sarah 文档同步 routine + Claude Code 每周 PR 增 200% + deploy verifier 案例),**8 个独立知识节点**,**核心反直觉**("主动式 agent 不要求人消失,要求人能叫停" + "AI 判断不稳定的根因往往不是模型态度,是流程没把信息接进来");**这是 Anthropic 第一次把 Routines 当作"产品定位"对外讲**;与 [[Claude-Code首席设计师Meaghan-Choi工作流]] [[Claude-Code一周年回顾-Boris-Cat]] [[Anthropic万字长文三个判断和一个阳谋]] **上游强关联**(同公司同系列 Routine 异步化的产品化落地),与 [[Addy-Osmani-Loop-Engineering]] [[APPSO-Codex-Claude-Code-Loop-Engineering]] [[Loop-Engineering-详解-把反馈循环放进工程现场]] **下游强关联**(5+1 积木的 Automations=Routines 方法论原典);**5 个对 Seetong 借鉴动作**(现有 cron 流程升级 Routines 思路 / 三大设计问题 checklist / "上下文=成功的上限"作为 Seetong Agent 设计原则 / "小处先赢"渐进路径 / 借鉴 Sarah 文档同步 routine 模式做 Seetong-tps 跨端 changelog 同步);与本文 + [[APPSO-Codex-Claude-Code-Loop-Engineering]] + [[Addy-Osmani-Loop-Engineering]] 形成 02-ai-coding "Routines 主题三角" ⭐⭐
- [[Claude-Code-主动式Agent-Routines-digest]] - 上一篇的速读摘要版(1 句话 + 4 金句 + 5 反直觉 + 5 Seetong 借鉴动作 + 关联指针)
- [[undefinedKi-AI-Second-Brain-10-Step-Guide]] - @undefinedKi 2026-06-20 X 推文长文(**385.6万 查看 / 9,297 书签**):**Karpathy LLM Wiki 模式的 2026-06 实操升级版** —— 一个晚上搭完的 10 步实操(Claude Desktop Pro + Obsidian + Local REST API + mcp-obsidian MCP + CLAUDE.md + 项目级 vault + Skill + Schedule);**核心反直觉**1)**keys, not prompts**——权限控制走 read-only scoped key,不靠"别删文件"的提示词 2)**"The big vault plans. A single project ships."**——大库做规划、单项目独立打开成 vault 才出活 3)**"You are not building a Claude setup. You are building your own memory"**——同订阅完全不同机器;**8 个知识节点**(第二大脑/LLM-Wiki/MCP连接/项目级Vault/Skill化/Schedule自动维护/权限控制优先/Claude-Desktop配置);**三个开源 ready-made 仓库**:claude-obsidian(AgriciDaniel) / obsidian-second-brain(eugeniughelbur,43 命令,跨 Claude/Codex/Gemini) / second-brain-starter(coleam00);**本工作区已有 6 篇相关页面**([[karpathy-knowledge-system]] / [[claude-obsidian-second-brain]] 5-12 旧版 / [[obsidian-claude-code-os]] / [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] / [[garry-tan-ai-second-brain]] / [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]),本文价值在"10 步完整实操"+"Schedule"+"keys-not-prompts";**与 [[Claude-Code-主动式Agent-Routines]] 下游强关联**(Schedule 任务的产品化形式);**5 个对 Seetong 借鉴动作**(MyAIWiki 本库做"现成 demo"/晨间简报升级 Schedule/Seetong 项目级 vault 隔离/重复任务 Skill 化/权限走 Key 不走 prompt);⭐⭐
- [[undefinedKi-AI-Second-Brain-10-Step-Guide-digest]] - 上一篇的速读摘要版(1 句话 + 5 核心观点 + 10 步流程 + 5 金句 + 3 反直觉 + 5 Seetong 借鉴动作 + 关联指针);**附:@ridark_eth 16M 浏览短推文**(https://x.com/ridark_eth/status/2068753952850546985)是本文的引用推广,作为"舆论扩散信号"存档

## Skills 编程实战(企业级落地)

- [[面向Skills编程-淘宝企业购端到端研发提效实践]] - 大淘宝技术(官亭,淘天集团-行业运营技术团队)2026-06-17：**"面向 Skills 编程"新范式——Skills = AI 研发的最小可复用单元**(工作流 + 领域知识 + 约束规则);**商品域端到端交付周期 23.5 人日 → 8 人日(整体提效 65%)**,**代码一次生成成功率 50% → 90%(全靠知识工程,不是换更强的模型)**;**五阶段演进路径**:Vibe Coding(对话驱动,2025.8)→ Prompt 模板(标准化语义翻译器,2025.9,**采纳率 70%**)→ SDD 规范驱动(2025.12,**可用率 40% → 80%**)→ Skill 沉淀(经验固化,2026.1-2)→ 云端集成(端到端产品,2026.2 探索中);**核心命题"质量瓶颈不在模型,在知识工程"**——50% → 90% 全靠知识注入和约束迭代,不是换更强的模型,领域知识(映射规则/API 签名/模式判定)不会从训练数据中涌现,必须显式注入;**确定性工程 + 不确定性 AI = 可控流水线**(脚本提取 + 架构拆分 + 约束沉淀);**三层架构**(原子能力层 + 模板层 + 适配层,AI 只聚焦适配层逻辑,**代码量 -60%**,多客户并行零冲突);**ADJUSTMENT_PLAN 五步闭环**(发现 → 定位 Skill → 补约束 → 验证 → 交叉验证)将 **11 类高频问题全部沉淀为 Skill 约束,不再复现**;**事前约束 → 运行时约束 → 事后审查 → 人工卡点 四层质量防线**;评估报告 Skill 实测 **15/15 接口覆盖,字段遗漏率 0%**;**8 节点 + 5 个对 Seetong 借鉴动作**(知识工程体检/三层架构重写 Seetong 适配层 Skill/ADJUSTMENT_PLAN 闭环建高频问题约束库/SOP 四层防线/Seetong 端到端生码平台 P0 小试点);与 [[阿里云开发者-淘宝主播Agent的Harness工程实战]] [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] 阿里淘系同源(主播=实时交互高风险/企业购=高频定制化交付/业务需求=研发流程自动化);与 [[Skill-Self-Evolution]] [[Agent Skills 系统性综述]] [[谷歌开源 agent-skills]] [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] [[PM-Skills-Marketplace-产品经理必备skill]] Skill 主线;与 [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] [[Notion-spec-driven-AI-workflow]] [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]] SDD/Spec 主线(本文 SDD 是 5 阶段中的第 3 阶段);与 [[Loop-Engineering-验证才是瓶颈]] 互补(本文讲 Skills 单元构建,那篇讲 Loop 验证闸门);与 [[腾讯-AI-Agent-Skill-测评方案落地]] "测评是 Demo→生产必须跨过的门槛"同主线;与 [[AI-Coding的顿悟时刻]] [[54万行代码的顿悟-Markdown才是新编程方式]] AI Coding 范式 ⭐⭐⭐
- [[面向Skills编程-淘宝企业购端到端研发提效实践-digest]] - 上一篇的速读摘要版

## 核心原则

1. **AI Coding 不是选择题，是必选题**
2. **提示词要具体，模糊的问题得不到好的答案**
3. **每次重构后复盘，积累有效的提示词**
4. **AI 生成的结果一定要review，不能直接用**

## 标签

#主题/AI-Coding
- [[Claude-Code负责人谈AI原生工程组织]]
