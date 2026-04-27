# MyAIWiki 知识库

## 定位

你的 **AI 学习营 + 研发弹药库**。

两大核心用途：
1. **内容创作**：收集好文章，拆解写作套路，积累开头钩子
2. **AI Agent 落地**：收集 Agent 落地方案，辅助 APP 研发

---

## 目录结构

```
MyAIWiki/
├── raw/                    # 原始素材暂存区
│   ├── articles/           # 收藏的文章原文
│   ├── notes/             # 随手记的笔记
│   └── screenshots/       # 截图/图片素材
│
├── wiki/                   # 编译后的知识库
│   ├── master-index.md    # 主索引
│   │
│   ├── ai-agents/         # AI Agent 落地方案 ⭐
│   │   ├── index.md
│   │   ├── agent-architecture.md
│   │   ├── tool-use.md
│   │   ├── memory-systems.md
│   │   ├── workflow-vs-agent.md
│   │   └── cases/          # 落地案例
│   │       ├── index.md
│   │       └── *.md
│   │
│   ├── app-dev/           # APP 研发流程 ⭐
│   │   ├── index.md
│   │   ├── ios/           # iOS 研发
│   │   ├── android/      # Android 研发
│   │   ├── server/       # 后端服务
│   │   └── architecture/  # 架构设计
│   │
│   ├── ai-coding/        # AI Coding ⭐
│   │   ├── index.md
│   │   ├── prompts/      # 常用提示词
│   │   ├── workflows/    # 工作流模板
│   │   └── cases/        # 实战案例
│   │
│   ├── rag-systems/       # RAG 系统
│   │   ├── index.md
│   │   └── *.md
│   │
│   ├── content-creation/   # 内容创作
│   │   ├── index.md
│   │   ├── hooks/        # 开头钩子库
│   │   └── structures/   # 文章结构库
│   │
│   ├── productivity/      # 效率工具
│   │   ├── index.md
│   │   └── *.md
│   │
│   └── ai-tech/           # AI 技术趋势
│       ├── index.md
│       └── *.md
│
└── CLAUDE.md              # 本文件
```

---

## 核心原则

1. **LLM 写，你读** - wiki 是 LLM 的领域，你很少手动编辑
2. **累积式增长** - 每次查询、每次拆解都在增强知识库
3. **索引即检索** - 聪明的文件结构替代复杂的检索算法
4. **透明可解释** - 所有数据都是人眼可读的 Markdown

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

| 命令 | 触发条件 | 输出 |
|------|----------|------|
| `/compile` | 收到文章链接 | 原文 + 拆解 + wiki |
| `/lint` | 要求体检 | 健康报告 |
| `/summary` | 要求存档对话 | 对话精华文档 |
| `/weekly` | 要求周复盘 | 复盘报告 |
| `/idea` | 分享灵感 | 灵感记录文档 |

详见 [[skills|Skills 命令手册]]

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

拆解结果会自动归档到 `wiki/content-creation/`，打上标签：
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
| AI Agent 落地方案 | wiki/ai-agents/index.md |
| APP 研发流程 | wiki/app-dev/index.md |
| AI Coding | wiki/ai-coding/index.md |
| 内容创作 | wiki/content-creation/index.md |
| 效率工具 | wiki/productivity/index.md |
| AI 技术趋势 | wiki/ai-tech/index.md |

---

## 使用示例

### 示例1：收集 Agent 落地方案
```
把我发给你的 [URL] 保存到 raw/
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
保存到 wiki/ai-coding/cases/ 下
```
