# Claude + Obsidian should be illegal

## 原文信息
- **作者**: Defileo 🔮 (@defileo)
- **链接**: https://x.com/defileo/status/2042241063612502162
- **发布日期**: 2026年4月9日
- **数据**: 198 回复、1128 转帖、9595 喜欢、45932 书签、718万+ 查看

---

## 核心观点

Every morning I open my laptop, Before I type a single word, Claude already knows who I am, what I'm working on, every crypto tool I use, every open task, every article I've ever written, and every idea I've ever captured. That's not a chatbot, that's a second brain that never sleeps, never forgets, and gets smarter every single day you use it.

## 内容摘要

### 作者的 setup 做了什么
每天早上打开电脑，在输入任何内容之前，Claude 已经知道：
- 你是谁
- 你在做什么项目
- 你使用的每个 crypto 工具
- 每个待办任务
- 每篇写过的文章
- 每个捕捉过的想法

这不是聊天机器人，而是一个永不睡觉、永不忘记、每天使用都会变得更聪明的第二大脑。

### 如何在 5 分钟内建立你的第二大脑

#### 第一步：下载 Obsidian
链接：https://obsidian.md/

#### 第二步：创建你的第二大脑（Vault）
给 Vault 起个名字，作者的叫 "Leo's workspace"

#### 第三步：下载 Claude Code
链接：https://claude.com/product/claude-code

#### 第四步：在 Claude Code 中选择你的 Vault

#### 第五步：使用 Andrej Karpathy 的提示词（核心）
作者提供了两段式提示词，是整个系统的核心。

---

## LLM Wiki A pattern（核心架构）

作者详细描述了一个基于 LLMs 构建个人知识库的架构模式：

### 核心思想
大多数人与 LLMs 和文档的交互方式像 RAG：上传文件集合，LLM 在查询时检索相关片段，然后生成答案。这种方式每次问题都要从头发现知识，没有积累。

新思路：LLM **增量构建和维护一个持久的 wiki**——一个结构化的、互相链接的 markdown 文件集合，介于你和原始资料之间。当你添加新资料时，LLM 不仅为其索引供后续检索，而是读取它、提取关键信息，并将其整合到现有 wiki 中——更新实体页面、修订主题摘要、注意新数据与旧声明的矛盾、加强或挑战不断发展的综合知识。

关键区别：**wiki 是一个持久的、复合的产物**。交叉引用已经在那里了。矛盾已经被标记了。综合已经反映了你所阅读的一切。wiki 随着你添加的每个来源和你提出的每个问题而不断丰富。

### 三层架构

**1. Raw sources（原始资料）**
你策划的源文档集合。文章、论文、图片、数据文件。这些是不可变的——LLM 从中读取但从不修改。这是你的真相来源。

**2. The wiki（wiki）**
LLM 生成的 markdown 文件目录。摘要、实体页面、概念页面、比较、概述、综合。LLM 完全拥有这一层。它创建页面、在新来源到来时更新它们、维护交叉引用并保持一切一致。你阅读它；LLM 编写它。

**3. The schema（模式）**
一个文档（例如 Claude Code 的 CLAUDE.md 或 Codex 的 AGENTS.md），告诉 LLM wiki 是如何组织的、约定是什么，以及在摄取来源、回答问题或维护 wiki 时遵循什么工作流程。这是关键的配置文件——它使 LLM 成为有纪律的 wiki 维护者而不是通用聊天机器人。你和 LLM 随着你对领域的理解共同发展这个。

### 操作

**Ingest（摄取）**
你将新来源放入原始集合并告诉 LLM 处理。示例流程：LLM 读取来源、与你讨论关键要点、在 wiki 中写摘要页面、更新索引、在整个 wiki 中更新相关实体和概念页面，并在日志中附加条目。一个来源可能涉及 10-15 个 wiki 页面。

**Query（查询）**
你针对 wiki 提出问题。LLM 搜索相关页面、读取它们并用引用综合答案。答案可以有不同的形式取决于问题——markdown 页面、比较表、幻灯片（Marp）、图表（matplotlib）、画布。

