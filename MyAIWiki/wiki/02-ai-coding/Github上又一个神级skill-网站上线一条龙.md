---
title: "GitHub 上的 golive-skill：把「网站上线一条龙」做成带审批的 Agent 流程"
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 主题/AI-Agent
  - 主题/Skill
  - 主题/Agent-Skills
  - 主题/部署
  - 主题/生产安全
  - 节点/golive-skill
  - 节点/detect-plan-approve-apply-verify
  - 节点/审批闸门
  - 节点/验证四态
  - 节点/资源所有权
  - 场景/个人项目部署
nodes: [golive-skill, detect-plan-approve-apply-verify, 审批闸门, 计划变更则批准失效, verify四态(pass-fail-warning-skipped), skipped不算通过, golive-status只读巡检, golive-teardown可确认责任边界, 服务归用户所有, Early-Alpha边界]
links: [[02-ai-coding/谷歌开源agent-skills]], [[01-ai-agents/Skill-Self-Evolution]], [[02-ai-coding/Codex工具入口与能力边界]], [[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]]
date: 2026-09-30
source: 微信公众号 / 开源日记（2026-09-29 15:38）
原始链接: https://mp.weixin.qq.com/s/snz6fkTaHa6qxuKVUz6G5g
status: published
---

# GitHub 上的 golive-skill：把「网站上线一条龙」做成带审批的 Agent 流程

> **核心结论**：golive-skill 把"让 Agent 部署项目"从一句自然语言祈使句，变成 `detect → plan → approve → apply → verify` 的**带审批闸门的过程**；它的真正价值不是自动化部署本身，而是把"人拍板"放进流程里，并且明确了一条边界——它只约束自己的流程，约束不了已经拿到云账号权限的 Agent。

## 分类提炼

- 场景：AI Coding / Agent Skills / 个人与小项目上线
- 标签： #主题/AI-Coding #主题/AI-Agent #主题/Skill #主题/部署 #主题/生产安全
- 类型：开源项目介绍 + 一手试用记录（作者自述亲自跑通一个网址缩短器项目）
- 证据等级：**作者主张为主**；官方 README、验证链路与安全边界均为文中转述，本文未独立复核 GitHub 仓库

## 知识节点

- **golive-skill**：一个开源 Agent Skill，目标是帮 Agent 把写好的项目直接部署到**用户自己的云账号**里；官方 README 明确 `No GoLive account, hosted backend or product telemetry.`[原文事实：转述 README]
- **detect → plan → approve → apply → verify**：五阶段上线流程。detect 识别框架与依赖服务；plan 列出要创建和修改的资源；approve 由人确认；apply 执行部署、数据库、环境变量与 DNS；verify 检查部署地址、域名与服务状态。[原文事实：作者对流程的描述]
- **审批闸门（approval gate）**：在真正改动账号前必须有人确认的流程节点。修改 DNS、删除资源、**第一次上线生产**都会单独再问一次。[原文事实]
- **计划变更则批准失效**：授权绑定的是**具体计划**而非时间段；一旦计划发生变化，之前批准的授权自动作废。这是把"人拍板"从一次性动作变成持续约束的关键设计。[本文推断：由原文"计划有变化则之前批准的东西无效"推出]
- **verify 四态（pass / fail / warning / skipped）**：验证结果分为通过、失败、警告、跳过四类；作者特别强调"**skipped 不算通过**"。[原文事实]
- **skipped 不算通过**：一个可直接迁移到任何验证流程的原则——"无法确认"必须显式暴露，不能默认并入成功。作者举例：环境变量存在不代表值正确，域名验证通过不代表邮件送达收件箱。[原文事实 + 本文泛化]
- **golive status（只读巡检）**：只读检查此前创建的 DNS、环境变量、Webhook、数据库与托管项目是否发生变化。[原文事实]
- **golive teardown（可确认责任边界）**：清理时只删除**能够确认由自己创建**的资源，删除前需再次确认；删不掉的资源会明确告知剩下什么、需要去哪里手动处理。[原文事实]
- **服务归用户所有**：Vercel、Supabase、域名、Resend、Stripe 均为用户自己的独立账号，golive-skill 只负责把它们连接起来——"资源归你，GoLive 做操作"。[原文事实：作者转述 README 精神]
- **Early Alpha 边界**：项目仍处早期，复杂云架构不是强项；工具只能约束自身流程，**Agent 若已持有云账号权限仍可绕过它直接操作**；本地凭据是明文文件（仅靠文件权限限制），并非系统钥匙串。[原文事实：作者明确列出的三项限制]

