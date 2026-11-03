---
title: Karpathy用Claude做HackerTube——社区共识替代平台推荐算法
category: 01-ai-agents
tags: ["#Agent落地", "#ClaudeCode", "#内容发现", "#数据开放", "#个人软件"]
nodes: HackerTube,社区共识过滤，few-shotted开发，ClaudeCode全流程，数据可复用性，人类意图与AI执行分工，HackerNews信号源，无登录设计
links: "[[51CTO技术栈-Agent能力不足维护代码库-HumanLayer创始人质疑无人值守软件工厂]]", "[[Datawhale-DeepSeek-Super-Agent架构-Router-Worker双层]]"
date: 2026-11-03
source: 微信公众号 / [AgenticHub](https://mp.weixin.qq.com/s/8flITf7_3Ie5VeqkIXgxgA)
---

# Karpathy用Claude做HackerTube——社区共识替代平台推荐算法

- 原文链接：https://mp.weixin.qq.com/s/8flITf7_3Ie5VeqkIXgxgA
- 原始作者：AgenticHub（转述 Karpathy 项目）
- 来源：AgenticHub
- 发布时间：2026-11-03
- 获取时间：2026-11-03

## 核心结论（一句话）
> Karpathy 用 Claude Code 花 2 小时处理 HN 20 年 4300 万条评论，筛出 6454 个被社区反复推荐的视频做成 HackerTube；展示了人类提意图、AI 完成从 0 到 1 全部实现的新工作流。

## 知识节点（8 个独立概念）
- **HackerTube**：基于 HN 社区共识而非平台点击优化的 YouTube 视频推荐站；无需登录、缩略图取视频中间帧、数据完全开放为 zip。
- **社区共识过滤**：用高质量社区（HN、Reddit、Discord）的历史讨论作为内容过滤器，替代平台算法的点击率优化；本质是把人类注意力和时间筛选过的信号批量提取。
- **few-shotted 开发**：Karpathy 用语"few-shotted for breakfast"——过去几周的项目现在用几轮对话在吃早餐功夫搞定；前提是清晰意图 + 关键决策由人完成。
- **Claude Code 全流程**：写代码、部署、加固服务器、优化前端全交给 Claude；人工只做 API key 申请、VPS 租赁、域名购买三件事。
- **数据可复用性**：分析数据公开为 zip，任何人可按自己口味再过滤、做客户端、接入知识库；比封闭网站更有长期价值。
- **人类意图与 AI 执行分工**：人类负责提出清晰意图和做关键决策，AI 负责机械、重复、需要耐心的工作；不是"AI 辅助写代码"而是"AI 把项目从 0 到 1 做完"。
- **Hacker News 信号源**：20 年、4300 万条评论中反复出现的 YouTube 链接，代表经得起时间检验的技术内容；6454 个视频是最终筛选结果。
- **无登录设计**：状态存本地浏览器，打开即用；降低使用门槛的同时避免用户数据收集，与平台算法形成对比。

## 关联图谱

### 上游（基于 / 来自）
- [[51CTO技术栈-Agent能力不足维护代码库-HumanLayer创始人质疑无人值守软件工厂]]：本文是 Agent 能力的正面案例（小项目从 0 到 1），该文是反面边界（复杂长期项目维护）

### 下游（应用于 / 验证于）
- 个人推荐引擎、社区信号提取工具、数据开放复用实践

### 同级（横向 / 并列）
- [[Datawhale-DeepSeek-Super-Agent架构-Router-Worker双层]]：Agent 架构设计与本文的 Agent 工作流实践互补

## 正文要点（3 条）
1. **内容发现范式转变**：从平台点击优化转向社区历史讨论作为过滤器；HN、Reddit、Discord 是经人类注意力筛选的信号源，AI 能批量系统提取；HackerTube 是这一范式的具体实现。
2. **个人软件开发门槛急剧下降**：过去几天到几周的 web 服务（爬数据、清洗、部署、前端），现在一个周末可完成；Karpathy 只做了 3 件体力活，其余全交给 Claude Code + Opus 5.5。
3. **数据开放比封闭产品更有价值**：分析数据打包为 zip 公开，任何人可按兴趣再过滤、做桌面客户端或 Android TV 应用、接入知识库做私人推荐引擎；已有人据此做出衍生产品。

## 3 个对 Seetong 团队可借鉴动作
1. **用社区信号做内部内容筛选**：把 Seetong 相关的 TAPD 评论、企微群讨论、GitHub issue 作为信号源，用 Agent 批量提取高频出现的技术方案和问题模式，替代人工翻记录。
2. **小工具尝试 few-shotted 开发**：内部工具类需求（如日志分析面板、版本质量看板），先花 10 分钟写清意图和约束，直接让 Claude Code 从 0 到 1 完成，欧阳荣或对应负责人验收即可。
3. **内部工具数据开放**：分析报告和监控数据导出为结构化文件而非仅在线查看，让团队成员可以按自己需求再加工，降低二次开发的启动成本。

**备注与链接**

- HackerTube 站点：https://hackertube.org/
- Karpathy 原帖：https://x.com/karpathy/status/2116957135661945283
- 模型版本：Claude Code + Opus 5.5
- 本文为二手转述，Karpathy 原帖为英文推文
