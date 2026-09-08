---
title: Anthropic AI-Native SDLC：用版本化产物重构软件开发流程 - 速读
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 主题/AI-Native研发
  - 主题/SDLC
  - 主题/验证驱动
nodes: [提交产物, 产物触发器, 策略分层, 受保护验证, 人类门禁]
links: [[02-ai-coding/Anthropic发布AI-Native软件开发流程-时代变了-该换套模式了]], [[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]], [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]]
date: 2026-09-08
source: Anthropic 官方博客 / Louis Claxton；中文参考：Founder Park
status: published
---

# Anthropic AI-Native SDLC：用版本化产物重构软件开发流程 - 速读

> AI-Native SDLC 的单位不是一次代码生成，而是可审查、可版本化、可触发下一阶段的产物；人的责任从逐次确认编辑，转为审批意图、规格、计划、风险与发布。

- **官方原文：** https://claude.com/blog/the-ai-native-sdlc-playbook
- **中文参考译文：** https://mp.weixin.qq.com/s/YeAL7XBmltR4n3rUnz3Pag
- **中文译文文件：** `raw/Anthropic-AI-Native-SDLC-playbook-中文译文.md`

- **代码两侧瓶颈**：实现提速后，规划、测试、审查和部署决定系统速度。
- **提交产物**：`intent.md → spec.md → plan.md → 代码/测试 → PR → 事故记录` 同时充当输入、交接和审计链。
- **产物触发器**：已审核产物启动下一门禁，线上异常又回流为新 intent。
- **策略分层**：Skill 管可变知识，Hook/CI 管不可违反的限制。
- **受保护验证**：让 Agent 自测，但不允许它通过修改测试来“证明”修复。
- **人类门禁**：人保留目标、风险、策略冲突和高影响发布决定。

最小试点：选择一个高频流程，将阶段输出固化为一个版本化模板；先手工验证它能被下一阶段消费，再加入自动触发、Eval 和更长的自主会话。

相关：[[02-ai-coding/AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]、[[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]]、[[02-ai-coding/宝玉AI-我的AI原生开发流程-真实案例复盘]]。

证据边界：官方页面已核对标题、发布日期、更新日期与正文；中文内容为 Founder Park 参考译文。
