# AI 编程三剑客：Spec-Kit、OpenSpec、Superpowers 深度对比与实战指南

> 来源：微信公众号  
> 深入介绍 GitHub 官方 Spec-Kit、社区热门 OpenSpec、跨平台方法论工具 Superpowers

## 一句话总结

| 工具 | 解决什么问题 | 类比 |
|------|------------|------|
| **Spec-Kit** | 按什么规矩干 | 建筑规范手册 |
| **OpenSpec** | 改了什么 | 施工变更单 |
| **Superpowers** | 怎么干 | 施工队工作手册 |

---

## 一、Spec-Kit：GitHub 官方的规范驱动开发框架

**仓库：** https://github.com/github/spec-kit  
**Stars：** 69.1k ⭐  
**技术栈：** Python (uv 包管理器)  
**适用 AI：** Claude Code、Copilot Agent 等

### 核心理念：先写规范，再写代码

### 5 阶段斜杠命令流程

```
/speckit.constitution  →  /speckit.specify  →  /speckit.plan  →  /speckit.tasks  →  /speckit.implement
   项目宪法              功能规范            技术计划         任务分解         执行实现
```

### 生成的文件

| 文件 | 内容 |
|------|------|
| `constitution.md` | 代码质量标准、测试规范、用户体验要求、性能要求 |
| `spec.md` | 用户故事、功能需求（只关注 what 和 why，不涉及技术栈）|
| `plan.md` | 技术栈选择、架构设计、API 契约 |
| `tasks.md` | 可执行的任务清单 |

### 安装

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装 Specify CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 3. 验证安装
specify check
```

### 初始化项目

```bash
# 创建新项目
specify init my-project --ai claude

# 在当前目录初始化
specify init . --ai claude
```

### 目录结构

```
your-project/
├── .specify/
│   ├── memory/
│   │   └── constitution.md  # 项目宪法
│   ├── scripts/              # 内置脚本
│   ├── specs/                # 功能规范目录
│   └── templates/            # 模板文件
└── CLAUDE.md                 # AI 助手配置
```

### 完整使用流程示例

```bash
# 1. 建立宪法
/speckit.constitution 建立代码质量、测试标准和用户体验一致性的原则

# 2. 定义规范
/speckit.specify Develop Taskify, a team productivity platform...

# 3. 技术计划
/speckit.plan We are going to generate this using .NET Aspire...

# 4. 分解任务
/speckit.tasks

# 5. 执行实现
/speckit.implement
```

---

## 二、OpenSpec：轻量级规范驱动开发工具

**仓库：** https://github.com/Fission-AI/OpenSpec  
**Stars：** 23.7k ⭐  
**技术栈：** TypeScript (npm)  
**适用 AI：** Claude Code、Cursor、Windsurf、OpenCode、Codex、Copilot 等 20+ 工具

### 核心理念：灵活的动作式工作流（OPSX Workflow）

```
/opsx:new  →  /opsx:continue  →  /opsx:apply  →  /opsx:archive
  创建       逐步实施         执行任务       归档知识库
```

### 核心命令

| 命令 | 描述 |
|------|------|
| `/opsx:new` | 开始新变更（创建 proposal） |
| `/opsx:continue` | 逐步创建工件（按依赖关系） |
| `/opsx:apply` | 执行任务，实时更新工件状态 |
| `/opsx:archive` | 归档到知识库 |
| `/opsx:explore` | 探索想法，思考问题 |
| `/opsx:ff` | 快速前进，一次性创建所有工件 |
| `/opsx:sync` | 同步到主分支 |

### 安装

```bash
# 全局安装（推荐）
npm install -g @fission-ai/openspec@latest

# 或使用 npx 直接运行
npx @fission-ai/openspec init
```

### 配置文件示例（可选）

```yaml
# openspec/config.yaml
schema: spec-driven
context: |
  Tech stack: TypeScript, React, Node.js
  API conventions: RESTful, JSON responses
  Testing: Vitest for unit tests, Playwright for e2e
  Style: ESLint with Prettier, strict TypeScript

rules:
  proposal:
    - Include rollback plan
    - Identify affected teams
  specs:
    - Use Given/When/Then format for scenarios
  design:
    - Include sequence diagrams for complex flows
