---
title: Lilian Weng Harness Engineering for Self-Improvement — 翁荔的 Harness 学术原典
category: 01-ai-agents
tags:
  - 主题/Harness
  - 主题/RSI
  - 主题/学术原典
  - 主题/翁荔
  - 主题/工程哲学
  - 主题/Anthropic
  - 主题/Thinking-Machines-Lab
  - 主题/Seetong借鉴
  - 场景/微信编译
  - 场景/AI-Researchers
  - 节点/Harness定义
  - 节点/操作系统类比
  - 节点/三种设计模式
  - 节点/五段优化路径
  - 节点/三类自动化优化
  - 节点/RL_reward_hacking
  - 节点/内部化预测
  - 节点/人在抽象栈高层
  - 作者/翁荔-Lilian-Weng
  - 编辑/Datawhale
nodes: [Harness定义, 操作系统类比, 三种设计模式, 五段优化路径, 三类自动化优化, RL优化_reward_hacking风险, Harness内部化预测, 人在抽象栈高层]
links: [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[01-ai-agents/HarnessEngineering企业级实战]], [[01-ai-agents/Harness工程AgentLoop]], [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]], [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]], [[01-ai-agents/Loop-Engineering-验证才是瓶颈]], [[02-ai-coding/Addy-Osmani-Loop-Engineering]], [[02-ai-coding/字节跳动洪定坤-AI-Coding的实践与探索]], [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]], [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]], [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]], [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]], [[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]], [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]]
date: 2026-07-08
source: 微信公众号「Datawhale干货」2026-07-08 推送 / 翁荔 Lilian Weng（编译）
---

# Lilian Weng Harness Engineering for Self-Improvement — 翁荔的 Harness 学术原典

- **原文链接**：https://lilianweng.github.io/posts/2026-07-04-harness/
- **公众号**：「Datawhale干货」2026-07-08 推送
- **原作者**：翁荔(Lilian Weng)，前 OpenAI 安全研究副总裁，现 Thinking Machines Lab 联合创始人，Lil'Log 博客主理（Google Scholar 引用量 5 万+）
- **编译**：Datawhale 编辑团队
- **分类理由**：本文是 Harness 主题**学术原典 + RSI 框架**视角（区别于实战派：阿里/腾讯/字节/0xCodez）；补完 01-ai-agents 现有 Harness 实战主线缺位的"理论框架 + 5 段优化路径 + 3 类自动化方法 + reward hacking 风险"维度
- **获取时间**：2026-07-08 10:38

## 核心结论

> **Harness 是包裹在裸模型和真实场景之间的"操作系统"——RSI（递归自我改进）近期路径不靠"模型改自己权重"，靠 Harness Engineering 演进到"元方法论"；优化对象会从 prompt→上下文→工作流→harness 代码→optimizer 代码 5 段路径推进。**

- **场景**：学术原典 / RSI 框架 / Harness 主题理论
- **类型**：Harness 主题**学术视角**补完（区别于实战派：阿里/腾讯/字节/0xCodez）
- **关键定位**：翁荔是 2023 年那条被引最广的 Agent 公式（"Agent = LLM + 记忆 + 工具 + 规划 + 行动"）的提出者；本文是她在 Harness 主题上的**正式长文**。

## 8 个知识节点（独立概念）

1. **Harness 定义**：包裹在基础模型外面的系统，负责编排执行过程——思考规划、工具调用、上下文感知、持久状态、评估结果。翁荔把"agent = LLM + 记忆 + 工具 + 规划 + 行动"作为对比起点，但 Harness 不再只是 prompt 模板，而是更接近运行时 + 软件系统设计。
2. **操作系统类比**：Harness 应该像 OS 把复杂逻辑封装起来同时保持接口简单；config、工具接口、协议会随行业发展逐渐标准化（类似 prompt engineering 时代的标准化）。
3. **3 种设计模式**：① 工作流自动化（loop engineering，Karpathy autoresearch 是干净例子） ② 文件系统作为持久记忆（状态存文件，不塞上下文） ③ 子 Agent 与后端任务（显式可检查，父 agent 跑进程管理器）。
4. **5 段优化路径**：指令 prompt → 结构化上下文 → 工作流 → harness 代码 → optimizer 代码。模型越强，能驾驭的目标越复杂（与 [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] 14 步路线图交叉印证）。
5. **3 类自动化优化**：ACE（context 当工作记忆，rollout + 批评 + 环境反馈整合）/ MCE（反思+进化搜索自动生成 context 策略，组合空间 `(M choose K)`）/ Meta-Harness（直接搜 harness 代码，如 Darwin Gödel Machine 在 SWE-bench 20%→50%）。
6. **RL 优化 Harness 的 reward hacking 风险**：模型可能绕过测试、修改测试用例、删功能性代码以让测试通过；必须保持在线训练 + 真实环境持续验证，否则就是"装腔作势"——与 [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] 验证闸门呼应。
7. **Harness 内部化预测**：harness 层改进会被内化进核心模型，但接口保留（类似 prompt engineering 历史——指令微调提升后，手工 prompt 技巧变得不那么核心，但"指定目标/约束/上下文/评估"的需求没消失）。这意味着**真正有效的 Harness 看起来"什么都没做"**。
8. **人在抽象栈高层**：harness design 仍由人主导，未来人往抽象栈更高层移动而非被从循环里挪走。3 类约束划分：硬编码 / 模型判断 / 运行时反馈——这 3 类划分仍由人主导。

## 关联图谱

