# MyAIWiki 知识库

## 我是谁（用户画像 · 2026-06-22 更新）

> 来源：用户核心规则 + 本次"让 Claude 重新面试你"工作流输出（参考 Karpathy LLM Wiki Step 5 "An empty brain is useless"）。

### 一句话

**监控行业 7+ 年，做 Seetong iOS/Android/SDK 全栈，AI 时代要"不掉队"+"把 AI 能力集成进 Seetong"**。

### 三个核心目标

1. **AI Coding 提效** — 用 Claude Code / Codex 加速 Seetong 三端 + 2 个 C/C++ SDK 的研发
2. **AI Agent 落地 Seetong** — 把 AI 能力做进监控 APP（智能告警 / 录像分析 / 设备诊断等场景）
3. **内容创作积累** — 拆解好文章的写作钩子，为"AI 时代的产品/技术公众号"积累弹药

### 三个工作禁区

- ❌ **不盲从** — "反对本本主义"：不唯书不唯上，只看项目实际需要（不因框架流行就用，不因别人说好就跟）
- ❌ **不堆抽象** — "反对形式主义"：用了一次不抽象、用两次可考虑、用三次才必须；删掉这段代码系统照常运行的就是形式主义
- ❌ **不盲目乐观** — "实事求是"：每个决策都要能回答"为什么"，每段代码要能解释"不这样会怎样"

### 三个语言规范

- 简体中文为主，技术术语可中英对照
- 代码标识符（变量/函数/类名）保留英文
- 注释、说明、对话一律用中文

### 三个复盘习惯

1. **每次任务以 To-do List 开始** — 明确步骤，确认逻辑闭环
2. **任务结束 git log 检查** — 看是否漏了 commit、是否动了不该动的文件
3. **每月底 lint 一次** — 检查孤立页面/过时内容/缺失交叉引用（已脚本化 `wiki-query.py`）

### 三个 Seetong 实战原则

- **Bigger context, not just smarter model** — 大上下文比小模型重要（CLAUDE.md 比换模型更能提效）
- **Keys, not prompts** — 权限控制走只读 scoped key / 硬规则脚本，不靠"请别删文件"的提示词
- **Plan → Review → Ship** — 写前先理清楚，改后让 reviewer 挑刺，最后再 ship（不写完就 push）

---

## 定位

你的 **AI 学习营 + 研发弹药库**。

两大核心用途：
1. **内容创作**：收集好文章，拆解写作套路，积累开头钩子
2. **AI Agent 落地**：收集 Agent 落地方案，辅助 APP 研发

---

## 目录结构

```
MyAIWiki/
├── .ai-wiki-schema.md      # AI 维护规则（核心！）
├── log.md                   # 时间序变更记录
├── raw/                     # 原始素材区（不可修改）
│   ├── inbox/              # 待处理入口（新素材先放这里）
│   ├── articles/           # 已处理的原文存档
│   ├── notes/              # 随手记的笔记
│   └── screenshots/        # 截图/图片素材（预留）
│
├── wiki/                    # 编译后的知识库（AI 写）
│   ├── master-index.md      # 主索引
│   ├── lint-report-*.md    # 健康检查报告
│   │
│   ├── 01-ai-agents/        # AI Agent 落地方案 ⭐
│   │   ├── index.md
│   │   ├── *.md
│   │   └── cases/           # 落地案例
│   │       └── index.md
│   │
│   ├── 02-ai-coding/        # AI Coding ⭐
│   │   └── index.md
│   │
│   ├── 03-productivity/     # 效率工具
│   │   └── index.md
│   │
│   ├── 04-app-dev/         # APP 研发流程 ⭐
│   │   └── index.md
│   │
│   ├── 05-content-creation/ # 内容创作
│   │   ├── index.md
│   │   ├── hooks/           # 开头钩子库
│   │   │   └── index.md
│   │   └── structures/      # 文章结构库
│   │       └── index.md
│   │
│   ├── 06-ai-tech/          # AI 技术趋势
│   │   └── index.md
│   │
│   └── 07-rag-systems/      # RAG 系统
│       └── index.md
│
├── prompts/                 # 提示词模板
│   └── bug-fix.md
│
└── CLAUDE.md                # 本文件
```

---

## 核心原则

1. **AI 写 wiki，人类读 wiki** - AI 负责所有维护工作（Ingest/Query/Lint），人类只做高价值决策
2. **Schema 驱动** - `.ai-wiki-schema.md` 定义了 AI 维护规则，是知识库的核心
3. **累积式增长** - wiki 是持久复合的产物，不是每次重新发现知识
4. **索引即检索** - 聪明的文件结构替代复杂的检索算法
5. **透明可追踪** - 所有变更记录到 `log.md`

---

## 工作流：Inbox 入口

新素材处理流程：
```
收到文章链接 → 保存到 raw/inbox/ → 编译成 wiki 页面 → 删除 inbox 中的原文
```

