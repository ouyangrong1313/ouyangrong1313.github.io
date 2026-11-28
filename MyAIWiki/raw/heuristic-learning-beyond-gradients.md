# Heuristic Learning：用规则系统超越神经网络强化学习

## 链接
https://mp.weixin.qq.com/s/-T5pI7bbil016_gK8nUjDQ

## 来源
AI寒武纪（公众号）

## 核心观点

### 背景：Continual Learning 的问题
神经网络灾难性遗忘：学了新东西，旧能力容易被覆盖。传统解决方案都卡在权重更新层面。

### 核心发现：Coding Agent 改变了规则维护成本曲线

OpenAI 翁家翌（后训练强化学习基础设施作者）做了一个实验：
- 目标：给游戏环境写几条便宜的测试规则，替代每次CI跑神经网络
- 工具：codex (gpt-5.4) 写了一套基于规则、完全不依赖神经网络的策略
- 结果：
  - Atari Breakout：从387分一路涨到理论最高分
  - MuJoCo Ant：跑到6000+分，进入深度强化学习量级
  - HalfCheetah：5局均值11836.7，同样进入深度强化学习量级
  - VizDoom：第一人称视觉任务，10个seed均值557.0
  - **Atari 57个游戏：中位数得分远高于PPO深度强化学习算法**
  - 全程没有训练任何神经网络

### Heuristic Learning (HL) 和 Heuristic System (HS)

**HL在做的事**：codex不是在反复写一条策略，而是在维护一套持续生长的软件系统。

**HS的组成部分**：
- 程序策略（规则、状态机、controller、MPC、宏动作）
- 状态表示
- 反馈入口
- 实验记录
- 回放或测试
- memory
- 更新机制

**HL vs 深度强化学习核心差异**：

| 维度 | 深度强化学习 | HL |
|------|-------------|-----|
| 策略 | 神经网络参数 | 代码（规则/状态机/MPC）|
| 反馈 | 固定reward | coding agent根据context提供（测试/日志/回放）|
| 更新 | 反向传播梯度 | coding agent直接修改代码 |
| 记忆 | on-policy基本没有，off-policy有replay | 显式记录trials/summary/失败原因/版本diff |

### 为什么以前没人做

人力维护heuristic的典型路径：
1. 今天加一条规则修了A
2. 明天发现B被修坏了
3. 后天再加一个if
4. 大后天没人敢删了

**问题不在heuristic没用，是没有人力能养得起。**

类比：人力维护专家系统像工业革命前手工纺纱；coding agent像纺织机，改变的是维护成本曲线。

### HL 也会有遗忘问题

- 新规则修好一个失败模式，同时破坏旧场景
- 新memory把agent反复带到错误方向
- 规则越堆越多，最后agent自己也维护不动

**HL不会自动解决Continual Learning**，但它把防遗忘变成了更工程化的问题：
- 旧能力可以被固化成回归测试、固定seed的回放、golden trace、失败视频、版本diff
- 历史是显式、可读、可删、可重构的
- 但只增长不压缩的HS最后会变成屎山代码

**健康的HS需要两个操作持续维持**：
1. **吸收反馈**：把新失败、新日志、新reward写回系统
2. **压缩历史**：把局部补丁折回更简单、更可维护的表示

Continual Learning从"怎么更新参数"变成了"怎么维护一个持续吸收反馈的软件系统"。

### HS能有多复杂

**耦合复杂度**：coding agent能维护多复杂的策略来支持HL。

关键因素：
- 代码侧：模块边界、接口稳定性、测试覆盖、日志观测性、回滚成本、状态可复现性
- agent侧：模型能力、上下文长度、memory质量、工具质量、迭代速度

**反例**：Montezuma记录到400分，但路线由86个宏动作组成，基本是开环执行。有些环境需要更强的程序形态（可组合宏动作、可恢复搜索状态、长期memory）。

### 下一个范式

当前范式转移路径：pretrain → RLHF → large-scale RL/RLVR。**凡是可以验证的，都开始能被解决。**

翁家翌认为 Online Learning 和 Continual Learning 可以通过 Heuristic Learning 部分解决。

### 最有希望的方向：神经网络 + HL

用HL处理在线数据快速生成在线经验，把在线经验内化成可训练、可回归、可筛选的数据，再周期性更新神经网络。

**可能的分工形态**（以机器人为例）：
- **浅层神经网络**（System 1）：感知、分类、物体状态估计，快而便宜
- **HL**（System 1）：最新数据处理、规则、测试、回放、memory、安全边界、局部恢复
- **LLM agent**（System 2）：给HL提供反馈、改进数据，周期性提取HL数据更新自身

层级结构：
- 关节级HL（安全和低延迟控制）
- 肢体级HL（步态和接触）
- 全身平衡HL
- 任务级HL（任务、恢复、长期记忆）

coding agent不一定直接懂得走路，更像插进系统里的**更新管线**。

### 核心结论

> 过去很多heuristic看起来没有前途，原因常常落在维护成本上；它们本身未必太弱。coding agent改变的是这条维护成本曲线。

规则、测试、日志、memory和补丁原来只是散落的工程材料，现在开始可以组成一个会持续更新的Heuristic System。

## 相关链接
- 原文实验详情：https://trinkle23897.github.io/learning-beyond-gradients/#zh

## 标签
#AI-Agent #Heuristic-Learning #Continual-Learning #Coding-Agent #强化学习