---
title: PM Skills Marketplace - 产品经理必备 Skill
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Agent, #主题/产品经理, #主题/Skill, #主题/方法论, #场景/工具推荐, #场景/方法论落地, #场景/公众号长文, #手法/案例叙事, #手法/痛点共鸣, #手法/数据冲击, #节点/Skill, #节点/Slash-Command, #节点/OpenCode, #节点/产品方法论]
nodes: [PM-Skills, Slash-Command, Skill, Command, OST, Lean-Canvas, JTBD, Pre-mortem, OpenCode, Claude-Code, 方法论编码]
links: [[mattpocock-skills]], [[Skill-Self-Evolution]], [[claude-code-large-codebase-best-practices]], [[与AI一起做产品的六条原则]], [[AI-PM核心技能-观测评估与反馈闭环]]
date: 2026-06-14
source: 微信公众号 / 开源日记 / 2026-06-13
---

# PM Skills Marketplace —— 产品经理必备 Skill

- 原文链接:https://mp.weixin.qq.com/s/7t3pCljov14VbIDXcsYuBw
- 来源:微信公众号 开源日记
- 获取时间:2026-06-14
- GitHub:https://github.com/phuryn/pm-skills (3 个月 16k Star)

## 核心结论(一句话)

> **通用 AI 给"文字模板",PM Skills 给"结构化执行路径"** —— Skill 的本质是领域专家把"做事路径"代码化,AI 不替你决策,只带你把方法论走一遍。

## 分类提炼

- 场景:产品经理 AI 工作流、Skills 生态、Slash command 落地
- 标签:#主题/AI-Coding #主题/Skill #场景/工具推荐 #场景/方法论落地
- 类型:工具评测 + 案例叙事 + 行业趋势观察

## 知识节点(11 个独立概念)

> 每条独立成段可被理解,对应一个可 grep 的关键词

- **PM-Skills**:phuryn/pm-skills 开源项目,把产品管理方法论编码成 AI 可执行 Skills 的市场,3 个月 16k Star
- **Skill**:独立的方法论单元,单一可调用,如 `/opportunity-solution-tree` 对应 Teresa Torres OST
- **Command**:多个 Skill 组合成的完整流程,如 `/discover` = 创意→假设→排序→实验四步串联
- **Slash-Command**:源自 Claude Code 的交互范式,正在外溢到 OpenCode、Cursor、Cline,成为 AI Coding 事实标准
- **OST**:Opportunity Solution Tree(Teresa Torres),从结果逆推机会、分解方案、实验验证的产品发现框架
- **Lean-Canvas**:精益商业模式画布,9 格快速验证商业假设,PM Skills 把"填什么"的难题转成引导式提问
- **JTBD**:Jobs-to-Be-Done,用户访谈脚本中的核心问题类型,关注"用户雇佣产品做什么任务"
- **Pre-mortem**:项目启动期风险分析方法,提前假设项目失败并归因,区分 Tigers/Paper Tigers/Elephants 三类风险
- **OpenCode**:开源 AI Coding 工具,兼容 Slash command + Skill 协议,PM Skills 主要安装目标(`~/.opencode/skills/`)
- **Claude-Code**:Slash command 协议起源者,Commands 功能目前仍是其和 Claude Cowork 独占
- **方法论编码**:Skill 生态的核心命题 —— 把领域专家的"做事路径"封装成 AI 可调用工作流,区别于"通用 Prompt 模板"

## 关联图谱

### 上游(基于 / 来自)
- [[mattpocock-skills]]:Skill 范式的同源案例,领域专家(TS 教学)把方法论编入 Claude Skill
- [[Skill-Self-Evolution]]:Skill 自进化的研究综述,本文是垂直领域 Skill 编码的实际落地

### 下游(应用于 / 验证于)
- 暂无,待后续应用 —— 可启发 MyAIWiki 把"开头钩子库""文章结构库"做成 `/hook-*` Skill
- 可启发 Seetong-iOS 把"PRD 模板""BUG 调研脚本"做成项目内 Skill

### 同级(横向 / 并列)
- [[claude-code-large-codebase-best-practices]]:Claude Code Skill 在工程域的同主题应用
- [[与AI一起做产品的六条原则]]:产品经理 AI 实践的方法论视角(本文是工具视角)
- [[AI-PM核心技能-观测评估与反馈闭环]]:产品经理 AI 工作流的能力视角

## Skill vs Command 对比

| 类型 | 定义 | 粒度 | 典型示例 |
|------|------|------|---------|
| **Skill** | 独立方法论 | 单步可调用 | `/opportunity-solution-tree` (OST) · `lean-canvas` · `pricing-strategy` |
| **Command** | Skill 组合 | 流水线 | `/discover` = 创意 + 假设 + 排序 + 实验 |

**积木 vs 流水线** —— Skill 是积木,Command 是流水线,Command 还需平台支持(目前仅 Claude Code / Cowork)。

## 项目结构 - 9 大插件

1. **Product Discovery** — 产品发现:OST、假设识别、机会分析
2. **Product Strategy** — 战略:愿景、价值主张、商业模式
3. **Execution** — 执行(最多 16 项):PRD、OKR、路线图、Sprint
4. **Market Research** — 市场研究
5. **Data Analysis** — 数据分析
6. **Go-to-Market** — 市场进入
7. **Marketing Growth** — 营销增长
8. **Toolkit** — 工具包
9. **AI Delivery** — AI 交付(最新)

