# 原文摘要 - How to Build a Company OS in Claude Code

## 一句话总结

Aakash Gupta 采访 Laurel CPO Jiaona Zhang：**公司 OS = 把 1% AI 高手的操作沉淀成全公司都能调用的技能**；具体方法：① 工作地图 ② 从第一个烦人的重复动作开始 ③ playbook 拆成 skill ④ 入口留 Slack/邮箱 ⑤ AI Ops 专职岗位 ⑥ Captain model 精简 PM 团队。

## 核心观点（6 条）

1. **公司 OS（Operating System）**：把 1% AI 高手的操作沉淀成全公司都能调用的技能；公司 OS 已进入团队分工、招聘标准、PM 交付判断
2. **1% vs 90-99% 鸿沟**：1% 高度 AI 化用户 + 90-99% 不知道什么时候该用什么——公司 OS 让 1% 经验不锁在个人电脑里
3. **从第一个烦人的重复动作开始**："公司 OS 不一定一开始就是 OS，它从第一个自动化的小工作流开始"——第一块砖 = 不再漏信息的表单
4. **50 页 playbook 拆成可调用 skill**：Dust agent builder + GTM agent 路由；playbook 从静态文档变成可执行动作
5. **入口必须留在 Slack 和邮箱**："换界面的摩擦会杀死习惯"——演示惊艳但月底没人打开
6. **AI Ops = 新的 Biz Ops**："当你说它是每个人的责任，它最后就成了没有人的责任"——必须设专职岗位

## 关键事实 / 案例

| 关键事实 | 内容 |
|---|---|
| 采访者 | Aakash Gupta（硅谷知名 PM 播客主持人） |
| 受访者 | Jiaona Zhang（Laurel CPO / 前 Airbnb/Dropbox/Webflow/WeWork 产品负责人 / Stanford/Yale/Reforge 教产品） |
| 工具栈 | Claude + Slack automation + Dust agent builder + GTM agent 路由 |
| 公司结构 | 5 个 PM + 4 个设计师（精简）+ Captain model（每 feature 1 个 captain） |
| 工作地图 | GitHub 风格按职能拆分：customer success / data science / design / engineering / finance / legal / marketing |
| 招聘创新 | 候选人 screen share 现场展示怎么用 AI，4 级成熟度 |
| AI 成熟度 4 级 | 1) 聊天 2) 自动化一个工作流 3) 给自己搭 app 4) 做 shared app ship 给客户 |
| AI Ops 路径 | 1 个 Sasha 证明效果 → 每个部门都要自己的 AI Ops（GTM/product/finance） |
| 转折点 | CEO Ryan 在 LLM/AI 时代推动产品和公司转向 AI-native |

## 决策树 / 反直觉

- **如果公司只有 1 个 AI 高手** → 1% 经验锁在个人电脑里 = 浪费；要做"公司 OS"让 1% 经验变 99% 都能用
- **如果你的 playbook 是 50 页 PDF** → 没人真的会照着做；拆成 Dust agent + GTM agent 路由 = 可执行动作
- **如果你做 AI 工具但放在新界面** → 演示惊艳，月底没人打开；入口必须留 Slack/邮箱
- **如果 AI 改造是"每个人的责任"** → 实际是"没有人的责任"；必须设 AI Ops 专职岗位
- **如果 PM 不愿意 ship 代码** → PM 能力跟不上工具变化；招聘 screen share 60 秒看出 4 级成熟度
- **如果你认为 AI 时代 PM 101 已经过时** → 错了；速度变快后 PM 101 反而更硬

## 核心金句（5 条）

1. "你有那 1% 的 AI 用户，也有剩下 90% 到 99% 不知道什么时候该用什么工具的人。"
2. "公司 OS 不一定一开始就是 OS，它从第一个自动化的小工作流开始。"
3. "基本原则从未改变，甚至比以前更重要；彻底改变的是工具和你的工作方式。"
4. "很多时候，当你说它是每个人的责任，它最后就成了没有人的责任。"
5. "一个 PM 现在能做的事比以往任何时候都多，但同时，真正具备这些技能、判断和好奇心的人并不多。"

## 关联图谱

### 上游（基于 / 来自）
- Aakash Gupta 硅谷 PM 播客
- Jiaona Zhang 个人 30 年产品经验
- Reforge AI leadership 课程（每 6 个月开一次）

### 下游（应用于 / 验证于）
- Seetong 团队：4G IPC 研发 / 客服 / 产品 各部门工作地图体检
- Seetong AI 助手：从 1 个最烦人的重复动作（工单分诊 / 反馈归类 / 工时记录）开始
- Seetong 招聘：技术岗 screen share 现场展示怎么用 AI
- Seetong 组织：是否需要 1 个 AI Ops 专职岗位？

### 同级（横向 / 并列）
- **[[陈春花-从岗位到角色-AI时代组织设计的新逻辑]]** - 03-productivity 已有组织管理主线
- **[[与AI一起做产品的六条原则]]** - 03-productivity 已有 AI 时代产品设计
- **[[use-ai-well-become-more-valuable]]** - 03-productivity 已有"用好 AI 的人更值钱"
- **[[APPSO-Obsidian+Codex-Karpathy同款本地知识库]]** - 本地知识库 3 层结构
- **[[Nikesh-Arora-模型过剩与记忆护城河]]** - 06-ai-tech 已有"硅谷 CEO 战略视角"
- **[[章文龙-AI分身时代-在场重新定价]]** - 06-ai-tech 已有 AI 时代哲学反思

## 备注与限制

- 本文是 Aakash Gupta 播客采访的中文总结版，原视频 YouTube 链接 https://www.youtube.com/watch?v=qsDX0PMKcaE
- 与 [[陈春花-从岗位到角色-AI时代组织设计的新逻辑]] 区别：陈春花是从岗位到角色的组织设计哲学（中文），本文是"公司 OS"具体方法 + 4 级 AI 成熟度招聘（英文播客翻译）
- 与 [[与AI一起做产品的六条原则]] 区别：六条原则是 AI 时代产品哲学原则，本文是 PM 实操方法 + 团队组织变化
- **未展开**：Laurel 公司其他 AI 工具栈的细节 / Dust vs Claude vs 其他 agent builder 的对比 / JZ 教 PM 101 的具体课程内容
- **重要**：本文是"组织管理 + 团队 AI 化 + PM 实操"三合一文章，挂在 03-productivity 而非 06-ai-tech 更贴切（核心是生产力方法 + 团队协作，不是 AI 行业战略）