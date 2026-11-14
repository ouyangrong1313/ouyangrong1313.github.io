# Codex和Claude Code负责人都不写提示词了,AI 圈爆火的Loop到底是什么 — Digest

- 原文链接:https://mp.weixin.qq.com/s/nM1fpAdA8F2wYPNh2jEvPg
- 公众号:APPSO / 作者:发现明日产品的
- 核心命题:Loop Engineering 不是"新瓶装旧酒",而是人机协作单位从"一次对话"升级为"完整反馈回路"——当 Agent 能连续跑几十分钟/几小时,人该从"每轮 prompt"退到"设计 loop";**分清"好提示词够了"和"必须 loop"的分界线,比"循环工程"这个名字本身更重要**

## 8 个核心观点

1. **时代迁移**:Prompt(写一句好提示词)→ Harness(给模型搭框架)→ Loop(把反馈系统写下来,人退到设计 loop)
2. **Loop 本质**:把"行动→观察→修正→再行动"的人手循环系统化;过去每轮靠人复制报错追问提醒,现在写成规则交给系统
3. **5 个必答问题**:何时开工 / 调哪些工具 / 怎么知道错了 / 结果记哪里 / 何时停下交人
4. **5+1 积木**(Addy Osmani 框架):定时任务(Codex Automations / OpenClaw HEARTBEAT / Claude Cowork Scheduled)+ worktree + Skill + 连接器(MCP)+ 子 Agent + 1 状态文件
5. **不只代码**:内容(选题筛选→事实核验→发布前检查)/ 客服(分诊+草稿+人工兜底)/ 产品运营(反馈聚合)/ 研究(论文追踪)四类同构场景;共同点=任务反复+流程稳定+结果可检查+判断在人
6. **3 个上手前提**:Token 管够 / 任务每周重复 / 有自动验证(测试/类型检查/构建)
7. **成本转移**:从"人时间成本"转到"系统 Token 成本";无限额度的人(龙虾之父、Boris、Addy)觉得常识,月付 20 美元跑两天就到周限额
8. **分界线**:一次性活=好提示词;反复活=必须 loop;**关键不在术语新不新,在"AI 已经能连续处理多轮时,人还要不要卡在每次追问里"**

## 关键引用(原话)

- Boris Cherny:「不跟 Agent 对话,跟 loop 对话,让 loop 替我来 prompt」
- Boris + Cat Wu 在 Claude Code 一周年节目:Loop 是下一个 Leap(飞跃)
- 龙虾之父 X 推:不要在 Coding Agent 类产品里写提示词了,设计循环来使用这些 Agent
- Codex 负责人 Tibo 转推:是否已经写嵌套循环了
- 龙虾之父 X 实践:Codex 每 5 分钟唤醒,统筹+分类+自动审核+Computer Use
- APPSO 收尾:「这个分界线,在当下看来,可能比『循环工程』这个名字本身重要得多」

## 速查表:5+1 积木对照

| 积木 | Codex | Claude Code | OpenClaw / 其它 |
|------|-------|-------------|-----------------|
| 定时任务 | Automations | (Claude Cowork: Scheduled) | **HEARTBEAT** |
| 隔离工作区 | worktree | worktree | worktree |
| 过程资产 | Skill | Skill | Skill |
| 外部连接 | MCP/连接器 | MCP | MCP |
| 子 Agent | 子 Agent | sub-agent | sub-agent |
| 状态文件 | plan.md | CLAUDE.md / memory | memory / 状态文件 |

## 4 个产业人物同向信号

- **Boris Cherny**(Claude Code 负责人):「我的工作已经变成写 Loops」(此前播客已有同主题)
- **Cat Wu**(Claude Code 产品负责人):与 Boris 同节目赞同 Loop 是下一个 Leap
- **Tibo / Thibault Sottiaux**(Codex 负责人):转推并问"是否已写嵌套循环"
- **Addy Osmani**(Google Cloud AI 总监):5+1 积木方法论

**这是 Loop 主题第一次出现"四个独立信息源同向共振"**——不再是单个 KOL 自说自话。

## 关联图谱(本次只画三段)

### 上游(本文基于/来自)
- [[Addy-Osmani-Loop-Engineering]] — 5+1 积木方法论原始来源
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] — 若飞 6 工程问题+4 入口+7 天试点
- Boris Cherny / Cat Wu 一周年节目 / 龙虾之父 X 推

### 下游(本文应用于/补全)
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]] — 三层演进框架
- [[Claude-Code一周年回顾-Boris-Cat]] — Boris/Cat Loop 表达原文
- [[Claude-Code之父品味不是人类护城河]] — Boris"我的工作变成写 Loops"
- [[claude-code-dynamic-workflows]] — Claude Code dynamic workflow 实现层
- [[Claude-Code团队5条工作原则-Fiona-Fung分享]] — Routine 异步化案例

### 同级(横向/并列)
- [[Claude-Code首席设计师Meaghan-Choi工作流]] — 同一波 AI Coding 大佬的"定时巡逻产品质量"实践
- [[Anthropic万字长文三个判断和一个阳谋]] — 产业战略层

## 对 Seetong 团队可借鉴 4 个动作

1. **盘点已有 loop 等价物**:OpenClaw HEARTBEAT、Seetong 团队日报/周报/简报 cron、神策/友盟/反馈每日 dry-run,都是 loop 雏形——把它们写进 [[Codex配置原则总览]] "已是 loop" 清单
2. **从"高 ROI + 高自动验证"场景试 7 天**:神策崩溃堆栈归类、Tapd 过期迭代关闭、用户反馈去重分类——都有"自动验证 = 结果可读可点"的便宜验证
3. **写 Loop 任务卡 8 项必填**(循环名称/触发频率/输入范围/最大运行/权限/验证/停止/交付物),参考 [[Loop-Engineering-详解-把反馈循环放进工程现场]] 的"任务卡预算"模板
4. **拒绝为 loop 而 loop**:Seetong 一次性需求(版本发版)继续用好提示词+Plan 模式,只有"每周/每天重复 + 流程稳定 + 验证便宜"三件齐全的场景才上 loop

## 限制与待补证

- **"四次独立信息源同向"是同温层信号**,未必代表行业共识——可能只是 4 个 AI 大佬社交网络互通
- "token 成本变化"的判断缺数据:一次 loop 的 token 实际 vs 一次对话追问几轮的对比未给数字
- 本文无 7 天试点/数据,纯方法论+产业信号,与 [[Loop-Engineering-详解-把反馈循环放进工程现场]] 互补
- 龙虾之父"5 分钟唤醒 Codex"的成功率/质量/成本未披露
