---
title: Meta Muse：个人 Agent 执行环境速读
category: 01-ai-agents
tags: [主题/Agent架构, 主题/权限控制, 主题/长任务恢复]
nodes: [个人执行环境, 模型与Harness分离, Runtime-Cell隔离, Sentinel授权, 确定性审批, 凭证代理, 污染数据出网, 状态与记忆分层, 外部副作用确认]
links: [[01-ai-agents/若飞-Meta-Muse-个人Agent执行环境]], [[01-ai-agents/InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]
date: 2026-09-27
source: 微信公众号「架构师」/ 若飞
status: published
---

# Meta Muse：个人 Agent 执行环境速读

> **一句话**：模型负责提议，运行时负责受限执行，Sentinel 负责授权，客户端负责人类审批，外部系统负责完成证据；这些状态不能混写。

| 层 | 职责 | 不等于 |
|---|---|---|
| Muse Spark／Hatch | 提议、装配上下文与调工具 | 获得权限或完成动作 |
| Runtime Cell／Sentinel | 隔离执行、出口检查、allow／deny／ask | 真实外部服务已成功 |
| 客户端／目标服务 | 承接审批、接管并回传执行结果 | 模型文字自称成功 |

## 三个关键判断

- 长上下文不是长期记忆：文件持久保存、可检索、进入本轮工作集是不同状态。
- 连接器 schema 约束参数，但不能代替进程权限、对象范围、凭证代理和网络出口策略。
- 请求发出后回执丢失，先查询目标系统再决定重试；事件日志可回放不代表外部副作用天然恰好一次。

## 对 Seetong 的最小应用

1. 群报告区分模型摘要、数据校验、发送动作和企微 ACK；没有 ACK 不记作送达。
2. 设备操作区分查询与变更权限；让用户明确批准写入和不可逆副作用。
3. 用同一任务 ID 保存当前目标、状态、授权、工具结果和恢复检查点，重启后先查权威结果。

[完整编译页](./若飞-Meta-Muse-个人Agent执行环境.md) · [清洗原文](../../raw/2026-09-若飞-Meta-Muse-个人Agent执行环境.md) · [公众号原文](https://mp.weixin.qq.com/s/nQTi_u4O0PnzaqEA_ukNww)

**证据边界**：若飞对 Meta 官方文章和社区项目的综合解读；社区逆向不等于官方 API，运行时与安全细节未独立复现。