## 关联图谱

### 上游（基于 / 来自）
- [[02-ai-coding/谷歌开源agent-skills]]：同为"把工程纪律封装成 Skill"的思路——那篇讲开发全流程的纪律，本篇讲交付末端的部署纪律
- [[01-ai-agents/Skill-Self-Evolution]]：Skill 如何做得更科学、方向可控；golive-skill 的"计划变更则批准失效"是 Skill 自我演化时保持可控的一个具体机制

### 下游（应用于 / 验证于）
- [[02-ai-coding/Codex工具入口与能力边界]]：golive-skill 正是"工具入口决定能力边界"的实例——它在 Agent 已有的云账号权限之外加了一层审批入口，但这层可被绕过
- [[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]]：可作为对照样本，检验一份部署类 Skill 是否具备清晰的触发器、边界与验证块

### 同级（横向 / 并列）
- [[02-ai-coding/被Harness圈捧成圣的PiAgent-接上DeepSeek-V4-Flash-如虎添翼]]：同为 Agent 能力外延的开源实践，一个补执行环境，一个补上线流程
- [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]]：企业级视角下"用 Skill 承载流程约束"，与个人项目视角的 golive-skill 形成规模对照

## 正文要点

1. **痛点定位**：AI 写代码已经不是瓶颈，上线才要面对托管、数据库、环境变量、域名、邮件、支付"一个都绕不开"。作者原话："AI 帮我操作没问题，但真到了生产账号，我还是不敢让它随便改。"
2. **流程形状**：`detect → plan → approve → apply → verify`，一句话概括为"先做计划，再执行，最后再看结果"。
3. **三个亮点**：上线过程可见（列出要动哪个账号、改哪些资源，出错就停在哪一步）；动账号前先问（修改 DNS、删除资源、第一次上线生产额外确认）；服务还是用户自己的。
4. **已验证链路**：文中称官方已跑通 Vercel + Supabase、Netlify + Neon，以及 DNS、Resend 邮件、Stripe 测试支付、Supabase Auth。[作者主张：未在本库独立复核]；作者判断目前最适合个人项目、小应用和测试环境。
5. **安装方式**：需 Node.js 20+，已验证 Codex 与 Claude Code；主推 `npx skills add https://github.com/mikehasa/golive-skill --skill golive --global`（Codex 加 `--agent codex --yes`），亦可 `npx golive@alpha install --agent codex`。
6. **边界与风险**：Early Alpha，复杂云架构非强项；无法阻止已有云账号权限的 Agent 绕过；本地凭据为明文文件而非系统钥匙串。作者态度是"当作一个有审批、有记录、有验证的上线助手，不会完全放手"。
7. **建议用法**：第一次先用测试项目跑，不要刚装完就把正式站点交出去。

## 事实 / 推断 / 未知

- **原文事实（作者转述或直接陈述）**：五阶段流程、审批闸门设计、verify 四态、`skipped 不算通过`、status 与 teardown 行为、安装命令、三项限制。
- **本文推断**：把"计划变更则批准失效"理解为"授权绑定具体计划"；把它归类为"部署状态机 + 审批闸门"，价值主要在可观察与可追溯，而非安全性提升。
- **未知 / 未独立验证**：GitHub 仓库当前实际状态与 star 数、五条验证链路的真实完备度、`golive teardown` 在边界情况下是否真能只删自己的资源、明文凭据的实际风险面。

## 相关链接

- 原文链接：https://mp.weixin.qq.com/s/snz6fkTaHa6qxuKVUz6G5g
- 开源地址：https://github.com/mikehasa/golive-skill
- 原始归档：raw/Github上又一个神级skill-网站上线一条龙.md（raw 目录不做 wiki 内链）
