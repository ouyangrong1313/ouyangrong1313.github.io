# 2026-07-储旭-从Prompt到Harness-企业级Agent工程的完整演进之路（原文摘要）

> **来源**：微信公众号「阿里妹」2026-07 推送（作者 储旭(槿柏) / 原文链接 https://mp.weixin.qq.com/s/xH4cyBJJJlG9cfcmSU5ztA）

## 一句话总结 + 核心金句

> **裸 LLM = 高性能 CPU，缺操作系统**——企业级 Agent 必须从 Prompt → Context → Harness → Agent OS 完整演进，构建 L1-L5 五层认知操作系统。

**5 句核心金句**：
1. **"不要用更大的模型掩盖工程层面的问题——模型从 32K 升级到 128K 不会解决注意力稀释，它只是把天花板从第 5 步推迟到第 8 步"**
2. **"信任不是一种态度，而是一种设计能力。最好的控制，看起来像自由"**
3. **"Agent 系统设计的本质不是控制 LLM 的行为，而是为 LLM 创造一个'犯错成本最低、正确路径最短'的执行环境"**
4. **"防御范式接受'模型会搬运数据'这个前提然后在后果上做文章；赋能范式直接消除了'模型需要搬运数据'这个前提"**
5. **"约束不是敌人，约束是创造力的起点。在这四面墙壁围成的房间里，我们构建了一套完整的操作系统"**

## 核心观点 5 条

1. **LLM 四大先天约束**是所有工程问题的源头：上下文窗口稀缺 / 注意力稀释 / 数据搬运谬误 / 无状态缺陷
2. **三层工程演进非可跃迁**：Prompt → Context → Harness，每层天花板推动下一层
3. **上下文管理 = 分层防御系统工程**：L1 工具结果压缩 / L2 语义压缩 / L3 对话压缩 / L4 数据总线——四层各管一段，无银弹
4. **从防御到赋能是设计哲学跃迁**：parameterBindings 替代 5 层修复管道（500 行占 50% 核心代码），消除"模型搬运数据"前提
5. **Agent OS 五层架构**：L1 执行集群 / L2 Runtime / L3 记忆语义 / L4 认知（注意力经济）/ L5 进化治理

## 关键参数 / 决策树

| 维度 | 阈值 / 公式 | 备注 |
|------|------------|------|
| 上下文窗口物理上限 | 128K | 5 步 + 3 轮即 200K+ |
| 注意力稀释阈值 | 第 8 步后质量明显下降 | 70% JSON / 20% 历史 / 10% 当前 |
| L1 触发条件 | >8000 字符 或 >10 数组元素 | 外置 MySQL + __refId |
| L2 触发条件 | >10000 字符 | temperature=0.3 LLM 蒸馏到 2000 字符 |
| L3 触发条件 | prompt_tokens / contextWindow >= 85% | 目标压缩到 30% |
| L4 预算 | 4096 字符 | 小数据全量 / 大数据 enhancedSummary |
| Transcript keepTarget | round(36 - steps × 0.8) | 5 步 ≈ 32 / 30 步 ≈ 12 |
| RecursionGuard | MAX_DEPTH=5 / MAX_CHAIN=20 | 同 skillId >=3 次拦截 |
| Agent 状态机 | candidate → shadow → probation → active → degraded → offboard | shadow 不生效仅记录 |
| 实际收益 | token -60%+ | 8 步衰减 → 30+ 步稳定 |

## 关联图谱 + 备注

### 上游（来自）
- ReAct Loop (Yao et al., 2022) / Anthropic Claude Code "Think Like an Agent" (2025) / OpenAI Codex / 治理理论：Douglas McGregor X/Y Theory / W. Edwards Deming 质量管理 / Richard Thaler Nudge Theory / Wittgenstein 语言哲学

### 下游（应用于）
- 企业级 Agent 平台搭建（L1-L5 完整 OS）/ OpenClaw 当前阶段定位（S1 → S2 → Agent OS）/ 断点续传 + 事件溯源（L2 执行账本模式）/ 从五层修复管道迁移到 parameterBindings

### 同级（横向）
- 现有 wiki 中的 [[0xCodez-Agent-Harness-14-Steps]] / [[HarnessEngineering企业级实战]] / [[Lilian-Weng-Harness-Engineering-自我改进]] / [[若飞-Agent-记忆与可验证自我改进怎么设计]] / [[InfoQ-Sam-Bhagwat-Harness长成Claw-心智争夺战]] / [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] / [[loop-engineering]] 等 Harness 主线文章

### 备注与限制
- **作者背景**：储旭(槿柏)，阿里巴巴 Agent 平台 S1/S2 主导者，本文是企业级 Agent 平台完整技术演进实录
- **5 大关键洞察**（6.1 节）：①"LLM 越跑越蠢"是工程问题非模型问题 ②上下文管理分层防御 ③Agent 动作空间必须治理（渐进式披露）④工具设计有半衰期 ⑤信任建立不能跳过人工确认
- **数据规模**：S2 实现后 token 消耗降低 60%+，Agent 从 8 步衰减、15 步几乎不可用 → 30+ 步稳定执行
- **理论参考**：本文综合 4 篇 2022-2025 关键文献 + 4 部 1960-2008 治理经典
- **未独立验证**：④ 工具设计半衰期未给具体可量化指标；⑤ 信任状态机 shadow → active 转换阈值未明
- **关联**：本摘要与原文 raw（80097 字节）/ wiki 编译页（≤8K）/ wiki digest（≤4K）配套
- **标签**： #主题/Agent架构 #主题/Harness工程 #主题/上下文管理 #主题/数据完整性 #主题/Action-Space #主题/企业级Agent #主题/Agent-OS #场景/Seetong借鉴 #作者/储旭 #作者/槿柏 #公众号/阿里妹 #公司/阿里巴巴