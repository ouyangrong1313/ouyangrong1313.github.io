# 原文摘要 - Task Decomposition（任务拆解）

## 一句话总结

**Task Decomposition 是 Agentic Workflow 最底层核心**——**90% 的问题不是模型不够聪明，是不会拆**；四步方法论：① 标准化（参数化 + Must/Should/May + Markdown）② 拆解（Pipeline + JSON 数据契约）③ 双向开发（小步快跑）④ MCP 整合（AI 世界的 Type-C）+ Human-in-the-loop Checkpoint。

## 核心观点（6 条）

1. **90% 的真相**：LLM 底层能力已足够强，**90% 的失败不是模型不够聪明，是不会把大任务拆成 AI 真正能跑得动的小 Task**
2. **三层世界观**：
   - **Human SOP**（写给人类看，含默会知识 Tacit Knowledge）
   - **Skill**（单点任务执行单元，打包成文件夹交给 Agent）
   - **Agentic Workflow**（串联多个 Agents/Tools/Skills/数据源的全自动生产线）
3. **Mega Agent 死路**：AGI 来了也不行——AI 没有读心术；黑箱 = 不可预测 + 不可观测 + 不可修复；大公司绝不敢让黑箱上 Production
4. **Divide and Conquer 老派工程智慧**：4 个小 Agent 各干一件边界明确的小事；哪里坏了改哪里，对症下药
5. **四步方法论**：标准化 / 拆解与连接 / 双向开发 / MCP 整合——核心是"小步快跑 + 严格数据契约 + AI 世界的 Type-C 接口"
6. **高风险节点必须 Human-in-the-loop Checkpoint**（如财务支出超 5000 元 / 权限变更 / 设备解绑 / 远程开门）

## 关键事实 / 案例

| 关键事实 | 内容 |
|---|---|
| 公众号定位 | RPA / AI 教程类 |
| 作者 | Leeka（影刀 RPA 高级工程师 + 生财有术航海教练） |
| 三层世界观 | Human SOP / Skill / Agentic Workflow |
| 工具栈 | Claude / ChatGPT / Cursor + MCP（Model Context Protocol） |
| 实战案例 | 200 人公司"内部请求分拣系统"——工单自动归类 + 自动回信 |
| 正确率提升 | 20 次测试 + 3 轮迭代 → 98%+ 正确率 |
| 高风险阈值 | 金额超 5000 元自动挂起等人工 Approve |
| Skill 命名 | internal-request-triage / weekly-report-drafting / invoice-categorization |
| 法则引入 | Must / Should / May（RFC 2119 网络协议高阶写法） |
| MCP 比喻 | AI 世界里的 Type-C 接口 |

## 决策树 / 反直觉

- **如果你想把整个开发流程塞给一个 AI** → 你在做 Mega Agent = 黑箱；按 Divide and Conquer 拆
- **如果你想等 AGI 来了不拆流程** → 错了；AI 没有读心术；AGI 来了也必须明确边界
- **如果你想写一份完美 SOP 一次性丢给 AI** → 错了；必须"小步快跑"——首发粗糙 + 踩坑 + 补 Must 规则 + 下一轮迭代
- **如果你的 AI 工作流是"一锅粥"** → 错；按 Pipeline Steps + 严格 JSON 数据契约分节点
- **如果你想完全无人化（高风险节点）** → 错；高风险节点必须 Human-in-the-loop Checkpoint
- **如果你的 SOP 是写给人看的散文** → 错；按 Must/Should/May + Markdown 重写

## 核心金句（5 条）

1. "90% 的原因不是模型不够聪明，而是你根本不知道怎么把一个巨大的、模糊的任务，拆成 AI 真正能跑得动的小 Task。"
2. "高超的任务拆解能力是构建稳定、可观测、生产就绪（Production-ready）系统的唯一地基。"
3. "大公司绝对不敢让这种黑箱系统上 Production，因为他们无法容忍这种不可预测的崩溃。"
4. "速度的本质，不是首发多完美，而是迭代有多快。"
5. "MCP 就是 AI 世界里的 Type-C 接口。"

## 关联图谱

### 上游（基于 / 来自）
- 斯坦福 AI 系统构建教学影片（2026）
- Leeka 个人 AI 落地咨询案例
- RFC 2119 网络协议规范

### 下游（应用于 / 验证于）
- Seetong AI 助手：如何拆成多个边界明确的小 Skill（避免 Mega Agent）
- Seetong 客服 SOP 翻译：Human SOP → Skill + Agentic Workflow
- Seetong 高风险节点：设备添加/远程开门/解绑/支付 → Human-in-the-loop Checkpoint

### 同级（横向 / 并列）
- **[[0xCodez-Agent-Harness-14-Steps]]** - Agent Harness 14 步法
- **[[Addy-Osmani-Loop-Engineering]]** - Loop Engineering 验证才是瓶颈
- **[[阿里妹-端到端业务需求专家Agent]]** - 4 层架构 8 步流程
- **[[阿里云开发者-淘宝主播Agent的Harness工程实战]]** - 阿里淘宝 Agent 工程实战
- **[[清华沈阳-自进化AI新物种]]** - 自进化 AI 新物种
- **[[Multica-AI-Native-组织-人是最慢的节点]]** - Multica AI Native 组织
- **[[Harness不是目的-知识才是护城河]]** - Harness vs 知识护城河

## 备注与限制

- 本文是 RPA/AI 教程类公众号推送，核心是 Agent 落地的"任务拆解"方法论
- 与 [[Addy-Osmani-Loop-Engineering]] 区别：Addy 关注"Loop 验证"，本文关注"任务拆解"——一个是"测"，一个是"拆"，互补
- 与 [[0xCodez-Agent-Harness-14-Steps]] 区别：0xCodez 是 14 步 Harness 工程框架，本文是 4 步 SOP 翻译方法
- 与 [[阿里妹-端到端业务需求专家Agent]] 区别：阿里妹是 4 层架构 8 步流程（业务端），本文是 4 步翻译法（Human SOP → Agentic Workflow）
- **核心反直觉**：AGI 来了也必须拆——"这跟帮手够不够聪明没有半毛钱关系"
- **未展开**：MCP 协议的具体技术细节（Leeka 假设读者已了解）；Skill 文件夹的具体结构