---
title: 从 Prompt 到 Harness：企业级 Agent 工程的完整演进之路
category: 01-ai-agents
tags:
  - 主题/Agent架构
  - 主题/Harness工程
  - 主题/上下文管理
  - 主题/数据完整性
  - 主题/Action-Space
  - 主题/企业级Agent
  - 主题/Agent-OS
  - 场景/Seetong借鉴
  - 作者/储旭
nodes: [LLM四大先天约束, 三层工程演进, 四层上下文防线, 三层记忆, 单一表示原则, 从防御到赋能, Agent-OS五层架构, Capability-Runtime, 五层认知模型]
links: [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]], [[01-ai-agents/HarnessEngineering企业级实战]], [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]], [[01-ai-agents/若飞-Agent-记忆与可验证自我改进怎么设计]], [[01-ai-agents/InfoQ-Sam-Bhagwat-Harness长成Claw-心智争夺战]], [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]], [[loop-engineering]]
date: 2026-07-21
source: 微信公众号「阿里妹」2026-07（作者 储旭(槿柏) / 原文链接 https://mp.weixin.qq.com/s/xH4cyBJJJlG9cfcmSU5ztA）
---

# 从 Prompt 到 Harness：企业级 Agent 工程的完整演进之路

- **原文链接**：https://mp.weixin.qq.com/s/xH4cyBJJJlG9cfcmSU5ztA
- **作者**：储旭(槿柏) | 阿里妹 | 2026-07

## 核心结论

> **裸 LLM = 高性能 CPU，缺操作系统**——企业级 Agent 必须从 Prompt → Context → Harness → Agent OS 完整演进，构建 L1-L5 五层 OS。

## 知识节点

### 1. LLM 四大先天约束
- 上下文窗口稀缺：128K 物理，5 步 + 3 轮即膨胀到 200K+
- 注意力稀释：第 8 步后 70% 上下文是工具返回 JSON
- 数据搬运谬误：LLM 当"数据搬运工"会截断 UUID / 漏数组元素
- 无状态缺陷：每轮对话都是"第一次见面"，崩溃即蒸发

### 2. 三层工程演进
- Prompt：CLAUDE.md + ⚠️ 标记 → S1 (MVP) 暴露 3 结构缺陷
- Context：四层防线 + 三层记忆 → S2 让 30+ 步稳定，token -60%+
- Harness：PERO + 断点续传 + Capability Runtime + 进化体系
- Agent OS：L1-L5 五层 + 双 Agent 平台（云端认知 + OpenClaw 执行）

### 3. 四层上下文防线
- L1 工具结果压缩：>8000 字符或 >10 数组元素 → 外置 MySQL + `__refId`
- L2 语义压缩：>10000 字符 → temperature=0.3 LLM 蒸馏到 2000 字符
- L3 对话压缩：>=85% 时启动 → 结构化交接文档（4 字段 + 已放弃路径）
- L4 数据总线：system prompt 维护全局索引表，按 `step.input` 预取

### 4. 三层记忆
- State：跨步骤 key-value 存储，确定性数据通道（不经过 LLM 搬运）
- Working Memory：Pinned 任务目标 + Insights 滚动关键发现（逆序注入）
- Transcript：最近 N 条消息，`keepTarget = round(36 - steps × 0.8)`

### 5. 单一表示原则
- 同源数据在任一后续 step 的 LLM 上下文中只允许一种表示形态
- 禁止组合：full + summary / summary + preview / full + tool_result preview / full + tool_results + assistant narration
- 工程实现：PromptBuilder 运行时检查多形态共存 → 直接拒绝组装抛告警

### 6. 从防御到赋能
- parameterBindings 替代 5 层修复管道（500 行占 50% 核心代码）
- step_control 工具让模型表达 complete / skip / need_info
- working_memory 工具让模型自主记录关键发现（生成效应）
- Action Space 动态裁剪（Richard Thaler 助推理论）

### 7. Agent OS 五层架构
- L1 执行集群：Control Plane + Bridge Runtime + Gateway Runtime + Mac 节点 / Slot 池（无状态）
- L2 Agent Runtime：对话引擎 + ReAct + PERO + 执行账本（事件溯源）+ 断点续跑
- L3 记忆与语义：三层记忆 + DataProductStore 共享黑板（语义索引）
- L4 认知层：感知 + 判断 + 调度 + **注意力经济**（动态优先级队列）
- L5 自主进化：Knowledge Pack → Skill Bundle → Eval → Cert → Release（candidate → shadow → probation → active）

