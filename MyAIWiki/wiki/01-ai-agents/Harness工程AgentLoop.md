# Harness 工程与 Agent Loop

## 一句话

Harness = 给无状态的 LLM 装上"脚手架"，让它从"文本补全工具"变成"智能体"。

## 核心公式

```
Agent = Model + Loop + Tools + Context Management
```

**Agent Loop 最小循环（20行）**：
```python
messages = []
while True:
    response = llm(messages, tools=available_tools)
    messages.append(response)
    
    if response.stop_reason != "tool_use":
        return response.text
    
    for tool_call in response.tool_calls:
        result = execute(tool_call)
        messages.append({"role": "tool", "content": result})
```

## 5 个关键工程决策

| 维度 | 核心问题 | 解决方案 |
|------|---------|---------|
| **生命周期** | 防止死循环 | Max Iterations + 僵死检测 + 资源配额 |
| **上下文管理** | "记不住" | 分层状态树（最佳）、摘要压缩、滑动窗口 |
| **工具挂载** | 模型与物理世界打通 | 原生 Function Calling / ReAct XML |
| **容错自愈** | 工具执行失败 | 混合：业务异常靠模型，系统异常靠 Harness |
| **调度拓扑** | 单 Agent 效率 vs 多 Agent 协同 | 单 Agent 并发 / 多 Agent（Planner+Executor） |

## 上下文管理策略对比

| 策略 | 适用场景 | 缺点 |
|------|---------|------|
| 全量回灌 | 极短任务 | 成本高 |
| 滑动窗口 | 简单任务 | 易丢早期约束 |
| 摘要压缩 | 中等任务 | 信息损耗 |
| **分层状态树** | **长程任务** | 复杂但最稳 |

参考 Claude Code `/compact` 机制。

## 4 大失效场景

| 场景 | 根因 | 解法 |
|------|------|------|
| 上下文雪崩 | 多次压缩后决策变形 | 分层状态树 + 定期 Reflection |
| 工具幻觉 | 小模型虚构工具/参数 | Harness Schema 校验 |
| 状态机死锁 | 陷入局部最优 | LLM-as-a-Judge 评估 |
| 目标发散 | 几十步后偏离核心诉求 | 工具白名单 + 步数预算 |

## 从 Demo 到工业级

参考项目：https://github.com/shareAI-lab/learn-claude-code

```
s01-s02: 基础连通，打通模型→工具
s03-s06: 稳定性，Todo防漂移 + Subagent隔离 + Context Compact
s07-s12: 工业级，持久化 + 多 Agent 协同 + 工作目录隔离
```

## 核心法则

> **The model is the agent. The code is the harness.**

模型的能力被锁死在"单次推理"，Harness 负责：
- 容错（不让它崩溃）
- 可控（不让它跑偏）
- 高效（不让它浪费资源）

## 未来

Harness 会不会被模型"吞噬"？
- 可能：模型进化后内部跑完整个闭环
- 不可能：企业级需要权限管控/审计/安全隔离

---

## 相关资源

- 原文：[[2026-05-07-Harness工程AgentLoop]]
- GitHub: https://github.com/shareAI-lab/learn-claude-code
- 相关：[[Skills驱动推理新范式]] / [[agent-architecture]]