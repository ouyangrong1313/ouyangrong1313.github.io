# Claude Code 之父：Boris Cherny 访谈 - Digest

- 原文链接：https://mp.weixin.qq.com/s/7xojGo-W7COYmWP3mxghOA
- 原始来源：机器之心对 Boris Cherny（Claude Code 创始团队成员）访谈
- 来源：微信公众号 / 机器之心
- 发布时间：2026-06-07 17:00
- 获取时间：2026-06-08

## 一句话总结

**Claude Code 是 Labs Team 的"意外产物"，但真正让其变强的是底层模型；Boris 已半年没写代码、卸了 IDE、同时跑 5-10 个 Claude 实例；他的工作变成"写 Loops"；招聘看 Generalist / Builder；给创始人的建议是"少招人，多给 tokens"；最后的护城河不是品味，是"价值观"。**

## 核心观点（5 个）

1. **Claude Code 是意外产物** — 2024 年底 Labs Team 探索未来产品形态；最初只能完成 10-20% 工作；"不是一开始就规划好的核心产品"
2. **编程 = AI Safety 天然实验场** — 反馈机制清晰（运行/不运行、通过/不通过）+ 解空间收敛 + 海量训练数据；Anthropic 重视 Coding 不只是商业价值
3. **Claude Code 变强的核心是模型变强** — Sonnet 4 → Opus 4 → Opus 4.5；产品功能是"增量改进"；整个公司每天用 Claude Code 写代码，反馈循环天然存在
4. **"我的工作已经变成写 Loops"** — Boris 去年 11 月卸载 IDE；不再直接 Prompt Claude；运行 5-10 个 Claude 实例监督；把"与 Claude 沟通"自动化
5. **品味也会被模型侵蚀** — Boris 自己函数式编程执念被模型证明是错的；现在几百个 Claude 跑产品探索；20% 想法是好的，等下一个模型会更多；**人类最后剩下的是"价值观"**

## 7 个分析角度 × 3 个开头钩子

### 角度 1：现象 / 反常识

- 钩子 1：Claude Code 之父已半年没写代码
- 钩子 2："我的 IDE 我卸了" —— 不是表态是真的 30 天没打开
- 钩子 3：为什么编程是 AI Safety 的天然实验场（不是商业价值）

### 角度 2：痛点 / 矛盾

- 钩子 1：为什么新人 2 天上手，公司扩张没拖慢
- 钩子 2：组织隐性知识被转移到 Agent 身上 —— 这是好事还是坏事
- 钩子 3：经验在 AI 时代是资产还是负债

### 角度 3：原因 / 为什么

- 钩子 1：为什么 Anthropic 编程"反馈机制清晰 / 解空间收敛"
- 钩子 2：为什么"写 Loops"比"写代码"高一个抽象层级
- 钩子 3：为什么模型能力跃迁比产品功能更重要

### 角度 4：方法 / 怎么做

- 钩子 1：少招人 = 每个项目故意少 50% 人头
- 钩子 2：多给 tokens = 让人疯狂实验
- 钩子 3：把"与 Claude 沟通"自动化 = 写 Loops / 写 Pipeline

### 角度 5：流程 / 迭代

- 钩子 1：从 IDE → Prompt Claude → 写 Loops，三段抽象层级
- 钩子 2：整个公司每天用 Claude Code，反馈循环 = 日常工作
- 钩子 3：每一次新模型出来，所有人 recalibrate

### 角度 6：类比 / 跨域

- 钩子 1：穿孔卡 → 汇编 → 高级语言 → 写 Loops = 抽象层级持续提升
- 钩子 2：Member of Technical Staff = Meta 学来的去层级化文化（避免 deference bias）
- 钩子 3：黄仁勋"买得越多省得越多" = Boris "tokens 越多越省"

### 角度 7：行动 / 启示

- 钩子 1：你还在 IDE 里写代码吗？想想什么时候可以卸载
- 钩子 2：你的招聘 JD 里"senior/principal"还在吗？想想 MTS
- 钩子 3：你有"品味"执念吗？想想会不会被下一个模型证明是错的

## 我的理解

- **"我的工作已经变成写 Loops" 是 2026 年 AI Coding 范式最具体的一句话**——跟 [[Claude-Code作者Boris-我已经不写prompt了我写loop]] 是同一句话的两次表达，**Boris 在多次访谈中反复强调**——说明这是他从"个人工作流"上升到"团队共识"的真实转变
- **跟 [[买了一样的AI为什么别家的比你的强]] (Hiten Shah) 强呼应** — skill / loop 都是"判断层的具体形态"；Hiten 说"模型是商品 skill 才是资产"，Boris 现身说法"我写 Loops"
- **跟 [[Anthropic万字长文三个判断和一个阳谋]] (快刀青衣) 同主线** — 快刀青衣拆的"执行力零价格 / 验收能力 / 慢变量"在 Boris 访谈里得到最具体验证：**他自己就是案例**
- **"经验是负债" 对 Seetong 团队是个警钟** — Boris 看到资深工程师"花好几个月 unlearn"；张威 / 黄松佳 / 梁添 / 李深生 / 付林青 的"老经验"哪些会被模型挑战？需要主动 unlearn 哪些？
- **"价值观是最后护城河" 是 Hiten Shah 的"skill 战略"在个人层面的延伸** — 模型吞噬技能，最后剩下的是"做对的事情"的判断；这条主线可作为 Seetong 团队 AI 化的北极星
- **"少招人，多给 tokens" 是个反直觉但有数据的建议** — Boris 给出"复利效应"的经济学解释：upfront cost 升高、ongoing cost 大降；pre-compiling 类比很贴切

## 关联文章

- [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - Boris 多次访谈反复强调"写 loop"
- [[买了一样的AI为什么别家的比你的强]] - skill 战略 = 写 Loops 战略
- [[Anthropic万字长文三个判断和一个阳谋]] - 同一主线
- [[AI-Coding的顿悟时刻]] - AI 编程范式转变
- [[54万行代码的顿悟-Markdown才是新编程方式]] - 抽象层级持续提升
