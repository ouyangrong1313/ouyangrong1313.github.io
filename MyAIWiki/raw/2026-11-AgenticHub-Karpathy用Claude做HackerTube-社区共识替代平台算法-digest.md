# Karpathy 用 Claude 做 HackerTube — 原文摘要

## 一句话总结
Karpathy 用 Claude Code + Opus 5.5 花 2 小时处理 HN 20 年 4300 万条评论，筛出 6454 个被社区反复推荐的 YouTube 视频，做成无需登录、数据开放的 HackerTube；展示了一种新工作流——人类提意图和决策，AI 完成从 0 到 1 的全部实现。

## 核心观点（3 条）
1. **内容发现范式转变**：从平台点击优化转向"高质量社区历史讨论"作为过滤器；HN、Reddit、Discord 是经人类注意力筛选的信号源，AI 能批量提取。
2. **个人软件开发门槛急剧下降**：过去几天到几周的 web 服务，现在一个周末可完成；Karpathy 只做了申请 API key、租 VPS、买域名三件事，其余全交给 Claude。
3. **数据可复用性被重新打开**：分析数据公开为 zip，任何人可按自己口味再过滤、做客户端、接入知识库；比封闭网站更有价值。

## 关键数字
| 指标 | 值 |
|---|---|
| HN 评论处理量 | 4300 万条 |
| 时间跨度 | 20 年 |
| 筛选出视频数 | 6454 |
| 开发耗时 | 约 2 小时 |
| 人工操作 | 3 件（API key、VPS、域名） |

## 核心金句（3 条）
- "Many awesome projects that would have normally taken weeks/months even can now be few-shotted for breakfast."
- "I was annoyed with YouTube's recommendations…"
- 人类负责提出清晰意图和做关键决策，AI 负责把中间大量机械、重复、需要耐心的工作做完。

## 关联图谱
- **上游**：[[51CTO技术栈-Agent能力不足维护代码库-HumanLayer创始人质疑无人值守软件工厂]]（Agent 能力边界对照）、Claude Code 工作流
- **下游**：个人推荐引擎、社区信号提取工具、数据开放复用
- **同级**：[[Datawhale-DeepSeek-Super-Agent架构-Router-Worker双层]]（Agent 架构）、[[透明玻璃-写作的最高境界]]（内容质量标准）

## 备注
- HackerTube 站点：https://hackertube.org/
- Karpathy 原帖：https://x.com/karpathy/status/2116957135661945283
- 模型版本：Claude Code + Opus 5.5
