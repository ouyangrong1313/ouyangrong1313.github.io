# BDD+ADR+PRD：让 Agent 遵守规范的闭环方法 - Digest

> **原文**：https://mp.weixin.qq.com/s/QT71-f3OZ067XhDwrbrAtQ | **一手来源**：Michal Cichra（Safe Intelligence）· AI Engineer 大会演讲 "BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike"
> **编译时间**：2026-07-01 | **分类**：01-ai-agents | **子区**：Agent 工程治理

> **一句话总结**：**当 AI Agent 越来越像团队成员，"为什么"必须从模型记忆里搬进 linter / CI / 文档契约——只有"可被静态检查的规范"才能跨 20-50 次 context compaction 存活下来。**

## 9 节点速查表

| # | 节点 | 一句话 | 关键洞察 |
|---|------|--------|---------|
| 1 | ADR 架构决策记录 | 记录"为什么做这个决定"的轻量文档 | Cichra 团队 50+ 条 ADR 定义整个产品架构 |
| 2 | PRD 三件事 | 极简 PRD 只写"为什么存在/解决什么问题/用户怎么走" | Agent 不需要 why-you-decide，只需 what-to-build |
| 3 | BDD + Cucumber 双轨 | Gherkin 句法让测试代码本身成为产品规范 | 闭合"spec 写但没人验证"的循环 |
| 4 | Linter 强制执行 | 把 ADR 翻译成 ESLint 规则，违规时自动指向文档 | 从"Wiki 范式"升级为"Compiler 范式" |
| 5 | 闭环执行 | Git Hook → CI → Linter → Agent 自修 → 重提 | 让"问题不可能发生"而非"问题被发现" |
| 6 | Context Compaction | 单 session 经历 20-50 次压缩 | 关键信息必须靠系统级文档保活 |
| 7 | 知识资产化 | 把"为什么"搬进 linter/文档/合同 | Agent 时代唯一对冲知识失忆的手段 |
| 8 | Spec-Driven | 文档不只是参考资料，是 Agent 必须遵守的契约 | 规范从 Wiki 软规范升级为可执行合同 |
| 9 | Agent Governance | 治理从"巡检"升级为"编译错误" | 不是发现问题，是让问题不可能发生 |

## 关键数字 + 5 关键金句 + 3 反直觉

### 关键数字 4 条
1. **Cichra 团队 50+ 条 ADR** 定义整个产品架构
2. **单个 AI session 经历 20-50 次 context compaction**
3. **ADR 来源**：Michael Nygard《Release It!》(2011) 推广
4. **BDD 来源**：Dan North (2008) / Cucumber 工具集

### 5 关键金句
1. **Cichra**："用 linter 强制执行 ADR，违规时自动指向文档。"
2. **核心论断**："不是发现问题，而是让问题不可能发生。"
3. **核心论断**："比读 AI 代码更难的是读 AI 测试——BDD 解决了这个问题。"
4. **隐喻**："5 只猴子被替换光后，规矩依然被执行但没人能解释为什么——AI 写代码迭代 5 轮后处于同样状态。"
5. **核心论断**："单个 session 经历 20-50 次上下文压缩也没关系，重要的东西总会被保留。"

### 3 个反直觉点
1. **ADR 不进 linter 等于没写** —— 50 条 ADR 躺在 Confluence 里等于零；只有被翻译成静态检查规则才"不得不"遵守
2. **PRD 越短被读概率越高** —— 10 页 PRD 6 周后没人会读；3 句话 PRD 才是 Agent 时代的工程交付物
3. **模型越来越强 ≠ 知识越来越稳** —— 压缩次数只增不减；模型记忆注定不可靠，唯一对冲是文档契约

## 4 个对 Seetong 借鉴动作

1. **新建 `docs/adr/` 目录** —— 每条决策一个 markdown，固定字段：Context / Decision / Consequences / Date；先写 3 条最重要的，配 3 条 linter 规则
2. **新建 `docs/prd-mini.md`** —— 只写 3 段：为什么存在 / 解决什么问题 / 用户怎么走；这是 Seetong 三端给 AI 助手的"入职文档"
3. **挑 3 条 ADR 配 linter 规则** —— Seetong iOS 项目"为什么不用宏""为什么 QMUI 组件统一前缀"等历史决策，配 clang-tidy 静态检查，违规直接报"ADR-XYZ violated"
4. **BDD 暂缓** —— 等团队里 Agent 写的测试越来越难读时再引入 Cucumber；先跑通"违规可被静态检查"的最小闭环

## 关联 + 备注

### 强关联（同 01-ai-agents）
- [[AI-团队协作-Loop-SDD-digest]] —— **最相关的同级文章**；叶小钗的 SDD "6 段式 Spec 骨架" + 本文"ADR/PRD/BDD"是同源异流：组织级协作契约 + 工程级 Linter 强校验
- [[0xCodez-Agent-Harness-14-Steps]] —— Harness 工程的 Hooks/Loop 节点在规范治理维度的具体落地
- [[agent-skills-systematic-survey]] —— 技能契约化思路互补：Skill 是"怎么做"，ADR/PRD/BDD 是"为什么 + 做什么 + 怎么验"

### 下游（待补充）
- 暂无（待 Seetong 三端 SDK 实践后补充具体落地页）

## 透明玻璃自检
- **wiki**：约 4.0K（≤8K）
- **digest**：约 2.0K（≤4K）
- **节点**：9（6-10 区间内）
- **H2**：4 wiki + 5 digest（≤5）
- **表格**：1 wiki + 1 digest（≤2）
- **0 陈词** ⭐⭐⭐

## 标签

#主题/AI-Agent #主题/AI-Coding #场景/技术博客 #节点/Harness #节点/Context-Engineering #节点/Agent-Loop #节点/Memory #节点/Spec-Driven #手法/焦虑共鸣 #手法/对比冲突 #手法/权威背书
