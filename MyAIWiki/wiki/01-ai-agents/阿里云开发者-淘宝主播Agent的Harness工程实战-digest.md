---
title: 淘宝主播 Agent 的 Harness 工程实战(速读摘要)
category: 01-ai-agents
tags: [#主题/Harness, #主题/AI-Agent, #主题/工程实践, #主题/记忆系统, #主题/AI安全, #主题/阿里, #场景/直播]
type: digest
date: 2026-06-18
source: 微信公众号 / 阿里云开发者(阿里妹系列) 2026-06-17
原始链接: https://mp.weixin.qq.com/s/Mv5U5kr_viixmB0JJronPA
---

# 淘宝主播 Agent 的 Harness 工程实战(速读摘要)

> **一句话**:Harness = 业务/框架分层 + 物理分治(MySQL/Hologres/GitLab)+ 纵深防御 5 层 + 记忆对账信任度闭环。

## 速查表

| 维度 | 核心命题 | 关键数字/设计 |
|---|---|---|
| Harness 形式化 | 6 元组 (E, T, C, S, L, V) | 主循环/工具/上下文/状态/Hook/评测 |
| 业务/框架分层 | 不变放框架,会变放业务 | 业务方写 Skill 声明,框架兜底 |
| 物理分治 | 三类资产三套存储 | MySQL(会话)/ Hologres(记忆)/ GitLab(Skill) |
| 上下文 | LLM 决策,Reducer 管状态 | system-hint 注入快照 |
| 工具三件套 | 边界+Schema+幂等 | 写操作必带 UUID 幂等键 |
| 错误码 | 3xxx/4xxx/5xxx/9xxx | 换策略/修参数/退避 3 次/通知 |
| Hook 5 时机 | 横切关注点解耦 | PreReasoning / PreToolCall / PostToolCall / PostReasoning / SessionEnd |
| 沙箱 | 不信任何输入 | CPU ≤ 50%,进程 ≤ 64,timeout 只能缩小,stdout 64KB |
| 5 层防御 | Prompt→Schema→Approval→验证→审计 | 前层漏后层兜 |
| Approval 4 档 | 风险分级 | auto / soft-gate / hard-gate(block) |
| DAG vs ReAct | 5 子任务平均 7 步 | 成功率 0.847 vs 0.737,冗余 0.587 vs 0.727,迭代 5.44 vs 8.02 |
| 记忆三层 | L1 主观/L2 事实/L3 行为 | L1 反映声明,L2+L3 给客观信任度 |
| 记忆对账 | 矛盾累积 ≥ 3 次才覆盖 | 不粗暴覆盖 L1,主动提示 |
| trust 增量 | 非对称 | 采纳好+0.05/采纳差-0.10(给错更伤)/ 拒绝主对-0.05/ 拒 Agent 对+0.03 |
| trust 决定输出 | ≥0.7 recommend / 0.4-0.7 弱参考 / <0.4 仅 evidence | 自适应输出形态 |

**5 个反直觉点**:① 不是"加规则"而是"分层独立演化" ② 不是"一套存储硬扛"而是"逻辑统一物理分治" ③ 不是"LLM 记住一切"而是"LLM 决策 + Reducer 管状态" ④ 不是"新覆盖旧"而是"矛盾累积等用户确认" ⑤ 不是"信任均匀增长"而是"非对称更新"——给错建议比不给更伤信任。

## 5 个对 Seetong 团队可借鉴动作

1. **Harness 六元组体检**:给 Seetong 所有 Skill 落表自查 E/T/C/S/L/V,补缺后再谈提升效率
2. **业务/框架分层重写 Skill 库**:`seetong-tapd-version-review` / `seetong-bug-triage` / `seetong-daily-briefing` 改"Skill 声明+框架兜底"
3. **记忆三层用到简报**:`seetong-daily-briefing` 加 L2(神策/友盟/TAPD)+ L3(运营类别),矛盾 ≥ 3 次主动确认
4. **Approval 4 档作为操作硬规则**:auto/soft-gate/hard-gate/block,合并 [[Claude-Code一周年回顾-Boris-Cat]] "Auto Mode 比手动更安全"
5. **写"Seetong PlanEngine" 7 天小试点**:周报流程按 PlanEngine 5 目标重写,5 项指标对比 vs ReAct

## 关联 + 备注

**关联**:Harness 主线 [[Harness工程AgentLoop]] / [[HarnessEngineering企业级实战]] / [[0xCodez-Agent-Harness-14-Steps]] / [[harness-engineering]] | 阿里妹同源 [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]] | 记忆 [[记忆是-agent-基建]] / [[llm-agent-unified-memory-framework]] | Loop [[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]] | Agent 安全+评测 [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] / [[腾讯-AI-Agent-Skill-测评方案落地]]

**备注**:作者署名未标注 / 2.6 节"响应超时"行被截断 / "矛盾累积 ≥ 3 次"经验值 / trust 4 档无话术模板 / 主播 Agent A/B 数字未披露 / 沙箱 64KB 是经验值
