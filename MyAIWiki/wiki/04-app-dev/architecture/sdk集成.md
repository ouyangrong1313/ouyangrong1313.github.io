# Seetong-iOS Native SDK 集成规范

## 项目 SDK 架构

```
Seetong-iOS
├── Seetong-CliCmpt-Net-Sdk     # 网络SDK（C/C++）
└── Seetong-CliCmpt-PlayCtrl-Sdk # 播放控制SDK（音视频解码）
```

## 网络 SDK

**路径**：`/Users/topsee/Seetong-CliCmpt-Net-Sdk/`

- **语言**：C/C++
- **构建**：CMake
- **核心**：Funclib（网络功能函数库）

### 集成方式

SDK 编译成静态库，引入项目：

```bash
# 构建脚本
mkdir build && cd build
cmake ..
make
```

## 播放控制 SDK

**路径**：`/Users/topsee/Seetong-CliCmpt-PlayCtrl-Sdk/`

### 组件

| 组件 | 说明 |
|------|------|
| faac-1.28 | AAC音频编码 |
| faad2-2.7 | AAC音频解码 |
| PlayCtrl | 播放控制模块 |

### 平台

- iOS
- Android

## SDK 对接规范

### 1. 初始化顺序

在 AppDelegate 中按顺序初始化：

```
1. 日志系统（Logan）
2. 数据库（Realm）
3. 网络管理器（STNetworkManager）
4. Native SDK
5. 第三方SDK（analytics、push等）
```

### 2. JNI 交互（Android）

Native SDK 使用 JNI 与 Java 层交互，注意：
- 线程安全
- 回调需切换到主线程
- 资源释放顺序

### 3. 内存管理

- C/C++ SDK 需注意内存分配和释放
- 使用 Instruments 检测内存泄漏
- MLeaksFinder 辅助检测 Objective-C 内存泄漏

### 4. 错误处理

```objc
// 网络错误
typedef NS_ENUM(NSInteger, STErrorCode) {
    STErrorCodeNetworkUnavailable = -1,
    STErrorCodeTimeout = -2,
    STErrorCodeServerError = -3,
    // ...
};

// SDK 错误回调
typedef void (^STSDKErrorBlock)(NSError *error);
```

## 相关文档

- [[01-ai-agents/index|AI Agent 落地方案]] - 可考虑集成 AI 能力到 SDK

## 标签

#主题/APP研发 #NativeSDK #C-CPP #iOS/SDK集成
