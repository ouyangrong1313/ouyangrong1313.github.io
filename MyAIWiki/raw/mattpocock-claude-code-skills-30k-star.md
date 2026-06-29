# Matt Pocock Claude Code Skills — 30k Star的工作流革命

## 原文信息
- **标题**：Github 30k star，TypeScript 大神把他 .claude 目录整套搬出来了！
- **来源**：微信公众号 — 彭涛主创团队 彭少
- **链接**：https://mp.weixin.qq.com/s/35B5cAQ9kA0LGAbFXrxCuQ
- **日期**：2026-05-03

---

## 核心观点

### 1. 问题诊断
- Claude Code 每次都要重新对一遍接口设计、测试、bug triage，效率上不去
- AI 写得太"自由"：测试批量生成跟业务脱节、PRD没人整理、git push force直接把main送走
- 根因：**把同一套工作流每天口头重复**

### 2. Matt Pocock 的解法
- 把每天用的 Claude Code Skill 全部开源
- 22 个 Skill，从计划设计到写代码到 code review 到知识管理
- 一周 1 万颗星

### 3. 两种路线的区别
| 路线 | 代表 | 思路 |
|------|------|------|
| "教你干活" | Addy Osmani agent-skills | 工程纪律系统，教AI"该做什么不该做什么" |
| "帮你干活" | Matt Pocock skills | 直接替AI执行，不教规矩 |

### 4. 22个Skill分类

**计划类**（把思路变成可执行的东西）
- `to-prd` — 当前对话变PRD并提交GitHub issue
- `to-issues` — 把计划拆成独立可认领的GitHub issue
- `grill-me` — 被AI反复质问每个设计决策
- `design-an-interface` — Design It Twice原则，并行多Agent设计后对比
- `request-refactor-plan` — 通过用户访谈生成详细重构计划

**编码类**（真的写代码）
- `tdd` — 红绿重构循环，反对水平切片（先写所有测试再写所有代码）
- `triage-issue` — 收到bug报告后深度探索代码库找根因
- `improve-codebase-architecture` — 基于领域语言找重构机会
- `setup-pre-commit` — 一键配Husky pre-commit hook
- `git-guardrails-claude-code` — 拦截危险git命令

**写作和知识类**
- `edit-article` — 改文章
- `ubiquitous-language` — 提取DDD风格术语表
- `obsidian-vault` — 搜索创建管理Obsidian笔记

**元Skill**
- `write-a-skill` — 教你怎么写Skill

### 5. 关键设计理念

**grill-me**
> "如果某个问题可以通过探索代码库得到答案，那就去探索代码库，不要问我。"

→ 直接解决AI动不动就问用户的毛病

**tdd 反对水平切片**
> 批量写出来的测试测的是你想象中的行为，不是实际行为，最终测的是数据结构和函数签名的形状，而不是用户能感知到的行为。

→ 正确做法：tracer bullet模式（一个测试 → 一个实现 → 一个测试 → 一个实现）

**git-guardrails-claude-code**
- 拦截 `git push`、`reset --hard`、`clean`、`branch -D` 等危险命令
- Claude 收到"你没有权限执行这个命令"，连确认机会都不给

**design-an-interface**
- 并行启动3个以上子Agent，每个接不同约束
- Agent 1 "最多3个方法"、Agent 2 "最大化灵活性"、Agent 3 "为最常见情况优化"
- 生成3版完全不同的接口设计，对比后挑最好或组合

### 6. 安装方式
```bash
npx skills@latest add mattpocock/skills/tdd
npx skills@latest add mattpocock/skills/grill-me
npx skills@latest add mattpocock/skills/triage-issue
```

---

## 技术要点提炼

### Skill自动激活机制
- Skill装进 `.claude/skills/` 后根据关键词自动激活
- 说"帮我 triage 这个 bug"，对应Skill接管

### 与现有Skills叠加
- 装了 Addy Osmani agent-skills？可以叠加
- agent-skills 管"怎么做"，这套帮"做什么"

### 核心洞察
> 好用不是因为它通用，反而是因为它有态度。装上之后，相当于把一个TypeScript大佬的工作习惯装进了你的Claude Code。

---

## 标签
标签：#主题/AI Coding #主题/Claude Code #场景/技术博客 #手法/权威背书 #手法/教程型
相关链接：https://github.com/mattpocock/skills