# Hermes Agent Masterclass

> 来源：Akshay 🚀 @akshay_pachaar | 2026-05-13
> 标签：#主题/AIAgent #场景/技术教程

## 核心信息

**90天 90,000+ GitHub stars**，开源 AI Agent。

**核心问题**：每次会话结束，所有编码偏好、项目规范、修复记录全部消失。

**三个关键能力**：
- 跨会话记忆
- 自进化 Skills（Agent 编写自己的 playbook）
- GEPA 离线优化

## 与 OpenClaw 的核心区别

> "Hermes packages a gateway around a learning agent. OpenClaw packages an agent around a messaging gateway."

## 三层记忆系统

| Tier | 类型 | 容量 | 速度 |
|------|------|------|------|
| 1 | MEMORY.md + USER.md | 2.2KB + 1.4KB | 始终在 context |
| 2 | SQLite 全文搜索 | 无限 | 搜索时触发 |
| 3 | 外部 providers（8 个插件） | 无限 | 按需预取 |

## Skills 自进化循环

触发条件：复杂任务完成 / 错误找到解法 / 用户纠正 / 发现新工作流

Curator 后台维护：30 天未用 → stale，90 天 → archived。永不自动删除，有快照回滚。

## GEPA（Genetic-Pareto Prompt Evolution）

离线优化 pipeline，读取执行 traces 理解失败原因，进化搜索提出改进。

- ICLR 2026 Oral paper，MIT 许可
- 成本：$2-10/次，无需 GPU
- 在 RL/GRPO 之前的高效替代方案

## 多 Agent 架构

通过 profiles 隔离，每个 Agent 有自己 SOUL.md、memory、skills、Telegram bot。

应用场景：programmer（委托 Claude Code）+ designer（学习视觉风格）+ researcher（每日 Telegram 简报）。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```