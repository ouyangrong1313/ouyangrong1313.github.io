---
title: 未来属于垂直领域 Agent - 原文摘要
类型: raw digest(原文结构化提炼,非 wiki 编译)
源文件: 2026-07-LaterCast-Justin-未来属于垂直领域Agent.md
---

## 一句话总结

未来的企业 Agent 不会沿着"一个大模型吃下所有工具"的路线长大,而会拆成一组更小、更专、更容易控制的 **domain-specific agents**——composition over inheritance。

## 核心观点(5 条)

1. **集成先卡 / 模型智商排后**——能跑 demo 的 Agent 离生产环境还差很远(Agentic loop / provider abstractions / durable execution / validations / stop conditions)。
2. **工具堆叠的反噬**——5 个 skills 还能忍,50+ / 100+ / 1000+ 以后,延迟、费用、误调用、权限风险会一起上涨;已有研究证明 skills 装太多会让 Agent 明显变差。
3. **Composition over inheritance**——拆出 Figma Agent / Gmail Agent / Travel Agent,每个小 Agent 都有自己的 system prompt / 工具 / 消息历史 / agentic loop;上面放一个 coordinator 分派任务。
4. **小 Agent ≠ 只暴露工具的服务器**——它是完整 Agent,有自己的消息历史和循环(影响产品设计:主 Agent 只需"说目标 + 接结果")。
5. **2027 = 多 Agent 编排之年**——Vercel Eve 等框架出现 company brain / personal assistant / domain-specific agent 词汇,2026 H2 framework 多,2027 orchestration 主流化。

## 关键参数 / 数字

- **80%+ token efficiency**:定义好任务边界后,单个任务经常能看到超过 80% 的 token 效率提升
- **2026 token 价格反转**:
  - 按 IQ 调整后,token 2026 年**上涨 29%**
  - 不按 IQ 调整,涨幅达 **76%**
- **小模型成本差**:DeepSeek V4 Flash vs Fable 5,前者单任务便宜 **137 倍**
- **递归 Agent 案例**:销售团队 coordinator → Salesforce / Google Workspace / 素材生成 / 法务 → GDPR / OSHA(4 层递归)
- **典型工具堆叠**:Figma + Playwright + Gmail + Sheets + 差旅 + 报销 + React lint + GitHub skill = 8+ 类工具进同一上下文

## 5 段核心论证(主张 + 案例)

| # | 主张 | 案例 |
|---|---|---|
| 1 | 集成是生产环境第一关,不是模型智商 | 房地产中介 / 私人保险经纪 / Fortune 500 自建 Agent 都卡在 durable execution + 验证 + 停止条件 |
| 2 | 工具堆叠导致 context 膨胀 + 权限风险 | 安排洛杉矶行程的 Agent 背着 8 类工具的说明 + 整段对话历史 |
| 3 | composition over inheritance | NASA 阿波罗登月:一组专家各掌握有限工具 + 消息协同,而非一个人背所有工具 |
| 4 | 小而专,80% token 效率 | Gmail Agent 查 "Debbie 最近那封邮件" 不需要 Figma / 报销 / 代码工具说明 |
| 5 | 2027 多 Agent 编排主流化 | Vercel Eve 官网出现 company brain / personal assistant / domain-specific agent 词汇 |

## 4 大原语(企业 Agent 必备)

1. **文件系统**——每个 Agent 有自己的小文件区(类比 ChatGPT/Claude/Codex 做 PDF 时的小文件区)
2. **沙盒执行**——隔离的代码执行环境
3. **hooks**——注入时间、触发副作用(如"模型不知道当前时间,用 hook 注入一条人工消息")
4. **rules**——限制回合数、验证要求、停止条件(企业 Agent 生产稳定性往往被这些小开关决定)

## 核心金句(5 条)

- "**2027 年,基本上会是多 Agent 编排之年。**"
- "**Token 已经不再变便宜了。**"
- "**Agent 是确定性软件,它把模型产生的非确定性结果,用在某个目标上。**"
- "**我们不是靠给一个人一堆工具,把送上月球的。**"
- "**组合是继承的替代方案。**"

## 关联图谱

### 上游(基于 / 来自)
- 软件工程老原则:composition over inheritance
- NASA 阿波罗登月组织模式:专家 + 消息协同
- Vercel AI SDK / Eve 框架

### 下游(应用于 / 验证于)
- 2026 H2 围绕 domain-specific agents 的框架 / 讨论 / 产品爆发
- 2027 多 Agent 编排成为主流话题
- 销售团队递归 Agent 案例(coordinator → 4 个子 Agent → 法务下再拆 GDPR/OSHA)

### 同级(横向 / 并列)
- Anthropic Claude Code 团队的小步快跑
- Multica "4 人 + 几十 Agent" 极端样本
- 阿里"业务需求专家 Agent 4 层 8 步"

## 备注与限制

- 演讲者 Justin Schroeder 是 StandardAgents CEO,工具栈偏早期生态,具体业务实践数据(80% token efficiency)来自其公司内部
- 137 倍价格差是 DeepSeek V4 Flash vs Fable 5 单任务对比,需考虑任务复杂度差异
- "2027 = 多 Agent 编排之年"是演讲者判断,非第三方数据
- 文中"Vercel AI SDK"和"Eve"的具体技术栈未展开
- 微信公众号为「晚点再听LaterCast」编译,不是原创,实际作者是 Justin Schroeder
