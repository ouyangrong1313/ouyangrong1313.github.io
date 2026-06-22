---
title: Claude Code 首席设计师的 AI 工作流:从并行到自动巡逻,人只在判断环节介入
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/AI-Native, #主题/Anthropic, #主题/Harness, #主题/工作流设计, #节点/Worktree并行, #节点/AI自决给理由, #节点/全链路自动化, #节点/AI自动巡逻, #节点/Auto模式+Loop, #节点/Opus1M上下文, #节点/AI设计边界, #节点/先把流程搭好等模型升级, #手法/方法论, #手法/反例论证, #场景/编译长文, #场景/Anthropic一手]
nodes: [Worktree并行, AI自决给理由, 全链路自动化, AI自动巡逻, Auto模式+Loop, Opus1M上下文, AI设计边界, 先把流程搭好等模型升级]
links: [[Claude-Code作者Boris-我已经不写prompt了我写loop]], [[Claude-Code之父品味不是人类护城河]], [[Claude-Code团队5条工作原则-Fiona-Fung分享]], [[Addy-Osmani-Loop-Engineering]], [[Agentic-Engineering-AI-Workbench]], [[买了一样的AI为什么别家的比你的强]], [[多Agent使用边界与并行判定]], [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
date: 2026-06-10
source: 微信公众号 / loonggg(编译自 Anthropic Claude Code 首席设计师 Meaghan Choi 演示)
---

# Claude Code 首席设计师的 AI 工作流:从并行到自动巡逻,人只在判断环节介入

- 原文链接:https://mp.weixin.qq.com/s/_WaCCvZ0FgMQiJ1PSVOMwA
- 原始作者:loonggg(微信公众号)
- 演示来源:Meaghan Choi(Anthropic,Claude Code 首席设计师)
- 来源:微信公众号 / loonggg
- 发布时间:2026-06-09 11:30
- 获取时间:2026-06-10

## 核心结论(一句话)

> **Anthropic Claude Code 首席设计师 Meaghan Choi 的日常 AI 工作流 6 条核心:①worktree 并行(同时开 4-5 个 Claude)②让 AI 自己做初判并给理由 ③不只让 AI 写代码,所有重复性工作全扔出去(commit / PR / Slack)④用定时任务让 AI 自动巡逻代码与产品质量 ⑤AI 现阶段做不好设计,人把控方向 ⑥始终开 Opus + 1M 上下文 + auto + loop,能自动化的全自动化,人只在判断环节介入。**

## 分类提炼

- 场景:Anthropic 内部工作流 / 个人 AI 工作流 / 团队 AI 化
- 标签:#主题/AI-Coding #主题/Anthropic #节点/Worktree并行 #节点/Auto模式+Loop
- 类型:方法论 / 一手观察 / 跨职能自动化

## 知识节点(8 个独立概念)

- **Worktree并行**:Anthropic 工程师日常同时开 4-5 个 Claude 窗口;worktree 给仓库创建隔离副本,让并行 Claude 互不打架
- **AI自决给理由**:`/prototype` 自定义技能让 Claude 选一个方案并解释为什么;初判也交给 AI,人只做最终确认
- **全链路自动化**:不只是写代码,所有重复性工作(commit / PR / 截图 / Slack 通知 / 简单修复)都交给 AI;小修复随手发云端任务,自动变成代码提交,改动小的自动过审上线
- **AI自动巡逻**:定时任务让 Claude 每天扫描前端改动,检查设计师是否参与过(Slack / 会议纪要 / 文档);没参与就自动生成替代设计 + 打包 PR + 私信工程师
- **Auto模式+Loop**:auto 模式分类器自动判断风险,没风险直接执行;loop 让 Claude 自己循环执行到完成;不再反复问"可以吗?确认吗?"
- **Opus1M上下文**:始终用 Opus 模型 + 1M 上下文窗口 + auto 模式 = Claude Code 推荐的"高交互"配置组合
- **AI设计边界**:AI 现阶段做不好设计(Claude 自己也承认);审美 / 产品决策 / 质量把控仍要人做;门槛降低反而要求标准不降低
- **先把流程搭好等模型升级**:即便 AI 能力不够(比如自动发消息质量差被关掉),整套流程保留着,等下一代模型直接接上 = 永远不浪费自己搭好的工作流

## 关联图谱

### 上游(基于 / 来自)

- [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - "写 Loops" 是 AI Coding 下一阶段,本文"auto + loop"是同一信号的 Claude Code 内化版
- [[Claude-Code之父品味不是人类护城河]] - Boris 谈品味被模型侵蚀,Meaghan 谈当下 AI 设计仍不够好,两者互补 = "AI 边界今天在哪,明天会移动到哪"
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]] - "Trust but verify" 规则的 AI 监控化 = 同一个 Anthropic 内部思路的不同切面
- [[Addy-Osmani-Loop-Engineering]] - 5+1 积木(auto / worktree / skill / mcp / sub-agent / memory)与本文方法完全对应

