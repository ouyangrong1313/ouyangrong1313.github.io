# 阿里妹·业务需求专家 Agent(摘要)

> 原文链接:https://mp.weixin.qq.com/s/9o_z-Poj9r4dbwe3NlC1pw | 作者:森叶(阿里妹) | 抓取:2026-06-15

## 一句话核心

**把业务需求从进入到结项的完整过程,组织成 Agent 能自主推进、人只在关键节点确认的闭环**——围绕 4 层横向架构(上下文输入 / 业务专家编排 / 工具执行 / 反馈学习)走完 8 步纵向流程(需求进入→澄清→方案→实现→CR 协同→验收→发布→结项沉淀)。

## 8 步流程 × 关键设计(精简)

| # | 阶段 | 主责 Skill | 关键设计 |
|---|------|-----------|----------|
| 3.1 | 需求进入 | superai-memories | **3 仓分离**(代码仓/项目记忆仓/长期 wiki 仓)+ **「不直接升级」**(过程材料留项目记忆,结项后才进长期 wiki) |
| 3.2 | 澄清(第一质量门) | superai-clarify | 结构化 requirements(目标/边界/验收/风险);**协作留痕到 Aone 评论** |
| 3.3 | 方案(第二质量门) | superai-plan + tjx-cli | 方案阶段就把"怎么验收"定清楚(HSF/SLS/监控);配置 schema 提前建好 |
| 3.4 | 实现 + 硬门禁 | superai-execute + superai-code-review | **TDD 反向**(测试先于实现);**pre-push git hook 硬绑 PMD + 覆盖率 + diff-to-test** |
| 3.5 | CR 协同 | superai-aone | Agent 主动读 unresolved 评论,改 → 新 commit → resolve;**评论最密在澄清/方案不在编码** |
| 3.6 | 验收 | superai-aone + superai-sls + superai-ops | **独立项目环境部署** + HSF/SLS/监控取证;**Agent 不会自动主预发/线上发布** |
| 3.7 | 发布 + 观察 | 复用 superai-sls + superai-ops | **上线是节点不是终点**;观察期无异常才进结项 |
| 3.8 | 结项沉淀 | superai-finish + superai-memories | **3 问蒸馏**:稳定知识(进长期 wiki)/ 流程改进(skill+prompt 候选)/ 一次性(归档);**每类需人工确认** |

## 5 条核心方法论 + 3 大现有问题

**5 条方法论**:①代码之外串联成本才是真瓶颈 ②「不直接升级」原则 ③质量门禁硬规则化(pre-push hook)④反馈留痕到平台(CR/issue/milestone 而非聊天框)⑤通用研发流程可复用(数据方向已复用同一框架)

**3 大现有问题**:①接入成本高(集团平台多只支持网页授权,未对 CLI 沙箱适配)②缺 Agent 效果度量体系(人工介入次数/方案返工率/验收一次通过率/回滚次数未量化基线)③单 Agent → Agent Team(共享 wiki 各自视角,**不按流程步骤机械切分,看真实需求**)

## 3 句核心金句

- "**业务需求专家 Agent,不是一个更聪明的代码生成器,而是把需求研发过程的上下文、工具调用、人工确认、验收证据和反馈沉淀组织成一个闭环**"
- "**质量门禁从'Agent 应该做'变成'不做就推不上去',是真正的工程化卡口,而不是靠提示词的自觉**"
- "**人不应该继续在每个需求里反复补位,而是把这些补位动作沉到系统里——Agent 缺什么,补什么**"

## 5 个对 Seetong / OpenClaw / MyAIWiki 可借鉴动作

1. **「不直接升级」→ 复用 MyAIWiki 的 raw/wiki 分层** —— raw 是项目记忆仓,wiki 是长期 wiki 仓,write-path 验证模板是蒸馏门
2. **质量门禁硬规则化 → 对应 [[Skill-Self-Evolution]] "验证 Gate 必填 + 失败自动回滚"** —— 后续 OpenClaw skill 自进化要把"硬规则(脚本/hook)"提到比"提示词"更优先
3. **结项沉淀 3 问 → 复用 [[seetong-tapd-version-review]]** —— 补"结项审计表"模板:稳定知识(进长期 wiki)/ 流程改进(进 SKILL.md 候选)/ 归档(进 raw)/ 待补证(回填清单)
4. **superai-* 命名体系 → 跟 Seetong `seetong-*` 对照** —— Seetong 已有 prd/bug-triage/weekly-report/requirement-clarifier 等,**但缺"按阶段编排"语义**;可补 clarify(澄清)/ plan(方案)/ execute(TDD 实现)/ finish(结项)4 阶段编排
5. **3 大问题 → Seetong 对应检查** —— ①接入成本:Seetong 平台工具(反馈/友盟/TAPD)是否都补齐 CLI/API?②度量体系:循环命中/误报/回滚/成本/证据 5 项指标有量化基线吗?③Agent Team:KMP 跨端天然适合"前端(KMP)/ 后端(SDK)/ 测试" 3 类 Agent 拆分

## 关联图谱(3 段)

- **上游(产业入门)→ 本文(阿里内部落地)→ 下游(Skill 形态)**:[[APPSO-Codex-Claude-Code-Loop-Engineering]] 4 人同向 → 本文 4 层 × 8 步 → [[Addy-Osmani-agent-skills-设计哲学]] 23 技能 + 7 块骨架
- **同级(Loop 主题 4 视角闭环)**:[[Addy-Osmani-Loop-Engineering]] 方法论原典 + [[Loop-Engineering-详解-把反馈循环放进工程现场]] 中文工程实操 + [[Agentic-Engineering-AI-Workbench]] 工作台 5 层视角
- **同级(组织/Harness 视角)**:[[Multica-AI-Native-组织-人是最慢的节点]] + [[清华沈阳-自进化AI新物种]] + [[从零设计生产级-Multi-Agent-Harness]] + [[make-for-agent-qi-shi-huan-shi-make-for-human]]

## 待补证

- 8 个 superai-* Skill 源码/实现细节未公开
- "独立项目环境部署"稳定性/成本数据未给
- "PD Agent / 数据专家 Agent"目前是规划还是已落地未明说
- 度量体系未给基线数据
- Agent Team 队长角色具体如何实现未展开
