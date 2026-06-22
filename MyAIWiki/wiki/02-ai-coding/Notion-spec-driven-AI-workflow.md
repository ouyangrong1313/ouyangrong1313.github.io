---
title: "规范驱动开发：Notion 的 AI 工程工作流程丨How I AI"
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Native, #主题/SDD, #主题/Harness, #主题/工程管理, #主题/DevX, #节点/规范驱动开发, #节点/Spec, #节点/Notion-AI, #节点/Codex, #节点/Code-Review, #节点/验证闭环, #手法/案例拆解, #手法/反例论证, #场景/编译长文, #场景/工程团队]
nodes: [Spec-driven-Development, Whisper-Codex流水线, 救CI, Standup-Prep自动化, Boxy-@Codex出PR, 我不懂PR评审, Spec-Verification可执行资产, 工程师角色重构]
links: [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]], [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]], [[AI-Coding的顿悟时刻]], [[Claude-Code团队5条工作原则-Fiona-Fung分享]], [[Claude-Code负责人谈AI原生工程组织]], [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]], [[54万行代码的顿悟-Markdown才是新编程方式]]
date: 2026-06-09
source: 微信公众号 / Capihom（编译自 Latent Space《How I AI》播客，嘉宾：Notion 工程师 Ryan Nystrom）
---

# 规范驱动开发：Notion 的 AI 工程工作流程丨How I AI

- 原文链接：https://mp.weixin.qq.com/s/3tD61I6xLWpjoOrF6goewA
- 原始来源：Latent Space《How I AI》播客（嘉宾：Ryan Nystrom，Notion 工程师 / Notion AI & Custom Agents 核心建设者）
- 来源：微信公众号 / Capihom（编译）
- 发布时间：2026-06-08 22:00
- 获取时间：2026-06-09

## 核心结论（一句话）

> **Spec-driven development 不是给团队平白多一层负担，而是把"原本就在做但停在会议等待区的设计文档"第一次变成 agent 的施工说明书和可执行工程资产**——Ryan 在 Notion 已经跑通"Whisper 说意图 → Codex 写 spec → @Codex 出 PR + 验证截图 → spec 进仓库做 change log"的完整流水线。

## 分类提炼

- **场景**：AI-Native 工程团队 / Spec 驱动的研发流水线 / 工程师角色重构
- **标签**：#主题/AI-Coding #主题/SDD #主题/Harness #主题/DevX
- **类型**：实战案例 / 编译长文 / 播客精炼
- **价值层级**：⭐⭐（一线 AI-Native 团队的真实流水线，与 [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] [[AI-Coding的顿悟时刻]] [[Claude-Code团队5条工作原则-Fiona-Fung分享]] 互为镜像）

## 知识节点（8 个独立概念）

- **Spec-driven Development**：文档驱动实现的工作流范式——spec 不再是会议材料，而是写进仓库、带着代码指针 / 行为说明 / 验证计划的工程文档；spec 进版本控制后兼具 change log 功能
- **Whisper→Codex Spec 流水线**：用语音先说出"功能该怎么工作" → 交给 Codex 写 spec → 指向 spec 说"Build it"；入口用"5 岁小孩都能懂"的 prompt 逼出隐含步骤
- **救 CI / DevX**：AI 编程时代慢 CI = "一次等待卡住整个验证回路"，速度问题直接变 AI 采用问题；Notion Afterburner 项目目标把 CI 时间压到 1/4
- **Standup Prep 自动化**：Notion AI custom agent 拉 24h Slack + 关闭任务 + 合并 PR + 昨天会议 + Honeycomb MCP 指标，按预定义格式生成 preread 发 Slack；高频会议没消失，低质量汇报先被淘汰
- **Boxy / @Codex 出 PR**：装好 Codex + Claude Code 的小型 VM 集群；工程师在 Notion 任务评论里 @Codex 写需求/截图/边角 → 10 分钟出 PR + preview + 自带测试说明 + UI 验证截图
- **"我不懂" PR 评审**：新 code review 模式——承认"不懂"发给 agent 是有效 debug，发给人是社交灾难；Codex 直白语气 > Claude Code 温柔语气；code review 从社交阻力里拽出来
- **Spec Verification / 可执行资产**：spec 底部明确写 verification（测试怎么过 / CLI 怎么跑 / agent 怎么被拉起 / 应该看到什么结果）；spec 进版本控制 = change log；配套 CLI 支持 ask mode / 普通模式切换 + 交互转录可复盘
- **工程师角色重构（系统思考者 + 架构师）**：重心从手工 plumbing 挪到"场景边界 / spec 写实度 / 验证回路 / agent 自证工具"；6~7 人小团队也能跑 AI-native 流程

## 关联图谱