### 下游(应用于 / 验证于)

- [[Agentic-Engineering-AI-Workbench]] - "AI 工作台"五层结构(计划/上下文/执行/验证/治理)= 本文方法论的结构化版本
- [[买了一样的AI为什么别家的比你的强]] - "AI 自己做初判 + 给理由"是 Hiten Shah "模型是商品,判断是资产"在个人层面的具体实现
- [[多Agent使用边界与并行判定]] - "同时开 4-5 个 Claude"需要先用"任务卡 + 隔离 + 可验证结果 + 合并规则"判定并行是否值得
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - 强模型也需 Harness,auto/loop 本身是 Harness 的一部分

## 正文要点(8 条)

### 一、并行工作靠 worktree

| 维度 | Meaghan 的实践 |
|---|---|
| 并行数量 | 4-5 个 Claude 窗口同时跑 |
| 隔离方案 | worktree(给仓库创建隔离副本) |
| 解决痛点 | 多 Claude 互相打架、改同一文件 |

> "Anthropic 内部的工程师,经常同时开四五个 Claude 窗口并行处理任务。这已经是他们的日常了。"

> **思路本身就值得琢磨**——哪怕不写代码,也可以想想:有没有办法让 AI 同时帮你处理多条线的工作?

### 二、让 AI 自己做决策,然后告诉你为什么

**`/prototype` 自定义技能**:
- 旧做法:让 Claude 生成 5 个版本,Meaghan 自己挑
- 新做法:**让 Claude 先选一个它觉得最好的,然后解释为什么**

> "以前大家用 AI 的习惯是:你给我几个选项,我来拍板。但她的做法是把初步判断也交给 AI,自己只做最终的确认。"

**关键副产品**:没有人再手写这些自定义技能了,全都是让 Claude 帮忙生成。"如果有人说他是自己手写的,那他在骗你。"

### 三、不只是写代码,所有重复性工作都丢给 AI

| 工作环节 | AI 参与度 |
|---|---|
| 写代码 | 100% |
| 自动 commit | AI 主导 |
| 发起 PR | AI 主导 |
| 截图记录功能效果 | AI 主导 |
| Slack 通知同事审核 | AI 主导 |
| 简单修复(按钮间距 / 颜色) | AI 直接修,改动小自动过审上线 |

> **核心理念**:任何她觉得不值得花时间亲自做的事情,全部扔出去。

### 四、用定时任务让 AI 自动巡逻产品质量

```
每日定时任务:
  Claude 扫描所有仓库前端改动
    ↓
  检查每个改动背后是否有设计师参与
    ↓ 查 Slack 聊天记录 / 会议纪要 / 文档协作
  未经过设计师审核?
    ↓
  AI 自动生成替代设计方案
    ↓
  打包成待审核的代码提交
    ↓
  私信工程师,提醒他去找设计师合作
```

**关键细节**:这套流程在 Claude 设计能力还不够好的时候,把"自动发消息"关掉(免得消息质量差让工程师烦),**但整套流程保留着**——等下一代模型能力更强,直接重新启用。

### 五、AI 现阶段做不好设计,人仍要把控方向

- 审美和产品决策:人类主导
- 什么该上线 / 什么不该上线:**人做判断**
- 质量把控体系:反而要求更强

> "工具变强了,门槛降低了,但标准不能跟着降低。反而因为产出变多了,筛选和把关变得更重要了。"

### 六、始终开 auto 模式,减少一切不必要的确认

| 配置 | 作用 |
|---|---|
| Opus 模型 | 强模型 |
| 1M 上下文窗口 | 大上下文 |
| auto 模式 | 分类器自动判断风险,没风险直接执行 |
| loop | 一直做,做到完为止 |

> **核心理念**:能自动化的全部自动化,人只在真正需要判断的环节介入。

