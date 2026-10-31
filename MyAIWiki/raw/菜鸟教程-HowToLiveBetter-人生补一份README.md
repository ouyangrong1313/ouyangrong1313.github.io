# 本想在 Github 学技术，结果刷到了一份人生指南：612 条建议，给人生补一份 README～

- **原文链接**：https://mp.weixin.qq.com/s/-LN8NNb-9DYZielCJtgQ8g
- **公众号**：菜鸟教程
- **来源**：微信公众号，2026-09-30 推送（Unix 时间戳 1790652420）
- **获取方式**：curl + Chrome UA，提取 `id="js_content"` 区段，Python 正则清洗（去 script/style、去推荐）、截断「阅读原文」后内容
- **获取时间**：2026-09-30 14:45 Asia/Shanghai

---

## 正文（清洗后）

这两天看到刘欢老师去世的消息，挺感慨的，才 63 岁，不应该这么早。

每次看到这种消息，都会暗暗提醒自己，少熬点夜，有空多陪陪家人，别什么都等以后。

可过几天，又回到熟悉的节奏，项目赶着上线，饭随便吃两口，运动留到周末，周末只想躺着，嘴上说身体最重要，日程表里却一直排不上号。

不只是健康，租房时没细看合同，接外包时没查清业务，离职时才想起来了解自己的权益……很多生活常识，都是吃了亏以后才补课。

我们花了不少时间学怎么工作，却很少认真学过怎么照顾自己、处理生活里的麻烦。

最近刷到了一个特别的项目：HowToLiveBetter《高性价比人生指南》，整理了 614 条建议，涉及健康、时间精力、省钱、就业、租房等问题。

看着看着觉得，代码有 README，人生好像也该补一份，至少遇到事的时候，除了硬撑，还能知道先查什么、从哪里下手。

开源地址：https://github.com/eternity4719/HowToLiveBetter

PDF 版下载：https://github.com/eternity4719/HowToLiveBetter/releases/download/epub-latest/HowToLiveBetter.pdf

关注度很高：

每节内条目按性价比从高到低排列，正文按节拆成 33 个文件放在 book/ 目录。

每个章节的主要内容：

安装与运行检索页是纯静态的，README.md 和 book/ 就是它的数据，没有后端、没有数据库、不用装依赖。克隆并本地启动：`git clone https://github.com/eternity4719/HowToLiveBetter.git` `cd HowToLiveBetter` `python -m http.server 8000`

然后浏览器打开 http://localhost:8000/，也可以把整个目录丢给任意静态服务器（Nginx、GitHub Pages、对象存储）。注意 index.html 必须经 http 打开，直接双击本地文件会空白（浏览器禁止网页读本地文件），那种场景请用离线单文件版。

自己生成电子版：

```
cd tools/epub && npm ci && npm run build # EPUB
node tools/offline/build.mjs # 离线单文件 HTML
node tools/pdf/build.mjs # PDF，另需 pandoc ≥ 3.1 和 typst ≥ 0.13
```

产物都在 dist/。另外再推荐一份人生进阶指南，从英语学习出发，扩展到 AI 协作、项目交付、资源层创业与人生复盘。

Github 地址：https://github.com/byoungd/up/

PDF 下载：https://github.com/byoungd/up/blob/master/docs/public/downloads/life-level-up-guide-zh.pdf

Star 数 60k+：

早期主线是英语，现在扩展为一套可复用的方法论——发现问题 → 主动学习 → 与 AI 协作 → 完成真实任务 → 保存证据 → 复盘迁移。

每一部对应 docs/threads/ 下的一个 part 目录：

---

## 备注

- **标题与正文数字不一致**：标题写「612 条建议」，正文写「整理了 614 条建议」，以仓库实际为准（编译页按正文 614 记，并标注此差异）。
- **图片内容未展开**：原文 12 张图片承载了「关注度」「章节主要内容」「每个 part 目录」等列表信息，本文档未做 OCR，正文中对应位置为「关注度很高：」「每个章节的主要内容：」「每一部对应 docs/threads/ 下的一个 part 目录：」等引出语后直接接图片。
- **命令被压缩**：原文多处 shell 命令因微信排版被合并成一行（如 `git clone ... cd HowToLiveBetter python -m http.server 8000`），本文档已按语义拆回多行。
- **未独立核验**：仓库 star 数、建议条数、33 个文件等均为文章转述，未打开仓库逐项核对。
