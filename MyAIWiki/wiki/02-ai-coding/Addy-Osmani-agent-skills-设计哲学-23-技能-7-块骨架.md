---
title: "Addy Osmani agent-skills 设计哲学:23 技能 + 7 块骨架 + 4 个杀手锏"
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Agent, #主题/Skill, #主题/工程实践, #主题/Harness, #节点/agent-skills, #节点/反合理化, #节点/统一骨架, #节点/渐进式披露, #节点/7命令流水线, #节点/Google工程文化, #手法/方法论, #手法/对比冲突, #公司/Addy-Osmani, #场景/工具推荐, #场景/方法论落地]
nodes: [agent-skills, AI-抄近路问题, 4个设计哲学, 7块统一骨架, 23技能全生命周期, 7命令流水线, 3角色4清单, Google工程文化整合]
links: [[谷歌开源agent-skills]], [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[Agentic-Engineering-AI-Workbench]], [[PM-Skills-Marketplace-产品经理必备skill]], [[APPSO-Codex-Claude-Code-Loop-Engineering]], [[从软件工程基本功到Agent落地:结合OpenClaw与Claude Code的实践理解]], [[从Prompt-Context到Harness-工程的三次进化与终局之战]]
date: 2026-06-15
source: 微信公众号 / ColaAI 2026-06-15 整理自 GitHub addyosmani/agent-skills v0.6.0(58.9k Stars)
---

# Addy Osmani agent-skills 设计哲学

- **项目地址**:https://github.com/addyosmani/agent-skills
- **原始作者**:Chrome 团队 Lead / Google 工程总监 Addy Osmani(@addyosmani)
- **项目快照(2026-06)**:⭐ 58.9k Stars | 🍴 6.4k Forks | ⚖️ MIT | 🔖 v0.6.0
- **本文来源**:微信公众号 ColaAI 2026-06-15 整理 https://mp.weixin.qq.com/s/ZU81MGzo5j0bwd6i7CfZCw
- **支持工具**:Claude Code / Cursor / Gemini CLI / Windsurf / OpenCode / Copilot / Kiro / Codex(纯 Markdown)

## 核心结论

agent-skills = 把"资深工程师工作流"打包成 23 技能 + 7 命令,治的是 AI 写代码"能跑但上生产就崩"的抄近路病;真正值钱的是**4 个设计哲学 + 7 块统一骨架**,不是技能数量。

**场景**:AI 编程 / Skill 架构 / 工程化方法论。**适合谁**:用 AI 写真实项目 / 受够"能跑就行" / 要给团队定规范的开发者。

## 知识节点(8 个独立概念)

- **agent-skills 项目**:Chrome 团队 Lead Addy Osmani 主理,58.9k Star,把资深工程师的工作流/质量关卡/最佳实践打包,纯 Markdown,支持 8+ 主流 AI 编程工具
- **AI 抄近路问题**:agent 默认走最短路径,跳过规格/测试/安全评审,能跑但上生产原形毕露——这是它要解决的核心矛盾
- **4 个设计哲学**:①流程而非文档 ②**反合理化**(每技能内置"借口→反驳"表,堵死偷懒退路)③验证不可妥协 ④渐进式披露(SKILL.md 入口 + 引用按需加载)
- **7 块统一骨架**:每个 SKILL.md 固定 7 节 —— 名称+描述 / 概述 / 何时使用 / 流程 / 反合理化 / 危险信号 / 验证;agent 理解一个就理解全部
- **23 技能覆盖全生命周期**:定义(3)→ 规划(1)→ **构建(7 重点)** → 验证(2)→ 评审(4)→ 发布(5)= 22 + 1 元技能
- **7 命令流水线**:`/spec` `/plan` `/build` `/test` `/review` `/code-simplify` `/ship` —— 对应开发全阶段,背后自动激活对应技能
- **3 角色 + 4 清单**:代码评审员 / 测试工程师 / 安全审计员(预设五维评审) + 测试 / 安全 / 性能 / 无障碍 4 张速查清单(按需加载不占上下文)
- **Google 工程文化整合**:Hyrum 定律 → 接口设计 / Beyoncé 规则 + 测试金字塔 80/15/5 → 测试 / 变更规模 ~100 行 → 评审 / Chesterton 栅栏 → 简化 / 主干开发 + 功能开关 → CI/CD

