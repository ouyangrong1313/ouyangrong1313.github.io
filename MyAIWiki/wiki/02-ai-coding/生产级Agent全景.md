---
title: 生产级 Agent 全景:架构、Harness 工程、组织与人才
author: 叶小钗(微信公众号同名,成都 TGO 7 组组长)
date: 2026-07-13
slug: 生产级Agent全景
category: 02-ai-coding
tags: [Agent全景, Harness, AI原生组织, 人才招聘, Workflow矩阵, 企业转型]
rating: ⭐⭐⭐
source_wechat: https://mp.weixin.qq.com/s/rZEqIQR-RcNBWMH_9xq2bw
source_topic: 上月为某企业 6 场生产级 Agent 系统性培训理论部分整理
digest: "[[生产级Agent全景-digest]]"
related:
  - "[[叶小钗-AI原生组织方法论-2026版]]"
  - "[[AI-团队协作-Loop-SDD]]"
  - "[[0xCodez-Agent-Harness-14-Steps]]"
  - "[[Lilian-Weng-Harness-Engineering-自我改进]]"
  - "[[WorkBuddy-Harness工程复盘]]"
  - "[[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]]"
  - "[[Multica-AI-Native-组织-人是最慢的节点]]"
  - "[[Capihom-AI-Native企业-Agent团队和AI-Factory重写公司体系]]"
---

# 生产级 Agent 全景:架构、Harness 工程、组织与人才

> 微信公众号「叶小钗」2026-07-13 推送
> 作者 叶小钗(成都 TGO 7 组组长,研究 AI 原生 + Loop 工程 + Harness + 员工蒸馏)
> 原文链接:https://mp.weixin.qq.com/s/rZEqIQR-RcNBWMH_9xq2bw
> 原文主题:上月 6 场生产级 Agent 系统性培训理论部分整理

## 核心命题

**企业让 Agent 长期、稳定地完成有价值任务 = 架构线 + 业务线 + 组织线 三线合一** —— Agent 是企业软件的"认知与行动层",Coding Agent 是早期优势场景,Workflow/Agent/Knowledge 三选一靠决策矩阵,人才招聘看 4 维度。

## 8 节点 + 关联图谱

### 节点 1:企业软件三层架构

Agent 不是替代 CRM/ERP,而是在 **用户入口与交互层 + 业务记录层** 之间新增一个 **认知与行动层**。Agent 接到任务后做 6 件事:理解意图 → 组织上下文 → 判断工具 → 调用系统 → 检查结果 → 写回业务系统。

价值双指标:**完成多少任务 + 完成任务有多大价值**(不是聊天次数 / 工具调用次数)。

### 节点 2:Coding Agent 是早期优势场景

为什么 AI Coding 率先跑通 Agent?4 个天然条件:
- 上下文清晰(代码/依赖/配置/文档全在仓库)
- 工具天然存在(终端/文件系统/编译器/Git)
- 验证机制完整(编译/测试/运行结果)
- 恢复成本低(Git diff/版本/回滚)

Manus 用 CodeAct 思路 → Codex/Claude Code 扩到通用工作 → Coding Agent 是观察通用 Agent 演化的窗口。

### 节点 3:Workflow vs Agent 决策矩阵

横轴 = 业务知识专业程度;纵轴 = 工具数量/行动次数/循环推理次数。

| 业务知识 ↓ / 行动复杂度 → | 低 | 高 |
|---|---|---|
| 通用 | 自动化脚本 | **通用 Agent**(Deep Research / Coding / 办公) |
| 专业 | **知识工程**(本体 + Skill + 知识图谱) | **业务型 Agent**(金融/法律/医疗/客服) |

补充:固定流程且异常少 → 直接 Workflow,不进决策矩阵。知识图谱不强制用图数据库,MySQL 也可保存对象/属性/关系/Action。

### 节点 4:Agent 产品形态选型

