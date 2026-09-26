# Harness Engineering for Self-Improvement（翁荔）- Digest

## 一句话总结

Lilian Weng(翁荔)把"Harness 是包裹在裸模型和真实场景之间的操作系统"这件事讲透了——**RSI 近期路径不靠"模型改自己权重",靠 Harness Engineering 演进到"元方法论";Harness 层优化对象会从 prompt→上下文→工作流→harness 代码→optimizer 代码 5 段路径**。

## 核心观点 5 条

1. **Harness = 模型与场景的操作系统**。定义："harness 是包裹在基础模型外面的系统,负责编排执行过程,决定模型怎么思考和规划、怎么调用工具和行动、怎么感知和管理上下文、怎么存储产出物、怎么评估结果。" Claude Code / Codex 的成功印证 Harness 与模型本身同等重要。
2. **三种设计模式**:① 工作流自动化(loop engineering,Karness + autoresearch) ② 文件系统作为持久记忆(状态存文件,不塞上下文) ③ 子 Agent 与后端任务(显式且可检查,父 agent 跑进程管理器)
3. **优化对象 5 段演进路径**:指令 prompt → 结构化上下文 → 工作流 → harness 代码 → optimizer 代码
4. **自动化优化 3 类方法**:ACE(把 context 当工作记忆)/ MCE(用反思+进化搜索自动生成 context 策略)/ Meta-Harness(直接搜 harness 代码,如 Darwin Gödel Machine 在 SWE-bench 从 20% 提到 50%)
5. **RL 优化 Harness 的最大风险 = reward hacking**:模型可能绕过测试、修改测试用例、删功能性代码以让测试通过——必须保持在线(避免离线过拟合)并在真实环境持续验证

## 关键参数 / 决策树

| 选择 | 何时用 | 反例 |
|---|---|---|
| 工作流自动化 | 任务可重复可迭代、有清晰目标 | 一次性探索 |
| 文件系统持久记忆 | 任务跨 session、状态>上下文窗口 | 短任务简单查询 |
| 子 Agent + 后端 | 主 agent 要并行多假设/独立子任务 | 强耦合任务 |
| ACE 工作记忆 | 任务长、需要错误信号整合 | 短时一次性 |
| MCE 反思搜索 | 任务模板稳定、可以组合 (M choose K) 种策略 | 任务高度异质 |
| Meta-Harness | harness 代码本身就是优化目标 | harness 还很小时 |
| RL 优化 | 真实环境反馈可量化 | 离线训练(易 reward hacking) |
| 人工规则 | 边界条件、用户协作、反模式提醒 | 规则太多反而损害泛化 |

## 速查表

### Harness 工程 4 件事(翁荔视角)

1. **设计原则** = 简洁 + 通用 + 依赖预训练知识(不要硬塞所有边界条件)
2. **操作系统类比** = Harness 应该像 OS,把复杂逻辑封装起来,接口简单
3. **协议标准化** = config / 工具接口 / 协议会随行业发展逐渐统一
4. **人在高层监督** = 哪些约束硬编码、哪些让模型判断、哪些运行时反馈——这 3 类划分仍由人主导

### 与已有 Harness 主线的对比

