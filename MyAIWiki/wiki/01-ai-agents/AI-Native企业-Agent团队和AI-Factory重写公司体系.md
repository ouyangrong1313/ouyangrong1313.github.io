---
title: AI-Native 企业：Agent 团队和 AI Factory 会怎么重写公司体系
category: 01-ai-agents
tags:
  - 主题/AI-Native
  - 主题/Agent落地
  - 主题/组织变革
  - 主题/Truth-Layer
  - 主题/Eval
  - 主题/企业AI
  - 手法/案例拆解
  - 手法/方法论
  - 场景/企业级落地
  - 场景/编译长文
nodes: [AI-native组织图, 每个职能都能构建, speedboat小队, build-vs-buy倾向自建, Truth-layer, Category-playbook-manifest, eval回流业务规则, 自主Agent规模双刃剑, 领导者自搭OS, 高管必须自己用AI]
links: [[01-ai-agents/未来属于垂直领域Agent]] [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] [[01-ai-agents/ThinkingAgent-Knock-AI-Native组织5级成熟度模型]] [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]] [[03-productivity/Laurel-CPO-Jiaona-Zhang-公司OS]] [[02-ai-coding/Addy-Osmani-Loop-Engineering]]
date: 2026-07-07
source: 微信公众号「晚点再听LaterCast」2026-07-07 推送（编译自 Augmented U 节目《Building the AI-Native Enterprise》/ 受访 Masha Sharma Groupon VP / 原视频 https://www.youtube.com/watch?v=pQj8qOyan-Q）
---

# AI-Native 企业：Agent 团队和 AI Factory 会怎么重写公司体系

## 核心结论（一句话）

> **AI-native 公司不是"加了 AI 的公司"，是先改组织图、再配 truth layer + eval 的公司——任务交给 Agent 执行，人负责指挥和审阅；先让一个小循环跑起来，比开会先定完整方案重要得多。**

## 分类提炼

- **场景**：企业级 AI 落地 / 组织变革 / AI Factory 实证
- **标签**：AI-Native / 组织图 / Truth Layer / Eval / Agent Crew / 企业落地
- **类型**：编译长文（Augmented U 节目浓缩）+ 一手访谈（Masha Sharma / Groupon VP）

## 知识节点（8 个独立概念）

### 1. AI-native 先改组织图（不是先改产品）

Groupon **2027 AI-native 时间表**——核心是"任务开始交给 Agent 执行，人负责指挥和审阅"。最容易被低估的 AI 变化不在模型发布会，而在组织内部——一个销售能不能自己搭 lead research 仪表盘、一个 PM 能不能直接问代码"这里有没有 hard-code"。**提案必须带输入样例、输出样例、失败场景和评估指标 4 件套**——"只带一个需求标题已经不够"。

### 2. 每个职能都要能动手搭 Agent（speedboat 模式）

非工程补 AI 能力的路径不是"上培训课"，是"放到能触达的位置"：训练资源、模型访问、共享 connector、MCP、Claude CoWork/Design/Code 全下沉到一线。具体执行是 **speedboat 模式**——业务 + 工程 2-3 人小队一起搭、一起集成、一起上线。她团队里的 PM 和 UX designer 现在至少都能 ship 到 staging。**"成为 builder，不是 vibing 一个原型然后放在那里。成为 builder，意味着你要 ship。"**

### 3. Build vs Buy 倾向自建（eval 不能外包）

过去 Masha 倾向先买、先把流程跑通再自建。**现在反过来**：采购、测试、流程都要时间，自建小版本反而更快更便宜。**"基础设施可以买，能形成 unfair advantage 的业务环节要自己建，尤其是 eval，那一层不能外包。"** ——eval 是企业的判断力护城河，不能交给 SaaS。

### 4. Truth Layer 决定 Agent 能不能进生产（业务专家写规则）

企业卡在 pilot → production 的真正原因不是模型不聪明，是 **Agent 不知道按哪套知识行动**。Groupon 把这层基础叫 **truth layer**——每个类别（激光脱毛、按摩等）由对应服务领域的**业务专家**维护权威 source of truth，做成 **AI-readable manifests**（category playbook）。关键设计：**谁拥有真相，谁维护真相**——类别经理不能只讲一次就放手，必须持续写规则；deal 表现能追到 playbook 里某次具体编辑，错了能回源头改。

### 5. Eval 把每条生成结果接回业务规则（双阶段上线）

Groupon 的 eval 体系 3 特征：①**确定性规则 + 概率性判断 + 回流循环** 三组合 ②**按服务层级聚合 insight**（按摩 20 种服务生成 60 个 deal 看上下文捕捉；eval 暴露"Reiki massage 偏得厉害"，立刻定位到 playbook 哪条规则）③**双阶段上线**——早期系统保持开放让团队学习 pattern match，学到足够多后才划门槛（什么指标触发 human review，什么允许全自动）。Groupon 还跑 **weekly quality control agents** 持续监测。

### 6. 自主 Agent 的规模双刃剑（blast radius）

**自主 Agent 的吸引力来自规模，风险也来自规模**。后台建议错了 = 内部返工；面向商家/消费者的自动决策错了 = 收入、信任、合规全部受损。Groupon 用**小比例 customer rollout 控制 blast radius**——换学习速度，守住客户信任。**先让系统暴露错误，再用门槛决定什么时候放手，最后才扩大自动化比例**——这与 Addy Loop "先仪表化再去扩循环"是同一思路的企业级版。

