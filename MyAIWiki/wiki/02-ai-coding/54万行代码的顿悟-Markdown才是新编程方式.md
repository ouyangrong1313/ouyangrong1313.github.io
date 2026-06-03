# 54 万行代码的顿悟：Markdown 才是新编程方式

- 原文链接：https://mp.weixin.qq.com/s/cqyQma3jFUlZf4_uJnH5lA
- 原文作者：Garry Tan（Y Combinator 总裁）
- 原文出处：X 长文 https://x.com/garrytan/status/2061454423034110372
- 编译时间：2026-06-03
- 来源层：raw（已存 `raw/articles/54万行代码的顿悟-Markdown才是新编程方式.md`）

## 核心结论（一句话）

**54 万行 Rails 代码只是产物，真正重要的是副产品 GStack——一个把 Markdown 当作"新编程方式"的工程体系。** 当你能用 Markdown 把意图直接转化为可运行、经过测试、可重复使用的系统时，**稀缺资源就从代码行数变成了人的意图清晰度、品味和判断力**。代码/模型经济方程、编程介质、稀缺资源三个反转同时发生；不在 Token 上砸钱的组织把先发优势拱手让人。

## 分类提炼

- 场景：AI Coding / Agent 工程 / Skill 设计 / 工程组织 / 范式反思
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/Harness #主题/工程管理 #主题/Skill #手法/范式反思 #手法/经济反转 #场景/YC公开课
- 类型：方法论整理 / 范式宣言 / 实战启发
- 关联主线：与 [[Claude-Code负责人谈AI原生工程组织]]、[[从Prompt-Context到Harness-工程的三次进化与终局之战]] 同主线，但视角更激进

## 三个反转（核心方法论）

| 反转 | 旧的 | 新的 |
|---|---|---|
| **经济方程** | 调用模型很贵，写代码很便宜 → 用代码当保姆 | 模型越来越便宜+聪明 → 价值/成本彻底反转 |
| **编程介质** | 代码是唯一表达（冻结的死逻辑） | Markdown（指令层，可即时编辑）+ 极薄 TypeScript（确定性层） |
| **稀缺资源** | 谁能写更多代码 | 谁的意图更清晰、品味更好、判断力更强 |

## "AI 富士康工厂"的具象化（看 Garry 的真实成本）

Garry 自己的 Garry's List：
- 26.2 万行应用代码 + 27.6 万行测试代码（"审计委员会"比"公司本身"还庞大）
- 127 个后台任务，其中 33 个 cron
- 一个 1778 行的"怀疑与核对"文件：把模型说的每句话分发给 5 个不同来源比对、打分、分流闸口
- 各种 Sanitizers / Validators / 层层重试循环

> 《瑞克和莫蒂》里那个被造来递黄油的机器人，蕴含无限可能，但被造来递黄油。我那 27.6 万行测试代码，就是那个黄油碟。

## Markdown 是新编程方式（不是随手 Prompting）

- **有版本控制、经过测试、可重复使用**
- **Markdown = 指令层**：意图、技能、如何完成工作的判断
- **TypeScript = 薄薄的确定性层**：必须由代码实现的、I/O、绝对不能幻觉的部分
- **关键：你要像测试代码一样测试 Markdown**

## "Skillify it" 循环（最值钱的工程实践）

构建某个东西直到能跑通 → "把它技能化（skillify it）" → 智能体自动产出：

1. Markdown 技能文档
2. 最低限度代码
3. 针对该代码的单元测试
4. 针对该技能的 LLM 评估机制
5. 贯穿两者的集成测试
6. 一个 resolver，让智能体在该技能相关时自动调用
7. 针对该 resolver 的评估机制

**整个组合就是 skill pack——一个可以产生复利效应的可复用能力单元。**

> "测试就是魔法所在：对技能的测试覆盖率，正是让它在改变时不会崩溃的保障。"

> 这就是它与 vibe coding 的区别。vibe coding 是玄学，skill pack 有实打实的测试。

Garry **已经拥有 350+ 个 skill pack**，覆盖大多数个人和工作任务。

## 关键引用（保留原文力度）

> "我建了这样的工厂。如今大家都在建。但我告诉你：别建了。"

> "升级了工具，却保留了 2013 年的思维模型。这个陷阱感觉起来并不像陷阱，因为代码确实能跑通。"

