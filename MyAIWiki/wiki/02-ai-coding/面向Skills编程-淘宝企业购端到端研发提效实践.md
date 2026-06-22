---
title: 面向 Skills 编程——淘宝企业购端到端研发提效实践
category: 02-ai-coding
tags: [#主题/Skills编程, #主题/AI-Coding, #主题/工程实践, #主题/SDD, #主题/Agent-Skills, #主题/阿里, #主题/范式升级, #场景/企业级落地, #场景/淘宝企业购]
nodes: [面向Skills编程范式, Skills-等于-AI行为契约, Skill-构建四步法, 五阶段演进路径, 知识工程为质量瓶颈, 确定性工程+不确定性AI, 三段式提效数据, 三层架构+ADJUSTMENT_PLAN]
links: [[阿里云开发者-淘宝主播Agent的Harness工程实战]], [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[Skill-Self-Evolution]], [[Agent Skills 系统性综述]], [[谷歌开源 agent-skills]], [[Addy-Osmani-agent-skills-设计哲学]], [[PM-Skills-Marketplace-产品经理必备skill]], [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]], [[Notion-spec-driven-AI-workflow]], [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]], [[Loop-Engineering-验证才是瓶颈]], [[腾讯-AI-Agent-Skill-测评方案落地]]
date: 2026-06-18
source: 微信公众号 / 大淘宝技术(官亭,淘天集团-行业运营技术团队) 2026-06-17 14:20
原始链接: https://mp.weixin.qq.com/s/8wJhwC4YuaOX-8GXMaFU5g
---

# 面向 Skills 编程——淘宝企业购端到端研发提效实践

> **核心结论**:**Skills 是 AI 研发的最小可复用单元**——封装工作流 + 领域知识 + 约束规则(SKILL.md / references / 禁止项);淘宝企业购近半年实战:**商品域端到端交付周期 23.5 人日 → 8 人日(提效 65%),代码一次生成成功率 90%**;**质量瓶颈不在模型,在知识工程——50% → 90% 全靠知识注入和约束迭代,不是换更强的模型**。

## 8 个知识节点

- **面向 Skills 编程范式**:DDD 分层 + 配置化在传统人写代码模式下行之有效,但高频定制化需求时参数空间爆炸;**新范式核心是"人写 Skills,LLM 基于 Skills 写代码"**——程序员从"实现逻辑"上升为"定义 Skills"。
- **Skills = AI 行为的契约**:类比"接口/抽象类"定义代码契约,Skills 定义 AI 行为契约——告诉 LLM"做什么、怎么做、不能做什么",让大模型从"知道分子"成为"行动专家"。
- **Skill 构建四步法**:**识别重复模式 → 封装不变量为 Skills → 将变化的部分作为输入 → LLM 在约束下执行**。垂直领域的 Skills 本身不通用,但**构建 Skill 的方法论是通用的**。
- **五阶段演进路径**:Vibe Coding(对话驱动,2025.8)→ Prompt 模板(标准化翻译器,2025.9,**采纳率 70%**)→ SDD 规范驱动(2025.12,**可用率 40% → 80%**)→ Skill 沉淀(经验固化,2026.1-2)→ 云端集成(端到端产品,2026.2 探索中)。**每一阶段都是对前一阶段"天花板"的突破**。
- **质量瓶颈不在模型,在知识工程**:**50% → 90% 的提升全部来自知识注入和约束迭代,不是换更强的模型**——领域知识(映射规则/API 签名/模式判定)不会从训练数据中涌现,必须显式注入。
- **确定性工程 + 不确定性 AI = 可控流水线**:高精度环节用脚本(接口提取),模型不稳定的用架构拆分绕过(推拉分离/子 Skill),反复出错的沉淀为约束——三者配合把"不可控的对话"变成"可复现的流水线"。
- **三段式提效数据**:代码一次生成成功率 **50% → 90%**;AI 生成代码可用率 **40% → 80%**(SDD 阶段);商品域端到端交付周期 **23.5 → 8 人日**(整体提效 **65%**);**11 类高频问题全部沉淀为 Skill 约束,不再复现**。
- **三层架构 + ADJUSTMENT_PLAN**:原子能力层 + 模板层 + 适配层(AI 只聚焦适配层逻辑,**代码量减少 60%**,多客户并行零冲突);ADJUSTMENT_PLAN 机制(**发现→定位 Skill→补约束→验证→交叉验证**)闭环 11 类问题;**事前约束 → 运行时约束 → 事后审查 → 人工卡点** 四层质量防线。

## 关联图谱