重要洞见：**好的答案可以作为新页面归档回 wiki**。你要求的比较、分析、你发现的联系——这些是有价值的，不应该消失在聊天历史中。这样你的探索就像摄入的来源一样在你的知识库中积累。

**Lint（检查）**
定期让 LLM 对 wiki 进行健康检查。寻找：页面之间的矛盾、新来源已取代的过时声明、没有入站链接的孤立页面、被提及但缺乏自己页面的重要概念、缺失的交叉引用、可能通过网络搜索填补的数据空白。LLM 善于建议新的问题来调查和寻找新的来源。这随着 wiki 的增长保持 wiki 健康。

### 两个特殊文件

**index.md** 是面向内容的。它是 wiki 中所有内容的目录——每个页面列出一个链接、一行摘要和可选的元数据如日期或来源数量。按类别组织（实体、概念、来源等）。LLM 在每次摄取时更新它。回答查询时，LLM 首先读取索引以找到相关页面，然后深入研究它们。这在中等规模（约 100 个来源、数百个页面）下效果出奇地好，避免了对基于嵌入的 RAG 基础设施的需求。

**log.md** 是时间序的。它是一个append-only的记录，记录发生了什么以及何时——摄取、查询、lint 通过。一个有用的提示：如果每个条目以一致的前缀开始（例如 `## [2026-04-02] ingest | Article Title`），日志可以用简单的 unix 工具解析——`grep "^## \[" log.md | tail -5` 给你最后 5 个条目。日志给你 wiki 演化的 timeline，并帮助 LLM 理解最近做了什么。

### 工具提示

- **Obsidian Web Clipper** 是一个浏览器扩展，将网页文章转换为 markdown。对于快速将来源放入原始集合非常有用。
- **本地下载图片**。在 Obsidian 设置 → 文件和链接，设置"附件文件夹路径"为固定目录（例如 `raw/assets/`）。然后在设置 → 热键中，搜索"下载"找到"下载当前文件的附件"并绑定到热键（例如 Ctrl+Shift+D）。剪辑文章后，按热键所有图片都下载到本地。这是可选的但有用——它让 LLM 直接查看和引用图片而不是依赖可能损坏的 URL。请注意 LLMs 不能原生地在一次传递中读取带有内联图片的 markdown——解决方案是让 LLM 先读取文本，然后分别查看一些或所有引用的图片以获得额外上下文。
- **Obsidian 的图形视图** 是查看 wiki 形状的最佳方式——什么连接到什么，哪些页面是中心，哪些是孤立的。
- **Marp** 是一个基于 markdown 的幻灯片格式。Obsidian 有它的插件。可用于直接从 wiki 内容生成演示文稿。
- **Dataview** 是一个 Obsidian 插件，对页面 frontmatter 运行查询。如果你的 LLM 向 wiki 页面添加 YAML frontmatter（标签、日期、来源计数），Dataview 可以生成动态表格和列表。
- wiki 只是一个 git 仓库的 markdown 文件。你免费获得版本历史、分支和协作。

### 为什么这有效

维护知识库的繁琐部分不是阅读或思考——而是簿记。更新交叉引用、保持摘要当前、注意新数据与旧声明的矛盾、在数十个页面间保持一致。人类放弃 wiki 是因为维护负担增长快于价值。LLMs 不会感到无聊、不会忘记更新交叉引用、可以一次触及 15 个文件。wiki 保持维护，因为维护成本接近于零。人类的工作是策划来源、引导分析、提出好问题、思考这一切意味着什么。LLM 的工作是其他一切。

这个想法在精神上与 Vannevar Bush 的 Memex（1945）相关——一种个人策划的知识存储，文档之间有关联轨迹。 Bush's 的愿景比网络变成的更接近这个：私人、积极策划，文档之间的连接与文档本身一样有价值。他无法解决的部分是谁来做维护。

### 注意

