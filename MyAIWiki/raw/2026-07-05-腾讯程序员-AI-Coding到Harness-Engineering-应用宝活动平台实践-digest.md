---
title: 从 AI Coding 到 Harness Engineering 应用宝活动平台端到端实践(原文摘要)
slug: 腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践-digest
source: 微信公众号 / 腾讯程序员
原始作者: zimingxing、kinglongli、yifhao(腾讯应用宝活动平台团队)
url: https://mp.weixin.qq.com/s/UE-RZH9hnbBd06CVapFGrA
pub_date: 2026-07-05
fetch_date: 2026-07-05
类型: 原文摘要
---

# 从 AI Coding 到 Harness Engineering 应用宝活动平台端到端实践(原文摘要)

## 一句话总结
**对话式 AI Coding 在 4 个痛点(上下文膨胀 / 业务知识缺 / 缺自动化闭环 / 单窗口无法并行)面前失效——Harness 化的本质不是给 AI 加规则,而是把"一个对话窗口"升级为"一套工程系统":知识库(底座)+ 状态文件驱动 + 12 个专家 Agent + DAG 并行编排 + 15 个流程脚本 + DevOps 多平台集成。**

## 5 条核心观点

1. **对话式 AI Coding 的 4 个死穴**:① 单窗口上下文随项目迭代快速膨胀,出现有损压缩遗忘与不按规则生成;② 缺乏完整业务知识,每次需求都要人先捋清楚多服务多业务的串联;③ 缺乏工程上的自动化闭环,只能加速 coding 环节,需求拆解/部署/验证/测试仍靠人;④ 单窗口无法并行,多独立任务要么串行要么开多窗口人来回切换。**任务越完整、越规模化、越可抽象成稳定流程,Harness 工程价值越高**。

2. **整体架构 = 知识库工程 ✖️ 端到端开发工程**:知识库工程负责沉淀散落在代码/文档/可观测系统中的工程知识,提供给上层消费;端到端开发工程以"状态文件"为驱动,实现需求拆解→澄清→任务拆解→并行开发→单测→CR→部署→请求构造→接口验证→提交的全流程 AI 执行。**当前规模**:800+ 结构化文档 / 90+ 微服务 / 12 专家 Agent / 30+ 业务 Skill / 10+ 流程脚本。

3. **状态文件驱动 = 端到端流程脱离对话窗口**:两类结构化 JSON——`product-state.json`(多 Story 并行,记录 breakdown / forking / joining)+ `e2e-state.json`(单 Story 端到端,记录 Phase 0~7 / 产出 / 接口验证结果)。配套 3 个 hook(Stop / SessionStart / SessionEnd)防止主调度器偷懒式提前停止。**解决 3 件事**:上下文有损压缩 / 流程中断无法恢复 / 推进缺乏可观测。

4. **专家 Agent 体系 + DAG 并行 + Fork-Join**:12 个专家 Agent 5 项设计原则(单一职责 / 上下文隔离 / 工具最小权限 / 确定性输入输出 / 模型可插拔)。两层并行——第一层 task-planner 按接口/模块拆任务构建 DAG 拓扑,同层任务并发配独立 git worktree;第二层多 Story 场景 Fork-Join(Phase R 产品拆解 → Fork 段 4 阶段并行 → Join 段 4 阶段串行收口)。**冲突治理 4 类**(Merge Conflict / Shared file / Proto 协议 / DB&配置变更)策略各异,核心思路"能事前隔离就事前隔离,必须共享就串行收口"。

5. **AI 负责认知,脚本负责执行 + 核心工程原则 7 条**:15 个脚本把确定性操作(状态文件 JSON 解析 / git worktree 操作 / 编译发布 / 知识库初始化)从 AI 手里收回。**7 条核心原则**:① AI 负责认知,脚本负责执行;② 长链路必须状态化;③ 知识库必须结构化;④ Agent 必须职责隔离;⑤ 执行步骤必须脚本化;⑥ Workflow 比 Prompt 更重要;⑦ 未来比拼的不是"用了多少 AI",而是能否把 AI 当作一个工程系统来设计。**3 个具体取舍**:弃用主子 Agent 模式 / 弃用 Shell 脚本(改 Go 强类型) / 严格禁用项目级 Memory(防止上下文串扰)。

## 关键参数/数字

