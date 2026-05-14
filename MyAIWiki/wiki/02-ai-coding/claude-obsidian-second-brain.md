# Claude + Obsidian 第二大脑系统

## 核心结论

Claude + Obsidian 构建的"第二大脑"系统，通过 AI 自动维护机制解决了传统知识管理系统的核心痛点：**维护负担超过价值导致系统崩溃**。该系统让 LLM 承担所有繁琐的簿记工作（总结、交叉引用、归档、更新），人类只需策划来源和提出好问题。

## 分类提炼

**场景**：AI Coding 工作流 | 个人知识管理 | 工具组合
**标签**：#主题/AI Coding #主题/效率 #工具/Obsidian #工具/Claude-Code
**类型**：实操指南 + 架构模式

## 要点列表

### 核心价值
- 每天早上 Claude 已经知道你的一切：身份、项目、工具、任务、文章、想法
- **不是聊天机器人，是第二大脑**：永不睡觉、永不忘记、每天使用都更聪明
- 关键数据：718万+ 查看、45932 书签、9595 喜欢

### 架构模式：LLM Wiki A

**三层架构**：
1. **Raw Sources**：只读原始资料（文章/论文/图片），不可变，真相来源
2. **Wiki**：LLM 完全拥有的 markdown 文件集合（摘要/实体/概念/比较/综合）
3. **Schema**：规则文档（CLAUDE.md/AGENTS.md），告诉 LLM 如何维护

**与 RAG 的核心区别**：不是每次问题从头发现知识，而是 LLM 增量构建持久 wiki，交叉引用已在、矛盾已标记、综合已完成

### 操作机制

**Ingest（摄取）**：
- Web Clipper 剪辑文章 → 原始来源文件夹
- Claude 自动：读取 → 提取关键要点 → 写摘要页 → 更新索引 → 更新相关概念页 → 记录日志
- 单个来源可能触及 10-15 个 wiki 页面

**Query（查询）**：
- LLM 扫描索引 → 拉取相关页面 → 用引用综合回答
- **好的答案必须归档回 wiki**（比较/分析/新联系），这样探索也积累到知识库

**Lint（检查）**：
- 每周一次健康检查
- 寻找：页面矛盾、孤立页面、缺少页面的概念、过时声明
- 输出修复报告

### 两个特殊文件

| 文件 | 用途 | 特点 |
|------|------|------|
| **index.md** | 内容目录 | 每个页面链接+一行摘要+元数据，按类别组织，LLM 每次摄取更新 |
| **log.md** | 时间序记录 | append-only，`grep "^## \[" log.md \| tail -5` 可快速查阅 |

### 工具链

- **Obsidian Web Clipper**：网页 → markdown
- **本地图片下载**：设置附件路径 + 热键 Ctrl+Shift+D
- **Graph View**：查看 wiki 形状（连接/孤立/中心页面）
- **Marp**：markdown 幻灯片
- **Dataview**：frontmatter 查询，生成动态表格
- **qmd**：本地 markdown 搜索引擎（BM25/向量搜索 + LLM 重排序）
- **Git**：版本历史、分支、协作（wiki 只是 markdown 文件的 git 仓库）

### 核心提示词

**摄取来源**：
```
claude -p "I just added an article to /raw-sources. Read it, extract the key ideas, write a summary page to /wiki/summaries/, update index.md with a link and one-line description, and update any existing concept pages that this article connects to. Show me every file you touched." --allowedTools Bash,Write,Read
```

**每周检查**：
```
claude -p "Read every file in /wiki/. Find: contradictions between pages, orphan pages with no inbound links, concepts mentioned repeatedly but with no dedicated page, and claims that seem outdated based on newer files in /raw-sources/. Write a health report to /wiki/lint-report.md with specific fixes." --allowedTools Bash,Write,Read
```

**早晨简报**：
```
claude -p "Write a Python script called morning_digest.py that: 1) reads Memory.md and surfaces any open actions due today 2) reads any new files added to /raw-sources in the last 24 hours 3) prints a clean briefing to the terminal. Then schedule it as a cron job every morning at 7:30am." --allowedTools Bash,Write
```

### 为什么这有效

**Vannevar Bush 的 Memex（1945）**：个人策划知识存储，文档间连接与文档本身一样有价值。他无法解决的是谁做维护——现在 LLM 解决了。

**维护即自动化**：人类放弃 wikis 是因为维护负担增长快于价值。LLMs 不会无聊、不会忘记更新交叉引用、可以一次触及 15 个文件。维护成本接近于零。人类做：策划来源、提出好问题、思考意义。LLM 做：其他一切。

## 相关链接

- [Obsidian 官网](https://obsidian.md/)
- [Claude Code](https://claude.com/product/claude-code)
- [原文](https://x.com/defileo/status/2042241063612502162)