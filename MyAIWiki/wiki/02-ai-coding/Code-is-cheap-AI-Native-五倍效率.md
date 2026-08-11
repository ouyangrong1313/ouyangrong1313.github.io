---
title: Code is cheap - AI Native 研发范式
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 主题/Harness工程
  - 主题/AI-Native研发
  - 主题/代码廉价化
  - 主题/Seetong借鉴
nodes: code-is-cheap, harness定义, 水流理论, 最小混沌单元, 6种checkpoint动作, 5层safety-net, 复述机制, 代码廉价化4层级
links: [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]], [[02-ai-coding/AI-Coding的顿悟时刻]], [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]], [[01-ai-agents/Skill-Self-Evolution]], [[02-ai-coding/Addy-Osmani-Loop-Engineering]], [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]]
date: 2026-07-03
source: 微信公众号「无岳」2026-07-03 推送(阿里妹导读);原文链接 https://mp.weixin.qq.com/s/t04ysxZN2qEc3986r2gyTA
---

# Code is cheap - AI Native 研发范式

- **原文链接**:https://mp.weixin.qq.com/s/t04ysxZN2qEc3986r2gyTA
- **公众号**:无岳(阿里妹导读)
- **实际作者**:匿名的"AI 编码深度实践者"
- **发布时间**:2026-07-03

## 核心结论

> 代码正从稀缺资源变成可快速生成 / 验证 / 丢弃的过程产物——**Harness(人定方向,模型推进)** 是 AI Native 研发的核心工程化范式,把控制点从代码细节上移到边界 / checkpoint / 风险通道。

- **场景**:AI Native 研发的工程化方法论(0→1 + 1→N)
- **核心命题**:Code is cheap / Harness / 水流理论 / 最小混沌单元

## 知识节点(8 个独立概念)

- **code-is-cheap**:20 天 70 万行 10 项目,模型整包接住"读地形 + 定方案 + 写实现 + 跑验证 + 修 bug";Google 新代码 AI 生成占比上升 / Cursor-Devin 团队规模压缩都是外部佐证
- **harness定义**:Harness(挽具)= 人定方向,模型推进;不是把每一步写死规定模型,而是把控制点从代码细节上移到边界 / checkpoint / 风险通道;两个底层事实(概率生成器 + 上下文宝贵)逼出 Harness 设计
- **水流理论**:协作姿态——边界(堤坝)→ checkpoint(水闸)→ 风险通道(安全通道);区分"漫溢"(允许但持续观察)和"溃堤"(违反 spec / 越界 / 连续验证失败,必须转向或回炉)
- **最小混沌单元**:任务结构——小到可检查,大到可自治;配套 spec(决策持久化)/ codemap(代码地形摘要)/ new-chat(把累积噪音留在原地)三件上下文设施
- **6种checkpoint动作**:放行 9% / 追问 25% / **加料 47%(最高频)** / 绕道 5% / 回炉 2% / 阻止 <1%;加料占比近一半,反映 checkpoint 实质是"细颗粒控盘"——人更多时候是补约束 + 追问
- **5层safety-net**:① 自验(7 维报告)→ ② 自测(接口级闭环)→ ③ 他测(review agent + 测试同学端到端)→ ④ 自动化回归 + 巡检(CI/CD)→ ⑤ 灰度 + 金丝雀 + 一键回滚(线上兜底);越靠后越靠人 + 工程基础介入
- **复述机制**:同一动作两种用法——实施前反 slop(揉搓 + 复述 + 纠正,收搜索空间到 spec 级别)vs 实施中对抗 lost-in-the-middle(用 recency bias 反向把目标推回尾段)
- **代码廉价化4层级**:① 现象(代码可抛弃性,卫生纸)→ ② 工作方式(高速迭代压倒一切)→ ③ 实践姿态(经常不看代码,只看结果 + 证据)→ ④ 身份层(工程师价值结构迁移)

## 关联图谱

- **上游**:软件工程协作姿态 / SDD(Spec-Driven Development)/ Lost in the Middle 论文(Liu et al. 2023, Stanford)/ sdd-riper 项目 RIPER 五阶段门禁
- **下游**:Case A 0→1 项目 adaptive-room-harness(已开源)/ Case B 1→N"敏感资源外发审批"治理(Tair 两段式幂等 processing lock 60s + active pending 30min)/ 团队 Harness 能力 skills 化
- **同级**:[[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]] Harness 落地 / [[02-ai-coding/AI-Coding的顿悟时刻]] AI Coding 范式 / [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] Harness 14 步骨架 / [[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] SDD 主线 / [[01-ai-agents/Skill-Self-Evolution]] Skill 沉淀 / [[02-ai-coding/Addy-Osmani-Loop-Engineering]] Loop 验证 / [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]] Skills 工程实战 23.5→8 人日

