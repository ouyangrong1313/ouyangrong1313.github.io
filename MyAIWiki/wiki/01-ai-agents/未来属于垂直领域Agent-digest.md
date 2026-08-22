---
title: 未来属于垂直领域 Agent - Digest
category: 01-ai-agents
type: digest
date: 2026-07-03
source: 微信公众号「晚点再听LaterCast」编译自 AI Engineer 大会 Justin Schroeder 演讲
tags:
  - 主题/未分类
nodes: []
---

# 未来属于垂直领域 Agent - Digest

> 未来企业 Agent 不会沿着"一个大模型吃下所有工具"的路线长大,而会拆成一组更小、更专、更容易控制的 **domain-specific agents**——composition over inheritance。

## 8 节点速查表

| # | 节点 | 一句话 |
|---|---|---|
| 1 | composition-over-inheritance | 别给同一个 Agent 加说明书,拆 Figma/Gmail/Travel Agent 各管各的 |
| 2 | 80% token efficiency | 任务边界后 token 效率 +80%+(StandardAgents 内部数据) |
| 3 | 2027 编排年 | 2026 H2 framework 多,2027 multi-agent orchestration 主流化 |
| 4 | 4 大原语 | 文件系统 / 沙盒执行 / hooks / rules 是企业 Agent 必备 |
| 5 | 递归子 Agent | coordinator→4 子 Agent→法务下再拆 GDPR/OSHA(销售 4 层) |
| 6 | 集成先卡 | 能跑 demo 离生产还差 durable execution / 验证 / 停止条件 |
| 7 | 工具堆叠反噬 | 5 个 skills 还能忍,50+ 后延迟/费用/误调用/权限一起涨 |
| 8 | 2026 token 价格反转 | IQ 调整后 +29% / 不调整 +76%(intelligence cost 不再降) |

## 关键数字

- **80%** token 效率(任务边界后)
- **137 倍** 单任务成本差(DeepSeek V4 Flash vs Fable 5)
- **+29% / +76%** 2026 token 价格上涨(IQ 调整后 / 不调整)
- **5+** skills 后收益开始递减(50+ 后明显变差)
- **4 层** 递归子 Agent(销售团队:coordinator→4 子 Agent→法务下再拆)

## 5 句金句 + 3 个反直觉点

**5 句核心金句**:"**2027 年,基本上会是多 Agent 编排之年。**"/ "**Token 已经不再变便宜了。**"/ "**Agent 是确定性软件,它把模型产生的非确定性结果,用在某个目标上。**"/ "**我们不是靠给一个人一堆工具,把送上月球的。**"/ "**组合是继承的替代方案。**"

**3 个反直觉点**:集成是生产环境第一关不是模型智商 / Skills 越多 Agent 越差(50+ 后模型在不相干规则间切换)/ 小 Agent 不是只暴露工具的服务器——是完整 Agent,有自己的消息历史和循环

## 6 个对 Seetong 借鉴动作

1. **Seetong AI 助手按 domain-specific 拆**:5 个小 Agent(设备分诊/反馈分诊/远程操作/添加设备/报警处理)而非 1 个 Mega Agent
2. **递归子 Agent 用在报警处理**:报警 Agent 下再拆 禽类/畜类/车/人 4 个小子 Agent(对照 7-02 1007107 BUG 修复)
3. **客服 SOP 拆 Skill + Agentic Workflow**:每条 SOP 独立成小 Agent,CoAgent 自然语言分发
4. **hooks + rules 4 大原语落地**:高风险操作(设备解绑/远程开门)→ hard-gate 人工 Approve
5. **Token 成本预警**:按"明年涨 1.5x"准备预算,不要按"降"准备
6. **MCP 标准化**:内部系统(设备/反馈/工单/Logan/神策/友盟)按 MCP 接入,每个子 Agent 只挂需要的

## 备注

- 80% / 137 倍 / 29% / 76% 数据均来自 StandardAgents 内部口径,未独立验证
- "2027 编排年"是演讲者判断,非第三方数据;Vercel Eve 官网词汇是早期信号
- 与 Leeka"任务拆解"+ 小龙虾"不存在通用 Agent" 形成"拆什么 + 怎么拆 + 何时拆"完整三角
- 补完 01-ai-agents 主线缺位的"多 Agent 编排具体形态"维度
