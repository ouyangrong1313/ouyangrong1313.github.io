---
title: 腾讯 TEG Agent Skill 测评方案 - Digest
category: 01-ai-agents
date: 2026-06-17
source: 微信公众号 腾讯程序员 2026-06-17
source_url: https://mp.weixin.qq.com/s/PUbGqheJhFMmb6hGj1ZtOw
main_entry: [[腾讯-AI-Agent-Skill-测评方案落地]]
---

# 腾讯 TEG Agent Skill 测评方案 — Digest

## 一句话总结

**测评是 Agent 从 Demo 可用走向生产可靠必须跨过的门槛。** 腾讯 TEG 网关测试团队给出"3 类评分器 + 5 大维度 + 5 步闭环"完整框架,核心反直觉:"过度触发比不触发更难发现,所以负向触发用例比正向触发更重要"。

## 速查表

**核心命题**:Agent/Skill 设计阶段就要把 Trace 输出作为标准能力,而非事后补救
**核心金句 4 条**:① 能用代码判断的绝不用模型 ② 过度触发比不触发难发现 ③ 用例基线=1 次人工确认的预期快照 ④ N 次中 1 次不通过即标记稳定性风险
**关键数字**:3 类评分器 / 5 大维度 / 5 步闭环 / 落地项目 TPerf 性能平台

## 反直觉 5 个

1. 测评不是写完代码再做,设计阶段就该把 Trace 纳入
2. 过度触发比不触发更难发现(负向触发比正向触发更重要)
3. 能用代码判断的绝不用模型(Rubric 是补盲区不是替代)
4. 不通过比例阈值因 Agent 类型而异
5. 过程评测比结果评测更通用

## 5 个对 Seetong 团队可借鉴动作

1. **建立"Seetong Agent 评测集"** — 对每个 Skill 都建"用例基线 + 评分规则 + 多轮稳定性评估"
2. **把 Trace 输出作为 Skill 设计阶段标准能力** — 当前 Seetong skill 默认不输出结构化 trace,需要补
3. **设"过度触发比不触发难发现"作为新 Skill 设计的硬规则** — 每个 Skill 必须配负向触发用例
4. **用例设计 5 步闭环作为 Seetong 内部 Agent SOP** — design → rubric → baseline → execute → maintenance
5. **TPerf 项目作为基准参考** — 腾讯 TEG 已在生产跑通,作为 Seetong Agent 评测体系"先例"参考

## 关联

**主条目**:[[腾讯-AI-Agent-Skill-测评方案落地]]
**上游**:[[Skill-Self-Evolution]] / [[陈进-读完Agent-Loop工程手册]] / [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]
**下游**:[[用Agent评测思路管理AI-Coding-31万行代码AI重构实践]] / [[如何构建一个更"好"的知识库]] / [[seetong-batch-issue-rootcause-analysis]] / [[seetong-daily-briefing]]
**同级**:[[清华沈阳-自进化AI新物种]] / [[Multica-AI-Native-组织]]

## 备注

- 速读版:核心结论 + 反直觉 + Seetong 借鉴动作 + 关联指针
- 完整编译页:同目录 [[腾讯-AI-Agent-Skill-测评方案落地]]
- 落地项目:TPerf 性能平台智能分析 Agent(腾讯 TEG 网关测试团队,生产环境跑通)
