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

## 核心原则

1. **AI Coding 不是选择题，是必选题**
2. **提示词要具体，模糊的问题得不到好的答案**
3. **每次重构后复盘，积累有效的提示词**
4. **AI 生成的结果一定要review，不能直接用**

## 标签

#主题/AI-Coding
- [[Claude-Code负责人谈AI原生工程组织]]
