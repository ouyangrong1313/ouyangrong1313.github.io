# YC 如何进行 AI-Native 组织改造：Agent 能力要向所有人开放

- 原文链接：https://mp.weixin.qq.com/s/dcpsur_udGz6tLW-yARU8w
- 来源：Founder Park
- 采访对象：**Pete Koomen**（YC 合伙人 + Optimizely 创始人） + **Gary**（即 **Garry Tan**，YC 总裁）
- 编译时间：2026-06-03
- 来源层：raw（已存 `raw/articles/YC如何进行AI-Native组织改造-Agent能力要向所有人开放.md`）

## 核心结论（一句话）

**真正的 AI-Native 组织 ≠ "把 AI 当 Copilot 用" —— AI 必须作为整个组织运转的建设层（building layer），系统性记录所有 artifacts 作为 Agent 可学习的原材料；前提是 Egalitarian（AI 能力向每人开放）+ Trust by default（默认信任）。YC 一年内演化出 350+ 工具的内部注册表 + 全员可见的 Agent 对话 + 每晚自动改进技能的 Dream Cycle。**

## 分类提炼

- 场景：AI-Native 组织 / Harness / Tool Registry / Skill / Dream Cycle / 文化建设
- 标签：#主题/AI-Coding #主题/AI-Native #主题/AI-Agent #主题/Harness #主题/Skill #主题/工程管理 #主题/组织文化 #手法/范式反思 #场景/YC播客
- 类型：一手经验 / 范式宣言 / 方法论
- 关联主线：与 [[Claude-Code负责人谈AI原生工程组织]]、[[54万行代码的顿悟]] 同主线（甚至**同一个人**！）

## 关键人物一致关系（重要发现）

文中的 **Gary** 就是 [[54万行代码的顿悟]] 的作者 **Garry Tan**（YC 总裁）。文里提到的 **Gbrain** 就是 [[54万行代码的顿悟]] 里的 **GBrain**（8 层 AI 第二大脑）。**这不是两个独立作者的两篇文章，是同一个人/同一段时间的不同侧面表达。**

**数据交叉印证**：
- [[54万行代码的顿悟]]：54 万行 Rails 代码（Gary's List）
- 本文："一月到二月我用 Rails 写了约五十万行代码，Gary's List"
- **完全吻合** → 同一项目的两次叙述

## 6 节核心方法论

### #01 从财务 Agent 开始 + 偷偷推 PR 开放生产数据库

- **起源动机**：财务团队向工程师描述工作流 → 翻译成软件，循环低效
- 改用 Agentic coding（Windsurf、Cursor、Claude Code）直接给财务团队构建 Agent
- 第一次 unlock：Jared 推 PR 给 Agent 开放**生产数据库完整只读权限**（"违规" 推的）
- 效果惊人

> **"真正阻碍这些工具发挥威力的，不是技术能力，而是我们对安全和隐私的过度担忧。"**

> 工作/生活的割裂："在家里用 Claude Code 或 OpenClaw 什么都能做，到了公司就被塞进一个狭窄的框里"

### #02 杰文斯悖论：成本下降 → 需求爆发

YC 优势：所有自研软件跑在**同一个 Postgres**。

> **"当某种资源的使用效率提高时，人们反而会消耗更多这种资源。"** —— 杰文斯悖论

- SQL 查询门槛降低后，不仅老问题更容易回答，**新问题（以前不敢问的）开始出现**
- **"成本下降带来的不是需求减少，而是需求爆发"**
- **数据反规范化**：从 schema + join → 针对 Agent 优化的大宽表（类似 BigTable）
- **Gbrain**：多源数据 + RAG + Graph RAG + RRF 混合重排序 + MCP/CLI 包装

### #03 上下文 + 工具注册表（Resolver） + Skill 抽象层

**YC Agent 核心架构（极简）**：
- Agent 循环
- **工具注册表（tool registry）= Resolver**
- 模型路由器