| 项 | 数字/范围 | 用途 |
|---|---|---|
| 知识库覆盖 | 90+ 微服务 / 800+ 结构化文档 / 4 业务域 | 应用宝游戏研发后台 |
| 端到端流程规模 | 12 专家 Agent / 30+ 业务 Skill / 10+ 流程脚本 | 重构后沉淀 |
| 自动生成文档类别 | 8 类(overview/interfaces/architecture/dependencies/storage/config/pitfalls/log.md) | 每服务一套 |
| 知识库目录结构 | 3 层(总览层/域层/服务层)+ 2 类(自动/手工) | LLM Wiki/Obsidian-Wiki 借鉴 |
| 知识加载层次 | 3 层渐进(关键词匹配 / grep meta.yaml / 按查询模式按需加载) | 替代 RAG |
| 知识查询模式 | 4 种(PRD 拆解 / 技术方案 / 接口搜索 / 知识库问答) | 按场景选 |
| 状态文件 | 2 类(product-state.json / e2e-state.json) | 流程持久化 |
| Hook 事件 | 3 个(Stop / SessionStart / SessionEnd) | 强制流程推进 |
| 专家 Agent 设计原则 | 5 项(单一职责/上下文隔离/工具最小权限/确定性输入输出/模型可插拔) | Agent 体系 |
| 专家 Agent 个数 | 12 个 | 沉淀 |
| 并行层级 | 2 层(Worktree 隔离 / Fork-Join) | 从串行到并行 |
| 冲突类型 | 4 类(Merge/Shared file/Proto/DB&配置) | 治理策略 |
| 流程脚本 | ~15 个(e2e-dev.py / worktree.sh / build-and-publish.sh / kb-init.sh 等) | 确定性操作脚本化 |
| 文档新鲜度检测 | git_hash 增量模式 + log.md 不可覆盖 | 知识保鲜 |
| 核心工程原则 | 7 条 | 向上抽象 |
| TDD 落地策略 | 不在代码层,在接口测试用例层 | 务实取舍 |
| Vibe Coding 边界 | 看板类(结果导向+容错高)适合黑盒化,核心在线业务系统仍需人守架构 | 场景区分 |

## 核心金句

1. **"任务越是完整、越是规模化、越是可抽象成稳定流程,其仅仅采用对话式 AI coding 来完成的弊端就越明显,采用 Harness 工程实践的价值也就越高。"**(全文核心论点)
2. **"AI 负责认知,脚本负责执行。"**(反复强调的工程核心思想)
3. **"过期知识比没有知识更危险。"**(曾因知识库未更新,AI 调了老接口,排查很久才发现)
4. **"Workflow 比 Prompt 更重要——流程编排的确定性,胜过反复打磨 prompt。"**(与 Leeka / Addy Loop 主线呼应)
5. **"未来比拼的不是'用了多少 AI',而是能否把 AI 当作一个工程系统来设计。"**(终局认知)
6. **"从'逐行审查'到'忘记代码',变化的从来不是代码的价值,而是人在系统中的位置。"**(5.3.3 收尾)

## 关联图谱

### 上游(基于 / 来自)
- **Harness Engineering 概念**:Claude Code / OpenClaw / Hermes / Addy Osmani 把"模型是概率的,真正让 Agent 可用可控的是外面那层骨架"带火
- **LLM Wiki / Obsidian-Wiki / GBrain**:知识库结构化方法论来源
- **强类型语言状态机思想**:Go 重构 Shell 脚本驱动的流程
- **多 Agent 并行思想**:task-planner + DAG 拓扑分层

### 下游(应用于 / 验证于)
- **应用宝活动平台重构**:上半年完成完整重构,4 业务域(活动/福利/商城/增长)
- **With 平台活动集成看板**:100% AI Vibe Coding 生成,无任何 CR——验证"代码黑盒化"的边界
- **Claude Workflow 模式**:团队正在探索"脚本串联流程,必要时脚本 call AI"

### 同级(横向 / 并列)
- Harness 主线:[[Harness工程AgentLoop]] / [[HarnessEngineering企业级实战]] / [[阿里云开发者-淘宝主播Agent的Harness工程实战]] / [[0xCodez-Agent-Harness-14-Steps]] / [[harness-engineering]]
- 端到端流程:[[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] / [[Hermes-Agent重构得物数仓工作流]] / [[Leeka-Task-Decomposition-Agentic-Workflow]]
- Loop 验证:[[Loop-Engineering-验证才是瓶颈]] / [[Addy-Osmani-Loop-Engineering]]
- AI Coding 范式:[[Code-is-cheap-AI-Native-五倍效率]] / [[字节跳动洪定坤-AI-Coding的实践与探索]]

## 备注与限制

- 当前阶段团队自评"仅处于'能跑'的刚起步状态",缺自进化能力 / 评估体系 / 工具解耦
- 整套体系重度依赖 codebuddy cli 工具,工程与工具未解耦
- 仅覆盖 Go 后台业务,前端 / 客户端 / 嵌入式系统未涉及
- 弃用项目级 Memory 与 Claude / OpenClaw 等工具的默认行为有冲突,需人工确认
- 知识库增量模式依赖 git diff,需保证 git 工作流稳定(避免 force push / squash)
- 7 条核心工程原则是"沉淀式",非实证,需团队具体场景验证优先级
- "5.3.1 TDD 在 AI 时代"和"5.3.3 代码还重要吗"是开放性思考,非 Harness 工程具体实施
- 文章附带文末推广"Mac 应用宝",与正文 Harness 工程无关