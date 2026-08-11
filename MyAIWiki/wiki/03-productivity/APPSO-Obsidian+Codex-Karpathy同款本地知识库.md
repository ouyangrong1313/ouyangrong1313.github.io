---
title: 用 Karpathy 思路搭一套本地知识库：Obsidian + Codex 完整搭建指南
category: 03-productivity
tags:
  - 主题/第二大脑
  - 主题/知识管理
  - 主题/个人生产力
  - 主题/AI时代个人定位
  - 主题/APPSO
  - 节点/3层结构
  - 节点/规则层AGENTS
  - 节点/AI持续整理
  - 节点/采访式SOP
  - 节点/RednoteStar
  - 节点/Claudian插件
  - 场景/Obsidian
  - 场景/Codex
nodes: [3层结构素材笔记规则, 规则层AGENTS.md, AI持续整理与自动复盘, 知识库不是收藏夹, 采访式SOP先问两件事, Prompt入职手册, RednoteStar收藏夹AI化, Claudian插件与飞书CLI]
links: [[03-productivity/karpathy-knowledge-system]], [[02-ai-coding/claude-obsidian-second-brain]], [[03-productivity/obsidian-claude-code-os]], [[02-ai-coding/undefinedKi-AI-Second-Brain-10-Step-Guide]], [[02-ai-coding/若飞-用ClaudeCode搭建AI学习系统]], [[03-productivity/2026年了-你的文件管理还停留在新建文件夹吗]]
date: 2026-06-29
source: 微信公众号「APPSO」2026-06-29 编辑团队原创（实操指南）
---

# 用 Karpathy 思路搭一套本地知识库

- 原文链接：https://mp.weixin.qq.com/s/oE0BONuRy3yPzk25zUpkFA
- 作者/出处：APPSO 编辑团队原创
- 发布时间：2026-06-29
- 参考来源：Karpathy LLM Wiki 开源 gist（https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f）

## 核心结论（一句话）

> **本地知识库的 3 层结构（素材层 / 笔记层 / 规则层）+ "AI 持续整理复盘"自动化 = 知识库从"收藏夹"变成"AI 可读的个人档案室"；记忆不再绑定某一个模型，而是沉淀在你自己的系统里。**

### 分类提炼

- 场景：个人知识库 / 第二大脑 / 本地 AI 协作工作流
- 标签： #主题/第二大脑 #主题/知识管理 #主题/个人生产力 #主题/AI时代个人定位 #主题/APPSO
- 类型：实操指南（提供完整 Prompt + SOP + 工具栈）

## 知识节点（8 个独立概念）

- **3 层结构（素材/笔记/规则）**：素材层只读不改、笔记层 AI 提炼+互链、规则层 AGENTS.md"入职手册"——对应主人 raw / wiki / log 三层架构
- **规则层 AGENTS.md**：跨模型可移植的关键层；主人换对话、换模型时，照着 AGENTS.md 就能接手
- **AI 持续整理 + 复盘 + 沉淀**：知识库不是"搭完就完事"，而是"会自我复盘、持续进化的系统"；每周一扫描脚本初稿→终稿差异，提炼规律
- **知识库不是收藏夹**：核心反直觉——资料多 ≠ 找到；问题不在资料量，在"AI 读没读懂你"
- **采访式 SOP（先问两件事）**：动手建文件前必须先问 ① 存哪里 ② 最想要什么；7 个核心方向选项（工作流/学习/健康/财务/项目/人际/灵感），可多选
- **Prompt 入职手册（完整模板）**："你是我的个人知识库架构师..." 完整 3 段 Prompt——3 层结构说明 + 7 个选项 + 工作方式 5 条纪律（一次只问一个 / 答一题立刻写文件 / 冲突标出来 / 不编造 / "体检"功能）
- **RednoteStar 收藏夹 AI 化**：自建 Skill 读小红书收藏夹→结构化笔记；让"以后再看"变成"可被 AI 调用的灵感库"
- **Claudian 插件 + 飞书 CLI**：Obsidian 内直接调 Codex / Claude；飞书开发者平台接入 CLI，发链接就能读云文档

## 关联图谱

### 上游（基于 / 来自）
- Karpathy LLM Wiki 开源 gist（核心思想来源）
- APPSO 编辑团队实操经验

### 下游（应用于 / 验证于）
- **主人已有**：`~/.openclaw/workspace`（MEMORY.md + SOUL.md + AGENTS.md + skills/ + knowledge/）—— 已是完整 3 层 + 规则层
- **主人可借鉴**：每周一自动复盘（扫描初稿→终稿差异）→ 主人 "writing-preference 沉淀脚本"
- **Seetong 团队可借鉴**：4G IPC 体验文档化（素材层）+ 反馈/工单自动归类（笔记层）+ 排班/SOP 规则文件（规则层）

