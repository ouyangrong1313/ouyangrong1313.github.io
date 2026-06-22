# Codex和Claude Code负责人都不写提示词了,AI 圈爆火的Loop到底是什么 — Digest

- 原文链接:https://mp.weixin.qq.com/s/nM1fpAdA8F2wYPNh2jEvPg
- 公众号:APPSO / 作者:发现明日产品的
- 节点数:8 | 表格:1 | 子标题:5

## 一句话总结

当 Agent 能连续跑几十分钟/几小时,人机协作单位从"一次对话"升到"完整反馈回路"——人该从"每轮 prompt"退到"设计 loop";**分清"好提示词够了"和"必须 loop"的分界线,比术语本身重要**。

## 速查表

| 维度 | 关键判断 |
|------|---------|
| 时代迁移 | Prompt(写好提示词)→ Harness(搭框架)→ Loop(写反馈系统) |
| Loop 本质 | 把"行动→观察→修正→再行动"系统化,人从每轮推动退到写规则 |
| 5 个必答 | 何时开工 / 调哪些工具 / 怎么知道错 / 结果记哪 / 何时停 |
| 5+1 积木 | 定时任务+worktree+Skill+连接器+子 Agent + 状态文件 |
| 4 类场景 | 内容 / 客服 / 产品运营 / 研究(共同点:反复+稳定+可检查+判断在人) |
| 3 个前提 | Token 管够 / 任务每周重复 / 有自动验证 |
| 成本转移 | 人时间 → 系统 Token;月付 20 美元跑两天到周限额 |
| 分界线 | 一次性=好提示词;反复=必须 loop |

## 关键金句(原话)

- Boris Cherny:「不跟 Agent 对话,跟 loop 对话,让 loop 替我来 prompt」
- Boris + Cat Wu 一周年节目:Loop 是下一个 Leap(飞跃)
- 龙虾之父 X 推:不要在 Coding Agent 类产品里写提示词了,设计循环来使用这些 Agent
- Codex 负责人 Tibo 转推:是否已经写嵌套循环了
- APPSO 收尾:「这个分界线,在当下看来,可能比『循环工程』这个名字本身重要得多」

## 4 个产业人物同向信号(值得记)

| 人物 | 职位 | 表达 |
|------|------|------|
| Boris Cherny | Claude Code 负责人 | "我的工作已经变成写 Loops" |
| Cat Wu | Claude Code 产品负责人 | 与 Boris 同节目赞同 |
| Tibo (Thibault Sottiaux) | Codex 负责人 | 转推问"是否写嵌套循环" |
| Addy Osmani | Google Cloud AI 总监 | 5+1 积木方法论 |

**Loop 主题第一次出现 4 个独立信息源同向共振**——不再是单个 KOL 自说自话。

## 对 Seetong 4 个可借鉴动作

1. **盘点已是 loop 的**:OpenClaw HEARTBEAT、Seetong 日报/周报/简报 cron、神策友盟反馈 dry-run、Login 成功率每日巡检——全是 loop 雏形,写进 [[Codex配置原则总览]] "已是 loop" 清单
2. **选 1 个"高 ROI + 验证便宜"场景试 7 天**:神策崩溃堆栈归类 / TAPD 过期迭代关闭 / 用户反馈去重——都满足"自动 verify=结果可读可点"
3. **写 Loop 任务卡 8 项必填**:循环名称/触发频率/输入范围/最大运行/权限/验证/停止/交付物
4. **拒绝为 loop 而 loop**:一次性需求继续用好提示词+Plan 模式;**只有"每周/每天重复+流程稳定+验证便宜"三件齐全才上 loop**

## 关联(三段)

### 上游
- [[Addy-Osmani-Loop-Engineering]] — 5+1 积木原始来源
- [[Loop-Engineering-详解-把反馈循环放进工程现场]] — 若飞中文实操

### 下游
- [[从Prompt-Context到Harness-工程的三次进化与终局之战]]
- [[Claude-Code一周年回顾-Boris-Cat]]
- [[claude-code-dynamic-workflows]]

### 同级
- [[Claude-Code首席设计师Meaghan-Choi工作流]]
- [[Anthropic万字长文三个判断和一个阳谋]]

## 限制

- 4 个信息源是同温层(头部 AI Coding 社交网络互通),未必代表行业共识
- "一次 loop 的 token 实际 vs 一次对话追问几轮"对比数据未给
- 无 7 天试点/数据,纯方法论+产业信号,与若飞详解互补
- 龙虾之父"5 分钟唤醒 Codex"的成功率/质量/成本未披露
