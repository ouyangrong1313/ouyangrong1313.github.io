---
title: Claude Tag - Karpathy 第三范式（Slack 异步协作）
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/ClaudeCode
  - 主题/Slack
  - 主题/异步协作
  - 场景/产品介绍
  - 场景/公众号长文
  - 节点/Agent-Loop
  - 节点/Harness
nodes: [Claude Tag, Slack协作, 第三范式, 自洽实体, ambient模式, 异步执行, 频道权限隔离, 价值观不可调教, 厂商agent, 开源替代, openclaw, 65%代码贡献]
links: [[02-ai-coding/Claude-Code-主动式Agent-Routines]], [[02-ai-coding/Claude-Code首席设计师Meaghan-Choi工作流]], [[02-ai-coding/Claude-Code一周年回顾-Boris-Cat]], [[02-ai-coding/Anthropic万字长文三个判断和一个阳谋]], [[02-ai-coding/Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
date: 2026-06-24
source: 微信公众号「逛逛 GitHub」（猜测）逛逛 2026-06-24
---

# Claude Tag - Karpathy 第三范式（Slack 异步协作）

## 核心结论

**Claude Tag** 是 Anthropic 2026-06-24 发布的 Claude in Slack 协作产品：让 Claude 进指定 Slack 频道，多人协作 + 上下文积累 + ambient 主动模式 + 异步执行。**Karpathy 转发时给出了"大模型 UI 第三次大改"的高评价**，定义三种范式：① 网站 ② 桌面 App ③ 自洽的、持续在线的、异步的实体。**Anthropic 内部版本已贡献产品团队 65% 代码**，今天起对 Claude Enterprise / Team 用户开放 beta（Opus 4.8）。

评论区三个争议：① 价值观不可调教 ② 厂商 agent 归属权 ③ openclaw 等开源替代迁移成本。

## 分类提炼

- **场景**：AI Agent 团队协作 | Claude 企业级落地 | 异步 Agent 范式
- **标签**： #主题/AI-Agent #主题/ClaudeCode #主题/Slack #主题/异步协作
- **类型**：产品发布 + 权威评论 + 争议解读
- **来源**：微信公众号（逛逛 GitHub 猜测）2026-06-24
- **关联**：[[02-ai-coding/Claude-Code-主动式Agent-Routines]] | [[02-ai-coding/Claude-Code首席设计师Meaghan-Choi工作流]] | [[02-ai-coding/Claude-Code一周年回顾-Boris-Cat]] | [[02-ai-coding/Anthropic万字长文三个判断和一个阳谋]]

## 要点列表

### Karpathy 三范式理论

| 范式 | 形态 | 例子 |
|------|------|------|
| **第一种** | 大模型是个你要去访问的网站 | ChatGPT、Claude.ai 网页 |
| **第二种** | 你下到电脑上的 App | Claude Code、Cursor、Codex CLI |
| **第三种** | **自洽的、持续在线的、异步的实体**，带着全组织的工具和上下文，和人类团队并肩干活 | Claude Tag、抖音豆包、公众号元宝 |

### Claude Tag 4 大新特点

| 特点 | 说明 |
|------|------|
| **多人协作** | 一个频道里只有一个 Claude，所有人都能看到它在做什么，谁都能从上一个人停下的地方接着聊 |
| **上下文积累** | 它会随频道积累上下文，不用每次从头解释 |
| **ambient 模式** | 打开后它会主动出手，跟进那些冷掉没结论的线程，从各个频道和工具里捞出它觉得你该知道的信息 |
| **异步执行** | 派完任务你就能去忙别的，它甚至能给自己排日程，连着几小时几天独立推进一个项目 |

### 权限与隔离机制

- **频道即权限边界**：管理员指定模型在哪些频道能用哪些工具和数据
- **记忆按频道隔离**：销售那套不会把记忆传给工程那套，工程师也碰不到销售的数据
- **token 花费上限**：管理员可设
- **全链路审计**：能查到 `@Claude` 做过的每一件事以及是谁让它做的

### 内部数据 & 商业化

- **内部版本已贡献产品团队 65% 代码**
- 用法已从工程扩散到：追产品指标、处理工单、查疑难 bug
- **可用性**：今天起对 Claude Enterprise 和 Team 用户开放 beta
- **底层模型**：Opus 4.8
- **替代**：替换原来的 Claude in Slack 应用

### 评论区三争议

| 争议 | 核心问题 | 解决思路 |
|------|---------|---------|
| **价值观不可调教** | Claude Tag 的价值观、文化和品味是 Anthropic 设定的，故意做成用户没法调教 | 一个"不受职场规则约束"的同事，是产品特性还是产品缺陷？ |
| **厂商 agent 归属权** | Claude Tag 是以厂商 agent 身份进你的频道；本地方案跑在你自己的硬件上、走你自己的 API | 两种所有权模型差得远，迁移成本差 10 倍 |
| **开源替代** | 开发者推荐 openclaw 等开源版本 | 别把公司记忆锁死在一家实验室 |

### 用法 / 工具范围

- 写或合并 PR
- 跑数据分析
- 帮忙定位线上故障的根因
- 追产品指标 / 处理工单 / 查疑难 bug

## 关键链接

- [Anthropic 官方说明](https://www.anthropic.com/news/introducing-claude-tag)
- [微信公众号原文](https://mp.weixin.qq.com/s/tDAFqGgFoXgFplyfFj-pXg)

---

标签： #主题/AI-Agent #主题/ClaudeCode #主题/Slack #主题/异步协作 #主题/开源替代 #手法/权威背书 #手法/对比冲突 #手法/争议放大 #场景/公众号长文 #场景/产品介绍