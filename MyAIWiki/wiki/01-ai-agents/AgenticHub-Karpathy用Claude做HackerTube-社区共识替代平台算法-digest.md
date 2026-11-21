# Karpathy 用 Claude 做 HackerTube — 速读摘要

## 一句话总结
Karpathy 用 Claude Code 花 2 小时处理 HN 20 年 4300 万条评论，筛出 6454 个视频做成 HackerTube；人类提意图、AI 完成从 0 到 1 全部实现。

## 速查表

| 核心观点 | 关键数字 / 案例 |
|---|---|
| 内容发现从平台算法转向社区共识 | HN 20 年、4300 万评论、6454 视频 |
| 个人软件开发门槛急剧下降 | 2 小时完成，人工只做 3 件事 |
| 数据开放比封闭产品更有价值 | zip 公开，已有人做衍生客户端 |

## 反直觉点
- 不是"AI 辅助写代码"，而是"AI 把项目从 0 到 1 做完"——人只做 API key、VPS、域名三件体力活。
- 最好的内容推荐不是更聪明的算法，而是更老的社区共识。

## 对 Seetong 可借鉴动作
1. 用 TAPD/企微/GitHub 讨论作为信号源，Agent 批量提取高频技术方案。
2. 内部小工具尝试 few-shotted 开发：10 分钟写清意图，让 Claude Code 完成。
3. 分析数据导出为结构化文件，降低二次加工启动成本。

## 关联 + 备注
- 对照：[[51CTO技术栈-Agent能力不足维护代码库-HumanLayer创始人质疑无人值守软件工厂]]（小项目 vs 复杂长期项目）
- HackerTube：https://hackertube.org/
- Karpathy 原帖：https://x.com/karpathy/status/2116957135661945283
