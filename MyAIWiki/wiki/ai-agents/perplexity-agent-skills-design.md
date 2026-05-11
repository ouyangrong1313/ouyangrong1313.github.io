---
name: perplexity-agent-skills-design
description: Perplexity Agent Skills 设计规范
---

# Perplexity Agent Skills 设计规范

> 原文：[Designing, Refining, and Maintaining Agent Skills at Perplexity](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)

## 核心范式

**Skill ≠ 代码**。写 Skill 不是写代码，是为模型构建上下文。

| Python 信条 | Skill 反信条 |
|------------|-------------|
| Simple > complex | 复杂性是特性 |
| Explicit > implicit | 隐式模式匹配 |
| 每 token 都要榨出最大信号 | Gotchas 才是最高价值 |

## 四步构建法

1. **Step 0** — 先写 Evals（最重要！）
2. **Step 1** — 写 Description（`Load when...` ≤50 词）
3. **Step 2** — 写 Body（意图陈述，非命令序列）
4. **Step 3** — 用层次结构（scripts/references/assets/config）

## 成本模型

| 层级 | 预算 | 何时付费 |
|------|------|----------|
| Index | ~100 tokens | 每次会话、永远 |
| Load | ~5,000 tokens | 会话内持续占用 |
| Runtime | 无上界 | 仅实际读取时 |

## 维护：Gotchas 飞轮

- Agent 错了 → 加 gotcha
- 误加载 → 收紧描述 + 加负例
- 该加载没加载 → 加正例

## 判断标准

**"没有这句话，Agent 会做错吗？"** 答否即删。

---

标签：#主题/AI Agent · #主题/Skill设计
原文：https://mp.weixin.qq.com/s/vXOpiUiAK-fG6GUgi2sD-A
