# OpenMythos：开源复现 Anthropic 神秘模型架构

## 基础信息

- **来源**: 微信公众号 - 逛逛 GitHub
- **原文链接**: https://mp.weixin.qq.com/s/XHxcCgL-PcNJmCOE_Axm0A
- **抓取时间**: 2026-05-07
- **主题标签**: AI模型架构, 开源复现, Transformer变体, 循环深度推理

---

## 核心内容

### 背景故事

- Anthropic 发布 Claude Mythos Preview 模型，能力极强
- 英国 AI 安全研究所测试：能自主完成32步骤企业网络攻击（专家估计需20小时）
- CTF 挑战成功率 73%，但不对公众开放，仅提供给 Project Glasswing 联盟
- 22岁开源开发者 Kye Gomez 从公开论文拼凑线索，用 PyTorch 复现架构
- 项目名 **OpenMythos**，GitHub: https://github.com/kyegomez/OpenMythos
- 开源4天近7000 Star，现已1.1万

### 核心创新：循环深度 Transformer

传统 Transformer 靠堆层数提升能力，OpenMythos 走不同路线：

**传统模型** = 读一本书，翻完就完了
**OpenMythos** = 让同一组权重反复读同一段，每遍更深入理解

770M 参数循环模型 ≈ 1.3B 传统 Transformer（参数量省近一半）

### 三段架构

1. **Prelude（前奏层）**：普通 Transformer 层，跑一遍
2. **Recurrent Block（循环块）**：核心，同一组权重循环 T 次
3. **Coda（尾声层）**：普通 Transformer 层

### 三大技术亮点

#### 1. 循环推理，越想越深
- 每轮把当前状态和原始输入重新混合
- 训练16轮，推理可跑24-32轮（深度外推能力）
- 简单问题少跑，难问题多跑，改参数即可

#### 2. MoE + MLA
- 混合专家系统，用 DeepSeekMoE 细粒度路由
- 不同循环深度激活不同专家子集
- 注意力支持两种后端：
  - **MLA（Multi-Latent Attention）**：KV 缓存缩小 10-20 倍
  - **GQA**：支持 Flash Attention 2
- **ACT（Adaptive Computation Time）**：模型自己决定在哪停下

#### 3. 训练稳定性保证（LTI 注入）
- 循环 Transformer 历史难题：梯度爆炸/消失
- 解法：状态更新做成线性时不变系统的离散化
- 注入矩阵 A 通过零阶保持构造，谱半径严格 < 1
- 数学上保证稳定，非调参

### 当前状态

⚠️ **重要提醒**：OpenMythos 目前状态：
- ✅ 架构代码可编译
- ❌ 没有训练好的权重
- ❌ 没有 benchmark 数据
- ❌ 没有实际推理输出

定位：架构假设的代码实现，不是可用的产品

### 使用方式

```python
import torch
from open_mythos import OpenMythos, mythos_1b
from open_mythos.tokenizer import MythosTokenizer

config = mythos_1b()
model = OpenMythos(config)
tokenizer = MythosTokenizer()

ids = torch.tensor([tokenizer.encode("Explain quantum computing")])
output = model.generate(ids, max_new_tokens=512, temperature=0.7)
```

预置配置：1B ~ 1T 七种规模

训练支持 PyTorch FSDP 分布式

---

## 关键启示

1. **Scaling 新维度**：从"堆多少参数" → "推理时算多少轮"
2. **开源方法论**：复现从未确认存在的架构，足够具体可被证伪
3. **循环 Transformer 路线**：参数效率高，值得关注

---

## 相关资源

- GitHub: https://github.com/kyegomez/OpenMythos
- Claude Mythos: Project Glasswing (非公开)