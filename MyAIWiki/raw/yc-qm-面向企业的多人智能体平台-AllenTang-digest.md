# 原文摘要：一文搞懂 YC-QM：面向企业的多人智能体平台

- **作者：** AllenTang（微信公众号「架构师带你玩转AI」编辑；同作者 7/22 已编 [[万字长文拆解Agent-架构设计-四-多-Agent-协作]]）
- **一手仓库：** https://github.com/yc-software/qm（MIT 协议 / YC 开源）
- **原文链接：** https://mp.weixin.qq.com/s/O8O6ttb-z9KmwjG4C9fe-Q
- **获取时间：** 2026-08-03 14:41 Asia/Shanghai

## 一句话总结

QM 是 YC 开源的多人智能体协作平台——从"个人助理"到"多人协作"靠 scope（作用域）隔离，6 大特性：无头核心 + 持久电脑 + 4 个 Harness 适配器 + Durable by default + 智能体=你本人 + 3 种安全 posture + 5 条工程文化铁律。

## 核心观点（6 节 + 8 节点）

### 一、Scope 隔离（灵魂概念）
每个员工/Slack 频道/群组/项目 = 独立 scope。每个 scope 拥有：记忆、文件、凭据视图、权限、定时任务、Web 应用、持久沙箱 7 项隔离资源。**个人定制 + 团队共享兼得**——大多数产品二选一，QM 靠 scope 两个都要。

### 二、落地场景（公司日常）
统一搜索 / 公司大脑检索 / 内部应用 / 邮件分身（学你语气打标签写草稿）/ 代码仓库作业 / 项目跟踪。Seed skills 包括 GitHub/GitLab/Google Workspace/Google Drive & Sheets/Dropbox/Linear/浏览器/晨间摘要/按语气起草邮件/应用发布。

### 三、架构（无头核心 + 持久电脑）
1. Core 本身无头；网页 UI / 管理后台 / 公共门户 / Slack 都是挂在 Core HTTP API 上的可选插件。
2. execute 工具把命令送进 scope 自己的隔离沙箱——官方称"持久电脑 Durable Computer"——装过的工具不会丢，重启重部署都在，不是一次性容器。
3. 状态不落内存，落 Postgres。**Durable by default**——核心蓝绿部署多实例运行；任何进程里的 Map/环形缓冲都会随部署被抹掉，凡是以后还要读回的东西必须进持久存储。
4. 技术栈：TypeScript + Node / Fastify / Slack Bolt / Vite + Lit。

### 四、不绑模型不绑框架（4 Harness 适配器）
智能体循环是可替换底座，已有 4 个适配器跑同一套核心：**Pi / OpenCode / Codex / Claude Code**。每种 substrate（harness/会话存储/沙箱/记忆）都躲在接口后面，换一个 wiring file 就能整体替换。**QM 想做的是智能体平台的"操作系统层"**。

### 五、安全：智能体 = 你本人
智能体以所服务那个人的身份行动，持其凭据、守其权限、全程留痕审计。3 种安全 posture：
- **Strict**——每次工具调用暂停等人工批准
- **Auto**——分类器在数据"抵达模型之前"做来源标记与筛查
- **Dangerous**——不筛查不暂停（自负后果）
- 命令策略（递归删除、破坏性 SQL 硬性拒绝）在所有 posture 下生效。
- **坦诚披露** SECURITY.md 主动列已知局限 + **供应链 7 天静置**（新 npm 包必须等 7 天才能进 lockfile）。

### 六、工程文化 5 条铁律（来自 AGENTS.md）
1. 修每一处，不只是被报告的那一处（全仓库 grep 同样模式）
2. 修复让系统更简单（能删代码就不加，能复用就不新建）
3. 永不合并未经陌生上下文审查的代码（写代码的人天然相信它对，必须派独立审查者找茬）
4. 仓库里不留注释（意图用命名/结构/测试表达，理由写 commit message）
5. **收文字不收代码**——你想改什么，在 adrs/ 写大白话 .txt/.md，官方认同后由他们实现（提案/实现解耦）。

## 关键数字

| 维度 | 数字 | 说明 |
|---|---|---|
| Scope 隔离资源 | **7 项** | 记忆/文件/凭据/权限/cron/Web/沙箱 |
| Harness 适配器 | **4 个** | Pi / OpenCode / Codex / Claude Code |
| 安全 Posture | **3 种** | Strict / Auto / Dangerous |
| 供应链静置 | **7 天** | 新 npm 包必须等 7 天才能进 lockfile |
| 工程文化铁律 | **5 条** | 修每一处/让系统更简单/独立审查/不留注释/收文字不收代码 |

## 关键金句（5 条）

