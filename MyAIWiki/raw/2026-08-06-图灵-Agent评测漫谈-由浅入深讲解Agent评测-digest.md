---
title: Agent评测漫谈 —— 由浅入深讲解Agent评测（拆解）
category: 01-ai-agents
tags: [#主题/AI-Agent, #主题/Agent评测, #主题/长程Agent, #主题/Skill评测, #主题/可观测性]
nodes: [Response-Evaluation, Trajectory-Evaluation, 评测搭桥, Rubric二元化, Good-Bad-Case飞轮, Task评测, Evaluation-Harness, 长程评测基础设施]
links: [[腾讯-AI-Agent-Skill-测评方案落地]], [[用Agent评测思路管理AI-Coding-31万行代码重构实践]], [[研发工程化升级-Coding-Agent-AI-Testing与Verification-First]], [[Harness工程AgentLoop]]
date: 2026-08-06
source: 微信公众号「美团技术团队」/ 图灵Agent评测
source_wechat: https://mp.weixin.qq.com/s/gZKWRqznB8sNBFf69fBIvw
---

# Agent评测漫谈 —— 由浅入深讲解Agent评测（拆解）

> 原文：[[Agent评测漫谈-由浅入深讲解Agent评测]]；图灵Agent评测；美团技术团队；2026-08-06。

## 核心观点

1. 评测服务迭代，不是离线榜单；它要回答 Agent 哪里好、哪里不好。
2. 评测对象从答案变成“模型 + 系统 + 工具 + 流程”的任务系统。
3. Trace 是地基；没有观测，就无法还原现场、定位根因和比较版本。
4. Rubric 下钻和二元化，让人人一致、人机一致成为可能。
5. 长程 Agent 需要回放、沙箱、归因、回归和发布门禁组成的评测基础设施。

## 7 个分析角度 / 21 个钩子

### 1. 从答案到行为
- Agent 做对了，为什么还不能算可靠？
- 只看最终答案，会漏掉哪些工程风险？
- 长程 Agent 到底该测“说得好”还是“做成事”？

### 2. 观测与 Trace
- 看不见的问题，为什么几乎无法稳定解决？
- 没有日志时，Agent 的偶然成功意味着什么？
- Trace 是调试附属品，还是评测的地基？

### 3. 指标搭桥
- 模型分数变高，为什么业务指标可能不动？
- 评测体系最重要的不是指标数量，而是解释性。
- 业务、系统、Agent 三层指标如何接起来？

### 4. 人机对齐
- “感觉更好”为什么不能作为迭代证据？
- 一个强标准制定者，为什么可能胜过十个散乱评分者？
- AI 评分要规模化，先要和人评多大程度一致？

### 5. Good/Bad Case
- 评测体系为什么应该被坏案例喂出来？
- 指标从少到多，为什么不靠一开始设计完美？
- Bad Case 暴露边界，Good Case 定义范式。

### 6. 长程 Agent
- Agent 从回答问题变成完成任务后，评测哪里变了？
- Skill 越容易生成，为什么评测越不能靠人工？
- 长程 Agent 的最小评测三元组是什么？

### 7. 评测产品化
- 评测为什么必须接入开发、发布和运营？
- 平台除了给分，还应该告诉你什么？
- 评测从动作变成基础设施，会新增什么能力？

## 关联与边界

- [[腾讯-AI-Agent-Skill-测评方案落地]]：评分器、五维指标、用例基线和 Trace。
- [[用Agent评测思路管理AI-Coding-31万行代码重构实践]]：评测驱动工程改造。
- [[研发工程化升级-Coding-Agent-AI-Testing与Verification-First]]：测试、验证前移和分层信任。
- 边界：正文配图表格未 OCR；案例和数字是作者团队经验，不直接作为跨业务基准。