```

### 目录结构

```
your-project/
├── .openspec/
│   ├── changes/              # 活跃变更
│   │   └── archive/         # 归档的变更（知识库）
│   ├── config.yaml           # 项目配置
│   └── schemas/              # 自定义工作流模式
└── .claude/skills/openspec- # 自动生成的技能提示
```

---

## 三、Superpowers：Claude Code 的"施工队工作手册"

**仓库：** https://github.com/obra/superpowers  
**Stars：** 50k ⭐  
**技术栈：** Markdown + JavaScript Plugin  
**适用 AI：** Claude Code、OpenCode、Codex

### 核心理念：让 AI 像高级工程师一样工作

```
┌─────────────────────────────────────────────────┐
│ Superpowers 方法论                               │
├─────────────────────────────────────────────────┤
│ 🧪 TDD-First     强制 AI 先写测试，再写实现       │
│ 🤖 Sub-Agents    拆分复杂任务给专门的子代理        │
│ 📝 Code Review   实现后自动触发代码审查            │
│ 🔍 Exploration   实现前先充分探索代码库            │
│ ✅ Verification  每步都要验证，不盲目前进          │
└─────────────────────────────────────────────────┘
```

### 安装（Claude Code）

```bash
# 在 Claude Code 中执行
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace

# 验证安装（看到 brainstorm、write-plan、execute-plan 三个命令即可）
/help
```

### 核心技能

| 技能 | 用途 |
|------|------|
| `brainstorming` | 任何创造性工作前先头脑风暴，理解需求 |
| `subagent-driven-development` | 子代理驱动开发：每个任务派独立子代理 + 两阶段审查 |
| `executing-plans` | 执行已制定的实施计划 |
| `finishing-a-development-branch` | 完成开发分支：合并、创建 PR |
| `requesting-code-review` | 请求代码审查 |
| `receiving-code-review` | 接收并处理代码审查反馈 |
| `systematic-debugging` | 系统化调试 |
| `test-driven-development` | TDD 工作流 |
| `verification-before-completion` | 完成前验证 |

### 工作原理

```
说出你的需求 → 分析请求类型 → 自动选择合适技能
     ↓
┌─────────────┬─────────────┬─────────────┐
│   新想法    │   有计划    │   要审查    │
│ brainstorming│ subagent   │ requesting  │
│  (头脑风暴) │ (子代理开发) │(代码审查)   │
└─────────────┴─────────────┴─────────────┘
```

### 完整工作流示例（添加优惠券功能）

**Step 1: 头脑风暴**
> "我想添加用户优惠券功能"

- 理解项目上下文（读取 CONSTITUTION.md、扫描代码库）
- 逐个问题澄清（优惠券类型？可否叠加？有次数限制？）
- 提出方案并对比
- 逐步确认设计
- 生成设计文档

**Step 2: 子代理驱动开发**
> "帮我实施优惠券功能，按照上面的设计文档"

- 提取所有任务到 TodoWrite
- 为每个独立任务派发子代理：
  - 🤖 Sub-Agent 1: 实现优惠券模型（TDD + 自审查）
  - 🤖 Sub-Agent 2: 实现认证服务（TDD + 自审查）
  - 🤖 Sub-Agent 3: 实现 API 端点（TDD + 自审查）
  - 🤖 Spec Reviewer: 验证是否符合规范
  - 🤖 Code Quality Reviewer: 代码质量审查
- 重复直到所有任务完成
- 最终整体审查

**Step 3: 代码审查**
> "请帮我审查一下这段代码"

---

## 三者对比总结

| 维度 | Spec-Kit | OpenSpec | Superpowers |
|------|----------|----------|-------------|
| **定位** | 规范文档管理 | 变更工作流 | 执行方法论 |
| **工作方式** | 固定阶段流程 | 灵活动作式 | 技能自动触发 |
| **适合场景** | 大型规范项目 | 快速迭代变更 | 高质量代码交付 |
| **学习成本** | 中等 | 低 | 中等 |
| **AI 编程深度** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**推荐组合：** OpenSpec（快速启动）+ Superpowers（高质量执行）