> "代码产物的形态彻底变了。相同的能力。更容易阅读。更容易维护。灵活得多，因为其行为存在于你可以用大白话随时编辑的指令中，而不是冻结在你写代码那一天的死板逻辑里。"

> "OpenClaw 是一辆你必须自带扳手才能开的法拉利。模型是引擎，而不是整辆车。"

> "今天的 10 万美元 Token，明天 1 万，后年 1000，2028 年底 100 美元——100 个有本事的创始人里会有 100 个答应这笔交易。"

> "写代码最少的工程师，往往是构建出最多东西的那个人。"

## Token 最大化（Tokenmaxxing）：2026 年活在 2028 年

- 准入门槛：你必须愿意在 Token 上砸钱
- **Peter Steinberger 每年花 ~100 万美元 Token**（OpenClaw 作者）
- **OpenAI 给每家 YC 公司 200 万美元无上限的 SAFE Token 额度**
- 99.99% 的组织被挡在门外，因为他们在为**价格正在暴跌的资源**斤斤计较

> 1980s 软件开发最大的浪费是"程序员时间"；2026 年最大的浪费是"不舍得用 Token"。

## OpenClaw / GStack / GBrain 关系

- **GStack**（10.5 万 Star，GitHub Top 100）：Garry 与 agent 协同编程的开源体系
- **GBrain**：8 层架构的 AI 第二大脑（另一个 1.6w Star 项目）
- **OpenClaw**（Peter Steinberger）：Garry 称之为"最喜欢的智能体 harness"，但**"你必须自带扳手才能开的法拉利"**

三者关系：GStack 是工作方法 + skill pack 体系；GBrain 是知识基础设施；OpenClaw 是底层 harness。

## 我的判断（编译者注）

1. **这文章和 [[Claude-Code负责人谈AI原生工程组织]] 互为镜像**：
   - 那篇是 Anthropic 的工程负责人讲组织侧瓶颈迁移
   - 这篇是 YC 总裁讲工程师侧的范式迁移
   - **合起来看**：AI-native 团队不只是"组织要变"，连"写代码这件事本身"都要变

2. **"Skill pack" 是范式的真正可操作单元**：
   - 之前 [[从Prompt-Context到Harness]] 提出 Harness 是 L2→L3 内部平台
   - 本文说 skill pack 是 agent 工程时代的"栈/堆/寄存器"
   - **两者结合**：内部平台 = harness + skill pack 库 + resolver + 评估机制

3. **"测试 Markdown" 这一步是当前最缺的实践**：
   - 大多数团队有"测试代码"但没"测试 Markdown"
   - 没有 LLM 评估 + 集成测试的 skill pack 不可靠
   - 这就是 [[任务类型到验证模板]] 应该补的一个新类型：**"知识/Markdown/Skill 验证"**

4. **"审计委员会"陷阱在 Seetong 这种存量代码项目里也常见**：
   - 看看我们有多少 sanitizers / validators / 重试逻辑是在不信任模型
   - 哪些是真必要、哪些是"富士康工厂的护栏"
   - 反思 2026 年的工程组织可以更激进一些

5. **"Tokenmaxxing" 不是花钱本身，是花钱的复利**：
   - 不是"用得多就赢"，是"今天用得多 = 提前 2-3 年 = 复利差距"
   - 我们 Seetong 团队的 token 预算分配也值得重新看

## 适合关联的主题

- AI 时代编程范式
- Markdown as Code / Prompt as Code
- Skill 设计 / Skill pack
- Harness 建设
- Agent 评估 / LLM Evaluation
- 富士康 vs Esalen（控制 vs 自由）
- Token 经济 / 推理预算

## 关键人物

- **Garry Tan**：Y Combinator 总裁
- **Peter Steinberger**：OpenClaw / GBrain 作者
- **Garry's List 团队**：本次案例主角（54 万行 Rails 代码）

## 行动建议

- [ ] 盘点自家代码库"审计委员会"占比：sanitizers / validators / 重试循环 / 怀疑与核对代码
- [ ] 找 1 个常用任务做 skill pack 化（Markdown + 极薄代码 + 单元测试 + LLM 评估 + resolver）
- [ ] 评估"测试 Markdown"能力的现状：是工具缺失、流程缺失、还是文化缺失
- [ ] 重新审视 token 预算分配：是不是"为正在暴跌的资源斤斤计较"
- [ ] 看看 OpenClaw / GStack / GBrain 是否能直接复用一个 skill pack 解决某个老问题
