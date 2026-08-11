---
title: Karpathy autoresearch：从上下文工程到自主研究循环
category: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 主题/AI-Agent
  - 主题/Loop-Engineering
  - 主题/Context-Engineering
  - 节点/autoresearch
  - 节点/固定评分器
  - 节点/单文件搜索空间
  - 节点/五分钟预算
  - 节点/val_bpb
  - 节点/棘轮提交
  - 节点/实验账本
  - 节点/多Agent扩展边界
  - 场景/开源实现
nodes: [autoresearch, 固定评分器, 单文件搜索空间, 五分钟预算, val_bpb, 棘轮提交, 实验账本, 多Agent扩展边界]
links: [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]], [[01-ai-agents/Loop-Engineering-验证才是瓶颈]], [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]], [[02-ai-coding/Agentic-Engineering-AI-Workbench]], [[02-ai-coding/AndrejKarpathy-AI写代码-只需要问自己这一个问题]]
date: 2026-07-28
source: 微信公众号「AgenticHub」二手解读；Andrej Karpathy GitHub 一手实现
---

# Karpathy autoresearch：从上下文工程到自主研究循环

- 二手原文：https://mp.weixin.qq.com/s/uYb5AzpAwHBHhO29_cvi_Q
- 一手实现：https://github.com/karpathy/autoresearch
- 一手规则：[`program.md`](https://github.com/karpathy/autoresearch/blob/master/program.md)
- 一手进展更新：https://x.com/karpathy/status/2031135152349524125
- 公众号发布时间：2026-07-27 21:30 Asia/Shanghai
- 官方仓库创建：2026-03-06；获取时 Star：92,180（2026-07-28）
- 原始素材：`../../raw/AgenticHub-Karpathy-autoresearch.md`
- 速读摘要：`../../raw/AgenticHub-Karpathy-autoresearch-digest.md`

## 核心结论（一句话）

`autoresearch` 的可复用部分不是“让 Agent 永不停止”，而是把自主试验限制在一个可证明进步的闭环里：**不可变评分器、单一可编辑面、固定预算、结果账本和 Git 回退**。

## 分类提炼

- 场景：模型训练优化 / 可验证 AI Coding / 自主试验循环
- 类型：开源实现原典 + 二手文章事实核验
- 核心约束：单 GPU、固定 5 分钟、`val_bpb` 越低越好、`prepare.py` 不可修改
- 非目标：通用业务 Agent、生产发布自动化、官方定义的多 Agent DAG

## 知识节点

- **autoresearch**：Karpathy 的单 GPU 自主研究最小实现；Agent 连续改变训练代码，并通过固定评测筛选改动。
- **固定评分器**：`prepare.py` 中的 `evaluate_bpb` 是不可编辑的真值来源；一旦评分器可改，实验比较就失效。
- **单文件搜索空间**：默认只允许 Agent 改 `train.py`，把架构、优化器、超参数和训练循环的探索范围限制在可审查的 Diff 内。
- **五分钟预算**：`TIME_BUDGET = 300` 秒；每次训练时间一致，才可比较不同模型与参数选择。
- **val_bpb**：验证 bits per byte，词表大小无关，越低越好；它是 keep/discard 的唯一硬判据。
- **棘轮提交**：先提交实验，再运行；指标改善即保留该 commit，持平或变差就回退，不让未验证改动污染分支。
- **实验账本**：`results.tsv` 单独记录 commit、指标、显存、状态和描述；日志是可审计的实验史，不应只相信 Agent 总结。
- **多Agent扩展边界**：DAG 和 Worktree 并非官方基线；在扩展前必须先定义任务拆分、共享指标、冲突归因和最终合并权。

## 一手核验

| 主题 | 一手实现 | 公众号处理 |
|---|---|---|
| 原文形态 | GitHub 仓库、README、`program.md` 与代码 | “9 页 PDF”不成立 |
| 实验规模 | Karpathy 更新：约 2 天、约 700 次实验 | 可引用 |
| 结果 | Karpathy 更新：约 20 项保留改进，2.02 小时到 1.80 小时 | “4 个 Bug”未证实 |
| 控制机制 | 固定评测、固定时长、Git keep/reset、TSV 账本 | 可作为实现主线 |
| Agent DAG | README 仅提及未来可增加更多 Agent | Worktree/DAG 是扩展设计，不是原项目默认架构 |

## 最小实现路径

官方仓库的运行条件是单张 NVIDIA GPU、Python 3.10+ 与 `uv`，并已在 H100 上测试。先在隔离环境按官方步骤跑通基线：

```bash
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch
uv sync
uv run prepare.py
uv run train.py
```

之后再让 Agent 执行 `program.md` 定义的循环：

1. 阅读 `README.md`、`prepare.py` 和 `train.py`，确认缓存数据与 tokenizer 已准备好。
2. 创建独立实验分支与未跟踪的 `results.tsv`，先记录未改代码的基线。
3. 只修改 `train.py`，提交改动并运行一次 5 分钟训练。
4. 从日志提取 `val_bpb` 与显存；失败则记录 `crash`。
5. `val_bpb` 更低才保留当前 commit，否则回退到实验前状态。
6. 继续下一项假设；每日审阅 Diff、TSV 和最优 commit，而不是只读文字总结。

## 迁移规则

将该模式迁移到非训练任务时，先补齐这五项，缺一项就不要启动无限循环：

1. **不可变 verifier**：独立于 Agent 修改面，可自动判定好坏。
2. **可比较预算**：固定时间、成本或样本集，避免实验口径漂移。
3. **最小写入面**：优先单文件、单模块或可隔离 Worktree。
4. **回退状态机**：只有 verifier 通过才允许推进分支或合并。
5. **人工停止边界**：生产、外部副作用、数据与安全路径不能照搬 `NEVER STOP`。

## 关联图谱

### 上游（基于 / 来自）

- Karpathy `autoresearch`：一手代码、评测约束和 Agent 循环的唯一事实基线。
- [[01-ai-agents/Lilian-Weng-Harness-Engineering-自我改进]]：将 autoresearch 归为工作流自动化的干净案例。
- [[01-ai-agents/Loop-Engineering-验证才是瓶颈]]：补充“循环是否值得运行取决于验证器”的通用原则。

### 下游（应用于 / 验证于）

- [[02-ai-coding/Code-is-cheap-AI-Native-五倍效率]]：将“高频生成”放入 checkpoint 与多层验证的工程框架。
- [[02-ai-coding/Agentic-Engineering-AI-Workbench]]：把受控计划、隔离和验证迁移到常规软件工程工作台。

### 同级（横向 / 并列）

- [[02-ai-coding/AndrejKarpathy-AI写代码-只需要问自己这一个问题]]：同样讨论 AI 承担执行的边界，但重点是“何时交给 AI”，本页重点是“交给 AI 后怎样形成可回退的研究循环”。

## 相关链接

- 官方仓库：https://github.com/karpathy/autoresearch
- 官方 README：https://github.com/karpathy/autoresearch/blob/master/README.md
- 官方 `program.md`：https://github.com/karpathy/autoresearch/blob/master/program.md
- 官方 `prepare.py`：https://github.com/karpathy/autoresearch/blob/master/prepare.py
- 官方 `train.py`：https://github.com/karpathy/autoresearch/blob/master/train.py
- 公众号原文：https://mp.weixin.qq.com/s/uYb5AzpAwHBHhO29_cvi_Q
