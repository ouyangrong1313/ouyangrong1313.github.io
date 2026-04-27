# 谷歌开源 Agent Skills — 拆解

## 核心观点

1. **AI 编程工具越强，走捷径的毛病越明显** — 不考虑长期稳定性和迭代维护
2. **Agent Skills = 谷歌资深工程师的工作规范封装** — 20 个 Skill + 7 个 Slash 命令 + 3 个 Agent 人设
3. **覆盖软件开发生命周期六阶段** — 定义→规划→构建→验证→评审→发布
4. **三工具对比** — Spec Kit（文档定AI）、Superpowers（流程带AI）、Agent Skills（纪律管AI）
5. **Agent Skills 意义** — 不是让 AI 更聪明，而是让 AI 有规可循

## 7 个分析角度

### 角度1：问题诊断 — AI 编程的捷径病
AI 模型强了但更会走捷径，不顾项目长期稳定性和维护成本。

### 角度2：解决方案架构 — Agent Skills 设计思路
把《Software Engineering at Google》的方法论封装成 20 个可组合的 Skill。

### 角度3：开发流程 — Slash 命令串联全链路
`/spec` → `/plan` → `/build` → `/test` → `/review` → `/ship` 完整流程。

### 角度4：质量保障 — 三大人设并行评审
code-reviewer、test-engineer、security-auditor 并行出具报告。

### 角度5：竞品对比 — 三种 AI 编程规范流派
文档驱动 vs 流程驱动 vs 纪律驱动。

### 角度6：工具选择 — 主流 AI 编程工具全覆盖
Claude Code、Cursor、Gemini CLI、Windsurf、GitHub Copilot、Codex。

### 角度7：行业洞察 — AI 编程工具的信任危机
模型能力增强但代码交付信任度未建立，稳定迭代 > 快速生成。

## 21 个开头钩子

### 角度1：问题诊断
1. "你有没有发现，AI 越强，越容易走捷径？"
2. "模型能写代码了，但为什么项目还是维护不下去？"
3. "AI 编程工具进化飞快，但有个毛病始终治不好……"
4. "初级和资深工程师的差距，AI 居然在复制……"

### 角度2：解决方案架构
5. "谷歌把 20 年工程经验塞进了一个 Skill 包里。"
6. "别让 AI 乱来，给它立规矩。"
7. "这个开源项目，把 Google 内部的开发规范公开了。"

### 角度3：开发流程
8. "一个命令搞定需求梳理，一个命令搞定代码评审。"
9. "`/spec` → `/ship`，六步走完整个开发流程。"
10. "Claude Code 新玩法：Slash 命令串联 AI 编程全链路。"

### 角度4：质量保障
11. "上线前，AI 会自动出具三份报告：代码、测试、安全。"
12. "部署前检查从未如此自动化——三个 Agent 并行开工。"
13. "让 AI 写代码不难，难的是让 AI 按工程标准写代码。"

### 角度5：竞品对比
14. "Spec Kit、Superpowers、Agent Skills 有什么区别？"
15. "三种 AI 编程规范流派，看完就知道选哪个。"
16. "文档定 AI、流程带 AI、纪律管 AI——你选哪派？"

### 角度6：工具选择
17. "两行命令，在 Claude Code 里装上谷歌同款开发规范。"
18. "Cursor 用户也能用——把 SKILL.md 复制到 rules 目录即可。"
19. "主流 AI 编程工具全覆盖，GitHub Star 23000+ 的项目了解下。"

### 角度7：行业洞察
20. "模型越来越强，但为什么我们还在担心 AI 写的代码能不能上线？"
21. "23000+ Stars 说明什么？大家对 AI 代码交付心里还是没底。"

## 标签

#主题/AI-Coding
#手法/权威背书
#场景/技术博客

## 相关链接

- 原文：https://mp.weixin.qq.com/s/DiRKOSV7BPkWaGUxPnLqyQ
- GitHub：https://github.com/addyosmani/agent-skills
