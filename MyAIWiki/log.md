# AI Wiki Log

时间序变更记录。格式：`## [日期] 操作 | 标题`

---

## 2026-05-13

### ingest | Good AI PM / Bad AI PM：AI 时代，PM 藏不住了
- 来源：https://mp.weixin.qq.com/s/7TMDbPzqWAI7JuWHBQKJew
- 原文：raw/good-ai-pm-bad-ai-pm.md
- 拆解：raw/good-ai-pm-bad-ai-pm-digest.md
- wiki：wiki/01-ai-agents/good-ai-pm-bad-ai-pm.md
- 标签：#主题/AI-Agent #主题/AI科技 #主题/APP研发
- 说明：提炼 AI 时代 PM 的核心分水岭：协调劳动被压缩后，真正稀缺的是客户洞察、现场感与判断力

## 2026-05-12

### ingest | Claude + Obsidian 第二大脑系统
- 来源：https://x.com/defileo/status/2042241063612502162
- 原文：raw/claude-obsidian-second-brain.md
- 拆解：raw/claude-obsidian-second-brain-digest.md
- wiki：wiki/02-ai-coding/claude-obsidian-second-brain.md
- 标签：#主题/AI-Coding #主题/AIAgent #主题/效率
- 说明：Defileo 的爆款推文，718万+ 查看，介绍 LLM Wiki A 架构模式

### schema | 创建 AI Wiki Schema
- 文件：.ai-wiki-schema.md
- 说明：参考 Defileo 的方案，增加 Schema 层定义 AI 维护规则

### script | 晨间简报脚本
- 文件：scripts/morning-digest.py
- 说明：Python 脚本，汇总最近变更和新增文件

### prompts | Bug Fix 提示词
- 文件：prompts/bug-fix.md
- 说明：优化了空的 bug-fix.md 模板

### organize | 整理 raw/articles/ 未编译文章
- 吴恩达AI提示词课 → wiki/02-ai-coding/吴恩达AI提示词课.md
- Agent时代架构师系统能力 → wiki/01-ai-agents/Agent时代架构师系统能力.md
- 说明：检查发现 3 篇文章已在 wiki 但缺正式版本，补充编译

<!-- 模板（不被解析）:
# [日期] 操作 | 标题
- 来源：URL
- 原文：raw/{slug}.md
- 拆解：raw/{slug}-digest.md
- wiki：wiki/{分类}/{slug}.md
- 标签：#主题/xxx #手法/xxx
- 说明：简短描述
-->
- 2026-05-13：编译公众号文章《深度解析LLM Wiki / Obsidian-Wiki / GBrain：Agent时代知识的“自组织”与“自进化”》，新增 raw、digest 与 wiki 条目。
