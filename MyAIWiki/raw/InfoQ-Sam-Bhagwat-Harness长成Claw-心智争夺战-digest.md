# 所有Harness终将长成"龙虾"，但最后活下来的只有几只 - Digest

> 微信公众号「InfoQ」 / 编译 宇琪 / 策划 Tina
> 原文链接：https://mp.weixin.qq.com/s/oGya1dWy0iSUt1a-C4Q5mQ
> 一手来源：Sam Bhagwat（Mastra CEO & 联创，曾参与 Gatsby 构建）技术分享
> 原视频：https://www.youtube.com/watch?v=X0QgldlzB1E
> 获取时间：2026-07-19 15:51 Asia/Shanghai

## 一句话总结

Agent 演进光谱是 LLM → Agent → Harness → Claw 的 4 阶段——施泰因伯格定律：**任何 Harness 都会膨胀成 Claw**，但用户每品类只容纳 1-2 个 Claw，未来 AI 公司要抢的是用户心智空间，不是任务执行能力。

## 5 条核心观点

1. **Agentic 4 阶段光谱**：LLM → Agent（添加循环 + 工具调用 + 状态）→ Harness（添加规划 + 并行子 Agent + 非回合制）→ Claw（添加心跳 Cron + 订阅 + 多通道网关 + 持续学习）。
2. **Harness 核心竞争力**：规划模式 + 并行子 Agent + 动态子 Agent + Skill 系统 + Bash 后台 + 上下文自动压缩 + 线程持久化 + 插队中断能力——不再是"LLM 一回合你一回合"的下棋式交互。
3. **云端 Harness = Always-on**：云沙箱 + 移动端穿隧 + 直接 PR 推到 GitHub，关掉笔记本让 Agent 跑完睡觉。
4. **Claw 决定性配置 = 心跳 + 订阅 + 网关 + 持续学习**：自发创建新 Skill + 基于用户操作习惯微调既有 Skill。
5. **心智空间争夺战**：用户每品类只容纳 1-2 个 Claw（如同地图/打车/外卖），长期竞争重点是粘性 + 信任 + 使用习惯，不是任务执行速度。

## 关键数字

| 数字 / 案例 | 含义 |
|---|---|
| **4 阶段** | LLM → Agent → Harness → Claw |
| **几个月** | Claude Code 流行到"Harness 时代" |
| **每三十分钟醒来一次** | Claw 心跳 Cron 频率 |
| **一次给我跑二十个** | 用户需求推动 Harness 化的极限诉求 |
| **1-2 个 Claw / 品类** | 用户心智空间容量上限 |
| **OpenClaw、Hermes Agent** | Claw 阶段代表产品 |

## 5 关键金句

1. "一旦模型开始拥有工具调用、重试机制和状态持久化，它就告别了单次文本转换的原始阶段。"
2. "Claude Code 不同，你可以插队，可以掌舵，可以中途打断它，这完全是一种新的交互启示。"
3. "施泰因伯格定律：任何一副 Harness，只要它不被干掉，它就会不断吸收功能，直到最终膨胀成一只 Claw。"
4. "我们想要的，是一个私人的多巴胺赌场：我们在入口塞进一堆 Token，然后使劲摇，看它能给我们吐出什么产出。"
5. "现实世界里的普通人，脑子里能留出来的位置，只够塞下屈指可数的几只 Claw。"

## 3 反直觉点

1. **Agent 命名不是文字游戏**，是用户需求驱动的"自然进化"——工具越有用用户越希望它随时可用+后台+持续工作+主动行动，最终从"等待命令的开发工具"变成"长期存在的 Agent"。
2. **Harness 不是终点，是中间形态**——任何 Harness 都会"膨胀"成 Claw，施泰因伯格定律。
3. **AI 公司未来真正的竞争不是任务执行，而是用户心智空间争夺**——每品类只活 1-2 个，跑得慢不会被淘汰，跑得"用户记不住你"会被淘汰。

## 关联图谱

### 上游（基于 / 来自）
- **Harness 理论原典**：与 [[Lilian-Weng-Harness-Engineering-自我改进]] 同主线——本文"4 阶段光谱"对应翁荔"Harness 操作系统演进"的不同切片。
- **Routines 与 Cron 触发**：与 [[Claude-Code-主动式Agent-Routines]] 强关联——Routines = Claw 心跳雏形（按 cron/GitHub 事件/webhook 主动启动远程会话）。
- **动态 Harness Pattern**：与 [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]] 同主线——动态生成子 Agent + Skill 系统 = Harness 阶段关键配置。

### 下游（应用于 / 验证于）
- **企业 AI-Native 终极形态**：与 [[Capihom-AI-Native企业-Agent团队和AI-Factory重写公司体系]] 强关联——Groupon Masha 的 "AI Factory" 是企业内部 Claw 化（一个 AI Factory 跑全公司业务）。
- **Harness 产品化路径**：与 [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] 互补——本文"Claw 决定性配置 = 心跳 + 订阅 + 网关 + 持续学习"对应 WorkBuddy 产品的具体落地。

### 同级（横向 / 并列）
- **AI 终局形态预测三角**：本文 + [[未来属于垂直领域Agent]] + [[Make-for-Agent-qi-shi-huan-shi-make-for-human]]——三篇同主轴"未来 AI 的终极形态是什么样"：本文偏"个人 Claw 心智争夺" / 未来属于垂直领域 Agent 偏"垂直行业" / Make for Agent 偏"为 Agent 而建的世界"。
- **OpenClaw 同主线**：本文直接提名 OpenClaw 作 Claw 阶段案例，与 [[小龙虾-OpenClaw-Agent价值与边界]] 同主线——本文给 OpenClaw 阶段定位（Claw 终极形态），小龙虾给"该不该用 + 何时用 Agent"决策树，两者互为上下游。

## 备注与限制

- **一次创作结构**：InfoQ 编译 Sam Bhagwat 技术分享演讲，非 Sam 本人直接写作；视频 + 编译稿组合产出。
- **关键原语定义不完整**：施泰因伯格定律只给叙事，**未明确"Steinberger"致敬何人**（可能是 Sam 自创 / 致敬 Michael Steinberger / Pat Steinberger 待补证）。
- **OpenClaw 提名为 Claw 阶段案例**：原文直接提到 "OpenClaw、Hermes Agent" 作 Claw 阶段案例——这是 Seetong AI 助手当前格局对标。
- **演讲视频保留**：原视频 https://www.youtube.com/watch?v=X0QgldlzB1E 待复核是否存在 + 内容是否一致。
- **分类理由**：放 `01-ai-agents` 而非 `02-ai-coding` 或 `06-ai-tech`——本文是 Agent 演进理论 + 新原语 Claw 定义 + 终局形态，核心是 Agent 体系方法论，与 [[Lilian-Weng-Harness-Engineering-自我改进]] / [[Claude-Code-主动式Agent-Routines]] / [[未来属于垂直领域Agent]] / [[小龙虾-OpenClaw-Agent价值与边界]] / [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] 同主线"Agent 演进 + 终局形态 + 心智争夺"，且补完 01-ai-agents 偏"理论框架 + 企业实证 + 任务拆解"缺位的"产品视角 Agent 阶段光谱 + 心智空间争夺"维度。
