---
title: 得物技术：Delivery Harness 与可控 AI 交付
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 主题/Harness工程
  - 主题/验证驱动
  - 主题/跨运行时
  - 主题/持续改进
  - 场景/企业研发
nodes: [语义分叉, Version-Contract, Execution-Boundary, Evidence-Gate, 业务不变量, Worktree隔离, Repair-Loop]
links: [[02-ai-coding/大淘宝技术-AI驱动研发体系-Price360-KB项目Harness]], [[02-ai-coding/AICoding之后-如何让Agent进入企业研发全链路-得物推荐的Harness实践]], [[02-ai-coding/大淘宝技术-永霸-AI-Coding-环境与验证驱动]], [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]
date: 2026-09-03
source: 微信公众号「得物技术」/ 正飞
status: published
---

# 得物技术：Delivery Harness 与可控 AI 交付

- 原文链接：https://mp.weixin.qq.com/s/Jcx_3OABcYwzzxWKFgivOA
- 来源：微信公众号「得物技术」；作者正飞
- 获取时间：2026-09-03

## 核心结论（一句话）

AI 扩大单人跨运行时交付半径后，可靠性不取决于更长 Prompt，而取决于将事实、改动范围、状态跃迁和真实反馈分别固化为 Version Contract、Execution Boundary、Evidence Gate 与 Repair Loop，使每项结论有对应证据、每次修复能改变下一次默认行为。

## 分类提炼

- 场景：多仓库/多运行时 AI Coding、业务规则一致性、质量门禁、发布可追溯性
- 标签： #主题/AI-Coding #主题/Harness工程 #主题/验证驱动 #主题/跨运行时 #主题/持续改进
- 类型：企业研发实践 / 单人全栈交付复盘 / Delivery Harness 方法

## 知识节点

- **语义分叉**：一个未确认的业务口径在 AI 高速生成下会同步进入接口、页面、测试与验收，形成局部自洽却整体错误的交付链。
- **Version-Contract**：显式登记本轮事实源、产品口径、技术影响、版本、仓库、分支、验收项和待确认状态，阻止临时推断自动成为长期事实。
- **Execution-Boundary**：以仓库、工作区、分支、文件范围、请求网关和环境权限约束 Agent 的动作半径，防止跨仓、跨环境和外部写入越权。
- **Evidence-Gate**：用命令结果、测试、接口、真机、发布和合入证据分别控制不同状态；证据不足时不得推进任务。
- **业务不变量**：跨运行时不可被局部实现拆散的业务语义，例如订单级原子性；应同时进入合同、接口、服务校验、反例测试和验收报告。
- **Worktree隔离**：将“一需求 × 一仓库”映射到独立工作树和分支，需求全生命周期复用同一现场，避免多任务共享未提交状态。
- **Repair-Loop**：将真实反馈记录为可复现的失败基线、候选修复与回归结果，再升级为测试、门禁或合同规则，令同类问题更早失败。

## 正文要点

1. **AI 放大错误传播，也放大工程半径**：一个人可并行推进 H5、后台、网关和服务，但业务语义若未锁定，会以更快速度变成跨模块共同前提。Harness 的首要价值是前移发现和阻断错误。
2. **四组件接管状态而非替代判断**：Version Contract 管事实，Execution Boundary 管权限和范围，Evidence Gate 管状态，Repair Loop 管学习。模型继续生成和推理，但不应反复猜测有客观答案的路径、分支和发布记录。
3. **工作区本身是边界**：每个需求/缺陷在首次写入前基于已核对基线创建专属 worktree；同一需求从开发、联调到发布收口复用该现场，清理必须在证据持久化和发布记录完整后进行。
4. **交付状态必须分开证明**：代码完成、研发验证、具备验收条件、真实环境验收、生产发布、稳定分支合入各有独立含义。自动化可检查状态和边界，真实体验及最终签字仍由责任人完成。
5. **跨运行时需要共同不变量**：多 SKU 履约示例将“订单是履约原子单位”贯穿产品、接口、服务、测试和验收，防止任何一层把订单误读为 SKU 而留下局部正确。
6. **反馈只有改变后续行为才算闭环**：Repair Case 需保存原始反馈、失败基线、候选结果和回归结果；环境恢复不可包装成代码修复，偶现问题也不可因暂时未复现而关闭。

## 关联图谱

### 上游（基于 / 来自）

- [[02-ai-coding/大淘宝技术-AI驱动研发体系-Price360-KB项目Harness]]：项目 Harness 组织稳定上下文、动态事实和机器可读迭代协议；本文进一步将其收敛为版本、范围、证据和修复四个交付控制面。
- [[02-ai-coding/大淘宝技术-永霸-AI-Coding-环境与验证驱动]]：提出模型能力与环境能力相乘、用分层验证提供反馈；本文给出跨仓工作区、业务不变量和发布证据的具体落点。

### 下游（应用于 / 验证于）

- [[02-ai-coding/AICoding之后-如何让Agent进入企业研发全链路-得物推荐的Harness实践]]：全链路 PDCA、环境护栏和评测机制可承载本文的 Version Contract、Evidence Gate 和 Repair Loop。
- [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]：本文将“验证是瓶颈”扩展为哪些状态必须有何种证据，以及失败如何形成下一轮规则。

### 同级（横向 / 并列）

- [[01-ai-agents/phodal-面向人机交互设计Harness-产物中心Agent-Loop]]：同样主张协作状态应留在可操作、可验证的产物中；本文偏多运行时交付、版本隔离与发布追溯。
- [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]：同样从模型能力之外的 Harness 寻找可靠交付条件，本文补充 Version Contract 和 Repair Case 的证据形态。

## 相关链接

- [原文归档](../../raw/得物技术-Delivery-Harness-可控AI交付.md)
- [分析拆解](../../raw/得物技术-Delivery-Harness-可控AI交付-digest.md)

## 证据边界

本页基于得物技术的单团队交付复盘。其工作区、合同、门禁、修复流程和多 SKU 案例均未独立复现，缺少完整实现、样本规模、对照数据与独立审计；它们适合作为 Delivery Harness 设计假设，不构成通用质量、合规、安全或生产发布保证。
