---
title: 读完 Agent Loop 工程手册，我有 8 个还没想明白的问题
category: 01-ai-agents
tags: [#主题/Agent-Loop, #主题/SELF-Protocol, #主题/治理薄壳, #主题/护栏, #主题/Memory, #主题/Maker-Checker, #主题/多Agent拓扑, #节点/Stopping-Condition, #节点/Context自动拼装, #节点/失败转技能, #节点/pre-publish-review, #手法/二手解读, #手法/单样本复盘, #场景/Agent落地, #场景/Loop选题]
nodes: [Agent-Loop-范式, Stopping-Condition, Context-动态组装, 失败转输入, 六种多Agent拓扑, SELF-治理薄壳, Memory三层分级, pre-publish-review, 护栏分层, 理解力腐蚀]
links: [[Addy-Osmani-Loop-Engineering]], [[Loop-Engineering-详解-把反馈循环放进工程现场]], [[APPSO-Codex-Claude-Code-Loop-Engineering]], [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]], [[Skill-Self-Evolution]], [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[清华沈阳-自进化AI新物种]], [[Multica-AI-Native-组织-人是最慢的节点]]
date: 2026-06-16
source: 微信公众号 腾讯云开发者 / 陈进（https://mp.weixin.qq.com/s/DtQ0FfSpUxYdRR8XOvppaw）
---

# 读完 Agent Loop 工程手册，我有 8 个还没想明白的问题

> **核心结论**：Agent Loop 是范式跃迁（Prompt→Loop），但 8 个真痛点没标准答案；SELF Protocol 是一份"治理薄壳"草稿，专门回答 Loop 没展开的那一面：转起来之后怎么不胡说、不失忆、不重复踩坑。

- **原文链接**：https://mp.weixin.qq.com/s/DtQ0FfSpUxYdRR8XOvppaw
- **原始作者**：陈进（公众号 腾讯云开发者转载）
- **二手解读警告**：作者明示读的是社群手册和公开讨论（Reddit/X 220 万讨论量），未接触 Peter Steinberger / Boris Cherny 原始全文；SELF Protocol 是作者 30 天单 Agent 单样本实验
- **获取时间**：2026-06-16
- **分类**：01-ai-agents（Agent 工程落地讨论，容错+鼓励拍砖；不是 AI Coding 实战，放 02 不合适）

## 知识节点（10 个独立概念）
- **Agent-Loop-范式**：把人机协作单位从一次对话升到完整反馈回路；Loop = Automations + Worktrees + Skills + Plugins + Sub-agents + Memory + Guardrails
- **Stopping-Condition**：写循环前先定义"什么算干完了"——硬目标用"写测试通过"，软目标用诚实分级 disclaimer
- **Context-动态组装**：不是写出来的，是从失败日志 / 文件树 / 调用记录自动拼进下一轮
- **失败转输入**：把错误堆栈/截图/Diff 喂回下一轮；传统"出错就停"翻成"出错就学习"
- **六种多Agent拓扑**：顺序流水线 / 协调者-工作者 / 扇出合并 / 生成-验证 / 共享状态 / 辩论对抗（**作者亲测"辩论对抗"会越聊越自信→一致同意错的**）
- **SELF-治理薄壳**：不抢 Loop 位置，专治"转起来怎么不跑偏"；~1500 行 Python + Markdown 约定
- **Memory三层分级**：l0 一句话摘要 / l1 几条结论 / l2 全文；答关键问题前强制翻笔记
- **pre-publish-review**：发布前自检清单（链接真假 / 数据出处 / 未核实结论），SELF 三件套之一
- **护栏分层**：认知类护栏做成可插拔（迭代快），资源类护栏写死在 Loop 框架（红线该写死）
- **理解力腐蚀**：Loop 越自动，人对系统理解越浅；出 bug 时反而修不动（作者亲测：两周后读不懂自己写的 loop）

## 关联图谱
### 上游（基于 / 来自）
- Peter Steinberger（OpenClaw 创始人）"从写 Prompt 到设计 Loop"范式
- Boris Cherny（Claude Code 创始人）公开实践"我的工作已经变成写 Loops"
- Reddit/X 社群整理的 Agent Loop 工程手册（讨论量 220 万）