### 七、先把流程搭好,等模型升级

这是 loonggg 自己提炼的"金句方向":

> "不要怕现在的 AI 做得不够好。先把流程搭起来,先把自动化的框架建好。等模型能力提升了,你的系统马上就能受益。"

**Anthropic 内部验证**:
- Meaghan 整套"AI 自动巡逻"流程保留
- 自动发消息关了,但骨架一直在
- 下一代模型一发布,直接接上

### 八、写在最后:从"一问一答"到"接管整条链路"

> "很多人用 AI 还停留在「问一个问题,得一个答案」的阶段。但真正把 AI 用到极致的人,已经在想怎么搭建一整套自动化的工作流了。**他们不是在用 AI 完成一个步骤,而是在让 AI 接管整条链路。**"

## 我的理解

- **"先把流程搭好,等模型升级"是 2026 年最高 ROI 的 AI 战略** —— Meaghan 关掉"自动发消息"但保留整套流程 = **永远不浪费自己搭好的工作流**;这条主线与 [[Addy-Osmani-Loop-Engineering]] [[Agentic-Engineering-AI-Workbench]] 是同一信号的不同切面
- **"auto + loop + Opus 1M 上下文"是 Claude Code 推荐的"高交互"配置组合** —— 但这套组合需要配合 **清晰的护栏(分类器判断风险 / loop 终止条件)**,否则容易失控;与 [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] "模型再强也需要 Harness 约束"互相印证
- **"用定时任务自动巡逻产品质量"是 Anthropic 内部的"AI 自我监控"实践** —— AI 不只帮工程师写代码,还帮设计师/PM 检查"有没有被绕过";这条与 [[Claude-Code团队5条工作原则-Fiona-Fung分享]] 的 "Trust but verify" 是同一条规则的产品化形式
- **"AI 做不好设计,人把控方向"是重要的"AI 边界论"** —— 与 [[Claude-Code之父品味不是人类护城河]] Boris 的"品味也会被模型侵蚀"形成互补:**AI 在"判断 + 审美"上边界还在,但边界会持续移动**;人要做的是 **持续把"今天模型做不到"的事结构化地留给未来模型**
- **"让 AI 自己做决策 + 给理由"是"判断力外包"的具体实现** —— 跟上 [[买了一样的AI为什么别家的比你的强]] 的"模型是商品,判断是资产"主线 —— Meaghan 把"选择哪个方案"这种初级判断也包进 Claude = **判断的颗粒度从"拍板"下沉到"初判 + 解释"**
- **对 Seetong 团队的 3 个可借鉴动作**:
  1. **worktree 并行改造**:选一个迭代试"同时 3 个 Codex 跑不同子任务"(参考 [[多Agent使用边界与并行判定]])
  2. **"AI 自动巡逻"小试点**:写一个 cron 任务,每天扫 Seetong Bug / 需求,自动标红"测试已 3 天未响应"等异常
  3. **Opus + 1M 上下文 + auto 模式**:在重决策(架构 / 重大 Bug 排查 / 跨模块重构)任务上用这套配置,先小范围验证

## 相关链接

- 原文:https://mp.weixin.qq.com/s/_WaCCvZ0FgMQiJ1PSVOMwA
- 演示者:Meaghan Choi(Anthropic,Claude Code 首席设计师)
- 关联 wiki:
  - [[Claude-Code作者Boris-我已经不写prompt了我写loop]] - "写 Loops"是 AI Coding 的下一阶段,本文"auto + loop"是同主线
  - [[Claude-Code之父品味不是人类护城河]] - Boris 谈品味被模型侵蚀,Meaghan 谈当下 AI 设计仍不够好,两者互补
  - [[Claude-Code团队5条工作原则-Fiona-Fung分享]] - "Trust but verify" 规则的 AI 监控化
  - [[Addy-Osmani-Loop-Engineering]] - 5+1 积木 + auto + loop 是同一信号的跨产品表达
  - [[Agentic-Engineering-AI-Workbench]] - "AI 工作台"五层结构 = 本文方法论的结构化版本
  - [[买了一样的AI为什么别家的比你的强]] - "AI 自己做初判 + 给理由"是判断力外包的具体形式
  - [[多Agent使用边界与并行判定]] - "同时开 4-5 个 Claude" 需要先判定并行是否值得
  - [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]] - 强模型也需 Harness,auto/loop 本身是 Harness 的一部分
