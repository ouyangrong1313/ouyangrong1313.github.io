# 构建 LLM-Wiki 智能知识库——实现 AI 辅助写作工作流 - Digest

- 原文链接：https://mp.weixin.qq.com/s/VTkeTzNejr9D39qN-jWcXg
- 获取时间：2026-05-14

## 一句话总结

这篇文章真正展示的不是“AI 写出一篇文章”，而是**如何基于 method / concepts / raw 三层知识结构，把 AI 写作变成一条可追溯、可复用、可迭代的知识生产流水线。**

## 关键观点

1. **AI 写作的稳定性来自知识结构，不只来自 Prompt**
   - 先有目录和分层
   - 再有检索、组装和输出

2. **method / concepts / raw 是三层关键结构**
   - method：场景方法模板
   - concepts：可组装知识单元
   - raw：原始材料血肉

3. **写作前必须先冻结大纲**
   - 未出完整框架，不进入正文生成

4. **concept 只是索引，raw 才能让文章长出厚度**
   - 要沿 `sources` 回到原文段落

5. **撰写阶段的核心不是创作，而是结构化组装**
   - 段首引入
   - 核心论点
   - 结构展开
   - 案例/对比
   - 段尾收束

6. **最后必须自检并沉淀 SOP**
   - 成功流程比一次性 Prompt 更有复利

## 我的理解

- LLM Wiki 的真正价值，不只是能问答，而是能支撑知识驱动的生产任务
- AI 写作如果没有 method / concepts / raw 这种分层，最终容易变成薄而散的总结文
- “先框架后内容、概念回溯原文、结构化输出”是非常值得复用的三条纪律

## 适合关联的主题

- [[AI知识库技术演进拆解-从RAG到NotebookLM再到LLM-Wiki]]
- [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]]
- [[企业知识库认知底座]]
- [[obsidian-claude-code-os]]
