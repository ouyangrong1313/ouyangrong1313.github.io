# 规范驱动开发：Notion 的 AI 工程工作流程 - Raw Digest

- 原文链接：https://mp.weixin.qq.com/s/3tD61I6xLWpjoOrF6goewA
- 来源：微信公众号 / Capihom（编译自 Latent Space《How I AI》播客，嘉宾：Notion 工程师 Ryan Nystrom）
- 发布时间：2026-06-08 22:00
- 获取时间：2026-06-09

## 一句话总结

**Spec-driven development 不是给团队平白多一层负担，而是把"原本就在做但停在会议等待区的设计文档"第一次变成 agent 的施工说明书和可执行工程资产**；Ryan 在 Notion 已经跑通"Whisper 说意图 → Codex 写 spec → @Codex 出 PR + 验证截图 → spec 进仓库做 change log"的完整流水线。

## 关键观点

1. **先说清楚，再写代码**
   - Ryan 写代码前先打开 Whisper 把"这个功能该怎么工作"一口气说出来
   - 语音交给 Codex → 写 spec → "Build it"
   - Prompt 里常挂一句："像给 5 岁小孩讲一样解释给我听"
   - 文档第一次真正开始驱动实现，"先说清楚"变成可复用的流水线

2. **AI 编程时代先要救 CI**
   - Afterburner 项目：把 Notion CI 时间压到当前的 1/4
   - 慢 CI 不再只是"工程师多等几轮"，而是"一次等待卡住整个验证回路"
   - 速度问题会直接变成 AI 采用问题
   - 大团队如果还没自己的 VM 策略和背景 agent 策略，现在就该补这堂课

3. **Standup prep 从手工抄状态变成自动汇总**
   - Notion AI custom agent：拉 24h Slack + 关闭任务 + 合并 PR + 昨天会议 + Honeycomb MCP 指标
   - 严格限权：只读项目数据库，不动全公司任务表
   - 输出格式 Ryan 事先写好（简短/有条理/带一点轻松）
   - 团队不再按人轮流念"我今天做了什么"

4. **20 分钟省下的，是反复切上下文的损耗**
   - 自动化真正消灭的不是 5 小时宏大叙事，而是会议前在 Slack/GitHub/任务表之间折返的认知切换
   - AI 没有替 Ryan 做战略判断，把最耗神的搬运活接走
   - 自动 prep 也是 burnout 保护——会议前整理最没成就感、最容易让人提前疲惫

5. **在 Notion 评论里 @Codex，10 分钟换 PR + 预览地址**
   - Boxy = 装好 Codex + Claude Code 的小型 VM 集群
   - 工程师不在本地拉环境，直接在任务评论里写需求/截图/边角
   - 案例：tab block 加 "copy link to tab"，4 句描述 + 1 张截图 → 10:40 开始 → 10:51 实现 → 10 分钟后 PR + preview
   - 关键：agent 附上自己的测试说明和 UI 验证截图（闭环跟着代码一起出现）

6. **Code review 新世界：先说"我听不懂"**
   - PR 评论里直接写"我不知道这里在干什么，这不太对"
   - 发给 agent 反而成了最有效的 debug——对方没介意，回了段解释并顺手修了
   - 故意把 prompt 写得很直白，逼 agent 把隐含步骤摊开
   - Codex 没有"嘿朋友我替你搞定了"的温柔语气，Ryan 反倒喜欢；code review 最稀缺的是把事情快速讲清楚
   - AI 没取消 code review，把它从社交阻力里拽出来

7. **Spec 进仓库，文档第一次成为可执行资产**
   - spec 不再是会议材料：写进仓库、带代码指针 + 行为说明 + 验证计划
   - 文档底部明确写 verification：测试怎么过 / CLI 怎么跑 / agent 怎么被拉起 / 应该看到什么结果
   - 进了版本控制 → 可回看演化 = change log
   - 配套 CLI：让 agent 在 ask mode 和普通模式之间切换 + 交互转录可复盘
   - 过去设计文档停在会议等待区，现在它们第一次变成工程资产

8. **工程师角色重构：系统思考者 + 架构师**
   - 重心从手工 plumbing 挪到"场景边界 / spec 写实度 / 验证回路 / agent 自证工具"
   - 如果验证还是模糊的，第一件该补的是让 agent 能自己跑起来的工具，再回头打磨 prompt
   - spec-first 没平白多一层负担——以前就在写，只是写完要排会、等 review、再实现
   - 文档从理论材料变成执行入口

## 7 角度 × 3 钩子（写作复用）

### 角度 1：范式（SDD / Spec-driven Development）
- 钩子 1：spec 不再是文档，是 agent 的施工说明书
- 钩子 2：spec 进版本控制 = change log
- 钩子 3：spec-first 不是新负担，是把"原本就在做"的事从会议等待区挪进仓库

### 角度 2：工作流（流水线与自动化）
- 钩子 1：Whisper→Codex→Spec→Build，10 分钟闭环
- 钩子 2：Standup prep 自动汇总，多界面折返被接走
- 钩子 3：@Codex 出 PR + 自带验证截图，闭环跟着代码一起出现

### 角度 3：瓶颈转移（验证 / 基建 / DevX）
- 钩子 1：AI 时代慢 CI = 一次等待卡住整个验证回路
- 钩子 2：VM 策略 + 背景 agent 策略是大团队的补课
- 钩子 3：工具基建 = 跑道；高频提交/验证/回滚都需要它撑住

### 角度 4：人机协作（Code Review / Prompt 心理）
- 钩子 1："我不懂"发给 agent 是有效 debug，发给人是社交灾难
- 钩子 2：Codex 直白语气 > Claude Code 温柔语气
- 钩子 3：承认"不懂"逼 agent 把隐含步骤摊开

### 角度 5：组织与角色（工程师价值迁移）
- 钩子 1：工程师 = 系统思考者 + 架构师
- 钩子 2：人继续写代码，但重心挪到 spec/验证/边界/自证
- 钩子 3：6~7 人小团队也能跑 AI-native 流程

### 角度 6：方法论（先说清楚 / Burnout 保护）
- 钩子 1：Whisper + "5 岁小孩" prompt = 摊开隐含步骤的入口
- 钩子 2：自动化消灭的不是时长，是反复切上下文的损耗
- 钩子 3：自动 prep 顺便干掉会议前的隐性疲惫

### 角度 7：可借鉴动作（今天就能试）
- 钩子 1：挑一段最重复的流程（standup 预读 / 评论触发 PR / 老设计文档改写为可执行 spec）先打通
- 钩子 2：先打通一小段，再把整条链路慢慢换掉
- 钩子 3：把 spec 放进 repo，改功能时先改 spec，再让 agent 回头改代码