1. "个人定制和团队协作，在大多数产品里是二选一。QM 的答案是：靠 scope 隔离，两个都要。"
2. "状态不落内存，落 Postgres——Durable by default，核心是蓝绿部署、多实例运行，凡是以后还要读回来的东西必须进持久存储。"
3. "QM 想做的是智能体平台的'操作系统层'：上层界面、下层模型和框架，全都可以换。"
4. "智能体以它所服务的那个人的身份行动，持其凭据、守其权限，所做的一切全程留痕审计。"
5. "它明确说自己还是'early, experimental software'，隔离设计'不是一个数据不会泄露的承诺'——在一个充斥着'我们的 AI 绝对安全'话术的行业里，这份诚实反而是一种专业。"

## 反直觉点（3 条）

1. **聊天机器人思路进企业必死**——QM 不做聊天机器人做多租户底座；scope 是灵魂不是特性。
2. **状态不落内存是铁律不是建议**——任何进程内 Map/环形缓冲会被蓝绿部署抹掉，"以后还要读回的东西必须进持久存储"。
3. **坦诚披露"还不安全"是专业**——SECURITY.md 主动列已知局限（命令策略可被混淆绕过/沙箱内凭据明文/管理员可读取敏感内容）+ 供应链 7 天静置 + 收文字不收代码——开源界几乎独一份。

## 关联图谱

### 上游（基于 / 来自）
- [[万字长文拆解Agent-架构设计-四-多-Agent-协作]]（2026-07-22）——同作者 AllenTang 同主线"多 Agent 编排"，本文是其"多租户底座"实战篇。
- [[0xCodez-Agent-Harness-14-Steps]] [[HarnessEngineering企业级实战]] [[Harness工程AgentLoop]] [[Lilian-Weng-Harness-Engineering-自我改进]] ——Harness 路线图 + 实战 + 理论框架。
- [[agent-architecture]] [[agent-architectures]] [[agent-principles-architecture-engineering]] ——Agent 架构原则。

### 下游（应用于 / 验证于）
- [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] ——Harness 实战，本文 4 适配器思路是同一脉络。
- [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] [[阿里云开发者-淘宝主播Agent的Harness工程实战]] [[腾讯-AI-Agent-Skill-测评方案落地]] ——企业级 Agent 平台落地。
- [[腾讯程序员-AI-Coding到Harness-Engineering-应用宝活动平台实践]] ——本文"Durable by default"在企业活动平台的具体化。
- [[cases/liangbo-execution-agent]] ——执行型 Agent 实战，本文 scope + execute 工具是同类思路。
- [[OpenClaw-vs-Hermes-多-Agent-架构设计]] ——多 Agent 架构对比，本文 scope 隔离是另一种范式。

### 同级（横向 / 并列）
- [[Harness不是目的，知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]] ——同主线"AI 工程交付团队"。
- [[企业知识库认知底座]] ——企业知识库视角。
- [[Agent Harness 与 OpenClaw：从工具到系统的中文解读]] [[Agent Harness 解析：智能体架构深度拆解]] [[从 Agent Harness 到知识复利：结合 OpenClaw 的一体化理解]] ——Harness 中文解读三连。
- [[未来属于垂直领域Agent]] [[lencx-Agent开发指南-技术太多-该怎么学]] [[Agent时代架构师系统能力]] ——Agent 工程能力主线。
- [[phodal-项目记住-Coding-Agent-5步法]]（2026-08-03 同日）——本文 5 条工程文化铁律与 Phodal 5 步法形成"治理/落地"对偶。

## 备注与限制

1. **作者来源：** 公众号名未在 HTML meta 暴露（`og:article:author=AllenTang` 已确认），按内容定位为「架构师带你玩转AI」，与 [[万字长文拆解Agent-架构设计-四-多-Agent-协作]] 同作者。
2. **发布时间：** 推断 2026-07 末至 2026-08。
3. **一手仓库：** https://github.com/yc-software/qm（MIT 协议）；本文是 AllenTang 解读/二手编译，非官方文档。
4. **可证伪点：** "4 个 Harness 适配器（Pi/OpenCode/Codex/Claude Code）"是文章快照，QM 主仓库 master 分支可能更新；"7 项 scope 隔离资源"是 AllenTang 归纳非官方完整列表。
5. **不适用：** 1 人小工具/单人项目——QM 的 scope 隔离价值在多租户，单人场景反而是 overhead。
6. **关联首选：** 与 [[万字长文拆解Agent-架构设计-四-多-Agent-协作]]（7/22 同作者）形成"多 Agent 编排 / 多租户底座"对偶；与 [[phodal-项目记住-Coding-Agent-5步法]]（8/3 同日）形成"治理 / 落地"对偶。