# Spec Coding 保姆级教程 — Digest

## 一句话总结

Spec-Kit 把"规格"从静态文档升级为可执行指令（constitution → specify → clarify → plan → tasks → implement 六步流水线），让 Claude Code / Copilot / Gemini 从"打字员"变成按图施工的"靠谱工程师"，终结 Vibe Coding 的反复拉扯。

## 5 核心观点

1. **规格成为唯一真理**：代码为规格服务（而非规格为代码服务）。`规格 → 计划 → 任务 → 代码`四阶段每一步都有可执行产物；改动从改 `spec.md` 开始，而不是改代码后补文档
2. **六步流水线是强制节奏**：constitution（项目宪法）→ specify（需求）→ clarify（消歧）→ plan（方案）→ tasks（拆解）→ implement（施工）。每步都生成 git 友好的版本化产物（如 `001-todo-app-core-features`），全程可回滚
3. **`/constitution` 是项目级宪法**：把技术栈偏好、代码风格、测试要求、UX 原则一次性写入，后面所有 AI 调用都受其约束，相当于给团队积累了一份"可复用的最佳实践资产"
4. **`/clarify` 是 AI 主动追问的反向环节**：需求模糊时让 AI 反过来问你（"庆祝动画是放烟花还是撒花？"），把人类隐含的偏好显式化为 spec 条目，从源头消灭返工
5. **不是取代、是约束 AI**：Spec-Kit 不是新 AI 工具，而是给 Claude Code/Copilot/Gemini 加的一套 harness。AI 的"自由发挥"被前置规范管住，产出更可预测

## 7 分析角度 + 开头钩子

### 角度 1：Vibe Coding 的痛点（焦虑共鸣）
- **钩子 1**：上周我跟 AI 结对差点崩溃，三轮"再改一次"后我才意识到——问题不在 AI，而在我没给它一张图
- **钩子 2**：JWT 还是 Session？Argon2 还是 MD5？AI 反复猜错技术选型，根本原因是它没看过你团队的"宪法"
- **钩子 3**：项目一变复杂，"我也不知道这功能是怎么感觉出来的"——这就是 Vibe Coding 的终极代价

### 角度 2：SDD vs TDD 的范式革命
- **钩子 1**：测试驱动开发（TDD）让代码先有验证；规格驱动开发（SDD）让代码先有蓝图
- **钩子 2**：软件工程那句老话——"先想清楚再动手"，在 AI 时代终于有了工具级的实现
- **钩子 3**：从"代码为王"到"规范为王"，是 AI 编程的 iPhone 时刻

### 角度 3：六步流水线的工程化思维
- **钩子 1**：为什么 SDD 落地难？因为你跳过了 `constitution`。没有宪法的团队，每一次 AI 调用都是重新谈判
- **钩子 2**：`/clarify` 是整个流水线最被低估的一步——AI 主动反问，比人类事后 review 省 10 倍时间
- **钩子 3**：每个 step 都生成 git 友好的版本化产物（`001-xxx/`），这意味着整条流水线天然可回滚、可审计、可对比

### 角度 4：`/constitution` 的组织复用价值
- **钩子 1**：你团队花了 3 年沉淀的"代码风格 + 架构约定"，现在可以写一份 `constitution.md` 让 AI 永远遵守——这不是文档资产，是 AI 时代的"团队记忆移植"
- **钩子 2**：Seetong iOS 项目有 QMUI 强制规范、ST 类前缀、ViewController 命名约定——这些如果都进 `constitution.md`，Claude Code 改你的代码就再也不会用错框架
- **钩子 3**：`/constitution` 不是"AI 的提示词"，是"团队的天条"。提示词是软约束，宪法是硬规则

### 角度 5：AI 工具无关性
- **钩子 1**：Spec-Kit 支持 Claude Code、Copilot、Gemini、Cursor、通义千问、Roo Code——你换 AI 助手不用换工作流
- **钩子 2**：从"锁死 AI 厂商"到"工作流跨厂商可移植"，这是 AI Coding 走向成熟的标志
- **钩子 3**：spec 格式 + plan 格式 + tasks 格式是 AI 中立的。你今天写的 `spec.md`，五年后换个模型照样能跑

### 角度 6：企业落地的现实路径
- **钩子 1**：Q"Spec-Kit 会不会太复杂反而增工作量？"——A：上手小成本，长期返工省大钱；小 demo 别用，中大型项目必用
- **钩子 2**：Q"老项目能用吗？"——A：`specify init .` 不动现有代码，先从小功能试点
- **钩子 3**：Q"需求变了咋办？"——A：回到 `/specify` 描述新需求，建新版本和分支，所有历史保留

