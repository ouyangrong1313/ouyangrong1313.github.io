# Better Harness 开源了：立即把 Harness 专家带进你的 AI Coding 工具

- 原文链接：https://mp.weixin.qq.com/s/PuMpxU1ruXlTgT_JWKoHfQ?scene=1&click_id=8
- 来源：微信公众号「phodal」
- 作者：phodal
- 发布时间：2026-07-28 21:28
- 获取时间：2026-07-30
- 一手项目：https://github.com/QoderAI/better-harness
- 原文清洗：保留正文、链接和图片占位，移除公众号页面导航与交互元素。

---

## 正文

上周，我们在 Qoder Desktop 中内置了 Better Harness。上线后，很多用户都在问：这个功能会开源吗？

答案是：会！

今天，我们正式开源 Better Harness。

项目地址：

https://github.com/QoderAI/better-harness

Better Harness 是一套面向 Coding Agent 工作流的开源分析与持续改进工具，将 Harness Engineering 与 Loop Engineering 的工程实践、评估模型和运行能力连接起来，并适配 Claude Code、Codex、Qoder 和 Cursor。

四个平台共享同一套判断模型，但会话分析、证据覆盖和输出能力尚未完全对齐。其中，Qoder 已在真实开发工作流中反复验证，是当前能力最完整的参考实现。

[图片：各平台安装或加载 Better Harness]

完成对应平台的安装或加载后，都可以在要分析的项目中执行：

/better-harness

你可以先让它跑起来，边看报告，边继续读这篇文章。如果某类证据不可用，Better Harness 会在结果中保留这个边界，而不会用配置数量或其他平台的数据替代它。

### Better Harness 关心的是 Agent 在任务中做了什么

假设 Agent 修改了一个模块，运行一条测试命令后便宣布任务完成。真正需要判断的，不是仓库“有没有测试”，而是这条测试是否与改动相关、是否覆盖主要风险，以及结果能否支持交付。

Better Harness 因此不会把 AGENTS.md、Rules、Skills、MCP、Hooks、Memory、测试或 CI 的存在，当成它们已经在任务中发挥作用。每条待优化项（Finding）都需要给出可追溯的证据、具体的用户影响、最小修复边界，以及修复后的验证方式。

下面是 Better Harness 在 Codex 中对自身项目进行的一次分析快照：

[图片：Codex 中的分析快照]

图中没有把“缺少 Codex 宿主测试”直接写成“Codex 已经失败”，而是保留未执行宿主测试的证据边界。分数只帮助定位问题，真正重要的是结论、影响、最小修复范围和验证方式。

这也是 Better Harness 与配置清单的区别：配置清单告诉你项目拥有什么；Better Harness 关注这些能力是否真正支持 Agent 完成了一次可信的任务。

而要让报告中的判断能够被检查、修改和重新验证，开源就不能只停留在一个可执行入口。

### Better Harness 的三层开源体系

如果只是把 /better-harness 的 Prompt 放到 GitHub 上，它当然也可以被称为开源。

但对 Coding Agent 来说，真正决定结果的从来不是某一句提示词，而是提示词背后的整套工作方式：什么值得检查，什么证据才算数，怎样形成判断，以及这些判断如何在真实项目中持续运行和修正。

[图片：Better Harness 三层体系]

因此，这次 Better Harness 开放的是三层彼此连接的内容。

#### 第一层：Harness Engineering 最佳实践

它回答的是：面对 Session、CLI、可观测性、Rules、Skills、MCP、Memory、Hooks 和自动化，我们应该检查什么，又有哪些结论不能仅凭配置存在就得出。

这些知识按照问题领域被组织在 references 中：

[图片：references 目录]

Better Harness 不会在每次运行时加载一个无限膨胀的总 Prompt，而是根据当前发现的问题，读取对应领域的判断依据。遇到诊断问题时进入可观测性实践，遇到 Skill 问题时进入 Skill Review，发现重复流程时再判断它是否应该由 Skill、Hook、Script 或 Automation 长期承载。

#### 第二层：Agent Work Loop 评估模型

它负责把工程实践转化为可以逐项检查的问题，并约束证据、评分与结论之间的关系。当前模型和证据状态定义公开在 Agent Work Loop 中。

鉴于标准尚未成熟，我们避免让单个模型主观定义“好的 Harness”。首轮内部评测选取 30 个 GitHub 真实项目，由四类模型基于 OpenAI 的 Harness Engineering 文章独立评估，生成 120 份标准化报告；随后通过跨模型对比和人工校准，明确证据要求、判断边界及项目类型差异，并应用更新准则对全部项目重新评估。

[图片：评估模型校准流程]

这条“自动评测—自动汇总—人工校准—自动复跑”的闭环，帮助我们得到第一个可复现、可持续调整的 Harness Engineering 评估模型。

