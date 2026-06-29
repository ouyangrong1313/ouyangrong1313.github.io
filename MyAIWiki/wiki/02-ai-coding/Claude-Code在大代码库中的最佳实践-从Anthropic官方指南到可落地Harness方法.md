# Claude Code 在大代码库中的最佳实践：从 Anthropic 官方指南到可落地 Harness 方法

## 核心结论

在大型代码库里，Claude Code 的关键不是“有没有更强模型”，而是**有没有一套成熟的 Harness 来帮助模型定位、约束、扩展与隔离上下文**。

Anthropic 官方总结出的七件套：

- CLAUDE.md
- Hooks
- Skills
- Plugins
- LSP
- MCP servers
- Subagents

本质上都在解决同一个问题：**如何让 agent 在实时、低噪音、可治理的大仓库环境中稳定发挥。**

## 一、为什么大代码库更依赖 agentic search，而不是 RAG

Claude Code 在大代码库里主要依赖 **agentic search**：

- 实时遍历目录
- grep 关键字
- 读取文件
- 跟踪引用关系

而不是先对整个代码库做 embedding 再检索。

原因很现实：

- 大仓库变化太快
- embedding 索引容易滞后
- 检索结果可能指向旧函数、旧路径、已删除模块

所以在活跃仓库里，**实时搜索虽然更重，但更可信**。

### 对实践的启发

大代码库里，优化重点不是“怎么让 agent 一次读更多代码”，而是：

1. 让目录结构更容易理解
2. 让搜索命中更精准
3. 让无关输出尽量少
4. 让上下文预算花在关键位置上

## 二、Harness 比模型更决定实际效果

Anthropic 把影响 Claude Code 实战效果的关键要素总结为七件套，这说明：

- 模型决定理论上限
- Harness 决定现实中能发挥多少

可以把它理解成：

- 模型 = 推理引擎
- Harness = 操作系统 + 权限层 + 工具层 + 工作流层

在小项目里，模型本身往往已经够用；但到了大代码库，真正拉开差距的是：

- 上下文是否分层
- 规则是否外置
- 搜索是否结构化
- 经验是否可复用
- 任务是否能隔离污染

## 三、CLAUDE.md：大代码库中的第一杠杆

Claude Code 会从当前目录向上逐层读取 CLAUDE.md，因此最有效的做法不是只在根目录放一个超长文件，而是做**分层上下文设计**。

### 推荐做法

#### 1. 根目录 CLAUDE.md 只放总览

根目录适合放：

- 仓库整体结构说明
- 通用工程约束
- 指向更细分文档的入口
- 少量关键注意事项

不要把所有模块细节都堆进去。

#### 2. 子目录继续放局部 CLAUDE.md

例如：

- `frontend/CLAUDE.md`
- `services/payment/CLAUDE.md`
- `mobile/ios/CLAUDE.md`

每层只写当前目录真正需要的：

- 该模块负责什么
- 改动时优先看哪些文件
- 测试命令是什么
- lint / build 命令是什么
- 有哪些局部禁区或约定

#### 3. 从任务相关目录启动 Claude Code

这样它自动加载的上下文会更聚焦，避免一上来就带入整个 monorepo 的噪音。

### 相关配套

Anthropic 还建议同时做三件事：

- 用 `.ignore` 排除生成代码、构建产物、第三方依赖
- 用 `.claude/settings.json` 写 deny 规则，形成项目级硬约束
- 如果目录混乱，至少补一个 codebase map 给 Claude 当索引

## 四、Hooks：把“必须发生”的动作从 Prompt 外置出去

Hooks 是 Claude Code 中很强但容易被低估的扩展点。

它可以绑定到：

- Start
- Stop
- PreToolUse
- PostToolUse

### 典型价值

#### 1. 自我进化

- 会话结束时复盘
- 提炼经验
- 回写 CLAUDE.md / Skill / 注意事项

这相当于把“越用越懂项目”部分自动化。

#### 2. 动态上下文注入

根据：

- 当前目录
- 当前用户
- 当前模块

动态加载不同约定，而不是让所有人手动切换配置。

#### 3. 强制规则执行

凡是必须发生的动作，优先放在 Hook 层：

- lint
- typecheck
- 危险命令拦截
- 提交前校验

### 一个重要判断

> Prompt 是建议，Hook 是约束。

能在 Hook 层做的，就不要只寄希望于模型“自觉”。

## 五、Skills 和 Plugins：一个解决复用，一个解决扩散

### Skills：按需加载的专业能力

Skills 适合承载：

- 调试 SOP
- 代码评审模板
- 功能开发工作流
- 某语言 / 某框架的特定约定

它的核心思想是：

- 常驻上下文只保留能力描述
- 详细操作细节在真正需要时再加载

这样才不会让上下文永远处于过载状态。

Anthropic 这次特别强调了一个进阶实践：

- **按路径 scope 激活 Skill**

也就是：

- 前端 Skill 只在前端目录生效
- 后端 Skill 只在后端目录生效
- iOS / Android / Infra 各自隔离

这能显著减少技能互相干扰。

### Plugins：把个人配置升级为团队能力

大团队常见的问题不是没人会配，而是：

- 只有少数老员工配置完善
- 新人根本不知道有哪些能力可用
- 配置分散在个人环境，无法共享

Plugin 的价值就是把：

- Skills
- Hooks
- MCP servers
- Settings