## 关联图谱

**上游**:Addy Osmani 2026-06-09 [[Addy-Osmani-Loop-Engineering]] Loop 方法论(本文是 Loop 在"工程化落体"维度的具象化);《Software Engineering at Google》(23 技能内嵌该书工程文化)。

**下游**:Claude Code / Cursor 等 8+ AI 编程工具的具体接入(仓库 docs 目录有每工具说明);任何想"给 AI 立规矩"的工程团队可复用 7 块骨架和 4 设计哲学。

**同级**:同主线 [[Addy-Osmani-Loop-Engineering]] + [[Loop-Engineering-详解-把反馈循环放进工程现场]] + [[APPSO-Codex-Claude-Code-Loop-Engineering]] —— 本文补"Skill 库是 Loop 的工程化落体"第四视角;同形态 [[PM-Skills-Marketplace-产品经理必备skill]] PM 域 Skill 库 + [[Agentic-Engineering-AI-Workbench]] AI 工作台;同设计 [[从Prompt-Context到Harness-工程的三次进化与终局之战]] Harness 层次 + [[从软件工程基本功到Agent落地:结合OpenClaw与Claude Code的实践理解]] 团队已有沉淀。

## 正文要点与借鉴动作(8+3 条)

1. **AI 写代码默认抄近路**:实现功能会用最短路径跑通,顺手跳过规格/测试/安全评审;能跑但上生产原形毕露
2. **23 技能 + 7 命令是入口/出口**:不用记 23 技能叫什么,记住 7 个动作就行;技能会按上下文自动激活
3. **4 个杀手锏最值钱**:①流程而非文档 ②**反合理化** ③验证不可妥协 ④渐进式披露
4. **7 块统一骨架是粘合剂**:每个 SKILL.md 7 节固定,23 个技能不散架靠的就是"理解一个就理解全部"
5. **3 角色是评审的"五维打分"**:代码评审员(看 staff 工程师会不会放行)/ 测试工程师(QA+先证明)/ 安全审计员(OWASP)
6. **4 清单是按需加载的上下文**:测试 / 安全 / 性能 / 无障碍 —— 平时不占上下文,技能调用时拉进来
7. **Google 工程文化直接嵌进流程**:Hyrum 定律 / Beyoncé 规则 / 测试金字塔 80/15/5 / 变更规模 ~100 行 / Chesterton 栅栏 —— 抽象口号变具体动作
8. **适配判断**:用 AI 写真实项目 / 受够"能跑就行" / 要给团队定规范 → 👍 适合;反之 → 🤔 不必

**对 Seetong / OpenClaw 借鉴 3 动作**:①Skill 7 块骨架审计——检查 30+ 现 Skill(seetong-prd/bug-triage/weekly-report 等)缺"反合理化""危险信号"的优先补;②`反合理化`列入团队 SKILL.md 必填项——5 个偷懒借口+标准反驳话术,补完后所有 Skill"不被跳过率"显著提升;③复用 7 命令到 Seetong 三端——`/spec /plan /build /test /review /code-simplify /ship` 接 [[seetong-tapd-version-review]] 工作流。

## 备注与链接

- **数据时效**:星标 58.9k 是 2026-06-15 抓取快照
- **评测缺口**:项目未公开"使用 23 技能 vs 不使用"的代码质量对照数据;**Seetong 可作首批 7 命令完整落地样板**
- **覆盖度**:7 命令覆盖开发全流程,未覆盖"上线后监控 / 客户反馈 / 数据回流"
- **项目**:https://github.com/addyosmani/agent-skills | **原文**:https://mp.weixin.qq.com/s/ZU81MGzo5j0bwd6i7CfZCw
- **旧版 wiki**:[[谷歌开源agent-skills]] 4-27(20 skills / 23k star)
- **同主线**:[[Addy-Osmani-Loop-Engineering]] | [[Loop-Engineering-详解-把反馈循环放进工程现场]] | [[APPSO-Codex-Claude-Code-Loop-Engineering]]
