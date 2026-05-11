# Google Agent Skill 设计模式：5种模式补上"内容设计"缺口

> 来源：Google Cloud Tech《5 Agent Skill design patterns every ADK developer should know》
> 整理：TopSee AI | 整理时间：2026-05-06

---

## 核心观点

### 1. Skills 从"格式怎么写"进化到"工作流怎么设计"

- **Anthropic** 解决了 Skill 的格式、加载、跨产品使用问题
- **Google** 补上了 Skill 的内容设计模式
- SKILL.md 的格式已经有共识，难点转到内部：这个 Skill 的工作流逻辑该怎么设计

> "Skill 不是普通文档。普通文档主要给人读，允许人自己补上下文、自己判断顺序、自己决定什么时候停。Skill 是给 Agent 在运行时读的。它要参与决策，进入上下文，影响工具调用，甚至影响文件修改和发布动作。"

### 2. Skill 更接近"过程资产"，不是"提示词模板"

- 提示词模板解决的是一次对话怎么说
- 过程资产解决的是这类事情以后怎么做

### 3. 5个模式对应5类失败修复

| 模式 | 解决的问题 | 典型场景 |
|------|----------|---------|
| **Tool Wrapper** | Agent 不懂某个库、框架或团队规范 | FastAPI、Terraform、Pandas 规范 |
| **Generator** | 每次输出结构都不稳定 | 报告、PR描述、API文档、周报 |
| **Reviewer** | 审查标准混在提示词里，难复用 | 代码审查、安全审查、Prompt审查 |
| **Inversion** | Agent 没问清需求就开始生成 | 架构设计、需求分析、迁移规划 |
| **Pipeline** | 复杂任务容易跳步骤 | 文档生成、发布、Incident复盘 |

---

## 各模式详解

### Tool Wrapper：按需加载的领域手册

**问题**：把 FastAPI、Terraform、Pandas 等规范塞进系统提示词，窗口很快变重。

**方案**：整理成 Skill，只有真正需要时才加载。大块知识留在外面（references/），SKILL.md 只负责触发和导向。

**关键**：
- 控制上下文进入方式
- 长期稳定、低频使用、领域明确的知识适合放这里
- 上下文窗口不适合当资料仓库

### Generator：带模板的填空流程

**问题**：报告、PR描述、周报、API文档，每次格式都不一样，一次看着不错，十次放在一起就乱。

**方案**：
- assets/ 放模板
- references/ 放风格指南
- SKILL.md 负责协调加载、补齐变量、填充模板

**关键分工**：
- 模板归模板
- 风格指南归风格指南
- 缺失变量单独补齐
- 该保留的章节就保留

### Reviewer：可替换的评分清单

**问题**：代码审查、安全审查、Prompt审查，把"怎么审"和"审什么"混在一个系统提示词里，早期能跑，后期很难维护。

**方案**：
- 把标准放进 references/review-checklist.md
- Skill 只规定审查协议

**协议要点**：
- 先读代码，理解目的
- 再按清单检查
- 按严重程度输出
- 解释为什么有问题，给具体修复建议

**核心类比**：和软件工程里的测试、Lint、静态扫描很像。清单可以版本化、替换、按项目分层。Agent 负责应用标准，不负责临时发明标准。

### Inversion：需求访谈器

**问题**：用户一句"帮我设计一个系统"，Agent 立刻开始画架构、选数据库，一口气说完看起来很完整，实际上很多关键约束都没问。

**方案**：把流程倒过来，Agent 先当采访者。

**示例**（项目规划 Skill）：
- 先问清问题、用户、规模
- 再问部署环境、技术栈、非协商约束
- 不到这些阶段完成，不进入最终方案合成

**最重要的**：门控。"如果需要可以提问"通常不够，Agent 很容易觉得自己已经知道了然后继续生成。需要明确阶段、退出条件、以及什么时候不能继续。

**适合场景**：
- 架构设计
- 需求分析
- 迁移规划
- 安全评估
- 企业流程自动化

### Pipeline：带检查点的工作流

**问题**：文档生成、发布、数据迁移、代码重构、Incident复盘，都不是"一次输出"能解决的任务。它们需要先清点，再生成，再确认，再组装，再质检。

**方案**：Pipeline 的关键是检查点。

**示例**（文档流水线）：
1. 解析公开 API，列成清单，让用户确认
2. 生成 docstring
3. 确认后才能进入组装
4. 最后按质量清单检查

**核心**：复杂任务最怕的不是慢，而是 Agent 把前置条件跳过去，直接给一个看起来完整、实际未经验证的结果。

