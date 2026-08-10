---
title: 别再反复教 Coding Agent——让项目记住自己如何工作的五个步骤
category: 02-ai-coding
tags: [#主题/Coding-Agent #主题/项目记忆 #主题/AGENTS-md #主题/Skill设计 #主题/CLI设计 #主题/Harness #主题/Loop-Discovery #主题/Seetong借鉴 #作者/Phodal]
nodes: [AGENTS-md项目地图, 渐进式披露, 文档任务路由, Skill探索门槛, CLI优先MCP兜底, Agent-Work-Loop, Loop-Discovery沉淀决策树, 写进仓库不等于实践生效]
links: [[phodal-Better-Harness-任务级证据评估]], [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]], [[面向Skills编程-淘宝企业购端到端研发提效实践]], [[loonggg-Claude-Code-技能心法-11条建议]], [[Agent自维护体系-完整实战]], [[腾讯-AI-Agent-Skill-测评方案落地]], [[lencx-Agent开发指南-技术太多-该怎么学]], [[Skill-Self-Evolution]], [[Loop-Engineering-验证才是瓶颈]], [[54万行代码的顿悟-Markdown才是新编程方式]], [[AI-Coding的顿悟时刻]]
date: 2026-08-03
source: 微信公众号 / Phodal（原文链接 https://mp.weixin.qq.com/s/1FrHNkfVpp8CE7keWt_lbQ）
---

# 别再反复教 Coding Agent——让项目记住自己如何工作的五个步骤

- 原文链接：https://mp.weixin.qq.com/s/1FrHNkfVpp8CE7keWt_lbQ
- 作者：Phodal（Better Harness / QoderAI；同作者 7/28 已编 [[phodal-Better-Harness-任务级证据评估]]）
- 仓库：https://github.com/QoderAI/better-harness
- 发布时间：推断 2026-08 / 获取时间：2026-08-03 10:29 / 原文约 4346 字

## 核心结论与分类

> 让 Coding Agent 不被反复教的关键，是让项目自己记住经验——AGENTS.md 给地图、文档接到任务路径、Skill 提炼重复工作、CLI 优先于 MCP、Agent Work Loop + Loop Discovery 让经验沉淀回流。

- 场景：AI Coding 项目工程化 / Agent 友好型项目结构化
- 类型：方法论 + 落地 SOP
- 主线：02-ai-coding / Skill 设计 + Harness 工程化
- 同作者姊妹篇：[[phodal-Better-Harness-任务级证据评估]]（7/28）——本文是 Better Harness 落地的"项目侧"篇，7/28 是"评估侧"篇

## 知识节点（8 个独立概念）+ 正文要点（5 条）

- **节点 1 AGENTS.md 项目地图：** 根目录放入口/命令/风险/文档导航；不是百科，是新人第一天进项目拿到的那张纸。
- **节点 2 渐进式披露：** 根目录 AGENTS.md 只放多数任务都需要的说明，详细架构/设计/工作流通过链接按需读取；Agent 能从代码看出来的不必写，写"它看不出来、却很容易猜错的事实"。
- **节点 3 文档任务路由：** 文档从"仓库里存在"变成"任务进行到这里时能够被找到"——更有效的写法不是链接列表，而是"修改模块边界前，阅读 ARCHITECTURE.md"这种带读取条件的小句。
- **节点 4 Skill 探索门槛 6 条：** 相似需求 ≥ 2 次 / 高成本高风险 / 输入稳定 / 步骤复用 / 结果可检查 / 不与现有重复——六条缺一不可。
- **节点 5 CLI 优先 MCP 兜底：** Agent CLI 六条（help 发现 / 非交互 / 稳定输出 + JSON / 明确错误退出码 / 超时 / dry-run）；CLI 与 MCP 建立在同一套底层能力和权限规则上。
- **节点 6 程序判断归脚本/Hook/CI：** 能被程序明确判断的规则（如禁止修改生成文件）不交给 Skill 提醒；生产/凭据/不可逆操作保留权限边界与人工确认。
- **节点 7 Agent Work Loop 五段：** 理解需求→找到知识→执行修改→验证交付；AGENTS.md 帮进入、核心文档提供上下文、Skill 与工具推动执行、测试/Hook/权限守住边界。
- **节点 8 Loop Discovery 沉淀位置决策树：** 反复出现的摩擦和有效经验才是下一轮改进起点——稳定事实→AGENTS.md / 重复方法→Skill / 确定性操作→CLI 脚本 Hook CI / 外部资源发现→MCP / 高风险→人工（不沉淀）。

