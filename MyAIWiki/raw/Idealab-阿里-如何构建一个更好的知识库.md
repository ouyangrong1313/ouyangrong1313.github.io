# 如何构建一个更"好"的知识库？

- 原文链接:https://mp.weixin.qq.com/s/77n3CmJ7qzyeEiXeFCjqtA
- 原始作者:阿里 idealab 团队(idealab.alibaba-inc.com)
- 来源:微信公众号 / 阿里内网 idealab 平台
- 发布时间:2026-06(具体日期文章未标注)
- 获取时间:2026-06-11
- 获取方式:curl + UA + 抓取 js_content 区段,Python 清洗

---

## 文章摘要

本文深入探讨构建高质量 RAG 知识库的垂直技术原理与工程实践。文章首先界定知识库作为外部记忆系统的角色，并引入 RAGAS 框架从检索相关性、生成忠实度及答案相关性维度建立评估标准。随后详细拆解离线索引与在线查询流程，重点分析文档切分策略如 Late Chunking 和意图驱动切分，对比稀疏、稠密及混合检索范式，并阐述HyDE等查询增强技术。此外，文章探讨 Cross-Encoder 重排序机制以优化精度，介绍 AutoRAG 自动化优化、 QuIM-RAG 问题倒排索引及 OpenViking 文件系统范式等前沿架构，旨在通过系统性技术选型解决幻觉、召回不准等问题，实现知识库性能的端到端优化。

---

## 一、什么是 Agent 构建中的知识库？

### ▐  考古一下，RAG 的起源

RAG（Retrieval-Augmented Generation，检索增强生成） 由 Facebook AI Research（现 Meta AI）于 2020 年首次提出。

https://arxiv.org/abs/2005.11401

论文的核心贡献在于提出了一种将参数化记忆（Parametric Memory） 与非参数化记忆（Non-Parametric Memory） 相结合的架构：

- **参数化记忆**：预训练 seq2seq 模型（如 BART）的模型权重
- **非参数化记忆**：Wikipedia 语料的密集向量索引，通过 DPR（Dense Passage Retriever）构建

这一架构在开放域问答（Open-Domain QA）任务上显著超越了纯参数化模型，奠定了后续 RAG 研究的基础。

### ▐  知识库的定义

在 Agent 构建的语境下，知识库（Knowledge Base） 是一个外部记忆系统，用于存储和检索不在模型参数中的信息。它作为 RAG 架构的核心组件，承担非参数化记忆的角色。

### ▐  使用知识库可以解决什么问题？

RAG 的基本工作流程：

```
Query → Retriever（检索器） → Top-K Documents → Context Augmentation → Generator（生成器） → Response
```

其中，知识库的核心接口，就是上传和召回。不同版本和理论，就是召回的内容和排序的区别。

这个问题应该回到 LLM 的固有局限上，知识库是一种对应的解决方案：（原文此处内容未展开）

### ▐  适用场景分析

适合构建知识库的场景：

（原文此处内容未展开）

不需要知识库的场景：

（原文此处内容未展开）

### ▐  RAG vs Long Context

随着上下文窗口的扩展（Claude 200K, Gemini 1M+），需要重新审视 RAG 的适用边界：

**选型建议**：

- 数据量 < 50K tokens 且更新频率低 → Long Context
- 数据量大、更新频繁、需要精确召回 → RAG
- 混合方案：RAG 粗筛 + Long Context 精读

---

## 二、如何评判一个知识库的好坏？

如题，我们想要构建更好的知识库，那么首先需要定义"好"的标准。

### ▐  评估框架：RAGAS

RAGAS（Retrieval Augmented Generation Assessment） 是目前最广泛采用的 RAG 评估框架，其核心价值在于无参考评估（Reference-Free）——无需人工标注 ground truth 即可进行自动化评估。

RAGAS 将 RAG 系统的评估分解为三个核心维度：

- **检索相关性（Context Relevance）** —— 召回的内容跟 query 相关吗
- **生成忠实度（Faithfulness）** —— 生成的答案是否忠于检索到的上下文
- **答案相关性（Answer Relevance）** —— 答案是否回应了用户问题

这三个维度相互独立但互补，共同覆盖 RAG 系统的端到端性能。RAGAS 的关键洞察：RAG 系统的失败往往是检索和生成环节共同造成的，因此必须分别评估，才能定位问题根因。

### ▐  检索质量指标

检索环节的目标是：召回与 query 相关的文档片段，并将相关内容排在前面。

**Context Precision（上下文精确率）**

定义：评估检索器将相关文档排在不相关文档之上的能力。

计算方法：（原文公式被截断）

直观理解：如果检索了 5 个 chunks，相关的 2 个排在第 1、2 位，比排在第 4、5 位的 precision 更高。

**Context Recall（上下文召回率）**

定义：评估回答问题所需的信息有多少被成功检索到。

计算方法：

具体步骤：

- 将参考答案分解为多个 claims（声明）
- 判断每个 claim 是否可归因于检索到的上下文
- 计算被支持的 claims 占比

注意：Context Recall 需要参考答案（reference），因此不是完全的 reference-free 指标。

**传统 IR 指标**

（除 RAGAS 定义的指标外，传统 IR（Information Retrieval）指标仍然适用）

**Precision、Recall 与 F1 的关系**

F1 是 Precision 和 Recall 的调和平均数，用于在两者之间取得平衡。当 Precision 和 Recall 差异较大时，F1 会偏向较小的那个值，因此 F1 高意味着两者都不能太低。

