# 端侧 AI 集成方案

## 端侧 AI 优势

| 优势 | 说明 |
|------|------|
| 隐私性 | 数据不上云，本地处理 |
| 延迟 | 无网络延迟，实时响应 |
| 离线 | 无网络环境下可用 |
| 成本 | 无云端计算费用 |

## 端侧 AI 挑战

| 挑战 | 说明 |
|------|------|
| 模型大小 | 端侧模型需压缩 |
| 算力限制 | 移动端算力有限 |
| 功耗 | 持续AI计算耗电 |
| 兼容性 | 不同芯片架构适配 |

## Seetong APP 端侧 AI 场景

### 监控类 APP 潜在场景

1. **人形检测** - 本地识别人形，减少误报
2. **人脸识别** - 门禁场景本地比对
3. **声音检测** - 异常声音识别（婴儿哭、玻璃破碎）
4. **场景识别** - 自动切换白天/夜间模式

### 技术选型

| 方案 | 适用场景 | 模型大小 |
|------|----------|----------|
| Core ML（iOS）| 图像/视频分析 | 中等 |
| MLKit | 人脸/文字识别 | 中等 |
| TensorFlow Lite | 通用AI | 可压缩 |
| ONNX Runtime | 跨平台 | 中等 |

## iOS 端侧 AI

### Core ML

```objc
#import <CoreML/CoreML.h>
#import <Vision/Vision.h>

// 人形检测示例
VNDetectHumanRectanglesRequest *request = [[VNDetectHumanRectanglesRequest alloc] init];
VNImageRequestHandler *handler = [[VNImageRequestHandler alloc] initWithCVPixelBuffer:pixelBuffer options:@{}];
[handler performRequests:@[request] error:&error];
```

### Vision 框架

- `VNDetectFaceRectanglesRequest` - 人脸检测
- `VNRecognizeTextRequest` - 文字识别
- `VNDetectBarcodesRequest` - 条码扫描

## Android 端侧 AI

### MLKit

```kotlin
val recognizer = FaceDetection.getClient()

recognizer.process(image)
    .addOnSuccessListener { faces ->
        // 处理结果
    }
    .addOnFailureListener { e ->
        // 错误处理
    }
```

## 注意事项

1. **功耗管理** - AI 计算耗电，合理安排任务优先级
2. **后台限制** - iOS 后台应用 AI 计算受限
3. **模型更新** - 需考虑热更新模型的能力

## 标签

#主题/APP研发 #AI-Agent #端侧AI
