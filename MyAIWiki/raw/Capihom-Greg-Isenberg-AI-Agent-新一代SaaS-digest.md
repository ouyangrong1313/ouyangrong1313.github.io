# AI Agent 新一代 SaaS（Greg Isenberg） - Digest

## 一句话总结

Greg Isenberg 把"SaaS 卖软件"翻成"**Agent SaaS 卖工作**"——Agent 产品接住的不是软件 license，是一份原本由人完成的具体工作；找到已经存在工资单上的重复流程、旁听员工 10-20 次判断路径、做最小 Agent（批准/分流/协调/限定动作）、用控制台 + 评测建立信任、按 30 天计划先卖试点再沉淀产品。

## 核心观点 5 条

1. **商业模式根本转变**：SaaS 卖软件（工具），Agent SaaS 卖工作（结果）；demo 不是展示按钮，是展示"一通电话如何被接起，一个预约如何被创建，一条投诉如何被标记给经理"
2. **5 特征工作流筛选法**：发生频率高 / 清晰终点 / 接触现有软件 / 边界情况烦但能学 / 买方能感到损失
3. **甜点区** = 中间那块"重复 + 烦 + 一点判断"的活（避开太简单/太判断依赖两端）
4. **先旁听 10-20 次人类员工**——再写 prompt；Agent spec 7 件事（触发/上下文/工具/自主动作/批准点/真人升级/成功标准）
5. **最小 Agent 4 类**：批准型 / 分流型 / 协调型 / 限定动作型——按"先可预测路径 → 后动态决策"渐进

## 关键参数 / 决策树

| 选择 | 何时用 | 反例 |
|---|---|---|
| SaaS 模式 | 卖工具给团队用 | 接住一份工作 = 卖结果 |
| Agent SaaS 模式 | 接住一份已经存在工资单的工作 | 想做一个"大平台" |
| 甜点区（中间） | 重复 + 烦 + 一点判断 | 太简单（Zapier 吃掉）/ 太判断依赖（第一版会碎） |
| 旁听员工 | 写 prompt 前必做 | 直接开 prompt |
| 4 种最小 Agent | 第一版先做"批准/分流/协调/限定动作" | 一上来做"完全自主员工" |
| 控制台 + 评测 | 上线前必须可复查 | 炫技 demo |
| 价格：设置费 + 月费 | 早期简单收费 | 一上来就结果计费 |
| 试点 3 个客户 | 同细分行业、同 workflow、同痛点 | 跨行业试水 |
| Workflow teardown 内容 | 内容分发首选 | 通用 AI 营销 |

## 速查表：Agent spec 7 件事

| # | 项 | Greg 描述 |
|---|---|---|
| 1 | 触发器 | 什么触发它启动 |
| 2 | 上下文 | 需要哪些上下文 |
| 3 | 工具 | 能使用哪些工具 |
| 4 | 自主 | 可以自己完成哪些动作 |
| 5 | 批准 | 哪里必须拿批准 |
| 6 | 真人升级 | 什么时候升级给真人 |
| 7 | 成功 | 成功长什么样 |

## 速查表：4 种最小 Agent

| 类型 | 场景 | Greg 案例 |
|---|---|---|
| 批准型 | 创意 / 合规 / 金额风险 | 起草回复、报价、摘要 → 人批准 |
| 分流型 | 维修 / 账单 / 退款 / 线索入口 | 工单 → 正确地方 |
| 协调型 | 查日程 / 补材料 / 催进度 | 系统 ↔ 人之间协调 |
| 限定动作型 | 规则清楚 | "50 美元以下退款"、预约、跟进 |

## 速查表：30 天计划

| 天数 | 动作 |
|---|---|
| Day 1 | 选一个漏掉工作就会损失钱的行业 |
| Day 2 | 访谈 10 个运营者（共享屏幕跑一遍流程）|
| Day 3 | 选一个高频 + 有痛感 + 能接软件 + 有清晰成功标准的 workflow |
| Day 4 | 写 Agent spec（触发器/上下文/工具/规则/交接/评测）|
| Day 5 | 用 Claude/ChatGPT 手工跑，验证 AI 是否帮得上忙 |
| Day 6 | 做最小版本（批准或分流通常足够）|
| Day 7 | 用 50 个真实案例做 eval |
| Week 2 | 卖两个同一行业的试点 |
| Week 3 | 补 wrapper：日志 / 审批 / 设置 / 分析 / 交接 |
| Week 4 | 发布 workflow teardown，把试点变成证据 + 建受众 |

