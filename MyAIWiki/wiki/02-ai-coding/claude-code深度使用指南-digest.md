原文: https://mp.weixin.qq.com/s/CSbQsQ1mB6Viec-8Ic27WA
来源: 微信公众号 - 富贵的胡思乱想
日期: 2026-03-26

---

# Claude Code 深度使用指南：Opus Plan、Skill 插件与 CLI 工具全攻略

**核心结论**: Claude Code 的门槛远比想象中低，但它的上限远比大多数人用到的高。真正的差距在于你如何使用它。

## 核心要点

### 1. 快速安装
一行命令安装：`curl -fsSL https://claude.ai/install.sh | bash`

### 2. 多端共用
核心引擎统一，`CLAUDE.md` 配置、MCP 服务器在所有端共用。终端、VS Code、JetBrains、桌面应用、网页版都能用。

### 3. 权限配置
`--dangerously-skip-permissions` 跳过所有确认，但需充分信任 AI 时再用。

### 4. 七大提示词技巧
1. **Opus Plan 模式**：`/model opusplan` = Opus 战略思考 + Sonnet 执行速度
2. **关注结果而非任务** — 描述目标而非功能
3. **说清"为什么"** — 提供背景和动机
4. **提供参考示例** — 截图比文字好，代码仓库最佳
5. **让 AI 反问你** — 像专家一样指出盲点
6. **合理使用 Skill** — 性能型/工作流型两类
7. **主动管理上下文** — 接近 20% 时用 `/clear` 重置

### 5. CLI 工具增强
Playwright、GitHub CLI、Supabase CLI 等工具可以极大增强 Claude Code 的能力。

---

## 关键洞察

> Claude Code 有 100 万 Token 上下文预算，前 20 万 Token（约 20%）是黄金区间，性能最佳。接近 100 万 Token 时，Opus 有效性降至约 78%。

> Skill 本质上是一段文本提示词，告诉 Claude Code 如何在特定场景下用特定方式完成工作。没有魔法，但效果显著。

---

## 标签

#主题/AI-Coding #场景/工具教程