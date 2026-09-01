---
title: Spec Coding 保姆级教程
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 场景/技术博客
  - 节点/Spec-Kit
  - 节点/SDD
  - 节点/规格驱动
  - 节点/Vibe-Coding
  - 节点/AI-Harness
  - 节点/工作流
nodes:
  - Spec-Kit
  - SDD
  - Vibe-Coding
  - 六步流水线
  - /constitution
  - /specify
  - /clarify
  - /plan
  - /tasks
  - /implement
links:
  - "[[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]]"
  - "[[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]"
  - "[[Anthropic发布AI-Native软件开发流程-时代变了-该换套模式了]]"
  - "[[大淘宝技术-AI-Coding-环境与验证驱动]]"
  - "[[AI-Coding的顿悟时刻]]"
  - "[[AICoding之后-如何让Agent进入企业研发全链路-得物推荐的Harness实践]]"
date: 2026-08-27
source: 智谱AI开放文档（原作者：爱汇，微信公众号首发）
source_url: https://docs.bigmodel.cn/cn/coding-plan/best-practice/spec-kit
---

# Spec Coding 保姆级教程

- 原文链接：https://docs.bigmodel.cn/cn/coding-plan/best-practice/spec-kit
- 微信公众号原文：https://mp.weixin.qq.com/s/CRH4WWtrA_3APBBFD1zMiQ
- 作者：爱汇
- GitHub 项目：github.com/github/spec-kit（34k+ Star）
- 获取时间：2026-08-27（通过 Mintlify `/cn/coding-plan/best-practice/spec-kit.md` 端点直拉，12.8KB）

## 核心结论（一句话）

> Spec-Kit 把"规格"从静态文档升级为可执行指令（constitution → specify → clarify → plan → tasks → implement 六步流水线），让 Claude Code / Copilot / Gemini 从"打字员"变成按图施工的"靠谱工程师"，终结 Vibe Coding 的反复拉扯。

- **场景**：AI Coding 工具实践教学（保姆级教程）
- **类型**：工具实战教程 + 方法论
- **标签**：#主题/AI-Coding #场景/技术博客 #节点/Spec-Kit #节点/SDD #节点/规格驱动 #节点/Vibe-Coding #节点/AI-Harness #节点/工作流

## 知识节点（10 个独立概念）

- **Spec-Kit**：GitHub 2025 年开源的 AI 编程工作流框架（34k+ Star），通过 CLI 工具 + 命令把 Claude Code/Copilot/Gemini 等通用 AI 助手约束为按规格施工的工程师
- **SDD**：Spec-Driven Development，规格驱动开发；规格成为唯一真理，代码为规格服务（而非反过来）
- **Vibe-Coding**：感觉式编程，无规格无约束，靠反复试错推进；项目一复杂就崩
- **六步流水线**：constitution → specify → clarify（可选）→ plan → tasks → implement，强制节奏
- **/constitution**：项目宪法命令；写入技术栈偏好、代码风格、测试要求、UX 原则等约束，所有后续 AI 调用都受其限制
- **/specify**：把自然语言需求转化为结构化 `spec.md`（用户故事 + 验收标准 + 边界条件），自动创建 `specs/{NNN}-{slug}/` 版本目录和 git 分支
- **/clarify**：AI 主动反问消除需求模糊（"庆祝动画是放烟花还是撒花？"），把人类隐含偏好显式化为 spec 条目
- **/plan**：根据宪法 + 需求生成完整技术方案（plan.md + data-model.md + contracts/ + research.md）
- **/tasks**：把 plan 拆解为可勾选的任务清单（Phase 1 / Phase 2 / T001 / T002 ...）
- **/implement**：按 tasks.md 严格施工，每完成一项 `[x]` 打勾；支持 YOLO 一口气跑完或单任务人工 review

## 关联图谱

### 上游（基于 / 来自）

- [[AICoding之后-如何让Agent进入企业研发全链路-得物推荐的Harness实践]]：Spec-Kit 是 Harness 实践的工具级落地，PDCA 框架在 SDD 中的具体化
- [[宝玉AI-我的AI原生开发流程-真实案例复盘]]：宝玉强调的"先可行性再设计"思想，与 `/clarify` 在流程入口前置的需求澄清同源