YC 工具从 20 → **350+**。工具注册表 = Resolver，"告诉 Agent '我能做什么'"。

**Skill 是对工具的更高层封装**（可复用 + 有明确语义）。

**两个元技能（meta skill）**：
1. **Skillify it**：做完某事说"skillify it" → Agent 自动封装注册
2. **check resolvable**：每次 Skillify 后调用，检查
   - **DRY**（Don't Repeat Yourself）：10 个做同一件事的技能是坏的
   - **MECE**（Mutually Exclusive, Collectively Exhaustive）：麦肯锡术语，模型天然理解

> "这些概念在各种 Agent harness 里被反复独立发现，Claude Code 有 skill registry，我们有 tool registry，OpenClaw 有 resolver。**感觉就像 Unix 早期发现栈和堆一样，我们正在定义 Agentic 系统的基础原语。**"

### #04 Dream Cycle + 两句话描述（具体例子） + 超级组织诞生

**Dream Cycle**：每晚通用 Agent 读取当天所有对话，识别"本可以做得更好的地方"，次日自动优化相关技能。

**两句话描述（具体例子）**：
- Tom 写提示词 → 多人使用 → group office hours 会议转录反馈 → Agent 改进技能
- 改进后效果肉眼可见地更好，**这个技能现在比任何一个人单独做都要好**

**超级组织诞生路径**：
1. 写提示词
2. 使用产生 artifacts
3. metaprompt 喂回
4. 每日 Dream Cycle 自动改进
5. 技能超越单个人
6. 把组织里每件事这样处理 = **超级组织**

> "不是理论，现在每个人都可以做到。"

**同类独立出现**：
- OpenClaw 的 Dream Cycle
- Karpathy 的 auto-research
- Codex 的 SLG（Self-Learning Goal）

### #05 所有对话对 YC 全员可见

每个 Agent 对话自动广播到内部 Slack 频道。

**三个好处**：
1. **知识传播**：看别人的用法来学习
2. **社会性控制**：让安全变宽松（高信任 + 操作可见 = 不需要严格技术控制）
3. **降低新员工门槛**：六个月上手 → 阅读对话快速了解（"AI 自动完成的学徒制"）

> "shared organizational brain" — 最接近"连接彼此大脑"的东西

**Anthropic CEO Dario 的话**："AI 进步的很多阻碍不是技术性的，而是社会文化性的"

**超级智能组织必须具备的两个文化特质**：
- **Egalitarian**（平等主义）：AI 能力必须向组织中每个人开放
- **Trust by default**（默认信任）：上下文和数据不锁在权限层级

**Token 成本**：$10K-100K/年

> "如果你投入了、建好技能体系、以开放方式跟团队协作，你基本上在活在 2028 年。**现在有一个一次性的时间跳跃窗口，你可以跳过所有现存的巨头、所有 Fortune 500、所有已有的创业公司。**"

### #06 Horseless Carriages：Agent 应该包裹确定性工具

**Pete 的 "Horseless Carriages"（无马马车）批评**：
- 现在的 AI 软件多数仍是"在确定性软件里嵌一小块 AI"
- Gmail AI 写邮件：prompt context 被开发者锁死，用户无法访问/修改
- **本质上是把 AI 的控制权集中在开发者手中**

**正确方向**：

> **"当 AI 越来越成熟，正确方向是 Agent 包裹确定性工具（agent wrapping deterministic tools），而不是确定性软件包裹 AI。"**

**Chat 作为 UI**：
- "Chat 最接近人类语言，人类语言最接近思维的表达"
- "你不能把它塞进框里"
- "Chat 是清晰智能的最近跳板"
- "Chat 是多模态的，文字、语音、图片、文件都行"

**just-in-time software**：
- Agent 当场生成单页 JS 用完即弃
- 技能文件可随时再调用

**Gary 真实数据交叉印证**：
- 54 万行 Rails 代码（1-2 月）
- 1 万 TypeScript + 2 千 Markdown 重写（3 天）—— **just-in-time software 真实体现**

