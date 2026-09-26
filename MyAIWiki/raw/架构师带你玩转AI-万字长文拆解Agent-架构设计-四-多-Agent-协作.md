# 万字长文拆解Agent 架构设计（四）：多 Agent 协作

**来源：** 微信公众号「架构师带你玩转AI」
**作者：** AllenTang
**日期：** 2026-07-22 23:17
**链接：** https://mp.weixin.qq.com/s/CFTp_TVA8DQLFuvirkrFvQ
**获取时间：** 2026-07-27 Asia/Shanghai
**地区：** 湖北

---

## 正文

本系列目标：拆解 Claude Code 源码，理解 Agent 底层架构的设计思路。核心方法：读源码 -> 理解设计决策 -> 用 TypeScript 手写核心逻辑。

每一篇聚焦一个子系统，讲清楚"为什么这么设计"比"代码怎么写"更重要。

引言

前三篇拆完了单个 Agent：记忆、工具、循环。模型能用到的全部信息——系统设定、工具列表、对话历史——每一轮都组装进一个上下文窗口，所有的判断都发生在里面。

任务超出一个上下文能装的范围时，直觉的答案是多派几个 Agent 分工。但问题随之而来：子 Agent 背后是同一个模型，它甚至不知道主 Agent 之前聊过什么——多派一个，凭什么让系统变强？

Claude Code 对这个问题的回答就是本篇的主题：多 Agent 协作切分的不是能力，而是上下文。

Part 1：拆解 Claude Code 源码

1.1 角色划分：编排者 / 子 Agent

Claude Code 里有一个隐式但很重要的角色划分：

```ts
// 两种角色的接口差异（简化自源码）
interface OrchestratorConfig {
 // 编排者：做规划、分解、汇总，尽量不直接执行会改动环境的工具
 allowedTools: ['task', 'read_file', 'list_dir']; // 只读 + 派发
 maxSubagents: number; // 最多同时存活多少子 Agent
 subagentBudget: TokenBudget; // 每个子 Agent 分到多少 token
}

interface SubagentConfig {
 // 执行者：做具体操作，不再派出子 Agent（默认）
 allowedTools: ['bash', 'write_file', 'read_file']; // 会改动环境的工具（执行命令、写文件）
 canSpawnSubagents: boolean; // 默认 false，防止无限递归
 inheritedContext: string; // 从父 Agent 继承的任务背景
}
```

关键设计：编排者和执行者的工具集互补，不重叠。编排者有 task 工具（派出子 Agent），但通常没有副作用工具——即会改动外部环境的工具，如 write_file、bash；执行者有这些工具，但默认没有 task 工具（不能再派子 Agent）。

这个划分防住了两个问题：一是编排者绕过规划直接乱改文件；二是执行者未经授权自行派出新 Agent，让调度树无限膨胀。

但角色划分只是表层结构，没有回答引言里的问题：同一个模型，换个角色就更强了吗？答案不在分工，在上下文隔离——下一节展开。

1.2 派发就是一次工具调用：Task 工具

Claude Code 里派子 Agent 的入口是 task 工具。形态上和普通工具一样（都是第二篇的 AgentTool），但语义特殊：输入是一段任务描述，输出是子 Agent 的最后一条消息。

```ts
// Task 工具（简化自源码）
const TaskTool: AgentTool = {
 name: 'task',
 description: '派发一个子 Agent 执行独立任务。适合需要大量阅读材料、但结论简短的广泛调研。',
 parameters: {
 subagent_type: { type: 'string' }, // 子 Agent 类型，决定角色设定和工具集
 prompt: { type: 'string' }, // 任务描述：唯一的输入
 },
 async execute(toolCallId, { subagent_type, prompt }, signal) {
 const def = loadAgentDefinition(subagent_type);
 // 1. 子 Agent 在全新的上下文中启动，看不到父 Agent 的对话历史
 // 2. 运行一个独立的 Agent Loop（第三篇那个循环）
 // 3. 返回值 = 子 Agent 的最后一条消息
 const finalMessage = await runSubagent(def, prompt, signal);
 return { content: finalMessage };
 },
};
```

子 Agent 的"角色设定"是一个 markdown 文件，放在 .claude/agents/ 目录下：

```md
<!-- .claude/agents/code-reviewer.md -->
---
name: code-reviewer
description: 审查代码改动，找 bug、安全问题和风格问题
tools: [read_file, bash, grep]
---
你是一个严格的代码审查员。读入改动，逐条审查。
只报你有把握的问题，每个问题附上具体文件和行号。
```

定义里的三个字段，读者各不相同：description 给主 Agent 的模型看，它靠这个决定"这事派给谁"；tools 给权限系统看，是子 Agent 的工具白名单；正文给子 Agent 自己看，是它的 system prompt。description 写得含糊就会派错活——它本质上也是一份接口。

1.3 上下文隔离：新桌子，只交结论

子 Agent 启动时拿到的上下文是全新的：独立的 system prompt、独立的工具定义，对话历史从一条消息开始——就是父 Agent 写的任务描述。父 Agent 之前聊过什么、用户的原始意图是什么，它一概看不到。

