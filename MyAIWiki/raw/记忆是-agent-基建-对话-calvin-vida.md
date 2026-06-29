# 记忆，是 Agent 基建｜对话 Calvin@Vida

**来源**：微信公众号 - 赛博禅心
**链接**：https://mp.weixin.qq.com/s/VZUhUo-ppqpICzbbGgCpbA
**作者**：金色传说大聪明
**日期**：2026年4月26日

---

## 正文

PRODUCT

虽然 AI 越来越聪明，但每次对话，你都得补充一堆东西
让 AI 记住你说过什么不难，但让它记住你做过的事儿很复杂
记忆这个东西，已经从产品功能逐渐变成了 Agent 基建

以上内容，来自我和 Calvin 的对话

北京时间4 月 21 日，OpenAI 给 Codex 上线了记忆功能，叫做 Chronicle，让它知道你刚才在看什么、两周前在做什么项目
[Codex 凌晨更新，将屏幕内容「放进记忆」](https://mp.weixin.qq.com/s?__biz=MzkzNDQxOTU2MQ==&mid=2247515836&idx=1&sn=58e032bf3a4c8755c05b89906bd2af2a&scene=21#wechat_redirect)

但是呢...这套东西仅面向 Pro 订阅的用户，也只给 mac 用户提供

一天后，4 月 22 日晚上，一个叫 OpenChronicle 的项目出现在 GitHub 上，提供了相同的开源实现，并在当天冲到了 X 的 today's news trending 第一

```
github.com/Einsia/OpenChronicle
```

Calvin 是这个项目的负责人之一，清华的 00 后，主要方向是 Proactive Agent

昨天下午，我和他聊了一个小时，本文为记录

对了，Calvin 的语速很快，虽然只聊了一个小时，但我俩聊了两万字

在对话前，我问 Calvin：为啥大家开始弄记忆了？

Calvin 说：以前模型能力太差，记不记得住影响都不大。但现在，随着 OpenAI、Claude 新一代模型的发布，乃至国内开源模型的追赶，模型之间的差距逐步缩小，真正影响用户使用体验的将是模型拥有的关于用户的记忆与 Context 多少

我们目前在做 Proactive Agent 的研究，核心要实现的，便是 Memory 和 Context。我们想要研究清楚，怎样记，记什么，才能让模型表现更好。我们关心的不只是怎么让现在这些擅长使用 LLM，擅长写 Prompt 人群用的更"爽"；我们还关心怎样让那些描述不清楚需求，不擅长使用 LLM 的群体用的更"轻松"。

记忆，让人与 AI 的交互，从无状态变成有状态，从有负担变成无负担，本文由此开始

## 把记忆，放回你的电脑

Chronicle 是 OpenAI 给 Codex 开发的记忆功能，为 Pro 订阅用户提供差异化的服务，通过记忆绑定提高高价值用户的迁移成本

OpenChronicle 是能够独立处理、保存用户记忆的 AI Infra，从处理用户上下文获得并保存 Memory，到给 Agent 使用都不与任何一个模型及 harness 强绑定。用户可以使用本地部署的模型处理 Memory 来保护隐私安全，也可以让 Claude、Codex、OpenCode 等任何具备 tool-Using 能力的 LLM 及 Agent Harness 接入这一系统发挥更大作用。

在 Calvin 的设想中，Agent 记忆的所有权，应该归属用户，而不是模型厂商

记忆该是设备里的一层基础设施，跟谁的模型协作都行

## AX Tree 优先

讲到「让 AI 看屏幕」的技术实现，我的第一反应是「截图保存 & OCR & RAG」，毕竟很多项目，包括 OpenAI 的，都是这么做的

然后我去翻阅了下 Open Chronicle 的代码，他是 AX Tree 优先

AX Tree 这个东西我没用过，就让 Calvin 去解释了下：

AX Tree 是 macOS 系统层的一个老接口，本来给残障辅助技术读屏用，把屏幕上的内容，做成一棵结构化的树状描述

当前打开的是哪个应用、焦点在哪个输入框、你正在编辑什么文字、网页 URL 是什么、按钮上写着什么字，AX Tree 直接给文本，不用走视觉

我们也想过纯走视觉，但算账之后还是觉得 AX Tree 这条路更扎实，至少在 mac 上是这样

跟截屏比，AX Tree 这件事有三个好处：

- 一是便宜，文本的处理成本远低于图片
- 二是更准，对意图信号的识别比 OCR 强很多
- 三是结构化且轻量化，存进数据库、做检索都更方便

我追问说， AX Tree 有什么短板？

Calvin 说，AX Tree 在 Word、飞书这类应用里，由于内部的渲染绕开了系统辅助通道，所以通常只能读到顶栏菜单和文档标题，无法以来 AX Tree。正应为如此 OpenChronicle 是个混合方案，AX Tree 优先，截图兜底

还有就是，OpenChronicle 的截图基于触发器，光标运动、页面滚动、应用切换才会触发处理。如果你打开 macOS 什么都不动，记忆系统不会每 5 秒拍一张图回去喂模型。避免你在看电影这种场景下，记忆频繁触发导致 Token 过量消耗与记忆污染

## Token 账：50 美分 vs 3 美金

当意识到有如此多屏幕内容的时候，我就不得不好奇了：Token 账怎么算？

具象一点来说，对于 8 小时工作日，纯静默记录、不主动调用的轻度工作，要消耗多少 Token？

"差不多 50 美分/天"，Calvin 这么说，然后又补充道：如果是高频调用、深度交互的重度场景，一天 3 到 5 美金

当然了，OpenChronicle 允许用户接入本地模型，所以如果你的电脑够强，其实...所需要的就是电费：
[在笔记本上，部署 gpt-oss-120b 模型](https://mp.weixin.qq.com/s?__biz=MzkzNDQxOTU2MQ==&mid=2247503516&idx=1&sn=d54671d03a4f4fb0b889680a5e9465c3&scene=21#wechat_redirect)

Calvin 顺嘴讲了他自己的使用习惯。他是 ChatGPT Pro 200 美金套餐的常年用户，平时把 Session Memory 全关了，因为 GPT 用着用着经常跨话题串台

Chronicle 出来他第一时间试了，Codex 效果还行，但日常 Workflow 那种凌乱场景里就跟不上了

Claude 的记忆在 General 层次上管得最稳，基本不会互相串台，但 Claude 的 Memory 也就只在 Claude 里有效

## 记忆，从「你说过什么」到「你怎么做事」

我接着问 Calvin：OpenChronicle 跟现在市面上 AI 产品已有的 Memory 功能，差在哪？

Calvin 的判断是，今天市面上 AI 产品的 Memory 量已经不缺，缺的是跨产品的连贯，上下文全靠手动维护，换个项目就要重新跟 AI 解释一遍你是谁、你在做什么、你之前的判断是怎么形成的

OpenChronicle 选的是另一种结构，把 mac 所有上的应用操作都进同一个本地记忆池，按 7 个分类扁平存成 Markdown 文件，分别对应你这个人、你的项目、你常用的工具、你关心的话题、你联系的人、你工作的组织、你经历的事件。对外通过 MCP 这个标准协议暴露成工具调用，Memory Layer 不再绑在某个产品里

Claude Code、Claude Desktop、Codex、OpenCode 都已经有一键集成的配置示例。意思是，你在 Cursor 里做的设计决策、在飞书里跟同事讨论的架构方向、在 Slack 里收到的需求反馈，可以在另一个对话窗口里被 Claude Desktop 直接承接

OpenChronicle 通过 MCP 协议跟各类 Agent 协作

记住你说过什么，是 AI 的认知层，而记住你想怎么做事，是 AI 的行动层，需要理解你在不同场景下的偏好、惯性、潜规则，要难得多：

比如，当你跟 AI 说「加个日程」的时候，这个日程是被放在飞书日程里，还是放在 Apple Calendar？

## 「我们在掀桌子」

聊到一半，我问 Calvin：今年许多团队，都在讲记忆叙事，然后去融资，那么你们为啥选择把这个东西开源？

Calvin 说：

掀桌子...然后看看谁能在场景里给出 Best Practice

搞记忆这个事情，Calvin 他们从去年底就开始做了，然后我就好奇，当看到 OpenAI 发 Chronicle 的那一刻，他第一反应是什么

Calvin说，第一秒确实有点慌，怕 OpenAI 一口气把所有场景都吃下来。但仔细看完文档和实测之后，发现 Codex 这种相对干净的环境里效果可以，到日常 Workflow 那种凌乱环境就还有距离

与此同时，记忆正在从「某个产品的差异化功能」逐渐变成「Agent 时代的基础设施」，Cursor 的记忆、Claude 的记忆、ChatGPT 的记忆，都按各自产品视角组织。OpenAI Chronicle 把这件事往前推了一大步，但是碍于商业却仍将记忆圈在自己的应用里

插入个题外话，据我所知，这次也不是 Calvin 他们第一次跟 OpenAI 撞车了

哈哈哈哈哈哈哈

## 回到 Calvin 自己在做的事

聊完工程细节和行业判断，话题滑回到 Calvin 自己，他所带领的 Vida 团队真正在研究的，是基于这套基础设施之上的主动式 Agent

Calvin 也给我解释一下「主动式」：现在大部分 Agent 是 reactive 的，你不问它就不动。主动式 Agent，能根据你的 context 主动判断、主动建议、主动行动

具体到场景，Calvin 跟我聊到他们在做的事，是把这套记忆能力跟具体的 Workflow 缝合起来。代码中断后恢复、跨文档协作、设计稿修改延续、长期个人知识沉淀。Agent 真正进入你的日常作息，需要的就是「我知道你怎么做事」这一层支撑

Agent 应该服务于人，去放大人的能力，不能让你变成各家厂商手里的资产，被争夺上下文，被争夺注意力

各家大模型厂商都在争夺用户的上下文，毕竟用户用得越多，Memory 越完整，迁移到别家的成本越高

OpenChronicle 这种本地优先、模型无关的开源路径，是希望记忆属于用户、可以接到任何 Agent 或者设备上

最后我问 Calvin，如果有了 Proactive Agent，它能服务谁？

Calvin 说：所有人

打通世界的记忆、同步现实的节律，让人更自由的去创造

如果你对他们这个方向感兴趣，可以在 Github 上找到更多的信息，地址在这里：

```
github.com/Einsia/OpenChronicle
```

---

#主题/AI-Agent #手法/权威背书 #场景/技术博客