第一版模型仍然更接近传统的软件工程成熟度扫描，关注项目是否拥有文档、测试、CI 和安全机制。但我们很快发现，静态资产不能证明 Agent 真正完成过一次任务。

为了持续追踪模型与项目能力的变化，我们采用 Spec 驱动的方式建设 Better Harness。随着 200 多份 Spec 的积累，模型逐渐从关注“仓库里有什么”，转向判断“任务中实际发生了什么”。

评估对象由仓库或会话，收敛为一个具体的任务；会话不再是评估对象，而只是承载证据的容器。模型也逐步稳定为五个维度：任务理解、可控执行、改动验证、可靠交付和经验沉淀。文件存在、配置数量、时间相邻，甚至一次命令成功，都不能再被直接推导为某项能力已经真正生效。

最终，Agent Work Loop 不再是一张静态评分表，而是一套围绕真实任务、能够复现并持续校准的判断系统。

#### 第三层：可运行的工程实现

它负责让前两层不只停留在文档和模型中，而是能够在真实项目里重复运行。Better Harness 通过插件或 CLI（项目 scripts 目录下的 JavaScript 代码）启动一次分析，先冻结任务范围，再分别采集三类证据：

- Session Evidence 还原 Agent 在真实任务中的行为；
- Project Harness 检查项目是否可启动、可诊断、可验证和可恢复；
- Agent Customize 检查 Rules、Skills、MCP、Memory 和 Hooks 的配置、路由与使用证据。

三类证据在采集和分析阶段保持独立，最终才由 Lead 结合 References 中的判断依据和 Agent Work Loop 评估模型进行综合判断。因为“项目拥有一项能力”和“Agent 在任务中真正使用了它”，始终是两个不同的事实。

[图片：三类证据到统一分析的架构]

最终输出的不只是一个分数，而是一组带有证据边界、用户影响、修复范围和验证方式的 Findings。报告经过渲染和校验后，可以继续进入修复流程；如果发现稳定的重复工作，则通过 Loop Engineering 判断它应该由 Skill、Hook、Script、Automation 或其他机制长期承载。

修复完成也不等于流程已经改善。只有在后续同类任务中再次观察到更好的结果，改进闭环才真正成立。

### 现在，从第一条可验证的问题开始

#### Qoder 用户

Qoder Desktop 已内置 Better Harness，更新到最新版即可，打开 Quest 视窗选择 Better Harness（Beta），或者直接运行 /better-harness。Qoder CLI 和 JetBrains 插件在装过 Qoder Desktop 的机器上同样直接可用。

#### 开源仓库

访问 Better Harness 的 GitHub 仓库：

https://github.com/QoderAI/better-harness

按照 README 安装并运行第一次 /better-harness。诸如 Claude Code 用户可以依次执行：

- /plugin marketplace add QoderAI/better-harness
- /plugin install better-harness@better-harness

然后运行：

/better-harness 分析我项目的 Harness 情况，生成 HTML 报告

第一次运行 Better Harness，不必立即构建一套完整的 Agent 工程体系，也不必追求满分。更实际的方式，是先找到一个证据明确、影响具体，并且能够快速验证的问题。

它可能是一条 Agent 找不到的检查命令，一段无法提供下一步诊断路径的错误日志，也可能是一个已经存在、却从未进入任务路由的 Skill。

修复一个问题，重新运行检查，再观察后续相似任务是否发生变化。Harness Engineering 不是一次性的配置工作，而是持续让项目更容易被 Agent 理解、执行和验证。

[图片：Better Harness 改进循环]

### 欢迎来给 Better Harness 贡献

Better Harness 已经在 Qoder 的真实研发流程里反复运行和校准过，但当前模型主要来自我们熟悉的项目类型和任务场景。

面对不同的技术栈、工程规模、团队约束和 Coding Agent，它仍然可能存在判断盲区，也需要更多真实证据来持续修正。

如果你愿意参与，可以从以下几个方面贡献：

- 补工程实践：往 references/ 里加一份某个语言、框架或者常见工作流的判断依据。不用写代码。
- 补评估视角：往 models/ 或 scripts/ 里加一个有证据支撑的检查维度或检测器，带上 fixture 和测试。
- 补宿主支持：为另一个 Coding Agent 补齐证据采集与验证，仓库的 Roadmap 里有现成的待办清单。
- 补真实案例：往 case-studies/ 里贡献一个脱敏的团队实践例子。

如果你不认同报告里的某一条 Finding，也热烈欢迎直接开 issue。对我们来说，一条来自真实项目的反驳，比一个 star 有用得多。

项目地址：

https://github.com/QoderAI/better-harness

标签：#主题/AI-Agent #主题/Harness #主题/Loop-Engineering #主题/AI-Coding #节点/Agent-Work-Loop #节点/任务证据 #节点/Findings #场景/开源项目 #场景/公众号长文
