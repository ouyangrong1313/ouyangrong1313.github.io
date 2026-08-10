# 从 Prompt 到 Harness：企业级 Agent 工程的完整演进之路（Digest）

> **来源**：微信公众号「阿里妹」2026-07 推送（作者 储旭(槿柏) / 原文链接 https://mp.weixin.qq.com/s/xH4cyBJJJlG9cfcmSU5ztA）

## 一句话总结

> **裸 LLM = 高性能 CPU，缺操作系统**——企业级 Agent 必须从 Prompt → Context → Harness → Agent OS 完整演进，构建 L1-L5 五层认知操作系统。

## 速查表

| 维度 | 关键数字 / 公式 | 备注 |
|------|----------------|------|
| 上下文窗口 | 128K 物理 / 30K+ 有效 | 5 步技能 + 3 轮迭代 → 200K+ 字符 |
| 注意力稀释触发 | 第 8 步后 | 70% JSON / 20% 历史 / 10% 当前 |
| L1 触发 | >8000 字符 或 >10 数组元素 | 外置 MySQL + __refId |
| L2 触发 | >10000 字符 | temperature=0.3 LLM 蒸馏到 2000 字符 |
| L3 触发 | prompt_tokens / contextWindow >= 85% | 目标压缩到 30% |
| L4 预算 | 4096 字符 | 小数据全量 / 大数据 enhancedSummary |
| Transcript keepTarget | round(36 - steps × 0.8) | 5 步 ≈ 32 / 30 步 ≈ 12 |
| RecursionGuard | MAX_DEPTH=5 / MAX_CHAIN=20 | 同 skillId >=3 次拦截 |
| Agent 状态机 | candidate → shadow → probation → active → degraded → offboard | shadow 不生效仅记录 |
| 实际收益 | token -60%+ | Agent 从 8 步衰减 → 30+ 步稳定 |

## 反直觉点 3 条

1. **"LLM 越跑越蠢"是工程问题不是模型问题**：换更大的模型只是把天花板从第 5 步推到第 8 步，趋势不变；真正的解决方案是管理信息质量而非扩大物理容量
2. **工具设计有半衰期**：模型升级后旧的防御机制可能变成不必要的约束——好的系统设计应当能从模型进步中"免费"获益，因此可观测性先行，定期 review 防御是否仍必要
3. **信任建立不能跳过人工确认**：AI 准确率即使达 95%，剩下 5% 错误一旦直接写入数据库，用户会立刻失去信任。状态机必须有 shadow / probation 阶段，不能直接 active

## 借鉴动作（速查）

| # | 动作 | 当前 OpenClaw 状态 | 下一步 |
|---|------|-------------------|--------|
| 1 | OpenClaw 阶段定位（Prompt/Context/Harness/Agent OS 四阶段） | dispatch + Harness 达 S2 | 补 L2 执行账本 + L4 注意力经济 + L5 5 道门 |
| 2 | Payload 内禁用 send_qiwei_message 强约束 | 7/21 14:06 patch 已完成 | 观察 7/22 06:30 cron run 是否复现 |
| 3 | 五层修复管道 → parameterBindings 迁移 | 7/21 加了"输出前自检 Gate"（雏形） | 升级为可机器验证 schema（节点数 / 表格数） |
| 4 | 三层记忆状态机落地 | channel memory 当前是 State | 把"读 channel memory"升级为强制 Pinned step |
| 5 | 数据清洁优先（L1 外置触发） | 友盟/神策 JSON 未触发外置 | 加 L1 触发机制 >8000 字符 |
| 6 | 注意力经济 + 优先级队列 | 5 个 cron 失败通知都进 AI Wiki 群 | 按严重度优先级 + 日报聚合 |
| 7 | 5 大关键洞察提炼 | 待沉淀 | 写入 MEMORY.md + 反面案例库 |

## 备注与限制

- **作者背景**：储旭(槿柏)，阿里巴巴 Agent 平台 S1/S2 主导者
- **5 大关键洞察**：①"LLM 越跑越蠢"是工程问题 ②上下文管理分层防御 ③Action Space 必须治理 ④工具设计有半衰期 ⑤信任建立不能跳过人工确认
- **理论参考**：ReAct / Claude Code "Think Like an Agent" / Codex / OpenCode Session Compaction + McGregor X-Y / Deming 质量 / Thaler Nudge / Wittgenstein 语言哲学
- **未独立验证**：工具设计半衰期未给具体可量化指标；信任状态机 shadow → active 转换阈值未明
- **本文配套**：raw（80097 字节）+ wiki 编译页（≤8K）+ wiki digest（本文件，≤4K）
- **标签**：#主题/Agent架构 #主题/Harness工程 #主题/上下文管理 #主题/数据完整性 #主题/Action-Space #主题/企业级Agent #主题/Agent-OS #场景/Seetong借鉴 #作者/储旭 #公众号/阿里妹