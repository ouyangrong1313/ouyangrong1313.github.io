---
title: Claude Code 之父：「品味」不是人类护城河；当工程师不再写代码，招聘看什么？
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI行业战略, #主题/Anthropic, #节点/Claude-Code起源, #节点/写Loops范式, #节点/抽象层级提升, #节点/Generalist黄金时代, #节点/MTS文化, #节点/少招人多给Tokens, #节点/品味被模型侵蚀, #节点/价值观护城河, #场景/编译长文, #场景/行业分析, #手法/访谈实录]
nodes: [Claude-Code起源, 写Loops范式, 抽象层级提升, Generalist黄金时代, MTS文化, 少招人多给Tokens, 品味被模型侵蚀, 价值观护城河]
links: [[Claude-Code作者Boris-我已经不写prompt了我写loop]], [[买了一样的AI为什么别家的比你的强]], [[Anthropic万字长文三个判断和一个阳谋]], [[AI-Coding的顿悟时刻]]
date: 2026-06-08
source: 微信公众号 / 机器之心（编译自 Boris Cherny 访谈）
---

# Claude Code 之父：「品味」不是人类护城河；当工程师不再写代码，招聘看什么？

- 原文链接：https://mp.weixin.qq.com/s/7xojGo-W7COYmWP3mxghOA
- 原始来源：机器之心对 Boris Cherny（Claude Code 创始团队成员）访谈
- 来源：微信公众号 / 机器之心
- 发布时间：2026-06-07 17:00
- 获取时间：2026-06-08

## 核心结论（一句话）

> **Claude Code 是 Labs Team 的"意外产物"，但真正让其变强的是底层模型；Boris 已半年没写代码、卸了 IDE、同时跑 5-10 个 Claude 实例；他的工作变成"写 Loops"；招聘看 Generalist / Builder；给创始人的建议是"少招人，多给 tokens"；最后的护城河不是品味，是"价值观"。**

## 分类提炼
- 场景：AI Coding 范式 / Anthropic 战略 / 组织方法论
- 标签：#主题/AI-Coding #主题/Anthropic #节点/写Loops范式 #节点/价值观护城河
- 类型：访谈实录 / 战略洞察 / 行业分析

## 知识节点（8 个独立概念）

- **Claude-Code起源**：2024 年底 Labs Team 探索未来产品形态的"意外产物"；最初只完成 10-20% 工作；"不是一开始就规划好的核心产品"
- **写Loops范式**：Boris 半年没写代码，去年 11 月卸载 IDE；不再直接 Prompt Claude，运行 5-10 个 Claude 实例；"我的工作已经变成写 Loops"
- **抽象层级提升**：编程史 = 抽象层级持续提升史（穿孔卡 → 汇编 → Fortran → Java → Python → 写 Loops）；每一次抽象提升都有人说"这不是真正的编程"
- **Generalist黄金时代**：分工瓦解，每个人都是 Builder；AI 降低跨领域迁移成本；"我们正在进入一个属于 Generalist 的黄金时代"
- **MTS文化**：Member of Technical Staff（Meta 学来的去层级化文化）；避免 deference bias；用想法本身竞争，不用资历
- **少招人多给Tokens**：给创始人的反直觉建议；每个项目故意少 50% 人头 + 大量 tokens；upfront cost 升 / ongoing cost 降；pre-compiling 类比
- **品味被模型侵蚀**：Boris 自己函数式编程执念被模型证明是错的；现在几百个 Claude 跑产品探索，20% 想法是好的；等下一个模型会更多
- **价值观护城河**：人类最后剩下的不是品味是"价值观"——"如何成为好的存在"，跟教孩子是同一件事

## 关联图谱

### 上游（基于 / 来自）
- [[Claude-Code作者Boris-我已经不写prompt了我写loop]]：同一作者多次访谈反复强调"写 loop"，本文是更详细的版本
- [[Anthropic万字长文三个判断和一个阳谋]]：同主线，Anthropic 长文的数据 + 本篇访谈的具体实践相互印证

### 下游（应用于 / 验证于）
- [[买了一样的AI为什么别家的比你的强]]：Hiten Shah 的"模型是商品 skill 才是资产"是组织视角；Boris 的"写 Loops"是个人视角
- [[AI-Coding的顿悟时刻]]：工厂模式半年标配 + 未来瓶颈=需求定义+架构设计 = 跟"Generalist 黄金时代"是同一信号

### 同级（横向 / 并列）
- [[54万行代码的顿悟-Markdown才是新编程方式]]：抽象层级持续提升是同一主线
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]：Harness 思想
- [[Claude-Code负责人谈AI原生工程组织]]：Anthropic 的组织方法论

## 正文要点（10 条）

### 一、Claude Code 是"意外产物"

| 维度 | 数据 |
|---|---|
| 起源时间 | 2024 年底 |
| 起源团队 | Labs Team（探索未来产品形态）|
| 最初完成度 | 10-20% 工作 |
| 当前状态 | "完全不是同一个东西" |

> 不是一开始就规划好的核心产品 — 是模型能力外溢 + 市场缺位的"自然产物"。

### 二、为什么 Anthropic 重视 Coding

**不是商业价值**，是 **AI Safety 实验场**：

