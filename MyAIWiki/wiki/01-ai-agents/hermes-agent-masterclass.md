# Hermes Agent Masterclass

- 来源：Twitter/X @akshay_pachaar
- 原文：https://x.com/akshay_pachaar/status/2054564519280804028
- 编译日期：2026-05-14
- 标签：#主题/AIAgent #场景/技术教程

## 核心要点

**Hermes Agent** by Nous Research：90 天获得 90,000+ GitHub stars，开源 AI Agent 领域增长最快。

**解决的核心问题**：每次会话结束，编码偏好、项目规范、修复记录全部消失。

## 架构特点

| 特性 | 说明 |
|------|------|
| **身份层 SOUL.md** | 定义 Agent 个性、语气、限制，固定框架内的运动部件 |
| **三层记忆** | Tier1（M+M/USER 文件）+ Tier2（SQLite 全文）+ Tier3（8 个外部 providers） |
| **自进化 Skills** | Agent 遇到问题 → 解决 → 保存为 SKILL.md → 下次直接调用 |
| **Curator 维护** | 后台垃圾回收，30 天未用 → stale，90 天 → archived |
| **GEPA 优化** | 离线进化，读取执行 traces 理解失败原因，$2-10/次 |

## 与 OpenClaw 的核心区别

> "Hermes packages a gateway around a learning agent. OpenClaw packages an agent around a messaging gateway."

## 多 Agent 场景

通过 `profiles` 隔离，每个 Agent 有独立 SOUL.md、memory、skills：

- **Programmer**：委托 Claude Code 执行，Hermes 编排
- **Designer**：学习视觉风格，创建 `my-design-style` skill
- **Researcher**：每日 Telegram 简报（GitHub trending + 大厂动态 + 论文 + 社交）

## 安装命令

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
hermes
```

## 相关资料

- [[hermes-obsidian-llm-wiki-knowledge-base]] - Roland.W 的 Hermes+Obsidian+LLM Wiki 本地知识库方案