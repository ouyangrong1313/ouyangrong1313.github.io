# AI Wiki Log

时间序变更记录。格式：`## [日期] 操作 | 标题`

---

## 2026-05-20

### compile | 知识卡片编译模板：长文如何压成 raw / digest / wiki 三层
- 来源：基于当前 MyAIWiki 编译实践整理
- wiki：wiki/02-ai-coding/知识卡片编译模板-长文如何压成raw-digest-wiki三层.md
- 标签：#主题/AI-Coding #主题/效率 #手法/工程实践
- 说明：把长文进入知识库时的三层卡片化结构和适用边界固定为标准模板

### compile | MyAIWiki写入规范与验证模板
- 来源：基于当前 Codex / OMX / MyAIWiki 使用约定整理
- wiki：wiki/02-ai-coding/MyAIWiki写入规范与验证模板.md
- 标签：#主题/AI-Coding #主题/效率 #手法/工程实践
- 说明：明确正式知识库默认路径、禁止写入位置和知识落盘后的最小验证动作

### compile | Codex配置优化清单：从Harness视角改造AGENTS、Skills、知识库与验证闭环
- 来源：基于《从Prompt、Context到Harness，工程的三次进化与终局之战》与当前 Codex / OMX / MyAIWiki 环境的归纳整理
- wiki：wiki/02-ai-coding/Codex配置优化清单-从Harness视角.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/工程实践
- 说明：把 Harness 文章中的三层框架映射为可直接执行的 Codex 配置改造清单

### ingest | 从Prompt、Context到Harness，工程的三次进化与终局之战
- 来源：https://mp.weixin.qq.com/s/b1VL28GX5d17sKPfkSbIsw
- 原文：raw/从Prompt-Context到Harness-工程的三次进化与终局之战.md
- 拆解：raw/从Prompt-Context到Harness-工程的三次进化与终局之战-digest.md
- wiki：wiki/02-ai-coding/从Prompt-Context到Harness-工程的三次进化与终局之战.md
- 标签：#主题/AI-Coding #主题/AI-Agent #手法/权威背书 #手法/对比冲突 #场景/公众号长文
- 说明：把 Prompt / Context / Harness 三层框架编译进 AI Coding 知识库，并补充工程化闭环视角

## 2026-05-21

### ingest | 来自 Codex 官方团队的分享：如何把 Codex 用到极致
- 来源：https://mp.weixin.qq.com/s/BzR8QdVkEg2nLtZP1wVXWQ
- 原文：raw/来自Codex官方团队的分享-如何把Codex用到极致.md
- 拆解：raw/来自Codex官方团队的分享-如何把Codex用到极致-digest.md
- wiki：wiki/02-ai-coding/来自Codex官方团队的分享-如何把Codex用到极致.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/权威背书 #场景/公众号长文
- 说明：提炼 Codex 官方团队关于 durable threads、工具外延、自动化、目标验证和共享记忆的整套工作流方法

### compile | Codex配置下一步改造：从规则层走向线程、工具、目标与共享记忆
- 来源：基于《来自 Codex 官方团队的分享：如何把 Codex 用到极致》与当前 Codex / OMX / MyAIWiki 配置现状的归纳
- wiki：wiki/02-ai-coding/Codex配置下一步改造-从规则层走向线程工具目标与共享记忆.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/工程实践
- 说明：把官方方法论映射成当前配置的下一阶段改造优先级，明确线程、工具面、目标模板和共享记忆四条主线

### compile | 任务类型到验证模板
- 来源：基于当前 Codex / MyAIWiki / 配置改造工作的通用收尾需求整理
- wiki：wiki/02-ai-coding/任务类型到验证模板.md
- 标签：#主题/AI-Coding #主题/效率 #手法/工程实践
- 说明：把知识库、文档、脚本、代码、配置和浏览器抓取任务的最小 verifier 模板固定下来

### compile | Codex长期线程设计草案
- 来源：基于《来自 Codex 官方团队的分享：如何把 Codex 用到极致》与当前高频任务模式整理
- wiki：wiki/02-ai-coding/Codex长期线程设计草案.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/工程实践
- 说明：定义长期线程的用途、输入、输出、stop condition 和 verifier，作为后续工作台设计基础

### compile | Codex工具入口与能力边界
- 来源：基于当前 Codex / Claude Code / Playwright / WebFetch / GUI 自动化实践总结
- wiki：wiki/02-ai-coding/Codex工具入口与能力边界.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/工程实践
- 说明：明确 shell、WebFetch、Playwright、MCP 和 GUI 自动化各自适用面与边界，减少入口选择错误

### compile | 多Agent使用边界与并行判定
- 来源：基于当前 Codex 子 agent 使用经验与长任务拆分实践整理
- wiki：wiki/02-ai-coding/多Agent使用边界与并行判定.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/工程实践
- 说明：定义多 agent 适用场景、禁用场景和并行前判定问题，避免把并行当默认解

### compile | Codex配置原则总览
- 来源：基于当前 Codex 配置规则页的统一收束与导航整理
- wiki：wiki/02-ai-coding/Codex配置原则总览.md
- 标签：#主题/AI-Coding #主题/AI-Agent #主题/效率 #手法/工程实践
- 说明：将配置改造、验证模板、长期线程、工具入口和多 agent 边界串成正式总入口，并回指顶层 AGENTS 保持精简

### script | 微信文章抓取脚本
- 文件：scripts/fetch_wechat_article.py
- 说明：复用本机缓存的 Playwright + Chrome 抓取微信文章渲染正文，输出标题、作者、时间与正文 JSON

### script | 微信文章 raw 初稿生成脚本
- 文件：scripts/build_wechat_raw.py
- 说明：在微信正文抓取脚本之上，直接生成符合 MyAIWiki raw 风格的 Markdown 初稿

### script | 微信文章 raw 落盘脚本
- 文件：scripts/write_wechat_raw.py
- 说明：基于微信正文抓取与 raw 初稿生成脚本，直接将文章写入 MyAIWiki/raw/{slug}.md

### script | 微信文章一键编译脚本
- 文件：scripts/compile_wechat_to_wiki.py
- 说明：从微信链接直接生成 MyAIWiki 的 raw、digest、wiki 草稿，并幂等更新 index 与 log

### prompts | 微信文章编译精修提示词
- 文件：prompts/wechat-compile-polish.md
- 说明：将自动编译出的 raw、digest、wiki 草稿交给 Codex 或 Claude 精修为正式知识条目

### script | 微信文章精修提示词打包脚本
- 文件：scripts/build_wechat_polish_prompt.py
- 说明：读取指定 slug 的 raw、digest、wiki 草稿，组装成可直接粘贴给模型的精修输入

### script | 微信文章精修结果回写脚本
- 文件：scripts/apply_wechat_polish_output.py
- 说明：将模型返回的两个 Markdown 代码块解析并回写到对应的 digest 与 wiki 文件

### script | 微信文章总入口脚本
- 文件：scripts/ingest_wechat_article.py
- 说明：串联编译、精修提示词生成和可选回写，作为微信文章进入 MyAIWiki 的统一入口
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
