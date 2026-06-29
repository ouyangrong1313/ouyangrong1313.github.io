# OpenClaw 的正确打开方式：从也就那样到离不开

> **来源**：Feisky（公众号）
> **日期**：2026年4月28日
> **链接**：https://mp.weixin.qq.com/s/AihoveTaONbtSt4ez87B2w

---

## 核心摘要

OpenClaw（龙虾）不是一个直接拼代码能力的工具，而是一个**完整的 Agent Runtime**。需要"养"，养好了才真正强大。

**核心区别**：
- Claude Code = 代码生成能力强
- OpenClaw = 完整 Agent 运行时（IM交互、记忆、Skills、ACP、Cron）

---

## 一、三个核心配置文件

| 文件 | 职责 | 更新频率 |
|------|------|---------|
| `SOUL.md` | Agent 怎么说话（身份定义，非 system prompt） | 很少变化 |
| `AGENTS.md` | Agent 怎么做事（纯流程） | 经常更新 |
| `USER.md` | Agent 怎么理解你（决策风格、偏好、沟通习惯） | 逐步补充 |

### SOUL.md 写法

1. **表达语气要具体**：写 "language with voltage"，不要写 "be helpful and concise"
2. **禁用词表**：comprehensive、robust、leveraging 等 AI 味词汇
3. **给好/坏输出示例**：比写规则更有效

**好示例**：
```
etcd compaction 的 revision 不对。看一下 --auto-compaction-retention 设的是不是 duration 模式，旧版本默认是 revision 计数。
```

**坏示例**：
```
Great question! Based on your use case, I'd recommend considering several factors when configuring etcd compaction...
```

### 经验教训

- **别写太长**：1000-2000 字足够，太长降低 Agent 智能
- **SOUL 和 AGENTS 要分离**：个性放 SOUL，流程放 AGENTS
- **每周回顾更新**：删无用内容，加新问题

---

## 二、记忆系统

### 文件结构

```
MEMORY.md              → 长期记忆
memory/2026-04-28.md   → 每日笔记
memory/working-buffer.md → 危险区缓冲
SESSION-STATE.md       → 活跃任务状态
```

### 写入机制：Write-Ahead Logging

> "让 OpenClaw 记住一件事，靠嘴说不可靠，写下来才可靠。"

OpenClaw 扫描消息，重要信息立即写入文件，再回复用户。

### Dreaming 功能

定时任务（凌晨）自动整理短期记忆：
```json
{
  "memory-core": {
    "config": {
      "dreaming": {
        "enabled": "true",
        "frequency": "0 19 * * *",
        "timezone": "Asia/Shanghai"
      }
    }
  }
}
```

**坑**：Dreaming 会把啰嗦内容也晋升，导致 MEMORY.md 臃肿，需定期手动清理。

**多项目建议**：每个项目建单独目录，主 MEMORY.md 只放索引。

### 长 Session 上下文压缩后恢复

1. 读 `working-buffer.md`（压缩前摘要）
2. 读 `SESSION-STATE.md`（当前任务状态）
3. 翻近两天日记

---

## 三、Skills 系统

### 三类 Skills

| 类型 | 示例 | 用途 |
|------|------|------|
| 通用增强 | `proactive-agent`、`self-improvement`、`context-window-management`、`systematic-debugging` | 预判需求、错误学习、上下文减负、调试 |
| 安全防护 | `skill-vetter`、`dangerous-action-guard`、`fact-check-before-trust` | 安全审查、危险操作确认、二次验证 |
| 领域专用 | `github`、`cve-check`、`ado` | 按工作场景选装 |

### 安全规则

**安装外部 Skill 前必须先跑 `skill-vetter` 审查**

作者实际案例：10 个外部 Skill 审查后跳过 3 个（一个偷偷发 Reddit、一个带自动 cron、一个藏遥测代码）

---

## 四、让它自己干活

### ACP（Agent Communication Protocol）

调用 Claude Code/Codex 等 Coding Agent：

```
你 → OpenClaw → 分析任务 → spawn Claude Code → 独立沙箱执行 → 完成后汇报
```

**应用场景**：`review [PROJECT] PR #375` → 自动切项目目录 → 收集上下文 → spawn Claude Code 审查 → 汇总结果 → 发布到 PR

**IM 绑定**：可绑定 Discord/Telegram/微信，消息自动创建 thread 并启动对应 ACP session。

### Cron 定时任务

每个 job 跑在隔离 session，不影响主 session。

**示例任务**：
- Git Sync：每小时自动备份 workspace
- AI News：每 8 小时抓新闻推 Discord
- Dreaming：每天凌晨整理记忆
- Issue Triage：每天上班前 triage issue 列表
- Version Check：每天检查项目更新

---

## 五、大模型配置

### Fallback Chain

```json
{
  "model": {
    "primary": "github-copilot/claude-opus-4.6",
    "fallbacks": [
      "github-copilot/claude-sonnet-4.6",
      "github-copilot/claude-opus-4.7",
      "openai/gpt-5.5"
    ]
  }
}
```

### Memory Search Provider

用 Azure OpenAI `text-embedding-3-small` + hybrid search。

---

## 六、踩坑清单

| 坑 | 解决方案 |
|----|---------|
| Gateway 重启后 ACP reconcile 失败 | 设 `tools.sessions.visibility = all`，能看到所有 session 状态 |
| 升级后 gateway 挂掉 | 先跑 `openclaw doctor --fix`，修好再重启 |
| Dreaming 导致 MEMORY.md 臃肿 | 定期手动清理 |
| SOUL.md 写太长 | 控制在 1000-2000 字 |

---

## 七、OpenClaw vs Claude Code

| 维度 | Claude Code | OpenClaw |
|------|------------|----------|
| 代码生成能力 | 更强 | 相对弱 |
| 定位 | Coding Agent | 完整 Agent Runtime |
| IM 交互 | ❌ | ✅ |
| 记忆系统 | ❌ | ✅ |
| Skills 扩展 | ❌ | ✅ |
| ACP 调度 | ❌ | ✅ |
| Cron 定时任务 | ❌ | ✅ |

**结论**：Claude Code 是更强的 coding agent，OpenClaw 是调度它们并提供持久化能力的运行时。

---

## 标签

#主题/AIAgent #场景/OpenClaw #场景/工具配置 #手法/经验分享
