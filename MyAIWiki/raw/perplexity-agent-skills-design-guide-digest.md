---
name: perplexity-agent-skills-design-digest
description: Perplexity Agent Skills 设计规范拆解
type: reference
---

# Perplexity Agent Skills 设计规范拆解

## 核心观点（5 个）

1. **Skill ≠ 代码**：不是写代码，是为模型构建上下文。工程师写代码的本能直接套到 Skill 上，几乎一定会失败。

2. **Description 是路由触发器，不是文档**：以 `Load when…` 开头 ≤50 词，描述用户意图而非工作流。

3. **Gotchas 才是最高价值内容**：Skill 的价值不在于告诉模型"怎么做"，而在于告诉模型"别踩哪些坑"。

4. **越靠上的层越贵**：Index ~100 tokens/Skill（永远付），Load ~5,000 tokens（会话内持续占用），Runtime 无上界（仅实际读取时付费）。

5. **先写 Evals，后写 Skill**：负例与正例同等重要，甚至更重要。

## 7 个分析角度

### 1. 范式差异（Python vs Skill）
| Python | Skill |
|--------|-------|
| Simple > complex | 复杂性是特性 |
| Explicit > implicit | 隐式模式匹配 |
| Sparse > dense | 每 token 榨出最大信号 |
| 规则优先 | Gotchas 优先 |
| 好实现 = 好解释 | 好解释 = 模型已会 = 删掉 |

### 2. 四重定义
- 目录（多级层次结构）
- 格式（frontmatter 规范）
- 可调用（加载流程）
- 渐进式（成本分层）

### 3. 五步构建法
```
Step 0: 先写 Evals（最重要！）
Step 1: 写 Description（Load when...）
Step 2: 写 Body（意图陈述，非命令序列）
Step 3: 用层次结构（scripts/references/assets/config）
Step 4: 迭代（小词级调优）
Step 5: Ship
```

### 4. Gotchas 飞轮
- Agent 错了 → 加 gotcha
- 误加载 → 收紧描述 + 加负例
- 该加载没加载 → 加正例
- system prompt 变了 → 检查冲突

### 5. 四类评测
- 加载评测（精度/召回/禁止）
- 渐进加载评测（读取附属文件）
- 端到端任务评测（LLM judge）
- 跨模型评测（多模型同时跑）

### 6. 三条红线
1. 模型已会的别写
2. system prompt 重复的别写
3. 变化太快的别写

### 7. 判断标准
**"没有这句话，Agent 会做错吗？"** 答否即删。

---

## 14 个开头钩子

1. "写 Skill 不是写代码，是为模型构建上下文"
2. "Description 写 README 是最常见的错误——它其实是路由触发器"
3. "Gotchas 才是最高价值内容，不是命令序列"
4. "Index 层是最贵的奢侈品柜台，每 token 都在和其他 Skill 抢预算"
5. "先写 Evals 是反直觉但回报最高的步骤"
6. "从 80/20 到 99.9%，全靠 gotcha 列表生长"
7. "不要规定路径，规定意图——模型在异常路径上表现更好"
8. "Skill 是仅追加为主的，不是每次都重写"
9. "PR 改描述却没附 evals，说明已经走偏了"
10. "Every Skill is a tax"
11. "Load when… 这个开头格式不是随便写的，是路由触发的语法"
12. "层次结构有代价，需要导航工具来对冲间接性"
13. "Action at a distance：新 Skill 会悄无声息降级现有 Skill"
14. "写 Skill 的能力本身在复利增长"

---

标签：#主题/AI Agent · #主题/Skill设计 · #场景/知识付费
原文：https://mp.weixin.qq.com/s/vXOpiUiAK-fG6GUgi2sD-A
