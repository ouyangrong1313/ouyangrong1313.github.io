# 一文搞懂 YC-QM：面向企业的多人智能体平台 - Digest

- 原文：https://mp.weixin.qq.com/s/O8O6ttb-z9KmwjG4C9fe-Q
- 作者：AllenTang（「架构师带你玩转AI」）编译 / 一手 https://github.com/yc-software/qm（MIT）
- 分类：01-ai-agents / 获取时间：2026-08-03 14:41

## 一句话总结 + 备注

QM 是 YC 开源的多人智能体协作平台——从"个人助理"到"多人协作"靠 scope 隔离；6 大特性：无头核心 + 持久电脑 + 4 个 Harness 适配器 + Durable by default + 智能体=你本人 + 3 种安全 posture + 5 条工程文化铁律。

作者：AllenTang（HTML meta 暴露 `og:article:author=AllenTang`）/ 一手 https://github.com/yc-software/qm（MIT）/ 发布推断 2026-07 末至 08 / 可证伪：4 适配器是文章快照主分支可能更新；7 项 scope 资源是归纳非官方完整列表。不适用：1 人小工具/单人项目——scope 隔离价值在多租户，单人是 overhead。

## 速查表

| 维度 | 数字 / 命题 | 说明 |
| --- | --- | --- |
| Scope 隔离资源 | **7 项** | 记忆/文件/凭据/权限/cron/Web/沙箱 |
| Harness 适配器 | **4 个** | Pi / OpenCode / Codex / Claude Code |
| 安全 Posture | **3 种** | Strict / Auto / Dangerous |
| 供应链静置 | **7 天** | 新 npm 包必须等 7 天才能进 lockfile |
| 工程文化铁律 | **5 条** | 修每一处/让系统更简单/独立审查/不留注释/收文字不收代码 |
| QM 定位 | **多租户底座** | 不是聊天机器人 |
| Durable by default | **状态落 Postgres** | 进程内 Map/环形缓冲会被蓝绿部署抹掉 |
| QM 想做什么 | **智能体平台操作系统层** | 界面/模型/框架全可换 |

## 关键金句 + 8 节点速查 + 3 反直觉

**5 关键金句：** ① "靠 scope 隔离，两个都要。" ② "状态不落内存，落 Postgres——Durable by default，凡是以后还要读回的东西必须进持久存储。" ③ "QM 想做的是智能体平台的'操作系统层'：上层界面、下层模型和框架，全都可以换。" ④ "智能体以所服务那个人的身份行动，持凭据、守权限、全程留痕审计。" ⑤ "它明确说自己还是'early, experimental software'——这份诚实反而是一种专业。"

**8 节点速查：** ① Scope 隔离 7 项资源 ② 持久电脑 Durable Computer（execute+沙箱）③ 4 个 Harness 适配器（Pi/OpenCode/Codex/Claude Code）④ Durable by default（状态落 Postgres）⑤ 智能体=你本人 ⑥ 3 种安全 Posture + 7 天 npm 静置 ⑦ 收文字不收代码 + 5 条工程文化铁律 ⑧ 多租户底座定位。

**3 反直觉点：** ① 聊天机器人思路进企业必死——QM 不做聊天机器人做多租户底座；scope 是灵魂不是特性。② 状态不落内存是铁律不是建议——任何进程内 Map/环形缓冲会被蓝绿部署抹掉。③ 坦诚披露"还不安全"是专业——SECURITY.md 主动列已知局限 + 供应链 7 天静置 + 收文字不收代码——开源界几乎独一份。

## 6 个对 Seetong 借鉴动作

见 wiki 编译页。核心 3 条：Scope 体检识别 4 类隔离场景 / Durable by default 把 cron+Skill 状态全进 Postgres / 5 条工程文化铁律入 SKILL.md。

## 关联（强）

- **同作者姊妹篇：** [[万字长文拆解Agent-架构设计-四-多-Agent-协作]]（7/22）——"多 Agent 编排 / 多租户底座"对偶
- **同日姊妹篇：** [[phodal-项目记住-Coding-Agent-5步法]]（8/3）——"治理 / 落地"对偶
- **Harness 路线图：** [[0xCodez-Agent-Harness-14-Steps]] [[HarnessEngineering企业级实战]] [[Lilian-Weng-Harness-Engineering-自我改进]] [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] [[agent-architecture]]
- **企业级 Agent：** [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] [[阿里云开发者-淘宝主播Agent的Harness工程实战]] [[腾讯-AI-Agent-Skill-测评方案落地]]