### 7. 领导者先搭自己的工作 OS（高管自己用 AI）

Masha 一年前还很保守（讨厌"经验不足的人把 thinking 外包给 AI"），现在她变了——**因为她先搭了自己的 operating system**：stakeholder、strategy、vision、metrics、source of truth、direct reports、决策记录 7 维全部持续进入她的知识库。她不逐封读邮件、不逐条读 Asana，信息先进入 Agent，按月/周策略排序给结论；外部知识（新工具、Claude 变化、GitHub trending repo）也先被 Agent 带回来再判断是否有用。她**直接问代码"这里怎么运行"**，四周自己写了 2-3 张 code audit tickets。

### 8. 高管必须自己用 AI（不要委托给 AI 团队）

**"不要把理解 AI 的责任委托给 AI 团队"**——高管、PM、运营、销售如果只等别人做培训，很快会看不懂自己公司的新生产方式。最好的训练方式是**自己搭一个小系统，让 Agent 读你的材料、理解你的目标、帮你完成一个真实任务**。

## 关联图谱

**上游**：[[01-ai-agents/未来属于垂直领域Agent]]（同"晚点再听LaterCast"，那篇是"未来形态预测"，本文是"Groupon 企业实证"）+ [[02-ai-coding/Addy-Osmani-Loop-Engineering]] Loop 5+1 积木（本文"先跑小循环"对应 Loop 最小可用版）+ [[03-productivity/Laurel-CPO-Jiaona-Zhang-公司OS]]（同样是"公司 OS"视角，Laurel 给方法，本文给实证）

**同级**：[[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]]（Anthropic 管理者视角）+ [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]（极端样本）+ [[01-ai-agents/ThinkingAgent-Knock-AI-Native组织5级成熟度模型]]（L3-L4 数据框架，本文是 Groupon 实证）+ [[01-ai-agents/Capihom-AI-Agent帮上门服务多接单-YC-Root-Access-Avoca]]（同 Capihom 编译系列）

## 5 个核心主张 + 操作

**主张 1**：AI-native 公司先改的不是产品，是组织图
操作：Seetong 画组织图，把每个岗位标"指挥 Agent"还是"亲自做"，找出 5 个还是"业务提需求-工程写 PRD"老链路的岗位

**主张 2**：每个职能都能搭 1 个最小 Agent（speedboat）
操作：客服/产品/测试/运营各 1 个最小 Skill，1 周 ship 到 staging（哪怕 60% 完成度）

**主张 3**：Truth Layer 是 Agent 进生产的瓶颈（eval 不能外包）
操作：设备配置/报警规则/反馈分类的 source of truth 由张威+各产品线 owner 维护 → AI-readable manifests

**主张 4**：Eval 是企业的护城河，不能外包
操作：设备分诊/反馈分诊 eval suite，验收=该分到正确类别，每周跑 quality control agents

**主张 5**：高管自己用 AI 是新素养
操作：主人月报加"上周 AI 做的决策数 vs 主人亲自做的决策数"指标对齐 Masha 模式

## 6 个对 Seetong 借鉴动作

1. **AI-native 组织图体检**——找出 5 个还是"业务提需求-工程写 PRD"老链路的岗位；主人+黄松佳+谭伟+张威共同标出待改节点
2. **每个职能搭 1 个最小 Agent**——客服/产品/测试/运营各 1 个 Skill（哪怕 60%），1 周 ship 到 staging；速度比完美重要
3. **小商家上线路 AI 化**——设备添加从"填 5 张表"到"对话一句话"，MCP 标准化 + 设备配网知识库 + 1 次性合规评估
4. **Truth Layer 沉淀**——设备配置/报警规则/反馈分类的 source of truth → AI-readable manifests（参考 [[01-ai-agents/腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] 的"知识库结构化"）
5. **Eval 接回业务规则**——设备分诊/反馈分诊 eval suite，每周跑 quality control agents；与 [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]] "用例基线"思路一致
6. **主人先搭自己的 OS**——7 维 OS + 月报加"AI 决策数 vs 主人亲自决策数"指标对齐 Masha 模式

## 备注与限制

- 所有数据（60 deal 评估、Reiki massage 偏差、4 周 code audit tickets）来自 Masha Sharma 本人口述，无第三方验证
- Masha 经验以 Groupon 1 万+ 员工公司实证为主，**Seetong 30-50 人团队不能直接套，需裁剪**
- "Truth Layer / Manifest / Speedboat" 是 Groupon 内部用法未标准化
- 偏"工程主管视角"未触及一线员工体验
- 原文 4000 字是晚点再听LaterCast 中文浓缩稿，Augmented U 原视频 30+ 分钟含更多问答细节未抓取

## 相关链接

- 原文：https://mp.weixin.qq.com/s/LkMuNLTHRHTFJUYD6iAyaA
- 一手原视频：https://www.youtube.com/watch?v=pQj8qOyan-Q
- 公众号：晚点再听LaterCast（Capihom）
- 同主线 wiki：[[01-ai-agents/未来属于垂直领域Agent]] [[01-ai-agents/Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] [[01-ai-agents/ThinkingAgent-Knock-AI-Native组织5级成熟度模型]] [[01-ai-agents/Multica-AI-Native-组织-人是最慢的节点]]
- 同 Capihom 编译系列：[[01-ai-agents/Capihom-AI-Agent帮上门服务多接单-YC-Root-Access-Avoca]] [[02-ai-coding/Capihom-OpenAI-Codex-Andrew-Ambrosino-产品工作新形态]]