---

## Skill 和 Harness 是一回事的两面

**Harness** 负责运行时主循环：
- 上下文怎么组
- 工具怎么调
- 状态怎么留
- 错误怎么反馈
- 权限怎么收口

**Skill** 负责把某类可复用方法带进运行时：
- 这类 API 怎么写
- 这类文档怎么生成
- 这类代码怎么审
- 这类需求怎么问
- 这类流程怎么跑

> "Skill 是 Harness 可以按需加载的过程模块。"

---

## 从"写提示词"到"设计工作流"

Agent 工程正在过一个分界点：
- 早期：怎么把一句 prompt 写好
- 后来：上下文怎么组织，工具怎么暴露，Subagent 怎么隔离，MCP 怎么接外部系统
- 现在：团队经验、流程、清单、模板、排障方法，开始被做成模型可发现、可加载、可执行的工作单元

---

## 写 Skill 前先问6个问题

### 1. 它什么时候该触发？

description 更像路由契约。如果只写"帮助处理部署相关任务"，触发边界会很虚。

更清楚的写法：
- 当用户要发布 Next.js 服务到 Vercel 时使用
- 当用户要检查预览环境时使用
- 当用户要处理构建失败时使用
- 当用户要回滚部署时使用

### 2. 它属于哪种模式？

先问一句：这个 Skill 主要是在注入知识、生成模板、审查结果、收集需求，还是跑流程？

- 知识注入 → Tool Wrapper
- 输出格式稳定 → Generator
- 质量门禁 → Reviewer
- 模糊需求 → Inversion
- 多阶段有验收点 → Pipeline

### 3. 哪些东西适合拆出去？

- 稳定但很长的规范 → references/
- 固定输出模板 → assets/
- 确定性、重复性动作 → scripts/
- 主文件只保留：路由、流程、边界和加载规则

### 4. 哪些步骤需要停下来？

生产级 Skill 通常需要检查点：
- 需求没问完，不生成架构方案
- API 清单没确认，不生成最终文档
- 测试没跑过，不宣称修复完成
- 风险项没分级，不进入发布建议
- 破坏性操作没确认，不执行

### 5. 失败以后怎么走？

很多 Skill 只写成功路径。现实里最常见的是失败路径：
- 依赖没装
- 环境变量缺失
- 测试超时
- API 返回 403
- 用户给的信息不够
- 文件结构和预期不一致

一个好的 Skill 至少要说清楚：
- 怎么识别失败
- 失败时先收集什么证据
- 哪些可以自动重试
- 哪些需要停下来问人
- 哪些动作不能为了完成任务而绕过去

### 6. 它怎么被版本化和审查？

Skill 一旦进入团队工作流，就更接近代码资产，而不是临时文档。

至少可以加几件事：
- 每个 Skill 有 owner
- 每次修改走 review
- 高风险 Skill 有测试样例
- 关键流程有变更记录
- 废弃规则定期清理
- 第三方 Skill 默认不信任，先读再启用

---

## 来源信任策略

| 来源 | 信任策略 |
|------|---------|
| 官方内置 Skill | 较高信任，但仍要看版本 |
| 团队自写 Skill | 走 review、测试和变更记录 |
| Agent 自动生成 Skill | 默认草稿，需要有人确认 |
| 社区第三方 Skill | 默认不信任，先做安全审查 |
| 带脚本 Skill | 按可执行代码对待，不按普通文档 |

---

## 重要提醒

**Skill 里的负面约束**会影响它有没有越权。Claude Code 文档里有一句很实在的话：

> "如果某条规则每次都要成立，更适合用 Hook 这类确定性机制强制，而不是只写在提示或 Skill 里。"

这就是工程边界：
- Skill 适合让 Agent 理解和应用流程
- 安全底线、危险命令阻断、权限控制、审计记录，更适合下沉到确定性更强的层

---

## 参考资料

- Google Cloud Tech：《5 Agent Skill design patterns every ADK developer should know》https://x.com/GoogleCloudTech/status/2033953579824758855
- Claude 官方博客：Introducing Agent Skills https://claude.com/blog/skills
- Claude Code Docs：Extend Claude with skills https://code.claude.com/docs/en/skills
- Anthropic 官方 PDF：The Complete Guide to Building Skills for Claude https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Simon Willison：Claude Skills are awesome, maybe a bigger deal than MCP https://simonwillison.net/2025/Oct/16/claude-skills/
- Zak El Fassi：SkDD: Skills-Driven Development https://zakelfassi.com/skdd-skills-driven-development