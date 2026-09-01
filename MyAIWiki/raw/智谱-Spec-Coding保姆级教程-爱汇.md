---
title: Spec Coding 保姆级教程
source: 智谱AI开放文档（原作者：爱汇）
source_url: https://docs.bigmodel.cn/cn/coding-plan/best-practice/spec-kit
wechat_url: https://mp.weixin.qq.com/s/CRH4WWtrA_3APBBFD1zMiQ
fetched: 2026-08-27
category_target: 02-ai-coding
tags:
  - 主题/AI-Coding
  - 场景/技术博客
  - 节点/Spec-Kit
  - 节点/SDD
---

# Spec Coding 保姆级教程（原文存档）

> 巧用 Spec-Kit，把AI训练成靠谱工程师！
>
> 本文作者：爱汇\
> 原文链接：https://mp.weixin.qq.com/s/CRH4WWtrA_3APBBFD1zMiQ

## 文档元数据

| 字段 | 值 |
|---|---|
| 原标题 | Spec Coding 保姆级教程 |
| 副标题 | 巧用 Spec-Kit，把AI训练成靠谱工程师！ |
| 作者 | 爱汇 |
| 首发平台 | 微信公众号（mp.weixin.qq.com） |
| 重发布平台 | 智谱AI开放文档（docs.bigmodel.cn） |
| GitHub 项目 | github.com/github/spec-kit（34k+ Star） |
| 抓取方式 | Mintlify 自动生成的 `spec-kit.md` 端点（HTTP 200, 12.8KB, 0.7s） |
| 抓取时间 | 2026-08-27 |

## 原文正文

（来自 Mintlify markdown 源端点 `/cn/coding-plan/best-practice/spec-kit.md`，完整保留）

### 前言：您是不是也被"Vibe Coding"逼疯过？

"我叫小张，一个天天跟 AI 结对编程的程序员。就在上周，我差点被AI逼疯了。"

> AI："没问题，看我的！"(一顿操作猛如虎，生成一堆代码)
> 您："不对不对，这里应该用JWT认证，不是Session啊喂！"
> AI："好的，已修改。"(又是一顿操作)
> 您："等一下！密码加密我要用Argon2，不是您默认的MD5！说过多少次了！"
> AI："..."

这种靠感觉、靠默契、反复试错，在跟 AI 的不断拉扯中勉强推进的开发模式，就是现在最火的词—— **"Vibe Coding"（感觉式编程）**。

在小项目里跑跑还行，但项目变复杂、团队一扩大，弊端就全暴露了：
- **需求理解全靠猜**：AI 常常"会错意"，做出来的东西跟想的完全是两码事
- **技术选型像开盲盒**：AI 可能随手就选不熟的技术栈，后续维护火葬场
- **代码质量堪忧**：生成的代码能跑，但结构乱七八糟，别说交接，自己看都费劲
- **协作基本为零**：除了您和AI，没人知道这功能是怎么"感觉"出来的

### 一、Spec-Kit 是啥？从"代码为王"到"规范为王"

**Spec-Kit 不是新的 AI 编程工具，它是一套工作流和方法论。**

通过命令行工具和模板，把"虎"的 AI 助手（Claude Code / Copilot / Gemini）调教成"靠谱工程师"。

核心理念：**规格驱动开发（Spec-Driven Development, SDD）**

- 传统开发：`规格`（爱看不看的文档）→ `代码`（一顿瞎写）→ `代码成为唯一真理`
- Spec-Kit 开发：`规格`（可被执行的指令）→ `计划`（AI自动生成）→ `任务`（AI自动拆解）→ `代码`（AI按图施工）→ `规格成为唯一真理`

> **一句话：代码为规格服务，而不是规格为代码服务。**

类比：Vibe Coding 像没图纸凭感觉盖茅草屋；Spec Coding 像先有图纸再按图盖摩天大楼。

### 二、Spec-Kit 的"六步流水线"

以开发 Todo List 为例走完整流程。

#### 第一步：准备工作（安装与初始化）

```bash
# 推荐用 uv（Python 包管理工具）
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 创建项目并初始化
specify init my-todo-app
cd my-todo-app
```

初始化时选 AI 助手（本文用 Claude Code + GLM4.6）和脚本类型（sh）。完成后项目会多出 `.claude/` 和 `.specify/` 目录。

#### 第二步：立规矩（`/constitution`）—— 给项目立"宪法"

可选但**强烈推荐**。项目开始前定好基本原则和约束。

```
/speckit.constitution 这是一个基于React的待办事项应用，要注重简洁和用户体验。
```

AI 会生成 `constitution.md`，包含：
- 技术栈偏好（优先 React Hooks，不用 Class Components）
- 代码风格（Airbnb JavaScript Style Guide）
- 测试要求（核心功能必须有单元测试）
- 用户体验原则（响应时间 <100ms）

这份"宪法"是天条，后面所有开发工作都得按这个来。

