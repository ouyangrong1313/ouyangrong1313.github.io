---
title: Andrej Karpathy：AI写代码，只需要问自己这一个问题
author: winkrun
date: 2026-07-15
slug: AndrejKarpathy-AI写代码-只需要问自己这一个问题
category: 02-ai-coding
tags: [#主题/AI-Coding, #主题/Skill, #主题/AI-Agent, #节点/思考发生点, #节点/判断执行分界, #节点/双资深一致, #节点/Workflow-Extractor, #节点/Skill-Score, #场景/公众号长文]
nodes: [思考发生点, 判断执行分界, 双资深一致, 工作流档位切换, Scout-Filter-Reader, Workflow-Extractor, Skill-Score, Reviewer-Publisher]
links: [[AI-Coding的顿悟时刻]], [[Code-is-cheap-AI-Native-五倍效率]], [[面向Skills编程-淘宝企业购端到端研发提效实践]], [[loonggg-Claude-Code-技能心法-11条建议]], [[Skill-Self-Evolution]], [[Loop-Engineering-验证才是瓶颈]]
digest: "[[AndrejKarpathy-AI写代码-只需要问自己这一个问题-digest]]"
source: 微信公众号 / winkrun
source_wechat: https://mp.weixin.qq.com/s/yEWfTLs9W3-QblvPbrGUPQ
---

# Andrej Karpathy：AI写代码，只需要问自己这一个问题

- 原文链接：https://mp.weixin.qq.com/s/yEWfTLs9W3-QblvPbrGUPQ
- 来源：微信公众号「winkrun」
- 获取时间：2026-07-15
- 速读摘要：[[AndrejKarpathy-AI写代码-只需要问自己这一个问题-digest]]

## 核心结论（一句话）

**AI Coding 最关键的不是“哪种工作流更先进”，而是先问“思考到底发生在哪一步”**。判断尚未完成的任务必须由人握住，判断已经完成且成功标准清晰的任务才适合交给 AI；rvaniaaa 的 GitHub 技能蒸馏系统，本质上就是把“人做判断，AI 做执行”工程化。

## 分类提炼

- 场景：AI Coding / Skill 自进化 / GitHub 工作流蒸馏
- 标签：#主题/AI-Coding #主题/Skill #主题/AI-Agent #节点/思考发生点 #节点/判断执行分界 #节点/双资深一致 #节点/Workflow-Extractor #节点/Skill-Score #场景/公众号长文
- 类型：判断框架 / 流水线拆解 / 工程启发
- 关联主线：[[AI-Coding的顿悟时刻]] 的“需求与架构最稀缺” + [[Skill-Self-Evolution]] 的“Skill 会持续沉淀”

## 知识节点（8 个）

- **思考发生点**：所有 AI Coding 决策都可以先压成一句问题：“思考到底发生在哪一步？”
- **判断执行分界**：需求取舍、架构设计、安全边界这类仍在判断期的任务，人不能外包；执行期任务才适合 AI 放大。
- **双资深一致**：如果两个资深工程师独立做会收敛到相近实现，这个任务通常就是 AI 的甜点区。
- **工作流档位切换**：自己写、用补全、把整段任务交给 Agent 不是三种宗教，而是同一问题的三个档位。
- **Scout-Filter-Reader**：找新 Skill 不该一上来读源码，而要先搜候选、再用确定性规则去噪，最后按 README→docs→examples→依赖→源码的顺序增量加载。
- **Workflow-Extractor**：真正值得沉淀的不是“这个仓库”，而是仓库里可复用的 workflow。
- **Skill-Score**：是否值得变成 Skill，优先用确定性检查项表达，而不是把所有判断都外包给 LLM。
- **Reviewer-Publisher**：生成与审核必须分离，自动化只负责提议，人类保留最终批准权。

## 关联图谱

### 上游（基于 / 来自）
- [[AI-Coding的顿悟时刻]]：同样强调“执行变便宜后，真正昂贵的是需求与架构判断”；本文把这件事压成更可操作的一句判断题。
- [[Code-is-cheap-AI-Native-五倍效率]]：同主线“代码越来越便宜，真正贵的是边界、验证和收口”；本文补上“何时放手给 AI”的简单判据。
- [[Skill-Self-Evolution]]：rvaniaaa 的项目是 Skill 自进化的工程化样本，和该页的三大学派综述形成“原理 ↔ pipeline”互补。

### 下游（应用于 / 验证于）
- [[面向Skills编程-淘宝企业购端到端研发提效实践]]：本文“先抽 workflow，再变 Skill”的思路，在企业研发交付里被落成可复用的生产线。
- [[loonggg-Claude-Code-技能心法-11条建议]]：本文生成 Skill 的流水线，需要后者补上“怎么把 Skill 写得真的可用”的方法论。
- [[Loop-Engineering-验证才是瓶颈]]：本文的 Reviewer / Skill Score / 不自动合并，正好落到“验证闸门才是产品”的验证主线上。

### 同级（横向 / 并列）
- [[undefinedKi-AI-Second-Brain-10-Step-Guide]]：都在讨论“知识如何持续积累”，但那篇偏个人记忆系统，本文偏 Agent 自动吸收新技能。
- [[买了一样的AI为什么别家的比你的强]]：同主线“模型是商品，判断与 Skill 才是资产”；本文更偏自动发现与编译 Skill 的流水线。
- [[PM-Skills-Marketplace-产品经理必备skill]]：这篇讲“把方法论打包进 Skill”，本文讲“如何自动找到并发布新 Skill”。

## 正文要点（5 条）

1. **Karpathy 给 AI Coding 的不是工具选择题，而是边界判断题。**
   - 判断没完成：需求、架构、安全、业务取舍，必须留在人手里。
   - 判断完成：CRUD、迁移、测试、样板、文档，这些成功标准清晰的执行任务才是 AI 杠杆位。
2. **“两个资深工程师会写出差不多实现”是一个很实用的验算器。**
   - 这条规则把“该不该放给 AI”从感觉题，压成了可操作的工程题。
   - 也解释了为什么 Karpathy 会在自己写 / 补全 / 全代理三种工作流之间切换。
3. **rvaniaaa 的系统把“人做判断，AI 做执行”拆成八段流水线。**
   - Scout 负责找仓库，Filter 负责去噪，Reader 负责先读意图再读实现。
   - Workflow Extractor 开始，系统处理的对象从“仓库”切换为“可复用 workflow”。
4. **后半段真正重要的不是“AI 会自己写 Skill”，而是“哪些环节故意不用 LLM”。**
   - Skill Score 用固定检查项判断是否通过。
   - Reviewer 把“写 Skill”与“批准 Skill”分开，避免自我背书。
   - Publisher 只自动提 PR，不自动合并，最终批准仍由人完成。
5. **这篇文章连接了两条常被分开讨论的主线：AI Coding 边界判断 + Skill 资产化。**
   - 前半段解决“什么该交给 AI”。
   - 后半段解决“交给 AI 之后，如何让它下次别再从零开始”。

- 备注：本文前半段是 Karpathy 的 AI Coding 判断框架，后半段是 rvaniaaa 的 GitHub 技能蒸馏项目拆解；整篇更像“方法论 + 项目样本”拼接，而不是单一原始论文。
- 已清理：公众号末尾“小程序/点赞/分享/进群”等交互噪声没有进入 wiki。
- raw: `../../raw/AndrejKarpathy-AI写代码-只需要问自己这一个问题.md` | raw-digest: `../../raw/AndrejKarpathy-AI写代码-只需要问自己这一个问题-digest.md` | wiki-digest: `./AndrejKarpathy-AI写代码-只需要问自己这一个问题-digest.md`