这个文档故意抽象。它描述了这个想法，而不是具体的实现。确切的目录结构、模式约定、页面格式、工具——所有这些都将取决于你的领域、你的偏好和你的 LLM 选择。以上提到的所有都是可选的和模块化的——选择有用的，忽略不是的。例如：你的来源可能只有文本，所以你根本不需要图片处理。你的 wiki 可能很小，索引文件就是你需要的，没有搜索引擎。你可能不关心幻灯片，只想要 markdown 页面。你可能想要完全不同的输出格式集合。正确使用这种方式是与你的 LLM 代理分享它，并共同努力实例化一个适合你需求的版本。文档的唯一工作是传达这个模式。你的 LLM 可以弄清楚其余的。

---

## 实际操作：日常运行

### Ingest（摄取）
用 Web Clipper 剪辑文章，它进入原始来源文件夹，你告诉 Claude：
```
claude -p "I just added an article to /raw-sources. Read it, extract the key ideas, write a summary page to /wiki/summaries/, update index.md with a link and one-line description, and update any existing concept pages that this article connects to. Show me every file you touched." --allowedTools Bash,Write,Read
```
一篇文章：Claude 链接 10-15 个 wiki 页面，浮现意想不到的联系，标记矛盾，准确记录什么改变了。

### Query（查询）
问 wiki，Claude 扫描索引、提取正确页面、用引用回答。然后它将最佳输出保存回 wiki——比较、分析、新的联系——所以见解不会在聊天中消失，你的知识库会积累。

### Lint（检查）
每周运行一次：
```
claude -p "Read every file in /wiki/. Find: contradictions between pages, orphan pages with no inbound links, concepts mentioned repeatedly but with no dedicated page, and claims that seem outdated based on newer files in /raw-sources/. Write a health report to /wiki/lint-report.md with specific fixes." --allowedTools Bash,Write,Read
```
你的知识库自动保持健康，维护不再是你的工作。

### 早晨简报（设置一次，永远运行）
```
claude -p "Write a Python script called morning_digest.py that: 1) reads Memory.md and surfaces any open actions due today 2) reads any new files added to /raw-sources in the last 24 hours 3) prints a clean briefing to the terminal. Then schedule it as a cron job every morning at 7:30am." --allowedTools Bash,Write
```
你设置一次，每天早上它运行，你不用碰任何东西。

### 处理通话记录并更新整个系统
```
claude -p "Read the transcript in /transcripts/call-today.md. Extract every decision made, every action item with owner and deadline, and a 3-bullet summary. Add actions to /Action-Tracker.md, log decisions to /Decision-Log.md, and create a client note in /clients/ linking back to this transcript." --allowedTools Bash,Write,Read
```
每个决定归档，每个动作跟踪，再也不会在聊天历史中丢失任何东西。

---

## 为什么几乎没有人有这个

这个还没有普及的原因很简单：构建了它的人没有清楚地解释它，而需要它的人不知道它存在。

大多数第二大脑项目以同样的方式死去。你开始很有条理。维护堆积，更新标签，保持交叉引用当前，当结构发展时重新组织。

这是额外的工作在一个满负荷的工作量之上 -> 你跳过它，系统退化 -> 你回到零散的笔记。

六个月后你尝试重建它，循环重复。

Claude 永久打破那个循环，维护只是一个命令。重新组织整个 vault 是一个提示。从 Notion 迁移？一个命令处理每个导出的文件，添加正确的属性，并将一切重新构建到你的新系统中。

人类的工作是策划来源、提出好问题、思考这一切意味着什么。
Claude 的工作是其他一切——总结、交叉引用、归档和簿记，使知识库真正随着时间有用。

Vannevar Bush 在 1945 年描述了类似的东西，一个个人策划的知识存储，文档之间的连接与文档本身一样有价值。他称之为 Memex，他无法解决的部分是谁来做维护。

现在你知道谁来做了：Build this once -> Use it forever, and it gets better every single day you add to it.

这就是为什么它应该是非法的。 - Leo

---

标签：#主题/AI Coding #主题/AIAgent #主题/效率 #手法/对比冲突 #场景/技术博客

相关链接：
- https://obsidian.md/
- https://claude.com/product/claude-code