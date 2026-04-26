# Prompt Engineering

## 三种范式对比

| 范式 | 说明 | 适用场景 |
|------|------|----------|
| **Zero-Shot** | 无示例，直接指令 | 简单任务 |
| **One-Shot** | 1个示例 | 格式要求 |
| **Few-Shot** | 3-5个示例 | 复杂任务、风格学习 |

---

## Chain of Thought (CoT) 思维链

### 核心思想
让模型展示推理过程，而不只是给出答案。

### 方法
1. **Zero-Shot CoT**: "Let's think step by step."
2. **Few-Shot CoT**: 提供推理示例

### 适用场景
- 数学问题
- 逻辑推理
- 多步骤任务

---

## ReAct (Reasoning + Acting)

### 核心思想
交替进行推理和行动，让模型在推理过程中调用工具。

### 模式
```
Thought → Action → Observation → Thought → ...
```

### 特点
- 结合推理和外部工具调用
- 适合复杂任务分解
- 是现代 Agent 的基础范式

---

## Prompt 优化技巧

### 结构化
- 明确角色（如"你是一个资深Python工程师"）
- 清晰的任务描述
- 明确的输出格式
- 必要的约束条件

### 迭代优化
1. 先写简单版本测试
2. 根据结果补充缺失信息
3. 添加格式要求
4. 加入few-shot示例

---

## 标签

#主题/AI Coding #场景/技术博客

## 相关链接

- [[wiki/ai-agents/agent-architectures|Agent架构模式]]
- [[wiki/ai-tech/llm-fundamentals|大语言模型基础]]