- **垂直能力 → 嵌入成熟产品**(CRM 客户分析 / 项目需求拆解 / 客服回复建议)
- **通用能力 → 独立 Agent 产品**(多部门统一任务入口,Web / 桌面端 / CLI 三入口)

判断标准:**服务已有业务 → 嵌入**;**服务多部门 / 统一任务入口 → 独立**。

### 节点 5:企业 AI 转型 4 阶段

1. **单点试用** —— 个人用 ChatGPT / Copilot
2. **工具集中** —— 内部 AI 平台 + 知识库 + Skill 管理
3. **多 Agent 协作** —— 跨系统任务 + 业务 Agent 协作
4. **AI 原生组织** —— 流程重构 + 人/Agent 协作模式

提效主体从个人 → 团队 → 跨部门 → 组织。

### 节点 6:AI 原生组织 3 变化

- **取消中层** —— AI 承担信息中转,决策权前移一线 + Agent
- **评价体系转变** —— 从过程指标(聊天次数/调用量)转结果指标(任务完成 + 价值)
- **跨部门沟通** —— Agent 代理部门间沟通,减少会议 + 信息传递损耗

### 节点 7:Agent 人才招聘 4 维度

- **基础素质**:聪明(学习速度)/ 乐观(投入意愿)/ 皮实(失败恢复)/ 自省(复盘)
- **专业能力**:P5 功能 / P6 模块 / P7 产品 / P8 产品线 / P9 创造业务;**P9 需要"平地抠饼"能力**
- **业务能力**:客户是谁 / 谁在赚钱 / 商业链路 / 共性需求 vs 高度定制
- **组织能力**:推动项目 / 处理冲突 / 获得资源 / 管理预期

### 节点 8:生产级 Agent 三线合一闭环

- **架构线** —— Agent Loop / Harness / Tool / Skill / Context / Memory / 任务调度 / 治理机制
- **业务线** —— 真实任务 Pipeline,输入/输出/责任人/交付标准/异常处理
- **组织线** —— 人与 Agent 职责划分,岗位边界 / 协作方式 / 评价体系 / 人才要求

闭环:**找到业务问题 → 搭持续交付系统 → 沉淀 Tool/Skill/Pipeline/评测集 → 组织反复使用**。

### 关联图谱

**上游(本文论点的来源)**:
- [[叶小钗-AI原生组织方法论-2026版]] —— 同作者叶小钗 7-07 篇,AI 原生组织 3.0 公式是本文基础
- [[AI-团队协作-Loop-SDD]] —— 同作者更早 SDD 篇
- [[0xCodez-Agent-Harness-14-Steps]] —— Harness 落地骨架 14 步

**下游(本文论点的应用)**:
- [[Lilian-Weng-Harness-Engineering-自我改进]] —— Harness OS 类比(理论框架)
- [[WorkBuddy-Harness工程复盘]] —— 产品视角 Harness 一体化

**同级(横向 / 关联)**:
- [[Datawhale-Claude-Code之父的老板-Fiona-Fung-Agent协作方法]] —— Anthropic 实证
- [[Multica-AI-Native-组织-人是最慢的节点]] —— AI 原生组织极端样本
- [[Capihom-AI-Native企业-Agent团队和AI-Factory重写公司体系]] —— Groupon 实证

## 正文要点(8 条 = 主张 + 案例 + 操作)

| # | 主张 | 案例 | 操作 |
|---|---|---|---|
| 1 | 企业软件三层架构 | CRM/ERP + Agent + 用户入口 | 盘点 Seetong 三层架构现状 |
| 2 | Agent 价值双指标 | 完成数 + 价值 | 弃用聊天次数/调用数作为 KPI |
| 3 | Coding Agent 是早期优势 | Manus CodeAct / Codex | 优先 Agent 化 SDK / 模板生成 |
| 4 | Workflow vs Agent 决策矩阵 | 决策 4 象限 | 列现有自动化,分类 Workflow/Agent/Knowledge |
| 5 | Agent 产品形态 2 选 1 | 垂直嵌入 vs 独立 Agent | 评估 Seetong AI 助手定位 |
| 6 | 企业 AI 转型 4 阶段 | 单点 → 工具集中 → 多 Agent → 原生 | Seetong 自评当前阶段 |
| 7 | AI 原生组织 3 变化 | 取消中层 / 结果评价 / AI 代理沟通 | 取消中层 + 结果导向试点 |
| 8 | 三线合一闭环 | 架构 + 业务 + 组织 | Seetong 三线周报 |

