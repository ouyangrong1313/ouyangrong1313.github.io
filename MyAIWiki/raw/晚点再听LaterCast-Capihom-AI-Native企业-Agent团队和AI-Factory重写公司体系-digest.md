# AI-Native 企业（Augmented U · Masha Sharma / Groupon VP）— 原文摘要

> 一句话总结：**AI-native 公司不是"加了 AI 的公司"，是先改组织图、再配 truth layer 与 eval 的公司——任务交给 Agent，人负责指挥和审阅；先让一个小循环跑起来，比开会先定完整方案重要得多。**

## 5 大核心观点

1. **AI-native 先改组织图**——任务从人执行改成"Agent 执行 + 人指挥/审阅"，每个职能都要能通过 Agent 构建；提案必须带输入样例、输出样例、失败场景、评估指标（"只带一个需求标题已经不够"）
2. **每个职能都要能动手搭 Agent**——销售能搭 lead research 仪表盘、PM 能直接问代码有没有 hard-code；非工程同事通过 speedboat 2-3 人小队与工程结对 ship 到 staging；build vs buy 倾向自建小版本（"基础设施可以买，能形成 unfair advantage 的业务环节要自己建，尤其是 eval"）
3. **Truth layer 决定 Agent 能不能进生产**——每个类别（如激光脱毛、按摩）由对应领域的业务专家维护权威 source of truth；category playbook 转成 AI-readable manifests；deal 表现能追到 playbook 里的某次具体编辑
4. **Eval 把每条生成结果接回业务规则**——每段 pipeline 都要被评估（确定性规则 + 概率性判断 + 回流循环）；上线分两阶段（早期开放学习 pattern match → 后期划门槛决定哪些指标允许全自动）；Groupon 跑 weekly quality control agents
5. **领导者先搭自己的工作操作台**——Masha 自己建了 stakeholder/strategy/vision/metrics/source of truth/direct reports/决策记录 7 维 OS；不逐封读邮件，Agent 按月/周优先级排序后给结论；高管 PM 运营销售必须自己用 AI（"不要把理解 AI 的责任委托给 AI 团队"）

## 关键金句（5 句）

> "AI 原生意味着，工作由 Agent 完成，人类负责指挥和审阅。"

> "成为 builder，不是 vibing 一个原型然后放在那里。成为 builder，意味着你要 ship。"

> "我们为每个类别建立了权威 source of truth，比如激光脱毛或按摩，由对应服务领域的专家来维护。"

> "我们把 insight 按服务层级聚合和量化，然后就能看到：Reiki massage 这里我们偏得很厉害。"

> "不要把你对 AI 的理解委托给团队。"

## 5 个关键数字 / 案例

| 数字 / 案例 | 内容 |
|---|---|
| **2027 目标** | Groupon 承诺到 2027 年成为 AI-native 公司 |
| **10 亿美元估值** | Masha 此前在 Avenue One 把公司做到 10 亿美元估值（团队背景） |
| **几分钟上线** | 材料齐全的小商家从"有活动想法"到"活动已上线"只需几分钟 |
| **20 种服务 + 60 个 deal** | 按摩类别评估方法：20 种服务 → 生成 60 个 deal 看上下文捕捉 |
| **Reiki massage 偏得厉害** | eval 暴露 Reiki massage 类规则漏洞的标志性案例 |

## 3 个反直觉点

1. **AI-native 公司先改的不是产品，是组织图**——Masha 的做法是"先把组织图改对，再用 Agent 把执行搬过去"，而不是反过来的"先把产品加了 AI，再看组织怎么调"
2. **eval 修的不是 prompt，是 source of truth**——Groupon 牙齿美白 eval 暴露的不是模型不会，是 playbook 只覆盖了一种交付方式；"修的是源头，后面生成、推荐、质控才会一起对齐"
3. **高管自己用 AI 才是 AI 团队最好的训练**——Masha 自己的 OS 是先搭出来，团队才跟上；"高管、PM、运营、销售如果只等别人做培训，很快会看不懂自己公司的新生产方式"

## 关联图谱