### 同级（横向 / 并列）
- [[03-productivity/karpathy-knowledge-system]] - Karpathy 原始思路（原理 + 主线）
- [[02-ai-coding/claude-obsidian-second-brain]] - 7200 Star 项目实践（工程实现视角）
- [[03-productivity/obsidian-claude-code-os]] - Obsidian + Claude Code 工作流
- [[02-ai-coding/undefinedKi-AI-Second-Brain-10-Step-Guide]] - Ki 的 10 步指南（同主线"第二大脑"）
- [[02-ai-coding/若飞-用ClaudeCode搭建AI学习系统]] - 若飞的 AI 学习系统
- [[03-productivity/2026年了-你的文件管理还停留在新建文件夹吗]] - 文件管理完全指南

### 正文要点（5 条）

1. **知识库 ≠ 收藏夹**：资料多 ≠ 找到；**核心问题是"AI 读没读懂你"**——只有让 AI 真正了解创作者习惯、节奏、表达、目标，才能让过去积累的素材持续参与未来
2. **3 层结构是核心方法论**：素材层（只读不改）/ 笔记层（AI 提炼 + 互链）/ 规则层（AGENTS.md 跨模型可移植）
3. **3 个最明显变化**：① 收藏夹能用了（RednoteStar）② 不用反复解释自己（AI 持续学习你）③ 换模型记忆不消失（资料全在本地）
4. **自动复盘机制**：每周一早上扫描脚本初稿→终稿差异，提炼写作规律更新到知识库；定期"体检"扫断链/重复/过时
5. **关键反直觉**：知识库真正开始发挥作用，**不是在搭完那一刻，是在后面反复使用、整理和复盘的时候**——搭完只是起点

### 6 个对 Seetong 团队可借鉴动作

1. **Seetong 的 3 层结构体检**：现在 Seetong 后台是否有素材层（埋点/Logan/反馈原始数据）+ 笔记层（神策分析报告 / 反馈分诊产物）+ 规则层（TAPD SOP / 排班规则）？哪一层最缺？
2. **每周一自动复盘脚本**：把 APPSO 的"周一扫描初稿→终稿差异"思路套到 Seetong——每周一扫"上周反馈分诊 vs 实际处理结果差异"→ 沉淀到 `seetong-feedback-triage/SKILL.md` 的"已知高频问题"区
3. **AGENTS.md 跨模型/跨人迁移**：让 Seetong 客服 SOP、研发 SOP 不绑定某一台机器/某一个人；新客服入职照着 AGENTS.md 就能接手
4. **"先问两件事" 防止一上来就建文件夹**：Seetong 任何新项目启动前，主人先问 ① 数据放哪个仓库 ② 这次最想要解决什么（4 选 1：稳定性 / 体验 / 效率 / 商业化）
5. **不编造 / 冲突标出来** 两条纪律：从今天起，所有 Seetong 知识库更新，AI 看到矛盾就停下来问主人，不擅自覆盖
6. **"体检" 触发词机制**：主人说"Seetong 知识库体检"→ 自动化扫过时 / 矛盾 / 孤立内容，10 分钟出清单（参考 `seetong-knowledge-lint` 已有工具）

### 备注与限制

- 本文是 APPSO 原创实操指南（不是编译），提供完整 Prompt + SOP + 工具栈
- 与 [[03-productivity/karpathy-knowledge-system]] 区别：本文是产品化模板（完整 Prompt + 安装步骤 + 自动复盘脚本设计），karpathy-knowledge-system 是原理/思路
- 与 [[02-ai-coding/claude-obsidian-second-brain]] 区别：后者是 7200 Star 开源项目（工程实现视角），本文是媒体视角（产品化方法论）
- **不适用**：纯云端聊天记录当知识库用（换模型 = 记忆清零）、"先建文件夹再问做什么"（结构错配风险）
- **未展开**：Claudian 插件具体配置细节 / 飞书 CLI 具体接入步骤（APPSO 认为简单到不需要展开）

### 相关链接

- 原文链接：https://mp.weixin.qq.com/s/oE0BONuRy3yPzk25zUpkFA
- Karpathy LLM Wiki gist：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- APPSO 公众号历史文章：见历次推送
- 同主线：[[03-productivity/karpathy-knowledge-system]] [[02-ai-coding/claude-obsidian-second-brain]] [[03-productivity/obsidian-claude-code-os]] [[02-ai-coding/undefinedKi-AI-Second-Brain-10-Step-Guide]]
