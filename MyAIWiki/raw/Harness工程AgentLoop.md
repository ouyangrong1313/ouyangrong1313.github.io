# Harness 工程：Agent Loop 从Demo到工业级

## 基础信息

- **来源**: 微信公众号 - AI技术研习社
- **原文链接**: https://mp.weixin.qq.com/s/OPwgRVnf3_eXr6ut_gyoGQ
- **抓取时间**: 2026-05-07
- **主题标签**: Agent工程, Harness, Agent Loop, 工业级落地

---

## 核心内容

### 一、核心认知：Agent ≠ Model

**Agent工程第一定律**：
```
Agent = Model + Loop + Tools + Context Management
```

LLM 本身是**绝对无状态**的（Stateless），每次推理都是"输入→输出"一次性函数，生命周期瞬间结束。

Agent 的"自主性"来自模型外部的 Agent Loop，而非模型本身。

### 二、最小可运行 Agent Loop（20行伪代码）

```python
messages = []
while True:
    # 1. 模型推理
    response = llm(messages, tools=available_tools)
    messages.append(response)
    
    # 2. 终止路由
    if response.stop_reason != "tool_use":
        return response.text
    
    # 3. 工具执行
    for tool_call in response.tool_calls:
        result = execute(tool_call)
        messages.append({"role": "tool", "content": result})
    
    # 4. 进入下一轮循环
```

**核心洞察**：模型的思考永远只发生在 llm() 被调用的那一瞬间，Loop 作为"系统节拍器"，不断将更新后的世界状态推送到模型面前。

### 三、Harness 的 5 个关键工程决策

#### 1. 生命周期管理（防止失控）

- 自然终止：模型主动停止
- 安全熔断（Max Iterations）：硬性步数上限
- 状态僵死检测：连续调用相同工具+相同参数 → 强制打断
- 资源配额：Token 消耗量 / 执行时间超时控制

#### 2. 上下文生命周期管理（解决"记不住"）

| 策略 | 适用场景 | 缺点 |
|------|---------|------|
| 全量回灌 | 极短任务 | 成本高 |
| 滑动窗口 | 简单任务 | 易丢失早期约束 |
| 摘要压缩 | 中等任务 | 信息损耗 |
| 分层状态树（最佳）| 长程任务 | 复杂 |

参考 Claude Code 的 `/compact` 机制：保留"最近操作流水+历史摘要+关键状态表"。

#### 3. 工具挂载机制

- **原生 Function Calling**：结构化约束高，主流稳定方案
- **Prompt 约定解析**（如 ReAct XML 标签）：适配无 FC 能力的小模型

#### 4. 容错与自愈

- **内环自愈**：将报错无损塞回 Context，依赖模型逻辑纠错
- **外环拦截**：Harness 层捕获致命错误，执行重试/降级/报警
- **混合范式（推荐）**：业务逻辑异常交模型，系统异常由 Harness 接管

#### 5. 调度拓扑

- **单 Agent 并发**：模型单次输出多个 Tool Call，Harness 并行处理
- **多 Agent 协同**：主 Agent（Planner）+ 子 Agent（Executor），状态隔离

### 四、从原型到工业级演进路径

开源项目：learn-claude-code（https://github.com/shareAI-lab/learn-claude-code）

```
阶段1：基础连通期（s01-s02）
  - s01: 打通"模型→工具"管道，完成基础闭环
  - s02: 多工具挂载 + dispatch map

阶段2：稳定性提升期（s03-s06）
  - s03: TodoWrite 工具，防止目标漂移
  - s04: Subagent 状态隔离
  - s06: Context Compact，三层压缩策略

阶段3：工业化成熟期（s07-s12）
  - 任务持久化、后台任务、多 Agent 团队协同、工作目录隔离
```

### 五、生产环境 4 大失效场景

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 上下文雪崩 | 信息信噪比下降 + 多次压缩损耗 | 分层状态树 + 定期自省（Reflection） |
| 工具幻觉 | 模型虚构未注册工具/参数 | Harness 层 Schema 校验 |
| 状态机死锁 | 陷入局部最优无法跳出 | LLM-as-a-Judge 动态轨迹评估 |
| 目标发散 | 执行数十步后偏离核心诉求 | 上下文压缩 + 工具白名单 + 步数预算 |

### 六、核心法则

> **The model is the agent. The code is the harness.**

模型即 Agent 本体，代码皆为脚手架。Harness 的唯一职责是"搭好舞台，防它出错"。

### 七、Harness 会消失吗？

- **可能被吞噬**：模型进化后，内部推理链+原生 Tool Use 可能替代外部 Loop
- **不会消失的理由**：企业级应用永远需要确定性——数据库、文件系统、沙箱环境，需要权限管控和操作审计

---

## 相关资源

- GitHub: https://github.com/shareAI-lab/learn-claude-code
- 开源项目演进：s01 → s12，从 50 行到 1000 行工业级脚手架