# AI 知识库技术演进拆解：从 RAG 到 NotebookLM，再到 LLM Wiki - Digest

- 原文链接：https://mp.weixin.qq.com/s/UtN4_bhOYBV3OnYIUGN4LQ
- 获取时间：2026-05-14

## 一句话总结

NotebookLM 不是“脱离 RAG”的新物种，而是把文档理解、多索引检索、检索排序、上下文装配和引用追溯做成黑盒产品的高阶 RAG 系统；而 LLM Wiki 则进一步把“查询式问答”推进成“编译式知识沉淀”。

## 关键观点

1. **NotebookLM 本质仍是 RAG，但不是低配 RAG**
   - 它把复杂链路产品化、黑盒化了

2. **真正决定知识库上限的，往往不是向量库，而是文档理解**
   - 标题层级
   - 章节树
   - 表格结构
   - 页码与引用关系

3. **高阶知识库需要多粒度 chunk + 多索引体系**
   - 向量检索
   - 关键词/BM25
   - 元数据索引
   - 文档树索引
   - 引用索引

4. **Retrieval and Ranking 前面还有问题理解与 query planning**
   - 不是直接把用户问题丢进向量库

5. **Context Engineering 是产品级知识库的分水岭**
   - 长上下文不是全文乱塞，而是结构化组织证据和辅助信息

6. **LLM Wiki 的意义在于知识持续沉淀**
   - 从“每次重新拼答案”走向“增量维护结构化 Wiki”

## 我的理解

- 很多企业知识库失败，不是输在模型，而是输在前处理和文档结构还原
- NotebookLM 值得学的，不是“它不用 RAG”，而是“它把 RAG 做成了用户无感的产品”
- AI 知识库长期会从“能回答”走向“能编译、能沉淀、能持续演化”

## 适合关联的主题

- [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]]
- [[企业知识库认知底座]]
- [[llm-agent-unified-memory-framework]]
- [[karpathy-knowledge-system]]
