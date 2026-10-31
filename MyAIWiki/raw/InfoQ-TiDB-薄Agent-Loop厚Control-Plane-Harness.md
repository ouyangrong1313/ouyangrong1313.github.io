# “薄 Agent Loop，厚 Control Plane”：TiDB 用数据库思维重做 Harness

- 原文链接：https://mp.weixin.qq.com/s/XwdD9d6jFbRFwMWhr5a7JA
- 来源：微信公众号「InfoQ」
- 作者：Tina
- 受访者：TiDB 唐刘
- 发布：2026-09-06 12:30（页面标注：天津）
- 获取时间：2026-09-07
- 抓取方式：`isolated-chrome-cdp`
- 抓取正文 SHA-256：`d9adc65a6f0e0c3e7f9d5e641ecb1c363cc533d244b90ddc530829947cd8b9a6`
- 清理说明：已去除转载声明、今日推荐与会议推广；保留采访正文。

## 正文

TiDB 团队启动了面向 Agent 的基础设施尝试 TiDB Cloud Filesystem：它将 Workspace 从 Session 和 Sandbox 生命周期中独立出来。Agent 继续使用熟悉的文件系统接口，底层则提供数据库级持久化、版本、分支、回滚与权限控制；Sandbox 被回收后，新 Executor 仍能接管同一份文件和状态。受访方称该系统已承载数百万个 Agent Workspace。

TiDB 没有从零编写 Agent Loop，而是基于开源项目完成最内层核心，将精力放在任务编排、权限、Sandbox、持久状态与失败恢复。这套 Harness 的哲学是“薄 Agent Loop，厚 Control Plane”：模型协议、Tool Calling、Streaming、Reasoning 变化很快且容易同质化；状态、权限与副作用边界必须保持稳定。类比数据库，SQL 与 Optimizer 可以不断变聪明，Transaction、Privilege、Durability 不能因上层更聪明而消失。

## 1. 数据库行业天然就在做 Harness

TiDB 的系统并非一套完整固定的最佳实践：最内层 Agent Loop 基于开源 Pi，任务编排、权限、持久状态、Sandbox 与失败恢复多由团队自行建设。这样可替换模型或 Agent Core，而不推倒 Sandbox、权限、状态和控制面；模型能力增强可扩大 Sandbox 内探索空间，但不应同时放松真实生产系统的副作用边界。

数据库的 Mission Critical 属性意味着发布不只要求代码能运行，还需保证客户数据不损坏、服务不中断、新旧版本兼容、异常后可恢复。测试代码、故障注入、随机测试、兼容性测试、性能测试和线上 Case 积累，本身就是 Harness。数据库代码是被测试对象，围绕它的验证体系决定系统是否敢进入生产。

不能相信组件声称自己正确，应以外部不变量证明正确。对 Agent 而言，“我已经修好”没有意义；要能回答哪个 Commit、什么测试、什么输入、什么故障条件、什么 Evidence，以及他人能否复现。代码测试只是较简单一环；云服务升级面对真实流量，Harness 更要支持渐进 Rollout、验证、观察、Fail Fast、Rollback 与业务连续性。

## 2. 模型能力、责任与工程判断

受访方不认同“模型到顶”。通用编程中模型差距确在收小，例如把已有实现转换成另一种语言的 Translation 任务；但 Cloud Service Upgrade 涉及多系统、多版本、客户环境、实时流量、灰度、恢复与业务连续性，难点超出写代码。

关键问题是能否在不完整信息、多目标权衡、风险、反事实和错误后果下做决策并承担后果。重要任务最终仍需工程师说 Go、Stop 或 Rollback，因为责任仍由人承担。随着 AI 遮蔽了 Debug、Core Dump、Oncall、日志分析与线上恢复等经验，工程师的系统直觉可能被削弱；另一种可能是工程抽象层上移，人更关注系统应具备的性质而非单行代码。

Planner、Coder、Reviewer、Search、Edit、Shell、Sub-agent 与 MCP 会逐渐成为标准部件。真正差异不在是否具备组件，而在它们如何组成能解决现实问题的系统，以及团队敢让 Agent 在什么边界内行动。

## 3. 编排会从命令式走向目标声明

受访方认为 Agent Orchestration 的未来可能是更少的显式 Orchestration。早期需要明确指定每一步、角色和协作 Prompt；模型增强后，只要声明“我要什么结果”，Agent 就可完成更多内部规划。这类似数据库从手写 Join 顺序走向只声明结果的 SQL，由 Optimizer 决定执行路径。

这不表示编排消失：复杂系统中 Context 有限、状态需持久化、错误要恢复，仍有更高层的任务边界。TiDB 探索让多个 Agent 独立解决同一问题，各自拥有隔离 Workspace、状态与实现，最后 Merge 或淘汰；这被类比为 MVCC，即先让多个执行者在自己的 Version 中探索，而不是争抢同一世界。

文件对 Agent 是自然接口，Agent 擅长通过 `ls`、`grep`、`cat`、改文件和目录理解世界；但 Agent 同时需要检索、索引、Transaction、Version、Branch、Rollback 与 Query。TiDB 的方向是让 Agent 看见 File，底层拥有 Database 能力，为 Agent 提供数据与状态基础设施，而非只追求更强 Agent Core。

## 4. 多 Agent：少通信、强状态边界

Kubernetes 擅长管理长期运行、声明式、相对稳定的 Service；Agent Workload 常为瞬时按需启动、空闲时间长、生命周期短，状态的重要性甚至高于 Compute，因此 Runtime 应随 Workload 改变。

TiDB 对多 Agent 比较克制，核心判断是“Communication is complexity”。高频 Agent 间问答、通知与同步会增加 Debug 难度和性能成本。较合适的拓扑接近 Unix Philosophy：一个 Agent 做好一件事，通过清晰 Input/Output 与共享状态解耦；上层 Workflow 或 Agent 可分配与汇总，但整体拓扑应尽量简单。能用一个 Agent 解决就不用五个，能共享状态就不消息广播，能异步就不建立同步依赖。

## 5. 长程可靠性：Fail Fast、限制传播、可信恢复

长程稳定性不等于模型能连续运行五十或一百步；关键是小错误能否在演变为故障前被拦住。分布式系统中的网络、磁盘、机器和 Timeout 必然失败，危险的是把 Failure 当普通事件不断 Retry，最终把小故障放大为雪崩。

对 Agent，错误若没有被阻断，会从第十步扩散到后续步骤，错误 Context 被后续 Agent 当作事实，最终无法判断从何处开始错误。成熟系统需要三种能力：尽早发现错误、限制错误成为后续事实、从最近可信状态恢复。Checkpoint、持久状态、换 Agent 或换路径继续，分别对应数据库的 Transaction Log、Checkpoint、Rollback 与 Failover。

成熟可靠性不追求永不失败，而是“Assume failure, contain failure, recover from failure”：假设失败必然发生，控制影响范围，并从失败中恢复。

标签： #主题/AI-Agent #主题/Harness工程 #主题/Control-Plane #主题/Agent运行时 #主题/可靠性工程 #主题/多Agent协作 #场景/公众号长文
