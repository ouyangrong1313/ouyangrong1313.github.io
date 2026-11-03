---
title: 亲自答丨如何评价 DeepSeek Harness 发布的 Super-agent 构想？
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Agent架构
  - 主题/长期记忆
  - 主题/AI治理
  - 手法/分层控制
  - 手法/证据边界
  - 场景/公众号长文
nodes: [Super-agent命名, 连续性与吞吐量, 跨Session长期记忆, 主Agent与Executor, 运行态与语义记忆, 计算状态环境解耦, 受信原型边界, Session外人机协作, 上下文边界与A2A, Agent安全与隐私]
links:
  - "[[01-ai-agents/Datawhale-DeepSeek-Super-Agent架构-Router-Worker双层]]"
  - "[[01-ai-agents/范冰-dsh-superagent-主动型Coding-Agent工程常识]]"
  - "[[01-ai-agents/InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]"
  - "[[01-ai-agents/从零设计生产级-Multi-Agent-Harness]]"
date: 2026-11-03
source: 微信公众号 / 知乎日报（问答回答者：崔添翼）
status: published
---

# 亲自答丨如何评价 DeepSeek Harness 发布的 Super-agent 构想？

- 原文链接：https://mp.weixin.qq.com/s/eP_4prXjvvrthOzTdBCL7w
- 发布账号：微信公众号「知乎日报」
- 回答者：崔添翼；回答中自述为 DeepSeek 产品部负责人、原文最终审稿人之一
- 发布时间：2026-11-02 20:00
- 获取时间：2026-11-03

## 核心结论（一句话）

Super-agent 指在执行任务的主 Agent 上方增加一层协调角色，尝试拆解跨任务连续性与吞吐量的冲突；它不是“更强的 Agent”，也不等于已经解决长期记忆、安全或规模化协作的生产系统。

## 分类提炼

- 场景：Agent 架构理解、长期任务与多 Agent 工作流设计
- 标签：双层架构、跨任务连续性、长期记忆、上下文边界、安全治理
- 类型：产品负责人问答 / 研究原型解读

## 知识节点（10 个独立概念）

- **Super-agent 命名**：Super 表示位于执行 Agent 上方的协调层，不代表模型或 Agent 能力天然更强。
- **连续性与吞吐量**：跨任务维持统一上下文与并行处理多个任务之间存在系统取舍，双层结构试图将两类职责分离。
- **跨 Session 长期记忆**：回答者称截至 2026-11-02，DeepSeek Harness 尚无内置跨 Session 长程记忆；该产品状态可能变化。
- **主 Agent 与 Executor**：上层 Session 负责判断和派工，下层 Session 承担具体 Ticket；交接契约决定隔离带来的成本。
- **运行态与语义记忆**：持久化 Ticket、Assignment、Input 或 Outbox 可支持执行恢复，但不能因此推断系统拥有跨任务项目知识记忆。
- **计算状态环境解耦**：回答者指出文章讨论的部分设计仍需大量工程实现；架构表述不代表原型已经完整具备。
- **受信原型边界**：回答者称当前原型只在小规模、受信任的内部环境跑通，外部规模和参与者复杂度尚未验证。
- **Session 外人机协作**：当用户在 Agent Session 之外插话、暂停或要求调整时，任务所有权和恢复规则仍是待解决问题。
- **上下文边界与 A2A**：Agent 间通信需要明确传递哪些上下文、哪些身份和权限随任务转移，而不只是交换消息。
- **Agent 安全与隐私**：源码、凭据、用户数据与执行环境的隔离，是从内部原型走向现实部署前仍需验证的设计问题。

## 关联图谱

### 上游（基于 / 来自）

- [[01-ai-agents/Datawhale-DeepSeek-Super-Agent架构-Router-Worker双层]]：同一 Super-agent 架构文章的技术解读，是本问答讨论的直接背景。
- `dsh-superagent-prototype`：DeepSeek Harness 团队公开的研究原型；回答者说明代码、设计和实验主要来自 Harness 团队其他成员。

### 下游（应用于 / 验证于）

- 当前知识库尚无基于本问答完成的生产部署或对照验证条目。Seetong 场景的迁移判断应以实际任务连续性、并发、恢复与安全证据为依据。

### 同级（横向 / 并列）

- [[01-ai-agents/范冰-dsh-superagent-主动型Coding-Agent工程常识]]：同一原型的工程机制与个人自动化反思；本篇补充作者对原型成熟度和长期记忆边界的说明。
- [[01-ai-agents/InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]：对照控制面职责与执行循环复杂度的讨论。
- [[01-ai-agents/从零设计生产级-Multi-Agent-Harness]]：从权限、评估、恢复与生产治理角度扩展多 Agent 设计。

## 机制解读：三种“连续性”

讨论 Agent 是否“记得住”时，至少要拆成三件事：

1. **会话连续性**：当前 Session 是否保留对话和上下文。
2. **任务连续性**：Ticket、Assignment、输入、分支和投递记录能否在中断后恢复。
3. **语义连续性**：跨 Session 是否能可靠检索长期项目知识、决策理由与经验。

Super-agent 的双层结构主要尝试让上层承担跨任务协调、下层并行执行具体任务；Stored Work 一类机制针对任务状态恢复。它们不能自动推出第三种能力已解决。回答者对当时 Harness 长期记忆现状的描述正好提醒：显式任务账本、会话历史和项目知识库是不同资产。

## 对 Seetong AI 工作流的启发

- 先识别瓶颈：若主要问题是上下文缺失，补强 `CONTEXT.md`、ADR、intent/spec 和任务证据；若是重复抢同一工作，再考虑 Thread 队列和独立 worktree。
- 保持授权独立于上下文：Issue 正文、评论和引用文档可以成为输入，不应自动提升任务权限；Trust tier、MR review 和发布 gate 仍由外部规则决定。
- 将“Ticket 可恢复”作为验证项：服务重启后能否定位分支、已完成步骤和待发回复，需要故障注入与 GitLab 记录验证，不以 Agent 声称“记得”为证据。
- 对跨端任务显式保留宿主边界：iOS、Android、Harmony、KMP、SDK 的验证状态必须逐端记录，不能由单个 Worker Session 代替真机和 CI 证据。

## 证据边界与限制

- 这是知乎日报转载的问答；对架构动机、内部实践和未实现部分的说明来自回答者自述，不等同于外部独立评测。
- “Harness 当时没有内置跨 Session 长程记忆”是 2026-11-02 的时点陈述；“可能快有了”是预期，不作为当前产品能力承诺。
- 回答没有提供吞吐量、RAM、规模上限或可靠性数据；不据此推断硬件开销或生产成功率。
- 文中“计算/状态/环境解耦”与安全、A2A、Session 外协作均保留为设计问题或待完成工作；不视作原型已完全实现。
- 回答者指出原型在小规模受信任环境跑通；这不能外推为适合开放 GitLab、多团队或更高风险权限场景。

## 相关链接

- [原文拆解](../../raw/知乎日报-崔添翼-Super-agent构想-双层架构与边界-digest.md)
- [dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype)
