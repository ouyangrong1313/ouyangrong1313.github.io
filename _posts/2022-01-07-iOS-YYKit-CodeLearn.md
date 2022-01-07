---
title: iOS YYKit 源码学习
author: Ouyang Rong
date: 2022-01-07 18:11:00 +0800
categories: [iOS, 源码学习]
tags: [YYKit, 源码学习]
---

YYKit 框架的作者是现任职于滴滴的郭曜源（ibireme）。

> 最近一系列开源项目 YYKit 在 iOS 社区引起广泛反响，由于其代码质量高，在短时间内就收获了大量的 star，它的作者是国人开发者 ibireme，优酷土豆的 iOS 开发工程师郭曜源，InfoQ 社区编辑唐巧对他进行了采访，了解这些开源项目背后的故事。

大家好，我叫郭曜源，是一个 iOS 开发者，现居北京，就职于优酷土豆。喜欢代码，爱好设计与音乐。

唐巧：你在 iOS 开发上是如何快速成长起来的？有没有什么心得可以分享给 iOS 开发新手？

ibireme：我接触 iOS 开发的时间很早，但是一直都是在工作之余靠着兴趣自学的。14 年我还在人人网时，部门内部有个新项目需要 iOS 开发，我才得以有机会在工作中使用 iOS 相关的技术。全职转为 iOS 开发后，我花费了大量的时间阅读和学习各种开源的代码、研究其中的实现原理、尝试自己实现相关技术、尝试在工作中使用，这使得我在 iOS 开发技术上进步很快。对于 iOS 开发来说，我觉得自学能力是很重要的。主动去研究一些优秀的开源项目、多在工作中实践和学习，这样就能逐步提升个人技术水平了。


# [YYModel](https://github.com/ibireme/YYModel)

YYModel是一个高性能的 iOS JSON 模型框架。


# [YYCache](https://github.com/ibireme/YYCache)

YYCache是一个缓存框架，支持磁盘和内存级别的缓存。


# [YYImage](https://github.com/ibireme/YYImage)

YYImage是一个功能强大的图像库，支持的格式比较全面、支持动画图像（比如GIF）和帧动画，另外还支持渐进式加载。


# [YYWebImage](https://github.com/ibireme/YYWebImage)

YYWebImage是一个异步图片加载框架。


# [YYText](https://github.com/ibireme/YYText)

YYText是一个富文本显示组件。


# [YYDispatchQueuePool](https://github.com/ibireme/YYDispatchQueuePool)

iOS 全局并发队列管理工具，主要解决concurrent queue创建大量线程导致主线程卡顿，可以解决UI卡顿的问题。


# [YYAsyncLayer](https://github.com/ibireme/YYAsyncLayer)

YYAsyncLayer是异步绘制与显示的工具类。


# [YYCategories](https://github.com/ibireme/YYCategories)

YYCategories是一系列Category工具类，基本涵盖了日常开发过程中常见的工具类。


# 参考文章

[YYKit Github](https://github.com/ibireme/YYKit)

[YYKit 源码探究](https://www.jianshu.com/c/261199576fa9)

[专访 YYKit 作者郭曜源：开源大牛是怎样炼成的](https://www.infoq.cn/news/2015/11/ibireme-interview/)

[YYKit 源码学习-总览](https://ustcqidi.github.io/2018/06/08/YYKit源码学习-总览/)

[看 YYKit 的源码-vanney](http://vanney9.com/2016/08/15/YYKit-source-code-analysis/)

[YYImage 源码分析-ChenAo](https://chenao0727.github.io/2017/02/04/YYImage/)

[YYWebImage 源码分析-宓珂璟](https://blog.csdn.net/Deft_MKJing/article/details/79895621)

[YYCache 源码剖析-波儿菜](https://www.jianshu.com/p/408d4d37bcbd)

[YYCache 设计思路-ibireme](https://blog.ibireme.com/2015/10/26/yycache/)

[YYImage 设计思路，实现细节剖析-聊宅](https://lision.me/tags/yykit/)

[YYCache 源码解析-J_Knight_](https://juejin.cn/post/6844903554214264840)
