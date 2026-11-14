# Heuristic Learning：用规则系统超越神经网络

**来源**：AI寒武纪（公众号）

## 一句话总结

OpenAI 翁家翌发现：用 coding agent 维护规则系统，不训练神经网络，在 Atari 57 个游戏上的中位数得分远高于 PPO 深度强化学习算法。

## 核心发现

**Coding agent 改变了规则维护成本曲线**

传统问题：专家系统/规则系统需要人工维护，成本太高没人养得起。

实验结果（全程不训练神经网络）：
- Atari Breakout：387分 → 理论最高分
- MuJoCo Ant：6000+分（深度强化学习量级）
- HalfCheetah：11836.7分（深度强化学习量级）
- Atari 57个游戏：中位数得分远高于PPO

## Heuristic System (HS) 的组成

- 程序策略（规则/状态机/MPC/宏动作）
- 反馈入口
- 实验记录、回放、测试
- memory
- coding agent执行的更新机制

## 关键洞察

1. **HL也会遗忘**：只增长不压缩会变成屎山代码，需要"吸收反馈+压缩历史"两个操作
2. **最有希望的方向**：神经网络+HL结合，HL生成可训练数据，周期性更新神经网络
3. **Coding agent 像纺织机**：改变了heuristic维护的成本曲线，让以前养不起的系统现在能养了

## 标签
#AI-Agent #Heuristic-Learning #Coding-Agent #Continual-Learning