# 别再反复教 Coding Agent——让项目记住自己如何工作的五个步骤 - Digest

- 原文：https://mp.weixin.qq.com/s/1FrHNkfVpp8CE7keWt_lbQ
- 作者：Phodal（Better Harness / QoderAI）/ 分类：02-ai-coding / 获取时间：2026-08-03 10:29

## 一句话总结 + 备注

让 Coding Agent 不被反复教的关键，是让项目自己记住经验——AGENTS.md 给地图、文档接到任务路径、Skill 提炼重复工作、CLI 优先于 MCP、Agent Work Loop + Loop Discovery 让经验沉淀回流。

作者：Phodal（公众号名未在 HTML meta 暴露）/ 发布时间推断 2026-08。可证伪点："相似需求 ≥ 2 次"是经验门槛非可量化阈值；Seetong 30-50 人小团队建议"≥ 3 次"。不适用：一次性项目 / 1 人小工具 / 教学 Demo——最小单元（入口/命令/风险/导航 4 项）才能落地。

## 速查表

| 阶段 | 产物 | 关键决策 |
| --- | --- | --- |
| 1. 开工 | AGENTS.md | 短/准确/可执行/渐进式披露 |
| 2. 知识路由 | 核心文档 + 读取条件 | "改什么读什么"，不是链接列表 |
| 3. 重复方法 | Skill | 探索门槛 6 条（相似 ≥ 2 次 + 5 个其他）|
| 4. 工程接口 | CLI > MCP | CLI 六条 / 程序判断归脚本 |
| 5. 持续改进 | Agent Work Loop + Loop Discovery | 5 类沉淀位置决策（见下）|

| 信号（Loop Discovery）| 沉淀位置 |
| --- | --- |
| 稳定事实 | AGENTS.md 或核心文档 |
| 重复方法 | Skill |
| 确定性操作与检查 | CLI / 脚本 / Hook / CI |
| 外部资源发现 + 持续交互 | MCP |
| 高风险、不可逆操作 | 权限边界 + 人工确认（不沉淀）|

## 关键金句（3 条）+ 8 节点速查

1. "一个 Agent 友好的项目，不是安装了多少工具，而是项目知识能否被发现，流程能否被执行，结果能否被验证，经验能否进入下一次任务。"
2. "Agent 能从代码中看出来的内容，没有必要再写一遍。真正值得写进去的，是它看不出来、却很容易猜错的事实。"
3. "所谓持续改进，不是不断增加配置，而是让这一次任务留下的东西，真正帮助下一次。"

8 节点速查：① AGENTS.md 项目地图（入口/命令/风险/导航 4 项最小集）② 渐进式披露（根目录只放多数任务都需要的说明）③ 文档任务路由（"改什么读什么"取代链接列表）④ Skill 探索门槛 6 条（相似 ≥ 2 次 + 5 个其他条件）⑤ CLI 优先 MCP 兜底（CLI 六条）⑥ 程序判断归脚本/Hook/CI ⑦ Agent Work Loop 五段（理解需求→找到知识→执行修改→验证交付）⑧ Loop Discovery 沉淀决策树（5 类信号 → 5 个沉淀位置）。

3 反直觉点：① AGENTS.md 越短越好，详细文档按需链接；② CLI 优先于 MCP，已有脚本先整理 CLI；③ 写进仓库 ≠ 实践生效，下一次任务 Agent 能否用上是唯一检验标准。

## 6 个对 Seetong 借鉴动作

详见 wiki 编译页。核心 3 条：AGENTS.md 体检 6 个主仓库 / Skill 探索门槛硬约束 6 条 / Skill 用上率 30 天评估三项。

## 关联（强）

- **同作者姊妹篇：** [[01-ai-agents/phodal-Better-Harness-任务级证据评估]]（7/28）
- **Skill 落地主线：** [[02-ai-coding/Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] [[02-ai-coding/面向Skills编程-淘宝企业购端到端研发提效实践]] [[02-ai-coding/loonggg-Claude-Code-技能心法-11条建议]] [[02-ai-coding/Agent自维护体系-完整实战]] [[01-ai-agents/腾讯-AI-Agent-Skill-测评方案落地]]
- **Harness / AI Coding 基础：** [[01-ai-agents/lencx-Agent开发指南-技术太多-该怎么学]] [[01-ai-agents/Skill-Self-Evolution]] [[01-ai-agents/Loop-Engineering-验证才是瓶颈]] [[02-ai-coding/54万行代码的顿悟-Markdown才是新编程方式]] [[02-ai-coding/AI-Coding的顿悟时刻]]