**Pete 的极简偏好**：
- **Pi**（极简开源 Agent harness）："代码量极小，但你可以用 Pi 修改和扩展 Pi 自身"
- 这种"自我扩展"的软件形态很迷人
- 未来商业软件 = 极小起点 + Agent 按需扩展

**Claude Code 的 Boris**：对简洁同样执念

## 关键引用（保留原文力度）

> "真正阻碍这些工具发挥威力的，不是技术能力，而是我们对安全和隐私的过度担忧。"

> "杰文斯悖论说的是：当某种资源的使用效率提高时，人们反而会消耗更多这种资源。**成本下降带来的不是需求减少，而是需求爆发。**"

> "工具注册表本质上是一个 Resolver（解析器），它告诉 Agent '我能做什么'。"

> "如果你有一个 DRY + MECE 的 Resolver 表，那就是最优解。"

> "感觉就像 Unix 早期发现栈和堆一样，我们正在定义 Agentic 系统的基础原语。"

> "这个技能现在比我们任何一个人单独做都要好。"

> "AI 进步的很多阻碍不是技术性的，而是社会文化性的。"

> "**现在有一个一次性的时间跳跃窗口，你可以跳过所有现存的巨头、所有 Fortune 500、所有已有的创业公司。**"

> "正确方向是 Agent 包裹确定性工具（agent wrapping deterministic tools），而不是确定性软件包裹 AI。"

> "**Chat 是清晰智能的最近跳板。**"

> "最好的 AI 软件往往是最小的，只在模型能力之上加最少量的预写代码，让模型做最多的工作。"

## 新方法论/术语清单（建议补到知识库）

- **Skill 抽象层**：对工具的更高层封装
- **Skillify it 元技能**：自动封装注册
- **check resolvable 元技能**：DRY + MECE 检查
- **Dream Cycle**：每晚自动改进技能
- **杰文斯悖论应用**：成本下降 → 需求爆发
- **数据反规范化**：针对 Agent 优化的大宽表
- **Agent 包裹确定性工具**（vs Horseless Carriages）
- **just-in-time software**：Agent 当场生成、用完即弃
- **社会性控制**：用高信任 + 操作可见代替严格技术控制
- **shared organizational brain**：组织集体技能和直觉
- **AI 超级组织两个文化特质**：Egalitarian + Trust by default
- **时间跳跃窗口**：2026 年活在 2028 年
- **Egalitarian + Trust by default**：超级智能组织的前提

## 我的判断（编译者注）

1. **本文是 [[54万行代码的顿悟]] 的官方补完**：
   - 同一作者（Garry Tan）同一时间段不同侧面表达
   - 54 万行顿悟讲"工程师个人范式"（Markdown 是新编程方式）
   - 本文讲"组织层面"（Egalitarian + Trust by default + 工具/Skill 注册表 + Dream Cycle）
   - **合起来 = 工程师个人 + 团队流程 + 组织结构** 三层完整的 AI-native 蓝图

2. **"偷偷推 PR 开放生产数据库" 是 YC 的"卢德分子"故事**：
   - Jared "觉得自己在违规" 推了 PR
   - 效果惊人
   - 教训：**在 AI 时代，"违规"往往就是创新**
   - 这和 [[Codex配置原则总览]] 提到的"边界必须明确，但不要过早"呼应

3. **"Skill + Skillify + check resolvable" 是超级具体的可操作新方法论**：
   - 之前 [[54万行代码的顿悟]] 讲 "Skillify it" 循环
   - 本文补完：**check resolvable + DRY + MECE**
   - **新组合**：Skillify 完必 check resolvable，保证 skill 库的健康
   - 这是 [[Codex配置原则总览]] / [[多Agent使用边界与并行判定]] 都应该补的新原则

