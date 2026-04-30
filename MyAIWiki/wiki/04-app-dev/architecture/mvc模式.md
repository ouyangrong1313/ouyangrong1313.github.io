# Seetong-iOS MVC 架构

## 整体架构

Seetong-iOS 采用 **MVC** 架构，部分模块向 **MVVM** 演进。

```
┌─────────────────────────────────────────────┐
│                   View                       │
│  (UIView, CustomView, Cell)                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              Controller                       │
│  (ViewController, 业务逻辑, 数据组装)          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│                Model                          │
│  (DataModel, Service, NetworkManager)         │
└─────────────────────────────────────────────┘
```

## 模块内部结构

每个业务模块（如 Login、Device）遵循：

```
Module/
├── Controller/          # ViewControllers
│   └── STXXXViewController.h/m
├── Model/               # 数据模型
│   └── STXXXModel.h/m
├── Services/            # 业务服务（含网络）
│   └── STXXXService.h/m
└── View/                # 专用视图
    ├── STXXXCell.h/m
    └── STXXXView.h/m
```

## 分层职责

### Controller（业务控制器）

| 职责 | 说明 |
|------|------|
| UI管理 | 创建视图、添加子视图 |
| 数据组装 | 接收 Model 数据，组装成 View 需要的形式 |
| 事件响应 | 处理用户交互，调用 Service |
| 生命周期 | 管理 ViewController 生命周期 |

**避免**：Controller 不应包含过多业务逻辑，应下放到 Service。

### Model（数据层）

| 类型 | 说明 |
|------|------|
| DataModel | 数据结构，与 JSON 对应 |
| Service | 业务逻辑、网络请求、数据缓存 |

### View（视图层）

| 类型 | 说明 |
|------|------|
| Cell | 表格/Collection Cell |
| CustomView | 可复用自定义视图 |
| EmptyView | 空状态视图 |

## 数据流向

```
用户操作 → Controller → Service → Network
                ↑           ↓
                ←── Model ←──┘
```

## Base 类支持

| Base类 | 父类 | 作用 |
|--------|------|------|
| BaseViewController | UIViewController | 通用VC基类 |
| BaseListViewController | BaseViewController | 列表VC基类 |
| BaseNavigationController | UINavigationController | 导航栏基类 |
| BaseModel | NSObject | Model基类，JSON序列化 |

## MVVM 演进

部分新模块尝试 MVVM：

```
View ←→ ViewModel ←→ Model
```

ViewModel 负责：
- 数据转换和格式化
- 业务逻辑处理
- 暴露可观察属性

## 相关文档

- [[ios/qmui组件库]] - View 层组件
- [[ios/项目规范]] - 编码规范

## 标签

#主题/APP研发 #MVC #架构
