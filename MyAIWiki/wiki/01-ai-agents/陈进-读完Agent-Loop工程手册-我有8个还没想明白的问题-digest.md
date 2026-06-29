# 读完 Agent Loop 工程手册，我有 8 个还没想明白的问题 · Digest

## 一句话总结
> **Agent Loop 是范式跃迁（Prompt→Loop），但 8 个真痛点没标准答案；SELF Protocol 是"治理薄壳"草稿，专治"转起来怎么不跑偏"。**

## 速查表

### 范式 4 件
- **Stopping Condition 第一**：写循环前先写"什么算干完了"
- **Context 自动拼**：失败日志 / 文件树 / 调用记录动态组装
- **失败是输入**：错误堆栈喂回下一轮，"出错就停"翻成"出错就学习"
- **6 种多 Agent 拓扑**：顺序流水线 / 协调者-工作者 / 扇出合并 / 生成-验证 / 共享状态 / 辩论对抗

### SELF vs Loop 5 件套
| 件套 | Loop 自带 | SELF 补强 | 评估 |
|---|---|---|---|
| Memory | Markdown/DB | l0/l1/l2 三层 + 答前翻笔记 | 仍有失焦 |
| Sub-agents | Maker-Checker | 单 Agent review 角色卡 | 同模型盲区共存 |
| Guardrails | 资源类 | + 认知类 | 拦 1 次，触发率不稳 |
| Skills | 可复用指令 | + 失败转技能 | 30 天 9 条，同类仍犯 |
| Stopping | 硬目标 | 软目标 + 诚实 disclaimer | 治不了软目标 |

### 8 个真痛点（速查）
| # | 痛点 | 土办法 | 仍未解 |
|---|---|---|---|
| 1 | 软目标停止 | LLM judge + disclaimer | judge 漂移（0.85→0.6） |
| 2 | Maker-Checker 同病 | 同模型 review | 不同模型？规则？ |
| 3 | 护栏分层 | 认知可插拔 / 资源写死 | 分法对不对？ |
| 4 | 记忆大小 | 三层 l0/l1/l2 | 仍有失焦 |
| 5 | 理解力腐蚀 | 无 | 怎么对冲？ |
| 6 | 拓扑选型 | "辩论对抗"更糊涂 | 哪些看着美用着崩？ |
| 7 | 一本正经胡说 | pre-publish review | 拦 1 次，触发率不稳 |
| 8 | 多 Agent 成本 | 便宜路由 + 中间产物不进 Prompt + 限轮数 | 模型分级？压缩？ |

### 反直觉点
- "辩论对抗"两个 Agent 会越聊越自信 → 一致同意错的
- 同底模 Maker-Checker 盲区高度重合，B 把 A 的 off-by-one 标 PASS
- LLM judge 评分会随时间漂移（上午 0.85 / 下午 0.6）
- Loop 越自动，人对系统理解越浅
- SELF 治不了软目标，但至少不会假装"完成了"

### 核心金句
- "别再死磕 Prompt 怎么写了，去设计一个能让 AI 自己转起来的循环（Loop）。"
- "模糊的目标会让 AI 自欺欺人，可验证的目标才是真护栏。"
- "Agent Loop 教我怎么让 AI 自己转起来，SELF 是我回答转起来怎么不跑偏的那一层薄壳——前者是骨架，后者是润滑层。"

## 对 Seetong 团队 6 个可借鉴动作
1. **Stopping Condition 优先**：写循环 cron 前先写"什么算做完了"
2. **fail-back 改造**：`isHaveStreamData=NO` 不重置 idle 计时器 → 失败转输入
3. **发布前自检清单**：iOS/Android/Harmony 发版前过 pre-publish review
4. **诚实 disclaimer 三档**：周报/简报里强制标"论文级/工件级/计划级"
5. **护栏分层**：OpenClaw 资源类护栏写死，认知类护栏做可插拔 Skill
6. **理解力腐蚀对冲**：每 2 周选 1 个 loop 让真人手动跑一遍

## 关联
- **上游**：Peter Steinberger "从 Prompt 到 Loop" / Boris Cherny 公开实践 / Reddit 220 万讨论
- **同级 Loop 主线四视角**：[[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]] / 本文
- **治理/护栏延伸**：[[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] / [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] / [[Skill-Self-Evolution]]
- **AI Native 组织**：[[Multica-AI-Native-组织-人是最慢的节点]] / [[清华沈阳-自进化AI新物种]]

## 备注
- **二手解读**：作者明示未接触 Peter Steinberger / Boris Cherny 原始全文
- **单样本无对照**：SELF 30 天单 Agent 个人体感
- **8 痛点无标准答案**：整篇是抛问题不是给答案
- **Close Beta**：SELF 不是产品，是开放协议
