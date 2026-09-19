# 这个 GitHub 有意思啊，Claude Code + Obsidian = 知识库王炸

## 原文信息
- **作者**：逛逛
- **公众号**：逛逛 GitHub
- **发布日期**：2026-06-23
- **原文链接**：<https://mp.weixin.qq.com/s/kV7eDR0SxbhiYViT90GDiA>

---

Karpathy 2026 年 4 月在 GitHub 上贴过一条 gist，标题叫 LLM Wiki。

不详细介绍了，之前提过。

![配图](https://mmbiz.qpic.cn/sz_mmbiz_png/M2ibDBMdECU0AaezNqPhZLg1uozd2sZNI5L7PGibQud5hbjvFy5DPzC4JGcTwicBEp4ibKTIINUkO6Ur2myLCzv8fl65ryNcYswfr0ROL7Fpe2U)

大意是说，理想的知识库就该让 LLM 自己来读、自己来链接、自己来维护。

你把资料丢进去，模型负责把碎片组织成一张互联的知识网，问问题时它从这张网里抽答案，而不是从训练数据里凭印象编。

这思路当时刷了不少屏，我也用过很多基于该思路的软件。

那个 gist 帖子的底部评论区就有很多方案。

![配图](https://mmbiz.qpic.cn/sz_mmbiz_png/M2ibDBMdECU1Ujhxf3zT0vwe0zrickeerdjj7QR24RUxp2UgwpbVickxf6B7LnibGUQq8klqb5rWflNiaKdS3s2eLUeAS6RAMrngVZrzfr197Ldg)

我最近用的比较多的，是一个叫 claude-obsidian 的项目。

也是对 Karpathy 这个理念的实践。

我用起来感觉这个很对味儿。现在这个项目差不多 7200 多的 Star。

## 01 开源项目简介

丢进去任何来源，比如网页、PDF、代码、聊天记录、YouTube 视频笔记，Claude 自己读完、抽概念、建链接、归档进一个完整的 Markdown 知识图谱里。

你问问题，它答的不是训练数据，是它自己读过、自己整理过的笔记。

![配图](https://mmbiz.qpic.cn/mmbiz_png/M2ibDBMdECU0Wugj7Bl2J2VQLle6Libtmf70pG6DNceVpVRy6TwbnhUcl0006j7T93hficJ2SH6agqAN7vCibIeN4j0bT4THRv6IHN0Tblphv7E)

作者反复用一个词：compounding knowledge，知识复利。

每一份资料丢进去都会被整合进现有的网络，越用越值钱，越问越聪明。这个心智模型跟普通 AI 笔记插件完全不在一个频道。

底子就是 Karpathy 那篇 LLM Wiki gist。

> [视频：项目演示]

claude-obsidian 更像是一个知识引擎。

**它会自动整理笔记。**

你丢进去的每份资料，它会自动建出实体页（人物、机构、项目）、概念页（理论、模式、方法）、来源页（原始材料），并且自动建立双向交叉引用。

**它会矛盾检测。**

笔记里互相冲突的论点它会发现，标出来并附上来源。

**它有会话记忆。**

每次会话结束会自动更新 hot.md，下次开局不用从头交代背景。

**支持 8 类健康检查。**

它把孤儿笔记、死链、过期声明、缺失引用全列出来。你的 wiki 会自己保持健康，不用每周手动清理。

**数据完全自主。**

全是本地 plain Markdown 文件，没有数据库，没有云端，没有订阅费。

![配图](https://mmbiz.qpic.cn/sz_mmbiz_png/M2ibDBMdECU0bJ297Xn6XBMbo5KlibH9KYREE1qNf0h5KGv991rI71GjmdmSFr37GIufH1g4ZaWRh0YK0nian13hE9iaL0YnoicAcHcaTUgEqIEg)

## 02 装起来很简单

**方式 1**：git clone 仓库

```bash
git clone https://github.com/AgriciDaniel/claude-obsidian
cd claude-obsidian
bash bin/setup-vault.sh
```

然后用 Obsidian 打开这个文件夹，再开 Claude Code 进同一个目录，输入 `/wiki`，它会一步一步带你跑起来。

setup-vault.sh 会自动配好 graph view 的颜色、过滤规则、CSS snippet，开箱即用。

**方式 2**：作为 Claude Code plugin 安装

```bash
claude plugin marketplace add AgriciDaniel/claude-obsidian
claude plugin install claude-obsidian@agricidaniel-claude-obsidian
```

安装完，会创建一个文件夹（大概率 `claude-obsidian`），用你的 Obsidian 打开这个文件夹就行。然后会问是不是信任，点击信任仓库作者并启用插件就行了。

![配图](https://mmbiz.qpic.cn/sz_mmbiz_png/M2ibDBMdECU1x60c4D7Zjic9lOzXabMFAHmbV6mU0Dft8IMNaAeKKLj3ibmsZicwYjFMV2bMx8aEB3uPJwGvFqmxmbSjHAtc8gg7CVzvr7zLkN8)

然后还有一个弹窗，让这几个预装的插件都打开就行：

- **Calenda**：右侧栏多一个月历视图，每个日期下面显示当天写了多少字、有没有未完成的 task，点日期直接跳到那天的 daily note。回看自己笔记产出节奏很直观。
- **Thino**：类似 flomo 的快速备忘录面板，随时弹出输入框写一句话灵感，自动归档到一个统一笔记里。后面可以让 Claude 把 Thino 里的速记批量 ingest 进 wiki。
- **Excalidraw**：Obsidian 内嵌的手绘画布，可以画流程图、白板、给图片加标注。
- **Banners**：给笔记顶部加一张 header 图，类似 Notion 的 cover。

![配图](https://mmbiz.qpic.cn/mmbiz_png/M2ibDBMdECU3h0VK5I8zMcISiaPpak39zrdGwzOzrDUibkNoJNAJVNwC8iaXrykt3icnNeibntCdmcolFkmich2SaYy8K3aHpwCx3gTQ3gFsoalJxg)

然后打开新终端，进入刚刚创建的那个目录，运行 Claude Code：

```bash
cd ~/Documents/claude-obsidian
claude
```

在那个 Claude Code 会话里输入 `/wiki`。

它会问你，这个知识库是用来做什么的，然后帮你搭出完整的 wiki 结构：`index.md` / `hot.md` / `log.md` / `dashboard` 等。

![配图](https://mmbiz.qpic.cn/sz_mmbiz_png/M2ibDBMdECU0VAibYvvNW3MNmmZBO6icOgjJM3IblYy3PSIWAuVAAzXZia7zYTk6ziatN2CWX94ibcKQsXnAibbYrnALa6JH9cxOibXvfNDz3rxqG18)

![配图](https://mmbiz.qpic.cn/sz_mmbiz_png/M2ibDBMdECU3v2OEukV5H64iaeOaTXabb61v2ibQngJcaUXpibhpZc9hItaQkZv6SdZTfu5NRibjjlNormQHZLmRNey0EWdoicDKEF8BED1RfiacfA)

## 用起来是这种感觉，日常使用的几个核心动作

- **丢东西进去**：把网页链接、PDF、视频笔记丢到 `.raw/` 目录，跟 Claude 说一句"吸收一下这些知识"，它读完会自动建出实体页、概念页、来源页，更新索引和 log。
- **问问题**：直接问"你对 X 怎么看？"，它会按 `hot.md → index.md → 具体页面` 这个顺序读，保持 token 成本可控，回答时引用具体页面而不是凭印象编。
- **健康检查**：`lint 一下`，孤儿笔记、死链、过期信息、缺失引用全列出来。你的 wiki 会自己保持干净。
- **可视化**：`/canvas` 命令打开可视化画布，可以把图片、PDF、笔记卡片摆上去做思维地图。这个画布符合 Obsidian 的 JSON Canvas 1.0 规范。
- **跨项目复用**：在任何 Claude Code 项目的 `CLAUDE.md` 里加一段引导，就能让那个项目读这个 vault 当知识库。你的执行助理、编程项目、内容创作流水线共享同一份知识。

这才是真正的第二大脑，不只是 Obsidian 里那个软件，是你所有 AI 工作流背后的公共记忆。

笔记越攒越值钱，越问越聪明。这种正反馈一旦跑起来很难回去。

如果你已经在用 Obsidian，这玩意儿值得花一个下午试试。

**相关链接**：

- 开源地址：<https://github.com/AgriciDaniel/claude-obsidian>
- 作者博客深度文：<https://agricidaniel.com/blog/claude-obsidian-ai-second-brain>
- Karpathy 原始 gist：<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

## 03 关注逛逛 GitHub

这个公众号历史发布过很多有趣的开源项目，如果你懒得翻文章一个个找，直接关注微信公众号「逛逛 GitHub」，后台对话聊天就行了。

---

标签： #主题/AI知识库 #主题/Obsidian #主题/ClaudeCode #主题/第二大脑 #手法/产品种草 #手法/工具安利 #场景/公众号长文 #场景/开源项目