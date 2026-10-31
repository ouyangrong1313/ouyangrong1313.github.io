# Agent Skills 系统性综述

**来源：** PaperToday
**原文：** [来了，首篇Agent Skills系统性综述！](https://mp.weixin.qq.com/s/UZi_lfZwjq8KFf4dbTtEjQ)

---

## 核心结论

Agent 的下一个关键竞争力不是模型更强，而是**技能管理能力更强**。模型是大脑，技能是肌肉记忆——大脑再聪明，没有肌肉记忆也快不起来。

---

## 技能定义

技能是三元组 **S = (M, R, C)**：
- **M**：主指令文档（告诉 Agent 怎么做）
- **R**：辅助资源（模板、脚本、参考资料）
- **C**：触发条件（什么时候该用）

按资源类型分三种：
- **纯文本型**：可读性强，执行确定性弱
- **纯代码型**：执行可靠，维护成本高
- **混合型**：兼顾可读性和可执行性（Claude Code 的 CLAUDE.md 即此类）

---

## 技能获取（四条路径）

| 路径 | 特点 | 代表 |
|------|------|------|
| 人类专家手写 | 精度最高，扩展性差 | 种子层 |
| 从经验提炼 | 主流，从成功轨迹提取 | Voyager、Reflexion、ExpeL |
| 即时构建 | 新任务直接生成 | CREATOR、ToolMakers |
| 外部资料挖掘 | 冷启动首选 | 文档、代码库、Kaggle |

---

## 检索策略（四类）

核心问题：**检索召回率 ≠ 执行成功率**

- 语义向量检索：最常用，但语义近≠适用
- 关键词检索：精确匹配，做补充过滤
- 生成式检索：融入推理，覆盖率难保证
- 结构化检索：利用层级/依赖关系

---

## 技能进化（五个环节）

1. **修订**：修改技能本身，而非记录错误
2. **验证**：通过测试才进正式库
3. **策略耦合**：技能库成为可训练参数
4. **仓库级进化**：单个技能→整个仓库治理
5. **运行时治理**：警惕"投毒技能"风险

---

## 生态现状

- SkillsMP：70万+ 技能
- SkillNet：30万+ 技能
- ClawHub：4万+ 技能

技能正成为独立基础设施层，不再是 Agent 产品的附属功能。

---

## 论文信息

- 标题: A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications
- 链接: https://arxiv.org/abs/2605.07358v1
- GitHub: https://github.com/JayLZhou/Awesome-Agent-Skills

---

**标签：** #主题/AIAgent
**相关：** [Awesome-Agent-Skills](https://github.com/JayLZhou/Awesome-Agent-Skills)