## 速查表：价格锚点

| 模式 | 价格 |
|---|---|
| 设置费 + 月费 | 1500 美元 + 1000 美元/月 / 一个 workflow |
| 设置费 + 单价 | 2000 美元 + 30 美元/合格预约 |
| 月费 + 票数 | 3000 美元/月 / 500 张处理票 |

## 核心金句 5 条

- "SaaS 卖软件，Agent SaaS 卖工作"
- "产品不是那个 Agent，产品是它接手的那份工作"
- "一个好 Agent，应该比初级员工更稳定，比外包更便宜"
- "在你开始写提示词、开始写代码之前，先旁听一个真正做这份工作的人"
- "先从一个可预测路径开始，只在判断能创造价值时再加入判断"
- "Agent 做工作，但 wrapper 创造信任"

## 关联图谱

### 上游（基于 / 来自）
- 传统 SaaS 商业模式（卖软件 license）
- Slang AI 等餐厅电话 Agent 产品案例
- Anthropic Agent 指南（workflow 先于 Agent）

### 下游（应用于 / 验证于）
- [[AI-Native企业-Agent团队和AI-Factory重写公司体系]] Groupon 视角（同样是"AI 时代企业落地"）
- [[Capihom-AI-Agent帮上门服务多接单-YC-Root-Access-Avoca]] Capihom 同主线（Avoca 上门服务 Agent）
- [[未来属于垂直领域Agent]] 垂直领域 Agent 路径印证
- [[Make-for-Agent-qi-shi-huan-shi-make-for-human]] 责任链 + 上下文基建
- [[Lilian-Weng-Harness-Engineering-自我改进]] Harness OS 类比 → Agent 接触现有软件
- [[Loop-Engineering-验证才是瓶颈]] 验证闸门 → Greg 控制台 + 评测
- [[Addy-Osmani-Loop-Engineering]] 5+1 积木 → Greg 4 种最小 Agent

### 同级（横向 / 并列）
- [[Capihom-OpenAI-Codex-Andrew-Ambrosino-产品工作新形态]] Capihom 同主线（Codex 产品工作）
- [[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] Anthropic 团队视角
- [[Multica-AI-Native-组织-人是最慢的节点]] 极端样本
- [[Leeka-Task-Decomposition-Agentic-Workflow]] 任务拆解视角
- [[小龙虾-OpenClaw-Agent价值与边界]] "什么时候选 Agent"

## 备注与限制

1. **原视频 YouTube URL 已确认**：https://www.youtube.com/watch?v=83fWzQSWB10
2. **Greg Isenberg 角色定位**：硅谷创业评论员 + Late Checkout 创始人，前 Reddit 战略；视角偏"硅谷 AI 创业方法论"
3. **Capihom 编译立场**：公众号定位"晚点再听LaterCast"，专注硅谷 AI 创业播客总结；本文是同主线第 N 篇编译
4. **价格锚点为美国市场**：1500/2000/3000 美元/月不直接适用于中国市场，但"设置费 + 月费 + 单价 + 票数"模式可参考
5. **30 天计划假定有 AI 编程能力**：第 5/6 天"用 Claude/ChatGPT 手工跑"+"做最小版本"对非开发者是难点
6. **不是入门文章**：本文假设读者已了解 Agent / SaaS / Eval 基础，适合 AI 产品方向思考者
7. **过度倾向"卖工作"**：本文极端主张 Agent 必须接住工作，忽略一些 Agent 工具型产品（Cursor/Codex 这种"卖工具但用户用来跑工作"的中间形态）
8. **workflow teardown 内容策略**：仅适合"老板每天能感到损失"的行业，复杂 B2B SaaS 不适用