| 视角 | 代表 | 核心贡献 |
|---|---|---|
| **学术原典** | **Lilian Weng(本文)** | Harness 定义 + RSI 框架 + 5 段演进路径 + 3 类优化方法 |
| X 长文 14 步 | [[0xCodez-Agent-Harness-14-Steps]] | Loop 地基 + 3 段 14 步 + 8 反模式 |
| 阿里企业实战 | [[HarnessEngineering企业级实战]] | 25%→90% AI 代码率 + 10 阶段 Pipeline + 四要素架构 |
| 阿里妹端到端 | [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] | 4 层 8 步 Agent 端到端 |
| 阿里淘宝主播 | [[阿里云开发者-淘宝主播Agent的Harness工程实战]] | 状态文件 + 8 阶段管道 + 6 类 SOP |
| 腾讯应用宝 | [[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] | 12 专家 Agent + DAG 并行 + 15 脚本 |
| 字节 TRAE | [[字节跳动洪定坤-AI-Coding的实践与探索]] | 3×3×100 实验 + Harness 基建 + 指标陷阱 |
| 字节 90% AI 代码 | [[Code-is-cheap-AI-Native-五倍效率]] | 代码是卫生纸 + 水流理论 + 6 种 checkpoint |
| Loop 验证 | [[Loop-Engineering-验证才是瓶颈]] | 验证闸门 + 5 步骨架 + 5+1 积木 |

## 核心金句 5 条

- "harness 是包裹在基础模型外面的系统,负责编排执行过程"
- "harness engineering 会朝'元方法论'的方向演进——优化的是获得更好答案的机制本身,而不只是答案"
- "成熟的 harness 反过来让模型自我改进的 auto-research 循环变得可能,而更聪明的模型也能防止 harness 被过度设计"
- "很多 harness 层的改进可能会被内化进核心模型的行为里,但与外部上下文和工具的接口应该会保留下来"
- "人应该往抽象栈的更高层移动,而不是被从循环里挪走"

## 关联图谱

### 上游(基于 / 来自)
- I. J. Good 1965 "超级智能机器"概念
- Yudkowsky RSI 反馈回路概念
- 翁荔 2023 《LLM Powered Autonomous Agents》"Agent = LLM + 记忆 + 工具 + 规划 + 行动" 公式
- Karpathy autoresearch 仓库(工作流自动化案例)

### 下游(应用于 / 验证于)
- [[0xCodez-Agent-Harness-14-Steps]] 14 步路线图 → 本文"5 段优化路径"对应"harness 代码→optimizer 代码"
- [[HarnessEngineering企业级实战]] 阿里 25%→90% → 印证本文"harness 与模型同等重要"
- [[Harness工程AgentLoop]] 5 大工程决策 + 4 失效场景 → 印证本文"3 种设计模式"
- [[Loop-Engineering-验证才是瓶颈]] 验证闸门 → 印证本文"reward hacking 风险"
- [[Addy-Osmani-Loop-Engineering]] 5+1 积木 → 印证本文"工作流自动化模式"
- [[Code-is-cheap-AI-Native-五倍效率]] 水流理论 → 印证本文"harness 应该刻意保持简洁通用"
- [[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] 12 专家 + DAG → 印证本文"子 Agent 与后端任务"
- [[字节跳动洪定坤-AI-Coding的实践与探索]] 3×3×100 实验 → 印证本文"RL 优化 Harness 风险"

### 同级(横向 / 并列)
- [[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] Anthropic 团队视角(管理者)
- [[AI-Native企业-Agent团队和AI-Factory重写公司体系]] Groupon 视角(VP 工程)
- [[Multica-AI-Native-组织-人是最慢的节点]] 极端样本(4 人+几十 Agent)
- [[Leeka-Task-Decomposition-Agentic-Workflow]] 任务拆解视角

## 备注与限制

1. **工具分类图未抓取**:原文给出 Claude Code/Codex 工具分类完整版(10+ 类工具)本次未抓取图,建议读 https://lilianweng.github.io/posts/2026-07-04-harness/ 原文
2. **工作流图也是图**:planning-execution-observation-loop 的工作流图未抓取
3. **DGM 20%→50% 数字未独立验证**:来自 Sakana 团队口径
4. **翁荔个人观点 vs 行业共识**:harness 内部化预测、3 类划分(硬编码/模型判断/运行时反馈)是翁荔本人观点,非行业共识
5. **不是入门文章**:本文假设读者已了解 LLM/Agent/RL 基础,适合 Harness 实战已上路的人
6. **4 段 RSI 路径翁荔判断近期不会 model-driven**:但学界/业界对这条预测有分歧,需关注后续