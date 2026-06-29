# Loop Engineering - Raw Digest

- 原文链接：https://x.com/addyosmani/status/2064127981161959567?s=20
- 来源：X / Addy Osmani（@addyosmani，Chrome 团队 Lead）
- 原始推文发布时间：2026-06-09 07:30
- 互动数据：41万 查看 / 3,266 赞 / 7,605 书签 / 570 转推 / 153 回复
- 获取时间：2026-06-09
- 抓取方式：CDP Proxy（X SPA）

标签：#主题/AI-Coding
#主题/AI-Agent
#场景/技术博客
#节点/Agent-Loop
#节点/Codex
#节点/Skill
#节点/Harness
#节点/Memory

---

## 一句话总结

**Loop engineering 是把"人主动 prompt agent"替换为"系统循环调度 agent"的新范式；其本质是 5 个积木（Automations / Worktrees / Skills / Plugins+connectors / Sub-agents）+ 1 个状态文件（Memory），Claude Code 与 Codex 都已具备——但真正的难点不是工具，是设计 loop 时的工程判断力；不警惕 verification / comprehension debt / cognitive surrender 三个反噬，再好的 loop 也会变成灾难加速器。**

---

## 关键观点

### 1. 范式跃迁：从"你按 turn 提示 agent"到"你设计一个系统去调 agent"

过去两年用 coding agent 的方式是：你写一个 prompt → 看输出 → 写下一个 prompt → 重复。**agent 是工具，你全程握着它**。这件事正在（或即将）结束。**新范式是：你建一个小型系统，让系统去找工作、分派工作、验收、记下结果、决定下一步——系统替你戳 agent。**

引述两条权威：
- @steipete：「You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents.」
- @bcherny（Anthropic Claude Code 负责人）：「I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops.」

### 2. Loop = 递归目标：定义目的，AI 迭代到完成

**一个 loop = 一个递归目标：你给一个目的，AI 迭代到完成**。这是对 loop 的最简定义。**Loop engineering 就是设计这种递归系统**——而其工程量在于"哪些东西必须放进 loop 里才能让它跑得起来"。

### 3. Loop engineering 坐在 Harness 之上的一层楼

Addy 自己梳理的三层抽象：
- **Agent harness engineering**（之前写过的）= 给单个 agent 配环境
- **Factory model**（也写过）= 造软件的系统
- **Loop engineering** = harness 上面的一层楼：harness 按时间表跑，spawn 小 helper，能喂自己

**位置定位：loop 之于 harness，等于工厂之于车间。** 工具是车间，loop 是工厂。

### 4. 惊喜：loop 不再是工具事，而是产品内置能力

一年前要做 loop 得自己写一堆 bash、维护一辈子、只能自己用。**现在 5 个积木都直接 shipping 在产品里**。Steinberger 列表几乎完全对到 Codex app，又几乎完全对到 Claude Code。**形状一样 → 别再争哪个工具好，直接设计一个无论坐哪个工具里都能跑的 loop**。

### 5. 5+1 积木框架（核心骨架）

| 积木 | 干什么 | Codex 实现 | Claude Code 实现 |
|------|--------|------------|-----------------|
| **Automations** | 定时触发，发现+分诊 | Automations tab（项目/频率/worktree 选） | `/loop`、cron、hooks、GitHub Actions |
| **Worktrees** | 并行 agent 隔离 git | 内建多线程 worktree | `git worktree` + `--worktree` flag + subagent `isolation: worktree` |
| **Skills** | intent 沉淀，避免每轮重述 | `$skill` 或 `/skills`，或自动匹配描述 | 同样 `SKILL.md` 格式 |
| **Plugins + Connectors** | 让 loop 接触真实工具 | MCP connector | MCP connector（互通） |
| **Sub-agents** | maker / checker 分离 | `.codex/agents/` TOML 文件 | `.claude/agents/` + agent teams |
| **Memory（第六块）** | 跨会话状态 | markdown / Linear board | 同 |

