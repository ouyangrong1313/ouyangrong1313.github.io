# Agent 架构模式

## 常见架构模式

### 1. ReAct (Reasoning + Acting)

**核心思想**：交替进行推理和行动

```
Thought → Action → Observation → Thought → ...
```

**适用场景**：
- 需要调用外部工具的任务
- 多步骤复杂任务
- 需要推理+执行的场景

---

### 2. Plan-and-Execute

**核心思想**：先规划，再执行

```
Planner: 生成完整计划
Executor: 按计划执行每一步
```

**适用场景**：
- 目标明确但步骤复杂的任务
- 需要预判执行路径

---

### 3. Executor 模式

**核心思想**：Agent自主决定下一步行动

- 每次收到反馈后决定是否继续
- 更灵活但更难控制

---

### 4. Control Signal

**核心思想**：通过控制信号引导Agent行为

- 自适应上下文窗口
- 动态策略选择
- 状态标记

---

## Multi-Agent 编排

### LangGraph

**核心思想**：用状态机编排多Agent

- 节点 = Agent或工具
- 边 = 状态转换规则
- 状态 = 共享上下文

```python
# 示例结构
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_agent)
workflow.add_node("executor", executor_agent)
workflow.add_edge("planner", "executor")
```

---

### AutoGen (微软)

**核心思想**：多智能体对话框架

- Agent之间可以对话协作
- 支持人类介入
- 适合复杂协作场景

---

### CrewAI

**核心思想**：角色扮演的多Agent框架

- 定义不同角色的Agent
- Agent有明确的任务和目标
- 支持顺序和并行执行

---

## Function Calling

### 核心概念
让LLM调用外部函数/工具

### 关键要素
- **JSON Schema** — 定义函数签名
- **并行调用** — 一次调用多个函数
- **错误处理** — 函数调用失败的兜底

---

## 标签

#主题/AIAgent #场景/技术博客

## 相关链接

- [[index]]
- [[harness-engineering|Harness Engineering]]
- [[tool-use|工具调用机制]]