正文 5 句要点：① 项目成长 4 阶段表格（开工→知识路由→重复方法→持续改进），新增内容按这张顺序填；② AGENTS.md 是地图不是百科；③ Skill 探索门槛 6 条缺一不可；④ CLI 优先 MCP 兜底（CLI 六条 + 程序判断归脚本）；⑤ 写进仓库 ≠ 实践生效，下一次任务 Agent 能否用上是唯一检验标准。

## 关联图谱

- **上游：** [[phodal-Better-Harness-任务级证据评估]]（同作者 7/28，对偶必读）[[lencx-Agent开发指南-技术太多-该怎么学]] [[Skill-Self-Evolution]] [[Loop-Engineering-验证才是瓶颈]]
- **下游：** [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] [[面向Skills编程-淘宝企业购端到端研发提效实践]] [[loonggg-Claude-Code-技能心法-11条建议]] [[Agent自维护体系-完整实战]] [[腾讯-AI-Agent-Skill-测评方案落地]]
- **同级：** [[54万行代码的顿悟-Markdown才是新编程方式]] [[AI-Coding的顿悟时刻]] [[Task-类型到验证模板]]

## 6 个对 Seetong 团队可借鉴动作

1. **AGENTS.md 体检：** 6 个 Seetong 主仓库（iOS/Android/Harmony/SDK-Net/SDK-PlayCtrl/Seetong-AI 助手）按"安装/测试/不修改/导航/边界"5 项打勾，缺项优先补。
2. **文档任务路由化：** `wiki/{分类}/index.md` 升级为"读取条件小句"而非链接列表——"改 iOS 端业务前，先读 [[Seetong-iOS-架构地图]]"。
3. **Skill 探索门槛硬约束：** Seetong AI 助手新增 Skill 走 6 条门槛，**任一条不满足则不沉淀 Skill**，直接在 SKILL.md 注明"未达沉淀门槛，临时使用"。
4. **内部 CLI 优先 MCP：** 神策/TAPD/Git/友盟运维脚本按 Agent CLI 六条升级（`--json` / `--dry-run` / 退出码 / 超时），让 Seetong AI 助手直接调用。
5. **Loop Discovery 月度复盘：** 每月 1 次回顾——哪个 Skill 帮了 ≥ 2 次任务 / 哪个应下架 / 哪个 Hook 拦截了真实风险，按 5 类沉淀位置决策调整。
6. **Skill 用上率检验：** 每个新 Skill 上线 30 天评估"触发次数 / 解决问题次数 / 返工减少次数"，0 项达标 = 改为临时 Skill 或下架。

## 备注与限制

1. **作者来源：** Phodal，公众号名未在 HTML meta 暴露；按内容与 Better Harness 仓库作者一致。
2. **发布时间：** 推断 2026-08。
3. **关联首选：** 与 [[phodal-Better-Harness-任务级证据评估]]（同作者 7/28 编译）形成"评估 / 落地"对偶，**两文应一起读**。
4. **可证伪点：** "相似需求 ≥ 2 次"是经验门槛非可量化阈值；Seetong 30-50 人小团队建议改为"≥ 3 次"更稳。
5. **不适用：** 一次性项目 / 1 人小工具 / 教学 Demo——本文最小单元（入口/命令/风险/导航 4 项）才能落地。