打包分发，让团队一键获得同一套增强能力。

从组织角度看，Plugin 解决的是 **tribal knowledge 无法扩散** 的问题。

## 六、LSP：让搜索从字符串匹配升级为符号导航

在大代码库里，grep 最大的问题不是慢，而是**结果太多且缺乏语义**。

搜一个 `getUser`，很可能出现：

- 定义
- 重载
- 注释
- mock
- 测试桩
- 无关同名实现

Claude 为了确认真正目标，只能打开大量文件，上下文预算很快被烧掉。

LSP（Language Server Protocol）提供的是更高质量的能力：

- 跳转定义
- 查找引用
- 查找实现
- 理解 class / interface / method 的语义关系

这相当于把搜索从：

- 文本匹配

升级成：

- 符号级导航

在 Go、TypeScript、Java、Python、Rust 等语言里，LSP 往往是让 Claude Code 在大代码库真正“顺手”的关键基础设施。

## 七、MCP 与 Subagent：一个扩边界，一个控污染

### MCP：把 Claude 接到它本来够不到的系统

MCP server 很适合暴露这些能力：

- 内部 API
- 文档系统
- 检索服务
- 仓库结构化分析工具

文章提到一个特别值得落地的方向：

- 针对代码库做专用 MCP

例如提供：

- 查找所有实现某接口的类
- 查找所有调用某 deprecated API 的位置
- 扫描某模块的依赖边界

这些查询用 grep 不稳定，用专用 MCP 会更干净。

### Subagent：把探索和修改分开

Subagent 最有价值的场景之一是：

- Explore / Edit 拆分

做法是：

1. 让只读 subagent 负责摸目录、读文件、画结构图
2. 输出一份精炼总结
3. 主 agent 基于总结进入修改阶段

### 为什么这很重要

因为探索阶段通常会：

- 读大量文件
- 带来海量细节
- 污染主上下文

等真要写代码时，模型注意力已经被很多无关信息稀释掉了。

Subagent 本质上是在做：

- 上下文隔离
- 信息压缩
- 注意力保护

## 八、Harness 要跟着模型升级一起“瘦身”

这是最容易被忽视、但特别重要的一点。

很多历史配置最初是为了解决旧模型的问题：

- 容易跳步
- 容易漏测
- 容易乱改
- 容易输出啰嗦计划

但模型升级后，这些补丁可能会反过来拖慢效率。

所以 Anthropic 建议：

- 每 3~6 个月 review 一次 Harness
- 或每次模型大版本升级后 review 一次

重点清理：

- 已过时的提示
- 临时修补的 Hook
- 重复或冲突的 Skill
- 不再需要的流程限制

这和代码里的技术债治理是同一类问题：

> Harness 也会腐烂，也需要重构。

## 九、组织层面：需要 DRI，而不是“大家自发摸索”

Claude Code 在团队里推广得顺，通常都有明确责任人来维护：

- Plugin
- CLAUDE.md 模板
- Settings 规范
- MCP 接入策略
- 安全 / 合规 / 留痕方案

文章提到的角色包括：

- agent manager
- DRI（Directly Responsible Individual）

本质上是在做一层“Agent 平台工程”。

如果没有这层治理，常见后果就是：

- 人人都在配
- 配法彼此冲突
- 经验停留在个人电脑
- 新人很难继承成熟打法

对于国内团队，还要额外考虑：

- 数据出境
- 审计留痕
- 敏感行业合规

## 十、可落地的实践顺序

如果要把这篇文章转成执行清单，我会推荐这个顺序：

### 1. 先做上下文分层

- 根目录 CLAUDE.md 写总览
- 核心子目录补局部 CLAUDE.md
- 每个子目录写清最小 test / lint / build 命令
- 配 `.ignore` 和 deny 规则降噪

### 2. 再做硬约束

优先上 Hook：

- 危险命令拦截
- 自动 lint / typecheck
- 会话结束复盘
- 按路径加载上下文

### 3. 把高频流程沉淀成 Skill

例如：

- code review
- debug playbook
- feature workflow
- 提交规范

并按路径激活。

### 4. 引入 LSP 和结构化搜索

能走符号级导航，就尽量不要只靠 grep。

### 5. 用 Subagent 隔离探索与修改

适合复杂代码、重构前摸底、影响面分析。

### 6. 用 Plugin 和 DRI 做团队扩散

把个人偏方升级成团队基础设施。

## 我的理解

这篇文章真正重要的不是“又多了几个 Claude Code 配置点”，而是它给出了一条更清晰的判断线：

> 在大代码库里，AI Coding 的主要矛盾，已经从“模型够不够强”逐渐转向“Harness 是否足够成熟”。

真正决定体验的，是你能不能把模型放进一个：

- 目录清晰
- 上下文分层
- 规则外置
- 搜索结构化
- 能力可复用
- 污染可隔离
- 团队可扩散

的工作环境里。

## 关联阅读

- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- [[OpenClaw的正确打开方式]]
- [[从软件工程基本功到Agent落地：结合OpenClaw与Claude Code的实践理解]]
- [[用Agent评测思路管理AI-Coding-31万行代码重构实践]]
- [[谷歌开源agent-skills]]

## 标签

#主题/AI-Coding #主题/Claude-Code #主题/Harness-Engineering #主题/Agentic-Search #来源/微信公众号
