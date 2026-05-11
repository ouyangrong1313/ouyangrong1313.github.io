# OpenMythos 与循环深度 Transformer

## 概念

**OpenMythos** 是一个开源项目，试图复现 Anthropic 从未公开的 Claude Mythos 模型架构。

核心思路：不再堆层数，而是让同一组权重循环推理多轮。770M 参数 ≈ 1.3B 传统 Transformer。

## 架构：三段式

```
输入 → [Prelude 普通Transformer] → [Recurrent Block 循环块] → [Coda 普通Transformer] → 输出
                              ↑
                         同一组权重循环 T 次
```

## 关键技术

| 技术 | 说明 |
|------|------|
| **循环推理** | 每轮混合状态和输入，可深度外推（训练16轮推理32轮） |
| **MoE + MLA** | 细粒度路由 + KV缓存压缩10-20倍 |
| **ACT** | 模型自适配计算时间 |
| **LTI注入** | 数学保证训练稳定 |

## 现状

| 状态 | 说明 |
|------|------|
| ✅ 可编译 | 代码完整 |
| ❌ 无权重 | 仅有架构假设 |
| ❌ 无benchmark | 未经验证 |

定位：**可证伪的架构假设**，非可用产品

## 意义

把 Scaling 从"堆参数"推向"推理时算多少轮"。参数量省一半，效果相当。

## 资源

- GitHub: https://github.com/kyegomez/OpenMythos
- 原文: [[2026-05-07-openmythos]] (微信公众号整理)