## 正文要点(5 条)

**1. Code is cheap + 长尾放大**——作者 20 天 70 万行 10 项目;真正的差距不在"会不会用 AI",在"用到第几层";同公司头部能 5 项目并行,尾部还在补注释——以周为单位放大。两条路:① 抢先用 AI 还没标准产品化的能力 ② 成为 100% AI 工作者。

**2. 两个底层事实 + Harness 的设计哲学**——① 概率生成器(给自由空间越大越跑偏 → best-practice slop);② 上下文宝贵(transformer 注意力限制 + Lost in the Middle U 型分布 + recency bias)。Harness 直接针对这两点:概率偏差 → 收边界 + 拆小单元;上下文腐烂 → spec / codemap / new-chat 三件套。

**3. 水流理论 + 最小混沌单元协作**——水流理论管动作维度(checkpoint 反应 / 转向判断 / safety net 兜底);最小混沌单元 + 三件套管原料维度(任务粒度 / 上下文设施)。两者唯一接触点在 checkpoint——它产出的笔记(加料内容 / 追问澄清事实)沉淀回 spec 和 codemap。**没有水流理论,最小混沌单元退化成"切碎遥控";没有最小混沌单元,水流理论在过大搜索空间里迷失。**

**4. 6 种 checkpoint 动作 + 加料是最高频**——不是放行占主(9%)而是加料占主(47%);3 条转向硬规则:① spec 冲突 ② 越界 ③ 连续验证失败。Case A 0→1 转向 1-2 次,Case B 1→N 高频 4+ 次连环转向(质疑 / 约束注入 / 叫停 / 提假设)+ new chat 干净实施。

**5. 5 层 safety net + 工程师价值结构迁移**——一线从写代码 → 切任务包 + checkpoint + 看证据;TL 从评审 PR → 定 spec + codemap + 看 review agent 报告;架构师从设计模式 → 设计协作姿态 + 控制面 + Harness 工具集;**QA 从写测试 → 设计测试策略 + 端到端回归 + 抓 AI 想不到的 corner case——multi-layer safety net 里唯一不能被 AI 替代的人为底线。**

### 6 个对 Seetong 团队可借鉴动作

1. **Seetong 内部建 Harness 工程实战库**:把"边界 + checkpoint + 验证"作为新员工入职培训和 Tapd 任务评审 checklist
2. **水流理论用在 Seetong AI 助手**:6 种 checkpoint 动作比例透明化;模型复述目标放在尾段对抗 lost-in-the-middle
3. **最小混沌单元用在 1007107 修复**:每个 commit 一个可验单元;spec 沉淀到 docs/specs/<日期>_<功能>.md
4. **spec 持久化建仓**:TAPD 需求关联的 spec 落本地文件(不只在 TAPD 描述里),跨 session 接得上;new-chat 是 clean restart 关键
5. **多层 safety net 应用到 iOS release**:5 层(单测 / UI 自动化 + pre-commit Hooks / 自动化巡检 + Crash 监控 / 灰度 + 金丝雀 + 一键回滚);8.3.13.4 灰度前夜清单
6. **代码作为卫生纸的边界判断**:权限 / 支付 / 安全 / 数据删除路径不在范围内(严格 review),其他按可抛弃处理(灰度兜底)

## 备注与限制

- 70 万行 / 6 种动作占比是作者自报口径,未独立验证
- "阿里妹" 是本公众号(无岳)内容策划导读,实际作者身份匿名
- Case A(adaptive-room-harness)已开源;Case B 是脱敏企业内部案例,触发链路 / 状态机 / 幂等策略保留真实结构
- "代码是卫生纸" + "不看代码"都有硬边界:权限 / 支付 / 安全 / 数据删除路径,基础库 / SDK / infra 核心,隐式 contract 多 / 测试覆盖差的老系统,没有灰度和回滚机制的线上改动——这些不适合这样玩
- Harness 直译"挽具",指人给模型套上约束 / 方向后让它推进的工程姿态
- 与 02-ai-coding 主线(Harness / SDD / Skill / Loop / Skills 实战)形成"AI Coding 完整闭环"