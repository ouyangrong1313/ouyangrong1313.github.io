# RAG 基础

## 什么是 RAG

**RAG = Retrieval Augmented Generation（检索增强生成）**

解决 LLM 的两大问题：
1. **知识过时** — 模型训练数据有截止日期
2. **幻觉** — 模型会编造不存在的内容

---

## RAG 流程

```
Query → 检索 → Context → LLM → Response
         ↓
    向量数据库
```

### 核心步骤

1. **文档处理**
   - 加载文档（PDF、TXT、HTML等）
   - 分块（Chunking）
   - Embedding 向量化

2. **检索**
   - Query 向量化
   - 相似度搜索
   - Top-K 召回

3. **生成**
   - Context 组装
   - Prompt 构建
   - LLM 生成

---

## Embeddings

### 核心概念
把文本映射到向量空间，语义相似的文本距离更近。

### 常用模型
- OpenAI: text-embedding-ada-002
-开源: BGE, M3E, Instructor

---

## Chunking 策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| 固定长度 | 按字符/词数切分 | 通用 |
| 语义分割 | 按段落/句子切分 | 保留语义 |
| 递归分割 | 按层级结构切分 | 文档结构 |

---

## 向量数据库

| 数据库 | 特点 |
|--------|------|
| **Pinecone** | 云原生托管 |
| **Chroma** | 轻量级，本地开发 |
| **FAISS** | Facebook开源，适合大规模 |
| **Milvus** | 开源，云原生 |

---

## RAG 优化

### Query 理解
- Query 改写
- Query 扩展
- 同义词替换

### 上下文窗口
- 控制 Context 长度
- 重要信息优先

### Re-ranking
- 根据相关性重排
- MMR（最大边际相关）

---

## 标签

#主题/RAG系统 #场景/技术博客

## 相关链接

- [[index]]
- [[wiki/ai-coding/prompt-engineering|Prompt Engineering]]（路径格式待修正）
