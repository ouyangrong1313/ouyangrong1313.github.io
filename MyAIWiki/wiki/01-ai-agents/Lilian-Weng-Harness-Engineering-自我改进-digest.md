# Lilian Weng Harness Engineering - Digest

## 一句话总结

Lilian Weng（翁荔）把"Harness 是包裹在裸模型和真实场景之间的操作系统"讲透了——**RSI 近期路径不靠"模型改自己权重"，靠 Harness Engineering 演进到"元方法论"；优化对象会从 prompt→上下文→工作流→harness 代码→optimizer 代码 5 段路径推进**。

## 5 段核心论证（速查表）

| 段 | 主题 | 关键命题 | 关键数据/概念 |
|---|---|---|---|
| 1 | Harness 在 AI 部署中的分量 | Harness 重要性 = 模型本身重要性 | Claude Code/Codex 印证；2023 Agent 公式作对比起点 |
| 2 | 三种设计模式 | 工作流自动化 / 文件系统记忆 / 子 Agent 并行 | Karpathy autoresearch；OS 类比；config/工具接口标准化 |
| 3 | Harness 怎么被优化 | 5 段路径：prompt→上下文→工作流→harness 代码→optimizer 代码 | ACE 工作记忆 / MCE 反思搜索 / Meta-Harness Darwin Gödel Machine SWE-bench 20%→50% |
| 4 | RL 优化 Harness 的风险 | Reward hacking 是巨大风险 | 模型可能绕过/修改/删除测试；必须在线+真实环境 |
| 5 | 人的角色 | 人往抽象栈高层移动，不被从循环里挪走 | 3 类约束划分：硬编码/模型判断/运行时反馈 |

## 8 节点速查

1. **Harness 定义** = 包裹模型外的系统（编排 + 思考 + 工具 + 上下文 + 持久 + 评估）
2. **OS 类比** = Harness 像 OS 封装复杂逻辑 + 接口简单
3. **3 种设计模式** = 工作流自动化 / 文件系统记忆 / 子 Agent 并行
4. **5 段优化路径** = prompt → 上下文 → 工作流 → harness 代码 → optimizer 代码
5. **3 类自动化优化** = ACE 工作记忆 / MCE 反思搜索 / Meta-Harness 搜代码
6. **Reward hacking 风险** = RL 优化必须在线 + 真实环境
7. **Harness 内部化** = 层改进会被模型内化，但接口保留
8. **人在高层** = 3 类约束划分仍由人主导

## 5 句关键金句

- "harness 是包裹在基础模型外面的系统，负责编排执行过程"
- "harness engineering 会朝'元方法论'的方向演进——优化的是获得更好答案的机制本身，而不只是答案"
- "成熟的 harness 反过来让模型自我改进的 auto-research 循环变得可能，而更聪明的模型也能防止 harness 被过度设计"
- "很多 harness 层的改进可能会被内化进核心模型的行为里，但与外部上下文和工具的接口应该会保留下来"
- "人应该往抽象栈的更高层移动，而不是被从循环里挪走"

## 3 个反直觉点

- **真正决定 AI 能力的是 Harness 不是模型**（Claude Code/Codex 印证）
- **优化 harness 反而是 RSI 近期路径**，而非"模型直接改自己权重"
- **Harness 内部化 → 真正有效的 harness 看起来"什么都没做"**

## 5 关键数字

- **5 段优化路径** = prompt → 上下文 → 工作流 → harness 代码 → optimizer 代码
- **3 类自动化优化** = ACE / MCE / Meta-Harness
- **3 种设计模式** = 工作流 / 文件 / 子 Agent
- **20%→50%** = Darwin Gödel Machine 在 SWE-bench 提升
- **3 类约束划分** = 硬编码 / 模型判断 / 运行时反馈

## 6 个对 Seetong 团队可借鉴动作

1. **CLI 工具分类体检**：10 类工具盘点，识别缺哪一类
2. **工作流自动化优先（5+1 积木）**：搭 5 积木 + 1 拒绝机制
3. **文件系统作为持久记忆**：状态文件（spec/codemap）替代"全塞上下文"
4. **5 段优化路径对照**：自评 Seetong AI 助手当前在哪一段
5. **Harness 内部化季度复盘**：删被模型内化的老 prompt、重写限制模型能力的 harness
6. **人在抽象栈高层**：主人+leader 走"Harness 设计评审+边界设定"角色，不写细节

## 强关联（同主线 8 个强关联）

- [[0xCodez-Agent-Harness-14-Steps]] 14 步路线图 → 5 段路径对应 harness 代码→optimizer 代码
- [[HarnessEngineering企业级实战]] 阿里 25%→90% → 印证 Harness = 模型
- [[Harness工程AgentLoop]] 5 工程决策 → 印证 3 种设计模式
- [[Code-is-cheap-AI-Native-五倍效率]] 水流理论 → 印证 Harness 简洁
- [[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] 12 专家 + DAG → 印证子 Agent
- [[字节跳动洪定坤-AI-Coding的实践与探索]] 3×3×100 → 印证 RL 风险
- [[Loop-Engineering-验证才是瓶颈]] 验证闸门 → 印证 reward hacking
- [[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] 团队视角

## 备注与限制

- 工具分类图 + 工作流图未抓取
- DGM 20%→50% 数字未独立验证
- 翁荔个人观点非行业共识
- 不是入门文章，适合 Harness 实战已上路的人
- 4 段 RSI 路径预测学界有分歧