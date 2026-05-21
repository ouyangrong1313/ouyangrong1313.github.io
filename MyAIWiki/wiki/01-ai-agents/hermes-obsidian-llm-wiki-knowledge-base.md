# Hermes+Obsidian+LLM Wiki 本地知识库

- 来源：Twitter/X @rwayne
- 原文：https://x.com/rwayne/status/2054523563248611675
- 编译日期：2026-05-14
- 标签：#主题/AIAgent #场景/落地案例

## 解决的问题

1. **信息碎片化** - 推特好文一顿复制，想找出来学习得手动翻半天
2. **笔记孤岛化** - Notion 几百篇笔记之间孤立，不知道某概念在其他地方出现过
3. **AI 无积累** - 每次从零搜索，Token 浪费一半，没有记忆
4. **数据不安全** - 笔记存在别人服务器上

## 核心链路

```
文档导入 → AI 整理 → Wiki 生成 → 双向链接
```

**四个优点**：完全自动化、本地存储、持久化积累、只需提问

## 三个工具分工

| 工具 | 角色 | 核心功能 |
|------|------|----------|
| **Hermes Agent** | 自动化执行引擎 | 内置 `llm-wiki` skill，自动提取实体/概念，创建 Markdown，添加双链 |
| **LLM Wiki** | 知识库标准 | 文件结构：raw/sources、wiki/entities、wiki/concepts、index、log |
| **Obsidian** | 笔记展示层 | 双向链接 + Graph View 可视化 |

## 使用规则

| 指令 | 行为 |
|------|------|
| 「写入知识库」 | Hermes 自动整理并写入 |
| 「结合知识库」 | Hermes 先检索再回答 |
| 日常对话 | 不访问知识库（避免污染） |

## LLM Wiki 文件结构

```
knowledge_base/
├── raw/sources/              # 原始素材
├── wiki/entities/            # 实体（人物、工具、项目）
├── wiki/concepts/            # 概念（方法论、原理）
├── wiki/index.md             # 知识库索引
└── wiki/log.md               # 更新日志
```

## 核心价值

> 让 AI 替你做繁琐的知识管理工作，你只需要专注于提问和探索。

## 相关资料

- [[deep-analysis-llm-wiki-obsidian-wiki-gbrain]] - 阿里云开发者《深度解析 LLM Wiki / Obsidian-Wiki / GBrain》，更深入的技术原理分析