# Anthropic 发布 AI-Native 软件开发流程：时代变了，该换套模式了

**来源：** Anthropic 官方博客（中文参考译文另存于下方）
**作者：** Louis Claxton / Anthropic Applied AI team
**日期：** 2026-08-21（2026-08-26 更新）
**链接：** https://claude.com/blog/the-ai-native-sdlc-playbook
**中文参考来源：** Founder Park 编译：https://mp.weixin.qq.com/s/YeAL7XBmltR4n3rUnz3Pag
**正文 SHA-256：** 6b536dde3750db3483543e997e0a41106df73c20349a66160d45abc8d418a4f0（官方英文正文提取）

---

## 正文

Anthropic 在 8 月 21 日发布了一篇博客《The AI-Native SDLC Playbook》，作者 Louis Claxton。SDLC 指的是「软件开发生命周期」，全称：Software Development Life Cycle，说的是软件从一个想法变成线上产品的完整过程，通常拆成规划、设计、构建、测试、部署、运维六个阶段。
在看文章之前，先看一下这个数据：App Store 销售额十年来首次下降。换言之：香草时代，结束了。
文章转载自「赛博禅心」的编译版本。全文约八千字，保留了原文全部代码示例和配置样板，并对部分章节的表述进行了适合中文读者的调整。
⬆️
关注 Founder Park，最及时最干货的创业分享
Founder Park 正在
持续寻找值得被看见的 AI 团队与项目。
我们将通过「AI 产品市集」、内容报道、社群分发等方式，帮你触达早期用户、获得真实反馈，以及建立关键连接。
如果你正在做 AI 相关的事，欢迎和我们聊聊。
01
代码不再是瓶颈
很多团队已经在用 AI 写代码了，速度快到一年前根本想不到。但代码周围的流程没跟上。
大部分工程团队还是老一套审批门禁、代码审查、人工交接、合规策略，把 Claude Code 这类 agentic coding 工具带来的效率提升活活卡住。
传统做法里，SDLC 的每个阶段是一个独立环节，各有各的负责人。产品经理写需求，技术架构师把需求变成设计，工程师按设计写代码，QA（Quality Assurance，质量保证）团队做验证，发布团队负责上线，运维团队盯线上。工作在这些环节之间流转，靠的是文档、工单和签批。
这套流程很重，是为了确保每一步都有人负责、有人管控。但它的设计前提是：
写代码和实现代码是最耗时、最费钱的阶段
。现在这个前提不成立了。PRD（Product Requirements Document，产品需求文档）、估时会议、产品安全审查，这些东西存在的意义是在可能长达数周、数月甚至数个季度的开发周期里强制对齐认知。
传统 SDLC 还有一个假设：每一步都是人在做。产出最大的那些组织已经围绕 agentic AI 的能力重建了流程，同时确保人始终在回路中。这份指南里，我们会逐阶段走一遍 Anthropic Applied AI 团队在内部集成 Claude 的最佳实践，加速开发、让流程跑得更快。
当代码不再是瓶颈、构建阶段跑得比传统 SDLC 允许的速度还快时，三件事变成了现实：
瓶颈转移到了构建阶段的左右两侧
。主要是规划、审查/测试和部署，这些环节还在以人的速度运行。
管控手段和现实脱节了
。代码是人写的时候，逐行审查是合理的。但当 agent 产出了大部分 diff，逐行审查跟不上了。
治理成本上升了
，因为例外情况还是要走会议和委员会，而这些会每周或每月才开一次。
构建不再是约束，
约束来
自构建
两侧那些人速运行的环节
拿安全审查做个例子。安全团队的人力配置是按人类产出量来的，agent 把代码产出量翻了好几倍之后，要么审查队列越积越长，要么代码没审就上线了。受监管的组织两种结果都接受不了，安全和合规检查必须跟上 agent 的速度。
要真正兑现 agentic AI 的效率收益并确保安全，传统 SDLC 需要经历和代码实现阶段同等程度的改造。
什么是 AI 原生 SDLC
AI 原生 SDLC 是一套重新设计的流程，把旧的管控目标和新的执行方式结合起来。流程从线性变成了循环，AI 嵌入到每个节点。AI 原生 SDLC 推动自动化的交接和后续步骤的触发，解决的是传统 SDLC 各阶段之间手动、笨重的衔接问题。
AI 原生 SDLC 循环
关键转变
贯穿 AI 原生 SDLC 的核心概念是
提交的产物（committed artifact）
。每个阶段结束时往版本控制里写一个产物（
intent.md
、
spec.md
、
plan.md
、代码 diff 及其测试、带审查结论的 PR、事故记录），下一个阶段从读取这个产物开始。
早期阶段的主要产物是 .md 文件，因为产品负责人和 agent 都能读、都能用。从构建阶段往后，产物就是代码和它的记录了。这条 commit 链本身就是审计链：谁提了什么需求，agent 产出了什么，谁批准了它。
人对每一个需要判断力的决策负责。在 agentic SDLC 的世界里，
人的注意力随着需要审查的产物一起转移。
02
各阶段 Play
Play 是这份手册的核心，按六个非线性阶段分组（规划、设计、构建、测试、部署、运维），覆盖完整生命周期。每个 play 包含：变化了什么、如何开始、具体实施步骤、治理考量、如何衡量效果。
这些步骤是模块化的，组织可以根据自身需要优先改造不同阶段。一个阶段在提交产物时结束，这次提交同时启动下一个阶段。一个通过审核的
intent.md
触发需求和设计环节，一个通过审核的
spec.md
触发 plan mode，一个合并的 PR 触发流水线，线上的监控指标突破控制带时写出下一个
intent.md
，循环继续。
一开始你手动触发每一步，最终状态是每个通过审核的产物自动触发下一个门禁。
人的注意力集中在门禁上，审查的是 agent 标记出来的内容，不用从头开始每个阶段。
Play 依赖图：箭头给出采纳顺序，
从任何没有箭头指入的 play 开始
03
第一阶段：规划
用 intent.md 捕获意图
intent.md
是软件开发流程的起点，可以从不同入口进来。一个人有了想法，一个工单被提交，或者一个告警触发了事故。
当一个人有了想法，他和 Claude 一起头脑风暴，产出一份 Markdown 格式的 proto-spec。传统 SDLC 里，这个人接下来得说服产品团队的人帮他写或替他写。Claude 生成的 proto-spec 是人类可读的、版本控制的，下一个阶段可以直接消费。
这是一次性的搭建工作，由平台或工程团队完成。仓库建好之后，没有 git 经验的人不需要直接用 git。一个连接到 GitHub 的 connector 可以让 Claude 在 claude.ai 或 Cowork 里代替他们提交 Markdown 文件。
具体怎么做
第一步
，发起人用自己的话向 Claude 描述问题。不需要正式语言。
第二步
，反复头脑风暴直到想法具体化。Claude 会问分析师该问的问题：范围、用户、约束、怎样算成功。
第三步
，让 Claude 按组织模板把结果写成
intent.md
。模板可以编码为一个 skill。
第四步
，发起人修正 Claude 理解错的地方。
第五步
，把
intent.md
提交到共享仓库。作者和时间戳加入记录。
一个
intent.md
长这样：
intent
.md 示例
# Intent: claims status self-service Author: J. Ortiz (claims operations). Status: draft.  ## Problem Customers phone the contact center to ask where their claim is. Handlers spend roughly a third of call time on status-only queries.  ## Proposed outcome Customers see claim status, next step and expected date in the portal.  ## Affected users and systems Claims handlers, portal team, claims-core API.  ## Constraints No new PII in the portal session. Existing authentication only.  ## Open questions Do third-party loss adjusters need access too?
治理考量
：
证据就是提交的 intent.md，列有作者、时间戳和完整修订历史，记录在 intent 仓库的 git 历史里。产品负责人审批，接受或拒绝的决定记录为合并或关闭审查。
04
第二阶段：设计
产品负责人批准后，Claude 拿着通过审核的
intent.md
生成需求和设计规格说明。这个过程受组织的 skills 指引，涵盖品牌、安全、合规和 UX。
产品负责人审查这份规格说明，但不写它
。这个流程的目标是产出一份工程团队可以据此规划的 spec，同时标记出需要关注的地方。
前端工作是最直观的例子。
intent.md
通过审核后，产品负责人在 Claude Design 里基于它做出 mock，反复迭代，然后导出到 Claude Code 来构建。
具体怎么做
产品负责人打开一个加载了组织 skills 的会话，附上
intent.md
。Prompt 指向
intent.md
，列出约束条件，要求标记关注点。一开始手动跑，然后编码成组织级别的 slash command。再往后，让
intent.md
在 intent 仓库中被接受这个动作成为触发器。
同一个产品负责人对照 idea 审查 spec。先处理标记出来的关注点，产品负责人在工程团队看到 spec 之前，和对应的策略负责人一起解决每一个。最后把
spec.md
和
intent.md
一起提交。
产品负责人决定 spec 和 intent 是否进入构建阶段，涉及组织认定的高风险内容时咨询技术负责人。
这个决定始终由人来做。
Prompt 长什么样
Read the attached intent
.md
and produce
a
requirements and design spec for integrating it into our existing codebase. Apply the skills available
to
you so the plan conforms
to
our brand guidelines, security policies and UX standards. Document the spec fully as spec
.md
, ready
to
hand
to
the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.
治理考量
：
组织的 skills 作为约束条件应用在 spec 上。不是等几周后在审查里才发现冲突，而是在 spec 编写时就读取并应用了现行策略。Spec、产生它的 prompt、以及生效的 skill 版本，全部记录在版本控制里。
05
第三阶段：构建
Claude Code Plan Mode 作为默认起点
工程师在 plan mode 下启动 Claude Code 会话，给 Claude 第二阶段产出的
spec.md
，让它提问、讨论，反复迭代计划，直到工程师满意。
工程师把
intent.md
和
spec.md
给 Claude，要求一份实施计划：列出要改的文件、工作顺序、证明它 work 的测试。质询计划：问这个改动可能破坏什么，哪一步风险最大，Claude 为什么没选其他方案。反复迭代，直到一个从没看过这段对话的工程师也能只凭这份计划完成改动。
把通过审核的计划提交为
plan.md
。接受计划，让 Claude 实施。有一份扎实的计划，实施通常一遍就完成了。
plan
.md 示例
# Plan: claims status self-service (from intent.md 2026-06-02)  ## Files that change portal/src/claims/StatusPanel.tsx (new), claims-api/routes/status.py, claims-api/tests/test_status.py  ## Order of work 1. Add the status endpoint behind existing auth. 2. Panel against the endpoint. 3. Wire into the portal nav.  ## Risks The claims-core API rate-limits at 50 rps; the panel must cache.  ## Proof test_status.py covers the four claim states; screenshot matches the approved mock.
治理考量
：
设计审查发生在任何代码生成之前，改方向还只是改文档的事。Plan mode 本身就强制执行了这一点，因为工程师接受计划之前 Claude 不能编辑文件。
Claude Code Auto Mode
Claude Code 也可以在 auto mode 下运行。工程师审批计划，满意之后 Claude 自动逐个应用变更，不需要每次编辑都确认。随着后续 play 的护栏成熟（调好的
CLAUDE.md
、编码了策略的 skills、拦截不安全操作的 hooks、Claude 能自己跑的测试套件），auto-accept 成为常规工作的默认模式。
注意力的重心从「看着 agent 做每一次编辑」转向
「在更长的自主会话之后审查产物」。
CLAUDE.md
CLAUDE.md
给 Claude 提供一个新人入职第一天需要知道的东西：代码规范、命令、架构、团队最常见的错误。过去存在人脑里和 wiki 上的知识，变成了 agent 每次会话开头都会读的文件，由整个团队维护，每犯一次错就迭代一次。
在仓库里跑
/init
，Claude 从它发现的东西里生成一个初始版本。把它精简到新人第一天需要的内容。一条实用规则：
Claude 犯同一个错两次，纠正就进 CLAUDE.md
。控制在一页以内。
CLAUDE
.md 示例
# Payments service  ## Commands - Build: make build - Test: make test (unit), make itest (integration, needs docker) - Lint: make lint (runs in CI; fix before pushing)  ## Conventions - Java 21, Spring Boot 3. No new Lombok. - Money is always BigDecimal, never double. - Every endpoint needs an integration test in src/itest.  ## Architecture - api/ holds REST controllers, core/ holds domain logic,   adapters/ talks to external systems. - Kafka events are defined in schemas/;   never edit generated classes.  ## Things Claude gets wrong - Do not bump dependency versions;   the platform team owns them. - The legacy v1/ package is frozen; changes go in v2/.
Skills：机构知
识的
可执行化
Skills 是组织让机构知识真正发挥作用的方式。指令是显式的、版本控制的、广泛适用的，策略变化时集中更新。经验法则：
需要一致性执行的机构知识写成 skill。
找一条今天执行不一致的知识，写成 skill，放在仓库的
.claude/skills/
目录里让它随代码一起分发。策略变化时改 skill，工程师在下一次会话自动获取新版本。
.claude
/
skills
/
secure
-
api
-
review
/
SKILL.md 示例
--- name: secure-api-review description: Apply the API security standard. Use whenever   creating or modifying an external-facing endpoint,   reviewing API code, or generating an OpenAPI spec. --- # Secure API review  When you create or change an API endpoint: 1. Authentication: every endpoint requires the gateway JWT;    no anonymous routes outside /health. 2. Input validation: validate request bodies against the    OpenAPI schema and reject unknown fields. 3. Audit: every state-changing endpoint emits an audit event    with actor, action, entity and timestamp. 4. Data classification: fields tagged pii in the schema must    never appear in logs or error messages.  Run scripts/check-endpoints.sh and include its output in your summary.
治理考量
：Skill 是一种管控手段，但是建议性的。必须无条件执行的策略需要在 skill 背后加一层确定性的东西，比如 hook。Skill 让违规变得少见，hook 让违规几乎不可能。
Hooks：构建阶段的护栏
Skill 是建议性管控，hook 是背后的确定性层。Claude 在实施阶段的大部分操作是文件编辑和 shell 命令，所以构建阶段是 hook 触发最频繁的地方。
构建阶段的 hook 可以做这些事情：阻止对受保护路径的编辑（比如生成的类或冻结的包），在文件编辑后跑 formatter 和 linter，把凭证挡在 diff 之外。
Hook 在每个匹配的操作上运行，所以构建阶段的 hook 要快、范围要限定在改动的文件上。更重的检查（比如跑完整测试套件）应该放在 commit 或 PR 阶段。
并行会话和子 Agent
一个工程师可以同时推进多条工作流。
并行会话
是另一个完整的 Claude Code 实例，在各自的 git worktree 里处理独立的任务。每个独立会话互不知道对方的存在，工程师是它们唯一的共享点。
子 agent（subagent）
运行在单个会话内部，有自己的上下文窗口和工具权限，适合在多个任务中重复出现的工作，比如验证应用是否按预期运行。
用第三阶段 plan mode play 的计划，把工作拆成改动不同文件的任务。每个并行任务用自己的 worktree，比如一个终端里
claude --worktree feature-auth
，另一个终端里
claude --worktree fix-rate-limit
。两到三个会话是合理的起点。
把重复的工作变成子 agent，定义在
.claude/agents/
的 Markdown 文件里：
.claude
/
agents
/
verifier.md
--- name: verifier description: Runs the app and checks the change works   before the session reports done tools: Bash, Read --- Start the app with make run. Exercise the changed behavior and the two nearest neighboring flows. Report what you ran, what you saw, and any behavior that does not match plan.md. Do not fix anything; report only.
给 Claude 一个反馈回路
始终给 Claude 一种验证自己工作的方式，不管是测试、构建还是截图 diff。
会话自己检查自己的工作，自己修正自己的错误，然后工程师才看到。
如果检查工作现在需要一连串命令和一些环境知识，把它包装成一个 target，比如
make test
或
npm test
，失败时返回非零退出码。在
CLAUDE.md
的 Commands 部分列出每个命令和健康输出的示例。
修 bug 时先写失败的测试。让 Claude 把 bug 复现为测试，跑一遍，确认它因为预期的原因失败。提交那个测试。然后才让 Claude 在不编辑测试的前提下修复它。一个修复前就存在、agent 不能改写的测试，就是 bug 已消除的证据。
回路本身也需要保护。修代码的 agent 不能同时削弱对那段代码的检查。一个在修复任务期间阻止编辑测试文件的 hook 可以做到这一点。
CLAUDE
.md 验证块
## Verifying your work  - Build: make build (must finish with "Build succeeded") - Test: make test (all green; never skip or delete   a failing test) - Lint: make lint (zero warnings)  Run all three before reporting any task complete, and paste the output. If a test fails, fix the code, not the test.
06
第四阶段：测试
CI 中的持续 Eval
Eval 是 AI 原生世界里的 stage-gate QA。具体来说就是一个测试套件，在 agent 的配置变化时运行。换了新模型或改了 prompt，eval 套件会告诉你 agent 是否还能保持同样的工作标准。
平台工程师从近期工作中收集 20 到 50 个真实任务及其预期/通过的结果。把每个任务写成 eval：prompt 加上定义「可接受」的检查项（测试通过、lint 干净、行为不变、策略被遵守）。
每个生产事故都变成一个 eval，作为回归测试永远留在套件里。
.github/workflows/agent-evals.yml
name: Agent evals on:   pull_request:     paths: [
'CLAUDE.md'
,
'.claude/**'
]   schedule:     - cron:
'0 2 * * *'
jobs
:   evals:     runs-on: ubuntu-latest     steps:       - uses: actions/checkout@v4       - run: npm install -g @anthropic-ai/claude-code       - name: Run
eval
suite
env
:           ANTHROPIC_API_KEY:
${{ secrets.ANTHROPIC_API_KEY }
}         run: |
for
eval
in
evals/*.json;
do
claude -p
"
$(jq -r '.prompt' $eval)
"
\               --allowedTools
"Read,Edit,Bash(make test)"
\               --output-format json > result.json             ./evals/check.sh
"
$eval
"
result.json
done
AI 参与 PR 审查
Claude 既做审查者，也做被审查者。它按组织策略审查传入的 PR，同时处理自己 PR 上收到的审查意见。
工程师可以把 PR 审查的注意力集中在行为上：判断意图和风险。
技术负责人把审查策略写成仓库根目录的
REVIEW.md
，分成组织关心的几个维度：bug 和逻辑错误、安全和漏洞、是否符合 spec。
REVIEW.md
还定义什么算 Important、什么算 Nit、以及什么可以跳过。
审查者或作者在审查评论上 @claude 时，Claude 处理评论并推送修复。对于 Claude 自己开的 PR，可以更进一步，让 Claude 看管 PR 直到合并：扫描未解决的审查评论和失败的 check，处理它们并推送修复，循环往复，直到 PR 是绿的、只等代码所有者批准。
审查结论反馈到
CLAUDE.md
。
同一个错误第二次被审查标记时，纠正就在那次审查中写入 CLAUDE.md
。因为审查会读
CLAUDE.md
，从下一个 PR 开始这个错误就会被提前捕获。
REVIEW
.md 示例
# Review instructions  ## Passes Run three passes and tag each finding with its pass: - Bugs: logic errors, broken edge cases, subtle regressions - Security: injection risks, authentication gaps, PII in logs - Compliance: the change matches spec.md, plan.md   and our design principles  ## What Important means here Reserve Important for findings that would break behavior, leak data or breach a policy. Style and naming are nits.  ## Cap the nits Report at most five nits per review; summarize the rest as a count.  ## Do not report Generated files under src/gen/ and anything CI already enforces.
治理考量
：职责分离得到保持。写代码的 agent 没有途径批准自己的代码。审查策略对所有 PR 生效。批准来自人（通过分支保护），依据是审查结论。
07
第五阶段：部署
Hooks 作为审批门禁
构建阶段的 hook 是护栏，允许或阻止操作，不需要人介入。但 hook 也可以暂停操作直到特定的人批准，这正是发布门禁需要的。
工程领导层与变更管理和合规团队一起，列出必须保留的人工审批门禁。平台工程师把每个门禁表达为 hook。团队 hook 放在 git 里的
.claude/settings.json
，不可协商的 hook 放在平台管理员拥有的 managed settings 里，个人工程师无法关闭。
.claude/settings.json
{
"hooks"
: {
"PreToolUse"
: [         {
"matcher"
:
"Bash"
,
"hooks"
: [             {
"type"
:
"command"
,
"command"
:
"
${CLAUDE_PROJECT_DIR}
/.claude/hooks/production-gate.sh"
}           ]         }       ]     } }
.claude/hooks/production-gate.sh
#!/bin/bash # Production deploys require a named release authorization cmd=$(jq -r
'.tool_input.command'
< /dev/stdin)
if
[[
"
$cmd
"
== *
"deploy"
* &&
"
$cmd
"
== *
"production"
* ]]; then
if
[ -z
"
$RELEASE_APPROVAL
"
]; then      echo
"Production deploys need a release authorization."
>&
2
exit
2
fi fi exit
0
治理考量
：Hook 就是审批门禁。门禁条件每次执行、对每个人执行。允许和阻止的决定带时间戳记录。
CI/CD 集成与部署
在 CI/CD（Continuous Integration / Continuous Delivery，持续集成与持续交付）流水线里非交互式地运行 Claude Code，沙箱化执行让长时间运行的 agent 安全运行，通过 MCP（Model Context Protocol，模型上下文协议）集成暴露部署能力，在 agent 真正需要之前先演练回滚路径。
平台工程师从只读的判断步骤开始。在流水线 job 里用
claude -p
来分类失败的构建、总结 flaky 测试、或起草 changelog。在现有门禁后面加写入步骤。Agent 写的任何东西都通过分支保护作为 PR 到达，
agent 没有直接推送到 main 的路径。
通过 MCP 暴露部署能力。部署、状态查询和回滚变成工具，按环境限定范围。按环境分级自主权：开发环境里 agent 自由部署，生产环境里 agent 准备发布、发布经理授权，预发布环境介于两者之间。
回滚应该是流水线里演练最多的路径
：一条命令，agent 能跑，在预发布环境里定期演练。
流水线步骤示例
- name: Triage failed build   if:
failure
()   run: >     claude -p
"Read the build log at out/build.log.     Identify the most likely cause, say whether the failure     looks flaky or real, and write a three-line summary     for the PR thread."
>> triage.md
治理原则
：agent 可以做到生产门禁为止，不能越过它。分支保护把 agent 写的任何东西变成 PR。生产部署 hook 在发布经理授权前阻止发布。每次非交互式运行都以 agent 自己的身份执行，流水线日志把 agent 做的事和触发它的工程师做的事分开。
0
8
第六阶段：运维与闭环
到目前为止，每个阶段都需要人来启动初始步骤。这个阶段的重点是
Claude 的自主运行来闭合整个循环。
比如一个持续运行的监控 agent 可以在一个 bug 工单被提出时创建
intent.md
，然后流经需求、计划、构建、测试和审查阶段。第六阶段无人值守地运行，阶段之间有独立的信心门禁来决定上一阶段的产出是继续流转还是升级给人处理。
闭合
循
环
一个确定性脚本监控生产环境，在控制带被突破时调用 Claude。
服务负责人或平台工程师选一个有稳定滚动基线的指标，比如 CI 测试失败率、部署后 5xx 率、或 PR 周期时间。写检测脚本：通常是滚动窗口上的均值和标准差，加规则（Western Electric 或类似方法）。
检测层完全确定性，不涉及模型。
在版本控制的配置文件里定义响应分级。1σ 只记日志，2σ 调用 Claude 只读诊断，3σ Claude 可以行动（但只能通过开 PR 进入审查门禁或触发预先批准的 runbook）。
bands
.yaml
示例（监控 CI 测试失败率）
metric: ci_test_failure_rate baseline: rolling_30d rules: western_electric tiers:
1s
igma: { action: log }
2s
igma: { action: diagnose,             tools:
"Read,Grep,Bash(gh run view *)"
}
3s
igma: { action: propose,             routes: [pull_request, runbook:rollback-deploy] }
Agent 按第一阶段格式把诊断写成
intent.md
：异常及其证据、预期结果、受影响的系统、待解答的问题。从这里开始，发现的问题和其他任何东西一样走流水线。
几个实际场景：
CI 测试失败率突破 3σ 时，agent 隔离 flaky 测试或开一个 revert PR，审查门禁做决定。
部署后 5xx 率突破 3σ 且时间窗口内有部署时，agent 触发现有的回滚流水线。
PR 周期时间触发漂移规则时，agent 为工程领导层写一份报告。这说明这套机制对流程指标和生产指标都管用。
Claude Tag：Claude 随叫随到
事故也可以通过 Slack 或 Teams 这样的工作通讯工具到达。Claude Tag（目前在 Slack 里公开 beta）让 Claude 以自己的身份成为频道的成员，每个新事故都能拿到第一响应。
对话和机构知识留在频道里，任何团队成员都能测试假说、探索新方案、实时调查，频道历史增加了可审计性。通过 MCP 访问，Claude 验证指标回到基线并在帖子里确认，把事后复盘写到版本控制的经验文件里。
事故不是 Claude Tag 接手的唯一工作。小的、边界清晰的修复作为 PR 进入审查门禁，更大的工作被写成
intent.md
进入第一阶段，
循环开始自我喂养。
频道就是审计链：请求、诊断、人的授权和修复，
全部留在事故被处理的地方
模型和框架越来越成熟了。组织现在可以改造的不只是写代码的方式，而是整个软件开发生命周期。
这种改造把人的判断力放在流程的中心位置，同时考虑了大型企业组织的治理和合规要求。
这份指南整合了 Anthropic Applied AI 团队每天为客户执行的真实最佳实践。希望对你有用。
更多阅读
对话陈炜鹏：Loopit 有了 1500 万件作品之后，我们决定做自己的互动世界模型
中美 NeoLab 对话：模型和 Agent 如何实现「持续学习」？
今年 AGI 大会上，这 10 个创业团队最受关注
宇树往事
Everything is a plugin，DeepSeek Harness 的真正野心，是 Agent 的自进化
转载原创文章请添加微信：founderparker

---

标签： #主题/AI-Coding #主题/AI-Native研发 #主题/SDLC #主题/Spec驱动 #主题/验证驱动 #场景/官方博客 #场景/公众号长文

## 官方一手原文（English snapshot）

- 官方标题：The AI-Native SDLC playbook
- 官方来源：https://claude.com/blog/the-ai-native-sdlc-playbook
- 作者：Louis Claxton / Anthropic Applied AI team
- 发布：2026-08-21
- 更新：2026-08-26
- 抓取方式：curl + official HTML
- 提取正文 SHA-256：6b536dde3750db3483543e997e0a41106df73c20349a66160d45abc8d418a4f0

## Code is no longer the bottleneck

Organizations have started using AI to write code at a speed unthinkable one year ago, yet the processes around the code haven't changed at the same pace.

Many engineering teams still have the same approval gates, reviews, handoffs, and policies, stalling productivity gains made by using agentic coding solutions like Claude Code .

The software development lifecycle (SDLC) is the process that takes software from idea to production. Most organizations run some version of the same six stages, covering planning, design, building, testing, deploying, and maintaining software. Traditionally, each stage is a discrete phase owned by a different role. Product managers write requirements, technical architects turn them into designs, engineers build the designs, QA teams at regulated enterprises verify it, releases teams ship it, and operations monitors what is running. Work moves between the phases through documents, tickets, and sign-offs.

The traditional software development lifecycle (SDLC) is process-heavy to ensure accountability and control at each step. However, the traditional SDLC was designed to maximize efficiency in an era where the most time-consuming and expensive stage was writing and implementing code, which is no longer the case. PRDs, estimation rituals, and product security reviews all existed to force alignment during what could be weeks, months, or quarters of development work.

The traditional SDLC also features controls that assume every step is performed by humans. The organizations generating the most value have rebuilt their process around what agentic AI can now do, while ensuring that humans stay in the loop. In this guide, we walk through several of our Applied AI team's best practices for integrating Claude internally across each stage of the SDLC to accelerate development and make processes run faster, inspired by working with our customers.

When code is no longer the bottleneck and the build phase runs faster than the traditional SDLC allows for, three things become true:

- The bottleneck moves to the steps to the left and right of the build phase. This is mainly plan, review/test, and deploy, which still run at human speed.
- The controls stop matching reality and become intractable. Reviewing each line by hand made sense when a person had written it, but it can't keep up once agents write most of the diff.
- Governance costs increase because exceptions still route through meetings and committees that meet weekly or monthly.
Let's use a security bottleneck as an example. Security teams are sized for human output, so when agents multiply code output, either the review queue builds or code ships under-reviewed. A regulated organization can't accept either outcome, so its security and policy checks have to keep pace with the agents.

To better realize the productivity gains of and secure agentic AI, the traditional SDLC lifecycle requires the same level of transformation as the implementation phase has undergone.

- Code is no longer the bottleneck
- Plays
- Stage 1 — Plan
- Stage 2 — Design
- Stage 3 — Build
- Stage 4 — Test
- Stage 5 — Deploy
- Stage 6 — Maintain
- Closing thoughts

## What is an AI-native SDLC?

The AI-native SDLC is a reimagined process that combines the old control objectives with new enforcement. Instead of a linear flow, the process becomes a loop, and AI is embedded at each point. The AI-native SDLC promotes automated handover and triggering of subsequent plays, helping to address the manual and clunky nature of handoff between the phases of the traditional SDLC.

You'll also hear this shift called the agentic SDLC, the AI SDLC, or simply agentic software development — the labels differ, but they describe the same thing.


### The shifts across the six stages of an AI-native SDLC

The table below highlights the ends of the spectrum between traditional SDLC and AI-native SDLC, supported by Claude. Most organizations sit somewhere between the two columns.

The thread running through the right-hand column is the committed artifact. Each stage ends by writing one to version control (including intent.md , spec.md , plan.md , the diff and its tests, the PR with its review findings, and the incident record) and the next stage begins by reading it. For the early stages, .md files are the predominant artifact because a product owner and an agent can both read and act on the same file. From Build onward, the artifact is code and its records. The chain of commits is also the audit trail: who asked for what, what the agent produced, and who approved it.

Humans remain accountable for every decision that requires judgment. In the agentic SDLC world, the human attention shifts along with the artifacts that must be reviewed.


## Plays

The plays are the core of the playbook and are grouped into six non-linear stages (Plan, Design, Build, Test, Deploy, Maintain), which together cover the complete lifecycle.

Each play covers:

- What changes;
- Getting started;
- Concrete steps for implementation;
- Governance considerations; and
- How you measure whether it worked.
The steps are modular and organizations may choose to prioritize transforming different stages at different times based on their unique needs. Each play names its dependencies under "Prerequisites," which the dependency graph further illustrates.

A stage ends by committing an artifact with the commit initiating the next stage. An accepted intent.md triggers the requirements and design pass, an approved spec.md triggers plan mode, a merged PR triggers the pipeline, and a breached control band in production writes the next intent.md and so the loop continues.

First, you prompt each step by hand with the end state being a loop in which each accepted artifact fires the next gate. Human attention concentrates at the gates, reviewing what the agent flagged rather than starting each stage from scratch.


## Plan


### Capture as intent.md

The intent.md , which kicks off the software development process can enter through different routes. A person has an idea, a ticket is filed, or an incident is surfaced via an alert (see Stage 6: Maintenance).

When a person has an idea, they brainstorm with Claude and produce a markdown proto-spec. In the traditional SDLC, the same person must then convince a member of the product team to write the idea up with them or on their behalf.

The proto-spec generated by Claude is human readable, version-controlled, and immediately consumable by the next stage. The proto-spec is saved as an intent.md .

Regardless of whether the intent originates from an event trigger or an agent, the same steps apply: the product owner reviews and corrects the agent-written intent.md before it is committed.

Setting this up is a one-time task for the platform or engineering team. A technical team member needs to stand up the intent home and decide who can write to it, since many contributors will come from across the organization.

Once the repository exists, contributors without git experience don't need to use git directly. Instead a connector to the version-control system (e.g. GitHub) lets Claude commit markdown files on their behalf from claude.ai or Cowork.


#### How to execute it

- The originator describes the problem to Claude in their own words. The originator may describe what they cannot do today, who is affected by the idea, what better looks like, or what is out of scope. No formal language is required.
- Brainstorm until the idea is concrete. Claude asks the questions an analyst would ask: scope, users, constraints, and what success looks like.
- Ask Claude to write the result as intent.md using the organization's template, which can be encoded as a skill set up by a technical team member and signed off by a lead. This can cover the problem, proposed outcome, affected users and systems, constraints, and open questions.
- The originator corrects anything Claude misunderstood.
- Commit intent.md to the shared home. Author and timestamp join the record, and the product owner picks the idea up from there.

#### Governance considerations

The evidence is the committed intent.md , which lists the author, the timestamp and the full revision history. It's logged in the git history of the intent home. The product owner approves, and the accept or reject decision that sends the intent into Stage 2: Design is recorded as the merge or the closing review.


## Design


### Requirements and design

Once approved by the product owner, Claude takes the accepted intent.md and produces a requirements and design spec. This is guided by the organization's skills for brand, security, compliance, and UX.

The product owner reviews that spec, but doesn't write it. The goal of this process is to create a spec the engineering team can plan against, with flagged areas of concern.

Front-end work is the clearest example. Once the intent.md is accepted, the product owner mocks the design up in Claude Design (beta) from the intent.md , iterates on the mock, and then exports it to Claude Code to build.


#### How to execute it

- The product owner opens a session with the organization's skills available and attaches the intent.md .
- The product owners prompt points at the intent.md , names the constraints, and demands flagged concerns. Run it by hand at first, then codify it as an organization-level slash command. From there make the acceptance of intent.md in the intent home the trigger, with a non-interactive job that fires on the merge, run the pass with the organization's skills loaded, and commit spec.md as a pull request (the CI/CD play in Stage 5: Deploy covers the plumbing). From that point the product owner's first involvement is the review.
- The same product owner reviews the spec against the idea. Does the spec solve the stated problem, and are the open questions from intent.md answered or carried forward?
- Work through the flagged concerns first as they are the points an analyst would have escalated. The product owner resolves each one with its policy owner before engineering sees the spec.
- Commit spec.md alongside intent.md . The file pair records what was asked for and what was decided.
- The product owner decides whether the spec and intent progress to build, consulting a technical lead for anything the organization classes as higher risk. A human team mate always makes this call, and accepting the spec is what starts the plan mode play in Stage 3: Build.

#### What it looks like (the prompt)


#### Governance considerations

Instead of being discovered in a review weeks later, the live policy is read and applied while the spec is written. The organization's skills are applied as constraints on the spec. The spec, the prompt that produced it, and the skill versions in force are all logged in version control. The product owner signs off the spec, and routes flagged concerns to the named policy owners.


## Build


### Claude Code plan mode as the default starting point

Engineers start Claude Code sessions in plan mode , give Claude the approved spec.md from Stage 2: Design, and let it interview them, iterating on the plan until the engineer is happy with it.


#### How to execute it

- The engineer starts the session in plan mode with Claude.
- The engineer gives Claude the intent.md and the spec.md and asks for an implementation plan that names the files that change, the order of the work, and the tests that prove it.
- Interrogate the plan by asking what the change could break, which step is most risky, and what other options Claude chose not to do.
- Iterate until an engineer who has never seen the conversation could implement the change from the plan alone.
- Commit the approved plan as plan.md . The plan joins the audit trail, and the PR review play (Stage 5: Deploy) checks the eventual diff against it.
- Accept the plan and let Claude implement. With a solid plan, the implementation is often a single pass.
- When implementation departs from the plan, update plan.md in the same commit. Consider using a hook to enforce synchronization between the two.

#### What it looks like (plan.md)


#### Governance considerations

Design review happens before any code is generated, when changing course is still a matter of editing a document. Plan mode enforces this itself, since Claude cannot edit files until the engineer accepts the plan. The plan and its revisions are logged along with who accepted it. Routine changes are approved by the engineer, and anything the organization classes as higher risk goes to a tech lead or architect.


### Claude Code on auto mode

Claude Code can also run in auto mode, where the engineer approves the plan and, once happy and iterated upon, Claude applies each change without a per-edit prompt. As the guardrails from the later plays mature (a tuned CLAUDE.md , skills that encode policy, hooks that block unsafe actions, and a test suite Claude can run), auto-accept becomes the default for routine work: a tight spec.md , a small blast radius, and code the tests already cover.

The shift is now away from the user watching the agent make the edits and reviewing actions, towards the review of artifacts after longer autonomous sessions. Auto-accept mode further enables parallelism across individuals and the team when used with worktrees and is fundamental to running the SDLC autonomously and closing the loop as described in Stage 6: Maintenance.


### Legacy systems and the source of truth


### The CLAUDE.md

CLAUDE.md gives Claude the context a new joiner would need, covering conventions, commands, architecture, and the mistakes the team sees most often. Knowledge that used to sit in people's heads and on wikis becomes a file the agent reads at the start of every session, maintained by the whole team and iterated on whenever a mistake is made.


#### How to execute it

- Run /init in the repo. Claude generates a starting CLAUDE.md from what it finds.
- Cut the generated file down to what a new joiner would need on day one. Keep the build, test and lint commands, the conventions that matter, and the things Claude keeps getting wrong.
- Check CLAUDE.md into git at the repo root so the whole team shares one version and changes are reviewed like code.
- A working rule helps here. When Claude makes a mistake twice, the correction goes into CLAUDE.md .
- Keep it under a page, because Claude reads all of it at the start of a session and anything stale is taking up context for no benefit.

#### What it looks like (CLAUDE.md)


#### Governance considerations

CLAUDE.md is version controlled, so the instructions the agent works to are reviewable and auditable. Team conventions are applied through the file, changes to it are logged in git history, and code owners approve those changes in PR review.


### Skills as institutional knowledge

Skills are how an organization makes its institutional knowledge operational. The instructions are explicit, version-controlled, applied broadly, and updated centrally when policy changes. The rule of thumb: write a skill for institutional knowledge that must be applied consistently; don't write a skill for components that belong in CLAUDE.md or a prompt.


#### How to execute it

- Pick one piece of knowledge that is enforced inconsistently today. This could be a security standard, an API design convention, or a brand rule.
- Write it as a skill, a folder containing a SKILL.md whose frontmatter says when it triggers and whose body says what to do. An engineer writes it from the policy owner's source of truth, using Claude to help.
- Put the skill in the repo at .claude/skills/<name>/ so it ships with the code, or distribute it organization-wide through a plugin .
- Test that the skill triggers. Ask Claude to do the relevant task in different ways and confirm the skill loads each time.
- When the policy changes, change the skill and have the policy owner sign off the change.
- Engineers pick up the new version automatically in their next session.

#### What it looks like (.claude/skills/secure-api-review/SKILL.md)


#### Governance considerations

A skill is a control, though an advisory one. It makes Claude likely to apply the policy while the code is written, and nothing forces a session to comply with it. A policy that must always hold needs something deterministic behind the skill, such as a hook that blocks the action or a review pass that re-checks the policy at the PR. The skill makes violations rare and the hook makes them close to impossible. Skill invocations are logged in session traces, and the policy owner reviews skill changes like code.


### Hooks as build-time guardrails

A skill is an advisory control while a hook is the deterministic layer behind it. Most of Claude's actions are file edits and shell commands during implementation, so the build phase is where hooks can end up firing most often.

Build-phase hooks can:

- Block edits to protected paths such as generated classes or a frozen package;
- Run the formatter and linter after file edits so drift never accumulates;
- Keep credentials out of the diff.
Back any skill whose policy has to hold without exception. A hook runs on each action that matches it, so build-phase hooks should be fast and scoped to the file that changed. Heavier checks such as the full test suite belong at the commit or the PR.

A hook that asks a human for approval belongs with the gates in Stage 5: Deploy, because an approval prompt during the build puts a person back on the critical path of all the sessions running in parallel.


### Parallel sessions and subagents

One engineer can drive several streams of work at once.

A parallel session is another full Claude Code instance, working a separate task in its own git worktree . Each independent session knows nothing about the others, and the engineer steering them is the only thing they share.

A subagent runs inside a single session as a scoped helper with its own context window and tool limits and suits jobs that recur in multiple tasks such as verifying the app runs as expected.

Parallel sessions raise the number of tasks an engineer can have in flight, while subagents keep each session focused on its own task. The engineer's job is steering and reviewing all of them.


#### How to execute it

- The engineer splits the work into tasks that touch different files, using the plan from the plan mode play (Stage 3: Build) to see where the work is independent. Tasks that share files run in a single session, one after another.
- Each parallel task gets its own worktree, for example claude --worktree feature-auth in one terminal and claude --worktree fix-rate-limit in another. A worktree is a separate checkout on its own branch, which stops sessions colliding on files.
- Two or three sessions is a sensible starting point. The practical ceiling is how many streams one person can review properly, so add sessions only while review is keeping up.
- Turn repeated jobs into subagents, as defined in markdown files in .claude/agents/ , each with a name, a description of when to use it, and the tools it may touch. Examples include a code simplifier that strips needless complexity after the main agent finishes, a verifier that runs the app and checks behavior, a researcher that explores the codebase and reports back without flooding the main context. Check the definitions into git so the whole team shares them.

#### What it looks like (.claude/agents/verifier.md)


#### Governance considerations

More sessions means more output, so the controls have to come from configuration in the repo. Hooks and permission settings there apply to all sessions, and what a session does is logged and attributed to the engineer who ran it.


## Test


### Give Claude a feedback loop

Always give Claude a way to verify its own work, whether tests, a build, or a screenshot diff. A session checks its own work and fixes its own mistakes before an engineer sees them.

The feedback loop should not be confused with a verifier subagent (Stage 3: Build). The feedback loop runs through the whole task as many times as the work. The verifier subagent, on the other hand, is one way to package the final check by running a fresh context window once the session believes the work is done. This way the verdict is not colored by the assumptions that produced the code.


#### How to execute it

- If checking the work today takes a sequence of commands and some environment knowledge, wrap it in a single target such as "make test" or "npm test" that exits non-zero on failure.
- In the CLAUDE.md 's Commands section, list each command with an example of a healthy output.
- State a target and make it quantifiable so Claude can check the work without asking you, for example: "All tests in test_status.py pass," "the screenshot matches the attached mock," or "the endpoint returns 200 with the new field".
- For bug fixes, write the failing test first. Ask Claude to reproduce the bug as a test, run it, and confirm it fails for the reason you expect. Commit that test. Only then ask Claude to make it pass without editing the test, with the test-file hook from the final step enforcing the restriction. A test that existed before the fix, and that the agent couldn't rewrite, is proof the bug is gone.
- For UI work, close the loop with a visual check. Give Claude a browser or screenshot tool, give it the mock, and let it iterate. Implement, screenshot, compare, and adjust. Two or three rounds is normal, and the result should improve with each one.
- Make verification part of "done." Instruction lives in CLAUDE.md . Run the tests before reporting a task complete, and show the output.
- Finally, the loop itself needs protecting, because an agent fixing code must not be able to weaken the check on that code. A hook that blocks edits to test files during a fix task does this. The alternative is to check the diff in review and reject any change that touches a test.

#### What it looks like (CLAUDE.md verification block)


### Continuous evals in CI

Evals are the AI-native equivalent of stage-gate QA. In practice that means a suite that runs whenever the agent's configuration changes. When a new model is swapped in or a prompt is rewritten, the eval suite says whether the agent still does the work to the same standard.

The evals should be seen as a live suite. As models improve, cases that once discriminated stop doing so and new ones must be added that arise from ongoing monitoring.

Depending on the use case, some teams may prefer to run these evals offline on a set cadence rather than on every change. The steps below are for continuous evaluations.


#### How to execute it

- The platform engineer collects 20 to 50 real tasks from recent work with its expected/accepted outcome.
- Write each task as an eval, meaning the prompt plus the checks that define acceptable (tests pass, lint clean, behavior unchanged, policy followed).
- The suite runs non-interactively in CI on a schedule and on any change to CLAUDE.md , skills or hooks, since that configuration steers the agent and deserves the regression testing that code gets.
- Gate configuration changes on the results. A skill change that drops the pass rate gets reviewed before it merges.
- Each production incident gets an eval, written by the team that owned the incident, and stays in the suite as a regression test.

#### What it looks like (.github/workflows/agent-evals.yml)


#### Governance considerations

Evals give QA a gate that keeps up with agent output. The pass-rate threshold is enforced as a merge check, runs are logged so results can be compared over time, and the team that owns the configuration change approves it.


## Deploy


### AI in the PR review loop

Claude both gives and receives reviews. It reviews incoming PRs against the organization's policies and addresses review comments on its own PRs. This allows engineers to focus on behavior in their PR review, which boils down to judging intent and risk.


#### How to execute it

- The managed Code Review service is the fastest start. An admin enables it and selects repositories. Run the review in your own CI with the claude-code-action when you need control of the pipeline or want API calls routed through your own cloud agreement (the CI/CD play covers that plumbing).
- The tech lead writes the review policy as REVIEW.md at the repo root, divided into the passes the organization cares about: bugs and logical errors; security and vulnerabilities; compliance against the spec ( spec.md from the requirements play), the implementation plan ( plan.md from the plan mode play) and design principles. REVIEW.md also defines what counts as Important as opposed to a Nit, and what to skip.
- The tech lead sets the human threshold. Findings do not approve or block a PR on their own, and branch protection still requires approval from a code owner. A platform engineer who wants to gate merges on findings can read the severity counts that the check run publishes as a machine-readable tally.
- When a reviewer or the author tags @claude on a review comment, Claude addresses the comment and pushes the fix. The PR thread records both the request and the change. This fix loop runs through the claude-code-action. In the managed service, commenting @claude review requests a fresh review instead. For PRs Claude opened, go further and let Claude babysit the PR to merge. Teams wrap the loop in a custom slash command that sweeps the unresolved review comments and failing checks on the PR, addresses them and pushes the fixes, until the PR is green and waiting only on code owner approval.
- Review findings feed back into CLAUDE.md . When a review flags a mistake for the second time, the correction goes into CLAUDE.md as part of that review, and because review reads CLAUDE.md the mistake is caught from the next PR onwards. Review also flags when a change has made CLAUDE.md outdated.
- Once a month the tech lead tunes the setup by rating findings so the reviewer improves and by capping Nit volume in REVIEW.md . Generated paths and anything CI already enforces are excluded.

#### What it looks like (REVIEW.md)


#### Governance considerations

Separation of duties is preserved, because the agent that wrote the code has no way to approve it. The review policy in REVIEW.md is applied to all PRs, and findings, fixes, ratings and approvals are logged in the PR history, so the PR is the audit record. Approval comes from a human through branch protection, informed by the findings.

For how these controls compose at production scale, see securing an AI-native SDLC at Anthropic .


### Hooks as approval gates

The build phase used hooks as guardrails, allowing or blocking actions with no human involved (Stage 3: Build). A hook can also ask, pausing the action until a specific person approves, which is what release gating needs.

The play sits in Stage 5: Deploy because the release gate is the clearest case, but hooks are not deploy-specific: they run wherever Claude acts. For example, hooks can block edits to migrations and infra without a change ticket during Stage 3: Build, and stop the agent editing test files during a fix task in Stage 4: Test.


#### How to execute it

- Engineering leadership, with change management and compliance, lists the human approval gates that must survive, such as change management sign-off, release authorization, and edits to protected paths.
- The platform engineer expresses each gate as a hook, a script that runs before Claude acts that can allow, ask, or block.
- Team hooks go in .claude/settings.json in git, and non-negotiable hooks go in managed settings owned by the platform or IT admin, where individual engineers cannot switch them off.
- A block should explain itself, so when a hook stops an action the reason and the route to approval appear in Claude's output.

#### What it looks like (.claude/settings.json)


#### And the gate itself (.claude/hooks/production-gate.sh)


#### Governance considerations

Hooks are the approval gates. The gate condition is enforced every time, for everyone. Allow and block decisions are logged with a timestamp. The gate also defines what counts as approval, whether that's an approved change ticket or the release manager's sign-off.


### Managed settings for a regulated enterprise


### CI/CD integration and deployment

Run Claude Code non-interactively inside the CI/CD pipeline, sandbox the execution so long-running agents run safely, expose deployment through MCP integrations, and rehearse the rollback paths before the agent ever needs them.


#### How to execute it

- The platform engineer starts with read-only judgment steps. Use claude -p in a pipeline job to triage a failed build, summarize a flaky test, or draft the changelog.
- Add write steps behind the existing gates for jobs like fixing lint, updating generated docs, or addressing review comments via the @claude mentions. Anything the agent writes arrives as a PR through branch protection, and the agent has no route to push to main.
- Execution is sandboxed. Agent jobs run in containers under a network policy with short-lived scoped tokens, and hold no production credentials by default.
- Expose deployment through MCP. Deploy, status, and rollback become tools, scoped per environment, so the agent's deployment powers are an allowlist rather than a shell script with credentials.
- Tier the autonomy by environment. In development, the agent deploys freely. In production, the agent prepares the release and the release manager authorizes it, and a hook enforces the production gate. Staging sits somewhere in the middle.
- Rollback should be the most rehearsed path in the pipeline, a single command that the agent can run and that is exercised regularly in staging. The closing the loop play (Stage 6: Maintenance) calls this rollback when a control band is breached, so it has to be proven in advance.

#### What it looks like (pipeline step)


#### Governance considerations

The governing principle is that the agent may act up to the production gate and cannot pass it. The controls below enforce this principle.

- Branch protection turns anything the agent writes into a PR, with no direct path to main.
- The production deploy hook blocks the release until a named release manager authorizes it. Each non-interactive run acts under the agent's own identity, so the pipeline log separates what the agent did from what the engineer who triggered it did.
- Per-environment permission tiers set how much the agent may do on the way to the gate.

## Maintain


### Maintenance and closing the loop

So far, we've discussed how to add Claude to each stage of the SDLC process, with each stage requiring a human to launch the initial steps. This stage, however, shifts the focus to autonomous running of Claude to close the loop.

For example, a continuously running monitoring agent could, off the back of a bug ticket being raised, create an intent.md , and flow through the requirements, plan, build test and review phases. Stage 6: Maintenance runs headless, with an independent confidence gate between stages, a deterministic check or an adversarial reviewing agent, deciding whether the previous stage's output continues or is escalated to a human.


### Closing the loop

A deterministic script watches production and invokes Claude when a control band is breached. Monitoring of a breach is a helpful example of the pattern for the loop running autonomously, while the Claude Tag (public beta) section at the end of the stage covers work arriving through different channels.


#### How to execute it

- The service owner or platform engineer picks one metric with a stable rolling baseline, such as CI test failure rate, post-deploy 5xx rate, or PR cycle time.
- They write the detection script, typically mean and standard deviation over a rolling window with rules (Western Electric or similar) so the bands catch slow drift as well as spikes. The script is version controlled and unit tested, and detection stays entirely deterministic, with no model involved.
- Response tiers are defined in version-controlled config ( bands.yaml below). At 1σ the script only logs, at 2σ it invokes Claude read-only to diagnose, and at 3σ Claude may act, though only by opening a PR into the review gate or triggering a pre-approved runbook.
- The trigger layer can be a scheduled workflow in GitHub or GitLab, a webhook from the existing monitoring stack, or a Cron Job inside the network. Claude runs stateless, either as a non-interactive step on a CI runner or as an Agent SDK service in a sandboxed container, and the CI/CD play covers the deployment and model-access options. Because the run is stateless and non-interactive, a loop can begin and end without anyone starting it.
- The agent writes its diagnosis as intent.md in the Stage 1: Plan format, covering the anomaly and its evidence, a proposed outcome, the affected systems and any open questions. From there the finding goes through the pipeline like anything else.
- The service owner or on-call engineer triages the queue, routing product-facing findings to the product owner. Fix now, schedule, or dismiss. Dismissals tune the bands and help to reduce noise.
- When a fix ships, add an eval for the incident (the continuous evals play) to ensure that such issues are protected against going forwards.

#### What it looks like (for example, a bands.yaml monitoring CI test failure rate)


#### Governance considerations

The tier boundaries are enforced from version-controlled config, with permissions and managed settings denying production access. Invocations, findings and triage decisions are logged with a timestamp. A service owner triages and approves findings, resulting changes go through the normal PR review gate, and the runbooks the agent may trigger were approved in advance.


#### Examples

- When the CI test failure rate breaches 3σ, the agent quarantines the flaky test or opens a revert PR, and the review gate decides.
- When the post-deploy 5xx rate breaches 3σ with a deployment in the window, the agent triggers the existing rollback pipeline.
- When PR cycle time trips a drift rule, the agent writes a report for engineering leadership, which shows the harness works for process metrics as well as production ones.

### Recurring codebase scans

A security scan is a point-in-time statement about a codebase under a particular model, and both halves go stale: the code changes every week, and each model generation finds vulnerabilities the previous one missed. The AI-native answer is to run the scan on a schedule, without a human in the invocation path, and to send what it finds through the same gates as any other change to the codebase.

Claude Security is the hosted form of scheduled scanning. Connect a GitHub repository, and scans run on Claude Mythos 5 in Anthropic's infrastructure, with each finding validated before it is reported and a confidence rating attached. Suggested patches are reviewed and applied in Claude Code on the web. The organization gets the findings without needing access to the model itself.


#### How to execute it

- The security lead connects the repositories and organizes them into projects by repo, service, or team, so ownership of findings is clear from the start.
- Run a first full scan of the most critical repositories, including ones that have been scanned before by other tools or by earlier models. Treat the first scan as the baseline. The first scan will likely surface findings in code that was considered clean.
- Set a schedule per project. Weekly is a sensible default for actively developed services; scope scans to a directory or branch where a repository is large or mixed.
- Triage findings with the confidence rating in hand. Dismiss with a reason, so the dismissal is recorded and the same finding does not return as new on the next run.
- For a bounded finding, open the suggested patch in Claude Code on the Web, review it, and send it through the PR review gate like any other change. The agent that proposed the fix has no route to approve it.
- For anything wider than one patch, such as an architectural weakness or a pattern repeated across services, write it up as intent.md in the Stage 1 format and start it at Plan.
- When a fix is released to production, add an eval for the vulnerability class to the suite from the continuous evals play, so the configuration that steers the agent is tested against that class from then on.
- Export findings as CSV or Markdown, or use webhooks, to keep the organization's existing tracker and audit systems as the system of record where auditors already expect them.

#### Governance considerations

The scan runs under the organization's admin controls meaning what repositories are connected, who holds a scan seat, and the spend limit are all set centrally. Every finding has a validation result and a confidence rating, and every dismissal has a reason, so the scan history is an audit record of what was found, fixed, and consciously accepted.

Fixes reach production through the PR review gate and branch protection rather than from the scan itself. Claude Security augments existing static analysis and dependency scanning. The deterministic checks stay in CI, and the model-driven scan covers the context-dependent vulnerabilities those checks are not built to find.


### Claude on call with Claude Tag

Incidents can also arrive via other means such as workplace communication apps, like Slack or Teams. Incidents can look like a 10pm Slack message for an urgent fix on an incident channel and can now be actioned immediately. Claude Tag (public beta currently available in Slack) makes Claude a member of those channels under its own identity, so each new incident gets a first responder and the response itself becomes part of the loop and memory for future incidents.

The conversation and institutional knowledge stay in the channel, with anyone in the channel able to guide and action the response. Any team member can test hypotheses, explore new options and investigate in real time with the channel history adding to the auditability. Through access to MCP Claude verifies the metric is back at baseline and confirms it in the thread, writes the post-mortem to a version-controlled lessons file that future investigations can read.

Incidents are not the only work Claude Tag picks up. Tagged on a ticket over MCP or asked in the channel, Claude triages the work the same way. A small, well-bounded fix arrives as a PR through the review gate, and anything larger is written up as intent.md for Stage 1: Plan, at which point the loop starts feeding itself. See: how Claude Tag runs on-call for CI/CD at Anthropic .


## Closing thoughts

Models and harnesses have become more advanced, allowing organizations to not just transform how they produce code, but the entire software development lifecycle.

This transformation keeps human judgement central to the process and considers the governance and regulation requirements of large enterprise organizations.

This guide consolidated many of the real best practices our Applied AI team executes on a daily basis for our customers, and we hope you found it a practical and actionable resource.


### Resources and acknowledgments

The documentation below is what a platform team needs to set those controls up, in roughly the order you would roll them out.

Thanks to Jim Blackhurst, Will Steuk, and Jamal Arif for their contributions to this guide, which was inspired by and built on much of their previous work.