**这是 Addy 文章的核心交付物——一张可以照搬的 loop 设计 checklist**。

### 6. `/loop` + `/goal` 是最值得知道的原语

`/loop` 按周期重跑。**`/goal` 跑到你写的条件真正成立**——每轮之后用一个独立小模型检查是否 done，**让写代码的 agent 不是给自己打分的那个**。给个条件如"test/auth 全过 + lint 干净"然后走开。**Codex 也有 `/goal`，同名同行为**——这是跨工具统一的原语。

### 7. Worktree 解机械冲突，但**人是天花板**

两个 agent 写同一文件 = 两个工程师改同一行没人对齐 → git worktree 解决"机械冲突"。**但你 review 的带宽决定你最多能跑几个 agent，不是工具**。Addy 自己说：worktrees take away the mechanical collision but **YOU are still the ceiling**。

### 8. Skill 是"写在外面的 intent"

agent 每会话冷启动，**任何 intent 上的洞都会被它自信地乱猜填上**（这是 Addy 之前文章《intent debt》的论点）。**Skill = intent 写在 agent 看得见的地方**：约定、build 步骤、"我们不这样写因为那次事故"。**没有 skill 的 loop 每轮从零重推项目；有 skill 的 loop 复利累积**。

**Skill 和 Plugin 的区别**（容易混）：
- **Skill = 创作格式**（`SKILL.md` 文件 + 可选脚本/引用/资源）
- **Plugin = 分发方式**（跨 repo 共享 + 打包一组 skill + connectors）

Codex 和 Claude Code 都是这个分法。

### 9. Sub-agent：让写代码的不是检查代码的

**最值得做的结构性动作** = 把"写的人"和"查的人"分开。写代码的模型给自己作业打分会**明显放水**——sub-agent 用不同指令、有时不同模型，**专门抓第一个 agent 把自己说服了的地方**。

Codex 让你在 `.codex/agents/` 写 TOML 定义（name/description/instructions/可选 model/reasoning effort），所以**安全审查员可以是 Opus 高强度，探索员可以是 Haiku 快速只读**。Claude Code 同款（`.claude/agents/` + agent teams）。**经典三件套：一个探索、一个实现、一个对照 spec 验证**。

**额外洞察**：`/goal` 在底层的实现就是这个分离——**一个全新的模型判断 loop 是否完成，而不是做工作的那个**。maker-checker 分离被应用到了 stop condition 本身。

### 10. 一个 loop 长什么样（Addy 自用模板）

```
每天早上 9 点在仓库跑 automation
  ↓
prompt 调起 triage skill：
  读昨日 CI failures / open issues / recent commits
  把 findings 写进 markdown 或 Linear board
  ↓
对每个值得做的 finding：
  在独立 worktree 开一个新线程
  sub-agent 写 fix
  第二个 sub-agent 对照项目 skills + 现有 tests review draft
  ↓
connector 让 loop 自动开 PR + 更新 ticket
  ↓
loop 处理不了的东西进 triage inbox 等人
  ↓
state file 是整个系统的脊椎：
  记住试过什么、什么过了、什么还开着
  → 明天的运行从今天停的地方继续
```

**关键认知：你只设计一次。其余步骤你一个都没 prompt。** 这就是 Steinberger 整篇文章的"实"。

### 11. 三个 loop 没替你解决的问题（更尖锐）

Loop 把工作变了，**没有把你从工作里删掉**。loop 越强，下面三件事**不是更简单，是更尖锐**：

1. **Verification 还是你的**。无人值守的 loop = 无人值守地犯错。**你分出 verifier sub-agent 的全部意义就是让 loop 的"完成了"变得可信——而"完成"仍是声明不是证明**。Addy 反复重复一句：your job is to ship code you confirmed works。
2. **理解会腐烂**。loop 越快产你没写的代码，"存在"和"你懂"之间的 gap 越大。**Comprehension debt**——一个顺滑的 loop 让它长得更快，除非你读 loop 造的东西。
3. **认知投降是最舒服的姿势**。loop 自跑时最诱惑的就是停止有意见、拿走什么是什么。Addy 叫这个 **cognitive surrender**。**设计 loop 是药（有判断地设计）也是毒（为不思考而设计）——同一个动作，反面结果。**

