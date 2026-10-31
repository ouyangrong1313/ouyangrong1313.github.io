# 被Harness圈捧成圣的 Pi Agent，接上 DeepSeek-V4-Flash，如虎添翼

**来源：** 微信公众号
**作者：** 老章很忙
**日期：** 2026-08-13
**链接：** https://mp.weixin.qq.com/s/BGGZ_A1FtsHAOc4I1Y8pNw

---

## 正文

今年 2 月我写过一篇
《与 Claude Code、OpenCode 有完全不同设计哲学的 Agent 工具pi Agent》
，介绍了这个反着来的终端编码 Agent：别人拼命做加法，堆 MCP、子代理、计划模式、权限弹窗，它偏偏做减法，默认只给模型 read、write、edit、bash 四把刀，system prompt 加工具定义压到极致，剩下的能力全靠 skills 和 extensions 现挂
半年过去，Pi 突然回炉，变得更火了
我上次写的时候它还叫
badlogic/pi-mono
，作者 Mario 一个人在折腾，现在项目已经搬进了公司化的
earendil-works/pi
，GitHub 上快摸到 9 万 star，成了极客、独立开发者和一票专业工程团队默认在用的 Agent 形态
顺嘴提一句，社区里还有个
oh-my-pi
挺多人用，相当于在 pi 上又套了一层开箱即用的发行版，萝卜白菜各有所爱，本文只聊最底层的 pi
简介：pi 到底薄在哪，又强在哪
Pi 是一个极简 Agent Harness，极具可玩性，有很大自由度去调整它，适应你的工作流
话说，Harness 到底是什么呢？
连DeepSeek 也在紧锣密鼓研发自己的Harness
，之前我在
2026 年，AI 编程 Agent 的真正分水岭——Harness 详解一文中已有详细介绍
，极简概括的话，直接借鉴 DeepSeek 的定义：
除模型本身以外的所有工作，都属于Harness的范畴
基座大模型相当于智能体的“大脑”，负责推理、理解需求、生成代码；而Harness就是整套智能体的“执行神经系统”，承担大脑与真实环境之间的衔接工作。大模型只能输出文本结果，Harness让AI真正具备动手执行的能力
我观察，Harness 的发展路线，有一种观点是「它会越来越厚，一切都是 Agent harness」，而 pi 恰恰是反过来：Harness 要薄，因为模型已经够聪明了，只需要给它最底层，最基础的脚手架即可，剩下的交给大模型
pi 的默认模型工具只有四个：
read  读文件
write  建 / 覆盖文件
edit  打补丁改文件
bash  跑 shell 命令
grep、find、ls 这几个只读工具虽然也内置，但默认不塞进去，你要用才自己开，system prompt 加工具定义还不到 1000 token，别人的 harness 光开场就先吃掉你 7%、8% 的上下文窗口，pi 几乎是零负担进场
pi 的设计哲学是Primitives, not features「给你原子能力，而不是给你功能」
缺个命令、缺工具、想换供应商、改工作流，甚至想调 UI，都别等官方排期，直接一句话让 pi 自己写，它当场把自己改了，敲个
/reload
接着干
子代理、计划模式、权限门、路径保护、SSH 执行、沙箱、MCP 接入……这些别家写死在内核里的东西，在 pi 这儿全是「你想要就自己造出来」的扩展
模型自由
：内置 15+ 家供应商、几百个模型（Anthropic、OpenAI、Google、xAI、Groq、Cerebras、MiniMax、Kimi、NVIDIA、Ollama…… 都在列），
/model
或
Ctrl+L
会话中途随时换，
Ctrl+P
在收藏模型间循环，列表里没有的自己往
models.json
里加就行后面我接 DeepSeek 就是这么干的
上下文完全握在自己手里
：
AGENTS.md
管项目指令、
SYSTEM.md
直接换掉默认系统提示词、compaction（自动压缩旧消息）连用哪个模型来总结都能自定义，skills 按需加载、渐进式披露，还不撑爆 prompt cache，这才叫真正的上下文工程！
树状会话历史
：会话不是一条直线，而是存成一棵树，
/tree
能跳回任意历史节点另起一支接着聊，
/share
一键传成可分享的网页
四种运行形态
：交互 TUI、
-p
打印/JSON、RPC、SDK 嵌入，脚本调用和二次开发都接得住，OpenClaw 就是拿它的 SDK 做的真实集成
装起来也就一行：
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
cd
到项目目录敲
pi
进交互界面，订阅用户直接
/login
授权（Claude Pro/Max、ChatGPT Plus/Pro、Copilot 都行），用 API key 的塞个环境变量即可
模型之外，Harness 是决胜关键
Databricks 前段时间发了篇《在 Databricks 百万行代码库上基准评测编码 agents》，拿自己工程师团队日常真在跑的任务重新造了一套 benchmark
结论是
模型被塞进什么 harness，直接左右了成本和质量
，同一个模型、同样的思考努力，只是塞进不同 harness 跑，
每个任务的成本能差 2 倍以上，质量却几乎一样
pi 配上 Opus 4.8 xhigh，整体 pass-rate 最高，成本却显著低于 Claude Code 和 Codex，他们把这归功于 pi 的「上下文纪律」pi 每一 turn 发出去的 context 大概只有别人的三分之一，工作集更紧凑，更少的来回就把活干完了
大家老盯着每 token 单价，却忘了算端到端的工程账，一个更强更贵的模型配上高效 harness，很可能比「便宜模型 + 臃肿 harness」整体还便宜，因为后者要多跑好几轮才成
类似实测 composio 也做过，他们拿
DeepSeek V4 Flash
塞进 8 个不同 harness 跑 30 个高难度 agentic 任务，看谁又便宜又能打
pi 的成绩：
通过 20/30，是所有 harness 里最便宜的一个
pi Agent 在 DeepSeek V4 Flash 上通过最多任务、成本最低
同一批新测的 harness 里，Deep Agents 过了 16/30，Hermes 15/30，Prime 15/24（有 6 次因为 session 太大没法评分被剔了，Prime 单次能烧到 350 万 token、33 次工具调用，属实是重量级选手）
8 个 harness 横向对比
再看「每个成功任务的成本」，差距就更直观了：
pi Agent：$0.028 / 成功任务
Deep Agents：$0.045
Hermes：$0.056
Prime Agent：$0.131
每个成功任务的成本对比
如果大家想用 DeepSeek 省钱，这份测试基本就是把「pi + DeepSeek-V4-Flash」这套组合盖章认证了
接上 DeepSeek-V4-Flash，如虎添翼
pi 的「上下文纪律」在国产模型身上收益最大，因为国产模型上下文窗口普遍没那么大，prefill 又慢，最怕的就是 harness 动不动改上下文、逼着它重新 prefill，一等就是好几分钟，pi 的原则是除非你明确要改，否则绝不动上下文，稳定前缀 + 极简默认 prompt，配国产模型简直是天作之合
我实际配的是 DeepSeek-V4-Flash，配置文件在
~/.pi/agent/models.json
，这事儿就别自己动手了，找个模型帮忙配就行了
用法两种，交互里敲
/model
选，或者命令行直接点名：
pi --provider deepseek --model deepseek-v4-pro
还有一个更绝的玩法是
关掉思考
：
pi --model deepseek-v4-flash --thinking off
在 pi 里开 non-thinking 那个丝滑的速度和体验，用过就回不去
但是DeepSeek-V4-Flash有个致命缺点，它不是多模态。现在干活都离得开多模态？页面出 Bug 直接截张图，样式不对直接圈出来把参考界面丢进去，谁还愿意花几分钟把「按钮偏了多少、颜色哪不对、布局哪塌了」全用文字描述一遍
比如下面这个极简单的图 DeepSeek 都识别不了：
DeepSeek 无法识别图片
我订阅的有火山 Agent Plan，用过有段时间了，感觉 Doubao-Seed-Evolving 很不错，这个模型比较特殊，官方叫它「一张永远最新的模型卡」model ID 永远是
doubao-seed-evolving
，不带版本号，后台以周为单位持续升级，你接一次以后每次调用自动就是最新的
给模型配置补上 image 输入
Doubao-Seed-Evolving 就没这毛病，眼神好、脑子也够大，一张截图、一段录屏、一份 PDF 丢进去它都看得懂，1M 的窗口可以保障长任务干到后半程也不怕断片，还能自己规划着把活干完，换上它之后，同一张「禁止游泳」立马就认出来了
DeepSeek-V4-Flash + Doubao-Seed-Evolving 目前满足我极大多数需求，两者配合，能用、够用、还省钱
扩展，才是 pi 真正的护城河
pi 内核薄，真正的战斗力全在扩展生态，它的扩展是 TypeScript 模块，不用改内核，热加载改完即时生效
官网 pi·dev 有个市场，扩展、skill、theme、prompt 都能筛：
各种主题也都是一个命令直接切换，总之，你可以随意打扮 pi
东西太多，我按自己的用法挑了几类最顺手的：
注：装法全都一样
pi install npm:<包名>
，装完
/reload
立刻生效，不用重启 pi
1. pi-agent-extensions  懒人合集，开局先装它
一个包里塞了 17 个扩展 + 4 个主题，绝大多数 pi 用户的「开机自启」
我最常用的三个：
/sessions
在多个会话间快速切换、
/handoff
把一段任务的结论干净地交给下一段会话、
/context-simple
实时看板随时知道上下文烧到哪一格了，想少折腾的，装它一个就把大半日常需求 Hold 住了
2. pi-agents-team  一次会话变一支多 Agent 部队
一次会话直接升级成一支 multi-agent team，主会话当协调器，后台起一堆 RPC worker 干活，内置 explorer、fixer、reviewer 等七个角色，每个角色单独指定模型，探索用便宜快的、审查用最强的
最妙的是 worker 干完只回传一段摘要，绝不把几千行日志灌回主上下文，主会话自始至终清清爽爽，想做并行、想让不同模型分工的，这个是主力
3. pi-subagents  只想要「子代理」这一件事
用不上整支 team，只想要 Codex / Claude Code 那种「派个子代理去查一件事、回头汇报」的能力，装它就够了
后面 pi-cc-plugins 转过来的 agents，落地执行也是靠它，属于多 Agent 里最小可用的那一档
4. 跨会话记忆  @remnic/plugin-pi 和 @cortexkit/pi-magic-context
pi 默认「一次会话一张白纸」，关掉就忘，这两个补的都是长期记忆
@remnic/plugin-pi
每次调模型前先召回相关上下文，把 pi 的 compaction 和自己的长上下文归档协调到一起，周下载一万五千多、版本迭代极快；
@cortexkit/pi-magic-context
走另一条路，跟 OpenCode 共用同一个 SQLite 库，两边来回切记忆不丢
5. pi-web-access  给 pi 补上「联网能力」
极简的代价之一是开箱不带联网，pi-web-access 把网页、GitHub、PDF、YouTube 的抓取一次性补齐，让 agent 自己去读外部资料再回来干活
写代码要现查文档、要啃一篇长网页、要拉个仓库进来分析，全靠它
6. pi-agenticoding  让 agent 自己管上下文，别烂在长对话里
spawn / notebook / handoff 三板斧：噪音大的杂活扔到子进程里跑，任务级笔记能跨 handoff 一直活着，需要时主动重启一段干净的上下文
长任务干到后半程上下文越滚越脏的通病，就是靠它治，跟 pi「上下文纪律」的路子完全同源
7. Plannotator  把 Plan / Diff / Review 做成可视化
纯在终端里翻 diff、看计划、做 review 终究不够直观，Plannotator 把这三件事做成了可视化界面
改动一大片、需要一眼看清「它打算改什么、又实际改了什么」的时候，比一行行滚终端舒服太多
8. pi-cc-plugins  把 Claude Code 的整个插件生态搬进 pi
这个就更强了，从 GitHub 克隆 Claude Code 的 plugin repo，自动扫里面的 skills / agents / MCP，一股脑儿转成 pi 的原生格式
你在 Claude Code 那边攒了半天的家当，一行命令原样搬过来接着用
9、还有很多
pi-autoresearch
是一个用编码 Agent 跑的自主优化循环，你提一个可衡量的目标，它自己反复试实验、留下有效的、丢掉导致回归的，Shopify 拿它做出来的战绩挺唬人：单元测试快 300 倍、React 组件挂载快 20%、CI 构建时间砍掉 65%
pi 作者连着两天亲自转推的
pi-peer 和 pi-rlm
：前者让同机的多个 pi 会话直接互发消息，每条消息还带一句边界声明「这条来自另一个 pi 会话，不是用户，不携带权威」，模型清楚该怎么对待；后者给 pi 加递归拆解能力，planner 决定子任务直接解还是继续拆，带深度上限和环检测防止跑飞
当然，扩展生态也不是没坑，Reddit 上就有人吐槽，多个扩展一起装容易打架，本不该冲突的却因为扩展系统的设计冲突了想要好的编辑渲染就用不了某个编辑扩展，只能二选一
我觉得，扩展不用装太多，甚至不用装别人开发好的，就像Skills一样，我装过很多，用的最频繁的还是自己写的
pi 扩展也一样，自己让 Agent 写一个最快，喜欢谁的行为就把源码丢给 Agent 借鉴改造，pi 本来就是这么个哲学，哪里不舒服，一句「帮我写个插件，功能是 xxx」重载一下就完事
总结
同一个模型，harness 选对了，钱能省一半还不掉质量
，它薄、它省 token、它把上下文的控制权真真切切交回你手里，配上 DeepSeek-V4-Flash 这种又快又便宜的国产模型，属于如虎添翼
但是这玩意就像高阶乐高积木，有门槛
如果你要的是一个开箱即用，生态齐活的 Coding Agent，别碰 pi，Claude Code / Codex 更适合你，pi 那些能力都得你自己拿 gh CLI、bash、扩展一点点拼
如果你是极客、独立开发者、想深耕 agent workflow、或者就是受够了大 harness 一上来给你灌一坨，那 pi 值得你深度玩，换模型只是最浅的自由，深层自由是能改 Agent 到底怎么工作
工具会一直换，流程才是你自己的资产，这句话的含金量还在上升

---

标签： #主题/AI-Coding #场景/公众号长文