## 6 个对 Seetong 团队可借鉴动作

1. **三层软件架构盘点**:Seetong APP(用户入口)+ Seetong AI 助手(认知行动)+ 设备/报警/录像库(业务记录)—— 三层现状评估,补足认知行动层
2. **Workflow vs Agent 决策矩阵落地**:列 Seetong 现有自动化/工作流(友盟告警 / 反馈分诊 / 设备添加 / 报警处理 / Bug 汇总),按"业务知识专业度 × 行动复杂度"分类,**哪些转 Workflow / 哪些转 Agent / 哪些维持**
3. **Coding Agent 优势域识别**:Seetong 中"上下文清晰 + 工具天然 + 验证完整 + 恢复低"子模块优先 Agent 化 —— 如 SDK 模板代码生成 / 跨端 iOS-Android-KMP 模板 / Seetong AI 助手 Skill 编写辅助
4. **企业 AI 转型 4 阶段定位**:Seetong 当前在第几阶段(单点试用 / 工具集中 / 多 Agent 协作 / AI 原生组织)?—— 自评建议:**当前 L2 工具集中**(Seetong AI 助手 + Skill 体系已成型),下一阶段 L3 多 Agent 协作是 6-12 个月目标
5. **AI 原生组织 3 变化试点**:
   - **取消中层**:位冬 + 许源 + 陈宝旺 = 一线 owner 直接对齐欧阳荣,绕开中间汇报
   - **结果评价**:日报"调用 AI 次数"指标降级,**升"判断决策占比"为新指标**
   - **AI 代理沟通**:Wecom 简报群 / AI Wiki 群 / Seetong 团队日报 由 Seetong AI 助手接管日常应答
6. **Agent 人才招聘 4 维度清单**:Seetong 下一个 AI 相关岗位招聘时,用 4 维度评估候选人 —— 基础素质 4 词 / 专业 P5-P9 / 业务能力(谁在赚钱/链路如何)/ 组织能力(冲突/资源/预期)

## 备注与限制

- **作者背景**:叶小钗(成都 TGO 7 组组长)是企业级 AI 培训讲师视角,6 场培训理论部分整理;具体企业 / 学员 / 培训案例未点名,**理论偏抽象**
- **公众号**:同名公众号「叶小钗」(成都 AI 应用生态大会演讲整理稿同源);文末"对 AI 感兴趣的同学"是常规引导,**已在 wiki/digest 摘掉**
- **数据缺位**:三层架构 / 4 阶段转型 / 4 维度招聘 是作者归纳框架,**无独立引用源**
- **抓取时间**:2026-07-13 13:52,推送日同天抓取
- **配套原文**:微信公众号 6 场培训理论部分整理稿(无视频/PPT 公开版本)
- **不适用场景**:不适用于"如何写一个具体 Agent 代码"(本文是全景架构图);不适用于"AI Coding 工具方法论"(本文是组织 + 人才维度)
- **本次编译严格按 compile-wx-article skill "透明玻璃"硬约束自检**:节点 8(6-10)/ H2 5(≤5)/ 表格 1(≤2)/ 0 陈词
- **待补证**:6 场培训具体企业的行业 / 规模 / 痛点;"4 维度招聘"中 P5-P9 级别对应 Seetong 现岗位;Seetong 当前 AI 转型阶段自评需团队 workshop

---

*本消息由 Seetong小助手 自动生成,欧阳荣 监督发布。*