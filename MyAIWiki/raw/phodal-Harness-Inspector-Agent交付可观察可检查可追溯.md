# Harness Inspector：让 Agent 交付过程可观察、可检查、可追溯

- 原文链接：https://mp.weixin.qq.com/s/1IkDdhFhpJQy3a9ABDuMsQ
- 来源：微信公众号「phodal」；作者：Phodal；获取时间：2026-08-17
- 关联项目：https://github.com/QoderAI/better-harness
- 原文清洗：保留正文、链接与代码，移除页面导航、图片和交互元素。

## 正文

Better Harness 正在尝试从真实 Agent 会话识别重复工作路径，再判断哪些经验可沉淀为可复用的 SKILL。作者认为，这远比分析一段 Session 复杂：软件开发任务从需求或用户故事开始，经理解、上下文探索、代码修改与验证，最后才成为可评审的代码贡献。只看 Session，能知道 Agent 做了什么，却难知道行为为何发生，以及哪些行为进入最终交付。

在项目目录执行：

```bash
npx @qoder-ai/better-harness inspector
```

可生成本地、只读的 Harness Inspector 页面，将 Agent Session、文件活动和 Git Commit 置于同一界面。

## 从 Session 到完整交付

Inspector 起初是会话调试工具，用来查看 Agent 的发言、工具调用和文件修改。但作者认为真正需要观察的是：一次软件变更如何从意图出发，经过 Agent 执行，最终形成可进入工程系统的产出；Session 只是中间部分。

一次 Coding Agent 交付包含三个连续但边界不同的对象：

- **意图（Intent）**：用户需求、Issue、Spec 或架构约束。
- **过程（Process）**：Session 中的搜索、读取、修改与验证。
- **产出（Output）**：交付到工程系统的结果，当前最清晰锚点是 Commit。

Story、Session 与 Commit 分别是 Intent、Process、Output 的可观察对象。它们在真实项目中更接近证据图而非直线：一个 Story 可经历多个 Session，一段 Session 也可涉及多个 Commit。

作者提供英文只读公开样本：https://qoderai.github.io/better-harness/inspector。单独看 Session，无法确定活动是否围绕原始需求、哪些修改真正进入仓库；单独看 Commit，也看不到 Agent 如何理解问题、建立上下文与完成验证。把三者放入同一界面后，Story 解释为什么改，Session 展示如何发生，Commit 记录最后留下什么。

## 三种观察方式

Harness Inspector 被定义为面向 Agent 交付过程的本地、只读工作台，用于检查软件变化为什么发生、怎样发生、最终留下什么。

- **Workbench**：查看需求、Session 与 Commit 的关系。它展示已观察到的关系；证据不足时保留为候选或未映射，不自动拼出看似完整的路径。
- **Trace**：展开 Session。它按 Turn 组织用户输入、中间回复、Tool Call 和文件活动，通过时间轴连接事件位置，并折叠连续重复活动。它不尝试还原模型未暴露的思考过程。
- **Replay**：沿已保留事件顺序回看任务展开。审查者可依次查看输入、回复、调用、文件和 Commit。它不重跑工具、不恢复工作区、不继续原 Session；缺少精确时间的内容只保留顺序，不补写过程。

Workbench 看关系，Trace 看结构，Replay 看顺序。三者共同将从需求到提交的 Agent 交付变为可逐层检查的过程。

## 从交付证据到 SKILL 沉淀

作者认为，值得沉淀的不是出现次数最多的 Tool Call。重复读取可能来自上下文不足，命令重试可能只是噪声。真正值得沉淀的，是相似任务中重复出现、并得到最终产出与验证结果支持的工作路径，例如确定修改边界、建立必要上下文、完成修改、执行验证与检查结果的路径。

SKILL 自动沉淀不是把一段 Session 总结成新的 `SKILL.md`，而是从多次真实交付识别稳定模式，再补充适用场景、上下文边界、执行步骤和验证方式。Inspector 的作用是让真实交付先留下边界清晰、可检查的证据，之后才能比较相似任务、形成 Skill 候选，并验证它是否真的改善工作方式。

标签： #主题/AI-Agent #主题/Harness #主题/AI-Coding #节点/交付证据链 #节点/可追溯交付 #节点/Skill-Discovery #场景/公众号长文