**为什么需要 Inbox？**
- 减少信息焦虑：不确定要不要存档？先丢 inbox，定期处理
- 避免 raw/ 变成垃圾堆：新素材直接进 inbox，有价值才转正

---

## 文件命名规范

1. **统一用 `-` 连字符**（不用 `_` 或其他）
2. **英文全部小写**
3. **中文保持原样**
4. **digest 后缀**：原文的拆解版本统一用 `-digest.md` 后缀
5. **版本控制**：如需版本，用 `_v1`、`_v2`（下划线）

**示例**：
- `谷歌开源agent-skills.md` — 原文
- `谷歌开源agent-skills-digest.md` — 拆解
- `AI时代给人类留了最后一份工作-是农民.md` — 中文原文
- `2026年了-你的文件管理还停留在新建文件夹吗-digest.md` — 中文拆解

---

## 角色分工

| 角色 | 职责 |
|------|------|
| **Obsidian（知识库）** | 负责"记" — 存储、结构、检索 |
| **Claude Code（你）** | 负责"想"和"做" — 分析、编译、体检、优化 |

**你的职责**：高价值的筛选与决策
- 判断什么值得存档
- 拍板最终结论
- 审核 AI 生成的内容

**AI 的职责**：繁琐节点的编织
- 获取和整理原文
- 提炼核心观点
- 生成拆解和角度
- 更新索引和链接
- 执行 Lint 检查

---

## Skills 命令

| 命令         | 触发条件   | 输出             |
| ---------- | ------ | -------------- |
| `/compile` | 收到文章链接 | 原文 + 拆解 + wiki |
| `/lint`    | 要求体检   | 健康报告           |
| `/summary` | 要求存档对话 | 对话精华文档         |
| `/weekly`  | 要求周复盘  | 复盘报告           |
| `/idea`    | 分享灵感   | 灵感记录文档         |

详见 [[02-ai-coding/skills|Skills 命令手册]]

---

## 三大用途

### 用途1：内容创作（写作弹药库）

当你发现好文章，想拆解其写作手法：

```
帮我拆解 raw/ 里的这篇文章，提取：
1. 文章结构（骨架）
2. 写作手法（招式）
3. 心理触发器
4. 7 个新角度 + 21 个开头钩子
```

拆解结果会自动归档到 `wiki/05-content-creation/`，打上
- `#主题/xxx` - 文章所属主题
- `#手法/xxx` - 使用的写作手法
- `#场景/xxx` - 适用场景

### 用途2：AI Agent 落地方案（研发弹药库）

当你研究 AI Agent 怎么落地到 APP：

```
帮我收集 raw/ 里关于 [具体场景] 的 Agent 落地方案
帮我对比一下 [方案A] 和 [方案B] 的优劣
帮我找一些 [你的APP类型] 相关的 AI 集成案例
```

### 用途3：AI Coding 提效

当你用 AI 辅助研发：

```
帮我整理 Claude Code 在 [iOS/Android/后端] 研发中的常用工作流
帮我写一个 [具体功能] 的提示词模板
帮我复盘这次重构学到的 AI Coding 技巧
```

---

## 标签体系

### 按主题
- `#主题/AI-Agent` - AI Agent 相关
- `#主题/APP研发` - APP 开发相关
- `#主题/AI-Coding` - AI 编程相关
- `#主题/内容创作` - 写作相关
- `#主题/效率` - 效率工具相关

### 按手法
- `#手法/焦虑共鸣` - 引发焦虑共鸣
- `#手法/对比冲突` - 对比冲突
- `#手法/好奇心循环` - 好奇心驱动
- `#手法/权威背书` - 权威引用

### 按场景
- `#场景/知识付费` - 课程招生文
- `#场景/技术博客` - 技术分享
- `#场景/公众号长文` - 公众号文章
- `#场景/产品介绍` - 产品文案

### 按节点主题（**2026-06 新增**）
- `#节点/LLM-Wiki` `#节点/Codex` `#节点/Harness` 
- `#节点/Context-Engineering` `#节点/Memory` `#节点/Skill` `#节点/Agent-Loop`

> 节点主题专门用于跨文章的概念检索，与 #主题/AI-Coding 互补。

---

## Wiki 链接格式

- 同一文件夹内：`[[页面名]]`
- 跨文件夹：`[[文件夹/页面名]]`
- 外部链接：`[显示文本](URL)`

---

## 目录导航

| 主题 | 路径 |
|------|------|
| 主索引 | wiki/master-index.md |
| AI Agent 落地方案 | wiki/01-ai-agents/index.md |
| APP 研发流程 | wiki/04-app-dev/index.md |
| AI Coding | wiki/02-ai-coding/index.md |
| 内容创作 | wiki/05-content-creation/index.md |
| 效率工具 | wiki/03-productivity/index.md |
| AI 技术趋势 | wiki/06-ai-tech/index.md |
| RAG 系统 | wiki/07-rag-systems/index.md |

---

## 使用示例

