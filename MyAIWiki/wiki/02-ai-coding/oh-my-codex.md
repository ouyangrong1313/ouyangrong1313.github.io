# oh-my-codex：让 Codex CLI 拥有 30 个专家团队

## 核心结论

oh-my-codex（OMX）是 OpenAI Codex CLI 的**多智能体编排层**，让 Codex CLI 从"单打独斗的 AI"变成"有纪律的作战团队"。

**核心洞察**：单 agent 的极限不在模型能力，而在工程化组织。

## 关键特性

### 裸 Codex CLI vs 装上 OMX

| 能力 | 裸 Codex CLI | OMX |
|------|-------------|-----|
| Agent 数量 | 单 agent 单 prompt | 30 个角色专家 |
| 流程管理 | 手动 | 39 个工作流技能 |
| 上下文 | 无持久上下文 | 项目记忆 + 会话笔记 |
| 协作 | 无多 agent | 6 个并发 + 验证/修复循环 |
| 验证 | 无 | 证据驱动 + 架构师签核 |

### 6 个扩展点用到极致
- `AGENTS.md` → 编排大脑
- `~/.codex/prompts/` → 30 个 agent 角色
- `~/.agents/skills/` → 39 个工作流技能
- `config.toml` → MCP 服务 + 通知钩子
- `.omx/` → 状态、记忆、计划、笔记

### 30 个 agent 分工
- 🔨 **构建组**：explore · analyst · planner · architect · debugger · executor · verifier
- 🔍 **评审组**：style · quality · api · security · performance · code reviewer
- 🎯 **专家组**：test-engineer · designer · writer · git-master · researcher 等
- 📊 **产品+协调组**：product-manager · critic · vision 等

### 39 个工作流技能
- `$autopilot` — 完全自动驾驶
- `$ralph` — 持续循环 + 架构师把关
- `$ultrawork` — 最大并行
- `$team` — N 个 agent 协同
- `$ultraqa` — 测试、验证、修复、再循环

### 特殊设计：critic agent
专门唱反调，对抗 AI"讨好用户"的本能。

## 安装使用

```bash
# 安装
npm install -g oh-my-codex

# 初始化
omx setup
omx doctor

# 使用
omx
> /prompts:architect "分析认证模块"
> $autopilot "搭一个用户管理 REST API"
```

## 适合人群

✅ Codex CLI 重度用户，中大型项目需要 plan/review/verify 闭环
❌ 只想裸用 Codex CLI 或纯 Windows 用户

---

## 标签
#主题/AI Coding #场景/技术博客

## 来源
- 原文：https://mp.weixin.qq.com/s/yHsO3duZZYnKsudWyPYpPQ
- GitHub：https://github.com/Yeachan-Heo/oh-my-codex
