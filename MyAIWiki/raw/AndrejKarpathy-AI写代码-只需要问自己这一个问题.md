# Andrej Karpathy：AI写代码，只需要问自己这一个问题

**来源：** 微信公众号
**作者：** winkrun
**日期：** 2026-07-15
**链接：** https://mp.weixin.qq.com/s/yEWfTLs9W3-QblvPbrGUPQ

---

## 正文

Andrej Karpathy有一个简单的判断框架，用来决定哪一行代码该由谁来写。这个框架可以浓缩成一个问题：
思考到底发生在哪一步？
如果难题本身还在找解决方案，那这个活就得自己攥在手里。架构设计、API定义、安全边界、动态变化的产品需求，所有这些依赖的上下文都在你脑子里，不在大模型里。AI可以给你出几个选项，但它没法靠谱地推断那些还没做出来的决策。
当一个任务不再需要判断的时候，它就不再是工程问题，变成了执行问题。这才是AI能发挥最大杠杆作用的地方。
CRUD接口、写文档、数据库迁移、重复重构、测试、样板代码，这些任务的成功标准都是可预测的。难的地方已经不是决定要做什么，而是把已经定义好的工作落地。
一个好用的经验法则是：如果两个资深工程师独立做，最后能写出差不多的实现，那这个任务交给AI就合适。如果实现依赖产品判断或者业务上下文，那还是得人来做。
这也是为什么Karpathy不固定用某一种AI工作流。他会在自己写、用补全、把整个任务交给AI代理之间切换，不是因为哪个工具更聪明，而是每个任务需要的判断层级不一样。
有网友说，当你用这个视角看AI编码，这三种工作流就不再是三个独立工具，而是同一个问题的三个不同答案。现在每次打开Claude或者Cursor之前，我都会先问自己：
思考已经完成了吗？
答案是肯定的，就交给AI做。答案是否定的，就自己攥住。
比如，写认证模块的代码？交给AI。要不要给你的产品做密码登录？这个决定自己留着。
真正的能力不是知道AI能做什么，而是知道哪些事还值得你自己思考。
这个判断逻辑刚好和另一位开发者rvaniaaa最近分享的项目对上了。他做了一套能让AI代理自己不断从GitHub学新技能的系统，核心分工逻辑完全符合Karpathy的框架：人做判断，AI做执行。
现在AI代理都有一个问题：你不给它更新技能，它永远不会自己进步。不是模型能力不够，是新的工作流、架构、工程技巧不会自己跑到代理里去。这些东西都藏在成千上万个GitHub仓库里，总得有人去找，去读，去判断有用没用，再手动教给AI代理。
既然AI已经能写代码、审PR、用工具了，为什么不能让它自己找新技能？
rvaniaaa做的系统就是解决这个问题的：它自动扫GitHub，提取可复用的工作流，转成AI代理能用的Skill，不用等人类更新，就能自己扩展能力。
高层架构
整个系统的高层架构如下。乍一看像一条流水线，实际上每个代理只做一件事，输出结构化结果传给下一个。这种分离让每个组件都保持简单，好维护，单个模块升级也不用动整体。
它把一个大问题拆成了八个独立步骤，每个代理只做一件事，输出结构化结果传给下一个。
每个代理只干一件事。整个系统的可靠性正来源于此。
下面逐个看每个步骤做什么。
1. Scout：找仓库
整个流程从找新想法开始。Scout只负责持续监控GitHub趋势榜，以及按固定关键词搜仓库，找可能包含新AI工作流、代理架构、工程模式的候选仓库。它不读代码，不判断质量，只出候选列表。
一个典型的搜索查询长这样：
Query:
("agent framework" OR langgraph OR mcp OR "multi-agent")
Filters:
stars:>100
pushed:>2026-06-01
language:Python
archived:false
sort:updated-desc
搜出来的仓库在进入模型之前就已经是结构化对象了：
{
"name": "awesome-mcp-server",
"stars": 842,
"language": "Python",
"last_updated": "2026-07-09T14:32:00Z",
"status": "QUEUED"
}
Input：
GitHub Trending、GitHub Search
Output：
新发现的仓库列表
2. Filter：筛掉噪声
找仓库容易，找有用的难。大部分仓库和可复用AI工作流没关系，提前用确定性规则干掉明显不相关的，比如CSS库、游戏项目、数据集，能省大量token和计算资源。
Filter不用LLM做分类，而是先跑一套固定规则。一个典型的决策长这样：
{
"repository": "awesome-mcp-server",
"category": "AI Agent",
"language": "Python",
"decision": "KEEP",
"reason": "Contains reusable agent workflows"
}
被拒掉的也长一样：
{
"repository": "css-animation-library",
"category": "CSS",
"language": "TypeScript",
"decision": "REJECT",
"reason": "Outside AI workflow scope"
}
目标不是做完美判断，只是干掉明显的噪声，让后面昂贵的LLM步骤只处理可能有用的候选。
3. Reader：读仓库找信息
Reader是整个流程里最重要的环节之一。大部分分析工具上来就读源码，其实这是最慢的方式。
文档解释意图，代码解释实现。你几乎总是需要先搞懂前者，再碰后者。
结构清晰的仓库，README和文档早就把架构说清楚了。Reader固定按以下顺序读，上一步信息够了就不往下走：
README
↓
docs/
↓
examples/
↓
package.json
↓
requirements.txt
↓
source code
好的仓库，在让你读代码之前就已经把事说清楚了。
Reader不是把整个仓库倒进模型，而是增量构建上下文：
{
"repository": "langgraph-agent",
"context_loaded": [
"README",
"docs/workflows.md",
"examples/basic_agent.py"
],
"source_code_loaded": false,
"decision_reason": "Workflow identified before code analysis."
}
很多时候文档和示例已经把工作流说清楚了，根本不用读源码。这个简单排序既省token，也让系统先搞懂项目做什么，再碰实现细节。
4. Workflow Extractor：抽工作流
这是整个系统的核心。目标不是搞懂整个仓库，而是找到值得复用的工作流。
如果找不到，仓库直接踢出流程。如果找到了，就抽成标准化结构，所有后续模块都能直接读懂：
{
"skill_name": "github-pr-reviewer",
"goal": "Review GitHub pull requests before merge",
"inputs": [
"Pull Request URL",
"Repository Context"
],
"steps": [
"Read changed files",
"Identify risky modifications",
"Check coding standards",
"Generate review comments"
],
"outputs": [
"Review Summary",
"Action Items"
],
"failure_modes": [
"Missing project context",
"Large architectural refactor"
]
}
可复用的工作流，比它们出处的仓库活得更久。
从这一步开始，流程就不再处理仓库，只处理可复用的工作流了。
剩下的都只是实现细节。
5. Skill Score：按规则打分
不是所有工作流都值得变成AI技能。rvaniaaa特意没让LLM做判断，而是用固定规则做客观评估。
不是每个决策都该交给LLM。
有些决策用确定性规则表达更好，更快、更便宜、结果也更稳定。
每个工作流按以下标准评估，任一必选项不通过就拒掉：
{
"skill_name": "github-pr-reviewer",
"score": 0.94,
"checks": {
"readme": true,
"examples": true,
"min_steps": true,
"reusable": true,
"general_purpose": true
},
"decision": "PASS"
}
结果就是：
Result
PASS
Confidence: 94%
6. Skill Generator：生成标准化技能包
过了评估，就把抽出来的工作流转成标准化的技能包。不管来自什么项目，都用统一格式：
name: github-pr-reviewer
version: 1.0.0
description: Review GitHub pull requests and generate actionable feedback.
inputs:
- github_pull_request
- repository_context
steps:
- Read changed files
- Identify risky modifications
- Verify coding standards
- Generate review comments
outputs:
- review_summary
- review_comments
tags:
- github
- code-review
- engineering
除了核心技能定义，还会自动生成配套文件：
github-pr-reviewer/
├── SKILL.md
├── examples.md
├── commands.md
├── metadata.json
└── tests.md
标准化是这个技能库能用的核心：不管是从LangGraph项目抽的，还是从MCP服务抽的，转成统一格式后，AI代理不用关心来源，直接就能用。
7. Reviewer：审核技能
Reviewer只做一件事：判断这个技能值不值得发布。
写技能的那个代理，永远不该由它自己来判断技能好不好。
生成和审核分开，能让整个流程靠谱很多。
它的prompt非常简单：
Would an experienced engineer install this Skill without editing it?
Answer only:
YES or NO
Explain your reasoning in one paragraph.
Point out any missing assumptions or unclear steps.
If NO, suggest the minimum changes required for approval.
Do not rewrite the entire Skill.
一次典型审核长这样：
{
"decision": "YES",
"confidence": 0.96,
"reason": "The workflow is reusable, clearly documented and can be applied outside the original repository."
}
答案是NO，流程直接停。答案是YES，进最后一步。
8. Publisher：发布拉取请求
审核通过后，剩下的发布流程全自动化：
GitHub Action
↓
Create Branch
↓
Commit Skill Package
↓
Open Pull Request
↓
Assign Reviewer
生成的PR已经包含了审核需要的所有内容：
Title:
Add Skill: github-pr-reviewer
Files:
✓ SKILL.md
✓ examples.md
✓ commands.md
✓ metadata.json
✓ tests.md
没有自动合并步骤。
自动化负责提议，人类负责批准。
整个流程：自动发现仓库、提取可复用工作流、生成技能、准备PR。最终批准永远属于人类审核者。
现在所有AI能力，都得先被人发现，才能给AI用。这就是当前的瓶颈。rvaniaaa这套系统就是要把整个发现、提取、整理的过程自动化，人只需要做最终判断，不用花几个小时翻仓库找新想法。
下一代代理不会只训练一次就定型。它们会持续从人类每天构建的软件中学习。
这个项目就是往这个方向走的一次尝试。说不定有人能基于这个做出更好的系统。
关注公众号回复“进群”入群讨论

---

标签： #主题/AI-Coding #主题/Skill #主题/AI-Agent #节点/思考发生点 #节点/判断执行分界 #节点/GitHub技能蒸馏 #场景/公众号长文
