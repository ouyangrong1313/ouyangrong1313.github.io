---
title: 架构腐朽与Loop-Engineering - Digest
category: 02-ai-coding
tags:
  - 主题/架构腐朽
  - 主题/Loop-Engineering
  - 主题/AI-Coding时代
  - 作者/lencx
date: 2026-07-15
source: 微信公众号「lencx」/ 作者 lencx（Mark Text 等开源工具作者）/ 原文 https://mp.weixin.qq.com/s/wINKSDQCroWBvf29h567zA
nodes: []
---

# 架构腐朽与 Loop Engineering - Digest

## 一句话总结

> 屎山源于不敢删，架构活于持续排熵；AI Coding 时代腐朽速率翻倍——唯一解药是把架构约束编码到 Loop + CI 里让机器维护。

## 8 节点速查表

| 节点 | 一句话 |
|---|---|
| **架构五层定义** | 图/决策/约束/运行时/"删起来贵的部分"（第五层是工程现实最贴的工作定义） |
| **腐朽必然性** | 历史负担 + 失败成本不对称 = 系统越来越没人敢动 |
| **重构悖论** | 立项永远漂亮，两年后多数人选择绕道——多一层壳包裹旧系统 |
| **Linux 外紧内松** | 稳定性预算花在系统调用/驱动 API/文件系统语义"对外承诺"接口；内部可激进重构 |
| **提交即重构** | 小步前进 + 主干可编译 + 重构不动语义 + 删死代码 + 命名即文档（5 条） |
| **守卫自检** | 永远 pass 的检查器信息量为零；每条规则配反例测试让检查器证明还能失败 |
| **删比改更重要** | 祖训是软件熵的化石；定期盘点 + 让删成为正常开发动作 + 删前加引用监控 |
| **Loop Engineering** | AI Coding 让代码生成边际成本接近 0；架构师从"画图"变成"把约束编码到 Loop" |

## 关键数字 + 5 关键金句

- **5 层**架构定义 / **2 个**腐朽必然条件 / **4 种**排熵工作模式 / **5 条**提交即重构原则 / **10x** AI Coding 代码量增长
- 金句①"屎山源于不敢删，架构活于持续排熵"
- 金句②"架构是那些删起来贵的部分"
- 金句③"外紧内松。承诺稳定的是接口，不是实现"
- 金句④"一个永远通过的检查，对判断当前代码是否破坏约束几乎没有信息量"
- 金句⑤"模型可以忘，流水线不能忘"

## 3 反直觉点 + 6 个 Seetong 借鉴动作

**3 反直觉点**：① 重构立项漂亮两年后多数人绕道 ② 永远 pass 的检查器信息量为零 ③ AI Coding 让腐朽速率同样翻倍

**6 借鉴动作**：

1. **列祖训清单**：欧阳荣+黄松佳+谭伟+张威 共同列 Seetong"祖训清单"（不能动的模块/字段/逻辑），反思哪些源于"不敢删"
2. **稳定性预算体检**：Seetong 监控/告警预算投在哪些边界的体检（4G IPC 协议/神策 schema/用户 API/Logan 格式）
3. **排熵机制**：每 sprint 强制 1 个删废弃代码 PR；review checklist 加"能不能删"
4. **守卫自检**：找出 Seetong 自动化检查中"永远 pass"的项（神策 schema/反馈分类/友盟字段/数据清洁），配反例测试
5. **删前加监控**：Seetong 删代码前加 1-2 周引用监控，确认 0 引用再删
6. **架构约束入 Loop + CI**：数据清洁体检/字段命名/反馈分类规则/报警阈值 → CI 卡口自动跑，与 seetong-feedback-radar 衔接做反馈分类 Loop 自动化

## 关联 + 备注

- **上游**：Linux 内核稳定性分配 + Addy Osmani Loop Engineering 推文 + Sairahul1 Loops 推文
- **同级**：[[02-ai-coding/Addy-Osmani-Loop-Engineering]] / [[02-ai-coding/AI循环-Claude-GPT和Mira到底什么才是真正好用的]] / [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] / [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]] / [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]]
- **限制**：lencx 独立开发者视角；"AI Coding 代码量 10x 增长"是经验判断非独立统计；Linux 内核稳定性简化表述
