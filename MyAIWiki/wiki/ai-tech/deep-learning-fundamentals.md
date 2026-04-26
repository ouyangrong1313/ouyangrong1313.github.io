# 深度学习基础

## 神经网络基础

### 激活函数
- **ReLU**: f(x) = max(0, x) — 最常用，收敛快
- **Sigmoid**: f(x) = 1/(1+e^(-x)) — 输出0-1，用于二分类
- **Tanh**: f(x) = (e^x - e^(-x))/(e^x + e^(-x)) — 输出-1到1

### 反向传播 (Backpropagation)
- 链式法则求导
- 梯度下降优化
- 损失函数最小化

---

## CNN (卷积神经网络)

### 核心概念
- **卷积层** — 提取特征，局部连接
- **池化层** — 下采样，减少参数
- **全连接层** — 分类/回归

### 应用场景
- 图像分类（ResNet、VGG）
- 目标检测（YOLO）
- 图像分割（U-Net）

---

## RNN / LSTM

### RNN 问题
- 梯度消失/爆炸
- 长期依赖难以捕捉

### LSTM (Long Short-Term Memory)
- **门控机制**：
  - 输入门：决定多少新信息写入
  - 遗忘门：决定多少旧信息保留
  - 输出门：决定输出什么

---

## Transformer 架构

### 核心组件

| 组件 | 作用 |
|------|------|
| **Positional Encoding** | 给序列位置信息（因为Attention本身无位置概念） |
| **Layer Normalization** | 稳定训练：γ ⊙ (x - μ) / √(σ² + ε) + β |
| **SublayerConnection** | 残差连接：x + Sublayer(x) |
| **Feed-Forward** | 两层线性变换 + ReLU |
| **Dropout** | 防止过拟合 |
| **Label Smoothing** | 软化标签，提高泛化 |

### Attention 机制

**Scaled Dot-Product Attention:**
```
Attention(Q,K,V) = softmax(QK^T / √d_k)V
```

**Multi-Head Attention:**
```
MultiHead = Concat(head_1,...,head_h)W^O
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

---

## 优化器

### Adam (Kingma and Ba)
- 自适应学习率
- 动量 + RMSProp 结合
- 默认首选优化器

---

## 标签

#主题/AI科技 #场景/技术博客

## 相关链接

- [[transformer-attention|Transformer与Attention机制]]
- [[llm-fundamentals|大语言模型基础]]
