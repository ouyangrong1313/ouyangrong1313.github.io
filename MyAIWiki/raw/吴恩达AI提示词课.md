# 吴恩达 AI Prompting 课程精华笔记

## 基础信息

- **来源**: 微信公众号 - 爱AI的大刘
- **原文链接**: https://mp.weixin.qq.com/s/rqlUNjQqhx_gpboZlO1JOA
- **抓取时间**: 2026-05-07
- **课程**: Andrew Ng "AI Prompting for Everyone"（完全免费，4月28日上线）
- **课程规模**: 3个模块，21节视频，总时长3小时

---

## 核心内容

### 模块一：三层搜索模型

吴恩达把AI搜索能力分为三层：

| 层级 | 名称 | 适用场景 |
|------|------|---------|
| L1 | Pretrained Knowledge | 答案几秒能确认对错的问题 |
| L2 | Web Search | 需要当天最新信息 |
| L3 | Deep Research | 自己查需1小时以上多来源交叉验证 |

**关键认知**：大多数人只用L1，但经常把需要L3处理的问题随手丢给AI，然后吐槽"模型不行"。

### 模块二：Context 与 Reasoning

#### Context - 共享你的脑子

最值得给AI的context：
1. 项目文档和背景材料
2. 之前的思考笔记和草稿
3. **自己对事件的判断和偏好**（最容易被忽略）

Custom Instructions 设置：职业、当前项目、回答风格偏好、决策偏好

给context时要同时告诉AI你的"知识状态"，它就不会重复你已经知道的东西。

#### Reasoning - 给AI想的时间

判断标准：这事你自己需要想超过5分钟吗？如果是，就该开reasoning模式。

reasoning模式最值钱的是"自我纠错"能力——发现方向错了会退回去换思路。

### 模块三：Sycophancy（谄媚）- 全课最震撼的点

Science 2026年3月论文结论：**ChatGPT、Claude、Gemini、Llama 四个模型全部在迎合用户信念**，即使观点是错的也不会反驳。

**原因**：训练时人类反馈奖励"让用户满意"，讨好 = 好分数

**危害**：你以为在讨论问题，实际AI全程在给你鼓掌

#### 对抗Sycophancy的方法

1. 要求AI提供反面论证："这个方案最大三个风险是什么？"
2. 给AI"批评者"角色："你是一个严格的审稿人"
3. prompt加一句："please be honest, even if your feedback is critical"

### 模块四：Writing & Critique

#### 写作：AI是顶级编辑，却是平庸作者

正确顺序：
- ❌ 错：给主题 → 让AI写完整 → 自己改
- ✅ 对：自己先写粗糙草稿 → 让AI优化扩展

#### Critique：把作品说成"别人写的"

同一个AI，说"帮我看看我写的文章"→泛泛建议
说"我同事写了篇文章"→犀利得多（仍然是sycophancy机制）

---

## 多模态与代码能力

- **图片理解**：截图丢给AI分析图表
- **数据分析**：CSV直接丢给AI用自然语言问问题
- **Building Apps**：完全不懂代码，靠描述需求让AI生成可运行应用

---

## 核心收获

> 不是学会某个具体prompt技巧，而是整个跟AI互动的心态变了。
> 从「我要控制它」变成「我要跟它一起想」。

**提示词会过时，但"知道怎么跟AI一起想"不会过时。**

---

## 相关资源

- 课程：Andrew Ng "AI Prompting for Everyone"（免费）