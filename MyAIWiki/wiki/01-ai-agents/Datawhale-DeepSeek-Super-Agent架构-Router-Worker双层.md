---
title: 突发！DeepSeek重磅开源：超级Agent架构！
category: 01-ai-agents
tags:
  - 主题/Agent架构
  - 主题/事件驱动
  - 主题/上下文管理
  - 手法/存算分离
  - 手法/两级过滤
  - 场景/团队级Agent底座
nodes:
  - Router 层
  - Worker 层
  - Batch 合并
  - 两级事件过滤
  - 订阅与直通路由
  - Inline & Spill
  - 链式召回
  - 投机执行
  - 异步全双工 ReAct
  - Watchdog 自愈
links:
  - "[[01-ai-agents/Harness工程AgentLoop]]"
  - "[[01-ai-agents/InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]"
  - "[[01-ai-agents/LangChainCEO-Agent越复杂-越需要自建Harness-恰恰不是]]"
  - "[[01-ai-agents/Agent时代架构师系统能力]]"
date: 2026-11-01
source: 微信公众号 / Datawhale
---

# 突发！DeepSeek重磅开源：超级Agent架构！

- 原文链接：https://mp.weixin.qq.com/s/LZxAxf0EO74YHQnZ2YOT9A
- 原始作者：Datawhale
- 发布时间：2026-10-31 22:32
- 开源仓库：https://github.com/deepseek-ai/dsh-superagent-prototype

## 核心结论（一句话）

> 把「维持全局连续性」和「高并发干活」拆成常驻 Router 与隔离 Worker，再用确定性过滤、订阅直通、局部性上下文与投机执行，让 Agent 从「拨一下动一下」变成被环境事件驱动。

## 知识节点（10 个独立概念）

- **Router 层**：永远在线，统一承接各入口交互，只做协调与分派，不配执行工具，用轻量模型即可。
- **Worker 层**：挂完整工具与最强模型，独立上下文专攻单一任务，只向 Router 汇报、不对人说话。
- **Batch 合并**：上一轮推理期间积压的事件自动合并成批，积压越多单次决策分摊成本越低（6.4 秒降至 1.6 秒）。
- **两级事件过滤**：白名单等确定性规则先走 Fast Path 滤噪，通过初筛的才交大模型做 Slow Path 语义判断。
- **订阅与直通路由**：同话题连续事件构成 Thread，Worker 订阅后新消息直通 Worker，不再麻烦 Router（决策 -30%、读缓存 Token -37%）。
- **Inline & Spill**：紧邻信息内联进窗口，超长内容溢出到窗口外只留摘要与对象 ID。
- **链式召回**：需要翻旧账时，顺着对象之间 ID 引用图一跳一跳按需检索，而不是一次性灌入。
- **投机执行**：像分支预测，看到报 Bug 不等下令先在后台试修复，成了拿出来，没成默默丢弃。
- **异步全双工 ReAct**：`run()` 拆成 `start()` / `stop()`，后台跑编译测试的同时前台可秒回新指令；IM 限 100 词，PR 出结构化报告。
- **Watchdog 自愈**：主回路之外另设定时唤醒的 Session，用模型检查 Worker 有无实质进展，支持自然语言问故障、在线热改提示词。

## 关联图谱

### 上游（基于 / 来自）

- 操作系统与 CPU 设计：批处理、分支预测、局部性原理、看门狗
- ReAct Loop：从单轮工具调用到异步全双工

### 下游（应用于 / 验证于）

- 团队级 Agent 平台：多入口（IM / PR / CI）统一到一个连续人格
- 长驻 Agent 稳定性：存算分离 + 外部 Watchdog 替代「进程还活着」的假健康

### 同级（横向 / 并列）

- [[01-ai-agents/InfoQ-TiDB-薄Agent-Loop厚Control-Plane-Harness]]：同样主张薄 Loop + 厚控制面，但走数据库可靠性路线
- [[01-ai-agents/LangChainCEO-Agent越复杂-越需要自建Harness-恰恰不是]]：对「堆 Harness」的反向主张，可与本文的四个经典设计对照

## 正文要点

**一、问题起点是人的注意力。** 一个人同时只能跟进 3 到 5 个活跃 Session，Agent 的多任务上限卡在这里，而不是算力。所以目标不是让 Agent 更聪明，是让它替人分担并发。

**二、分层的判据是「谁配拥有工具」。** Router 干脆不给 Bash，Worker 才有完整工具。这条设计比「Router 用轻模型」更本质：能力边界决定了它不会成为瓶颈，也不会因误用工具污染全局。

**三、Batch 合并让洪峰变成优势。** 常规系统里消息越多越慢，这里积压反而摊薄了单次决策成本。前提是 Router 的决策必须无状态、可推迟，否则合并会丢语义。

**四、四个设计都在回应同一个约束：上下文窗口稀缺。** 过滤是减少进入窗口的事件，直通是减少经过 Router 的中转，Inline & Spill 是压缩单次入窗体积，投机执行是把探索挪到窗口之外。

**五、信噪比决定架构形态。** 真实群聊高噪音低触发率，所以必须两级过滤；如果场景是低频高价值事件，直接上大模型判断反而更简单。这套架构不适合稀疏场景。

**六、稳定性判据从「进程活着」改成「有实质进展」。** Watchdog 用模型看 Worker 有没有推进，这是把「空转」这一最隐蔽的故障显性化。对长驻 Agent 来说，空转比崩溃更贵。

## 对 Seetong 团队可借鉴动作

- **别把巡检和深挖塞进同一个流程**：类似 Router / Worker，定时巡检只做「发现与分派」，深挖另起隔离上下文，避免一次排查污染整条链路。
- **给长任务加「进展判据」而非只看退出码**：现有脚本以「文件是否落盘」判成功是对的，但应再加「内容是否实质推进」，防止 agent 写出空壳报告也算成功。
- **积压场景优先做批处理**：反馈雷达一次扫上百条反馈，若每条都单独调模型会很贵；聚成批一次判断，成本随积压下降。
- **投机执行可用于 Bug 复现**：新反馈进来先自动尝试复现与定位，有结论再叫人，没结论不留噪音。
- **上下文用 ID 引用而非全文重灌**：Logan、TAPD、反馈记录之间用 ID 串起来按需取，比一次性全塞进 prompt 更省也更能追问。

## 备注与限制

- 全部性能数字（6.4→1.6 秒、30% / 37%、p95 15.7 vs 29.5 分钟）转述自 DeepSeek 官方长文，未给实验条件与样本量。
- 仓库名为 `dsh-superagent-prototype`，是原型，不宜直接按生产级方案采纳。
- 「Session 焦虑」「链式召回」「投机执行」为原文用语，非官方术语。

## 相关链接

- [原文摘要](../../raw/2026-10-Datawhale-DeepSeek-Super-Agent架构-Router-Worker双层-digest.md)
- [开源仓库](https://github.com/deepseek-ai/dsh-superagent-prototype)
