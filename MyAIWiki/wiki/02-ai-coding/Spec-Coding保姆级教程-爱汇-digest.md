---
title: Spec Coding 保姆级教程 - 速读
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 场景/技术博客
  - 节点/Spec-Kit
  - 节点/SDD
links:
  - "[[Spec-Coding保姆级教程-爱汇]]"
date: 2026-08-27
source: 智谱AI开放文档（原作者：爱汇）
---

# Spec Coding 保姆级教程 - Digest

## 一句话总结

Spec-Kit 把"规格"升级为可执行指令（constitution → specify → clarify → plan → tasks → implement 六步流水线），让通用 AI 助手从"打字员"变按图施工的"靠谱工程师"，终结 Vibe Coding 反复拉扯。

## 节点速查 + 关键数字

| 节点 | 一句话 | 关键数字 |
|---|---|---|
| Spec-Kit | GitHub 开源 AI 编程工作流框架（34k+ Star） | 上线几个月狂揽 34k+ Star |
| SDD | 规格驱动开发，规格成为唯一真理 | 颠覆"代码为王"的传统开发 |
| Vibe-Coding | 感觉式编程，无规格反复试错 | 项目一复杂就崩 |
| 六步流水线 | constitution→specify→clarify→plan→tasks→implement | 6 命令（5 必选 + 1 可选） |
| /constitution | 写入技术栈/风格/测试等约束 | 项目宪法，所有 AI 调用受限 |
| /specify | 转自然语言需求为结构化 spec.md | 自动建版本目录 + git 分支 |
| /clarify | AI 主动反问消除模糊（可选） | 反向环节最被低估 |
| /plan | 生成 plan.md + data-model.md + contracts/ + research.md | 4 个产物文件 |
| /tasks | 拆解为可勾选任务清单 | 支持 YOLO 或单任务 review |
| /implement | 按 tasks.md 严格施工 | 支持 Claude Code/Copilot/Gemini/通义千问等 |

## 关键金句与反直觉

- **"Vibe Coding 已死，Spec Coding 当立！"**（文章终结论断）
- **"代码为规格服务，而不是规格为代码服务"**（SDD 根本翻转）
- **"规格不再是写完就扔的静态文档，而是可以被执行、被验证的'源代码'"**
- **`/constitution` 是被低估的杠杆**：团队 3 年沉淀的代码风格/架构约定可一次性写入宪法
- **"从打字员变成能够理解意图、参与设计的工程师伙伴"**（AI 协作范式）
- **反直觉 1**：Spec-Kit 不是新 AI 工具而是 harness —— 不替代 Claude Code，是给它加工作流约束；换 AI 厂商不用换工作流
- **反直觉 2**：`/clarify` 比 `/specify` 更影响产出 —— 跳过消歧看似省时间，实际在 plan/tasks 阶段带来指数级返工

## Seetong 借鉴动作

- **iOS 端沉淀** `constitution.md`：把 QMUI 强制用法 + ST 类前缀 + ViewController 命名约定 + ARC/MRC 边界一次性写入，让 Claude Code 改 Seetong 代码自动遵守
- **Android 端试点** `specify init .`：挑非核心功能（如告警规则 UI）跑完整流水线，验证老项目渐进集成可行性
- **Bug 模板升级**：把 `/tasks` 思想套到 issue 模板，强制按"复现→根因→验证→影响"4 段拆
- **三端 + 2 SDK 共享宪法**：iOS/Android/SDK + C/C++ 共用一份宪法，把约定变可复用资产

## 强关联 + 备注

- **横评** → [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]]：Spec-Kit vs OpenSpec vs Superpowers
- **企业落地** → [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]：Spec-Kit vs BMAD
- **范式表达** → [[Anthropic发布AI-Native软件开发流程-时代变了-该换套模式了]]：提交产物版本化
- **互补视角** → [[大淘宝技术-AI-Coding-环境与验证驱动]]：Spec 定"做什么"，环境/验证定"做得对不对"
- **方法论上游** → [[AICoding之后-如何让Agent进入企业研发全链路-得物推荐的Harness实践]]：Harness 把 SDD 接入 PDCA
- **备注**：工具入门教程未深入**评估指标**（任务完成度、宪法遵守率）；与同类横评**未独立验证**，建议交叉参考

**透明玻璃自检**：wiki 7.3K(≤8K)/ digest 3.8K(≤4K)/ 节点 10(6-10)/ H2 5 wiki / H2 5 digest(≤5)/ 表格 1 wiki / 表格 1 digest(≤2)/ 0 陈词 ⭐⭐⭐