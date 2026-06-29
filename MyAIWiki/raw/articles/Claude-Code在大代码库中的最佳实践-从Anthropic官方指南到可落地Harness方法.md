# Claude Code 在大代码库中的最佳实践：从 Anthropic 官方指南到可落地 Harness 方法

- 来源：微信公众号文章
- 原文链接：https://mp.weixin.qq.com/s/l7XskL2QcZyE9YtWt0LpkA
- 编译时间：2026-05-17
- 归档位置：AI Coding / Harness / Claude Code

## 一句话总结

这篇文章的核心不是“Claude Code 在大代码库里怎么搜代码”，而是：**大型代码库里真正决定体验上限的，不只是模型，而是围绕模型搭起来的 Harness**。Anthropic 官方把这套方法拆成了 CLAUDE.md、Hooks、Skills、Plugins、LSP、MCP servers、Subagents 七件套，本质是在解决同一个问题：**如何让 agent 在实时、低噪音、可约束、可扩展的环境里稳定工作。**

## 文章核心观点

### 1. Claude Code 在大代码库里依赖的是 agentic search，而不是 RAG

文章先区分了两种典型路径：

- **RAG**：提前对代码库做 embedding，查询时检索
- **Agentic search**：像工程师一样实时遍历文件系统、grep、读文件、跟踪引用

在持续重构、提交频繁的大仓库里，RAG 的主要问题是**索引滞后**。一旦 embedding 数据不是最新代码，检索结果就可能指向已经重命名、移动、甚至删除的模块。Claude Code 采用实时搜索，虽然更“笨重”，但在高变化代码库里更可靠。

这意味着大仓库要想让 Claude Code 真正好用，重点不在“给它更多全文”，而在于：

- 让目录结构能被快速理解
- 让搜索命中尽量精准
- 让上下文不要被噪音淹没

这也是后面所有工程化实践的基础。

### 2. Harness 比模型更重要

Anthropic 给出的七件套：

- CLAUDE.md
- Hooks
- Skills
- Plugins
- LSP
- MCP servers
- Subagents

作者的判断很明确：**同样的模型，裸跑和带完整 harness 跑，效果完全不是一个量级。**

模型决定“理论能力上限”，而 harness 决定“这个能力到底能被释放多少”。

这和传统软件工程很像：

- 模型像 CPU
- Harness 像操作系统、编译器、调度器、权限系统、调试工具

没有后者，前者再强也很难稳定落地。

### 3. CLAUDE.md 是大代码库里最重要的第一层配置

Anthropic 对 CLAUDE.md 的建议特别实用，核心是**分层加载**。

Claude Code 会从当前目录向上查找 CLAUDE.md，并叠加加载，因此最有效的做法不是把所有规则都塞进根目录，而是：

- **根目录 CLAUDE.md 只保留总览、指针、关键约束**
- **在核心子目录继续放局部 CLAUDE.md**
- 让用户在更靠近任务的位置启动 Claude Code

这种方式的价值在于：

- 让上下文更聚焦
- 不同模块可以有不同的 lint / test / 风格规则
- 避免改一个子服务却触发整个 monorepo 的测试和噪音输出

Anthropic 还建议配合：

- `.ignore` 排除 build、生成代码、vendor 目录
- `.claude/settings.json` 中写 deny 规则，形成项目级约束
- 如果目录结构很差，至少提供一个 codebase map，给 Claude 一张“目录地图”

### 4. Hooks 是最容易低估、却最具约束力的扩展点

文章提到 Hooks 的几个关键事件：

- Start hook
- Stop hook
- PreToolUse
- PostToolUse

它的价值主要有三类：

1. **自动进化**：结束会话时复盘，把经验沉淀到 CLAUDE.md
2. **动态上下文注入**：根据路径、用户、模块自动加载不同配置
3. **硬约束**：危险命令拦截、自动 lint、提交前 typecheck 等

这里有个很重要的工程判断：

> Prompt 是建议，Hook 是约束。

凡是“必须发生”的动作，不应该只寄希望于模型自觉，而应该尽量外置到 hook 或脚本层实现。

### 5. Skills 和 Plugins 解决的是“能力复用”和“团队扩散”

文章把 Skills 定义为“按需加载的专业能力”，强调的不是“把所有说明都提前塞进上下文”，而是 **progressive disclosure（渐进展开）**：

- 常驻的是能力描述
- 真正细节在用到时再加载

这样才适合大代码库和多任务类型场景。

Anthropic 这次还提了一个很有价值的做法：

- **Skill 按路径 scope 激活**

这能显著降低不同技能互相干扰的问题。

Plugins 则更偏组织层：

- 把 skill、hook、MCP、settings 打包成安装包
- 避免能力停留在少数“老员工”的私有配置里
- 让新人一键获得成熟工程能力

从组织视角看，Plugin 真正解决的是 **tribal knowledge 无法扩散** 的问题。

### 6. LSP 让搜索从“字符串匹配”跃迁为“符号级导航”

这一节对大代码库尤其关键。

grep 的问题不是不能用，而是：

- 命中太多
- 无法区分同名符号
- 结果缺少语义

LSP（Language Server Protocol）带来的不是“更快搜索”，而是**从 text search 升级到 symbol search**：

