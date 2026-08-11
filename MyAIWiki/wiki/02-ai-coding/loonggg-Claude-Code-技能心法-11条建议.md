---
title: Claude Code 团队的技能(Skills)心法大曝光
category: 02-ai-coding
tags:
  - 主题/Claude-Code
  - 主题/Skill
  - 主题/工程实践
  - 主题/Anthropic
  - 主题/AI-Coding
  - 主题/Seetong借鉴
  - 场景/Skill设计
  - 场景/团队实践
nodes: [9大类技能盘点, 验证类技能被严重低估, 别说废话只说AI不知道的, 踩坑记录是含金量最高, 渐进式信息披露, 给AI灵活度, 让AI有记忆, 多给工具少给指令, 描述要写给机器看, 从小处在实践中迭代, 分享管理让好东西流动]
links: [[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]], [[02-ai-coding/PM-Skills-Marketplace-产品经理必备skill]], [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]], [[02-ai-coding/谷歌开源agent-skills]], [[02-ai-coding/Claude-Code团队5条工作原则-Fiona-Fung分享]], [[02-ai-coding/Claude-Code作者Boris-28分钟教你写真正有效的Prompts]], [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]], [[01-ai-agents/harness-engineering]]
date: 2026-07-04
source: 微信公众号 / loonggg 2026-07-04 18:56(中文解读编译自 Anthropic Claude Code 团队分享)
原始链接: https://mp.weixin.qq.com/s/2FeY2RbptAoj-49LBW2WWA
---

# Claude Code 团队的技能(Skills)心法大曝光

> **核心结论**:**Claude Code 团队内部把 Skill 沉淀成"操作手册 + 踩坑记录",分 9 大类,提炼 11 条写 Skill 心法**——核心是"验证类技能最被低估 + 渐进式信息披露 + 给 AI 灵活度 + 踩坑记录含金量最高 + 自下而上分享管理"。与 [[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] 同主线,但更偏"做事方法论 + 大白话",适合推广至非工程读者。

## 8 个独立知识节点(精选 11 条中的 8 条核心)

- **9 大类技能盘点**:Claude Code 团队内部把 Skill 分 9 类——库/API 参考 / 产品验证 / 数据获取与分析 / 业务流程自动化 / 代码脚手架与模板 / 代码质量与审查 / CI/CD 部署 / 运维手册 / 基础设施运维。**核心反直觉**:**验证类价值最高,值得一整周投入**(录测试视频 + 程序化断言 + 状态校验)。这与 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]"验证是产品,其余是管道"互为印证——同一个团队的不同切片。

- **别重复 AI 已经知道的(踩坑记录 / 渐进式披露)**:第一条心法——写 Skill 时别说废话,只说 AI 不知道的。Claude 本来就会写代码,重复它会做的就是浪费上下文。**真正有用的是把 AI 从惯性思维里拉出来**(如纠正"审美默认值"——总是 Inter 字体 + 紫色渐变)。**渐进式信息披露**——主文件只告诉 AI 有哪些子文件可参考,需要时再读,避免上下文过载。**踩坑记录(Gotchas)是含金量最高的**:来自 AI 反复犯的错,如"subscriptions 表只追加,找版本号最高的行,不是创建时间最新的";如"request_id 在网关 / trace_id 在计费,其实是同一字段"。

- **给 AI 灵活度 + 让 AI 有记忆**:Claude 严格遵守指令,所以指令太死板它就在不该死板时也死板——**不要"过度控制"**(类比:好的管理者告诉目标/边界/注意事项,不规定每一步)。**给 AI 加记忆**——用日志文件追加每次执行结果,下次运行时 AI 读到自己上次做过什么,自动对比变化(如"每日站会报告"技能能看到昨天内容)。**核心反直觉**:**"做"的工作早就自动化了,下一步是让 AI 在历史基础上迭代,不是每次从零开始**。

- **多给工具少给指令 + 描述写给机器看**:与其写一大段文字告诉 AI 怎么做,不如直接给脚本和工具函数——把基础能力封装好,让 AI 专注于"决定做什么"和"怎么组合"。**描述要写得像触发条件**:技能描述的目的是让 AI 判断**什么时候该触发**,不是给读者看的摘要——要站在"执行者"角度,不是"观察者"角度。

- **MVP 起步 + 自下而上管理**:**没有人一开始就写出完美的技能**——最佳实践都是几行简单指令 + 一条踩坑记录开始,后续随边界情况补充。**分享管理**:小团队技能放代码仓库 / 大团队搞内部技能市场;**不设委员会审批**,谁觉得好用先放试用区,确实有人在用再正式上架;**用钩子统计使用频率**,数据驱动管理而非审批制度。**核心反直觉**:**好东西自己会说话,真实环境检验比任何评审流程都靠谱**。

## 关联图谱