4. **"Dream Cycle" 是 AI-Native 组织的关键基础设施**：
   - 没有 Dream Cycle，技能库会"用着用着烂掉"
   - 有了 Dream Cycle，技能库会**每天自动变强**
   - 我们的 MyAIWiki 知识库**就是缺这个机制**——可以考虑加一个 weekly dream cycle，让 AI 读本周新加的内容自动归并、提炼、改进

5. **"Egalitarian + Trust by default" 是文化层面的硬约束**：
   - 技术上容易实现，**文化上最难**
   - 大多数企业 command and control 模式是反 AI-native 的
   - **Seetong 团队反思**：我们 AI 工具谁先用？决策权谁有？信息是否锁在层级里？
   - 这不是技术问题，是文化问题

6. **"Agent 包裹确定性工具" 是 AI 软件设计原则**：
   - 大部分产品现在还是 "确定性软件包 AI"（Horseless Carriages）
   - 真正未来 = "极小起点 + Agent 按需扩展"
   - 验证方法：问"我们这个产品，是让用户表达意图，还是让用户按按钮？"

7. **"Chat 是清晰智能的最近跳板" + "just-in-time software" = 对我们产品设计的启示**：
   - Seetong App 如果走"按按钮"模式，迟早被淘汰
   - 应该走"自然语言 + Agent 现场生成 UI"模式
   - 用户问"最近 24 小时 XX 设备的异常告警"，Agent 现场生成一个针对性的页面

8. **"现在有一次性的时间跳跃窗口" 是这篇文章给的最大商业启示**：
   - $100K 投入 → 2028 年的能力
   - 不投入 → 永远在后面
   - 验证：$10K-100K/年 token 在 Seetong 团队算不算大钱？如果团队一年 50 万工程师成本，**5-20% 的 token 投入可能带来 50%+ 的产出**

## 适合关联的主题

- [[Claude-Code负责人谈AI原生工程组织]] — 同主线，组织侧瓶颈迁移
- [[54万行代码的顿悟]] — **同一个人**，**同一段时间**的工程师个人范式
- [[AI-Coding的顿悟时刻]] — Spec→LDD 流水线 + Scrum 反思
- [[Codex配置原则总览]] / [[Codex配置优化清单-从Harness视角]] — 工具注册表 + Skill 设计原则
- [[Codex才是最适合普通人的顶级牛马-Agent]] — Agent 工作台化
- [[来自Codex官方团队的分享：如何把Codex用到极致]] — durable threads + 共享记忆
- [[多Agent使用边界与并行判定]] — 应该补 Skillify + check resolvable
- [[你不知道的 Agent：原理、架构与工程实践]] — Agent 架构基础
- [[软件工程的功底是智能时代生死攸关的要素]] — 反思
- [[知识卡片编译模板-长文如何压成raw-digest-wiki三层]] — 知识库本身的 skill pack 化样本
- [[任务类型到验证模板]] — 应该补"知识/Markdown/Skill 验证"类型

## 行动建议

- [ ] **盘点自己团队**：AI 工具谁先用？决策权谁有？信息是否锁在层级里？—— Egalitarian + Trust by default 不是技术问题
- [ ] **建一个工具注册表（Resolver）**：哪怕是 20 个工具起步
- [ ] **把 Skillify + check resolvable 流程化**：每次新建 skill 必 check DRY + MECE
- [ ] **Dream Cycle 试点**：每周跑一次，让 AI 读本周对话/任务自动改进技能
- [ ] **数据反规范化**：评估自家数据是否要为 Agent 优化一次
- [ ] **产品设计的 Horseless Carriages 检查**：问"我们产品，是让用户表达意图，还是让用户按按钮？"
- [ ] **时间跳跃窗口判断**：$10K-100K/年 token 在我们团队算不算大钱？是否能换来 50%+ 产出？
- [ ] **推 PR 心态**：让团队有"违规推 PR 也能起效"的安全感
- [ ] **对标 YC 的"两句话描述"**：能不能也把自己团队的核心动作做"原子化、技能化"？