### 下游（应用于 / 验证于）
- SELF Protocol Knot Skill 33837 v1.6.7（作者 30+ 天单 Agent 实测）
- 8 个真痛点反哺 Loop 工程方法论（求评论区拍砖）

### 同级（横向 / 并列）
- [[Addy-Osmani-Loop-Engineering]] — 方法论原典（5+1 积木）
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] — 中文工程实操（6 工程问题 + 7 天试点）
- [[APPSO-Codex-Claude-Code-Loop-Engineering]] — 产业信号（4 人同向共振）
- [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] — Skill 是 Loop 的"每步不被跳过"
- [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] — 业务需求 Agent 的 4 层×8 步实操
- [[清华沈阳-自进化AI新物种]] — 自进化方向
- [[Multica-AI-Native-组织-人是最慢的节点]] — AI Native 组织样本
- [[Skill-Self-Evolution]] — Skill 自进化三大学派

## 正文要点 + 8 个真痛点
### 4 个值得琢磨的设计法
1. **Stopping Condition 第一**：模糊目标 = AI 自欺；可验证目标 = 真护栏
2. **Context 自动拼**：失败日志 / 文件树 / 调用记录动态组装
3. **失败是输入**：把错误堆栈/截图/Diff 喂回下一轮；与"出错就停"反过来
4. **6 种多 Agent 拓扑**：手册给的"模式词典"，看着场景挑

### 8 个真痛点（速查）
| # | 痛点 | 作者土办法 | 仍未解 |
|---|---|---|---|
| 1 | 软目标停止条件 | LLM judge + 诚实 disclaimer | judge 漂移（上午 0.85 / 下午 0.6） |
| 2 | Maker-Checker 同病 | 同模型 review 卡 | 不同模型？规则引擎？ |
| 3 | 护栏分层 | 认知可插拔 / 资源写死 | 这分法对不对？ |
| 4 | 记忆给多大 | 三层 l0/l1/l2 | 仍有失焦；token 截断 vs 相关性打分 vs 时间衰减？ |
| 5 | 理解力腐蚀 | 无 | 怎么对冲？ |
| 6 | 拓扑选型 | 试过"辩论对抗"更糊涂 | 哪些拓扑看着美用着崩？ |
| 7 | AI 一本正经胡说 | pre-publish review 清单 | 拦下 1 次，触发率不稳 |
| 8 | 多 Agent 成本 | 便宜模型路由 + 中间产物不进 Prompt + 限轮数 | 模型分级？压缩？缓存？ |

## 6 个对 Seetong 团队可借鉴动作
1. **Stopping Condition 优先**：写循环 cron（神策崩溃归类 / TAPD 过期迭代关闭 / 反馈去重）前先写"什么算做完了"
2. **fail-back 改造**：`isHaveStreamData=NO` 不重置 idle 计时器（4G 弹窗 6 大漏洞 #4）→ 失败转输入
3. **发布前自检清单**：iOS/Android/Harmony 发版前过 pre-publish review（链接真假 / 数据出处 / 未核实结论）
4. **诚实 disclaimer 三档**：周报/简报里强制标"论文级 / 工件级 / 计划级"——软目标不假装完成
5. **护栏分层**：OpenClaw 资源类护栏（maxTokens/timeoutSeconds）写死；认知类护栏（pre-publish）做成可插拔 Skill
6. **理解力腐蚀对冲**：Seetong 内部每 2 周选 1 个 loop 让真人手动跑一遍

## 备注 / 限制 / 相关链接
- **二手解读警告**：作者明示未接触原始全文——任何细节差异以原作为准
- **单样本无对照**：SELF 所有"有效"都是 30 天单 Agent 个人体感
- **8 痛点无标准答案**：整篇是抛问题不是给答案，作者"求评论区拍砖"
- **Close Beta 形态**：SELF 不是产品，是开放协议；当前是 Knot Skill 33837 v1.6.7
- raw 原文：[[2026-06-陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]]
- raw digest：[[2026-06-陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题-digest]]
- wiki digest：[[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题-digest]]
- Loop 主线四视角：[[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]] / 本文
- 治理/护栏延伸：[[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]（4 层×8 步）/ [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]]（Skill 库是 Loop 在工程化落体的形态）
