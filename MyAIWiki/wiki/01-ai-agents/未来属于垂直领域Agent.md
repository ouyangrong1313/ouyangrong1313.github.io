---
title: 未来属于垂直领域 Agent
category: 01-ai-agents
tags:
  - 主题/多Agent编排
  - 主题/Domain-Specific
  - 主题/企业Agent
  - 主题/Token经济
  - 主题/Harness
  - 主题/Seetong借鉴
nodes: composition-over-inheritance, 80%token效率, 2027编排年, 4大原语, 递归子Agent, 集成先卡, 工具堆叠反噬, 2026-token价格反转
links: [[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]], [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]], [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]], [[01-ai-agents/Capihom-AI-Agent帮上门服务多接单-YC-Root-Access-Avoca]]
date: 2026-07-03
source: 微信公众号「晚点再听LaterCast」2026-07-03 编译自 AI Engineer 大会 Justin Schroeder 演讲;原视频 https://www.youtube.com/watch?v=spNAUEgq_A8
---

# 未来属于垂直领域 Agent

- **原文链接**:https://mp.weixin.qq.com/s/PEoe-AuccFxXplyqoRmFNA
- **原视频**:https://www.youtube.com/watch?v=spNAUEgq_A8
- **演讲者**:Justin Schroeder(StandardAgents CEO / Dmux / ArrowJS 作者)
- **编译来源**:微信公众号「晚点再听LaterCast」2026-07-03 推送

## 核心结论

> 未来企业 Agent 不会沿着"一个大模型吃下所有工具"的路线长大,而会拆成一组更小、更专、更容易控制的 **domain-specific agents**——composition over inheritance 是企业 Agent 走向生产环境的必经之路。

- **场景**:企业 Agent 架构选型(单一巨型 → 多 Agent 编排)
- **核心命题**:composition over inheritance;小 Agent 不是工具服务器而是完整 Agent;2027 = 多 Agent 编排之年

## 知识节点(8 个独立概念)

- **composition-over-inheritance**:别给同一个 Agent 加说明书工具箱,拆 Figma/Gmail/Travel Agent 各管各的,上面放 coordinator 分派任务
- **80% token efficiency**:StandardAgents 内部数据——定义好任务边界后,单个任务 token 效率提升 80%+(Gmail Agent 查邮件不需要 Figma/报销/代码工具说明)
- **2027 编排年**:2026 H2 framework 多,2027 multi-agent orchestration 主流化;Vercel Eve 官网出现 company brain / personal assistant / domain-specific agent 词汇
- **4 大原语**:企业 Agent 必备——文件系统(每个 Agent 自己的小文件区)/ 沙盒执行 / hooks(注入时间/副作用)/ rules(回合数/验证/停止条件)
- **递归子 Agent**:销售团队案例 coordinator → Salesforce / Google Workspace / 素材生成 / 法务 → GDPR / OSHA(4 层递归,每个小 Agent 短上下文)
- **集成先卡**:能跑 demo 离生产还差 durable execution / 验证 / 停止条件——企业真正卡的不是模型智商
- **工具堆叠反噬**:5 个 skills 还能忍,50+ / 100+ / 1000+ 后延迟 / 费用 / 误调用 / 权限风险一起涨;研究证明 skills 装太多 Agent 明显变差
- **2026 token 价格反转**:IQ 调整后 +29% / 不调整 +76%——巨型模型单次费用开始把"放到客户面前"的场景挡在门外

## 关联图谱

- **上游**:软件工程 composition over inheritance / NASA 阿波罗登月专家+消息协同 / Vercel AI SDK & Eve
- **下游**:2026 H2 domain-specific agent 框架爆发 / 2027 multi-agent orchestration 主流 / 销售/法务/客服递归子 Agent
- **同级**:[[01-ai-agents/Leeka-Task-Decomposition-Agentic-Workflow]](怎么拆)/ [[01-ai-agents/阿里妹-端到端业务需求专家Agent-4层架构8步流程]](4 层 8 步)/ [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]](Harness 14 步)/ [[01-ai-agents/小龙虾-OpenClaw-Agent价值与边界]](不存在通用 Agent)/ [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]](4 人+几十 Agent 极端样本)/ [[01-ai-agents/Capihom-AI-Agent帮上门服务多接单-YC-Root-Access-Avoca]](垂直行业商业化)

