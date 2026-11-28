# Addy Osmani agent-skills 设计哲学 — Digest

> **一句话**:agent-skills = Chrome 团队 Lead 把"资深工程师工作流"打包成 23 技能 + 7 命令,治的是 AI 写代码"能跑但上生产就崩"的抄近路病。

## 速查表

| 维度 | 数字 | 含义 |
|---|---|---|
| Star | 58.9k | 4 月至今从 23k → 58.9k(写文章时 4 万→6 万) |
| 技能 | 23 | 22 生命周期 + 1 元技能 |
| 命令 | 7 | `/spec` `/plan` `/build` `/test` `/review` `/code-simplify` `/ship` |
| 角色 | 3 | 代码评审员 / 测试工程师 / 安全审计员 |
| 清单 | 4 | 测试 / 安全 / 性能 / 无障碍 |
| 工具 | 8+ | Claude Code、Cursor、Gemini CLI、Windsurf、OpenCode、Copilot、Kiro、Codex |
| License | MIT | v0.6.0 |
| 项目地址 | github.com/addyosmani/agent-skills | — |

## 4 个杀手锏(设计哲学)

1. **流程而非文档** —— 技能=有步骤+检查点+退出条件的工作流,不是参考资料
2. **反合理化** —— 每技能内置"借口→反驳"表,堵死 agent 跳步退路
3. **验证不可妥协** —— 每技能以"拿证据"收尾(测试/构建/运行数据)
4. **渐进式披露** —— SKILL.md 是入口,详细引用按需加载(token 友好)

## 7 块统一骨架(每个 SKILL.md 都有)

`名称+描述` → `概述` → `何时使用` → `流程` → `反合理化` → `危险信号` → `验证`

## 7 命令流水线

| 命令 | 阶段 | 原则 |
|---|---|---|
| `/spec` | 定义 | 先有规格再写代码 |
| `/plan` | 规划 | 拆成小而独立的任务 |
| `/build` | 构建 | 一次只做一小片 |
| `/test` | 验证 | 测试就是证据 |
| `/review` | 评审 | 改善代码健康度 |
| `/code-simplify` | 简化 | 清晰胜过聪明 |
| `/ship` | 发布 | 越快越安全 |

## 23 技能按生命周期排

定义(3)→ 规划(1)→ **构建(7 重点)** → 验证(2)→ 评审(4)→ 发布(5)= 22 + 元(1)

## Google 工程文化整合

- **Hyrum 定律** → 接口设计
- **Beyoncé 规则 + 测试金字塔 80/15/5** → 测试
- **变更规模 ~100 行 + 评审速度** → 代码评审
- **Chesterton 栅栏** → 代码简化
- **主干开发 + 功能开关** → git / CI/CD
- **代码当负债** → 废弃技能

## 适配判断

- ✅ 适合:用 AI 写真实项目 / 受够"能跑就行" / 要给团队定规范
- ❌ 不必:偶尔写小脚本 / 完全不碰工程化 / 嫌"立规矩"拖慢节奏

## 对 Seetong / OpenClaw 3 个可借鉴动作

1. **Skill 统一骨架审计** —— 检查现有 30+ Skill 是否都按 7 块结构(名称/概述/何时用/流程/反合理化/危险信号/验证)写;不一致的改一致
2. **加"反合理化"环节** —— 现有 Skill 大多没"借口→反驳"表,补全这一节,从"为什么 agent 不会跳过"角度重新设计
3. **复用 7 命令流水线到 Seetong** —— 把 `/spec` `/plan` `/build` `/test` `/review` `/ship` 做成 Seetong 7 命令 Skill,接 TAPD 需求流转

## 关联

- [[谷歌开源agent-skills]] —— 4-27 旧版(20 skills / 23k star),本文为最新数据 + 4 设计哲学 + 7 块骨架完整解读
- [[Addy-Osmani-Loop-Engineering]] —— 同源主线姊妹篇(方法论原典)
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] —— 中文工程实操
- [[PM-Skills-Marketplace-产品经理必备skill]] —— Skill 库同主题
- [[Agentic-Engineering-AI-Workbench]] —— AI 工作台
- [[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]] —— 团队已有沉淀

## 备注

- 4 个旧 wiki 数据从 23k / 20 skills 更新到 58.9k / 23 skills,2026-04 → 2026-06 增长明显
- 文章是 ColaAI 转载整理,但核心数据 + 4 设计哲学 + 7 块骨架 + Google 工程文化整合是 Addy Osmani 原文,本文是中文工程社区视角
