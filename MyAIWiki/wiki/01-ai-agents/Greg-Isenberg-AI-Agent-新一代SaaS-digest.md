# Greg Isenberg AI Agent 新一代 SaaS - Digest

## 一句话总结

Greg Isenberg 把"SaaS 卖软件"翻成"**Agent SaaS 卖工作**"——Agent 产品接住的不是软件 license，是一份原本由人完成的具体工作；找到已经存在工资单上的重复流程、旁听员工 10-20 次判断路径、做最小 Agent（批准/分流/协调/限定动作）、用控制台 + 评测建立信任、按 30 天计划先卖试点再沉淀产品。

## 5 段核心论证（速查表）

| 段 | 主题 | 关键命题 | 关键数据/概念 |
|---|---|---|---|
| 1 | 产品定义 | SaaS 卖软件，Agent SaaS 卖工作 | 餐厅电话 / 维修调度 / 客服退款 / 物业分派 |
| 2 | 工作流筛选 | 5 特征 + 20 工作清单 + 5 维打分 | 频率/清晰终点/接触软件/边界可学/买方感到损失 |
| 3 | 旁听员工 | 先旁听 10-20 次再写 prompt | Agent spec 7 件事（触发/上下文/工具/自主/批准/真人/成功）|
| 4 | 最小 Agent | 4 种第一版（批准/分流/协调/限定动作）| Anthropic 指南：workflow 先于 Agent |
| 5 | 信任 + 30 天计划 | 控制台 + 评测 + 试点 3 客户 + teardown 内容 | 1500+1000 / 2000+30 / 3000+500 三种价格锚点 |

## 8 节点速查

1. **SaaS 卖工作** = 商业模式根本转变
2. **5 特征工作流筛选** = 频率/清晰/软件/边界/损失
3. **甜点区** = 中间那块"重复+烦+一点判断"
4. **旁听员工 10-20 次** = 写 prompt 前必做
5. **Agent spec 7 件事** = 触发/上下文/工具/自主/批准/真人/成功
6. **4 种最小 Agent** = 批准/分流/协调/限定动作
7. **控制台+评测** = wrapper 创造信任
8. **30 天试点计划** = Day 1-7 + Week 2-4

## 6 句关键金句

- "SaaS 卖软件，Agent SaaS 卖工作"
- "产品不是那个 Agent，产品是它接手的那份工作"
- "一个好 Agent，应该比初级员工更稳定，比外包更便宜"
- "在你开始写提示词、开始写代码之前，先旁听一个真正做这份工作的人"
- "先从一个可预测路径开始，只在判断能创造价值时再加入判断"
- "Agent 做工作，但 wrapper 创造信任"

## 3 个反直觉点

- 产品不是 Agent 而是 Agent 接手的那份工作（不是 demo 漂亮，是工作稳定）
- 甜点区不是"完全自主"，是"中间那块重复 + 烦 + 一点判断"（避开太简单和太判断依赖）
- 旁听员工比写 prompt 重要（顺序/小动作/判断路径才是真规则）

## 5 关键数字

- **5 特征** = 工作流筛选（频率/清晰/软件/边界/损失）
- **20 个工作** = 选行业后列清单
- **10-20 次** = 旁听员工数
- **7 件事** = Agent spec
- **4 种最小 Agent** = 批准/分流/协调/限定动作

## 6 个对 Seetong 团队可借鉴动作

| # | 借鉴动作 | 对应节点 |
|---|---|---|
| 1 | 列出 Seetong 内部 20 个重复工作 → 5 维打分选最小 Agent 切入点 | 5 特征 + 20 工作 |
| 2 | 客服"接住整份工作"路线图（接电话 → 接反馈+派单+回访）| SaaS 卖工作 |
| 3 | 销售/产品旁听 10-20 次录屏 → 拆解判断路径 | 旁听员工 |
| 4 | Seetong AI 助手最小 Agent 选型（推荐分流型：反馈分诊）| 4 种最小 Agent |
| 5 | Seetong Agent spec 7 件事模板写入 skill.md 顶部 | spec 7 件事 |
| 6 | Seetong 控制台 + 评测（"今日处理 N 条 + 转人工率 Y%"）| 控制台评测 |

## 强关联（同主线 6 个）

- [[01-ai-agents/AI-Native企业-Agent团队和AI-Factory重写公司体系]] Groupon 实证
- [[01-ai-agents/Capihom-AI-Agent帮上门服务多接单-YC-Root-Access-Avoca]] Capihom 同主线
- [[02-ai-coding/Capihom-OpenAI-Codex-Andrew-Ambrosino-产品工作新形态]] Capihom 同主线（产品工作）
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] Harness OS
- [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] 验证闸门 → 评测
- [[02-ai-coding/Addy-Osmani-Loop-Engineering]] 5+1 积木 → 4 种最小 Agent

## 备注与限制

- 原视频已确认：https://www.youtube.com/watch?v=83fWzQSWB10
- Greg Isenberg 视角偏"硅谷 AI 创业方法论"
- Capihom 是同主线编译（晚点再听LaterCast）
- 价格锚点 1500-3000 美元/月是美市场
- 30 天计划假定有 AI 编程能力
- 过度倾向"卖工作"，忽略 Agent 工具型产品（Cursor/Codex 这种）