### ▐  生成质量指标

生成环节的目标是：基于检索到的上下文，生成准确、相关的答案。

**Faithfulness（忠实度）**

定义：生成的答案在事实上是否与检索到的上下文一致。取值范围 [0, 1]，值越高表示答案忠实于上下文。

计算方法：

- 使用 LLM 从答案中提取所有声明（claims）
- 对每个声明，验证是否能从检索上下文中推断
- 计算被支持的声明占比

**Answer Relevance（答案相关性）**

定义：答案是否直接且恰当地回应了问题。该指标不考虑事实准确性，而是惩罚不完整或包含冗余信息的答案。

核心思想：如果答案正确回应了问题，那么从答案反向生成的问题应该与原问题高度相似。

### ▐  幻觉问题的深入分析

Faithfulness 指标的本质是检测幻觉。RAG 系统的幻觉可进一步细分为三类：

（原文此处内容未展开）

不同 RAG 应用场景（医疗、法律、通用 QA）对检测器的要求不同，需根据具体场景选择。

**幻觉检测方法**

（原文此处内容未展开）

### ▐  RAG 场景的特殊考量

传统 IR 指标基于语义相似度评估检索质量，但在 RAG 场景下存在一个核心问题：**语义相似 ≠ 对 LLM 有用**。

ICLERB（In-Context Learning Embedding and Reranker Benchmark）提出了端到端评估思路，这意味着：一个"好"的检索结果，不仅要语义相关，还要能有效支撑 LLM 生成正确答案。

```
检索候选文档 → 注入 LLM 生成答案 → 评估答案准确性 → 反推检索器效果
```

参考论文：https://arxiv.org/abs/2411.18947

---

## 三、构建知识库分为几步？

知识库的构建可以分为两个阶段：**离线索引阶段（Indexing）** 和 **在线查询阶段（Querying）**。本章节结合 idealab 平台（https://idealab.alibaba-inc.com/#/aistudio）的操作进行讲解。

离线索引阶段：Load → Split → Embed → Store
在线查询阶段：Query → Retrieve → Rerank → Generate

### ▐  离线索引阶段

**Step 1: Load（文档加载）**

这一步很好理解，就是将原始数据从各种来源和格式中提取出来。目前 idealab 提供的知识库支持的有 odps、语雀、钉钉文档、本地文件。

**Step 2: Split（文档切分）**

将长文档切分为适合检索和上下文注入的片段（chunks）。这是影响检索质量的关键环节。目前 idealab 提供的知识库支持的有默认智能切分（使用 Opensearch 切分方案），自定义切分（固定长度，符号切分），自定义工具切分。

关键参数：

- **chunk_size**：块大小，通常 256-1024 tokens
- **chunk_overlap**：重叠区域，通常 10%-20%，防止切断关键信息

**Step 3: Embed（向量化）**

使用 Embedding 模型将文本块转换为稠密向量。本环节 idealab 提供了多种模型可供选择。

**Step 4: Store（存储与索引）**

将向量及其元数据存入向量数据库，建立高效检索索引。

### ▐  在线查询阶段

**Step 5: Query（查询处理）**

对用户原始查询进行预处理和增强。这一步需要 Agent 的搭建者进行处理，最为简单的方式就是交给大模型自己来。充分信任基模的能力。以下是一些常见的手段：

（原文提及但未展开：HyDE 查询增强技术、Late Chunking、意图驱动切分）

**Step 6: Retrieve（向量检索）**

从向量数据库中召回与查询最相关的文档片段。

```
Query Embedding → ANN Search → Top-K Chunks
```

检索模式：

- **稠密检索**：基于向量相似度（余弦、内积）
- **稀疏检索**：基于词频统计（BM25）或学习权重（SPLADE）
- **混合检索**：稠密 + 稀疏，取长补短

同样的，idealab 支持多种配置项。

**Step 7: Rerank（重排序，可选）**

对初筛结果进行精排，解决初步召回不够准确的问题，尤其是混合召回后的排序。提升最终送入 LLM 的内容质量。

（原文提及 Cross-Encoder 重排序机制但未展开）

**Step 8: Generate（答案生成）**

将检索到的上下文与用户问题一起送入 LLM 生成最终答案。

### ▐  知识库的开源项目和案例

RAG 系统涉及众多模块（分块策略、Embedding 模型、检索方式、Reranker 等），不同模块组合在不同数据集上表现差异很大。手动调优耗时且难以找到最优解。

**案例一：AutoRAG - 自动化 RAG 模块优化框架**

核心方法：（原文未展开）

适用场景：

- 需要为特定领域数据集优化 RAG 配置
- 缺乏调优经验或资源
- 希望系统化比较不同方案

**案例二：QuIM-RAG - 问题倒排索引匹配**

（原文内容未展开）

**案例三：OpenViking - 文件系统范式**

（原文摘要提及但正文中未详细展开）

---

## 备注

1. 文章摘要提到 Late Chunking、HyDE、Cross-Encoder、AutoRAG、QuIM-RAG、OpenViking 等多个前沿架构,但部分内容在微信文章正文中未详细展开,只能看到标题与简要定位
2. 部分段落(尤其具体公式)在微信 HTML 抽取时被截断或样式异常,需后续通过原文 PDF/图片补充
3. 文章配套平台 idealab(https://idealab.alibaba-inc.com/#/aistudio)是阿里内网工具,外部访问受限
4. 这是阿里内部 idealab 团队对 RAG 知识库工程的系统性梳理,适合作为 RAG 评估与构建的入门到中阶参考