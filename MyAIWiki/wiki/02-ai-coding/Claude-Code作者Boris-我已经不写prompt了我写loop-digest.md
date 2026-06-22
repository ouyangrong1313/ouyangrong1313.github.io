# Claude Code 作者 Boris：我已经不写 prompt 了，我写 loop - Digest

- 原文链接：https://mp.weixin.qq.com/s/-Mhg_EEibje5tkWlVazdMA
- 来源：微信公众号 / winkrun
- 原始内容：Boris Chernyshev（Claude Code 作者）30 分钟演讲
- 获取时间：2026-06-04

## 一句话总结

**Boris 已经不写 prompt 了，他写 loop**——Claude Code + loops + Dynamic Workflow 把"写代码"从"对话拿一次结果"变成"养管道"，核心是用 `agent() / parallel() / pipeline()` 三个 API 配合 6 种基本模式（Classify-and-act / Fan-out / Adversarial / Generate-and-filter / Tournament / Loop until done）组合出 2-4 种真实 workflow。

## 关键观点

1. **核心论断**
   - "我的工作是写 loop"——从对话者变成管道养作者
   - 配置：**Claude Code + loops + Dynamic Workflow**

2. **Dynamic Workflow（2026-05-28 上线）**
   - Claude 临场写 harness（JS 文件）而不是用通用模板
   - 每个子 agent：独立上下文 + 可指定模型（Opus/Sonnet/Haiku）+ 隔离级别（worktree/remote）
   - 触发词 `ultracode`；中途打断可恢复

3. **结构性解决三个老毛病**
   - Agentic laziness：长任务做一半就宣布完成
   - Self-preferential bias：验证自己时偏袒
   - Goal drift：多轮后约束悄悄消失
   - **解法**：不同 Claude / 各自上下文 / 目标聚焦 / 状态隔离

4. **核心 API 三件套**
   - `agent()`：生成独立子 agent
   - `parallel()`：**barrier**——扇出后等所有结果回来
   - `pipeline()`：流式——每个元素独立流过（更便宜）
   - **决策标准**：下一步是否必须等全部结果？是 → parallel；否 → pipeline

5. **6 种基本模式**（实战组合 2-4 个）
   - Classify-and-act：分类路由，便宜模型做分类
   - Fan-out-and-synthesize：50 个文件安全审计
   - Adversarial verification：专治 self-preferential bias
   - Generate-and-filter：30 个想法 + rubric 筛
   - Tournament：配对比较淘汰
   - Loop until done：循环 + /goal 硬性标准

6. **真实案例**：Bun 从 Zig 重写到 Rust 用的是"Fan-out → 对抗验证 → loop until done"

7. **8 个避坑点**
   - 别给日常任务上 workflow
   - **必须设 token 预算**——不封顶能烧 5-10 倍
   - 别让同一 agent 既干活又验证
   - 区分 parallel vs pipeline
   - loop 必须配 /goal
   - 不可信内容必须 **quarantine**
   - 排序用 tournament，不用绝对打分
   - 跑通的 workflow 必须保存

8. **旁观者视角**
   - "Boris 不小心把 n8n 整套 UX 哲学说了一遍"
   - "**你不再跑任务，你在养管道**"
   - "但编排层得先稳，再上动态路由，不然会被自己绕死"

## 我的理解

- **这是 Dynamic Workflow 主题的"第 3 篇"**——三篇配套看最完整：
  - [[claude-code-dynamic-workflows]]（6-3 英文官方版）：侧重六种模式 + Prompt 示例
  - [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]（上午 Feisky 版）：侧重判断 + 取舍
  - **本篇（Boris 实战版）**：侧重 API 三件套 + 避坑指南

- **"写 loop 不写 prompt" 是 2026 年最值得记住的范式转变**——跟 [[Claude-Code团队只招聘两类人]] 是同一团队在两个层面的呼应

- **token 预算是真实坑**——`"use 10k tokens"` 必须成习惯

- **quarantine 模式** = 陈春花说的"隔离区"——读和写分离避免 prompt injection

- **"你不再跑任务，你在养管道"** 对 Seetong 团队很有启发——核心问题不是"AI 能不能做 task"，而是"我能不能维护一个长期跑的管道"

## 适合关联的主题

- [[claude-code-dynamic-workflows]]
- [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- [[Claude-Code团队只招聘两类人-会做梦的人+懂底层的人]]
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]
- [[Harness工程AgentLoop]]
- [[HarnessEngineering企业级实战]]
- [[Skills驱动推理新范式]]
- [[陈春花-AI时代管理者重建判断权]]
