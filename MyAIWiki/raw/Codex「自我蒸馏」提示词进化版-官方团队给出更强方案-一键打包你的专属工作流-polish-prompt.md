# WeChat Compile Polish Prompt

## 使用方法

把生成后的完整提示词粘贴给 Codex 或 Claude，用来把自动编译草稿精修成可长期保留的 `digest` 和 `wiki` 页面。

推荐先执行：

```bash
python3 /Users/topsee/ouyangrong1313/MyAIWiki/scripts/build_wechat_polish_prompt.py --slug <slug> --category 02-ai-coding
```

## 目标

基于以下输入：
- 原文 `raw/{slug}.md`
- 自动生成的 `raw/{slug}-digest.md`
- 自动生成的 `wiki/{category}/{slug}.md`

请把这篇微信文章精修为：
1. 一个质量足够高的 `digest`
2. 一个质量足够高的正式 `wiki`

## 精修要求

### 对 digest

- 保留标题和来源信息
- 重写“核心观点”，不要机械摘句，要提炼真正的判断
- 输出 7 个分析角度，每个角度写成可复用的拆解点
- 输出 21 个开头钩子，按 7 组组织，每组 3 个
- 风格要简洁、能复用、避免空话
- 如果草稿质量低，不要沿用，应直接重写

### 对 wiki

- 保留 `# 标题`
- 必须遵循以下结构：
  - `## 核心结论（一句话）`
  - `## 分类提炼`
  - `## 要点列表`
  - `## 标签`
  - `## 相关链接`
- `核心结论` 要体现文章最值得长期保留的一句话
- `要点列表` 以 3-7 条为宜，每条都应是高度压缩后的可执行认知
- `分类提炼` 里的场景、标签、类型要合理，不要照抄草稿里的低质量归纳
- `相关链接` 里如果没有足够信息，不要虚构页面名，可保留最小链接集合

## 输出要求

只输出两个 Markdown 代码块，顺序固定：

1. 第一个代码块：精修后的 digest 完整内容
2. 第二个代码块：精修后的 wiki 完整内容

不要输出解释，不要输出点评，不要加额外标题。

精修完成后，可用下面的命令把两个代码块回写到知识库文件：

```bash
python3 /Users/topsee/ouyangrong1313/MyAIWiki/scripts/apply_wechat_polish_output.py --slug <slug> --category 02-ai-coding --input /path/to/model-output.md
```

---

## 输入材料

### raw/Codex「自我蒸馏」提示词进化版-官方团队给出更强方案-一键打包你的专属工作流.md

```markdown
# Codex「自我蒸馏」提示词进化版！官方团队给出更强方案，一键打包你的专属工作流

**来源：** 微信公众号
**作者：** AI寒武纪
**日期：** 2026年5月24日 22:49
**链接：** https://mp.weixin.qq.com/s/SDYTJrkpzFk-QbSCJQaLuQ

---

## 正文

↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新




 

前几天我介绍了一个小的codex不断蒸馏自己的提示词，文章看这里：

Codex隐藏神技：一句提示词自动蒸馏你自己，让日常重复工作全自动化

这个提示词比较粗糙，执行起来可能会有很多问题

今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词

总体思想是让 Codex 回顾你的会话、Memories 和 Chronicle，识别其中的模式，复用已有内容，并且只创建最小但有用的技能、子代理或自动化。

但是这个提示词还会不断往前发展，有了更好的版本我会持续分享

提示词如下

复制粘贴以下提示词到codex就行（记得打开Chronicle），可以边用边实践，不满意的话，可以让codex删除就行。

回顾我最近 30 天的工作；如果可用历史少于 30 天，就回顾全部可用历史，找出值得打包的重复性手动流程。

按以下优先顺序使用可用证据：

• 最近的 Codex 会话和任务摘要。
• Codex Memories 和 rollout 摘要，用来发现跨会话重复出现的模式。
• 如果启用了 Chronicle，用它来发现 Codex 之外的重复工作。Chronicle 仅用于发现；重要细节尽可能回到相关源系统中确认。
• 现有技能、自定义代理和自动化，优先复用或扩展已有内容，避免重复创建。

广泛寻找那些重复、耗时、容易出错、上下文负担重，或受益于一致流程的工作。范围包括编码、研究、写作、规划、沟通、运营、分析和个人事务管理等。

只有当候选项满足以下条件时才采取行动：

• 至少发生过两次，或明显很可能再次发生且重复成本较高；
• 输入稳定、流程可重复，并且有明确产出或停止条件；
• 能明显提升速度、质量、一致性或可靠性；
• 尚未被现有内容充分覆盖。

选择最小且合适的形式：

• Skill：可复用的流程或操作手册。
• Custom subagent：适合委派的边界清晰的专家角色或调查任务。
• Automation：定时或重复执行的检查、报告、提醒或监控。
• Skip：过于一次性、模糊、敏感，或证据不足、不适合打包的工作。

先生成一份简洁候选清单，包含：

• 重复工作流
• 支持证据和日期
• 频率/置信度
• 推荐形式：skill、subagent、automation、extend existing 或 skip
• 为什么值得或不值得创建

然后只创建高置信度且缺失的项目。保持范围窄、实用、能感知来源，并且易于验证。不要创建猜测性的、重叠的或过于宽泛的资产。

最后总结：

• 你创建或扩展了什么
• 你有意跳过了什么
• 哪些内容需要更多证据后再打包”

英文版


Ask Codex to look across your sessions, Memories, and Chronicle, identify patterns, reuse what already exists, and only create the smallest useful skill, subagent, or automation.

"Look back over my recent work from the last 30 days, or all available history if shorter, and identify repeated manual workflows worth packaging.

Use available evidence in this order:
- Recent Codex sessions and task summaries.
- Codex Memories and rollout summaries to find patterns repeated across sessions.
- Chronicle, if enabled, to spot repeated work outside Codex. Use Chronicle for discovery only; confirm important details in the relevant source system when possible.
- Existing skills, custom agents, and automations, so you reuse or extend what already exists instead of duplicating it.

Look broadly for work that is repeated, time-consuming, error-prone, context-heavy, or benefits from a consistent process. Include workflows across coding, research, writing, planning, communication, operations, analysis, and personal administration.

Only act on a candidate when it:
- occurred at least twice, or is clearly likely to recur and costly to repeat;
- has stable inputs, a repeatable procedure, and a clear output or stopping condition;
- would materially improve speed, quality, consistency, or reliability;
- is not already adequately covered.

Choose the smallest appropriate form:
- Skill: a reusable workflow or playbook.
- Custom subagent: a bounded specialist role or investigation task suitable for delegation.
- Automation: a scheduled or recurring check, report, reminder, or monitor.
- Skip: work that is too one-off, ambiguous, sensitive, or poorly evidenced to package.

First produce a compact shortlist with:
- repeated workflow
- supporting evidence and dates
- frequency/confidence
- recommended form: skill, subagent, automation, extend existing, or skip
- why it is or is not worth creating

Then create only the high-confidence missing items. Keep them narrow, practical, source-aware, and easy to validate. Do not create speculative, overlapping, or overly broad assets.

Finish with:
- what you created or extended
- what you deliberately skipped
- what needs more evidence before packaging"


 







--end--




最后记得⭐️我，每天都在更新：如果觉得文章还不错的话可以点赞转发推荐评论

/...@作者：你说的完全正确（YAR师）

---

标签：#主题/AI-Coding #场景/公众号长文
```