### 示例1：收集 Agent 落地方案
```
把我发给你的 [URL] 保存到 raw/inbox/
提取这篇文章里的 Agent 落地方案，分析：
- 这个方案解决了什么问题
- 用了什么技术架构
- 可以怎么借鉴到我的 [APP类型] 里
```

### 示例2：积累写作钩子
```
帮我拆解这篇文章，生成 7 个角度的开头钩子
这些钩子要能直接用在我的 [知识付费/产品介绍] 文章里
```

### 示例3：研发复盘
```
复盘一下我们这次 [功能开发/重构] 的 AI Coding 过程
总结：
- 哪些提示词特别有效
- 踩了哪些坑
- 下次可以怎么改进
保存到 wiki/02-ai-coding/cases/ 下
```

### 示例4：晨间简报
```bash
# 手动运行晨间简报
python3 ~/ouyangrong1313/MyAIWiki/scripts/morning-digest.py
```

### 示例5：Lint 健康检查
```
检查一下知识库的健康状况：
1. 孤立页面（没有被引用）
2. 过时内容（被新来源更新）
3. 缺失交叉引用
生成报告到 wiki/lint-report-YYYY-MM.md
```

---

## 自动化

### 晨间简报（可选）
每天 7:30 自动运行：
```bash
# 设置 cron job
(crontab -l 2>/dev/null; echo "30 7 * * * python3 ~/ouyangrong1313/MyAIWiki/scripts/morning-digest.py") | crontab -
```

### 每月 Lint
每月最后一天健康检查：
```bash
# 设置每月最后一天运行 lint
(crontab -l 2>/dev/null; echo "0 20 28-31 * * python3 ~/ouyangrong1313/MyAIWiki/scripts/morning-digest.py --lint") | crontab -
```

---

## 🚀 轻量查询工具（2026-06 升级）

参考 LLM-Wiki Skill 方法论，新增两个基于 ripgrep 的零 LLM 依赖查询工具：

### `wiki-query.py` — 8 种查询模式
```bash
# 按知识节点
python3 scripts/wiki-query.py node "LLM-Wiki"

# 按标签
python3 scripts/wiki-query.py tag "#主题/AI-Coding"

# 按双向链接（精确/前缀/包含三级匹配）
python3 scripts/wiki-query.py backlink "Codex"

# 按分类
python3 scripts/wiki-query.py category "02-ai-coding"

# 按日期
python3 scripts/wiki-query.py date "2026-06"

# 全文检索（ripgrep）
python3 scripts/wiki-query.py text "知识库"

# 找孤立节点
python3 scripts/wiki-query.py orphan

# 找缺 frontmatter 的文章
python3 scripts/wiki-query.py frontmatter-missing
```

### `theme-search.py` — 主题多轮筛选
```bash
# 输入主题 → 提取关键词 → 多轮 ripgrep 收窄 → 排序输出
python3 scripts/theme-search.py "知识工作者编排 Agent"
python3 scripts/theme-search.py "Codex 知识库 优化" --rounds 2
python3 scripts/theme-search.py "Harness 实践" --limit 10
```

**优势**：
- ⚡ 极快（毫秒级，无 LLM 介入）
- 💰 Token 成本几乎为 0
- 🎯 命中精确（基于 frontmatter / 双向链接 / 全文）

### `morning-digest.py` — 升级支持节点融合
晨间简报新增"🌱 今日新节点（发芽报告升级版）"章节：
- 自动从最近 48h 新增的 wiki 文章里提取 frontmatter.nodes
- 为每个新节点找 3-5 个关联节点（精确匹配 + 双向链接 substring 匹配）
- 提示用户做"节点碰撞"——这是 LLM-Wiki 发芽报告的核心动作

---

## 📐 新文章结构（2026-06 起生效）

参考 LLM-Wiki Skill 的"三层存储 + 知识节点"思想：

1. **YAML Frontmatter**（新文章必填，老文章不动）
   ```yaml
   ---
   title: 文章标题
   category: 02-ai-coding
   tags: [#主题/AI-Coding, #场景/公众号长文, #节点/Codex]
   nodes: [Codex, 知识工作者, 工作流编排, 多任务并行, 知识产物]
   links: [[Codex才是最适合普通人的顶级牛马-Agent]], [[AI-Coding的顿悟时刻]]
   date: 2026-06-04
   source: 微信公众号 / 智见AI
   ---
   ```

2. **知识节点**（替代原"要点列表"）
   - 每条独立成段可理解
   - 对应一个可 grep 的关键词（2-6 字中文 / 1-3 词英文）
   - 5-10 条最核心节点

3. **关联图谱**（新增区）
   - 上游（基于 / 来自）
   - 下游（应用于 / 验证于）
   - 同级（横向 / 并列）

完整模板见 `prompts/wiki-template.md`。

---

**最近升级**：2026-06-04
**升级原因**：参考 LLM-Wiki Skill 核心方法论
**存量文章**：133 篇不强制升级，lint 报告可标记
