# WorkBuddy Harness 工程复盘：从模型到可用 Agent - Digest

## 一句话总结

WorkBuddy 这篇长文最有价值的地方，不是再讲一遍“模型很强”，而是把 **Function Call / MCP / Skill / Plugin、Context Engineering、Memory、Harness、Loop、业务验证边界** 串成一条完整的产品化链路：**模型决定上限，上下文和 Harness 决定能不能稳定落地。**

## 5 段核心论证（速查表）

| 段 | 主题 | 核心命题 | 关键结构 |
|---|---|---|---|
| 1 | 模型抽象 | 模型先看成无状态函数；状态和实时信息都在模型外维护 | 预训练 / 后训练 / 偏好优化 |
| 2 | 能力分层 | Function Call / MCP / Skill / Plugin 解决不同层次问题 | 动作协议 / 外部接入 / 任务流程 / 能力分发 |
| 3 | 上下文与记忆 | Context 不是堆 token；Memory 不是越多越好 | 5 个上下文动作 + 5 类长期记忆 |
| 4 | Harness | Harness = 驾驭 + 约束 + 整合；最终落成 5 层控制系统 | 运行环境 / 引导 / 反馈 / 编排 / 迭代 |
| 5 | Loop 与边界 | Loop 解决跨时间连续执行；业务正确性仍是最大验证缺口 | 8 个 Loop 组件 + 4 个验证问题 |

## 10 节点速查

1. **无状态模型**：模型不记状态、不自动联网、不自动执行动作
2. **工具调用协议**：模型发请求，Agent 真执行；权限和审计都在模型外
3. **MCP 三原语**：Resources / Tools / Prompts
4. **SkillPlugin 分层**：Tool 管动作，Skill 管流程，Plugin 管打包分发
5. **上下文五动作**：Write / Select / Retrieve / Compress / Isolate
6. **长期记忆准入**：稳定事实、知识背景、行为信号、表达偏好、会话延续
7. **Harness 三能力**：Steer / Constrain / Integrate
8. **五层 Harness**：运行环境 / 引导 / 反馈 / 编排 / 迭代
9. **Loop 组件**：Trigger / Workspace / Skills / Tools / Sub-agents / Memory / Sensors / Stop Conditions
10. **业务验证缺口**：实现、测试和 PRD 可能共享同一个误解

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

1. **先统一词汇表**：把 Tool / MCP / Skill / Plugin 的边界写成一页规则，避免不同人把流程、工具、插件混着说
2. **把 Context 五动作做成检查表**：每个新 Skill 都过一遍 Write / Select / Retrieve / Compress / Isolate
3. **Memory 和 Skill 硬切分**：用户事实进 Memory，稳定做法进 Skill，别让偶然有效的流程长期污染系统
4. **Harness 先补反馈层**：lint / build / test / review / E2E / rollback / audit 先补齐，再谈更强自治
5. **Loop 必须绑验证器**：定时任务、版本回顾、报警汇总如果没有 eval 和 stop condition，就不算可用 Loop
6. **先挑高 Harnessability 模块试点**：优先选结构清晰、验证信号足、回滚成本低的模块

## 关联 + 备注

**关联**：[[Lilian-Weng-Harness-Engineering-自我改进]]（理论原典） / [[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]]（工程实战） / [[Loop-Engineering-验证才是瓶颈]]（验证边界） / [[0xCodez-Agent-Harness-14-Steps]]（路线图） / [[HarnessEngineering企业级实战]]（Pipeline 门禁） / [[AI-团队协作-Loop-SDD]]（组织协作补丁） / [[腾讯-AI-Agent-Skill-测评方案落地]]（评测工程）

**备注**：这篇文章最强的是“解释层”和“结构层”，不是给出可直接复制的代码实现；业务正确性验证缺口被指出了，但没有给出成熟通解。
