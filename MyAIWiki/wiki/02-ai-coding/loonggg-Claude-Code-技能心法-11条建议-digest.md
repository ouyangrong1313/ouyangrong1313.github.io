---
title: Claude Code 团队的技能(Skills)心法大曝光(速读摘要)
category: 02-ai-coding
tags:
  - 主题/Claude-Code
  - 主题/Skill
  - 主题/Anthropic
  - 主题/AI-Coding
  - 主题/Seetong借鉴
  - 场景/Skill设计
type: digest
date: 2026-07-04
source: 微信公众号 / loonggg 2026-07-04(中文解读编译自 Anthropic Claude Code 团队分享)
原始链接: https://mp.weixin.qq.com/s/2FeY2RbptAoj-49LBW2WWA
---

# Claude Code 团队的技能(Skills)心法大曝光(速读摘要)

> **一句话**:**Claude Code 团队内部把 Skill 沉淀成"操作手册 + 踩坑记录",分 9 大类,提炼 11 条心法**——验证类最被低估 + 渐进式披露 + 给 AI 灵活度 + 踩坑记录含金量最高 + 自下而上分享管理。

## 速查表

| 维度 | 核心命题 | 关键设计 |
|---|---|---|
| 技能定义 | 预先写好的指令(操作手册),AI 拿到后按场景处理 | 类比 SOP + Gotchas |
| 9 大类分类 | 库/API / 验证 / 数据 / 流程自动化 / 脚手架 / 质量 / CI-CD / 运维 / 基建 | 全场景覆盖 |
| 验证类 | 所有 Skill 中价值最高,值得花一整周投入 | 录视频 + 程序化断言 + 状态校验 |
| 别说废话 | 不重复 AI 已经知道的事,只说 AI 不知道的 | 纠正 AI 惯性思维(如审美默认值) |
| 踩坑记录 | Gotchas 是含金量最高的部分,持续更新 | 反复犯的错是核心资产 |
| 渐进式披露 | 主文件只给索引,详情放子文件 | 避免上下文过载 |
| 给 AI 灵活度 | 指令太死板,Claude 严格遵守=在不该死板时也死板 | 类比管理"目标+边界,不规定每一步" |
| 让 AI 有记忆 | 日志文件追加每次执行结果,下次自动对比 | 不每次从零开始 |
| 多给工具 | 基础能力封装成脚本/函数,AI 专注"决定做什么" | 把重复劳动自动化 |
| 描述写法 | 触发条件式,不是功能摘要 | 站在"执行者"角度 |
| MVP 起步 | 几行指令 + 一条踩坑记录起步,实践中迭代 | 别等到想清楚再开始 |
| 自下而上 | 不设委员会,试用区→正式上架,钩子统计使用频率 | 数据驱动管理 |

**5 个反直觉点**:① **"验证"比"做"更能提升质量**(完工不复盘是常见浪费)② **别重复 AI 已经会的**(写废话是浪费上下文空间)③ **指令太死板会杀死创造力**(Claude 严格遵守在不该死板时也死板)④ **AI 加记忆后不是每次从零开始**(日志追加让重复工作自动迭代)⑤ **没有委员会审批 = 更高效率**(好东西自己说话,数据比评审靠谱)

## 5 个对 Seetong 团队可借鉴动作

1. **Seetong AI 助手所有 Skill 加 Gotchas 段**:复盘过去 6 个月最常犯的 10 个错,写进对应 Skill,格式"这个字段在 iOS 端叫 X / Android 叫 Y 其实是同一值"
2. **把"验证类"作为 Skill 设计硬性环节**:Seetong Skill 默认配 Evaluation Gate——输出后跑程序化断言或对账脚本(seetong-daily-briefing 加 L2(神策/友盟/TAPD)+ L3(运营类别)对账),与 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] 验证闸门呼应
3. **渐进式信息披露入 Seetong Skill 模板**:Seetong AI 助手每个 Skill 主体只写"用得最多的 30%"信息,详细参考资料 / API 文档 / 示例代码放子文件——参考 [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] 3 层知识加载
4. **描述写得像触发条件**:Seetong 每个 Skill 描述统一格式"当用户问 X / 场景是 Y / 需要 Z 时,触发本技能"——反例"本技能负责反馈分诊",正例"当用户上传 7 张截图 + '我的设备远程开门失败'时触发本技能,先查 X 字段"
5. **MVP 起步 + 自下而上管理**:Seetong 内部维护 `skills/INDEX.md`,谁写新 Skill 登记一行(试用状态 / 使用次数 / 踩坑记录),不设委员会审批,1-2 月后砍掉没人用的

## 关联 + 备注

**关联**:Skill 设计主线 [[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] / [[02-ai-coding/PM-Skills-Marketplace-产品经理必备skill]] / [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]] / [[02-ai-coding/谷歌开源agent-skills]] | AI Coding 实践 [[02-ai-coding/Claude-Code团队5条工作原则-Fiona-Fung分享]] / [[02-ai-coding/Claude-Code作者Boris-28分钟教你写真正有效的Prompts]] / [[02-ai-coding/字节跳动洪定坤-AI-Coding的实践与探索]] | 知识库 [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] | 验证 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]

**备注**:作者 loonggg 微信公众号"老码农" AI/技术自媒体 | 非 Anthropic 官方原文,是一手文章的中文解读 | 9 大类分类为 loonggg 整理可能与官方有差异 | 11 条心法多数是经验总结,缺量化指标 | 文末含 loonggg 个人付费星球社群广告与正文无关