- **反馈机制清晰**：运行/不运行、通过/不通过、编译成功/失败
- **解空间收敛**：编程 vs 诗歌（无数优秀答案）
- **训练数据海量**：互联网有无穷代码

> Coding / Tool Use / Computer Use 是"研究模型如何与真实世界交互的天然实验环境"。

### 三、Claude Code 变强的核心 = 模型变强

| 模型节点 | 能力提升 |
|---|---|
| Sonnet 4 | 显著 |
| Opus 4 | 更显著 |
| Opus 4.5 | "每一次都直接反映在 Claude Code 表现上" |

> 产品功能是"增量改进"，模型能力是"上限决定者"。

### 四、生产力数据

- 每位工程师产出代码量：**3 倍**（"实际远超"）
- 新工程师上手时间：从数周 → **2 天**
- 关键变化：隐性知识被转移到 Agent 身上

> "Claude Code 提升的并不仅仅是代码生成速度，而是在逐渐压缩组织内部知识传递的成本。"

### 五、抽象层级持续提升（编程史）

```
穿孔卡 → 汇编 → Fortran/Cobol → Java/Python/JS → 写 Loops
```

> "每一次抽象层级的提升，都会有人认为：这已经不是真正的编程了。"

Boris 的工作三段式：
1. IDE + 写代码 + 自动补全
2. 向 Claude 描述需求 → Claude 写 → 人类检查
3. **写自动运行的 Loops → 程序向 Claude 下指令** ← 现在

> **2025 年 11 月，Boris 卸载了 IDE**（已经 30 天没打开）。

### 六、Generalist 黄金时代

- Claude Code 团队最爱：Generalist（通才）
- 分工瓦解：工程师兼用户研究、设计师、PM、数据分析
- Anthropic 设计师也在写代码、财务同事也在写代码
- 关键术语：**Builder**（Satya Nadella 提出）

> 未来最有优势的人，未必是某一个领域最深的专家，而可能是"能够快速跨越不同领域、不断整合资源的人"。

### 七、MTS 文化

**Member of Technical Staff**（Meta 学来的）：

- 优点：用想法本身竞争，不用资历；避免 deference bias
- 缺点：Slack 上不知道对方是设计师 / 工程师 / 经理
- 关键洞察：**经验在 AI 时代不是线性累积，有时甚至是负债**

> 那些有 20-30 年经验的资深工程师，反而要花好几个月"unlearn"。
> 而新毕业的大学生天然就用模型思维去思考。

### 八、少招人，多给 tokens

**给所有创始人的反直觉建议**：

1. **尽量多给 tokens**（黄仁勋类比："买得越多，省得越多"）
2. **每个项目故意少给一点人**（4 个人 → 2 个人 + 大量 tokens）

> 你会发现，他们大概率真的能做到——把能自动化的全自动化，下次再做更快更便宜，**复利效应**。

**经济学解释**：
- 预算从人的工资 → tokens
- upfront cost 升 / ongoing cost 降
- **pre-compiling 类比**：一次脏活累活 → 后面重复执行几乎免费

### 九、品味被模型侵蚀

**Boris 自己的反例**：
- 喜欢函数式编程 / Haskell / Scala
- Claude Code 早期定规矩"不准用 class，只能用 function"
- 周末工程师偷偷提交带 class 的代码，周一被他 reject
- 模型开始写 class → 他看了半天 → "好吧，也许模型是对的"

**未来的品味问题**：
- 现在已有几百个 Claude 跑产品探索
- 目前 20% 想法是好的
- **等下一个模型 + 3-6 个月** → 大部分想法可能都是好的

### 十、价值观是最后护城河

主持人问：人类最终还有什么独特的东西？

Boris 想了一下，说：**价值观**。

> "最终我们要教模型的，和我们教孩子的是同一件事：如何成为一个好的存在。如何做对的事情，而不仅仅是把事情做对。"

## 我的理解

- **"我的工作已经变成写 Loops" 是 2026 年 AI Coding 范式最具体的一句话** — 跟 Boris 自己 6-04 那篇是同一句话的两次表达
- **跟 [[Anthropic万字长文三个判断和一个阳谋]] 同主线** — 快刀青衣拆的"执行力零价格 / 验收能力 / 慢变量"在 Boris 访谈里得到最具体验证
- **"经验是负债" 对 Seetong 团队是个警钟** — Boris 看到资深工程师"花好几个月 unlearn"；需要主动识别哪些"老经验"会被模型挑战
- **"价值观是最后护城河" 是 Hiten Shah 的"skill 战略"在个人层面的延伸** — 模型吞噬技能，最后剩下的是"做对的事情"的判断

## 相关链接

- 原文：https://mp.weixin.qq.com/s/7xojGo-W7COYmWP3mxghOA
- 原始视频：https://www.youtube.com/watch?v=RkQQ7WEor7w&t=1s
- 关联 wiki：
  - [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - Boris 多次访谈反复强调"写 loop"
  - [[买了一样的AI为什么别家的比你的强]] - skill 战略
  - [[Anthropic万字长文三个判断和一个阳谋]] - 同一主线
  - [[AI-Coding的顿悟时刻]] - AI 编程范式转变
  - [[54万行代码的顿悟-Markdown才是新编程方式]] - 抽象层级持续提升
  - [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - Harness 思想
  - [[Claude-Code负责人谈AI原生工程组织]] - Anthropic 的组织方法论
