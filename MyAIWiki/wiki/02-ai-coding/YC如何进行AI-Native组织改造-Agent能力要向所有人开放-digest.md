# YC 如何进行 AI-Native 组织改造 - Digest

- 原文链接：https://mp.weixin.qq.com/s/dcpsur_udGz6tLW-yARU8w
- 原文：[[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]]
- 抓取时间：2026-06-03

## 一句话总结

YC 合伙人 Pete Koomen 主导搭建 AI-Native 基础设施，**一年内演化出 350+ 工具的内部注册表 + 全员可见的 Agent 对话 + 每晚自动改进技能的 Dream Cycle**。**真正的 AI-Native ≠ Copilot** —— AI 必须作为组织运转的建设层（building layer），系统性记录所有 artifacts 作为 Agent 可学习原材料；前提是 **Egalitarian**（AI 能力向每人开放）+ **Trust by default**（默认信任）。

## 关键观点

1. **真正的 AI-Native ≠ Copilot**：Copilot 是 2023-2024 做法，AI 辅助具体任务，流程/决策/知识仍在人头脑里；AI-Native 是把 AI 作为**整个组织运转的建设层**
2. **从财务 Agent 开始 + Jared 偷偷推 PR 开放生产数据库完整只读权限**——"真正阻碍的不是技术，是安全过度担忧"
3. **杰文斯悖论应用**："当某种资源使用效率提高时，人们反而消耗更多"——**成本下降带来的不是需求减少，而是需求爆发**
4. **数据反规范化**：从 schema+join 变成针对 Agent 优化的大宽表（类似 BigTable）
5. **YC Agent 核心架构**（极简）：Agent 循环 + 工具注册表（Resolver） + 模型路由器
6. **工具注册表 = Resolver**："告诉 Agent '我能做什么'"；YC 工具从 20 → **350+**
7. **Skill 是对工具的更高层封装**——可复用 + 有明确语义
8. **两个元技能（meta skill）**：
   - **Skillify it**：做完某事说"skillify it" → Agent 自动封装注册
   - **check resolvable**：每次 Skillify 后调用，检查 **DRY + MECE**
9. **"Agentic 系统的基础原语"**："感觉就像 Unix 早期发现栈和堆一样"
10. **Dream Cycle**：每晚通用 Agent 读取当天所有对话，识别"本可以做得更好的地方"，次日自动优化相关技能
11. **"两句话描述"具体例子**：写提示词 → 使用产生 artifacts → Dream Cycle 改进 → **效果超过任何单个人**
12. **超级组织诞生路径**：写提示词 → 使用 → artifacts → metaprompt → Dream Cycle → 超越个人 → 整个组织这样 = 超级组织
13. **同类独立出现**：OpenClaw Dream Cycle / Karpathy auto-research / Codex SLG
14. **所有 Agent 对话对 YC 全员可见**（广播到内部 Slack）：
    - **知识传播**：看别人用法学习
    - **社会性控制**：用高信任 + 操作可见代替严格技术控制
    - **降低新员工门槛**：六个月上手 → 阅读对话快速了解
15. **AI 超级组织两个文化特质**（必要条件）：
    - **Egalitarian**（平等主义）：AI 能力必须向组织中每个人开放
    - **Trust by default**（默认信任）：上下文和数据不锁在权限层级
16. **Token 成本**：$10K-100K/年
17. **时间跳跃窗口**："现在有一个一次性的时间跳跃窗口，你可以跳过所有现存的巨头、所有 Fortune 500"
18. **Horseless Carriages 批评**：现在的 AI 软件多数仍是"在确定性软件里嵌一小块 AI"——**Gmail AI 写邮件 prompt context 被开发者锁死**
19. **正确方向**："Agent 包裹确定性工具（agent wrapping deterministic tools），而不是确定性软件包裹 AI"
20. **Chat 作为 UI**："Chat 最接近人类语言，人类语言最接近思维的表达"——**Chat 是清晰智能的最近跳板**
21. **just-in-time software**：Agent 当场生成单页 JS 用完即弃
22. **极简偏好**：Pi（极简开源 Agent harness）"代码量极小，但你可以用 Pi 修改和扩展 Pi 自身"
23. **AI 最大的潜力**：**将软件的控制权从开发者转移到用户手中**

## 关键人物一致关系（重要发现）

文中的 **Gary** 就是 [[54万行代码的顿悟]] 的作者 **Garry Tan**（YC 总裁）。文里提到的 **Gbrain** 就是 [[54万行代码的顿悟]] 里的 **GBrain**（8 层 AI 第二大脑）。**这是同一个人/同一段时间的不同侧面表达。**

**数据交叉印证**：
- [[54万行代码的顿悟]]：54 万行 Rails 代码（Gary's List）
- 本文："一月到二月我用 Rails 写了约五十万行代码"
- **完全吻合** → 同一项目的两次叙述

## 我的理解

- **本文是 [[54万行代码的顿悟]] 的官方补完**：54 万行顿悟讲"工程师个人范式"，本文讲"组织层面"（Egalitarian + Trust by default + 工具/Skill 注册表 + Dream Cycle）。**合起来 = 工程师个人 + 团队流程 + 组织结构** 三层完整的 AI-native 蓝图
- **"偷偷推 PR 开放生产数据库"是 YC 的"卢德分子"故事**：在 AI 时代，"违规"往往就是创新
- **"Skill + Skillify + check resolvable" 是超级具体的可操作新方法论**：之前讲 "Skillify it" 循环，本文补完 **check resolvable + DRY + MECE**。**新组合**：Skillify 完必 check resolvable，保证 skill 库健康
- **"Dream Cycle" 是 AI-Native 组织的关键基础设施**：我们的 MyAIWiki 知识库**就是缺这个机制** —— 可以考虑加一个 weekly dream cycle，让 AI 读本周新加内容自动归并、提炼、改进
- **"Egalitarian + Trust by default"是文化层面的硬约束**：Seetong 团队反思：AI 工具谁先用？决策权谁有？信息是否锁在层级里？
- **"Agent 包裹确定性工具"是 AI 软件设计原则**：验证方法 —— 问"我们这个产品，是让用户表达意图，还是让用户按按钮？"
- **"Chat 是清晰智能的最近跳板" + "just-in-time software"** 对 Seetong 启示：用户问"最近 24 小时 XX 设备异常告警"，Agent 现场生成针对性页面
- **"现在有时间跳跃窗口"是最大商业启示**：$100K 投入 → 2028 年能力；不投入 → 永远在后面

## 关键术语

- **AI-Native 组织**（vs Copilot 用法）
- **建设层（building layer）**
- **Egalitarian**（平等主义）
- **Trust by default**（默认信任）
- **杰文斯悖论应用**
- **数据反规范化**（denormalize）
- **工具注册表 / Resolver**
- **Skill 抽象层**
- **Skillify 元技能**
- **check resolvable 元技能**（DRY + MECE）
- **Dream Cycle**
- **两句话描述（原子能力）**
- **shared organizational brain**
- **社会性控制**（vs 严格技术控制）
- **时间跳跃窗口**
- **Horseless Carriages 批评**
- **Agent 包裹确定性工具**
- **just-in-time software**
- **极小起点 + Agent 按需扩展**
