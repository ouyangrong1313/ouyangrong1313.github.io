# Matt Pocock Claude Code Skills

## 核心结论

Matt Pocock 开源了一套 22 个 Claude Code Skill，覆盖计划→编码→review→知识管理的完整工作流，一周 30k star。

**关键洞察**：Skill 有态度才有用 — 好用不是因为通用，是因为它带着强烈的个人工作偏好（信 TDD、反对水平切片、信设计前多画几版）。装上之后，相当于把一个 TypeScript 大佬的工作习惯装进了你的 Claude Code。

---

## 与 Addy Osmani agent-skills 的区别

| 路线 | 代表 | 思路 |
|------|------|------|
| "教你干活" | Addy Osmani | 工程纪律系统，教 AI"该做什么不该做什么" |
| "帮你干活" | Matt Pocock | 直接执行，不教规矩 |

两套可以叠加：agent-skills 管"怎么做"，这套帮"做什么"。

---

## Skill 分类

### 计划类
- `to-prd` — 当前对话直接生成 PRD 并提交 GitHub issue
- `to-issues` — 把计划拆成独立可认领的 GitHub issue
- `grill-me` — AI 反复质问每个设计决策，直到每个分支都想清楚
- `design-an-interface` — Design It Twice，并行多 Agent 从不同约束出发设计后对比

### 编码类
- `tdd` — 红绿重构循环，**反对水平切片**（"先写所有测试再写所有代码是 crap tests"）
- `triage-issue` — bug 报告进来，深度探索代码库找根因，生成修复计划
- `git-guardrails-claude-code` — 拦截 `push --force`、`reset --hard`、`clean` 等危险命令

### 写作和知识类
- `edit-article` — 改文章
- `obsidian-vault` — 管理 Obsidian 笔记

### 元 Skill
- `write-a-skill` — 教你怎么写 Skill

---

## 关键设计理念

### grill-me 的核心原则
> "如果某个问题可以通过探索代码库得到答案，那就去探索代码库，不要问我。"

→ 直接解决 AI 动不动就问用户的毛病

### tdd 的 tracer bullet 模式
正确做法：测试 → 实现 → 测试 → 实现，每次只走一小步，但每步都是端到端的完整切片。

### git-guardrails 的设计
拦截危险命令时，Claude 收到"你没有权限执行这个命令"，连确认机会都不给。

### design-an-interface
并行启动 3 个以上子 Agent，每个接不同约束（如"最多 3 个方法"、"最大化灵活性"），生成多版设计后对比挑最好或组合。

---

## 安装
```bash
npx skills@latest add mattpocock/skills/tdd
npx skills@latest add mattpocock/skills/grill-me
npx skills@latest add mattpocock/skills/triage-issue
```

Skill 装进 `.claude/skills/` 后根据关键词自动激活。

---

## 标签
#主题/AI Coding #主题/Claude Code #场景/知识付费 #场景/技术博客

## 相关链接
- GitHub：https://github.com/mattpocock/skills
- 原文：https://mp.weixin.qq.com/s/35B5cAQ9kA0LGAbFXrxCuQ