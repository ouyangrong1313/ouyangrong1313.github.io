# AI 学习笔记 2025 索引

## 源文件

~~`/Users/topsee/ouyangrong1313/MyAIWiki/raw/学习笔记2025.pdf`（343页）~~（已删除）

## 笔记结构概览

### 第一部分：AI 基础（页1-60）

#### 机器学习基础
- 监督学习、无监督学习、强化学习
- 神经网络基础
- 反向传播
- 激活函数

#### 深度学习基础
- CNN（卷积神经网络）
- RNN/LSTM
- Deep Learning Workshop 总结
- **Attention Is All You Need** ⭐

---

### 第二部分：Transformer 架构（页61-140）

#### Attention 机制
- Scaled Dot-Product Attention
- Multi-Head Attention
- Self-Attention

#### Transformer 核心组件
- Positional Encoding
- Layer Normalization
- SublayerConnection
- Feed-Forward Networks
- Dropout
- Label Smoothing

#### 优化器
- Adam (Kingma and Ba)
- 学习率调度

---

### 第三部分：大语言模型（页141-200）

#### GPT 系列
- GPT-1~GPT-4 演进
- ChatGPT 发展历程
- GPT-4 Turbo

#### LLaMA
- Meta 开源模型
- LLaMA 2

#### Prompt Engineering
- **Few-Shot** ⭐ - 3-5个示例
- **One-Shot** - 1个示例
- **Zero-Shot** - 无示例
- **Chain of Thought (CoT)** ⭐ - 思维链
- **ReAct** ⭐ - 推理+行动

#### Fine-tuning
- **RLHF** ⭐ - 人类反馈强化学习
- **LORA** ⭐ - 低秩适配
- Prefix-Tuning
- Control Signal

---

### 第四部分：RAG 系统（页201-240）

#### RAG 基础
- 检索增强生成流程
- Embeddings
- 向量数据库

#### RAG 优化
- Query 理解
- 上下文窗口
- Chunking 策略
- Re-ranking

---

### 第五部分：LangChain（页241-280）

#### LangChain 核心概念
- Chains
- Agents
- Memory
- Callbacks

#### LangChain 组件
- Document Loaders
- Text Splitters
- Embeddings
- Vector Stores
- Retrievers

---

### 第六部分：Agent 系统（页281-320）

#### Agent 架构模式
- **ReAct** ⭐ - 推理+行动
- **Plan-and-Execute** ⭐
- **Executor** 模式
- **Control Signal** ⭐

#### Multi-Agent
- **LangGraph** ⭐ - 状态机编排
- **AutoGen** ⭐ - 微软多智能体框架
- **CrewAI** ⭐ - 角色扮演 Agent 框架

#### Function Calling
- JSON Schema
- 并行调用
- 错误处理

---

### 第七部分：高级主题（页321-343）

#### 向量数据库
- Pinecone
- Chroma
- FAISS

#### Memory System
- 短期记忆 / 长期记忆
- 记忆检索
- 记忆总结

#### Control Signal 进阶
- 自适应上下文
- 动态策略选择

---

## 核心要点提炼

### 最值得掌握的10个概念

1. **Transformer** - 注意力机制替代RNN，成为LLM基础架构
2. **Attention** - Scaled Dot-Product和Multi-Head Attention
3. **RLHF** - 让LLM符合人类偏好的核心技术
4. **CoT** - 思维链提示，让模型推理更准确
5. **ReAct** - 推理和行动结合的Agent范式
6. **RAG** - 解决LLM知识过时和幻觉问题
7. **LangChain** - LLM应用开发框架
8. **LangGraph** - 复杂Agent编排的状态机方案
9. **LORA** - 高效微调大模型的方法
10. **CrewAI** - 多Agent协作框架

### 关键公式

1. **Scaled Dot-Product Attention:**
   ```
   Attention(Q,K,V) = softmax(QK^T / √d_k)V
   ```

2. **Multi-Head Attention:**
   ```
   MultiHead = Concat(head_1,...,head_h)W^O
   where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
   ```

3. **Layer Normalization:**
   ```
   LN(x) = γ ⊙ (x - μ) / √(σ² + ε) + β
   ```

---

## 相关 Wiki 页面

- [[wiki/ai-tech/index|AI Tech]] - AI技术趋势
- [[wiki/ai-agents/index|AI Agents]] - AI Agent落地方案
- [[wiki/rag-systems/index|RAG Systems]] - RAG系统
- [[wiki/ai-coding/index|AI Coding]] - AI辅助编程

## 标签

#主题/AI科技 #主题/AI-Agent #场景/技术博客
