# QMUI 组件库使用要点

## 简介

QMUI 是腾讯开源的 iOS UI 组件库，Seetong-iOS 项目基于它进行 UI 开发。

## 基础类继承体系

```
UIViewController
    ↓
BaseViewController（QMUIKit扩展）
    ↓
STXXXViewController
```

## BaseViewController 核心功能

### 导航栏管理

```objc
// 自定义导航栏
@property (nonatomic, copy) NSString *stTitle;
@property (nonatomic, strong) TZTabBarView *navView;

// 显示/隐藏导航栏
@property (nonatomic, assign) BOOL navViewHidden;

// 设置导航栏颜色
- (void)setNavBarBackgroundColor:(UIColor *)color;
- (void)setStatusBarBackgroundColor:(UIColor *)color;
```

### EmptyView 空状态

```objc
@property (nonatomic, strong) QMUIEmptyView *emptyView;

// 配置空状态视图
- (void)configureEmptyView;
- (void)showEmptyView;
- (void)showEmptyViewWithLoading;
- (void)hideEmptyView;
```

### 返回按钮

```objc
- (void)backBarButtonAction:(id)sender;
```

## 常用 QMUI 组件

### QMUITips Toast 提示

```objc
// 显示Toast
[QMUITips showWithText:@"操作成功" inView:self.view hideAfterSeconds:2];

// 显示加载中
[QMUITips showLoading:@"加载中..." inView:self.view];

// 隐藏
[QMUITips hideAllTips];
```

### QMUIAlertController 弹窗

```objc
QMUIAlertController *alert = [QMUIAlertController alertControllerWithTitle:@"提示"
                                                                   message:@"确定删除？"
                                                            preferredStyle:QMUIAlertControllerStyleAlert];

[alert addAction:[QMUIAlertAction actionWithTitle:@"取消" style:QMUIAlertActionStyleCancel handler:nil]];
[alert addAction:[QMUIAlertAction actionWithTitle:@"确定" style:QMUIAlertActionStyleDefault handler:^(QMUIAlertAction *action) {
    // 处理确定
}]];

[alert showWithAnimated:YES];
```

### QMUIGridView 网格布局

适合设置页面等均匀分布的网格布局。

### QMUISegmentControl 分段控件

替代原生 UISegmentedControl，样式更统一。

### QMUIButton 图片+文字按钮

支持图标和文字的多种排列方式。

## Masonry 约束

QMUI 建议配合 Masonry 使用 Auto Layout：

```objc
#import <Masonry/Masonry.h>

[self.titleLabel mas_makeConstraints:^(MASConstraintMaker *make) {
    make.centerX.equalTo(self);
    make.top.equalTo(self).offset(20);
    make.left.greaterThanOrEqualTo(self).offset(16);
    make.right.lessThanOrEqualTo(self).offset(-16);
}];
```

## 主题定制

QMUI 支持全局主题定制，通常在 AppDelegate 中配置：

```objc
// 配置全局主题
[QMUIConfiguration sharedInstance].xxx = xxx;
```

## 注意事项

1. **导入方式**：使用 `#import <QMUIKit/QMUIKit.h>` 导入全部组件
2. **BaseViewController**：业务 VC 应继承自 BaseViewController，而非直接继承 UIViewController
3. **横竖屏**：BaseNavigationController 已处理横竖屏切换
4. **Dark Mode**：QMUI 原生支持 Dark Mode，适配时使用 QMUITheme 相关 API

## 标签

#主题/APP研发 #QMUI #iOS/UI组件
