# 图工程（Graph Engineering）来了？LangChain说不是新东西 - Digest

> 抓取来源：微信公众号「AI工程化」2026-07-23 18:39 推送
> 作者：winkrun
> 原文链接：https://mp.weixin.qq.com/s/_uUffN2JEgASnLQNfDWSDw
> 获取时间：2026-07-27 Asia/Shanghai
> 原文主题：把“Graph Engineering”从新词热度拉回工程判断，回答 Agent 图怎么画、什么时候该用图、什么时候该让 Harness 接管

---

## 一句话总结

**Graph Engineering 不是比 Prompt / Loop / Harness 更“新”的东西，而是把 Agent 的真实依赖关系显式画出来：只有下一步真的读取上一步输出时，边才成立；能预画路径的任务用图，路径本身需要探索的任务用 Harness。**

## 核心观点（5 条）

1. **图工程是拓扑显式化**：Prompt / Context / Harness / Loop 背后一直在处理同一件事，只是现在把依赖关系单独画出来了。
2. **线性 Agent 常常是退化图**：如果下游不消费上游结果，就不该为它保留边和等待。
3. **稳定图靠契约**：节点要有输入、输出和单一职责，边要表达数据依赖，路由尽量代码化。
4. **生产图通常有环**：重试、补问、验证回修和人工恢复，本质都是循环。
5. **图和 Harness 是分工关系**：可预画路径用图；路径需探索用 Harness。

## 关键结构

- **判定句**：下一步是否真的读取上一步输出？
- **3 个关键模式**：并行 / 钻石拓扑 / 验证器节点
- **3 个补充机制**：条件路由 / 循环直到收敛 / 模型分层
- **选型边界**：可预画路径用图；开放探索用 Harness
- **6 个即用场景**：安全扫描 / 深度研究 / 模块移植 / diff 审查 / 定时扫描 / 未知规模发现

## 5 个对 MyAIWiki / Seetong 可借鉴动作

1. **并行判定前置**：把“下游是否真的读取上游输出”做成多 Agent 并行前的第一问。
2. **节点返回统一契约**：子 Agent 输出统一走 JSON Schema 或结构化 Markdown，减少自由文本污染。
3. **钻石拓扑优先复用**：研究、审查、迁移类任务优先用 fan-out / reduce / synthesize，而不是一条长链。
4. **验证器独立成节点**：review / critic / validator 不要内联在主 Agent 里，让它们成为可复用的显式节点。
5. **开放探索别强上 DAG**：深度研究、未知规模发现和开放式排障要有 Harness / Loop 入口，不要一开始就把边画死。

## 关联

- **上游**：[[0xCodez-Agent-Harness-14-Steps]] / [[Lilian-Weng-Harness-Engineering-自我改进]] / [[Claude-Code动态工作流-让AI自己写Harness-这事靠谱吗]]
- **下游**：[[从零设计生产级-Multi-Agent-Harness]] / [[WorkBuddy-Harness工程复盘-从模型到可用Agent]] / [[阿里云开发者-淘宝主播Agent的Harness工程实战]]
- **同级**：[[Loop-Engineering-验证才是瓶颈]] / [[未来属于垂直领域Agent]] / [[多Agent使用边界与并行判定]]

## 备注与限制

- **文章来源结构**：这是公众号解读稿，混合了 LangChain 官方博文、Codez 图工作流文章和作者评论，不是单一一手原文直译。
- **最有价值的增量**：不是“Graph Engineering 是新东西”，而是那句很能落地的判定句和“图 vs Harness”边界。
