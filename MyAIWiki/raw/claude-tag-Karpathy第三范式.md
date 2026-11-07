# Karpathy：大模型交互的第三种范式来了？这是不是夸大其词

## 原文信息
- **作者**：逛逛（猜测，待确认）
- **公众号**：逛逛 GitHub（猜测，待确认）
- **发布日期**：2026-06-24
- **原文链接**：<https://mp.weixin.qq.com/s/tDAFqGgFoXgFplyfFj-pXg>

---

Anthropic 上线了 **Claude Tag**，一种让团队在 Slack 里直接和 Claude 协作的方式。给它开放指定频道，连上你选好的工具、数据甚至代码库，然后频道里任何人都能 `@Claude`，把活儿丢给它，自己去忙别的。

> [视频：官方演示]

用法和 Claude Code 一脉相承：用大白话 `@` 它提需求，它把任务拆成几个阶段，逐个用手头的工具完成，干完在 Slack 线程里把成果回给你。它能写或合并 PR、跑数据分析、帮忙定位线上故障的根因。

![配图](https://mmbiz.qpic.cn/sz_mmbiz_jpg/rY5icXvTTrJibuQFApo6774Gibdia8dQAyF0q49ZB7rgDibEwibgxhtxwgKpwlaf032t5YS8tj4rHT7haYoMJXmZRHaht4usfLYj9xKFns3AFNs)

几个新东西值得说：

1. **多人协作**：一个频道里只有一个 Claude，所有人都能看到它在做什么，谁都能从上一个人停下的地方接着聊。
2. **上下文积累**：它会随频道积累上下文，不用每次从头解释。
3. **ambient 模式**：打开后它会主动出手，跟进那些冷掉没结论的线程，从各个频道和工具里捞出它觉得你该知道的信息。
4. **异步**：派完任务你就能去忙别的，它甚至能给自己排日程，连着几小时几天独立推进一个项目。

![配图](https://mmbiz.qpic.cn/mmbiz_jpg/rY5icXvTTrJ8FZsQ6aZha7HFUlsfwqfF2SIILPVXiaibibmTbbat2l02ecwLBswCbLaQHySmNKTFnSFiamtgibeJcO0Bq3MPAibTqvbGIPcC18KkHI)

权限是按频道隔离的。管理员指定模型在哪些频道能用哪些工具和数据，记忆也只在对应频道里有效。**销售那套不会把记忆传给工程那套，工程师也碰不到销售的数据**。管理员能设 token 花费上限，能查到 `@Claude` 做过的每一件事以及是谁让它做的。

Anthropic 给的数据是，**内部版本现在贡献了产品团队 65% 的代码**，而且这套用法已经从工程扩散出去，被用来追产品指标、处理工单、查疑难 bug。Claude Tag 今天起对 Claude Enterprise 和 Team 用户开放 beta，跑在 Opus 4.8 上，会替换原来的 Claude in Slack 应用。

---

## Karpathy 的评价：大模型 UI 的第三次大改

平心而论，这个功能并不是很新奇，很多产品已经是这么做了，比如抖音里的豆包，或是公众号里的元宝，但 **Karpathy 转发时却给了个很高的评价**，他认为这是大模型 UI 的第三次大改：

> **第一种范式**：大模型是个你要去访问的网站。
> **第二种范式**：你下到电脑上的 App。
> **第三种范式**：一个自洽的、持续在线的、异步的实体，带着全组织的工具和上下文，和人类团队并肩干活。

他说要花点时间才能转过弯来，但它确实管用。

---

## 评论区争议

评论区没全顺着夸。

1. **价值观不可调教**：这个新同事的价值观、文化和品味是 Anthropic 设定的，而且故意做成用户没法调教的。一个你没法用职级压、用社交压力影响的同事，这和 Slack 里其他人确实不一样。
2. **归属权问题**：Claude Tag 是以厂商 agent 的身份进你的频道，而本地化的同类方案跑在你自己的硬件上、走你自己的 API，两种所有权模型差得远。
3. **开源替代**：开发者直接推荐 **openclaw** 这类开源版本，理由是别把公司的记忆和上下文锁死在一家实验室，迁移成本会比换 SaaS 贵十倍。

不过，这一功能有了大厂大咖的背书，会消减很多原本的决策困难，相信很快你的通信录里会多一个这样的"数字员工"。

更多信息见 Anthropic 官方说明 <https://www.anthropic.com/news/introducing-claude-tag>

关注公众号回复"进群"入群讨论。

---

标签： #主题/AI-Agent #主题/ClaudeCode #主题/Slack #主题/异步协作 #主题/开源替代 #手法/产品发布 #手法/权威背书 #手法/对比冲突 #场景/公众号长文 #场景/产品介绍