- **上游**：与 [[未来属于垂直领域Agent]] 同公众号主线，但本文是"Groupon 一家企业实证"，未来属于垂直领域 Agent 是"未来形态预测"
- **下游**：本文产出 8 个独立知识节点 + 6 个 Seetong 借鉴动作；详见 wiki 编译页
- **同级**：与 [[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] 同"AI Native 团队/组织图"主题——本文 Groupon 实证 + Fiona Anthropic 实证对照
- **关联**：与 [[ThinkingAgent-Knock-AI-Native组织5级成熟度模型]] 强关联——本文是 L3-L4 阶段的"Groupon AI Factory 实证"

## 备注与限制

- 原文约 4000 字（清洗后 5735 字符），已是中文编译浓缩稿；最完整信息源为 Augmented U 原视频 https://www.youtube.com/watch?v=pQj8qOyan-Q （微信公众号只浓缩无日期标注）
- Masha Sharma 是 Groupon VP of Engineering，工程师 + 产品 + CTO + 创始人背景；本文未给具体营收/团队规模数字，所有数据来自她本人口述无第三方验证
- 评估方法（每类 20 服务 × 3 deal = 60 deal 评估）是 Groupon 内部实践，未标准化成可复用模板
- **已知限制**：本文偏"工程主管视角"未触及一线员工体验；"每个职能都能构建"在 Groupon 这种 1 万+ 员工公司可行，Seetong 30-50 人团队不能直接套
- 公众号"晚点再听LaterCast"未提供具体推送时间（og:description 无时间戳），按微信公众号抓取时间 2026-07-07 11:27 推断

## 6 个对 Seetong 借鉴动作（速查）

| # | 动作 | 来源论点 |
|---|---|---|
| 1 | **AI-native 组织图体检**——Seetong 当前组织图哪些岗位其实是"指挥 Agent"而不是"亲自做"，哪些还是"业务提需求-工程写 PRD"老链路 | "AI-native 先改组织图" |
| 2 | **每个职能都能搭 1 个最小 Agent**——客服/产品/测试/运营 各 1 个 Skill，1 周 ship 到 staging（哪怕只是 60% 完成度） | "每个职能都要能动手搭 Agent" |
| 3 | **小商家上线路 AI 化**——Seetong 设备添加流程从"填 5 张表"到"对话一句话"——MCP 标准化 + 设备配网知识库 + 1 次性评估合规 | "几分钟从想法到上线 campaign" |
| 4 | **Truth layer 沉淀**——Seetong 设备配置/报警规则/反馈分类的 source of truth 由张威+各产品线 owner 维护 → AI-readable manifests | "Truth layer 决定 Agent 能不能进生产" |
| 5 | **Eval 接回业务规则**——Seetong 设备分诊/反馈分诊 eval suite，验收=该分到正确类别（"中医把脉 vs 误诊"），每周跑 quality control agents | "Eval 把生成结果接回业务规则" |
| 6 | **主人先搭自己的 OS**——7 维（stakeholder/strategy/vision/metrics/sot/direct reports/决策记录），主人月报加"上周 AI 做的决策数 vs 主人亲自做的决策数" | "领导者先搭自己的工作操作台" |

## 6 个最强相关 wiki 条目

1. [[未来属于垂直领域Agent]] — 同公众号"晚点再听LaterCast"主线，本文是企业实证，那篇是未来形态预测
2. [[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] — 同"AI Native 团队/组织图"主题（Groupon 实证 vs Anthropic 实证）
3. [[ThinkingAgent-Knock-AI-Native组织5级成熟度模型]] — 本文是 Knock 5 级模型中 L3-L4 阶段的"Groupon AI Factory 实证"
4. [[Multica-AI-Native-组织-人是最慢的节点]] — 主流大厂样本（Groupon/Anthropic）vs 极端样本（Multica 4 人+几十 Agent）
5. [[Laurel-CPO-Jiaona-Zhang-公司OS]] — 同样是"公司 OS"视角，Laurel 给方法，本文给实证
6. [[Addy-Osmani-Loop-Engineering]] — 本文"小循环先跑起来"对应 Addy Loop 5+1 积木最小可用版