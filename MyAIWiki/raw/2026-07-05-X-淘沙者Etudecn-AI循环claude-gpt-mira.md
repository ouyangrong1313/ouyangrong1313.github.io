---
title: AI循环：Claude、GPT和Mira，到底什么才是真正好用的
author: 淘沙者(TheSandPicker)
handle: @Etudecn
platform: X (Twitter)
url: https://x.com/Etudecn/status/2073072648922481000
focus_url: https://x.com/Etudecn/article/2073072648922481000
publish_time: 2026-07-03T15:53:29.000Z
publish_time_cn: 2026年7月3日 23:53
fetch_time: 2026-07-05
engagement: {reply: 58, retweet: 167, view: 270000}
media:
  - https://pbs.twimg.com/media/HMUIfOJaMAAGmMU?format=jpg&name=large
  - https://pbs.twimg.com/media/HMUIeusbsAAq6R8?format=jpg&name=large
length_chars: 8798
type: X长文章 + 配图
status: inbox
tags: [#主题/AI-Agent, #主题/AI-Coding, #节点/Agent-Loop, #节点/Mira, #节点/Harness, #节点/Skill]
---

# AI循环：Claude、GPT和Mira，到底什么才是真正好用的

> 淘沙者(TheSandPicker) @Etudecn · 2026-07-03 · 58 回复 / 167 转发 / 27万 浏览

## 开场

AI 已经普及好几年了，大多数人每天都在用，但用的方式却是最慢的那种：打个字、等回答、不满意再改、再问，全程自己动手。不是因为有更快的方法太复杂，而是没人告诉他们快的方法长什么样。

更快的方法叫"循环"（Loop），也是目前全世界顶尖 AI 工程师最在意的东西。这篇文章就是来补上没人讲清楚的那一环。看完之后，你会比时间线上99%的人更懂循环：它是什么，底层怎么运作，什么时候值得用、什么时候是陷阱，怎么在 Claude 或 ChatGPT 里手搓一个基础版本，还有哪些简单到能在日常生活里跑起来的循环。

## 一、提示词 vs 循环

先仔细想想"一次只问一个问题"这个习惯，因为整个问题就在这里。每一步都要经过你：你决定问什么，你判断答案好不好，你决定下一步做什么。AI 不会自己动，你推一下它才动一下，你一停，它就停。这样用没问题，但它有天花板。你是发动机，AI 只是你手里的工具，工具自己不会做事。

还有另一种工作方式，也是顶尖工程师们正在改变做法的原因。你不用一步步带着 AI 走，而是只给它一个目标，然后让它自己跑。它自己规划、自己干活、自己检查结果、自己修补弱点，反复循环，直到达成目标。你退出来，活儿还在继续。

## 二、循环的五步骨架

提示词是单条指令，循环是 AI 持续努力去达成的目标。 你可以把它理解成一个"递归目标"：你定义一个目的，AI 反复迭代，直到完成。

```
DISCOVER  →  work out what needs doing
PLAN      →  decide how to do it
EXECUTE   →  do the work
VERIFY    →  check it against the goal
ITERATE   →  not there yet? feed the result back in and repeat
```

这五步里有三步才是真正干活的：验证、状态、停止条件。

**验证（Verify）是循环的心脏。** 如果没有对结果的真正检查，你就不是在做循环，你是在让 AI 自己跟自己互相点头。检查才是把"重复"变成"进步"的东西。它可以是硬性测试（"代码能不能通过"），可以是可衡量的条件（"数字有没有超过 X"），也可以是一套让模型打分的评分标准。没有这道关卡，就是让 AI 给自己改作业。

**状态（State）让循环能学到东西。** 每一轮，AI 都得记住自己已经试过什么，不然就会永远犯同样的错。一个真正的循环会在旁边记一小本账：什么做完了，什么失败了，下一步是什么。

**停止条件让循环保持理性。** 没有出口的循环会一直跑，要么成功，要么崩溃，要么掏空你的账户。每个正经的循环都有两种停止方式：成功，和硬性上限（"试了8次就停，然后报告"）。

## 三、什么时候值得搭循环

只有四个条件全部满足，才值得搭循环：

1. 任务是重复性的，至少每周一次。频率更低的话，搭建成本永远收不回来。
2. 有东西能自动拒绝差的输出（测试、类型检查、构建、硬规则）。
3. AI 能自己从头到尾把活干完，而不是干一半丢回给你。
4. "完成"是客观的，不是凭感觉。

少一条，就老老实实用手动提示词。

## 四、编程循环示例

```
▸ LOOP SPEC
GOAL: every test in /tests/auth passes, lint is clean, no type errors.

EACH ITERATION:
  1. run the test suite and read every failure
  2. pick the single highest-impact failure
  3. write the smallest change that fixes it
  4. re-run the tests, lint, and type checker

VERIFY: green tests + zero lint warnings + zero type errors
STOP WHEN: verify passes, OR 8 iterations reached
ON STOP: summarize what changed and what still fails
```

## 五、循环的五个积木

Claude Code 和 Codex 现在已经把这五个全内置了：

1. **自动化（心跳）** — /loop、/goal、hooks、cron、GitHub Actions，结果会主动来找你。
2. **技能（可复用的指令）** — 把规则存成文件，循环每次读取它。
3. **子代理（让干活的人和检查的人分开）** — 写手又快又便宜，审稿人又慢又严格。
4. **连接器（让它动手，而不是建议）** — "自己打开合并请求、关联工单"与"给你修复方案"的区别。
5. **验证器（关卡）** — 唯一决定循环到底是在帮你还是只是在花钱的积木。

有个工程师用这样的循环，大约六天就把整个代码库从一种编程语言翻译成另一种，手动做大概要将近一年。

## 六、循环的代价：Token 经济学

循环跑的是 token，token 就是钱。

```
▸ ROUGH COST OF ONE LOOP
single agent, one medium task: ~50,000 – 200,000 tokens
context re-sent every iteration: grows each pass
a fleet of agents in parallel: multiply all of the above
```

真正重要、但几乎没人追踪的指标，是"每个被采纳的修改花多少钱"。**采纳率低于50%，它就在亏钱。**

循环还会安静地失败。工程师 Geoffrey Huntley 管这叫 **"Ralph Wiggum 循环"**：AI 太早觉得自己做完了，在一个半成品上退出，循环却还在跑、还在花钱，什么也不产出。

## 七、搭建顺序比工具更重要

```
1. Get ONE manual run reliable first.
2. Turn that into a skill (save the instructions).
3. Wrap the skill in a loop (add the gate + stop condition).
4. THEN put it on a schedule.
```

跳过前面，直接给一个你还没手动跑可靠的东西排上日程，就是循环在你睡觉时炸掉的原因。

## 八、轻量版：手搓循环提示词

在任何大语言模型里，你只用一段提示词就能手动跑一个简单循环：

```
▸ SELF-CHECKING LOOP  (paste into Claude or ChatGPT)
You will work in a loop until the task meets the bar.

TASK:
[describe exactly what you want produced]

SUCCESS CRITERIA (be strict, no soft passes):
- [criterion 1]
- [criterion 2]
- [criterion 3]

LOOP PROTOCOL, repeat every turn:
1. PLAN - state the single next step.
2. DO - produce or improve the work.
3. VERIFY - score the result 1-10 on each criterion.
            Be brutally honest. List exactly what is still weak.
4. DECIDE - if every criterion is 8+, print "FINAL" and stop.
            Otherwise print "ITERATING" and go again, fixing
            the weakest point first.

RULES:
- Never call it done until every criterion is 8 or higher.
- Each pass must fix the weakest score from the last VERIFY.
- Do not ask me questions. Make a sensible assumption, note it,
  and keep going.

Begin. Run the loop until FINAL.
```

但注意还缺了什么：**你是触发器**。关掉标签页，它就没了。要得到一个能自己跑、按计划、被真实事件触发、不需要你盯着看的循环，你通常得走进重型世界。

## 九、Mira：把循环做到 Telegram 里

> ⚠️ 本节属 Mira 软广 / advertorial，需谨慎看待

剥掉代码和成本，剩下的就是一个简单但真正有用的概念：一个能自己跑的任务，按计划或者在某件事发生的那一刻启动，不需要你记着它、也不需要你在场。

**Mira** 住在 Telegram 里，循环叫"技能"（Skill）。每个 Skill 内置了真正循环需要的东西：触发器、动作、自己运行的方式——只是你永远不用自己接线。

```
▸ SKILL
"Every weekday at 7am, check my Gmail and Google Calendar.
Send me a short brief: my 3 most important meetings, anything
urgent in the inbox, and one thing I said I'd follow up on but
haven't. Keep it under 120 words."
```

ChatGPT 回答，Mira 行动。Mira 通过 **Composio** 连接500多个 App（Notion、Gmail、Google 日历、GitHub、Figma、Stripe 等），有跨会话和群聊的长期记忆，不绑定单一模型（GPT / Claude / Gemini 按任务切换）。

### 场景示例

**工作场景**：
- "An hour before each meeting, remind me with the context and decisions from our last conversation with that person."
- "When I forward a message here, turn it into a Linear ticket with the right priority and assign the owner."
- "Every Friday at 4pm, collect the team's task status and metrics and post a clean weekly digest in our chat."

**创作者场景**：
- "I'll send a voice note with a raw idea. Turn it into a finished post with a caption and hashtags."
- "Take this one idea and write versions for X, Instagram, LinkedIn, Email, and a newsletter."
- "Generate 3 image options for this post."

**语音场景**：
- "Transcribe my voice messages into clean text."
- "Read this article back to me as audio."

**生活场景**：
- "Every evening at 7, ask if I trained today. Keep a streak."
- "Every night, ask me 3 questions about my day, remember the answers."
- "Watch this flight route and buy when the price drops to my number."

## 十、收尾

循环不是一阵风。它是"谁来做这件事"的转移。AI 不再等你推着它走每一步，而是开始自己把整件事跑完。话虽如此，这不是什么要追的东西，也不是什么要硬塞到不合适地方去的东西。更多时候，你只是在白花钱。

**我的建议**：先用现成的、免费的东西，等你真的觉得不够了，再去想自己到底需要什么。

---

## 原始 metadata

- 抓取方式：Playwright + DOM eval（X 反爬，无法走 WebFetch/Jina）
- 抓取页：对话页 + 长文专注模式（/article/）合并
- 媒体：2 张图（HMUIfOJaMAAGmMU、HMUIeusbsAAq6R8），保存位置 `raw/inbox/screenshots/`
- 互动：58 回复 / 167 转发 / 27万 查看