### 上游（基于 / 来自）
- I. J. Good 1965 "超级智能机器"概念 / Yudkowsky RSI 反馈回路
- 翁荔 2023《LLM Powered Autonomous Agents》"Agent = LLM + 记忆 + 工具 + 规划 + 行动" 公式（行业最被引）
- Karpathy autoresearch 仓库（工作流自动化案例）

### 下游（应用于 / 验证于）
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] 14 步路线图 → 本文"5 段优化路径"对应"harness 代码→optimizer 代码"
- [[01-ai-agents/HarnessEngineering企业级实战]] 阿里 25%→90% AI 代码率 → 印证 Harness 与模型同等重要
- [[01-ai-agents/Harness工程AgentLoop]] 5 大工程决策 + 4 失效场景 → 印证"3 种设计模式"
- [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]] 水流理论 + 6 种 checkpoint → 印证"Harness 应该刻意简洁通用"
- [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] 12 专家 + DAG → 印证"子 Agent 与后端任务"
- [[02-ai-coding/字节跳动洪定坤-AI-Coding的实践与探索]] 3×3×100 实验 → 印证"RL 优化 Harness 风险"
- [[02-ai-coding/Addy-Osmani-Loop-Engineering]] 5+1 积木 → 印证"工作流自动化模式"

### 同级（横向 / 并列）
- [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] Anthropic 团队视角（管理者）
- [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]] Groupon 视角（VP 工程）
- [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]] 极端样本（4 人+几十 Agent）
- [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]] 任务拆解视角
- [[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]] "什么时候选 Agent" 视角
- [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]] 单 Agent 端到端 4 层 8 步

## 正文要点（5 条）+ Seetong 借鉴动作（6 条）

### 正文要点
1. **Harness 重要性 = 模型重要性**。"Lilian Weng 特别强调'部署系统'这个词……包在裸模型和真实场景之间的这一层，重要性不亚于模型本身的原始智能。Claude Code、Codex 这类编码 Agent 产品的成功，印证了 harness 在 AI 部署里的分量。"
2. **Harness 简洁性 vs 边界条件**。"把很多条件硬塞到 prompt 里或加到 harness 里，反而会损害系统在新场景下的泛化能力"——Harness 应该刻意保持简洁、通用，依赖预训练已经学到的知识，而不是把所有边界条件都罗列出来。
3. **人工规则局限**。"LLM 不会精确遵循每条规则，而且对 LLM 能力越强，越能在执行中'绕过'规则"——这是 1.0 prompt 时代的根本局限，也是 Harness 要向"元方法论"演进的原因。
4. **人不在循环里 = 错**。"人应该往抽象栈的更高层移动，而不是被从循环里挪走"——harness 工程的很多挑战，最终都需要人的反馈和引导才能解决。
5. **接口会保留**。"很多 harness 层的改进可能会被内化进核心模型的行为里，但与外部上下文和工具的接口应该会保留下来"——这意味着即使 Harness 层被模型内化，工具 API/MCP 协议这类外部接口不会消失。

### Seetong 借鉴动作

| # | 借鉴动作 | 对应翁荔节点 | 关联条目 |
|---|---|---|---|
| 1 | **CLI 工具分类体检**：Seetong AI 助手工具集按"文件/shell/搜索/编辑/版本控制/测试/文档/agent 调度/通讯/用户交互"10 类盘点，识别缺哪一类 | 节点 1 定义 | - |
| 2 | **工作流自动化优先（5+1 积木）**：Seetong AI 助手按 Loop 思路搭 5 个积木（自动化/技能/子代理/连接器/验证器）+ 1 个拒绝机制 | 节点 3 模式① | [[02-ai-coding/Addy-Osmani-Loop-Engineering]] [[02-ai-coding/AI循环-Claude-GPT和Mira到底什么才是真正好用的]] |
| 3 | **文件系统作为持久记忆**：Seetong 状态文件（spec/codemap/新对话上下文）替代"全塞上下文" | 节点 3 模式② | [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] product-state.json 模式 |
| 4 | **5 段优化路径对照**：Seetong AI 助手自评当前在哪一段（指令 prompt？结构化上下文？工作流？harness 代码？optimizer 代码？）——明确下一步演进方向 | 节点 4 路径 | [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] |
| 5 | **Harness 内部化季度复盘**：每季度 review——哪些"老 prompt 技巧"已被模型内化（删掉）？哪些"老 harness 设计"反而限制了模型能力（重写）？ | 节点 7 内部化 | - |
| 6 | **人在抽象栈高层**：Seetong 主人+黄松佳+谭伟+张威按"Harness 设计评审 + 边界设定"角色走，**不**在 harness 代码细节里写 | 节点 8 人在高层 | [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] "Fiona 团队 8 倍产出靠慢方法论" |

## 备注与限制

- **工具分类图未抓取**：原文给出 Claude Code/Codex 工具分类完整版（10+ 类工具）本次未抓取图，建议读 https://lilianweng.github.io/posts/2026-07-04-harness/ 原文
- **工作流图也是图**：planning-execution-observation-loop 工作流图未抓取
- **DGM 20%→50% 数字未独立验证**：来自 Sakana 团队口径
- **翁荔个人观点 vs 行业共识**：harness 内部化预测、3 类划分是翁荔本人观点，非行业共识
- **不是入门文章**：本文假设读者已了解 LLM/Agent/RL 基础，适合 Harness 实战已上路的人
- **4 段 RSI 路径翁荔判断近期不会 model-driven**：学界/业界对这条预测有分歧，需持续跟踪
- **建议补条目**：[[thinking-machines-lab]] 翁荔现公司（暂未建）