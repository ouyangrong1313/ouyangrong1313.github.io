# InfoQ - 所有 Harness 终将长成"龙虾"（Digest）

> 微信公众号「InfoQ」 / 编译 宇琪 / 一手 Sam Bhagwat Mastra CEO
> 原文链接：https://mp.weixin.qq.com/s/oGya1dWy0iSUt1a-C4Q5mQ
> 编译：2026-07-19

## 一句话

Agent 演进是 LLM → Agent → Harness → Claw 的 4 阶段光谱——施泰因伯格定律要求任何 Harness 都膨胀成 Claw，但用户每品类只容纳 1-2 个 Claw，未来 AI 公司要抢的是用户心智空间。

## 8 节点速查表

| 节点 | 一句话定义 | 关键数字 / 案例 |
|---|---|---|
| Agentic 4 阶段光谱 | LLM → Agent → Harness → Claw，应用逐阶段积累特性 | OpenClaw / Hermes Agent 是 Claw 阶段 |
| LLM-Agent 界限 = 循环 | 工具调用 + 重试 + 状态持久化让 LLM 告别单次文本转换 | 2025 七 / 八月业内开始流行上下文工程 |
| Harness 核心竞争力 | 规划 + 并行子 Agent + 非回合制 + Skill + 上下文压缩 | Claude Code / Codex 是典型 Harness |
| 云端 Harness = Always-on | 云沙箱 + 移动端 + 直接推 PR，让 Agent 全勤在线 | Devin 活在 Slack / 推 PR 到 GitHub |
| Claw 决定性配置 | 心跳 Cron + 订阅 + 多通道网关 + 云端记忆 | **每三十分钟**心跳醒来 |
| Claw 持续学习 | 自发捏造新 Skill + 用户行为微调既有 Skill | 越做越溜 |
| 施泰因伯格定律 | 任何 Harness 都会不断吸收功能直到膨胀成 Claw | 多巴胺赌场 / Token 入 → 结果出 |
| 心智空间争夺战 | 用户每品类只容纳 1-2 个 Claw，长期竞争是粘性 + 信任 + 习惯 | 地图 / 打车 / 外卖每品类最终只活 1-2 个 |

## 5 关键金句

1. "一旦模型开始拥有工具调用、重试机制和状态持久化，它就告别了单次文本转换的原始阶段。"
2. "Claude Code 不同，你可以插队，可以掌舵，可以中途打断它，这完全是一种新的交互启示。"
3. "施泰因伯格定律：任何一副 Harness，只要它不被干掉，它就会不断吸收功能，直到最终膨胀成一只 Claw。"
4. "我们想要的，是一个私人的多巴胺赌场。"
5. "现实世界里的普通人，脑子里能留出来的位置，只够塞下屈指可数的几只 Claw。"

## 3 反直觉点

1. **Agent 命名不是文字游戏**，是用户需求驱动的"自然进化"——工具越有用用户越希望它随时可用 + 后台 + 主动。
2. **Harness 不是终点，是中间形态**——任何 Harness 都会"膨胀"成 Claw。
3. **AI 公司未来真正的竞争不是任务执行，而是用户心智空间争夺**——"用户记不住你"会淘汰。

## 5 个对 Seetong 可借鉴动作

1. **把 Seetong AI 助手定位 Claw 阶段**：已有心跳 / 订阅 / Skill 系统雏形，按 4 阶段光谱自查当前在哪一段。
2. **Skill 库持续学习**：微调既有 Skill（自动调整反馈分诊阈值 / crash 看板优先级）。
3. **多通道网关延展**：不止 OpenClaw Web / CLI，未来延展微信小程序 / 桌面小组件 / 邮件订阅。
4. **内部心智空间抢占**：先喂满现有 Seetong AI 助手再起新 Agent，避免内部功能分裂。
5. **听用户需求驱动进化**：用户没说"能不能跑二十个"前别自己加并行功能。

## 备注与限制

- **一次创作结构**：InfoQ 编译 Sam Bhagwat 技术分享演讲，非 Sam 本人直接写作。
- **关键原语定义不完整**：施泰因伯格定律未明确"Steinberger"致敬何人，**待补证**。
- **OpenClaw 提名为 Claw 阶段案例**：原文直接提到 OpenClaw、Hermes Agent——与 Seetong AI 助手格局直接对标。
- **Mastra 私心**：Sam 作为 Mastra 创始人，演讲有"框架推销"私心。
- **分类理由**：放 `01-ai-agents`——本文是 Agent 演进理论 + 新原语 Claw 定义 + 终局形态，与 [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] / [[02-ai-coding/Claude-Code-主动式Agent-Routines]] / [[01-ai-agents/未来属于垂直领域Agent]] 同主线。