#### 第三步：提需求（`/specify`）—— 您只要说"要什么"

只谈功能，别谈技术。

```
/speckit.specify 我要做一个待办事项应用。
核心功能：
- 用户可以添加新的待办事项。
- 用户可以标记待办事项为"已完成"。
- 用户可以删除待办事项。
- 完成任务时，要有一个好玩儿的庆祝动画。
```

Spec-Kit 会：
1. 在 `specs/` 下创建新版本（如 `001-todo-app-core-features`）
2. 生成详细 `spec.md`（用户故事、验收标准、边界条件）
3. 自动建新 Git 分支（如 `feat/001-todo-app-core-features`）

#### 第四步：清疑点（`/clarify`）—— 消除模棱两可

可选。需求模糊时（如"好玩儿的动画"）让 AI 主动追问。

```
/speckit.clarify
```

AI 可能会反问：
- Q1：庆祝动画是放烟花还是撒花？
- Q2：待办事项有字数限制吗？
- Q3：要不要支持任务优先级？

回答后 AI 自动更新 `spec.md`。

#### 第五步：出方案（`/plan`）—— AI 变身架构师

```
/speckit.plan
```

AI 根据"宪法"和"需求"生成完整技术方案文档：
- `plan.md`：技术栈决策（React 18 + Zustand + Framer Motion）
- `data-model.md`：数据结构定义（如 Todo 长啥样）
- `contracts/`：API / 组件接口定义
- `research.md`：为啥这么选型，做了哪些调研

#### 第六步：拆任务（`/tasks`）—— 把大象装进冰箱

```
/speckit.tasks
```

AI 把 `plan.md` 拆成详细 `tasks.md`：

```
Phase 1: 项目设置 (3 个任务)
- [ ] T001: 初始化 React + Vite 项目。
- [ ] T002: 安装 Zustand 和 Framer Motion 依赖。
- [ ] T003: 配置 ESLint 和 Prettier。

## Phase 2: 核心组件开发 (4 个任务)
- [ ] T004: 开发 TodoItem 组件。
- [ ] T005: 开发 AddTodoForm 组件。
```

可选 `YOLO` 模式一口气干完，或每个任务后人工检查。

#### 第七步：写代码（`/implement`）—— AI 终于"施工"

```
/speckit.implement
```

AI 严格按 `tasks.md` 列表完成编码、写测试，每搞定一个就 `[x]` 打勾。稍等一会儿就得到一个结构清晰、文档齐全、完全符合所有规范的 Todo App。

### 三、Spec-Kit 的核心价值

1. **高质量、可预测的输出**：前置规范管住 AI 自由发挥，产出更符合预期
2. **自动化文档生成**：需求/方案/任务全记录，形成跟代码同步的"活文档"，不怕过期
3. **团队协作效率飙升**：标准化流程降低沟通成本，维护简单
5. **沉淀团队最佳实践**：架构约定/代码规范写进 `/constitution`，让经验变可复用资产
5. **真正的"AI 工程师"**：从"打字员"变"工程师伙伴"

### 四、常见问题 FAQ

**Q1：会不会很复杂反而增加工作量？**
上手需一点点学习成本。中大型项目长期看绝对提升效率；小 demo 直接用 AI 助手就行。

**Q2：能在老项目里用吗？**
可以！项目根目录运行 `specify init .`，不动现有代码，先从小功能试点。

**Q3：需求变了咋办？**
回到第三步 `/specify` 描述新需求，Spec-Kit 创建新版本和分支，再走 `/plan`、`/tasks`、`/implement`。历史版本都保留，迭代过程清清楚楚。

**Q4：支持哪些 AI 工具？**
几乎所有主流：GitHub Copilot、Claude Code、Gemini、Cursor、通义千问、Roo Code 等。初始化时随便选。

### 结语

> **Vibe Coding 已死，Spec Coding 当立！**

Spec-Kit 把软件工程"先想清楚再动手"的古老智慧，跟 AI 的强大生产力完美结合。

GitHub 地址：https://github.com/github/spec-kit

## 关键事实清单（编译参考用）

- **GitHub 项目**：github.com/github/spec-kit（34k+ Star）
- **命令行工具**：`specify-cli`，通过 `uv tool install` 安装
- **六步流程**：constitution → specify → clarify（可选）→ plan → tasks → implement
- **支持 AI 助手**：Claude Code、GitHub Copilot、Gemini、Cursor、通义千问、Roo Code 等
- **生成产物目录**：
  - `.claude/` + `.specify/`（初始化产生）
  - `constitution.md`（项目宪法）
  - `specs/{NNN}-{slug}/spec.md`（需求规格）
  - `plan.md` + `data-model.md` + `contracts/` + `research.md`（技术方案）
  - `tasks.md`（任务清单）
- **核心哲学**：SDD = Spec-Driven Development，规格成为唯一真理
- **与 Vibe Coding 对比**：Vibe = 感觉式反复试错；Spec = 规格驱动可预测