### 8. Capability Runtime
- 6 种 kind：skill / builtin_tool / service_tool / workflow_tool / mcp_tool / tool_pack
- 三大原则：Agent-first / Tool-first Execution / Artifact-first

### 9. 五层认知模型
- L1 语义：MetricRegistry 统一指标口径 + 版本管理
- L2 感知：Sensor Skill 三种触发模式（定时 / 事件 / 阈值），阈值判断用 execute_code 而非 LLM
- L3 推理：统计归因 + LLM 叙述解读 + 置信度标注
- L4 决策：Advisor Skill 转 2-3 方案 + ApprovalGateway 三种审批模式
- L5 元认知：注意力控制器 + 自我评估 + 能力演化引擎

## 关联图谱

### 上游
- [ReAct Loop](https://arxiv.org/abs/2210.03629)（Yao et al., 2022）/ Anthropic Claude Code "Think Like an Agent" (2025) / OpenAI Codex / 治理理论（McGregor / Deming / Thaler / Wittgenstein）

### 下游
- 企业级 Agent 平台搭建 / OpenClaw 阶段定位（S1 → S2 → Agent OS）/ 断点续传 + 事件溯源 / 从五层修复管道迁移到 parameterBindings

### 同级（横向）
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] 14 步路线图 / [[01-ai-agents/HarnessEngineering企业级实战]] 阿里 25%→90% AI 代码率 / [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]] Anthropic Harness 理论框架 / [[01-ai-agents/若飞-Agent-记忆与可验证自我改进怎么设计]] Memory 治理控制面 / [[01-ai-agents/InfoQ-Sam-Bhagwat-Harness长成Claw-心智争夺战]] Claw 阶段 / [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]] 产品视角 Harness 实战 / [[loop-engineering]] Loop Engineering 验证主线

## 7 个对 Seetong 借鉴动作

1. **OpenClaw 阶段定位**：基于 Prompt/Context/Harness/Agent OS 四阶段，盘点各子系统对应阶段——dispatch + Harness 达 S2，缺 L2 执行账本 + L4 认知层 + L5 进化层 → 优先补"断点续传 + 注意力经济 + 5 道门"
2. **Payload 禁用 send_qiwei_message**：7/21 06:30 cron 因调已废弃 MCP 工具失败 → 已在 7/21 14:06 patch 完成（announce hook + openclaw message send fallback）
3. **五层修复管道 → parameterBindings 迁移**：SKILL.md 7/21 加的"输出前自检 Gate"是 parameterBindings 雏形 → 下一步升级为可机器验证 schema
4. **三层记忆状态机落地**：State = channel memory / Working Memory = 最近 3 天作为 Pinned / Transcript = 当次 run 上下文 → "读 channel memory"升级为强制 Pinned step
5. **数据清洁优先**：L1 触发"字符 >8000 / 数组 >10" → 友盟 / 神策嵌套 JSON 加"L1 外置触发"机制
6. **注意力经济 + 优先级队列**：OpenClaw 5 个 cron 失败通知都进 AI Wiki 群容易"过载" → 借鉴"动态优先级队列"
7. **5 大关键洞察提炼**：**"LLM 越跑越蠢"是工程问题不是模型问题** / 上下文管理分层防御不是银弹 / 工具设计有半衰期（模型升级后旧防御可能变成不必要约束）/ 信任建立不能跳过人工确认

## 备注与相关链接

- **作者背景**：储旭(槿柏)，阿里巴巴 Agent 平台 S1/S2 主导者
- **5 大关键洞察**：①"LLM 越跑越蠢"是工程问题非模型问题 ②上下文管理分层防御 ③Agent 动作空间必须治理 ④工具设计有半衰期 ⑤信任建立不能跳过人工确认
- **数据规模**：S2 实现后 token -60%+，Agent 从 8 步衰减 → 30+ 步稳定执行
- **理论参考**：综合 4 篇 2022-2025 关键文献 + 4 部 1960-2008 治理经典
- **未独立验证**：④ 工具设计半衰期未给可量化指标；⑤ 信任状态机 shadow → active 转换阈值未明

- [原文链接](https://mp.weixin.qq.com/s/xH4cyBJJJlG9cfcmSU5ztA)
- [[01-ai-agents/0xCodez-Agent-Harness-14-Steps]] Harness 路线图 / [[01-ai-agents/HarnessEngineering企业级实战]] 阿里 Harness / [[loop-engineering]] Loop Engineering 验证主线