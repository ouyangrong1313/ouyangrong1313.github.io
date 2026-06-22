---
title: 如何使用 AI 打造一个智能、高效、省 Token 的 AI 知识库？LLM-Wiki Skill 设计详解
category: 07-rag-systems
tags: [#主题/AI-Coding, #主题/AI-Agent, #场景/公众号长文, #节点/LLM-Wiki, #节点/Memory, #节点/Skill, #节点/Context-Engineering]
nodes: [LLM-Wiki, 知识节点, 三层存储, grep 查询, 发芽报告, 主题融合, Token 经济, 意图识别绕过, 命令式查询, 图谱关系]
links: [[AI知识库技术演进拆解-从RAG到NotebookLM再到LLM-Wiki]], [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]], [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]], [[hermes-obsidian-llm-wiki-knowledge-base]], [[ai-personal-knowledge-base-problems]]
date: 2026-06-04
source: 微信公众号 / moss
---

# 如何使用 AI 打造一个智能、高效、省 Token 的 AI 知识库？LLM-Wiki Skill 设计详解

- 原文链接：https://mp.weixin.qq.com/s/zw7lNCj00dyaDvl8UaMXDw
- 来源：微信公众号 / moss
- 获取时间：2026-06-04

## 核心结论（一句话）

> **LLM-Wiki Skill 的核心方法论**是：用结构化存储降低输入成本（拆知识节点 + 三层存储），用 grep 命令式查询降低输出成本（绕开意图识别）——让知识库不管存多少内容，输出成本都可控。

## 分类提炼
- 场景：个人知识库 / 团队知识沉淀 / Agent 驱动的第二大脑
- 标签：#主题/AI-Coding #主题/AI-Agent #节点/LLM-Wiki #节点/Memory
- 类型：方法论 / 工程实操 / Skill 设计

## 知识节点

- **LLM-Wiki Skill**：moss 设计的本地 AI 知识库 Skill，能自动消化文章、做每日发芽报告和主题融合
- **知识节点**：从一篇文章中拆分出的独立概念或判断，每条独立可 grep
- **三层存储**：原文 / 知识节点 / 索引文件，三层协同支撑轻量检索
- **grep 查询**：用命令行工具（grep / ripgrep）做结构化检索，不依赖 LLM 意图识别
- **发芽报告**：每日回顾——把今日新节点和图谱关联节点融合，生成新观点
- **主题融合**：输入主题 → 多轮 grep 筛选收窄 → 融合多篇生成新文章
- **Token 经济**：用 grep 绕开意图识别后，整个查询 token 控制在几千以内
- **意图识别绕过**：大模型最费 token 的环节是意图识别，grep 查询直接跳过
- **命令式查询**：靠命令 / 标签 / 关键词直接查询，不做大规模语义理解
- **图谱关系**：知识节点之间的关联结构（基于 / 引用 / 并列 / 验证）

## 关联图谱

### 上游（基于 / 来自）
- [[AI知识库技术演进拆解-从RAG到NotebookLM再到LLM-Wiki]]：RAG → NotebookLM → LLM-Wiki 的技术演进背景
- [[ai-personal-knowledge-base-problems]]：传统个人知识库的痛点分析
- [[hermes-obsidian-llm-wiki-knowledge-base]]：Obsidian + LLM Wiki 的混合实现

### 下游（应用于 / 验证于）
- [[MyAIWiki写入规范与验证模板]]：本 Wiki 正是 LLM-Wiki 方法论的具体应用
- [[.ai-wiki-schema]]：本 Wiki 的 schema 是 LLM-Wiki 思想的工程化

### 同级（横向 / 并列）
- [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]：同作者 moss 的 LLM-Wiki 上篇
- [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]]：LLM-Wiki + Obsidian 的深度分析

## 正文要点

- **核心痛点**：把文章存进笔记软件后再也没打开过——这不是知识管理，是收藏
- **真正的目标**：每天生成"发芽报告"（今日新节点回顾 + 关联节点融合）；想写内容时自动基于知识库整理成文章
- **输入端三层存储**：原文 / 知识节点 / 索引文件——精准找节点、不用读整篇；输入 token 固定
- **输出 1：发芽报告**——今日新节点 → 通过图谱找 4-5 个关联节点 → 碰撞融合 → 生成新观点
- **输出 2：主题融合**——主题 → 意图识别（拆 10 个标签）→ 多轮 grep 筛选收窄 → 融合生成
- **关键洞察**：大模型里真正费 token 的大头是**意图识别**，grep 命令式查询绕过了这一步
- **设计原则一句话**：用结构化存储降低输入成本，用 grep 命令式查询降低输出成本

## 表格：输入 vs 输出成本对比

| 环节 | 设计 | Token 消耗 |
|------|------|----------|
| 输入：链接/文字 → 拆节点 | 三层存储（原文/节点/索引） | **固定且低**（不随知识库增长） |
| 输出 1：发芽报告 | grep 找关联节点 + 融合 | **极低**（绕开意图识别） |
| 输出 2：主题融合 | 意图识别（拆 10 标签） + 多轮 grep + 融合 | **可控**（整流程几千 token） |
| 核心方法 | **结构化存储 + 命令式查询** | 不管存多少，输出成本都低 |

## 落地 MyAIWiki 的改造对照

| LLM-Wiki 已有 | MyAIWiki 现状 | 改造方向 |
|-------------|------------|---------|
| 三层存储（原文/节点/索引） | 原文 + 整理稿两层 | 加"知识节点"层 |
| grep 命令式查询 | 没用 ripgrep | Skill 加 `rg` |
| 每日发芽报告 | 有 morning-digest.py | 升级为节点融合版 |
| 主题融合生成 | 手动选文章 | 加 ripgrep 多轮筛选 |
| 关联图谱 | Obsidian 自带反链 | 显式声明 3 维度关联（上游/下游/同级） |

## 我的理解

- **这是 MyAIWiki 升级的核心方法论**——本 Wiki 已经写完两篇 LLM-Wiki 相关文章，这篇是工程实操的标杆
- 核心不是"做工具"，而是**改变存储 + 改变查询的范式**：
  - 存储：从"整篇文章" → "独立知识节点"
  - 查询：从"问 LLM" → "grep 命令"
- 跟 [[AI-Coding的顿悟时刻]] 的判断一致：复利来自 Skill / Memory / Context Engineering，不是单条 prompt
- MyAIWiki 的下一阶段重点：**所有新文章按知识节点 + 关联图谱写，老文章逐步加 frontmatter**

## 适合关联的主题

- [[AI知识库技术演进拆解-从RAG到NotebookLM再到LLM-Wiki]]
- [[构建LLM-Wiki智能知识库-实现AI辅助写作工作流]]
- [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]]
- [[hermes-obsidian-llm-wiki-knowledge-base]]
- [[ai-personal-knowledge-base-problems]]
- [[rag-fundamentals]]
- [[llm-agent-unified-memory-framework]]
- [[claude-obsidian-second-brain]]
- [[MyAIWiki写入规范与验证模板]]
