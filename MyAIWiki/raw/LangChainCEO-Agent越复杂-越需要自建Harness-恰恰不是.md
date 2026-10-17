# LangChain CEO：Agent 越复杂，越需要自建 Harness？恰恰不是

**来源：** 微信公众号
**作者：** DataFun
**日期：** 2026-08-22
**链接：** https://mp.weixin.qq.com/s/KHVwdqr8aWR9gcH_ZzqQPQ

---

## 正文

导读
Agent 做不好，最直接的反应往往是换模型。推理不够强，就换更大的；工具调用不稳定，就换更新的；Coding Agent 表现不好，再找一个 Coding 更强的模型。
但 Harrison Chase 在这场关于 Agent Harness 的分享里，给出了另一种判断。在 LangChain 的拆分中，一个 Agent 由 Model、Context 和 Harness 三部分组成：模型负责生成与推理，Context 是模型当前拿到的信息，Harness 则负责组织整个运行过程，让固定信息、动态信息、工具结果和外部反馈在合适的时间进入模型。Harrison 对 Harness 的概括很直接：它最主要的工作，是在正确的时间把 Context 带给模型。
主要内容包括以下几个部分：
1.
自建 Harness，不是看 Agent 有多复杂
2.
Agent 出错，问题可能不在模型
3.
Harness 开始进入持续优化闭环
图 1｜Harrison Chase 在分享中讨论 Evals 与 Harness。来源：演讲视频画面
01
自建 Harness，不是看 Agent 有多复杂
今天大部分 Agent 的底层结构并不复杂：请求进入模型，模型生成结果；如果需要调用工具，就执行工具，再把结果返回给模型，继续下一轮，直到任务结束。Harrison 认为，大量 Agent 仍然建立在这个基本 Loop 上。不同 Harness 的差别，主要在于给这个循环加入什么：文件系统、Sandbox、Memory、Sub-agent、Summarization、Context Offloading，以及 Hooks、Plugins 和 Middleware。Context 太长，可以在模型调用前先摘要；工具返回内容太多，可以先卸载部分信息；工具调用前后，也可以插入额外的检查和控制逻辑。核心 Loop 没有改变，改变的是对执行过程的控制方式。
因此，Harrison 并不建议所有团队一开始就搭一套复杂 Harness。他更倾向于先从通用 Harness 开始。现在的模型和通用 Agent Harness 已经能够覆盖大量基础任务，等业务场景逐渐明确，再按需要加入 Gates、Checks，甚至更具体的 Cognitive Architecture。真正决定定制程度的，是 Distribution：如果任务与模型已经熟悉、训练过的大量任务接近，现成 Harness 往往就能工作得很好；越偏离这一分布，越需要调整 Harness。
但任务整体超出模型熟悉的分布，并不意味着 Harness 里的每一部分都应该重写。Harrison 用 Legal AI 举例：完整的法律任务可能不在模型最熟悉的分布里，但“编辑文件”仍然是模型已经大量接触过的能力。不同模型在各自 Harness 中编辑文件的方式并不完全相同，这些方式又可能是模型更熟悉的交互模式。于是更合理的做法是，业务层可以定制，但模型已经熟悉的局部能力尽量保持与模型匹配。LangChain 在 Deep Agents 中加入 Model Profiles，就是为了根据不同模型切换相应的文件编辑实现。
这说明模型和 Harness 并没有完全解耦。支持多个模型，也不只是替换一个 API。Custom Harness 真正要解决的是：哪些环节应该按照业务重新设计，哪些环节应该保留模型已经熟悉的运行方式。
02
Agent 出错，问题可能不在模型
如果 Distribution 回答了什么时候需要改 Harness，接下来更实际的问题是：Agent 表现不好时，到底应该改什么？Harrison 把一次 LLM Call 出错的原因概括成两类：一种是模型本身不够好，另一种是模型收到的 Context 不够好。而他的判断是，更多时候问题来自第二种。
这意味着，Agent 最后的错误输出可能只是结果，真正的问题早在前几步就已经发生：模型没有拿到正确文件，工具结果没有进入 Context，之前的信息在摘要时丢掉了关键内容，或者错误信息被继续带进后续调用。如果只盯着最终答案，很容易把 Context 或 Harness 的问题误判成模型能力问题。
所以 Agent 的 Observability 不能只记录最终结果，而需要看到完整执行轨迹：每一步模型收到了什么 Context、调用了哪些工具、工具返回了什么，这些信息又是怎样逐步进入模型上下文的。只有把这条轨迹还原出来，才能判断真正需要调整的是 Model、Context 还是 Harness。
03
Harness 开始进入持续优化闭环
这也是 Harrison 后半场重点讲 Evals 和 Observability 的原因。一个真正进入业务的 Agent，最终需要自己的 Benchmark，用同一批任务去比较不同模型、不同 Harness，甚至不同 Reasoning Effort 的实际表现。评测也不能只看 Accuracy，Latency、Token 和 Cost 同样需要一起衡量。
当 Benchmark、Trace 和 Feedback 连在一起，Agent 优化就形成了一个闭环：运行 Agent、收集 Traces、找出问题、运行实验、修改系统，再重新评测。被修改的并不只有模型，Harness 可以通过 Harness Engineering 调整，模型可以 Fine-tune，Context 也可以通过 Memory 等机制继续变化。
图 2｜持续改进闭环：Monitor → Build → Test → Deploy。来源：演讲相关展示图示
LangChain 已经开始尝试让 Agent 自动参与这个过程。Harrison 展示的 LangSmith Engine 本身就是一个 Agent，它可以读取大量 Traces，寻找共性问题，生成 Issue，关联对应 Trace 作为证据，再进一步提出修改 Prompt、Context，甚至 Harness 代码的建议。
图 3｜LangSmith Engine 对 Trace 中的问题进行聚类、关联证据并提出修复建议。来源：演讲相关展示画面
更有意思的是，LangChain 还会用 Benchmark 比较不同模型和 Harness。Harrison 提到，他们曾发现 Codex 会主动写很多小脚本分析 Traces，而且这种方式表现很好，于是团队又把这种行为吸收到 Engine 自己的 Harness 中。Harness 因此不只是开发阶段搭好的一套框架，而开始成为可以根据真实运行数据持续调整的系统。
模型越来越强，通用 Harness 的确会覆盖更多基础任务。但当 Agent 真正进入特殊业务，问题会逐渐从“模型能不能做”变成“模型应该怎样做”：它应该看到哪些 Context、使用什么工具、哪些步骤允许自主执行、哪些步骤必须受到控制，以及失败之后如何追溯和改进。Harrison 提到，一些金融服务客户面对高度自主的通用 Agent 时，担心的并不是能力不够，而是系统过于不可控，因此更希望采用可预测、可约束的定制架构。
所以，判断是否应该自己做 Harness，真正值得问的不是“这个 Agent 有多复杂”，而是：你的任务离模型已经熟悉的世界有多远。越接近模型熟悉的任务，越可以依赖通用 Harness；越深入垂直业务、特殊流程和强控制场景，越需要重新设计模型外面的运行系统。而当 Agent 出现问题时，也不必第一时间换模型，先看模型这一轮究竟拿到了什么 Context，以及 Harness 是怎样把这些信息送进去的。
本文整理自：
Harrison Chase (LangChain CEO)公开演讲
往期推荐
OpenAI 开源 Codex Harness：Claude、Google、DeepSeek 都押注了同一层
让Data Agent自己进化：人民大学张绍磊提出Data–Ontology–Agent协同进化框架
Palantir开始给Agent算“工时”了：企业Agent正在进入可观测时代
资本开始买“语义层”了：Graphwise 获控股投资，AI Agent 的新基础设施正在成形
Palantir开始给Agent算“工时”了：企业Agent正在进入可观测时代
VeloxCon China 2026定档12月5日，议题征集全球同步启动！
Palantir把Claude、OpenAI和Google的Agent接到了Ontology之上
DeepSeek Harness被谷歌盯上：Agent下一战场，开始从模型转向系统
Agentic Search 2.0：从单轮对话到企业级 AI 搜索自动驾驶 Agent
走进腾讯滨海大厦：探索AI搜索在Agent时代的范式跃迁！
点个
在看
你最好看
SPRING HAS ARRIVED

---

标签： #主题/AI-Agent #主题/Harness工程 #场景/公众号长文 #节点/任务分布 #节点/Context诊断 #节点/Trace闭环
