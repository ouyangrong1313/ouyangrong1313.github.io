# LangChain CEO：Agent 越复杂，越需要自建 Harness？恰恰不是 - 拆解

- 原文链接：https://mp.weixin.qq.com/s/KHVwdqr8aWR9gcH_ZzqQPQ
- 来源：微信公众号「DataFun」；整理自 Harrison Chase（LangChain CEO）公开演讲
- 发布与获取：2026-08-22

## 核心观点

1. **Harness 的职责是 Context 编排**：在正确时间将固定信息、动态信息、工具结果与外部反馈送入模型，不等同于另造一个复杂 Loop。
2. **定制由任务分布决定**：任务越偏离模型已熟悉的交互与工作分布，越需要业务化 Harness；复杂度本身不是判断标准。
3. **局部保留模型熟悉的交互**：即使业务整体需要定制，文件编辑等模型已熟悉的局部能力也不应随意重写。
4. **先诊断 Context 再换模型**：大量失败源于缺文件、工具结果未进入上下文、摘要丢失关键信息或错误被持续传递。
5. **Harness 需要进入优化飞轮**：Trace、Benchmark、Feedback 和实验相连，才能比较模型、Context 与 Harness 的真实效果。

## 关键结构与原文句

| 层 | 作用 | 首要问题 |
|---|---|---|
| Model | 生成与推理 | 能力是否不足？ |
| Context | 当前可见信息 | 是否拿到了正确证据？ |
| Harness | 运行过程编排 | 信息何时、以何种控制进入？ |

- “在正确的时间把 Context 带给模型。”
- “自建 Harness，不是看 Agent 有多复杂。”
- “更多时候问题来自 Context。”
- “不要只盯着最终答案。”
- “运行 Agent、收集 Traces、找出问题、运行实验、修改系统，再重新评测。”

## 对 Seetong 的借鉴动作

1. 按“接近模型熟悉任务 / 垂直业务偏移 / 强控制”给 Agent 场景分级，再决定复用还是定制 Harness。
2. 每次失败先回放 Context：输入文件、工具参数、返回结果、摘要和错误是否完整进入下一轮。
3. 保留模型擅长的文件编辑与工具交互模式，只在业务规则、权限、审批和状态层扩展。
4. 为报警分诊、设备诊断等关键流程记录结构化 Trace，并以真实任务建立 Benchmark。
5. 将准确率、时延、Token、成本和人工接管率一同纳入回归，不以单次模型效果替代系统评测。

## 关联图谱

- [[01-ai-agents/WorkBuddy-Harness工程复盘-从模型到可用Agent]]：从产品实践补充 Tool、Skill、Context、Harness 与 Loop 的分层。
- [[01-ai-agents/Agent评测漫谈-由浅入深讲解Agent评测]]：把 Trace、任务评测和回归基础设施落到评测体系。
- [[01-ai-agents/阿里云开发者-淘宝主播Agent的Harness工程实战]]：以六元组补充 Context 管理、生命周期 Hooks 与评测接口的工程实现。

**证据边界**：本文为 DataFun 对公开演讲的二手整理；LangSmith Engine、Model Profiles 和客户案例的细节未独立复现，不能据此推断所有模型或场景的最佳 Harness 策略。

标签： #主题/AI-Agent #主题/Harness工程 #场景/公众号长文 #节点/任务分布 #节点/Context诊断 #节点/Trace闭环
