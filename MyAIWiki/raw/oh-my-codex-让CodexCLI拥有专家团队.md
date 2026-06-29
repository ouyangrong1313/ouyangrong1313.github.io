# Codex 你不是一个人在战斗

**来源**：微信公众号 - ColaAI
**作者**：ColaAI
**日期**：2026年4月23日
**链接**：https://mp.weixin.qq.com/s/yHsO3duZZYnKsudWyPYpPQ

---

你是不是也遇到过这种情况？

用 Codex CLI 写代码，单个 agent 一个 prompt，复杂任务要不停切换上下文，没有记忆、没有分工、没有验证……

结果是：AI 写得飞快，你 debug 更快。

今天要讲的这个项目，正在悄悄改变这一切。

---

## 01｜oh-my-codex 到底是什么？

oh-my-codex（简称 OMX）是 OpenAI Codex CLI 的多智能体编排层。

名字致敬了 oh-my-zsh —— 就像 oh-my-zsh 让你的终端脱胎换骨，OMX 要做的，是让 Codex CLI 从「单打独斗的 AI」变成「有纪律的作战团队」。

它由韩国开发者 Yeachan-Heo 主导，灵感来自他自己的另一个项目 oh-my-claudecode。

关键设计：OMX 不是 fork，而是 pure add-on。它完全基于 Codex CLI 的原生扩展点，你永远跟着官方主线走，不用担心被"锁死"。

装上 OMX 前后，差距有多大？

| 裸 Codex CLI | 装上 OMX 之后 |
|-------------|--------------|
| 单 agent 单 prompt | 30 个角色专家 |
| 手动管理流程 | 39 个工作流技能 |
| 没有持久上下文 | 项目记忆 + 会话笔记 |
| 无多 agent 协作 | 6 个并发 + 验证/修复循环 |
| 无验证机制 | 证据驱动 + 架构师签核 |

---

## 02｜它是怎么做到的？

OMX 的精妙之处，在于它不发明新协议，而是把 Codex CLI 已有的 6 个扩展点用到极致：

- `AGENTS.md` → 编排大脑（启动即加载）
- `~/.codex/prompts/` → 30 个 agent 角色
- `~/.agents/skills/` → 39 个工作流技能
- `config.toml` → MCP 服务 + 通知钩子
- `.omx/` → 状态、记忆、计划、笔记

**一句话总结：把 Codex CLI 当成执行引擎，把"纪律"装在外面。**

---

## 03｜30 个 agent，组成一支"数字工程队"

### 🔨 构建与分析组
explore · analyst · planner · architect · debugger · executor · verifier

### 🔍 代码评审组（6 个专家分工）
style-reviewer（格式）· quality-reviewer（逻辑）· api-reviewer（接口）· security-reviewer（安全）· performance-reviewer（性能）· code-reviewer（综合）

### 🎯 领域专家组
test-engineer · designer · writer · git-master · researcher · dependency-expert · qa-tester · scientist ……

### 📊 产品组 + 协调组
product-manager · ux-researcher · information-architect · product-analyst · critic（唱反调）· vision（读图）

**💡 注意看 critic 这个角色** —— 它专门唱反调。你让 AI 写代码，最大的风险是它"讨好你"。OMX 主动引入一个挑刺的 agent，这是很多团队都会忽略的一个细节。

---

## 04｜39 个工作流技能 = 开箱即用的"战术手册"

如果说 agent 是"人"，那么 skill 就是"打法"。用 `$技能名` 即可触发。

### 🚀 执行模式（8 种）
- `$autopilot` — 完全自动驾驶，从想法直接到可运行代码
- `$ralph` — 持续循环，不完成不罢休（有架构师把关）
- `$ultrawork` — 最大并行，多 agent 同时开工
- `$team` — N 个 agent 协同处理共享任务列表
- `$pipeline` — 流水线式串行协作
- `$ecomode` — 省钱模式，走轻量模型
- `$ultrapilot` — 并行自动驾驶 + 文件归属分区（防冲突）
- `$ultraqa` — 测试、验证、修复、再循环

### 📋 规划 + 其他
`$plan` · `$ralplan` · `$tdd` · `$security-review` · `$build-fix` · `$frontend-ui-ux` ……

### ✨ 魔法关键词（Magic Keywords）
只要说 "ralph"、"别停"、"autopilot"、"build me"，OMX 的编排大脑会自动帮你激活对应技能。

---

## 05｜怎么用？三步上车

### ⚠️ 前置要求
- ✅ Node.js ≥ 20
- ✅ OpenAI Codex CLI：`npm install -g @openai/codex`
- ✅ OpenAI API Key（或 Codex Pro 订阅）
- ✅ 推荐 macOS / Linux（Windows 支持较弱）

### 🪜 Step 1：安装
```bash
npm install -g oh-my-codex
```

### 🪜 Step 2：初始化
```bash
omx setup    # 自动安装 prompts、skills、配置
omx doctor   # 运行 9 项健康检查
```

### 🪜 Step 3：开始用
```bash
omx

> /prompts:architect "分析认证模块"
> /prompts:executor "给登录流程加输入校验"
> $autopilot "搭一个用户管理 REST API"
> $team 3:executor "修复所有 TS 错误"
```

---

## 06｜它适合谁？不适合谁？

### ✅ 适合这些人
- 已经在用 Codex CLI，想让它"更像一个团队"
- 做中大型项目，需要 plan / review / verify 的闭环
- 熟悉 macOS / Linux 命令行
- 希望 AI 编码流程有记忆、有纪律、有协作

### ❌ 不适合这些人
- 只想"裸用" Codex CLI，不需要额外一层
- 纯 Windows 用户（官方明确说支持较弱）
- 不用 Codex CLI，只用 IDE 插件（那应该看 Cursor / Copilot）

### ⚠️ 危险选项
`omx --madmax` 会绕过所有审批和沙箱，让 Codex 完全自由执行。只在隔离环境里用，不要在你的主工作目录玩这个。

---

## CORE INSIGHT

> 单 agent 的极限，
> 不在模型能力，
> 而在工程化组织。
> OMX 做的，就是给 AI 装上"项目管理"这件事

---

## 最后说一点真心话

AI 编码工具卷到现在，真正的竞争点已经不是"模型多聪明"，而是能不能把 AI 组织好。

oh-my-codex 的思路很清爽：不做新模型、不造新协议、不卷 UI，就只干一件事 —— 让 Codex CLI 变成一支有纪律的队伍。

如果你是 Codex CLI 的重度用户，这可能是今年最值得装的一个 npm 包。

---

标签：#主题/AI Coding #手法/工具测评 #场景/技术博客

相关链接：
- 原文：https://mp.weixin.qq.com/s/yHsO3duZZYnKsudWyPYpPQ
- GitHub：https://github.com/Yeachan-Heo/oh-my-codex
