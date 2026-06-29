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
