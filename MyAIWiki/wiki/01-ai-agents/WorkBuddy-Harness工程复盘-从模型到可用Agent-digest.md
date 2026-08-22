---
title: WorkBuddy Harness 工程复盘：从模型到可用 Agent（速读摘要）
category: 01-ai-agents
tags:
  - 主题/WorkBuddy
  - 主题/Harness
  - 主题/Context-Engineering
  - 主题/Loop-Engineering
  - 主题/MCP
  - 主题/Skill
  - 主题/Memory
  - 场景/产品拆解
type: digest
date: 2026-07-12
source: 微信公众号「Founder Park」2026-07-12 推送 / Anne（WorkBuddy 团队策略产品经理）
原始链接: https://mp.weixin.qq.com/s/GkhemHUAhKWV-3Uxaa1Mqg
nodes: []
---

# WorkBuddy Harness 工程复盘：从模型到可用 Agent（速读摘要）

> **一句话**：这篇文章把 Agent 产品从“模型 + prompt”拆回成完整工程系统：**Function Call / MCP / Skill / Plugin 负责能力分层，Context / Memory 负责信息调度，Harness / Loop 负责执行控制与持续运行，业务验证缺口决定自治上限。**

## 速查表

| 维度 | 核心命题 | 关键结构 |
|---|---|---|
| 模型抽象 | 模型先看成无状态函数，状态和实时信息都在模型外维护 | 预训练 / 后训练 / 偏好优化 |
| 能力分层 | Tool / MCP / Skill / Plugin 不是一回事 | 动作协议 / 外部接入 / 任务流程 / 能力打包 |
| 上下文工程 | Context 不是堆 token，而是信息调度 | Write / Select / Retrieve / Compress / Isolate |
| 长期记忆 | 不是越记越好，而是决定谁有资格影响未来 | 5 类长期记忆 + 作用域分层 |
| Harness | Harness = 驾驭 + 约束 + 整合 | 5 层 Harness 控制系统 |
| Loop | Goal 不等于 Loop | 8 个组件 + Trigger / Eval / Stop Condition |
| 边界 | 业务正确性缺口仍然存在 | 4 个验证问题 + 自治度分级 |

## 10 节点速查

1. **无状态模型** = 状态、记忆、实时信息都要在模型外维护
2. **工具调用协议** = 模型提请求，Agent 真执行；权限和审计都在模型外
3. **MCP 三原语** = Resources / Tools / Prompts
4. **SkillPlugin 分层** = Tool 管动作，Skill 管流程，Plugin 管分发
5. **上下文五动作** = Write / Select / Retrieve / Compress / Isolate
6. **长期记忆准入** = 稳定事实 / 知识背景 / 行为信号 / 表达偏好 / 会话延续
7. **Harness 三能力** = Steer / Constrain / Integrate
8. **五层 Harness** = 运行环境 / 引导 / 反馈 / 编排 / 迭代
9. **Loop 组件** = Trigger / Workspace / Skills / Tools / Sub-agents / Memory / Sensors / Stop Conditions
10. **业务验证缺口** = 实现、测试和 PRD 可能共享同一个误解

## 5 个关键结构

- **5 个 Context 动作**：Write / Select / Retrieve / Compress / Isolate
- **3 个 MCP 原语**：Resources / Tools / Prompts
- **5 类长期记忆**：稳定事实 / 知识背景 / 行为信号 / 表达偏好 / 会话延续
- **5 层 Harness**：运行环境 / 引导 / 反馈 / 编排 / 迭代
- **8 个 Loop 组件**：Trigger / Worktree / Skills / Tools / Sub-agents / Memory / Sensors / Stop Conditions

## 3 个反直觉点

- **System Prompt 只能引导，不能强制**：真正的权限校验、Sandbox、Approval Gate 都必须在模型外执行
- **Procedural Memory 不应该直接进长期记忆**：做事方法一旦以长期记忆注入，会把一次偶然有效的流程误升级成长期规则
- **Goal 不等于 Loop**：保存长期目标只是状态组件；真正的 Loop 还需要触发器、验证器、执行环境和停止条件

## 6 个对 Seetong 团队可借鉴动作

1. **统一词汇表**：Tool / MCP / Skill / Plugin 的边界写成一页规则
2. **Context 五动作检查表**：每个新 Skill 都过一遍 Write / Select / Retrieve / Compress / Isolate
3. **Memory 与 Skill 硬切分**：用户事实进 Memory，稳定做法进 Skill
4. **Harness 先补反馈层**：lint / build / test / review / E2E / rollback / audit 先补齐
5. **Loop 必须绑验证器**：没有 eval 和 stop condition 的定时任务，不算可用 Loop
6. **先挑高 Harnessability 模块试点**：优先做结构清晰、验证信号足、回滚成本低的模块

## 关联 + 备注

**关联**：[[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] / [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] / [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] / [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] / [[01-ai-agents/HarnessEngineering企业级实战]] / [[01-ai-agents/AI-团队协作-Loop-SDD]] / [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]

**备注**：这篇文章最强的是“解释层”和“结构层”，不是给出可直接复制的代码实现；业务正确性验证缺口被指出了，但没有给出成熟通解。
