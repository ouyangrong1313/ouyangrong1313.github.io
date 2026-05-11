---
name: perplexity-agent-skills-design
description: Perplexity 内部规范：Agent Skill 设计迭代维护的 5 个步骤、4 类评测、3 条红线
type: reference
---

# Perplexity Agent Skills 设计规范

> 原文：[Designing, Refining, and Maintaining Agent Skills at Perplexity](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
> 作者：Perplexity Agents 团队
> 发布：2026 年 5 月 9 日

## 核心范式转变：Skill ≠ 代码

| Python 信条 | Skill 反信条 |
|------------|-------------|
| Simple is better than complex | Skill 是文件夹，复杂性是特性 |
| Explicit is better than implicit | 激活靠隐式模式匹配 + 渐进披露 |
| Sparse is better than dense | 每 token 都要榨出最大信号 |
| 特例不应破坏规则 | Gotchas（坑）才是最高价值内容 |
| 容易解释的实现是好实现 | 容易解释的，模型已经会了 → 删掉 |

## Skill 四重定义

### 1. Skill 是目录（不是单文件）
标准结构：`SKILL.md` + `scripts/` + `references/` + `assets/` + `config.json`

复杂领域用多级层次。如美国税法有 1945 个 IRC 条款，分三级嵌套后才可用。

### 2. Skill 是格式
frontmatter 必须有：
- `name`（小写、连字符、与目录同名）
- `description`（**路由触发器**，不是文档）

常见错误：写 "This Skill does X"
正确写法：`Load when …`

### 3. Skill 是可调用的
```
load_skill()
  → 拷贝目录入沙箱
  → 递归装载 depends: 中的依赖
  → 剥离 frontmatter，仅暴露 body 与附属文件
```

### 4. Skill 是渐进式的（成本模型）
| 层级 | 内容 | 预算 | 何时付费 |
|------|------|------|----------|
| Index | 所有 Skill 的 name+description | ~100 tokens/Skill | 每次会话、每个用户、永远 |
| Load | SKILL.md body | ~5,000 tokens | 一次加载，会话内持续占用 |
| Runtime | scripts / references / 子 Skill | 无上界 | 仅模型实际读取时 |

越靠上的层，每个字越贵。Index 是「奢侈品柜台」，Runtime 是「无限仓库」。

## 构建五步法（顺序不可调）

### Step 0 — 先写 Evals
来源：真实查询、已知失败、邻域混淆。**负例比正例更重要**。

### Step 1 — 写 Description（最难的一行）
- 以 `Load when…` 开头
- ≤ 50 词
- 描述用户意图（用真实抱怨语："babysit"、"watch CI"、"make sure this lands"）
- 不要总结工作流
- 唯一目标：路由准确

### Step 2 — 写 Body
- 跳过显然的
- 不要罗列命令序列
- **用意图陈述代替过程脚本**

❌ `git log; git checkout main; git checkout -b; git cherry-pick`
✅ "Cherry-pick 到干净分支，保留意图解决冲突，落不下时说明原因。"

重点放 **gotchas / 负例**。

### Step 3 — 用层次结构
- `scripts/` — 确定性逻辑
- `references/` — 条件加载的重文档
- `assets/` — 输出模板
- `config.json` — 首次运行配置

### Step 4 — 迭代
用一个评测集做小词级调优（描述里一字之差就能引发路由级联）。

### Step 5 — Ship

## 维护：Gotchas 飞轮

Skill 是**仅追加为主**的：
- Agent 错了 → 加 gotcha
- 误加载 → 收紧描述 + 加负例
- 该加载没加载 → 加关键词 + 加正例
- system prompt 变了 → 检查冲突与重复

从 80/20 走向 99.9% 的过程，几乎全靠 gotcha 列表生长，而不是改描述或加更长的指令。一旦 PR 改描述却没附 evals，"已经走偏了"。

## 评测套件分四类

1. **加载评测**：精度、召回、禁止加载（避免污染邻域）
2. **渐进加载评测**：Skill 加载后是否正确读取附属文件
3. **端到端任务评测**：跑完整 agent loop，用 LLM judge 按 rubric 打分
4. **跨模型评测**：在 GPT / Opus / Sonnet 上同时跑

## 三条「最反直觉」要点

1. **上下文是稀缺资源**，不是代码空间。Skill 设计本质是上下文经济学。
2. **路由 ≠ 文档**。description 实际是个隐式的分类器输入。
3. **不要规定路径，规定意图**。模型在面对"目标 + 约束"时比面对"步骤清单"表现更好。

## 什么时候不需要 Skill

"Every Skill is a tax." 三类典型滥用：
- 模型已会的（写一串 git 命令 → 是好文档，是坏 Skill）
- 重复 system prompt 的
- 变化太快的（远端 MCP 工具版本频繁变）

判断单句是否该留的尺子：**"没有这句话，Agent 会做错吗？"** 答否即删。

---

标签：#主题/AI Agent · #主题/Skill设计 · #场景/技术博客
原文：https://mp.weixin.qq.com/s/vXOpiUiAK-fG6GUgi2sD-A
