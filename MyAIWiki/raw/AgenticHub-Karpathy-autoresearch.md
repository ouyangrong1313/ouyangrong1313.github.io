# Karpathy重磅论文拆解：从上下文工程到 AI Agent DAG

- 原文链接：https://mp.weixin.qq.com/s/uYb5AzpAwHBHhO29_cvi_Q
- 来源：微信公众号「AgenticHub」
- 署名：南七技校
- 发布时间：2026-07-27 21:30:13 Asia/Shanghai
- 获取时间：2026-07-28
- 一手来源：Andrej Karpathy / `karpathy/autoresearch`
  - 仓库：https://github.com/karpathy/autoresearch
  - README：https://github.com/karpathy/autoresearch/blob/master/README.md
  - Agent 指令：https://github.com/karpathy/autoresearch/blob/master/program.md
  - 进展更新：https://x.com/karpathy/status/2031135152349524125

---

## 正文

Karpathy 最近发布了一套围绕 `nanochat` 的自动研究实验：让 AI Agent 反复修改训练代码，在固定预算内训练和评分，只保留有效改动。

公众号将这一模式概括为从 Context Engineering 走向 Agent DAG，并给出以下结论：

- 两天内执行约 700 次实验；
- 发现 4 个代码 Bug；
- 训练时长从 2.02 小时降到 1.80 小时，提升约 11%；
- `nanochat` 仓库在约四个月内获得 90,900 Star。

文章认为，核心不再只是模型本身，而是可持续运行的 Agent 架构。其给出的闭环是：

1. Agent 修改代码；
2. 在固定预算内运行测试；
3. 指标变好则 Git 提交，变差则 Git 回滚。

文章将这个只进不退的机制称为 Ratchet（棘轮）。

随后文章给出六个实践步骤：

1. **寻找单一评分指标**：用一个可自动比较的数字定义目标，而不是“让代码更好”这类主观目标。
2. **物理隔离评分文件**：评分逻辑和数据准备文件不可修改，Agent 只能改可编辑区，防止通过改评分标准获得高分。
3. **锁定时间预算**：每次尝试必须在相同的时间预算内执行，才能让分数可比。
4. **写入永不暂停指令**：在 Agent 指令中要求它开始实验后持续推进，不因礼貌性确认而停下。
5. **睡眠时运行，醒来读 Diff**：不只依赖 Agent 的文字总结，而用 Git Diff 和实验日志核验结果。
6. **从单循环扩展到 DAG**：文章建议多 Agent 使用独立 Git Worktree，避免同时修改同一目录，并把演进后的形态称为 Agent DAG。

文章最后的结论是：竞争焦点从训练更大的模型转向构建更可靠的循环。

---

## 一手来源核验

### 已确认

Karpathy 的一手原文不是“9 页 PDF”，而是 GitHub 仓库 `karpathy/autoresearch`。仓库于 2026-03-06 创建，README 将其定义为：让 AI Agent 在单 GPU 的 `nanochat` 简化训练环境中自主试验，修改代码、训练 5 分钟、检查结果、保留或丢弃改动，然后继续循环。

官方基线由三个关键文件组成：

- `prepare.py`：固定常量、数据准备、数据加载和评测；不可修改。
- `train.py`：唯一允许 Agent 修改的训练代码。
- `program.md`：由人维护的 Agent 指令，定义实验循环和约束。

官方固定的比较条件：

- 训练时间预算：300 秒，即 5 分钟。
- 评价指标：`val_bpb`，越低越好。
- 评测实现：`prepare.py` 的 `evaluate_bpb`，不可修改。
- 保留规则：指标改善则保留当前 Git commit；相同或变差则回退。
- 实验账本：`results.tsv` 记录 commit、指标、显存、状态和尝试说明。

Karpathy 在 2026-03-26 的公开更新中报告：约两天、约 700 次实验、约 20 项保留改进，训练时间从 2.02 小时降至 1.80 小时。

### 不应作为官方实现事实

- **“9 页 PDF”**：官方可验证的一手材料是 GitHub README、`program.md` 与代码，不是论文 PDF。
- **“发现 4 个 Bug”**：未在 README、`program.md` 或该公开更新中得到确认；不要以此作为实现依据。
- **“Prompt Engineering 已过时”**：官方仓库没有作出这一结论。它强调把 Agent 的长期上下文和循环规则写进 `program.md`。
- **“Agent DAG + 独立 Worktree 是官方基线”**：官方 README 只说未来可加入更多 Agent；默认 `program.md` 是一个 Agent 在专用分支上运行，未定义 DAG 或 Worktree 编排方案。

标签： #主题/AI-Coding #主题/AI-Agent #主题/Loop-Engineering #主题/Context-Engineering #节点/autoresearch #节点/固定评分器 #节点/棘轮提交 #节点/不可变评测 #场景/公众号长文
