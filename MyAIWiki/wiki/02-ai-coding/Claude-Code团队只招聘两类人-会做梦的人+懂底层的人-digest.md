# Claude Code 团队只招聘两类人：会做梦的人 + 懂底层的人 - Digest

- 原文链接：https://mp.weixin.qq.com/s/0Mcn6DAzVMBGSK6NMb5IZQ
- 来源：微信公众号 / 老章很忙
- 原始内容：Anthropic 官方博客 + 28 分钟视频演讲
- 获取时间：2026-06-04

## 一句话总结

**AI 时代工程团队最大的变革不是"用上 AI"，而是"杀掉旧流程"**——所有建立在"代码很贵"前提上的旧流程（SLA/设计 review/双周 demo/月度路线图）都失效。Claude Code 团队做了 5 件事：**JIT 规划 / Trust but Verify 评审 / 第一周 ship / 招两类人 / 扁平化组织**——**招聘只锁定会做梦的人 + 懂底层的人**，因为纯产出量已不稀缺，稀缺的是判断力和深度。

## 关键观点

1. **The Shift（瓶颈位移）**
   - 2000 年代：CD-ROM 装运 → 死硬截止日期
   - 互联网：在线分发 → 敏捷开发
   - Agentic Coding：写代码本身 → **验证/评审/安全**成为新瓶颈
   - "Coding rarely is the slow part anymore"

2. **Processes rarely kill themselves（流程很少会自己死掉）**
   - 反面例子：SLA 多到需要"SLA 优先级排序表"——给优先级排优先级
   - "什么 SLA 都重要 = 什么 SLA 都不重要"

3. **5 个改造动作**（按重要性）
   - **规划**：JIT 规划——不写 Design Doc，直接 prototype；让 Claude 跑三个 PR 替代会议室白板
   - **代码评审**：Claude 接 Style/Lint/PR 反馈/常见 Bug/加测试；人必审法律/信任边界/产品感
   - **入职**：新人第一周 ship 真代码
   - **招聘**：两类人——会做梦的人 + 懂底层的人；不看 commit 行数
   - **组织形状**：扁平化、Manager 必先做 IC、dogfood、统一 mission

4. **Trust vs Verify 的边界要随模型升级重定**
   - 今天必须人审的部分，下一代模型可能不需要
   - 每次发模型都要重新评估
   - **国内团队最容易忽略**：2024 年定的"必须人审清单"现在还还原封不动在用

5. **招聘只招两类人**
   - **会做梦的人**：Creative builder with product sense——好奇心、想做产品、愿为体验反复迭代
   - **懂底层的人**：Deep systems expertise——分布式系统、性能、底层基建
   - **不再看原始产出量**——纯产出已是模型的事，稀缺的是判断力和深度

6. **上下文获取的范式转变**
   - 老："Who made this change?" → 找作者
   - 新：**double click**——先问"这件事 Claude 能不能直接答？"

7. **Source of Truth：代码即真相**
   - Claude 翻代码直接给答案，不用维护永远滞后的文档
   - 老章补：对一般业务团队建议保留 spec，**check 进 repo** 让 Claude 直接对齐

8. **三个度量指标**
   - Onboarding 爬坡时间 ↓
   - PR Cycle Time ↓
   - Claude-assisted commit 比例 ↑
   - **冷水**：Don't confuse throughput with success

9. **大方承认还没想明白的 3 件事**
   - iOS/Android 还要不要分？
   - 自动化 review 边界？
   - 角色模糊怎么保证"专业感"？
   - **"我也还没想明白"的姿态比"已经全面 AI-native"可信 100 倍**

## 我的理解

- **跟 [[Claude-Code团队5条工作原则-Fiona-Fung分享]] 是同一团队的不同切面**——Fiona 侧重原则，本篇侧重动作
- **跟 [[陈春花-AI时代管理者重建判断权]] 是一体两面**——陈春花说"管理判断权不能外包"，本篇展示"Manager 必做 IC + 吃狗粮"是工程层的判断权接回
- **"the shift" 是最值钱的判断**——所有 5 个改造动作都建立在这一个观察上
- **国内团队最大盲区**：加了 AI 工具但旧流程不动
- **"会做梦的人 + 懂底层的人"** 对小团队特别重要——大厂可分开招，**小团队更看重 T 型**
- **"代码便宜后团队对齐文化更重要"**——这一句反直觉但深刻

## 适合关联的主题

- [[Claude-Code团队5条工作原则-Fiona-Fung分享]]
- [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]
- [[Claude-Code架构深度解读-Agent系统的真正护城河不在模型-而在-Harness]]
- [[HarnessEngineering企业级实战]]
- [[Harness不是目的-知识才是护城河：一个 AI 工程交付团队的知识沉淀实践]]
- [[AI-Coding的顿悟时刻]]
- [[陈春花-AI时代管理者重建判断权]]
- [[Harness工程AgentLoop]]
- [[Claude-Code在大代码库中的最佳实践]]
