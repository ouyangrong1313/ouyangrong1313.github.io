# 谷歌 Agent Skills：23000+ Stars 的 AI 编程纪律包

## 核心结论

Agent Skills 是谷歌 Gemini 团队主管 Addy Osmani 开源的项目，将《Software Engineering at Google》的方法论封装成 20 个可组合 Skill，让 AI 在每个开发阶段都按工程规范工作。

**一句话：Spec Kit 用文档定 AI，Superpowers 用流程带 AI，Agent Skills 用纪律管 AI。**

## 解决的问题

AI 编程工具模型能力越强，走捷径的毛病越明显：
- 不考虑项目长期稳定性
- 顾不上后续迭代维护
- 这正是初级开发者与资深工程师的差距

## 核心功能

### 20 个 Skill + 7 个 Slash 命令

覆盖软件开发生命周期六阶段：

| 阶段 | 命令 |
|------|------|
| 定义 | `/spec` 需求梳理 |
| 规划 | `/plan` 任务拆分 |
| 构建 | `/build` 增量实现 |
| 验证 | `/test` 跑测试 |
| 评审 | `/review` 代码评审 |
| 发布 | `/ship` 部署上线 |

### 3 个 Agent 人设

在 `/ship` 部署上线时并行开工：
- `code-reviewer` — 代码评审报告
- `test-engineer` — 测试报告
- `security-auditor` — 安全评估报告

最终给出是否可以上线的结论。

## 竞品对比

| 工具 | 思路 |
|------|------|
| Spec Kit | 「先写清楚再动手」— 用文档约束 AI |
| Superpowers | 开发流水线 — 用流程串联 AI |
| Agent Skills | 工程师习惯 — 用纪律管理 AI |

## 支持平台

Claude Code、Cursor、Gemini CLI、Windsurf、GitHub Copilot、Codex

### Claude Code 安装
```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

### Cursor 安装
复制 SKILL.md 到 `.cursor/rules/` 目录

## 标签

#主题/AI-Coding #手法/权威背书

## 相关链接

- GitHub：https://github.com/addyosmani/agent-skills