## 正文要点(5 条)

**1. 集成先卡 / 模型智商排后**——能跑 demo 离生产还差 provider abstractions / durable execution / 验证 / 停止条件;Vercel AI SDK / Eve 正为这些而生。

**2. 工具堆叠的反噬**——5 个 skills 还能忍,50+ 后主 Agent 每次带着一整包无关材料;用户问"安排洛杉矶行程",Agent 背着 Figma/差旅/报销/React lint/GitHub skill 上路。**Inheritance 路径在 Agent 时代翻车。**

**3. composition over inheritance**——NASA 阿波罗类比:一组专家各掌握有限工具,大脑像 LLM,面板按钮像 tools,嘴巴负责 messages。Figma Agent 只懂 Figma;Gmail Agent 只处理邮件;coordinator 像团队主管分派任务。**小 Agent 不是只暴露工具的服务器——它是完整 Agent,有自己的消息历史和循环。**

**4. 80% token efficiency + token 反转**——StandardAgents 内部数据:任务边界后 token 效率 +80%。叠加 2026 token 反转(IQ 调整 +29% / 不调整 +76%),窄域拆分让团队把高价模型留给少数难题,把确定动作交给小模型/工具函数/子 Agent——少花钱也少暴露权限。

**5. 2027 = 多 Agent 编排之年**——4 大原语(文件系统/沙盒执行/hooks/rules)是每个 Agent 必备的"小执行环境";递归子 Agent(销售团队 4 层:coordinator→4 子 Agent→法务下再拆 GDPR/OSHA)给企业落地画了具体图。**"别急着给一个大 Agent 继续加工具——把边界缩小,成本/权限/稳定性问题会提前浮出来。**

### 6 个对 Seetong 团队可借鉴动作

1. **Seetong AI 助手按 domain-specific 拆**:5 个小 Agent(设备分诊/反馈分诊/远程操作/添加设备/报警处理)而非 1 个 Mega Agent 背所有 SOP
2. **递归子 Agent 用在报警处理**:报警 Agent 下再拆 禽类/畜类/车/人 4 个小子 Agent(对照 7-02 1007107 BUG 修复)
3. **客服 SOP 拆 Skill + Agentic Workflow**:每条 SOP 独立成小 Agent,CoAgent 自然语言分发
4. **hooks + rules 4 大原语落地**:高风险操作(设备解绑/远程开门/超 N 元支付)→ hard-gate 人工 Approve
5. **Token 成本预警**:按"明年涨 1.5x"准备预算(不是降)——如果不拆 Agent,剩余 20% 固定开销会随 token 单价上涨而恶化
6. **集成先做 MCP 标准化**:内部系统(设备/反馈/工单/Logan/神策/友盟)按 MCP 接入,每个子 Agent 只挂需要的

## 备注与限制

- 80% / 137 倍 / 29% / 76% 等数据均来自 StandardAgents 内部口径,未独立验证
- "2027 编排年"是演讲者判断,非第三方数据;Vercel Eve 官网词汇是早期信号
- 小 Agent 完整定义(有 system prompt/工具/消息历史/agentic loop)与一般 MCP server 区别在"是否有消息历史和循环"
- 销售团队 4 层递归案例未必适合所有业务——Seetong 报警处理建议 2 层,可能 3 层封顶
- 补完 01-ai-agents 现有"Harness/Loop/端到端/任务拆解/AI Native 组织"主线缺位的"多 Agent 编排具体形态"维度
- 作者立场:Justin Schroeder 是 StandardAgents CEO,工具栈偏早期生态
- **原视频**:https://www.youtube.com/watch?v=spNAUEgq_A8
