---
title: Warp CEO 的 Claude 实战：用双 Skill 把人类反馈编译为 Agent 改进
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/自我改进
  - 主题/Skill
  - 主题/人类反馈
  - 主题/Harness
  - 场景/公众号长文
nodes: [反馈蒸发, 双Skill闭环, 最小变更PR, 程序性知识, 解释型反馈, 渐进披露, 验证门禁, 共享改进器]
links: [[01-ai-agents/一篇讲透Agent自进化飞轮怎么搭-评测→记忆→落地→控制]], [[01-ai-agents/若飞-Agent-记忆与可验证自我改进怎么设计]], [[01-ai-agents/Skill-Self-Evolution]], [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]
date: 2026-09-01
source: 微信公众号「Datawhale」；Warp CEO / Anthropic Claude Blog 案例
---

# Warp CEO 的 Claude 实战：用双 Skill 把人类反馈编译为 Agent 改进

- 原文链接：https://mp.weixin.qq.com/s/vIJ5uP5dcUd87Smi2BuP-w
- 原始案例：https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude
- 来源：Datawhale 对 Warp CEO 案例的整理
- 获取时间：2026-09-01

## 核心结论（一句话）

> 可持续改进不是让 Agent 从一次对话自动“记住”，而是将可解释的人类反馈交给独立 improver，生成可审查、可回滚的最小 Skill 变更，并以验证与人类审批决定是否进入默认行为。

## 分类提炼

- 场景：code review、issue triage、spec-writing 等可反馈 Agent
- 类型：基于文件的 Skill 改进工作流与客户案例
- 标签： #主题/AI-Agent #主题/自我改进 #主题/Skill #主题/人类反馈 #主题/Harness #场景/公众号长文

## 知识节点

- **反馈蒸发**：只在会话里纠正 Agent 不会改变下一轮行为，导致同类错误重复出现。
- **双Skill闭环**：base skill 承担任务执行，improver skill 按计划聚合反馈并提出更新建议。
- **最小变更PR**：候选经验应收敛为对具体 Skill 的小型 PR，而不是无边界重写 prompt。
- **程序性知识**：稳定的任务规范应放入可版本化、可审查、可复用的 Skill，而非动态 Memory。
- **解释型反馈**：反馈同时说明期望行为和理由，才能使 Agent 在相邻场景中泛化。
- **渐进披露**：Skill 应保持小，详细资源与脚本按需引用，避免把完整知识库一次塞入上下文。
- **验证门禁**：反馈源、回归证据和人工 review 共同防止错误经验成为长期默认规则。
- **共享改进器**：共性改进逻辑可由少数 improver 复用，领域差异再叠加局部权重。

## 关联图谱

### 上游（基于 / 来自）

- [[01-ai-agents/Skill-Self-Evolution]]：提供从任务轨迹归纳、验证和优化 Skill 的研究路径。
- [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]：为候选改动提供基线、评分器和稳定性检查方法。

### 下游（应用于 / 验证于）

- [[01-ai-agents/若飞-Agent-记忆与可验证自我改进怎么设计]]：把反馈候选如何准入、读取、发布和回滚扩展为受治理经验系统。
- [[01-ai-agents/一篇讲透Agent自进化飞轮怎么搭-评测→记忆→落地→控制]]：将这类 Skill PR 放入评测、记忆、候选发布和控制面的全链路飞轮。

### 同级（横向 / 并列）

- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]：从 Harness 视角解释为何评测与不可编辑的控制边界应位于自改进循环之外。

## 正文要点

1. Warp 的案例说明，部分正确的 code review Agent 仍可能因噪声严重损害体验；手动调 prompt 或增加 AGENTS.md 只能局部修补，核心缺口是反馈未跨会话沉淀。
2. base skill 保存领域指令，improver skill 从积累的人类反馈、原始建议及任务上下文中识别系统性问题，并只建议最小的 base skill 编辑。
3. Skill 作为文件资产进入正常 PR 流程。这样每次“学到”的规则都有变更说明、review、批准、版本历史与回滚路径。
4. `ready to spec` 漏标案例表明，带理由的维护者反馈可被转成精确的判定条件；improver 将它制成候选规则，而非把单个事件直接写成永久结论。
5. 高质量 Skill 写原则并解释原因，保持短小并按需加载资源；反馈入口则应嵌入已有工作环境，减少人为收集成本。
6. 自我改进应预设反馈会错。可验证任务优先建立 harness 和确定性检查；不可验证任务限制专家反馈，并让最终审查保持人类控制。

## 备注

- Warp 的“约 80% 正确率”、产品用户规模、融资额、运行范围与改进效果来自客户案例转述，未独立复核。
- 该模式适合稳定、可验证、低副作用的任务先行。直接将反馈自动写入高风险或开放式任务规范，可能放大偏差。

## 相关链接

- [[01-ai-agents/一篇讲透Agent自进化飞轮怎么搭-评测→记忆→落地→控制]]
- [[01-ai-agents/若飞-Agent-记忆与可验证自我改进怎么设计]]
- [[01-ai-agents/Skill-Self-Evolution]]
- [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]
