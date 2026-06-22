---
title: 淘宝主播 Agent 的 Harness 工程实战
category: 01-ai-agents
tags: [#主题/Harness, #主题/AI-Agent, #主题/工程实践, #主题/记忆系统, #主题/AI安全, #主题/阿里, #场景/直播, #场景/生产环境]
nodes: [Harness-六元组, 业务框架分层, 逻辑统一物理分治, Reducer-上下文模式, 工具调用三件套, 生命周期Hook, 五层纵深防御, 记忆对账-信任度自进化]
links: [[Harness工程AgentLoop]], [[HarnessEngineering企业级实战]], [[0xCodez-Agent-Harness-14-Steps]], [[harness-engineering]], [[阿里妹-端到端业务需求专家Agent-4层架构8步流程]], [[记忆是-agent-基建]], [[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]], [[腾讯-AI-Agent-Skill-测评方案落地]], [[从零设计生产级-Multi-Agent-Harness]]
date: 2026-06-18
source: 微信公众号 / 阿里云开发者(阿里妹系列) 2026-06-17 08:30
原始链接: https://mp.weixin.qq.com/s/Mv5U5kr_viixmB0JJronPA
---

# 淘宝主播 Agent 的 Harness 工程实战

> **核心结论**:把 Harness 从"个人助手"推到"淘宝主播"高风险生产场景后,工程骨架的本质是**业务/框架彻底分层 + 物理存储分治(MySQL/Hologres/GitLab)+ 纵深防御 5 层 + 记忆对账信任度闭环**——不是"加更多规则",而是把"会变的"和"不变的"拆成两层独立演化。

## 8 个知识节点

- **Harness 六元组 (E, T, C, S, L, V)**:Execution Loop + Tool Registry + Context Manager + State Store + Lifecycle Hooks + Evaluation Interface。把零散 Prompt 升级为有明确分工的系统架构,经验是"六块少一块,某天就崩在那一块"。
- **业务/框架分层架构**:业务方以 Skill 形式声明"能干什么 / 风险等级 / 参数校验",框架层兜住执行循环/上下文/安全/状态/观测这些不变能力。**判断原则:不变的放框架,会变的放业务**——业务迭代和工程质量解耦。
- **逻辑统一 / 物理分治**:逻辑上向 Agent 暴露统一"工作区";物理上三类资产分存——**MySQL 存会话**(强一致+点查)/ **Hologres 存记忆**(向量+全文+标量三路召回)/ **GitLab 存 Skill**(版本管理+灰度)。反直觉:不是一套存储硬扛所有负载,而是按读写特征各选最优。
- **Reducer 上下文模式**:LLM 只决策(产生 Action),Reducer 函数负责状态变更(纯函数、确定性)。每轮对话前把最新 State 通过 system-hint 注入,模型看到"当前商品 SKU / 价格 / 库存 / 目标"快照,而不是从 20 轮历史大海捞针。**三件事一次解决**:状态模糊/上下文膨胀/不可回放。
- **工具三件套 + 结构化错误码**:① 能力边界声明(防越权) ② Schema 强约束 + 幂等性(写操作必带 UUID 幂等键,防"双切品/双改价"灾难) ③ 错误码 3xxx 换策略/4xxx 修参数 1 次/5xxx 退避 3 次/9xxx 通知主播。
- **生命周期 Hook 5 个时机**:PreReasoning(注入 State+场景记忆)/ PreToolCall(能力+幂等+风险)/ PostToolCall(交叉验证+Reducer)/ PostReasoning(幻觉检测)/ SessionEnd(记忆回写)。Hook 把"安全/可观测/演化"从业务解耦到框架层。
- **五层纵深防御 + Approval 4 档**:Prompt 边界 → Schema → Approval(**auto/soft-gate/hard-gate/block**)/ 工具验证 → 审计。前一层漏掉由后一层兜底;hard-gate 阻塞等主播二次确认无超时,block 触发平台红线即时拒绝。
- **记忆三层 + 记忆对账 + 信任度自进化**:L1 主播主观声明 / L2 实时数据 / L3 行为聚合。**核心反直觉**:"主播'说的'和'做的'矛盾时不粗暴覆盖 L1,而是累积证据 ≥ 3 次后由 Agent 主动和主播确认"——避免"AI 自作主张改了我的设定"破坏信任。trust_score 非对称更新(采纳好 +0.05 / 采纳差 -0.10 / 拒绝主播对 -0.05 / 拒绝 Agent 对 +0.03),反向决定输出形态(≥0.7 recommend / 0.4-0.7 弱参考 / <0.4 仅 evidence)。

## 关联图谱

### 上游(基于 / 来自)
- **Harness Engineering 概念走红**:OpenClaw、Claude Code、Hermes 把"模型是概率的、会漂移的,真正让 Agent 可用可控的是外面那层骨架"这个主张带火
- **ATA "水流理论"**:人控制方向+设定边界,AI 在边界内推进,工程师建"河道、闸门、护栏"
- **前端 Reducer 状态管理**:LLM = Action(决策),Reducer = State(纯函数状态变更),system-hint = 状态快照注入

### 下游(应用于 / 验证于)
- **淘宝主播生产环境**:每日数千场直播,操作即时生效,错误代价真金白银
- **PlanEngine vs ReAct 评测**(基模 qwen3.7-max,平均 7 步 query):执行成功率 **0.847 vs 0.737** / 子任务覆盖率 **0.976 vs 0.883** / 工具执行冗余率 **0.587 vs 0.727** / 迭代轮次 **5.440 vs 8.020**
- **Langfuse trace + 离线对抗样本**(极端改价/违规诱导/模糊指令)+ 在线指标看板(操作成功率/审批通过率/主播干预率/端到端延迟)

### 同级(横向 / 并列)
- Harness 主线:[[Harness工程AgentLoop]] / [[HarnessEngineering企业级实战]] / [[0xCodez-Agent-Harness-14-Steps]] / [[harness-engineering]]
- 阿里妹同源:[[阿里妹-端到端业务需求专家Agent-4层架构8步流程]]
- 记忆主线:[[记忆是-agent-基建]] / [[llm-agent-unified-memory-framework]]
- Loop 主题:[[Addy-Osmani-Loop-Engineering]] / [[Loop-Engineering-详解-把反馈循环放进工程现场]] / [[APPSO-Codex-Claude-Code-Loop-Engineering]]
- Agent 安全+评测:[[陈进-读完Agent-Loop工程手册-我有8个还没想明白的问题]] / [[腾讯-AI-Agent-Skill-测评方案落地]]
- Agent 架构:[[从零设计生产级-Multi-Agent-Harness]] / [[OpenClaw-vs-Hermes-多-Agent-架构设计]]

## 5 个对 Seetong 团队可借鉴动作

1. **Harness 六元组体检**:给 Seetong 所有 Skill 落表自查 E/T/C/S/L/V 缺哪一块,补缺后再谈"提升效率"——不要先优化"能跑但不知道对不对"的流程。
2. **业务/框架分层重写 Skill 库**:`seetong-tapd-version-review` / `seetong-bug-triage` / `seetong-daily-briefing` / `seetong-prd` / `seetong-decompose` 现在"业务规则+工程实现"混在一起,业务一变就要动骨架。改成"**Skill 声明 = 能干什么+风险等级+参数校验,框架兜住上下文/状态/Hook/观测**",业务迭代不再踩工程。
3. **记忆三层 + 记忆对账用到简报**:`seetong-daily-briefing` 现在是 L1 一句话,缺 L2(神策/友盟/TAPD)和 L3(运营类别)。加 L2+L3 就能给"主播说的关注点 vs 实际数据高发"对账,矛盾 ≥ 3 次触发主动确认。
4. **Approval 4 档作为 Seetong Agent 操作硬规则**:自动关过期迭代=auto,自动打标签=soft-gate,自动修 7 天未响应 Bug=hard-gate(阻塞等二次确认),自动改版本号/动主分支=block 即时拒绝。与 [[Claude-Code一周年回顾-Boris-Cat]] "Auto Mode 比手动更安全"合并用。
5. **写"Seetong PlanEngine" 7 天小试点**:挑"每周版本回顾"按 PlanEngine 5 目标(可恢复 Checkpoint/可观测 TraceID/并行调度/增量 Replan/SubAgent 隔离)重写,7 天后用 5 项指标对比 PlanEngine vs 原 ReAct。

## 备注与限制

- 作者署名未标注(推断阿里/淘宝直播技术团队)
- 微信抽取时第 2.6 节"响应超时"行被截断
- "矛盾累积 ≥ 3 次"是经验阈值,无实验数据
- trust 4 档输出形态无具体话术模板
- 主播 Agent A/B 验证数字未披露
- 沙箱 64KB stdout 是经验值,未给不同业务量级最优阈值
- 原始链接:https://mp.weixin.qq.com/s/Mv5U5kr_viixmB0JJronPA
- raw:[../../raw/2026-06-17-阿里云开发者-淘宝主播Agent的Harness工程实战.md](../../raw/2026-06-17-阿里云开发者-淘宝主播Agent的Harness工程实战.md) | raw-digest:[../../raw/2026-06-17-阿里云开发者-淘宝主播Agent的Harness工程实战-digest.md](../../raw/2026-06-17-阿里云开发者-淘宝主播Agent的Harness工程实战-digest.md) | wiki-digest:[./阿里云开发者-淘宝主播Agent的Harness工程实战-digest.md](./阿里云开发者-淘宝主播Agent的Harness工程实战-digest.md)
