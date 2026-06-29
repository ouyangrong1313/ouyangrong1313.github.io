# 从零设计生产级 Multi-Agent Harness - Digest

- 原文链接：https://mp.weixin.qq.com/s/JPhcyDc4JwRmnMQ-76A-FQ
- 获取时间：2026-05-14

## 一句话总结

生产级 Multi-Agent 系统真正的门槛不在 Prompt，也不在 Agent 数量，而在背后的 **Harness**：调度、工具治理、状态与记忆、评估、预算控制、MCP 接入、安全和可观测性，缺一不可。

## 关键观点

1. **Harness 是 Agent 的操作系统**
   - Prompt 解决“怎么理解任务”
   - Harness 解决“怎么可靠完成任务”

2. **Agent 负责局部智能，Harness 负责全局控制**
   - 生命周期
   - 计划裁决
   - Agent 路由
   - 失败处理
   - 硬终止条件

3. **Tool Registry 是安全边界，不是函数列表**
   - 工具必须受权限、Schema、审计、风险等级治理

4. **状态与记忆必须分层**
   - State 关注一致性
   - Memory 关注相关性
   - 记忆系统必须支持遗忘

5. **Eval 不能只看最终答案，还要看执行轨迹**
   - Component Eval
   - Trajectory Eval
   - Task Completion Eval
   - End-to-End Eval

6. **Token Budget 是生产生命线**
   - 模型路由
   - 上下文压缩
   - 分级降级与熔断

7. **MCP 降低了接工具成本，但不会替代治理**
   - MCP 提供能力
   - Harness 提供可信边界

## 我的理解

- 真正让 Agent 系统跨过 Demo 到生产鸿沟的，不是更强模型，而是更强运行时治理
- 多 Agent 最难的不是让多个 Agent 跑起来，而是让它们在成本、权限、状态、记忆和结果解释上可控
- 未来团队竞争的重点，会从“谁 Prompt 写得好”转向“谁的 Harness 更稳、更可运营”

## 适合关联的主题

- [[OpenClaw-vs-Hermes-多-Agent-架构设计]]
- [[HarnessEngineering企业级实战]]
- [[Harness工程AgentLoop]]
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