### 同级（横向 / 并列）

- [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]]：Spec-Kit vs OpenSpec vs Superpowers 三种 SDD 工具横评，本文可作为 Spec-Kit 侧的实战补充
- [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]]：Spec-Kit vs BMAD 在企业落地 SDD 的对比
- [[Anthropic发布AI-Native软件开发流程-时代变了-该换套模式了]]：Anthropic 的 AI-Native SDLC 也强调"提交产物版本化"，与 Spec-Kit 的 `001-xxx/spec.md` 思路一脉相承
- [[大淘宝技术-AI-Coding-环境与验证驱动]]：永霸认为代码生成趋近被解决后瓶颈在环境与验证；本文强调规格驱动；两者互补——规格定"做什么"，环境与验证定"做得对不对"
- [[AI-Coding的顿悟时刻]]：AI Coding 的顿悟系列中的工具实战篇

### 下游（应用于 / 验证于）

- 待补充（本文是工具入门，后续应用 Seetong 三端的实战待落地）

## 正文要点（7 条 + 命令映射）

- **规格成为唯一真理**：代码为规格服务（而非反过来）。`规格 → 计划 → 任务 → 代码` 每一步都有 git 友好的版本化产物，整条流水线天然可回滚、可审计、可对比
- **`/constitution` 是被低估的杠杆**：很多团队跳过这一步导致 `/specify` 时 AI 反复猜技术栈；正确的做法是先把团队 3 年沉淀的代码风格/架构约定/测试要求一次性写入宪法
- **`/clarify` 是 AI 主动反问的反向环节**：需求模糊时让 AI 反问你，把人类隐含偏好显式化，从源头消灭返工；这一环节经常被跳过，结果是后面 plan/tasks 阶段反复返工
- **每个 step 都生成版本化目录**（如 `001-todo-app-core-features/`），git 分支自动创建（`feat/001-xxx`），所有历史保留，迭代过程清清楚楚
- **AI 工具无关性**：Spec-Kit 支持 Claude Code / Copilot / Gemini / Cursor / 通义千问 / Roo Code；spec 格式 + plan 格式 + tasks 格式是 AI 中立的，未来换模型也能跑
- **不是新 AI 工具而是 harness**：Spec-Kit 不替代 Claude Code，而是给它加一套工作流约束；定位类似 Hooks / Subagents 对 Claude Code 的扩展关系
- **支持老项目渐进试点**：`specify init .` 不动现有代码，先从一个新功能模块试点；需求变了回到 `/specify` 重新走流程而非直接改代码

**六步流水线命令 / 产物 / 必选映射**：

| 阶段 | 命令 | 产物 | 必选？ |
|---|---|---|---|
| 准备 | `specify init` | `.claude/` + `.specify/` | 必选 |
| 宪法 | `/speckit.constitution` | `constitution.md` | 强烈推荐 |
| 需求 | `/speckit.specify` | `specs/{NNN}-{slug}/spec.md` + git 分支 | 必选 |
| 消歧 | `/speckit.clarify` | 更新 `spec.md` | 可选 |
| 方案 | `/speckit.plan` | `plan.md` + `data-model.md` + `contracts/` + `research.md` | 必选 |
| 拆解 | `/speckit.tasks` | `tasks.md` | 必选 |
| 施工 | `/speckit.implement` | 代码 + 测试 | 必选 |

## 我的理解（Seetong 借鉴）

- **iOS 端**：把"QMUI 强制用法 + ST 类前缀 + ViewController 命名约定 + ARC/MRC 边界"沉淀为 `constitution.md`，让 Claude Code 改 Seetong 代码时自动遵守
- **Android 端**：先挑非核心功能（如告警规则 UI）跑 `specify init .` 试点，验证老项目渐进集成可行性
- **不盲从**：Spec-Kit 是工具级方案非范式定论；同时段还有 OpenSpec / Superpowers / BMAD 等同类工具，应按团队规模与项目复杂度选用

**透明玻璃自检**：wiki 7.5K(≤8K)/ digest 4.2K(待 ≤4K)/ 节点 10(6-10)/ H2 4 wiki / H2 5 digest(≤5)/ 表格 1 wiki / 表格 0 digest(≤2)/ 0 陈词 ⭐⭐⭐