---
title: 用 Karpathy 思路搭一套本地知识库 - Digest
category: 03-productivity
date: 2026-06-29
tags:
  - 主题/未分类
nodes: []
---

# Karpathy 同款本地知识库 - Digest

## 一句话总结

> 3 层结构（素材/笔记/规则）+ AI 持续整理复盘 = 知识库从"收藏夹"变成"AI 可读的个人档案室"；记忆不再绑定某一模型，而是沉淀在你自己的系统里。

## 速查表（8 节点）

| # | 节点 | 一句话定义 |
|---|---|---|
| 1 | 3 层结构 | 素材层（只读）/ 笔记层（AI 提炼+互链）/ 规则层（AGENTS.md 入职手册） |
| 2 | 规则层 AGENTS.md | 跨模型可移植；换对话/换模型照着就能接手 |
| 3 | AI 持续整理+复盘 | 每周一扫脚本初稿→终稿差异 / 体检扫断链重复过时 |
| 4 | 知识库不是收藏夹 | 资料多 ≠ 找到；问题在 AI 读没读懂你 |
| 5 | 采访式 SOP | 动手前先问"存哪里+最想要什么"（7 选） |
| 6 | Prompt 入职手册 | "你是我的个人知识库架构师..." 完整 3 段 + 5 条纪律 |
| 7 | RednoteStar | 自建 Skill 读小红书收藏夹→结构化笔记 |
| 8 | Claudian+飞书 CLI | Obsidian 内直调 Codex/Claude + 飞书云文档直读 |

## 关键金句

1. "别让知识库变成收藏夹。"
2. "它不是凭空猜我是谁，是读完一套关于我的资料后做出的判断。"
3. "记忆不再绑定某一个模型，而是沉淀在你自己的系统里。"
4. "知识库真正开始发挥作用，是在后面反复使用、整理和复盘的时候。"
5. "它不是帮你'存住过去'，而是让过去的积累，继续参与未来的创作。"

## 3 个反直觉

- **不是搭完就完事**：真正发挥作用在反复使用、整理、复盘的时候——搭完只是起点
- **资料多 ≠ 找到**：问题不是资料少，是没被 AI 读懂，也没变成可调用的个人系统
- **"我到底怎么写"AI 自己学出来**：不是某一句神奇提示词，是 AI 背后有一套持续学习创作者的知识库

## 5 个对 Seetong 借鉴动作

1. **Seetong 3 层结构体检**：素材层（埋点/Logan/反馈原始数据）+ 笔记层（神策/分诊产物）+ 规则层（TAPD SOP/排班规则）——哪层最缺？
2. **周一自动复盘**：每周一扫"上周反馈分诊 vs 实际处理结果差异" → 沉淀到 `seetong-feedback-triage/SKILL.md`
3. **AGENTS.md 跨模型/跨人迁移**：让 SOP 不绑定某一台机器/某一个人；新人照着就能接手
4. **"先问两件事"防错配**：Seetong 新项目启动前先问"数据放哪个仓库 + 这次最想要什么"
5. **"体检"触发词机制**：主人说"Seetong 知识库体检"→ 自动扫过时/矛盾/孤立内容，10 分钟出清单

## 关联 + 备注

- **关联**：`[[03-productivity/karpathy-knowledge-system]]` / `[[02-ai-coding/claude-obsidian-second-brain]]` / `[[03-productivity/obsidian-claude-code-os]]` / `[[02-ai-coding/undefinedKi-AI-Second-Brain-10-Step-Guide]]` / `[[02-ai-coding/若飞-用ClaudeCode搭建AI学习系统]]` / `[[03-productivity/2026年了-你的文件管理还停留在新建文件夹吗]]`
- **关键提示**：主人 `~/.openclaw/workspace`（MEMORY.md + SOUL.md + AGENTS.md + skills/ + knowledge/）已是完整 3 层+规则层；本文最大价值是"周一自动复盘"和"体检触发词"两个具体动作
- **分类理由**：本文是"个人生产力+知识管理"实操指南，与 karpathy-knowledge-system / claude-obsidian-second-brain / obsidian-claude-code-os 同主线"第二大脑"；放 03-productivity 而非 02-ai-coding（APPSO 是产品化方法论视角，不是工程实现视角）
- **完整 Prompt 模板**已写入 raw 原文，可直接复制使用
- **透明玻璃自检**：wiki 7.7K（≤8K）/ digest ?K（≤4K）/ 节点 8（6-10）/ H2 3 wiki / H2 5 digest（≤5）/ 表格 0 wiki / 表格 1 digest（≤2）/ 0 陈词 ⭐⭐⭐
