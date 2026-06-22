---
name: compile-link
description: 一句"compile URL"完成 raw + digest + wiki + index + log 5 步全流程。微信公众号 / X 推文 / 任意 URL 都可用。
type: skill
trigger: 用户发来一个 URL + 任何"编译知识库"语境
---

# /compile-link — 链接编译知识库统一入口

> 设计来源：Karpathy LLM Wiki Step 8 "Build a skill so you never repeat yourself"——任何重复 2 次的任务做 Skill。

## 触发条件

- 用户发来一个 URL（微信公众号 / X 推文 / 任意文章）
- 伴随"编译知识库"、"存档"、"入知识库"、"加 wiki"、"做 digest"等关键词
- 或单独一句 `/compile https://...`

**反例（不该触发）**：
- 用户发 URL 但说"看看这篇写什么"——这是**阅读**，不是编译
- 用户发 URL 但说"对比一下 X 和 Y"——这是**研究**，不是编译
- 用户发自己的草稿——这是**修改**，不是编译

## 输入规范

| 字段 | 必填 | 默认 | 说明 |
|------|------|------|------|
| URL | ✅ | — | 要编译的文章链接 |
| 分类 | ⚠️ | 02-ai-coding | wiki 分类（01-ai-agents / 02-ai-coding / 03-productivity / 04-app-dev / 05-content-creation / 06-ai-tech / 07-rag-systems） |
| 是否短链 | ⚠️ | 否 | X 推文等短内容标 true，节省 digest 篇幅 |
| force | ⚠️ | 否 | 已存在文件时是否覆盖 |

## 5 步流程

```
fetch → raw → digest → wiki → index+log
```

### Step 1：fetch（抓取原文）

- 微信公众号 / 知乎 / 一般博客 → Playwright CDP 抓（curl 会被反爬）
- X 推文 → Playwright CDP 抓（X 是 SPA + 反爬严格）
- 已经保存过的 raw 文件 → 跳过

**输出**：`raw/{slug}.md`（完整原文 + 元信息 + 标签行）

### Step 2：raw（原文存档）

- 文件命名：`raw/{YYYY-MM-DD}-{slug}.md`（`{slug}` = URL 主题 lowercase-with-hyphen）
- 包含：原文链接、作者、发布日期、平台、关键数据、完整正文
- 底部添加：`标签：#主题/xxx #手法/xxx #场景/xxx #节点/xxx`

### Step 3：digest（拆解版）

- 文件命名：`raw/{YYYY-MM-DD}-{slug}-digest.md`
- 包含：1 句话总结 + 5 条核心观点 + 关键参数表 + 5 句核心金句 + 5 个对 Seetong/MyAIWiki 借鉴动作 + 关联图谱
- **透明玻璃自检**：≤4K 字节、6-10 节点、≤5 个 H2

### Step 4：wiki（知识库页面）

- 文件命名：`wiki/{分类}/{slug}.md`
- **遵循 `prompts/wiki-template.md` 新结构**（YAML frontmatter + 知识节点 + 关联图谱 + 正文要点 + 备注）
- 同时建 `wiki/{分类}/{slug}-digest.md`（速读版，≤4K 字节）
- **透明玻璃自检**：≤8K 字节、6-10 节点、≤5 个 H2

### Step 5：index + log（索引同步）

- `wiki/{分类}/index.md` 追加新页面链接（在合适分类区，**不**简单 append 到末尾）
- `wiki/master-index.md` 追加到「最近更新」区顶部 + 对应分类区
- `log.md` 追加 ingest 记录（按现有格式：操作类型/标题/作者/链接/数据/位置/命题/节点/金句/Seetong 借鉴/关联/待补证/透明玻璃自检/标签）

## 验证清单（每跑一次 /compile 必过）

### 输入
- [ ] URL 可访问（不是 404 / 私域）
- [ ] 分类目录存在

### raw
- [ ] 原文完整（不是片段、不是摘要）
- [ ] 包含链接、作者、日期、平台元信息
- [ ] 底部有标签行

### digest
- [ ] 1 句话总结讲清"为什么值得长期保留"
- [ ] 5 核心观点 / 5 金句 / 5 借鉴动作 / 关联图谱完整
- [ ] ≤4K 字节

### wiki
- [ ] YAML frontmatter 完整（title / category / tags / nodes / date / source）
- [ ] `nodes` 5-10 条，每条独立可 grep
- [ ] `links` ≥ 3 个（上游/同级/下游各 1+）
- [ ] 关联图谱有上游/下游/同级三段
- [ ] ≤8K 字节

### index / log
- [ ] 分类 index.md 已追加
- [ ] master-index.md 已追加（最近更新 + 分类区）
- [ ] log.md 已追加（按格式）

## 反合理化（不偷懒借口表）

| 偷懒借口 | 反驳 |
|---------|------|
| "原文很短，不需要 digest/wiki" | 短文也要走完整流程——重点是分类+节点+关联，不是字数 |
| "原文是英文，跳过中文 digest" | 英文也编译中文 digest——这是中英对照知识库的价值 |
| "已有相关页面，跳过编译" | 已有页面要更新（增量添加）不是跳过；新页面要建（去重差异化） |
| "抓取失败，就用用户给的文字版" | 文字版也要打 raw 标签 + 来源说明，不直接当原文 |
| "AI 跑全套质量不稳，留人工" | 这违背"AI 跑全套"约定；如确实质量差，先跑完再二次精修 |
| "分类不确定，先放 02-ai-coding" | 不确定就 AskUserQuestion；不要默认 |
| "8K 字节超了，先这样" | 重新压缩到 8K 内——内容密度比字数重要 |
| "5 个借鉴动作想不出来，跳过" | 想不出 5 个就做 3 个真实的；不要凑 5 个假的 |

## 与现有组件的关系

| 组件 | 角色 | /compile 怎么用 |
|------|------|-----------------|
| `scripts/compile_wechat_to_wiki.py` | 自动出 raw/digest/wiki 草稿 | Step 1-4 内部调用 |
| `scripts/build_wechat_raw.py` | 单步抓取微信文章 | Step 1 内部调用 |
| `scripts/apply_wechat_polish_output.py` | 把精修结果回写文件 | Step 3-4 精修环节 |
| `prompts/wiki-template.md` | 新文章结构模板 | Step 4 严格遵循 |
| `prompts/wechat-compile-polish.md` | 精修提示词 | Step 3-4 精修环节 |
| `scripts/wiki-query.py` | 查询/验证工具 | Step 5 验证 frontmatter/links |
| `prompts/bug-fix.md` | 另一个独立 Skill | 与本 Skill **无关**，不串 |

## 快速测试

```bash
# 跑一次完整的 /compile
/compile https://mp.weixin.qq.com/s/xxx 01-ai-agents

# 跑完后用户应该看到：
# - 5 个新文件（raw + raw-digest + wiki + wiki-digest）
# - 3 个索引文件被更新（分类 index + master-index + log）
# - 一份"完成报告"（列出所有文件路径 + 透明玻璃自检结果）
```

---

**最后更新**：2026-06-22 ｜ **设计来源**：`raw/2026-06-22-undefinedKi-AI-Second-Brain-10-Step-Guide-digest.md` Step 8 + [[Addy-Osmani-agent-skills-设计哲学-23-技能-7-块骨架]] 反合理化节
