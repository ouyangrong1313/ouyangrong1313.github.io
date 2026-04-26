# Deep Research Stack：开源深度研究方案

## 核心结论

**用三个开源工具（Onyx + CrewAI + Voxtral）搭建深度研究系统，可在基准测试上打败 OpenAI/Gemini/Perplexity。**

关键：阶段分离 + 推理检索 + 循环反思

---

## 技术栈

| 组件 | 工具 | 作用 |
|------|------|------|
| 检索层 | **Onyx** | RAG、Web 搜索、多 Agent 研究 |
| 编排层 | **CrewAI** | Flow/ Skills/ MCP 集成 |
| 语音层 | **Voxtral** | 语音输入 + 报告叙述 |

---

## Onyx 三阶段架构

```
Clarification → Planning → Iterative Execution
```

### Phase 1: Clarification
- 最多 5 个针对性问题
- 短或模糊查询才触发

### Phase 2: Planning
- 最多 6 个探索方向
- **关键**：Planner 无工具权限，只出计划

### Phase 3: Iterative Execution
- 最多 8 轮迭代
- 每轮并行 3 个 Agent

### 两个关键分离
- Orchestrator 从不直接搜索
- Research Agent 从不看完整查询/计划

---

## 6步检索管道

| 步骤 | 内容 |
|------|------|
| 1 | Query generation — 并行多路查询 |
| 2 | Search recombination — 混合索引 + RRF |
| 3 | LLM selection — LLM 过滤相关块 ⭐ |
| 4 | Context expansion — 读周围块定上下文 |
| 5 | Prompt building — 组装 + 引用 |
| 6 | Answer synthesis — grounded 答案 |

---

## CrewAI 编排

### 三个原语
- **Flows** — 独立 Crews 接力
- **Skills** — SKILL.md 行动点注入
- **MCP Integration** — 直接附加 MCP 服务器

### 三 mini-crews，不是 one crew

一个 Crew 三顺序任务 = **deep frying**（上下文污染）：
- 事实被反复解读
- 矛盾被平滑
- 源材料面目全非

正确做法：三个独立 Crews，每棒只传干净输出。

---

## 为什么 Self-Hosting 重要

| 闭源问题 | 自托管优势 |
|----------|------------|
| 查询在别人服务器 | 数据不离开基础设施 |
| 内部数据被索引 | 索引在自己网络 |
| 保留/审计由他们定 | 你决定一切 |
| 配额/价格随时变 | 完全可控 |

---

## 标签

#主题/AIAgent #场景/技术博客

## 相关链接

- [[index]]
- [[agent-architectures]]
- [[harness-engineering]]
