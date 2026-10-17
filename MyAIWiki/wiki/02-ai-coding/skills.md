# Skills 命令手册

Obsidian 负责"记"，Claude Code 负责"想"和"做"。项目内已注册的 Codex Skills 是 `$compile-link` 和 `$wiki-health`；下文的 `/summary`、`/weekly`、`/idea` 仍是手工工作流说明，不应误认为已安装的 Skill。

---

## /compile — 编译文章到知识库

**实际入口**：`.codex/skills/compile-link/SKILL.md`

**触发条件**：用户提供微信公众号/X/网页链接，要求整理知识库

**标准流程**：
1. 用 Playwright 浏览器获取原文内容
2. 保存原文到 `raw/{主题-lowercase-with-hyphen}.md`
3. 生成拆解文档到 `raw/{主题-lowercase-with-hyphen}-digest.md`（包含7角度+21钩子）
4. 编译成 wiki 页面到 `wiki/{分类}/{主题-lowercase-with-hyphen}.md`
5. 更新对应 index.md 和 master-index.md

**输出格式**：
```
| 文件 | 说明 |
|------|------|
| raw/xxx.md | 原文 |
| raw/xxx-digest.md | 拆解文档 |
| wiki/xxx.md | 正式 wiki |
```

**分类参考**：
- AI Agent 相关 → `wiki/01-ai-agents/`
- AI Coding 相关 → `wiki/02-ai-coding/`
- 效率工具 → `wiki/03-productivity/`
- APP 研发 → `wiki/04-app-dev/`
- 内容创作 → `wiki/05-content-creation/`
- AI 技术趋势 → `wiki/06-ai-tech/`
- RAG 系统 → `wiki/07-rag-systems/`

---

## /lint — 知识库体检

**实际入口**：`.codex/skills/wiki-health/SKILL.md`

**触发条件**：用户要求检查知识库健康状态

**检查项**：

### A 类：链接完整性
- [ ] 所有 wiki 页面是否能正常跳转
- [ ] 是否有孤岛页面（写了但从未被引用）
- [ ] index.md 是否包含所有页面

### B 类：内容质量
- [ ] 是否有空页面或只有标题的页面
- [ ] 是否有过时内容（日期超过6个月）
- [ ] 标签是否规范使用

### C 类：结构一致性
- [ ] 新页面是否更新了对应 index.md
- [ ] master-index.md "最近更新" 是否最新
- [ ] raw/ 和 wiki/ 是否同步

**输出格式**：
```
python3 scripts/wiki-health-check.py

# 仅修正 frontmatter tags 和正文标签空白边界后复查
python3 scripts/wiki-health-check.py --fix

# 修复唯一可判定的链接别名，并补齐分类索引入口
python3 scripts/wiki-health-check.py --fix-link-aliases --fix-indexes
python3 scripts/wiki-health-check.py
```

---

## /summary — 对话存档

**触发条件**：用户要求把本次对话精华存档

**标准流程**：
1. 提炼对话中的核心观点和结论
2. 提炼2-3个可复用的工作流或提示词模板
3. 保存到 `raw/conversation-{日期}.md`
4. 如有后续行动项，更新到知识库相关页面

---

## /weekly — 每周复盘

**触发条件**：用户要求做知识库周复盘

**复盘维度**：
1. **本周新增**
   - 新增了多少页面
   - 新增了哪些主题

2. **认知变化**
   - 本周哪些观点和之前认知冲突
   - 哪些认知被强化

3. **盲区识别**
   - 哪些领域没有覆盖到
   - 哪些主题需要深挖

4. **下步行动**
   - 需要补充哪些资料
   - 需要整理哪些现有内容

---

## /idea — 灵感记录

**触发条件**：用户分享一个想法或灵感

**标准流程**：
1. 记录灵感的核心观点
2. 标注可能的应用场景
3. 关联到已有的知识节点
4. 存入 `raw/notes/{日期}-{一句话描述}.md`

---

## 标签体系

### 按主题
 #主题/AI-Agent
 #主题/APP研发
 #主题/AI-Coding
 #主题/内容创作
 #主题/效率
 #主题/AI科技
 #主题/RAG系统

### 按手法
 #手法/焦虑共鸣
 #手法/对比冲突
 #手法/好奇心循环
 #手法/权威背书
 #手法/开头钩子
 #手法/文章结构

### 按场景
 #场景/知识付费
 #场景/技术博客
 #场景/公众号长文
 #场景/产品介绍
 #场景/落地案例

---

## 相关链接

- [[index]]
- [[02-ai-coding/prompt-engineering]]
- [[01-ai-agents/harness-engineering]]