### 上游（基于 / 来自）
- 原始素材：Latent Space《How I AI》播客 S2E?，嘉宾 Ryan Nystrom
- 同源案例基础：Notion AI / Custom Agents 团队的实战沉淀

### 下游（应用于 / 验证于）
- [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]：从工具/方法论视角做对照——Spec-Kit 拉上限(强秩序) / BMAD 拉下限(角色化+圆桌) / Notion 这条是"已经跑通的活案例"
- [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]]：SDD 工具谱系中的 Notion 实战坐标
- [[AI-Coding的顿悟时刻]]：Spec→LDD 流水线、工程师角色向两端收缩的"组织层/个人层"印证
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]：瓶颈转移到验证/评审/安全 + JIT 规划 + 团队级 harness——Notion 这条把"验证前置 + spec 驱动"做了完整工程化落地
- [[Claude-Code负责人谈AI原生工程组织]]：AI 原生组织的另一种描述口径
- [[YC如何进行AI-Native组织改造-Agent能力要向所有人开放]]：Egalitarian + Trust by default 的组织层注脚
- [[54万行代码的顿悟-Markdown才是新编程方式]]：Markdown 是新编程方式 + Tokenmaxxing 的"个人层"版本

### 同级（横向 / 并列 / 镜像）
- [[Anthropic万字长文三个判断和一个阳谋]]：执行力的零价格 / 验收能力——本篇是"验收能力"的一线落地版
- [[买了一样的AI为什么别家的比你的强]]：skill 沉淀视角——本篇的 spec 仓库 = 一种"组织级 skill"
- [[为什么说React是比HTML更合适的AI设计稿格式]]：结构化文本优先——spec 进仓库与 React 组件化是同一精神

## 正文要点（8 条）

### 一、先说清楚，再写代码（Whisper→Codex 入口）

Ryan 开 prompt 时常挂一句："我真的不知道这里在干什么，你得像给 5 岁小孩讲一样解释给我听。"——这种自爆"不懂"的话，对 agent 是有效输入（逼出隐含步骤），对人则容易变成情绪和防御。

做功能的入口不再是 IDE，而是 Whisper + 空白 markdown：先把"这个功能该怎么工作"一口气说出来，语音丢给 Codex 写 spec，再指向 spec 文件说"Build it"。Ryan 的判断很明确：文档还会继续写，只是文档第一次真正开始驱动实现，"先说清楚"第一次变成可复用的流水线。

### 二、AI 时代先要救 CI（DevX / 跑道）

Ryan 在 Notion 带 6~7 人小团队，目标把 CI 时间压到当前 1/4（项目名 Afterburner）。他坦白自己不是 CI 专家，但知道慢 CI 在 AI 编程时代会把整个组织拖住。

关键判断：**以前构建慢，最多是工程师多等几轮；现在背景 agent、Codex、Claude Code 并行跑任务，一次等待会卡住整个验证回路，速度问题会直接变成 AI 采用问题。** Claire Vo 补刀：大团队如果还没自己的 VM 策略和背景 agent 策略，现在就该补这堂课。

### 三、Standup Prep 从手工抄状态变成自动汇总

Notion AI custom agent 后台流程：读 24h Slack + 关闭任务 + 合并 PR + 昨天会议 + Honeycomb MCP 指标 → 按 Ryan 预定义格式生成 preread → 发回 Slack。严格限权：只读项目数据库，不动全公司任务表。

会议也随之变样：团队不再按人轮流念"我今天做了什么"，而是围着一份已经聚好上下文的材料直接讨论问题/决定取舍/确认下一步。**高频会议没有消失，低质量汇报先被淘汰了。**

### 四、20 分钟省下的，是反复切上下文的损耗

很多人把自动化想成"每天节省 5 小时"的宏大叙事，Ryan 真正获得的往往只是每天 20 分钟。但那 20 分钟原本最伤人的部分不是时长，是反复切上下文——在 Slack / GitHub / 任务表 / 会议口气之间折返。AI 没有替 Ryan 做战略判断，却把这段最耗神的搬运活接走了。

另外，自动 prep 也是 burnout 保护：会议前整理最没成就感，最容易让人提前疲惫。AI 没造神话，只是把"人肉拼接状态"收掉，让高频会议终于像会议，而不是一场集体抄作业。

### 五、在 Notion 评论里 @Codex，10 分钟换 PR + 预览地址

Boxy = 装好 Codex + Claude Code 的小型 VM 集群。工程师不必先在本地拉环境，而是直接在 Notion 任务评论里 @Codex 写需求/截图/边角。

案例：tab block 加 "copy link to tab"。Ryan 写了 4 句描述 + 1 张截图 + 几个边角 URL，10:40 开始 → 10:51 实现 → 再 10 分钟，PR 链接和 preview URL 回来了。**关键不是"生成几百行代码"，而是 agent 附上了自己的测试说明和 UI 验证截图**——闭环跟着代码一起出现，工程师没离开主工作流，却把外包对象从人换成了 agent。