任务完成后，进入父 Agent 上下文的只有子 Agent 的最后一条消息。子 Agent 跑了多少轮、调了什么工具、走了什么弯路，父 Agent 一概不知道。

```text
主 Agent 的上下文：用户请求 + 各子 Agent 交回的一页页结论
 ├── 子 Agent 1 的上下文（全新）：文件 1–10 -> 一条结论消息
 ├── 子 Agent 2 的上下文（全新）：文件 11–20 -> 一条结论消息
 └── 子 Agent 3 的上下文（全新）：文件 21–30 -> 一条结论消息
```

为什么要这样？把上下文窗口想象成 Agent 的桌子：任务越大，摊在桌上的资料越多。这张桌子有两个硬约束：一是容量有限，堆满后早期信息就被挤出去；二是更隐蔽的一条——资料越多，模型越难聚焦，注意力被每一份资料稀释（长上下文里中部的信息最容易被漏掉，即 "lost in the middle"）。子 Agent 做的，就是把一摞资料挪到自己桌上看完，最后只交回一页结论。父 Agent 的桌上多了一页纸，少了一万页资料。

这就是引言那个问题的答案：多 Agent 协作的本质不是能力分工，而是上下文切分。子 Agent 不比主 Agent 多懂什么，它强的地方只是"桌子干净"。

Part 2：手写核心逻辑（TypeScript）

延续系列的项目结构，这一篇新增四个文件。四个文件里，值得看的只有 spawn.ts。

2.1 项目结构

```text
multi-agent/
├── src/
│ ├── types.ts
│ ├── agent-def.ts
│ ├── spawn.ts
│ └── task-tool.ts
├── package.json
└── tsconfig.json
```

- `types.ts`：子 Agent 定义与返回结构
- `agent-def.ts`：markdown + frontmatter 定义解析
- `spawn.ts`：派发核心：上下文隔离 + 权限交集 + 只交回最后一条消息
- `task-tool.ts`：Task 工具：子 Agent 即普通工具

2.2 派发核心：spawn.ts

多 Agent 派发的全部逻辑就是一个函数，里面三处注释正好对应 1.2-1.5 的三个设计：

```ts
async function spawnSubagent(
 parent: AgentContext,
 def: AgentDefinition, // 子 Agent 定义：systemPrompt + 工具白名单（markdown 定义的 frontmatter，见 1.2）
 taskPrompt: string, // 父 Agent 写的任务描述：背景全在这里面
 signal: AbortSignal,
): Promise {
 // 1. 权限交集：定义声明 ∩ 父 Agent 拥有，并默认去掉 task 工具（规则二）
 const allowedTools = deriveSubagentPermissions([...parent.tools.keys()], def.tools);
 const subagentTools = new Map(allowedTools.map(name => [name, parent.tools.get(name)!]));

 // 2. 全新上下文：这里没有”把父 Agent 历史传给子 Agent”的代码——没有就是设计
 // 子 Agent 需要知道的一切，都应该写在 taskPrompt 里
 const loop = new AgentLoop(
 new ContextAssembler(def.systemPrompt, subagentTools, new MemoryStore(), new HistoryCompactor()),
 new PermissionManager(subagentTools),
 parent.llm,
 allocateSubagentBudget(parent.budget), // 规则一：预算只减不增
 );

 // 3. 返回值 = 最后一条消息；中间过程留在子 Agent 自己的上下文里
 try {
 const finalMessage = await loop.run(taskPrompt, crypto.randomUUID(), signal);
 return { status: 'success', output: finalMessage };
 } catch (e) {
  return { status: 'failed', output: `子 Agent 执行失败：${String(e).slice(0, 200)}` };
 }
}
```

这里的 AgentLoop 就是第三篇那个循环：system prompt、工具定义、对话历史全是全新的，只有 taskPrompt 作为第一条用户消息传进去。子 Agent 跑的是一个普通得不能再普通的 Agent Loop，没有任何特殊执行路径——这正是"多 Agent 层"几乎不产生新逻辑的原因，它只是把已有部件组合起来。

2.3 Task 工具：一个薄封装

task-tool.ts 更简单：把 spawnSubagent 注册成一个普通工具（第二篇的 AgentTool 接口），参数 prompt 进去，最后一条消息作为工具结果出来。唯一有心思的地方在工具的 description：

```ts
description:
 '派发一个子 Agent 执行独立任务。适合需要大量阅读材料、但结论简短的任务。' +
 `可用类型：${[...defs.values()].map(d => `${d.name}（${d.description}）`).join('；')}`,
```

把所有候选子 Agent 类型和它们的描述列出来——主 Agent 的模型靠读这段话决定派谁。prompt 就是 API 契约，从这里就开始了。

并行的部分一行新代码都没有：模型在一轮里发出多个 task 调用，第三篇的循环本来就并发执行。哪些并行、哪些串行，是模型的判断——我们没有写调度器，模型就是调度器。

---

标签： #主题/AI-Agent #主题/Claude-Code #主题/多-Agent #主题/Context-Engineering #主题/Agent-Architecture #主题/Sub-Agent #场景/公众号长文 #来源/架构师带你玩转AI
