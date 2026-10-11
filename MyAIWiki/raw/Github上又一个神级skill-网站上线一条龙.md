# Github 上又一个神级 skill ，网站上线一条龙。

**来源：** 微信公众号
**作者：** 开源日记
**日期：** 2026年9月29日 15:38
**链接：** https://mp.weixin.qq.com/s/snz6fkTaHa6qxuKVUz6G5g
**抓取方式：** playwright-chromium
**正文 SHA-256：** 7da945cc9fc927d72ae8ce1fcf80e26aa0e57a5e085fbfbf96aa012c861b9bc0

---

## 正文

大家好，我是熊叔，今天继续逛 GitHub。

现在用Claude、Codex来写一个工具，几分钟就可以跑起来了。

但是要让别人用的话就必须要部署到云服务器上。

真要上线，托管、数据库、环境变量、域名、邮件、支付这些东西，一个都绕不开。

AI 帮我操作没问题，但真到了生产账号，我还是不敢让它随便改。

最近我在 GitHub 上看到一个开源项目，叫 golive-skill。

它就是帮 Agent 把写好的项目，直接部署到你自己的云账号里。

为了看得更直观，我直接拿一个小项目跑一遍

我用AI写了一个网址缩短器，在本地已经跑通了。

以前到这一步的时候，我还要自己去Vercel上建项目、开数据库、配环境变量，最后再跑到DNS后台绑定域名。

现在有更加方便的方法。

安装好golive-skill之后，就直接对Codex说：

使用golive将该项目上线。

它首先进行detect，检测出项目用到了哪些框架、需要哪些服务。

然后进入到plan中，把要创建和修改的资源列出来。

确定之后再执行apply，处理部署、数据库、环境变量以及DNS。

最后再做一次验证，看下部署地址、域名和相关服务是否都正常。

整个过程就是：

detect → plan → approve → apply → verify


总结一下就是先做计划，再执行，最后再看结果。

我觉得它最值得看的有三个地方

01 上线的过程是可见的。

很多Agent部署项目的时候，只告诉你一句部署成功，中间改了什么不清楚。

golive-skill 会把要动哪个账号、改哪些资源都列清楚，哪一步出错了就停在哪一步。

执行的结果也会保留下来，之后想要检查或者清理的时候还可以继续进行。

02 当你要动账号的时候，它会先问你。

golive-skill 会先让你确认；比如修改DNS、删除资源、第一次上线生产，还会再单独询问一次。

如果计划有变化，那么之前批准的东西就无效了。

我可以让AI帮我干活，但是真的要动生产账号的时候，至少要先告诉我它准备干什么。

03 服务还是你自己的。

Vercel、Supabase、域名、Resend 和 Stripe 都是自己单独的账号，golive-skill 只负责将它们连接起来。

官方的README写得很直接：

No GoLive account, hosted backend or product telemetry.

也就是说，资源归你，GoLive 做操作。

它现在能干到什么程度

官方已经跑通过几条完整链路，比如 Vercel + Supabase、Netlify + Neon，DNS、Resend 邮件、Stripe 测试支付和 Supabase Auth 也都做过验证。

目前它最适合拿来部署个人项目、小应用和测试环境。

golive-skill 的 verify 会把结果分成 pass、fail、warning 和 skipped。

skipped 不算通过。

比如环境变量存在，不代表值一定正确；域名验证通过，也不代表邮件一定送到了收件箱。

能自动验证的它会检查，无法确认的地方直接列出来。

另外还有 golive status，可以只读检查之前创建的 DNS、环境变量、Webhook、数据库和托管项目有没有变化。

测试项目不用了，可以运行 golive teardown。

它只删除能够确认由自己创建的资源，删除前还要再次确认。

删不了的资源也会告诉你剩下什么，需要去哪里手动处理。

想试的话，装起来很简单

golive-skill 目前已经验证过 Codex 和 Claude Code，需要 Node.js 20+。

安装：


npx skills add https://github.com/mikehasa/golive-skill --skill golive --global


指定 Codex：

npx skills add https://github.com/mikehasa/golive-skill --skill golive --global --agent codex --yes


也可以走 npm：

npx golive@alpha install --agent codex


装完以后，在 Agent 里直接说：

用 golive 把这个项目上线。


第一次用，我建议先拿测试项目跑，别刚装完就把正式站点交进去。

到这里边界也给大家提提

它现在还是 Early Alpha，复杂云架构并不是它的强项。

golive-skill 只能约束自己的流程；如果 Agent 本身已经拿到了云账号权限，它仍然可以绕开 GoLive 直接操作。

本地凭据也是明文文件，只是对文件权限进行了限制，并不是系统钥匙串。

所以真正上生产的时候，我会把它当作一个有审批、有记录、有验证的上线助手，不会完全放手。

写在最后

我认为golive-skill最值钱的地方就是把Agent从“写完代码”推进到了“真正上线”。

代码写完，它继续帮你建数据库、配环境变量、绑域名，最后把项目送到线上。

有兴趣的朋友可以试试。

开源地址：https://github.com/mikehasa/golive-skill

平时我会持续分享一些有趣的开源项目，有兴趣的朋友可以关注一下。

回复关键词，可以找到你想要的项目。

---

标签： #主题/AI-Coding #场景/公众号长文
