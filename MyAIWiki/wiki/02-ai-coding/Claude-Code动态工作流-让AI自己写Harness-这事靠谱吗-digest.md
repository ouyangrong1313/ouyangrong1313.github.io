# Claude Code 动态工作流：让 AI 自己写 Harness，这事靠谱吗 - Digest

- 原文链接：https://mp.weixin.qq.com/s/gSwA5Y2Alyf9fu9mmn-32Q
- 原始博客：https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code
- 来源：微信公众号 / Feisky
- 获取时间：2026-06-04

## 一句话总结

Claude Code 的 **Dynamic Workflows** 把"写 Harness"这件事也交给 Claude 自己——看任务后自动生成确定性 JS 脚本来调度独立子 Agent，绕开单 Agent 的偷懒/自我偏爱/目标漂移三大退化模式。**适合"不知道最优拆分方式"的探索性任务**，常规编程任务用静态工作流或单 Agent 仍更划算。

## 关键观点

1. **单 Agent 三大退化模式**
   - 偷懒：长上下文里 50 个检查只查 20 个
   - 自我偏爱：评判自己天然给好评
   - 目标漂移：上下文压缩有损，需求边缘条件丢失

2. **Dynamic Workflows 的核心**
   - 子 Agent 各自独立干净上下文窗口
   - **确定性 JS 脚本**调度执行顺序和依赖
   - 区别于静态：Claude 现场写脚本而不是用通用模板

3. **六种调度模式**
   - 分类路由、扇出合并、对抗验证、生成过滤、锦标赛、循环到完成
   - 可组合：先扇出 → 每分支对抗验证 → 合并时锦标赛

4. **强项场景**（按价值排序）
   - 大规模迁移和重构（避免交叉污染）
   - 深度验证（事实性声明核实）
   - 排序（锦标赛比绝对评分可靠）
   - 根因分析（不锁定假设，多假设并行验证）
   - 规则遵守（CLAUDE.md 规则的执行验证）

5. **不该用工作流的标准**
   - 能用一句话说清楚要做什么
   - 做完能自己快速验证
   - **大部分常规编程任务不需要**

6. **触发和限制**
   - 触发词 `ultracode` 或 Prompt 里明确要求
   - `/loop` + `/goal` 控制
   - "用 10k token" 限制消耗
   - 按 `s` 保存脚本到 `~/.claude/workflows` 或作为 Skill

7. **哲学判断**：Harness 可能像 prompt engineering 一样是**模型不够强时的中间状态**——下一代模型可能自己就能在内部完成分解和对抗验证

## 我的理解

- 跟 [[Harness不是目的，知识才是护城河]] 是同一判断的两个侧面：工程化重要但不是终局
- **80/20 实战**：日常工作别上动态工作流（成本不划算），只在"知道复杂 + 验证成本高"时用
- **对 MyAIWiki 的启发**：动态工作流可以"保存成静态"——这正是 Skill 沉淀的逻辑
- 跟 [[claude-code-dynamic-workflows]]（6-3 写的英文编译版）配套看，那篇侧重六种模式 + Prompt 示例，本篇侧重 Feisky 的判断和取舍

## 适合关联的主题

- [[claude-code-dynamic-workflows]]
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]]
- [[HarnessEngineering企业级实战]]
- [[Harness工程AgentLoop]]
- [[Claude-Code在大代码库中的最佳实践]]
- [[Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]
- [[AI-Coding的顿悟时刻]]
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]