### 六、新世界代码评审：先说"我听不懂"

PR 里有一处类型相关改动，Ryan 看不懂，直接留言："我不知道这里在干什么，这不太对。"发给 agent，对方没介意，回了段解释并顺手修了类型问题。

Ryan 甚至故意把 prompt 写得很直白，因为只有先承认"不懂"，才会逼 agent 把隐含步骤摊开。Claire 调侃 Codex 没有 Claude Code "嘿朋友我替你搞定了"的温柔语气，Ryan 反倒喜欢。**在他看来，code review 最稀缺的是把事情快速讲清楚。** AI 没有取消 code review，它把 code review 从社交阻力里拽了出来。

### 七、Spec 进仓库，文档第一次成为可执行资产

那份 spec 已超出简短需求说明的范围：写进仓库、带着代码指针 + 行为说明 + 验证计划。文档底部明确写 verification：测试怎么过 / CLI 怎么跑 / Notion AI 怎么被拉起 / 要向它发哪些查询 / 最后应该看见什么结果。Ryan 第一次完整跑下来花了几个小时，回来做 code review，自己又玩了一遍才放行。

> "spec 就是事实来源。"

进版本控制后，Ryan 可以回看 spec 演化，等同于 change log。代码当然有历史，但纯代码很难让市场/运营/其他团队快速理解"这项能力现在到底怎么工作"——写进 repo 的 plain English 文档，agent 能读，工程师能查，别的团队也能拿去转成对外说明。

配套 CLI：让 agent 在 ask mode 和普通模式之间切换 + 交互转录可复盘。Ryan 的总结：**过去设计文档停在会议等待区里，现在它们第一次真的变成了工程资产。**

### 八、工程师角色重构：系统思考者 + 架构师

Ryan 自己"管人 + 继续写代码"，但重心已经挪到：
- 场景边界有没有想清楚
- spec 有没有把行为写实
- 验证回路是否足够硬
- agent 在不确定时有没有工具自证

> **"如果验证还是模糊的，第一件该补的是让 agent 能自己跑起来的工具，把自测链路先搭出来，再回头打磨 prompt。"**

Ryan 拆掉常见误解：spec-first 没平白多一层负担——技术设计文档 / 规格说明 / 实现讨论以前本来就在写，只是写完后要排会、等 review、再实现。现在人的注意力被推到了更值钱的位置，文档从理论材料变成执行入口。

Claire 结尾的复盘（Ryan 认可）：
- 别再手工准备会议
- 从你最常工作的地方直接 @ 背景 agent
- 把 spec 放进 repo，改功能时先改 spec，再让 agent 回头改代码

## 写给团队的可借鉴动作（今天就能试）

| 起点动作 | 期望打通 | 阻力 |
|---|---|---|
| standup 预读 | 把"会议前 20 分钟"从抄状态变成决策 | 低 |
| Notion 任务评论 @Codex 触发 PR | 把"小需求"从排期变成 10 分钟闭环 | 中（需后台 VM 基建） |
| 把老设计文档改写成可执行 spec | 让设计文档第一次能驱动实现 | 中（习惯阻力） |
| 给 agent 搭"自测链路"（CLI + 验证脚本） | 让验证回路变硬 | 中（DevX 投入） |

Ryan 的建议：**先打通一小段，再把整条链路慢慢换掉，阻力会小很多，团队也更容易跟上。**

## 关键术语索引

- **Spec** / **Spec-driven Development**（规范驱动开发）：本文核心范式
- **Whisper**（OpenAI 语音转文字）：Ryan 的入口工具
- **Codex**（OpenAI 代码 agent）：本文主力 agent
- **Boxy**（Notion 内部项目）：装好 Codex + Claude Code 的小型 VM 集群
- **Afterburner**（Notion 内部项目）：CI 时间优化到 1/4
- **Honeycomb MCP**：可观测性平台 MCP 接入
- **ask mode** / **普通模式**：Notion 内部 CLI 切换的两种 agent 交互模式
- **Ryan Nystrom**：Notion 工程师 / Notion AI & Custom Agents 核心建设者 / 本篇核心信源

## 写作引用建议

- 引用本篇时优先用：spec 是 agent 的施工说明书 / 一次等待会卡住整个验证回路 / 速度问题直接变 AI 采用问题 / 高频会议没消失，低质量汇报先被淘汰 / code review 从社交阻力里拽出来
- 与本篇强关联的引用方向：[[AI-Coding的顿悟时刻]]（"未来瓶颈 = 需求定义 + 架构设计"） / [[Anthropic万字长文三个判断和一个阳谋]]（验收能力） / [[Claude-Code团队5条工作原则]]（瓶颈转移到验证/评审/安全）
