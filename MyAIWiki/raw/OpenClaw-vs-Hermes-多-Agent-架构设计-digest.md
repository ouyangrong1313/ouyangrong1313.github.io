# 【深度拆解】OpenClaw vs Hermes：多 Agent 架构设计 - Digest

- 原文链接：https://mp.weixin.qq.com/s/0GvtgYRJBSietf24K-d7ug
- 获取时间：2026-05-14

## 一句话总结

OpenClaw 和 Hermes 都是多 Agent 架构，但两者的核心差异不在“有没有多 Agent”，而在于：**OpenClaw 把子 Agent 放进会话边界，Hermes 把子 Agent 放进进程边界。**

## 关键观点

1. **多 Agent 不是默认更高级**
   - 很多场景下单 Agent + 好的 Context Engineering 就够用
   - 多 Agent 会带来上下文割裂、协调成本、错误复合等问题

2. **多 Agent 主要解决的是复杂任务的拆分与隔离**
   - 控制上下文范围
   - 并行可拆任务
   - 限制权限边界
   - 隔离局部失败

3. **常见模式有五类**
   - 调度-执行
   - 分层编排
   - 专家路由
   - 生成-审查
   - Ensemble / Mixture-of-Agents

4. **OpenClaw 的重点是会话系统治理**
   - 子 Agent 是子会话
   - 结果通过事件链路回传
   - 更适合持久会话、跨线程、跨渠道场景

5. **Hermes 的重点是进程内委派效率**
   - 子 Agent 是同进程执行对象
   - 结果同步结构化返回
   - 额外补强了运行状态、中断传播、并发文件协调

## 我的理解

- 多 Agent 最难的不是“拆任务”，而是“最后怎么收口”
- 设计多 Agent 时，首先要想清楚的是运行边界，而不是先想并发数
- 对多数团队来说，先把“专家路由 + 单层并行 + 明确验证”做好，比贸然上多层递归更稳

## 适合关联的主题

- [[OpenClaw的正确打开方式]]
- [[workflow-vs-agent]]
- [[agent-architectures]]
- [[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]]