### raw/Codex「自我蒸馏」提示词进化版-官方团队给出更强方案-一键打包你的专属工作流-digest.md

```markdown
# Codex「自我蒸馏」提示词进化版！官方团队给出更强方案，一键打包你的专属工作流 — 拆解

**来源：** https://mp.weixin.qq.com/s/SDYTJrkpzFk-QbSCJQaLuQ
**作者：** AI寒武纪
**标签：** #主题/AI-Coding #场景/公众号长文

> 自动编译草稿，建议人工补齐核心观点与钩子质量。

---

## 核心观点

1. **↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新**
2. **前几天我介绍了一个小的codex不断蒸馏自己的提示词，文章看这里：**
3. **Codex隐藏神技：一句提示词自动蒸馏你自己，让日常重复工作全自动化**
4. **这个提示词比较粗糙，执行起来可能会有很多问题**
5. **今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词**

---

## 7个分析角度

### 这篇文章主要回答了什么问题
- 文章把重点放在：↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新

### 为什么这个判断值得关注
- 它反复强调：前几天我介绍了一个小的codex不断蒸馏自己的提示词，文章看这里：

### 对个人工作方式的直接启发
- 可直接落地的一点是：Codex隐藏神技：一句提示词自动蒸馏你自己，让日常重复工作全自动化

### 对团队协作的启发
- 放到团队场景里，可以理解为：这个提示词比较粗糙，执行起来可能会有很多问题

### 它反对的低效做法是什么
- 反过来看，它也在提醒不要忽视：今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词

### 最值得沉淀进知识库的内容
- 适合长期保留的结论是：今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词

### 下一步可以怎么继续深入
- 继续延展时，可围绕这一点展开：今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词

---

## 开头钩子

1. 如果你只把这篇文章当作常规经验帖，那最关键的一层你还没抓到：↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新
2. 真正值得记下来的，不是表面案例，而是它指向了：前几天我介绍了一个小的codex不断蒸馏自己的提示词，文章看这里：
3. 这篇内容最有价值的地方，在于它把一个常被忽略的问题说透了：Codex隐藏神技：一句提示词自动蒸馏你自己，让日常重复工作全自动化
4. 很多人会直接跳到结论，但更该看到的是：这个提示词比较粗糙，执行起来可能会有很多问题
5. 把它放到日常工作里看，最先该调整的是：今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词
6. 真正能复用到后续任务里的，其实是这一点：今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词
7. 如果要把全文压成一句执行提醒，我会保留：今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词

---

## 相关链接

- 待补充：人工补齐相关页面
```

### wiki/02-ai-coding/Codex「自我蒸馏」提示词进化版-官方团队给出更强方案-一键打包你的专属工作流.md

```markdown
# Codex「自我蒸馏」提示词进化版！官方团队给出更强方案，一键打包你的专属工作流

## 核心结论（一句话）

↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新

## 分类提炼

- 场景：AI Coding / 公众号长文
- 标签：#主题/AI-Coding #场景/公众号长文
- 类型：自动编译草稿 / 待人工复核

## 要点列表

1. ↑阅读之前记得关注+星标⭐️，😄，每天才能第一时间接收到更新
2. 前几天我介绍了一个小的codex不断蒸馏自己的提示词，文章看这里：
3. Codex隐藏神技：一句提示词自动蒸馏你自己，让日常重复工作全自动化
4. 这个提示词比较粗糙，执行起来可能会有很多问题
5. 今天codex 团队的Vaibhav (VB) Srivastav分享了更完整的执行性更高的提示词
6. 总体思想是让 Codex 回顾你的会话、Memories 和 Chronicle，识别其中的模式，复用已有内容，并且只创建最小但有用的技能、子…
7. 但是这个提示词还会不断往前发展，有了更好的版本我会持续分享

## 标签

#主题/AI-Coding #场景/公众号长文

## 相关链接

- 原文链接：https://mp.weixin.qq.com/s/SDYTJrkpzFk-QbSCJQaLuQ
- 待补充：人工补齐相关页面
```
