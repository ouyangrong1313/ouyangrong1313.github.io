# Claude Code 团队 5 条工作原则 - Digest

- 原文链接：https://mp.weixin.qq.com/s/iBELIhdHf44aWKs0Z-Iudg
- 原文：[[Claude-Code团队5条工作原则-Fiona-Fung分享]]
- 抓取时间：2026-06-03
- 原始作者：Fiona Fung（Anthropic Claude Code 团队工程总监）
- 转载方：卡兹克

## 一句话总结

**AI 时代软件工程的前提变了：写代码不再是瓶颈。瓶颈没有消失，只是转移了 —— 转移到验证、代码评审、安全。** Claude Code 团队工程总监 Fiona Fung 分享 5 条工作原则：**JIT 规划 / 自动化肌肉记忆 / Trust but verify / Taste is scarce typing is not / 团队级 harness**。

## 关键观点

1. **核心判断**：**瓶颈没有消失，只是转移了** —— 从"写代码太贵"转移到"验证、代码评审、安全"
2. **过去所有软件工程流程（瀑布/敏捷）本质上是围绕"写代码太贵"展开的**
3. **5 个旧领域正在失效**：规划方式 / 代码所有权 / 代码评审 / 团队构成 / 知识共享
4. **JIT 规划**（Just-In-Time）："在对的时间做恰好足够的规划"。六个月路线图三个月就过时
5. **"代码赢才牛逼"**：让 Claude 把两个方案都做成原型，看实物判断
6. **"Building is cheap, Arguing is expensive"** —— 实物比 PPT 吵高效一万倍
7. **过度规划就是浪费**
8. **自动化肌肉记忆**：每件事追问"能不能自动化"。重点不是这件事，是这个习惯
9. **"几乎所有重复超过 3 次的事情都应该自动化"** —— 自动化成本几乎为零
10. **触发器 hook**（Agent+hook）是新自动化利器，几分钟就能跑起来
11. **"一个一个小的自动化攒起来，会一起长成了一颗苍天大树"**
12. **Trust but verify**（信任但验证）：**Claude 干 60-70% 风格/lint/PR/bug/test**
13. **trust 和 verify 之间的平衡是动态的**（"像打游戏，每个版本答案都不一样"）
14. **人类 review 不可替代**：法律合规 / 信任边界 / 安全敏感代码 / 产品方向 / 品味判断
15. **角色界限模糊化**：PM 在大量写代码，工程师在做设计
16. **人类还是最终决策者，只是不再是写初稿的人**
17. **"Taste is scarce, typing is not"** —— 品味是稀缺资源
18. **招聘看两种人**：有产品 sense 的创意 builder + 有深厚系统背景的工程师
19. **"subtly wrong is still wrong"** —— 微妙的错误仍然是错误
20. **"我根本不在乎你一小时写多少行代码，我在乎的是你选择去做什么，以及你怎么知道它是对的"**
21. **团队原则分两类**：灰色（必须硬性要求）+ 黑色（自己摸索空间）= **团队级 harness**
22. **"人不会主动删除流程，只会在旧流程上叠新流程"** —— 你得主动站出来
23. **Fiona 的 3 个没答案的问题**（重要！）：
    - 还需要单独的 iOS 和 Android 团队吗？
    - 全自动化的 review 能推到多远？
    - 角色越来越模糊时，怎么确保所有角色都对自己的产出有信心？
24. **真正的 AI 原生组织**："从规划方式到知识管理到评审流程到人才结构，每一层都是重新设计过的" —— **不是买 Claude 会员或 API Key**

## 我的理解

- **5 条原则和 [[54万行代码的顿悟]]、[[YC如何进行AI-Native组织改造]] 高度互补**：那两篇偏"组织/范式"层，本文偏"具体实操"层（JIT 规划 / 自动化肌肉记忆 / Trust but verify / 团队 harness）。**三层合并**：范式 → 组织 → 实操 = 完整的 AI-native 蓝图
- **"JIT 规划"是 PR/原型先行 + 文档后补的最强背书**：适用于 Seetong 团队，**别再写长篇设计文档了**，有想法先做原型，能用了再说
- **"Trust but verify" 是 AI 时代 Code Review 的金标准**：可借鉴——**Claude 先干 60-70% 风格/lint/PR/bug/test，人 review 真正需判断处**。立刻可行动：把 Code Review 工具集成到 Seetong 项目的 PR 流程
- **"Taste is scarce, typing is not" 是招聘新标准**：不再是"几年 iOS 经验 / 写过多少个 APP"，而是"**能不能识别该做什么，能不能快速做出原型，能不能判断对错**"
- **"3 个 Fiona 也没答案的问题" 是最重要的部分**：iOS/Android 团队 / 自动化 review 边界 / 模糊角色信心。**Fiona 敢公开"没答案"这一点**比很多 AI 公司都强——我们是不是也敢？
- **"团队级 harness"（灰+黑）是 Seetong 团队可以立刻借鉴的**：灰色 = 硬性要求（不能太多，否则又变回 command and control）；黑色 = 团队自摸索
- **"Pick your noisiest workflow" 是个可立即行动的口号**：让每个团队成员找一件今天重复做的事，花 10 分钟让 Claude Code 自动化。**这是 AI 转型的"最低门槛"行动**
- **Fiona 的 "6 个月前别人问得最多的问题 = 跟不跟得上 review 速度" 是个路标**：6 个月后 Fiona 已经能给出标准答案。**意味着 6 个月前这个问题还是个开放问题**。**现在问 Seetong 团队：我们的"6 个月前没答案、现在可能有答案"的问题是什么？**

## 关键术语

- **JIT 规划**（Just-In-Time）
- **代码赢才牛逼** / **Building is cheap, Arguing is expensive**
- **自动化肌肉记忆**
- **触发器 hook**（Agent+hook）
- **Trust but verify**
- **Taste is scarce, typing is not**
- **subtly wrong is still wrong**
- **团队级 harness**（灰色硬性 + 黑色自摸索）
- **瓶颈转移**（写代码 → 验证/评审/安全）
- **Pick your noisiest workflow**

## 适合关联的主题

- [[Claude-Code负责人谈AI原生工程组织]] — 同主线
- [[54万行代码的顿悟]] — 工程师个人范式
- [[AI-Coding的顿悟时刻]] — 团队流程 + Scrum 反思
- [[YC如何进行AI-Native组织改造]] — YC 内部 AI 改造
- [[Codex配置原则总览]] — Harness / Skill 设计
- [[多Agent使用边界与并行判定]] — 应补 JIT 规划 / Trust but verify / 团队 harness
- [[知识卡片编译模板-长文如何压成raw-digest-wiki三层]] — JIT 规划的另一个样本
- [[任务类型到验证模板]] — 验证流程往前推的具体实施