### 角度 7：从工具到工程范式的跃迁
- **钩子 1**："Vibe Coding 已死，Spec Coding 当立"——这句话不是口号，是 34k+ Star 的 Spec-Kit 给整个行业敲响的警钟
- **钩子 2**：Spec-Kit 把"软件工程"和"AI 编程"重新缝合在一起——你不用选 AI 能力还是工程纪律，你可以两个都要
- **钩子 3**：未来的 AI 工程师不是"会用 Cursor 的人"，而是"会写宪法 + 会拆任务 + 会验收 AI 产物的人"

## 关键数字 / 事实清单

- **GitHub Star**：34k+（上线才几个月）
- **命令入口**：`specify-cli`（`uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`）
- **六步流水线**：constitution → specify → clarify（可选）→ plan → tasks → implement
- **支持 AI 工具**：Claude Code、GitHub Copilot、Gemini、Cursor、通义千问、Roo Code
- **初始化产物**：`.claude/` + `.specify/`
- **核心文件**：`constitution.md` / `specs/{NNN}-{slug}/spec.md` / `plan.md` + `data-model.md` + `contracts/` + `research.md` / `tasks.md`
- **版本化目录**：`001-todo-app-core-features`（自增数字 + 语义 slug）
- **执行模式**：YOLO（一口气跑完） vs 单任务 review
- **作者**：爱汇（智谱 AI 开放文档首发于微信公众号）
- **概念对比**：Vibe Coding = 感觉式反复试错；Spec Coding = 规格驱动可预测
- **核心理念翻转**：代码为规格服务（而非规格为代码服务）

## 强关联（已有 wiki 文章）

- **同级 / 工具对比**：
  - [[AI编程三剑客-SpecKit-OpenSpec-Superpowers深度对比]] — Spec-Kit vs OpenSpec vs Superpowers 三种 SDD 工具横评
  - [[AI原生研发落地实践-Spec-Kit和BMAD跑了一遍SDD]] — Spec-Kit vs BMAD 在企业落地的对比
- **同级 / 范式讨论**：
  - [[Anthropic发布AI-Native软件开发流程-时代变了-该换套模式了]] — Anthropic 的 AI-Native SDLC（提交产物版本化）
  - [[大淘宝技术-AI-Coding-环境与验证驱动]] — 永霸观点：代码生成被解决后，瓶颈转到环境与验证（与 Spec-Kit 的"规格驱动"互补）
  - [[AI-Coding的顿悟时刻]] — AI Coding 的顿悟系列
- **上游 / 方法论**：
  - [[AICoding之后-如何让Agent进入企业研发全链路-得物推荐的Harness实践]] — Harness 把 SDD 接入企业 PDCA 闭环
  - [[宝玉AI-我的AI原生开发流程-真实案例复盘]] — 宝玉的 AI 原生开发流程（可行性 / 设计 / 原型 / 实现 / 测试）
- **同级 / 文化反思**：
  - [[瑟瑟发抖-WorkBuddy培训结束后-老板开始用AICoding亲自做产品了]] — AI Coding 的组织级下沉
- **概念出处**：Spec-Kit 是 GitHub 在 2025 年开源的 AI Coding 工作流框架，哲学根源可追溯到 ATDD/SBE（Specification By Example）

## 待办（编译 wiki 时落地）

- [ ] 编译 `wiki/02-ai-coding/Spec-Coding保姆级教程-爱汇.md`（主文）
- [ ] 编译 `wiki/02-ai-coding/Spec-Coding保姆级教程-爱汇-digest.md`（速查版）
- [ ] 更新 `wiki/02-ai-coding/index.md`（追加新文章 + digest）
- [ ] 更新 `wiki/master-index.md`（顶部"最近更新"含详细摘要一行式）
- [ ] 更新 `log.md`（追加变更记录）
- [ ] 透明玻璃自检：wiki ≤8K / digest ≤4K / 节点 6-10 / H2 ≤5 / 表格 ≤2 / 0 陈词

## 标签

`#主题/AI-Coding` `#场景/技术博客` `#节点/Spec-Kit` `#节点/SDD` `#节点/规格驱动` `#节点/Vibe-Coding` `#节点/AI-Harness` `#节点/工作流`