### 上游(基于 / 来自)
- **Anthropic Claude Code 团队官方分享**:11 条心法的一手来源(原文 URL 未给出)
- **loonggg 公众号中文解读**:翻译风格偏"大白话 + 个人理解",不是 Anthropic 原文
- **Addy Osmani agent-skills 项目**:同一主线"如何设计好 Skill"的另一权威版本(7 块骨架 + 反合理化)

### 下游(应用于 / 验证于)
- **Claude Code 内部 Skill 库**:9 大类覆盖、验证类专项投入 1 周
- **企业内部技能市场**:大团队规模后的自下而上管理实践
- **Loonggg 个人读者群**:用于日常工作反思("写文章不复盘就发" / "做方案不复盘")

### 同级(横向 / 并列)
- Skill 设计主线:[[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] / [[02-ai-coding/PM-Skills-Marketplace-产品经理必备skill]] / [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]] / [[02-ai-coding/谷歌开源agent-skills]]
- AI Coding 实践主线:[[02-ai-coding/Claude-Code团队5条工作原则-Fiona-Fung分享]] / [[02-ai-coding/Claude-Code作者Boris-28分钟教你写真正有效的Prompts]] / [[02-ai-coding/Claude-Code在大代码库中的最佳实践-从Anthropic官方指南到可落地Harness方法]] / [[02-ai-coding/字节跳动洪定坤-AI-Coding的实践与探索]]
- Harness 框架主线:[[02-ai-coding/Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]] / [[02-ai-coding/Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- 知识库主线:[[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] / [[01-ai-agents/harness-engineering]]
- 验证主线:[[01-ai-agents/Loop-Engineering-验证才是瓶颈]] / [[01-ai-agents/530万人-自循环-提示词]]

## 5 个对 Seetong 团队可借鉴动作

1. **Seetong AI 助手所有 Skill 加"Gotchas 段"**:复盘过去 6 个月 Seetong AI 助手最常犯的 10 个错,把"易踩坑点"明确写进对应 Skill(seetong-bug-triage / seetong-daily-briefing / seetong-tapd-version-review)。格式建议:"这个字段在 iOS 端叫 X,在 Android 端叫 Y,其实是同一个值" / "用户反馈 iOS 14 设备扫码后崩溃,原因是 Z"。
2. **把"验证类"作为 Skill 设计硬性环节**:Seetong Skill 默认配 Evaluation Gate(不只 9 大类中的"产品验证"类,所有类都要有)——输出结果后跑一段程序化断言或对账脚本(seetong-daily-briefing 加 L2(神策/友盟/TAPD)对账、L3(运营类别)对账,与 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] 验证闸门呼应)。
3. **渐进式信息披露入 Seetong Skill 模板**:Seetong AI 助手的每个 Skill 主体只写"用得最多的 30%"信息,详细参考资料 / API 文档 / 示例代码放在子文件 / 链接,避免一次塞全文——参考 [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] 的"3 层知识加载 + 4 查询模式"。
4. **描述写得像触发条件**:Seetong 每个 Skill 描述统一格式"当用户问 X / 当场景是 Y / 当需要 Z 时,触发本技能",而不是抽象的功能描述。**反例**:"本技能负责反馈分诊";**正例**:"当用户上传 7 张内 App 截图 + 一句'我的设备远程开门失败'时,触发本技能,先查 X 字段"。
5. **MVP 起步 + 自下而上管理**:Seetong 内部维护一个"技能清单"(`seetong-knowledge-system/skills/INDEX.md`),谁写了新 Skill 都登记一行,带试用状态 / 使用次数(钩子统计)/ 踩坑记录。**不设委员会审批**,让真正好用的技能自然留下,1-2 月后砍掉没人用的。

## 备注与限制

- **作者**:loonggg(微信公众号"老码农"类 AI/技术自媒体),非 Anthropic 官方原文,是一手 Anthropic 文章的中文解读
- **一手原文未公开链接**:本文没有给出 Anthropic Claude Code 团队分享的原始英文文章 URL,所有内容是 loonggg 的编译解读
- **9 大类分类为 loonggg 整理**:可能与 Anthropic 官方分类略有差异
- **11 条心法的边界**:多数是经验总结,缺具体量化指标(如"验证类技能提升 X%")
- **目标读者偏广泛**:不像工程实践文,更偏"做事方法论"风格,可读性强但技术深度有限
- **微信公众号文末推广**:原文包含 loonggg 个人付费"星球社群"广告(199 元→169 元),与正文 Harness 工程无关
- **11 条心法的内在逻辑**:"验证类最被低估"是首要点,其他 10 条围绕"信息/记忆/灵活度/管理/迭代"展开,构成完整 Skill 工程心法体系
- raw:../../raw/loonggg-Claude-Code-技能心法-11条建议.md | raw-digest:../../raw/loonggg-Claude-Code-技能心法-11条建议-digest.md | wiki-digest:./loonggg-Claude-Code-技能心法-11条建议-digest.md