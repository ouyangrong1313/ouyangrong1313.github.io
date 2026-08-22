---
title: "DeepSeek Harness 拆解：一套能拼装的 Agent 架构"
category: 01-ai-agents
tags:
  - 主题/AI-Agent
  - 主题/Harness
  - 主题/插件运行时
  - 主题/运行时架构
  - 节点/可逆副作用
  - 节点/Fiber生命周期
  - 节点/Scope继承
  - 节点/Code-Mode
  - 场景/公众号长文
nodes: [一切皆插件, 可逆副作用, Fiber生命周期, effect撤销栈, 系统边界, Scope继承, Code-Mode隔离, 工具遮蔽]
links: ["[[01-ai-agents/Harness工程AgentLoop]]", "[[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]", "[[01-ai-agents/2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]]", "[[02-ai-coding/Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]"]
date: 2026-08-17
source: "微信公众号「腾讯程序员」/ DeepSeek Harness 二手技术解读"
---

# DeepSeek Harness 拆解：一套能拼装的 Agent 架构

- 原文：https://mp.weixin.qq.com/s/DeIty-Nn8tQvE4osy7_bpg
- 作者：chino（腾讯 WXG 微信小店前端开发工程师）
- 发布时间：2026-08-14 17:20 CST；获取时间：2026-08-17

## 核心结论（一句话）

> DeepSeek Harness 将 agent loop、模型、工具、会话和 UI 都放入以 Cordis 为中心的插件生命周期；其关键不只是可扩展，而是让每项副作用都携带可执行的逆操作，使热更新、替换和失败清理尽量收敛到插件边界。

## 分类提炼

- 场景：Agent Runtime、插件化 Harness、热更新、工具治理、Code Mode
- 类型：二手源码解读 / 运行时架构拆解

## 知识节点（8 个独立概念）

- **一切皆插件**：模型接入、工具、会话、循环和界面使用同一插件运行时组织，减少不可替换的特殊核心。
- **可逆副作用**：每次共享环境修改登记对应 disposer，卸载时按逆序执行以清理影响。
- **Fiber生命周期**：插件实例通过 PENDING 到 ACTIVE、FAILED、UNLOADING 等状态等待依赖、运行和收束。
- **effect撤销栈**：事件、服务、定时器和子组件由 `ctx.effect()` 登记，子组件随父 Fiber 级联清理。
- **系统边界**：框架可跟踪 Context 内操作；公共资源、全局变量和已发射数据不自动可逆。
- **Scope继承**：预设插件树可真实挂载一次，会话通过逻辑父子关系复用和继承。
- **Code-Mode隔离**：模型代码经隔离执行环境以消息通道调用工具，并复用统一工具管线。
- **工具遮蔽**：工具按 scope 层叠、限制与当前层直接注册计算可见性，令预设能局部覆盖能力。

## 可逆插件运行时

原文将 Cordis 与普通 DI 或钩子扩展区分开来：重点不是“如何把逻辑挂进去”，而是“如何在依赖变化、HMR 或初始化失败时把它完整拿出来”。插件通过 `ctx.effect()` 执行副作用并返回清理函数；运行时按照 LIFO 收集和调用，父 Fiber 的释放会级联到子 Fiber。

这使卸载成为与加载对称的一等操作：HMR、运行时装卸、失败中断都可在结构上触发清理。不过运行时只能保证清理函数被调用，不能证明清理函数语义正确。对共享外部资源，需通过 service 封装访问与补偿逻辑，不能把“可逆”外推到所有副作用。

## Scope、Code Mode 与工具治理

预设由真实 Cordis scope 承载，而会话到预设采用逻辑绑定，目标是共享已挂载的插件实例。工具可见性按全局层、祖先 scope、限制规则和当前 scope 的直接注册逐层计算；注册工具本身亦被视为 effect，插件退出时应自动撤销。

Code Mode 的设计目标是让模型在一次隔离执行中编排多次工具调用，减少逐轮交互。原文称 DSH 使用 `worker_threads` 并以消息通道回到统一工具执行内核；它与 Codex V8 isolate 的对比是二手解读，适合作为“隔离模型与运行时取舍”的研究线索，而不是实现事实的直接依据。

## 采用边界

- 不把“插件可卸载”误当成“任何外部效果都可回滚”；不可逆操作必须有延迟发射、补偿或人工确认策略。
- 对长期服务，先将资源访问收敛进可测试的 service，再考虑热更新和插件自修改。
- 对 Code Mode，隔离、资源限额、可中断性和与普通工具调用相同的策略检查缺一不可。
- 原文的源码细节、生态规模与产品前景未经本条目独立验证，应回到 DeepSeek Harness 和 Cordis 的对应版本资料复核。

## 关联图谱

### 上游（基于 / 来自）
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]：将 Harness 视为围绕模型的运行系统；本文给出插件生命周期与可逆副作用的具体实现视角。
- [[01-ai-agents/Harness工程AgentLoop]]：提供 Agent Loop 工程决策背景；本文讨论如何让 loop 本身也成为可替换组件。

### 同级（横向 / 并列）
- [[01-ai-agents/2026-07-29-人月聊IT-通用AI-Agent平台-Harness技术底座]]：该文按能力面列底座；本文按插件运行时的生命周期、边界与作用域机制展开。
- [[02-ai-coding/Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]：两者都关注 Harness；本文的 Codex 比较仅保留为二手技术线索。
- [[01-ai-agents/叶小钗-DeepSeek-Harness-实测]]：同样解读 DSH；该文补充服务依赖、消息调度、Session 重建与单任务体验结果的证据边界。

## 相关链接

- [原文](https://mp.weixin.qq.com/s/DeIty-Nn8tQvE4osy7_bpg)
- [原文归档](../../raw/腾讯程序员-DeepSeek-Harness-可逆插件运行时.md)
- [速读摘要](../../raw/腾讯程序员-DeepSeek-Harness-可逆插件运行时-digest.md)