### 上游(基于 / 来自)
- **DDD 分层 + 配置化编程**:经典范式,天花板在"高频定制化时 SPI 扩展点变手写适配"
- **Anthropic Agent Skills 标准**:SKILL.md + references/ + scripts/ + 渐进式加载
- **OpenSpec / Spec-Kit / BMAD / everything-claude-code / superpowers**:SDD 工具链 + 开源最佳实践

### 下游(应用于 / 验证于)
- **淘宝企业购客户对接**(商品/交易/结算三大业务域)+ **15 个接口商品域全流程跑通**(评估→技术方案→编码)
- **OneDay + Aone 沙箱端到端生码平台**:2026.2 探索中

### 同级(横向 / 并列)
- 阿里淘系同源:[[阿里云开发者-淘宝主播Agent的Harness工程实战]](主播=实时交互高风险)/ [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]
- Skill 主线:[[Skill-Self-Evolution]] / [[Agent Skills 系统性综述]] / [[谷歌开源 agent-skills]] / [[Addy-Osmani-agent-skills-设计哲学]] / [[PM-Skills-Marketplace-产品经理必备skill]]
- SDD/Spec 主线:[[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] / [[Notion-spec-driven-AI-workflow]] / [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]]
- Loop 主题:[[Loop-Engineering-验证才是瓶颈]](本文讲 Skills 构建,那篇讲 Loop 验证)/ [[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]]
- 评测+范式:[[腾讯-AI-Agent-Skill-测评方案落地]] / [[AI-Coding的顿悟时刻]] / [[54万行代码的顿悟-Markdown才是新编程方式]]

## 5 个对 Seetong 团队可借鉴动作

1. **用"质量瓶颈在知识工程"做体检**:Seetong 现有 Skill 库 `seetong-bug-triage` / `seetong-tapd-version-review` / `seetong-daily-briefing` / `seetong-prd` 成功率卡在 60-70%,**优先排查 references 是否有完整领域知识映射规则**,不是换模型——50% → 90% 全靠知识注入。
2. **复制"三层架构"重写 Seetong 适配层 Skill**:Seetong 三端(Login/Message/Device/Mine)有大量"换端实现"适配代码——**原子能力层**(API/Socket/DB)+ **模板层**(端口无关流程)+ **适配层**(AI 填充端差异),预期代码量 -60%,多端并行零冲突。
3. **借鉴 ADJUSTMENT_PLAN 五步闭环建高频问题约束库**:`seetong-bug-triage` 跑出的"3 天内同 Bug 复现 2 次根因 X"——**先在 Skill 里加约束条款**,不只写文档;Seetong 已有 11 类 iOS 6 大漏洞/4G 6 类问题列表直接沉淀为 Skill 约束(对应 [[seetong-ios-quality-review]] / [[seetong-batch-issue-rootcause-analysis]])。
4. **"事前约束→运行时约束→事后审查→人工卡点"作为 Seetong SOP 四层防线**:事前 references 禁止项;运行时 Hook/结构化错误码拦截(对应 [[阿里云开发者-淘宝主播Agent的Harness工程实战]] 五层防护);事后 Trace 审查;人工卡点(改版本号/主分支二次确认)。
5. **写"Seetong 端到端生码平台" P0 小试点**:TAPD 需求 → 神策 → 友盟 → 反馈 → 周报(对应 [[seetong-tapd-version-review]] + [[seetong-daily-briefing]] + [[seetong-weekly-report]]),先建 Skill references(Seetong 三端 API + 已知 bug 模式),再试 1 个真实 TAPD 需求端到端跑通,7 天内成功率从 baseline → 80%。

## 备注与限制

- 作者官亭,淘天集团-行业运营技术团队(招聘 zezhou.jzz@taobao.com)
- 阶段 5 云端集成尚未规模化,具体上线日期未披露
- 评估报告 Skill"字段遗漏率 0%"是否多项目稳定待验证
- kn-fetcher CLI 对接 Skill 体系时间表未明
- Code Wiki/KBase 试跑数据未披露召回率
- ADJUSTMENT_PLAN 11 类高频问题具体清单未列
- 原文:https://mp.weixin.qq.com/s/8wJhwC4YuaOX-8GXMaFU5g
- raw:[../../raw/2026-06-17-大淘宝技术-面向Skills编程-淘宝企业购端到端研发提效实践.md](../../raw/2026-06-17-大淘宝技术-面向Skills编程-淘宝企业购端到端研发提效实践.md) | digest:[./面向Skills编程-淘宝企业购端到端研发提效实践-digest.md](./面向Skills编程-淘宝企业购端到端研发提效实践-digest.md)