- 直接找定义
- 找引用
- 找调用链
- 识别类 / 方法 / interface 之间的真实关系

这会极大降低 Claude Code 打开无关文件、浪费上下文预算的概率。

尤其在 Go、TypeScript、Java、Python、Rust 等生态较成熟语言里，LSP 是让大代码库 agent 体验“从可用到好用”的关键一跳。

### 7. MCP 和 Subagent：一个解决能力边界，一个解决上下文污染

MCP server 的作用是接入 Claude 本来碰不到的东西，比如：

- 内部 API
- 文档系统
- 搜索服务
- 结构化代码查询能力

文章提到一个很有启发的方向：

- 专门做面向代码库的 MCP server
- 把“查找所有实现某接口的类”“查找所有调用某 deprecated API 的位置”这类能力工具化

这比纯 grep 更稳定，也比让模型自己拼复杂搜索语句更可控。

Subagent 则是上下文管理利器。

文中重点推荐的模式是：

- 让 explore subagent 只做读文件、摸结构、出地图
- 主 agent 拿到总结后再 edit

原因非常现实：

- explore 阶段会读大量文件
- 这些信息会污染主上下文
- 到真正写代码时，模型注意力已经被大量探索细节稀释

Subagent 把探索与修改隔离开，本质上是在做**上下文分区与摘要回流**。

### 8. 配置会过时，Harness 也要做技术债治理

Anthropic 特别提醒：

- 为旧模型写的提示词，可能会束缚新模型
- 为临时问题加的 hook / skill / 规则，可能会逐渐变成噪音
- 模型升级后，要定期 review harness

推荐节奏是：

- 每 3~6 个月回顾一次
- 或每次大版本模型升级后回顾一次

需要重点问：

- 哪些规则仍然必要？
- 哪些是历史补丁？
- 哪些 hook 可以删？
- 哪些 skill 应合并或重写？

这和清理技术债、删除过时注释本质上是同一件事：**Harness 不是配置完就结束，而是持续演化的系统资产。**

### 9. 组织层面需要 DRI / agent manager，而不是靠自发热情

文章最后上升到组织治理层，指出 Claude Code 在团队中推广得好的公司，通常都有明确负责人：

- 维护 plugin marketplace
- 管理 CLAUDE.md 规范
- 统一 settings 决策
- 推进安全、审计、合规等基础设施

这部分很像平台工程（Platform Engineering）的思路：

- 不是人人都自己造一套 agent infra
- 而是先有一层可复用的公共基础设施
- 再让业务团队在上面迭代

对于国内团队，还需要额外考虑：

- 数据出境
- 审查留痕
- 敏感行业合规边界

## 可直接落地的方法论

结合文章内容，可以把“大代码库里的 Claude Code 最佳实践”浓缩成下面这套可执行顺序：

### 第一步：先做上下文分层

- 根目录放总览型 CLAUDE.md
- 核心子目录分别放局部 CLAUDE.md
- 每个子目录写清 lint / test / build 的最小命令
- 配好 `.ignore` 和 deny 规则，先降噪

### 第二步：再补硬约束

优先上 Hooks，而不是继续堆 prompt：

- 危险命令拦截
- 提交前 typecheck / lint
- 结束会话自动复盘
- 按目录动态注入配置

### 第三步：把高频操作技能化

把重复工作沉淀成 Skills：

- code review
- debug playbook
- feature workflow
- test / build / release 规范

并且按路径 scope 激活，避免全局污染。

### 第四步：引入 LSP 和结构化工具

如果仓库语言支持良好：

- 优先让 Claude 走 symbol 级导航
- 必要时用 MCP 暴露结构化查询能力

### 第五步：用 Subagent 做上下文隔离

尤其适合：

- 复杂模块探索
- 多方案调研
- 大规模影响面扫描
- Explore / Edit 拆分

### 第六步：把配置当系统资产，而不是个人偏方

- 用 Plugin 打包分发
- 设定 DRI 负责维护
- 模型升级后定期瘦身和回顾

## 对我的启发

这篇文章最有价值的地方，不是它又列了一次“Claude Code 有哪些扩展点”，而是它明确指出：

> 在大代码库里，问题从来不是“模型够不够聪明”，而是“环境有没有把模型引导到正确位置”。

真正高质量的 AI Coding 系统，不靠单个神 prompt，也不靠一次性堆满配置，而是靠一整套不断演进的 harness：

- 用 CLAUDE.md 管上下文入口
- 用 Hook 管硬约束
- 用 Skill 管经验复用
- 用 Plugin 管团队扩散
- 用 LSP / MCP 管搜索质量
- 用 Subagent 管上下文污染

这也是为什么说，**AI Coding 的工程差异化正从“谁模型更强”逐渐转向“谁的 Harness 更成熟”。**

## 适合放进知识库的关联主题

- Claude Code
- Harness Engineering
- Agentic Search
- 大代码库 AI Coding 方法论
- CLAUDE.md 分层设计
- Hooks / Skills / Plugins / MCP / Subagent 协同
- LSP 与符号级搜索

## 标签

#主题/AI-Coding #主题/Claude-Code #主题/Harness-Engineering #手法/知识编译 #来源/微信公众号