### 12. 结尾金句

> Build the loop. Stay the engineer.

> Loops can also result in different outcomes depending on you. **Two people can build the exact same loop and get completely opposite results.** One uses it to move faster on work they understand deeply. The other uses it to avoid understanding the work at all. The loop doesn't know the difference. You do.

> That's what makes **loop design harder than prompt engineering**, not easier. Cherny's point isn't that the work got easier. **It's that the leverage point moved.**

---

## 跨产品对照表（Addy 整篇最有价值的一张图）

| 维度 | Codex | Claude Code | 异同 |
|------|-------|-------------|------|
| 触发定时 | Automations tab | `/loop` / cron / hooks / GitHub Actions | **同能力，不同入口** |
| 硬性完成条件 | `/goal`（同名同行为） | `/goal`（同名同行为） | **完全一致** |
| Worktree | 内建 | `--worktree` flag + subagent `isolation: worktree` | Claude Code 给你更多旋钮 |
| Skill 格式 | `SKILL.md` 文件夹 | `SKILL.md` 文件夹 | **完全一致** |
| Connector | MCP | MCP | **互通，写一个两边都能用** |
| Sub-agent | `.codex/agents/` TOML | `.claude/agents/` + agent teams | 名字不同，模式相同 |

**关键洞察**：形状一样 → 别再争工具，**直接设计在两边都能跑的 loop**。

---

## 7 角度 × 3 钩子（写作复用）

### 角度 1：范式跃迁（人 → 系统）
- 钩子 1：你不再按 turn 提示 agent，你设计一个系统去戳它
- 钩子 2：从"握着工具"到"养管道"——同一个动作的两种描述
- 钩子 3：Loop = 递归目标：你给目的，AI 迭代到完成

### 角度 2：跨产品一致性（Codex ≈ Claude Code）
- 钩子 1：Steinberger 的列表对到 Codex，又对到 Claude Code——形状一样
- 钩子 2：别再争工具好；设计一个在两边都能跑的 loop
- 钩子 3：MCP connector 写一个两边用，sub-agent TOML 模式相同

### 角度 3：5+1 积木框架
- 钩子 1：Automations 是心跳，Worktrees 是隔离，Skills 是 intent，Connectors 是手脚，Sub-agents 是制衡
- 钩子 2：第 6 块 Memory = agent 忘，repo 不忘
- 钩子 3：一套可以照搬的 loop 设计 checklist

### 角度 4：核心原语 /loop + /goal
- 钩子 1：`/goal` 让写代码的 agent 不是给自己打分的那个
- 钩子 2：Codex 和 Claude Code 同名同行为的 `/goal`——跨工具统一原语
- 钩子 3：每轮之后用独立小模型验是否 done，是 maker-checker 分离的终级形态

### 角度 5：警示三件套（Verification / Comprehension / Surrender）
- 钩子 1：loop 越强，下面三件事不是更简单是更尖锐
- 钩子 2：comprehension debt——loop 顺滑 = 理解腐烂速度更快
- 钩子 3：cognitive surrender——为不思考而设计的 loop 是毒药

### 角度 6：工程师角色（Stay the engineer）
- 钩子 1：Build the loop. Stay the engineer.
- 钩子 2：杠杆点移动了，不是工作变简单了
- 钩子 3：两个人造同一个 loop，结果完全可能相反——loop 不知道差异，你知道

### 角度 7：可借鉴动作（今天就能试）
- 钩子 1：把"每天重复没人解决"的事挑一件，用 `/loop` + `/goal` 跑起来
- 钩子 2：写一份 SKILL.md 把项目约定沉淀，比每次 prompt 解释省 10 倍
- 钩子 3：给团队装一台"自动 review 第二人" sub-agent，从对抗性 code review 开始
