# BDD+ADR+PRD：让 Agent 遵守规范的闭环方法

## 基本信息

- **原文链接**：https://mp.weixin.qq.com/s/QT71-f3OZ067XhDwrbrAtQ
- **文章 mid**：2247486014
- **公众号 biz**：MzkyNDIxMzA2NQ==
- **发布时间**：2026-06-10 01:05:03 UTC
- **抓取时间**：2026-07-01
- **状态**：description 元数据完整；正文为图片/卡片形态，curl 静态抓取只能拿到摘要
- **一手来源**：Michal Cichra（Safe Intelligence）在 AI Engineer 大会的演讲
- **原演讲标题**：BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike
- **演讲者背景**：微软 / Red Hat 十年老兵

---

## 原文内容（description 元数据完整版）

> 🐒 科学家把五只猴子关笼子里，谁拿香蕉就用冷水浇所有猴子。逐只替换后，没有一只原始猴子了——但新猴子依然暴揍任何碰香蕉的同伴，没人知道为什么。
>
> 这就是 AI 写代码的现状：改了几轮之后，连它自己都不知道为什么这么写。
>
> 💡 微软/Red Hat 十年老兵 Michal Cichra 给出了四个文档武器
>
> 📋 **ADR（架构决策记录）**
> - 记录"为什么"做某个技术决定
> - 他的团队有 50+ 条 ADR 定义整个产品架构
> - 用 linter 强制执行，违规时自动指向文档
>
> 📝 **PRD（产品需求文档）**
> - 只记三件事：为什么存在、解决什么问题、用户怎么走
> - 不只给 Agent 看，更是给六周后的你自己
>
> 🧪 **BDD + Cucumber**
> - 用人类语言描述产品行为，同时可以执行验证
> - 比读 AI 代码更难的是读 AI 测试——BDD 解决了这个问题
> - 闭合了"spec 写了但没人验证"的循环
>
> 🔄 **闭环执行：Git Hook → CI → Linter**
> - Agent 提交代码 → 被拒绝 → 收到反馈和文档链接 → 自己修 → 再提交
> - 不是发现问题，而是让问题不可能发生
>
> ⚡ 单个 session 经历 20-50 次上下文压缩也没关系，重要的东西总会被保留
>
> 📎 【AI Engineer】BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence
>
> #AI编程 #ADR #BDD #PRD #架构规范 #AIAgent #代码质量 #Cucumber #设计系统 #工程效率

---

## 关联主题标签

 #主题/AI-Agent #主题/AI-Coding #场景/技术博客 #节点/Harness #节点/Context-Engineering #节点/Agent-Loop