合计:**68 技能 + 42 命令**,覆盖产品全生命周期。

## 高价值 Skill 速查

| Skill 命令 | 作用 | 适用场景 |
|-----------|------|---------|
| `/interview-script` | 生成结构化访谈脚本(含 JTBD、满意度) | 用户调研启动 |
| `/opportunity-solution-tree` | 引导构建 Teresa Torres OST | 需求来源不明 |
| `identify-assumptions-existing` | 按价值/可用/可行/生存四维度揪出隐藏假设 | 产品复盘 |
| `/discover` | 完整产品发现 Command | 新需求立项 |
| `/product-strategy` | 9 部分战略画布 | 战略制定 |
| `lean-canvas` | 引导填完 Lean Canvas | 新业务设计 |
| `pricing-strategy` | 定价模型 + 竞品 + 弹性分析 | 定价决策 |
| `create-prd` | 8 部分 PRD 模板 | 文档输出 |
| `outcome-roadmap` | 功能列表 → 成果导向路线图 | 路线图重构 |
| `pre-mortem` | 项目启动期风险分析(Tigers/Paper/Elephants) | 立项评估 |

## 正文要点

- **"给文字"vs"给结构化执行路径"是 AI 工具的分水岭** —— 通用 ChatGPT 给的是要反复修改的模板,PM Skills 是 AI 主动提问、带你走流程的引擎
- **AI 工具成熟度看"领域方法论编码"** —— 模型差距已经收敛,真正差距在领域专家有没有把"做事路径"代码化
- **Slash Command 正在成为 AI Coding 事实标准** —— 从 Claude Code 起源,扩散到 OpenCode、Cursor、Cline,统一的交互层正在形成
- **AI 提问、用户决定 —— 这是边界不是缺陷** —— 刻意保留的决策点让 Skill 比"全自动写文档"更可靠
- **方法论壁垒被抬高** —— Skill 平民化了执行,会驾驭 Skill 的人价值跃迁,只会填模板的人加速淘汰
- **Skill 生态仍在 jQuery 插件时代** —— SKILL.md 协议有了,但分发、版本、依赖、命名空间都没解决
- **个人 Wiki 的下一步是"可调用"** —— 把开头钩子库做成 `/hook-anxiety`,把文章结构库做成 `/structure-discover-solve`

## 案例:用 `/interview-script` 做 OA 调研

- **背景**:作者要给企业级 OA 工作流系统做用户访谈调研
- **传统做法**:打开 ChatGPT,输入"帮我写一个用户访谈脚本",拿到通用模板,反复改"对电商怎么改"几轮才能用
- **PM Skills 做法**:OpenCode 中输入 `/interview-script` → AI 主动问"本次采访目的是什么" → 给出 OA 调研需求 → 一分钟后生成 `customer-interview-oa-workflow.md`,含 JTBD 问题、满意度等结构化内容
- **结果**:从"AI 给文字、人手动加结构"变成"AI 带流程、人填决策",时间从几轮迭代缩到一分钟

## 已知限制

- ❌ **Commands 仅 Claude Code / Claude Cowork 支持**,其他工具只能用 Skills
- ❌ **Windows 不稳定**
- ❌ **需要方法论基础** —— 不懂 OST、Lean Canvas 的人,AI 提问时答不上来
- ❌ **手动安装**,无统一 Marketplace(jQuery 插件时代,没有 npm)

## 我的理解

- 最触动我的点:**"AI 不替你做决定,只带你把方法论走一遍"** —— 这句把当前 AI 工具的合理边界讲清楚了,反对"AI 全自动生成"的盲目期待
- 对 MyAIWiki 的启发:本知识库 200+ 篇散文目前只能"读",下一步应该 Skill 化 —— `/hook-anxiety`(从钩子库挑焦虑共鸣型开头)、`/structure-discover-solve`(套用发现→方案结构)、`/find-relevant` (从 nodes 关联图谱中匹配相关条目)
- 对 Seetong-iOS 的启发:可以把"PRD 模板""BUG 复盘表""需求拆分 Checklist"做成项目内 Skill,接入 Claude Code 后产品/研发协作可以走 Slash command

## 适合关联的主题

- [[mattpocock-skills]]:领域专家把方法论做成 Skill 的同源案例
- [[Skill-Self-Evolution]]:Skill 自进化研究综述
- [[claude-code-large-codebase-best-practices]]:Claude Code Skill 在工程域的应用
- [[与AI一起做产品的六条原则]]:产品经理 AI 实践方法论视角
- [[AI-PM核心技能-观测评估与反馈闭环]]:产品经理 AI 工作流能力视角

## 安装

```bash
git clone https://github.com/phuryn/pm-skills.git

mkdir -p ~/.opencode/skills
cp -r pm-skills/pm-product-discovery/skills/* ~/.opencode/skills/
cp -r pm-skills/pm-product-strategy/skills/* ~/.opencode/skills/
cp -r pm-skills/pm-execution/skills/* ~/.opencode/skills/
# 其他插件类同
```

Claude Code 用户可直接享用 Commands;OpenCode 等其他工具只能用 Skills 部分。
