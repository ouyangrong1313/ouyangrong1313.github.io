---
title: 从 AI Coding 到 Harness Engineering 应用宝活动平台端到端实践
category: 01-ai-agents
tags: [#主题/Harness, #主题/AI-Agent, #主题/知识库, #主题/端到端开发, #主题/多Agent, #主题/工程实践, #主题/腾讯, #主题/Seetong借鉴]
nodes: [状态文件驱动, 专家Agent体系, Worktree-DAG-Fork-Join并行, 冲突治理四象限, 脚本化执行, DevOps多平台集成, 结构化知识库与渐进式加载, 文档新鲜度检测]
links: [[阿里云开发者-淘宝主播Agent的Harness工程实战]], [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[HarnessEngineering企业级实战]], [[Harness工程AgentLoop]], [[0xCodez-Agent-Harness-14-Steps]], [[harness-engineering]], [[Hermes-Agent重构得物数仓工作流]], [[Code-is-cheap-AI-Native-五倍效率]], [[Loop-Engineering-验证才是瓶颈]], [[Leeka-Task-Decomposition-Agentic-Workflow]]
date: 2026-07-05
source: 微信公众号 / 腾讯程序员 2026-07-05(腾讯应用宝活动平台团队 / zimingxing、kinglongli、yifhao)
原始链接: https://mp.weixin.qq.com/s/UE-RZH9hnbBd06CVapFGrA
---

# 从 AI Coding 到 Harness Engineering 应用宝活动平台端到端实践

> **核心结论**:**Harness 化不是给对话式 AI Coding 加更多规则,而是把"一个对话窗口"升级为一套工程系统——拆上下文 + 状态文件 + 确定性编排 + DAG 并行 + 脚本化执行 + DevOps 集成**;知识库是底座(800+ 文档覆盖 90+ 微服务),端到端流程沉淀 12 个专家 Agent + 30+ 业务 Skill + 10+ 流程脚本。

## 8 个独立知识节点

- **状态文件驱动(product-state.json + e2e-state.json)**:把端到端流程从"对话历史"中抽出来,持久化到两类结构化 JSON——多 Story 并行的 `product-state.json`(breakdown / forking / joining) + 单 Story 端到端的 `e2e-state.json`(Phase 0~7 / 产出 / 接口验证结果)。子 Agent 在独立上下文执行完毕后写状态文件,主调度器直接读文件判断"下一步干什么",**三件事一次解决**:上下文有损压缩、流程中断无法恢复、推进缺乏可观测。配套 3 个 hook(Stop / SessionStart / SessionEnd)防止主调度器"偷懒式"提前停止。

- **专家 Agent 体系(12 个专家 + 5 项设计原则)**:每个 Agent 只做一件事——code-reviewer 只评不改、interface-verifier 只诊断不改、code-fixer 只在收到问题清单后才动手。**5 项设计原则**:单一职责 / 上下文隔离 / 工具最小权限(审查类不给写文件,规划类不给发布) / 确定性输入输出(不靠对话传信息,靠结构化字段) / 模型可插拔(便宜模型做状态解析,强模型做代码审查)。沉淀 12 个专家(prd-decomposer / task-planner / story-developer / unit-test-agent / codar-reviewer / galileo-root-cause / test-case-designer / code-reviewer / publisher / git-committer 等)。**3 个收益**:行为稳定 / 主调度器负担减少 / 单点修改不影响全局。

- **Worktree 隔离 + DAG 编排 + Fork-Join(从串行到并行)**:两层并行。**第一层** task-planner 根据需求文档按接口/模块拆任务,标注依赖关系,构建 DAG 拓扑分层,同层任务并发,每个并发任务分配独立 git worktree,本轮结束后统一 merge。**第二层** 多 Story 场景:Phase R 产品需求拆解 → Fork 段并行跑 Phase 1~4(任务拆解→波次开发→单测→代码审查) → Join 段串行收口(合并→发布→验证→提交)。**两个反直觉**:① 不仅是性能优化,主流程上下文也会因并发而大幅减少 ② 多 Story 场景模拟"人协作的临时分支",而不是"每个 Story 独立发布"。

- **冲突治理四象限(能事前隔离就事前隔离,必须共享就串行收口)**:并行多 Agent 改代码不可避免冲突,4 类冲突 4 种策略。① **Merge Conflict**:task-planner touches 做文件级事前隔离,真冲突正常解,绝不用 --no-verify/丢弃绕过;② **Shared file**(如 main.go):并行阶段禁改,统一收敛到集成收口阶段单 Agent 执行;③ **Proto 协议**:仅当 has_pb_change=true 时由 proto-engineer 在 Rick 平台统一变更+生成桩代码,下游基于已生成桩开发;④ **DB/配置变更**:全局变更一次性前置确认(task-planner 阶段汇总),落地由专门 Agent 执行。

- **脚本化执行(AI 负责认知,脚本负责执行)**:把状态文件 JSON 解析 / git worktree 创建 / 编译发布 / 知识库初始化等"确定性操作"从 AI 手里收回到脚本。**核心原因**:让 AI 做这些事不仅消耗 token,还引入不必要随机性(写错 shell 语法 / 用错参数 / 同需求多次跑结果不一致)。前后沉淀约 15 个脚本——`e2e-dev.py` 状态机解析 / `worktree.sh + sub_worktree.sh` 多 worktree 操作 / `build-and-publish.sh` 一键发布 / `kb-init.sh` 知识库初始化。**判断标准**:有明确输入输出 / 操作路径非常清晰 → 脚本化;需要判断/分析/生成 → 留给 AI。

- **DevOps 多平台读写集成(打通最后一公里)**:端到端不止写代码,还要 TAPD 建子需求 / Rick 改协议 / 123 发布服务 / 七彩石改配置 / 伽利略查日志。**集成策略**:公司内大部分平台都有 MCP 服务或 Skill,集成到 Knot 平台 + 03 平台,AI 经人工确认后可直接读写。**两个具体方案**:① **tRPC-Gateway**:本地 AI 调通 123 内网 idc 接口(为每个服务申请白名单不通用);② **Codar CR skill**:AI 写代码让 AI 来审——增量 CR 由 Codar CLI 执行,问题清单返回主调度器,FIX Agent 修复。**已知例外**:七彩石 mcp 不支持 tconf 集群,123 业务配置页无法通过七彩石 mcp 读写。

- **结构化知识库 + 渐进式加载(替代 RAG)**:借鉴 LLM Wiki / Obsidian-Wiki / GBrain,**两层结构**:自动生成(AI 读代码生成)+ 人工沉淀(custom.md + common/ 沉淀业务背景/架构决策/使用规范)。**三层目录**:总览层 backend/overview.md → 域层 {group}/meta.yaml + custom/ → 服务层 {service}/*.md(8 类)+ custom/。**8 类自动生成文档**:overview / interfaces / architecture / dependencies / storage / config / pitfalls / log.md(不可覆盖历史)。**渐进式加载 3 层**:第一层关键词匹配缩小到 1-2 业务域 → 第二层 grep 在 meta.yaml 精确筛选 → 第三层按查询模式只加载必要文档类型(接口搜索连 overview.md 都不读)。**4 种查询模式**:A PRD 拆解 / B 技术方案拆解 / C 接口搜索 / D 知识库问答。**相对 RAG 的 4 个优势**:精准定位 / 自顶向下按需吸收 / 主动探索 / 维护成本低。

- **文档新鲜度检测(过期知识比没有知识更危险)+ 核心工程原则 7 条**:`meta.yaml` 记录 `git_hash`(上次生成时代码版本),与仓库当前 HEAD hash 对比,超阈值标记过期,派发 codebuddy 命令行以增量模式更新。**增量模式 3 特性**:① 最小改动原则(避免大改);② 人工批注保留(业务背景说明、使用示例等"高价值内容"继承);③ log.md 追加不可覆盖(可审计、可回溯)。**实战教训**:曾因知识库未更新,AI 调用了老接口,整个链路通了但拿不到预期结果,排查很久才发现。**7 条核心工程原则**(从具体场景向上抽象):① AI 负责认知,脚本负责执行;② 长链路必须状态化;③ 知识库必须结构化;④ Agent 必须职责隔离;⑤ 执行步骤必须脚本化;⑥ Workflow 比 Prompt 更重要;⑦ 终局认知——未来比拼的不是"用了多少 AI",而是能否把 AI 当作一个工程系统来设计。

## 关联图谱

### 上游(基于 / 来自)
- **Harness Engineering 概念走红**:Claude Code / OpenClaw / Hermes / Addy Osmani Loop 思想带火"模型能力是概率的,真正让 Agent 可用可控的是外面那层工程化骨架"
- **LLM Wiki / Obsidian-Wiki / GBrain**:知识库结构化方法论
- **强类型语言与状态机思想**:Go 强类型重构 Shell 脚本 + 状态文件 = 流程可中断可恢复

### 下游(应用于 / 验证于)
- **应用宝活动平台重构**:上半年完成,4 业务域(活动/福利/商城/增长) / 90+ 微服务 / 800+ 结构化文档 / 12 专家 Agent / 30+ 业务 Skill / 10+ 流程脚本
- **With 平台活动集成看板**:100% AI Vibe Coding 生成,无任何 CR,适合"结果导向 + 容错率高 + 无强一致性"场景——验证"代码黑盒化"的边界
- **Claude Workflow 模式**:团队正在探索"由脚本串联流程,必要时脚本 call AI",而非"AI 串联流程"

### 同级(横向 / 并列)
- Harness 主线:[[Harness工程AgentLoop]] / [[HarnessEngineering企业级实战]] / [[阿里云开发者-淘宝主播Agent的Harness工程实战]] / [[0xCodez-Agent-Harness-14-Steps]] / [[harness-engineering]] / [[Code-is-cheap-AI-Native-五倍效率]]
- 端到端流程:[[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] / [[Hermes-Agent重构得物数仓工作流]] / [[Leeka-Task-Decomposition-Agentic-Workflow]]
- Loop 验证:[[Loop-Engineering-验证才是瓶颈]] / [[Addy-Osmani-Loop-Engineering]]
- 多 Agent 架构:[[OpenClaw-vs-Hermes-多-Agent-架构设计]] / [[从零设计生产级-Multi-Agent-Harness]]

## 6 个对 Seetong 团队可借鉴动作

1. **状态文件驱动先于多 Agent**:把 Seetong AI 助手每个长流程(如 Bug 修复、版本回顾、简报生成)的状态写盘——当前 Phase / 已完成步骤 / 下一步动作 / 中间产物。即使会话中断也能续上,这是"AI 提效 ≠ AI 可靠"的关键工程动作。优先用 JSON 而非数据库(MVP 阶段)。
2. **专家 Agent 5 项原则体检 Seetong Skill**:单一职责(seetong-bug-triage 不该同时改代码)/ 上下文隔离(每个 Skill 只加载必要文档)/ 工具最小权限(只读 Skill 不给写权限)/ 确定性输入输出(参数化,Skill 之间不靠对话)/ 模型可插拔(便宜模型做分类,强模型做根因)。12 个专家 Agent 体系可借鉴但不强求规模。
3. **冲突治理四象限入版本流程**:Seetong 多版本分支(8.3.x / 8.4.x)合并时的冲突类型映射——Merge Conflict(配置/路由文件)/ Shared file(Info.plist)/ Proto 协议变更 / 配置变更,各对应一个收口负责人或脚本。
4. **知识库先建"分层加载 + 自定义沉淀"再谈 RAG**:借鉴应用宝的"meta.yaml 注册中心 + 渐进式 3 层加载 + 4 种查询模式"。MyAIWiki 已经是结构化,但 Seetong AI 助手用的 Seetong 项目知识库(seetong-iOS / seetong-android / Seetong-cli 等)还需要按"3 层加载"重构,避免把所有文档一次塞上下文。
5. **15 个脚本沉淀 + 调度架构转 Go 强类型**:把 Seetong 重复执行的操作(Git worktree 操作 / TAPD 工时填写 / 反馈分诊 SOP / 简报模板渲染)沉淀为 shell 脚本或 Python 脚本;主调度器如果未来要做,优先 Go 而非 Shell(大模型生成的 Shell 脚本常潜藏隐性语法错误,长链路末端才暴露,极耗排查)。
6. **Vibe Coding 边界体检**:Seetong 内部区分"看板类系统"(适合 AI 全自动生成 + 不 CR)与"核心在线业务系统"(仍需人守住架构)。比如 Seetong 后台运营看板 / 内部工具 / Demo 类需求,可放开让 AI 100% 生成不 CR;4G IPC / 4G 远程开门 / 支付 / 安全 / 数据删除等路径,严守 review + 测试 + 灰度。

## 备注与限制

- **作者**:zimingxing、kinglongli、yifhao(腾讯应用宝活动平台团队),发布于腾讯程序员公众号
- **当前阶段**:团队自评"仅处于'能跑'的刚起步状态",缺少自进化能力 / 评估体系 / 工具解耦
- **范围**:仅 Go 后台业务覆盖,前端/客户端/嵌入式系统未涉及
- **依赖**:整套体系重度依赖 codebuddy cli 工具运行,工程与工具解耦未完成
- **未来方向**:Claude Workflow 模式启发下,探索"脚本串联流程"替代"AI 串联流程",让"确定性的归脚本,认知的归 AI"
- **取舍**:弃用主子 Agent 模式(改由外部主程序编排) + 弃用 Shell 脚本(改 Go 强类型) + 严格禁用项目级 Memory(防止上下文串扰)
- **微信原文**:约 15.8K 字符,5 个一级章节 + 27 个二级章节,涵盖知识库工程 + 端到端开发工程两条主线
- raw:../../raw/2026-07-05-腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践.md | raw-digest:../../raw/2026-07-05-腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践-digest.md | wiki-digest:./腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践-digest.md