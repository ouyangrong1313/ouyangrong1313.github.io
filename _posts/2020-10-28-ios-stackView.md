---
title: 设置页面用UIStackView布局多个UIView达到UITableView的效果
author: Ouyang Rong
date: 2020-10-28 16:14:00 +0800
categories: [iOS, UI]
tags: [UIStackView, UITableView]
---

# 需求设计

![设置页面](https://tva1.sinaimg.cn/large/0081Kckwly1gk5488dpt2j30910ikta8.jpg)

# 实现思路

这个设置页面之前就是直接在UIViewController的XIB上布局的，一个设置选项就是一个UIView。现在新需求来了，多增加了几个设置选项，如果还这样直接在VC上加View的话，屏幕较小的手机就有可能显示不全。因此，我在VC上增加了一个UIView，然后，依此添加UIScrollView和UIStackView在其上，最后把这些充当Cell的UIView都添加到UIStackView上去。

> 备注：这个UIScrollView布局出现了好些问题，报错提示说什么内容视图布局不清晰，后来去掉了内容布局，再加了一个UIView作为UIScrollView的父视图，才没报错。
>

![XIB截图](https://tva1.sinaimg.cn/large/0081Kckwly1gk54gni8xcj314l0lwafv.jpg)

# UIStackView是什么？

在iOS9中苹果在UIKit框架中引入了一个新的视图类UIStackView。UIStackView 类提供了一个高效的接口用于平铺一行或一列的视图组合。Stack视图管理着所有在它的 arrangedSubviews 属性中的视图的布局。这些视图根据它们在 arrangedSubviews 数组中的顺序沿着 Stack 视图的轴向排列。

简而言之，即UIStackView，就是一个ContainerView，可以沿横向或纵向按照一定的规则布局内部的子View。

UIStackView使用arrangedSubviews数组来管理子视图。

需要注意的是这个数组是一个readonly的属性，我们需要调用方法对arrangedSubviews数组进行操作。


```
初始化数组:
- (instancetype)initWithArrangedSubviews:(NSArray<__kindof UIView *> *)views;
添加子视图:
- (void)addArrangedSubview:(UIView *)view;
移除子视图:
- (void)removeArrangedSubview:(UIView *)view;
根据下标插入视图:
- (void)insertArrangedSubview:(UIView *)view atIndex:(NSUInteger)stackIndex;
```

> 注意： addArrangedSubview 和 insertArrangedSubview， 会把子控件加到arrangedSubviews数组的同时添加到StackView上，
>       但是removeArrangedSubview， 只会把子控件从arrangedSubviews数组中移除，
>       不会从subviews中移除，如果需要可调用removeFromSuperview

![](https://tva1.sinaimg.cn/large/0081Kckwly1gk5453ipi8j30q10jhdgo.jpg)
