---
title: 多线程详解
author: Ouyang Rong
date: 2021-09-01 10:57:00 +0800
categories: [iOS, 多线程]
tags: [NSThread, GCD, NSOperation]
---


# 概述

在iOS中每个进程启动后都会建立一个主线程（UI线程），这个线程是其他线程的父线程。由于在iOS中除了主线程，其他子线程是独立于Cocoa Touch的，所以只有主线程可以更新UI界面。iOS中多线程使用并不复杂，关键是**如何控制好各个线程的执行顺序、处理好资源竞争问题**。

我们运用多线程的目的是：将耗时的操作放在后台执行。

- 进程（Process）：是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础，每一个进程都有自己独立的虚拟内存空间。简单来说，进程是指在系统中正在运行的一个应用程序，每一个程序都是一个进程，并且进程之间是独立的，每个进程均运行在其专用且受保护的内存空间内。
- 线程（thread）：是程序执行流的最小单元线程是程序中一个单一的顺序控制流程。是进程内一个相对独立的、可调度的执行单元，是系统独立调度和分派CPU的基本单位指运行中的程序的调度单位。简单来说，一个进程要想执行任务，必须得有线程。线程中任务的执行是串行的，要在一个线程中执行多个任务，那么只能一个一个地按顺序执行这些任务，也就是说，在同一时间内，一个线程只能执行一个任务，由此可以理解线程是进程中的一条执行路径。一个进程中至少包含一条线程，即主线程，创建线程的目的就是为了开启一条新的执行路径，运行指定的代码，与主线程中的代码实现同时运行。
- 主线程（mainthread）：处理UI，所有更新UI的操作都必须在主线程上执行。不要把耗时操作放在主线程，会卡界面。
- 多线程（multithreading）：是指从软件或者硬件上实现多个线程并发执行的技术。具有多线程能力的计算机因有硬件支持而能够在同一时间执行多于一个线程，进而提升整体处理性能。在同一时刻，一个CPU只能处理一条线程，但CPU可以在多条线程之间快速的切换，只要切换的足够快，就造成了多线程一同执行的假象。

> 线程就像火车的一节车厢，进程则是火车。车厢（线程）离开火车（进程）是无法跑动的，而火车（进程）至少有一节车厢（主线程）。多线程可以看做多个车厢，它的出现是为了提高效率。 多线程是通过提高资源使用率来提高系统总体的效率。
>
> 优点：
>
> - 能适当提高程序的执行效率
> - 能适当提高资源利用率（CPU、内存利用率）
>
> 缺点：
>
> - 开启线程需要占用一定的内存空间（默认情况下，主线程占用1M，子线程占用512KB），如果开启大量的线程，会占用大量的内存空间，降低程序的性能
> - 线程越多，CPU在调度线程上的开销就越大

- 同步（sync）：只能在当前线程按先后顺序依次执行，不开启新线程。
- 异步（async）：可以在当前线程开启多个新线程执行，可不按顺序执行。异步是多线程的代名词
![队列](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E9%98%9F%E5%88%97.png)
- 队列：装载线程任务的队形结构。(系统以先进先出的方式调度队列中的任务执行)。
![并发队列](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%B9%B6%E5%8F%91%E9%98%9F%E5%88%97.png)
- 并发队列：线程可以同时一起进行执行。实际上是CPU在多条线程之间快速的切换。（并发功能只有在异步（dispatch_async）函数下才有效）
![串行队列](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E4%B8%B2%E8%A1%8C%E9%98%9F%E5%88%97.png)
- 串行队列：线程只能依次有序的执行。

注意:

- 一个进程可有多个线程。
- 一个进程可有多个队列。
- 队列可分并发队列和串行队列。


# 线程的状态与生命周期

**线程的生命周期是：新建 - 就绪 - 运行 - 阻塞 - 死亡**

- 新建：实例化线程对象。
- 就绪：向线程对象发送start消息，线程对象被加入可调度线程池等待CPU调度。
- 运行：CPU 负责调度可调度线程池中线程的执行。线程执行完成之前，状态可能会在就绪和运行之间来回切换。就绪和运行之间的状态变化由CPU负责，程序员不能干预。
- 阻塞：当满足某个预定条件时，可以使用休眠或锁，阻塞线程执行。`sleepForTimeInterval`（休眠指定时长），`sleepUntilDate`（休眠到指定日期），`@synchronized(self)：`（互斥锁）。
- 死亡：正常死亡，线程执行完毕。非正常死亡，当满足某个条件后，在线程内部中止执行或在主线程中止线程对象。`[NSThread exit]`一旦强行终止线程，后续的所有代码都不会被执行。线程外死亡，`[thread cancel]` 并不会直接取消线程，只是给线程对象添加`isCancelled`标记。死亡后线程对象的 `isFinished`属性为`YES`；如果是发送`calcel`消息，线程对象的`isCancelled` 属性为`YES`；死亡后stackSize == 0，内存空间被释放。

**线程的状态转换**

- 如果CPU现在调度当前线程对象，则当前线程对象进入运行状态，如果CPU调度其他线程对象，则当前线程对象回到就绪状态。
- 如果CPU在运行当前线程对象的时候调用了sleep方法\等待同步锁，则当前线程对象就进入了阻塞状态，等到sleep到时\得到同步锁，则回到就绪状态。
- 如果CPU在运行当前线程对象的时候线程任务执行完毕\异常强制退出，则当前线程对象进入死亡状态。

只看文字可能不太好理解，具体当前线程对象的状态变化如下图所示。

![线程的状态](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%8A%B6%E6%80%81.png)


# 多线程的四种解决方案

多线程的四种解决方案分别是：pthread，NSThread，GCD， NSOperation。

- pthread：运用C语言，是一套通用的API，可跨平台Unix/Linux/Windows。线程的生命周期由程序员管理。
- NSThread：面向对象，可直接操作线程对象。线程的生命周期由程序员管理。
- GCD：代替NSThread，可以充分利用设备的多核，自动管理线程生命周期。
- NSOperation：底层是GCD，比GCD多了一些方法，更加面向对象，自动管理线程生命周期。


# 多线程对比

![对线程对比](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%A4%9A%E7%BA%BF%E7%A8%8B%E5%AF%B9%E6%AF%94.png)

## NSThread

每个NSThread对象对应一个线程，真正最原始的线程。
- 优点：NSThread 轻量级最低，相对简单。
- 缺点：手动管理所有的线程活动，如生命周期、线程同步、睡眠等。


## NSOperation

自带线程管理的抽象类。
- 优点：自带线程周期管理，操作上可更注重自己逻辑。
- 缺点：面向对象的抽象类，只能实现它或者使用它定义好的两个子类：NSInvocationOperation 和 NSBlockOperation。


## GCD

Grand Central Dispatch (GCD)是Apple开发的一个多核编程的解决方法。
- 优点：最高效，避开并发陷阱。
- 缺点：基于C实现。


## 选择小结

- 简单而安全的选择NSOperation实现多线程即可。
- 处理大量并发数据，又追求性能效率的选择GCD。
- NSThread本人选择基本上是在做些小测试上使用，当然也可以基于此造个轮子。

## 场景选择

- 图片异步加载

这种常见的场景是最常见也是必不可少的。异步加载图片有分成两种来说明一下。
> - 第一种，在UI主线程开启新线程按顺序加载图片，加载完成刷新UI。
> - 第二种，依然是在主线程开启新线程，顺序不定地加载图片，加载完成个字刷新UI。

- 创作工具上的异步

这个跟上边任务调度道理，只是为了丰富描述，有助于“举一反三”效果。如下描述的是app创作小说。
> - 场景一，app本地创作10个章节内容未同步服务器，同时发表这10个章节产生的一系列动作，其中上传内容，获取分配章节Id，如果后台没有做处理最好方式做异步按顺序执行。
> - 场景二，app本地创作列表中有3本小说为发表，同时发表创作列表中的3本小说，自然考虑并行队列执行发表。


# 线程安全问题

多个线程访问同一块资源进行读写，如果不加控制随意访问容易产生数据错乱从而引发数据安全问题。为了解决这一问题，就有了加锁的概念。加锁的原理就是当有一个线程正在访问资源进行写的时候，不允许其他线程再访问该资源，只有当该线程访问结束后，其他线程才能按顺序进行访问。对于读取数据，有些程序设计是允许多线程同时读的，有些不允许。UIKit中几乎所有控件都不是线程安全的，因此需要在主线程上更新UI。

**解决多线程安全问题的方法**

## 方法一：互斥锁（同步锁）

```
// 注意：锁定1份代码只用1把锁，用多把锁是无效的
@synchronized(锁对象) {
    // 需要锁定的代码
}
```

使用互斥锁，在同一个时间，只允许一条线程执行锁中的代码。因为互斥锁的代价非常昂贵，所以锁定的代码范围应该尽可能小，只要锁住资源读写部分的代码即可。使用互斥锁也会影响并发的目的。

判断的时候锁对象要存在，如果代码中只有一个地方需要加锁，大多都使用self作为锁对象，这样可以避免单独再创建一个锁对象。加了互斥做的代码，当新线程访问时，如果发现其他线程正在执行锁定的代码，新线程就会进入休眠。

## 方法二：自旋锁

加了自旋锁，当新线程访问代码时，如果发现有其他线程正在锁定代码，新线程会用死循环的方式，一直等待锁定的代码执行完成。相当于不停尝试执行代码，比较消耗性能。 属性修饰atomic本身就有一把自旋锁。

下面说一下属性修饰 nonatomic 和 atomic

- nonatomic 非原子属性（非线程安全），不会为setter方法加锁，同一时间可以有很多线程读和写。不过效率更高，一般使用nonatomic。适合内存小的移动设备。
- atomic 原子属性（线程安全），为setter方法加锁（默认就是atomic），保证同一时间只有一个线程能够写入（但是同一个时间多个线程都可以取值），atomic 本身就有一把锁（自旋锁）。需要消耗大量的资源。

atomic加锁原理：

```
@property (assign, atomic) int age;
- (void)setAge:(int)age
{
    @synchronized(self) {
       _age = age;
    }
}
```

建议：
1. 所有属性都声明为nonatomic
2. 尽量避免多线程抢夺同一块资源
3. 尽量将加锁、资源抢夺的业务逻辑交给服务器端处理，减小移动客户端的压力

## 方法三：NSLock

```
_lock = [[NSLock alloc] init];
 - (void)synchronizedMethod {
    [_lock lock];
    //safe
    [_lock unlock];
 }
```


# pthread

## pthread 简介

pthread 是一套通用的多线程的 API，可以在Unix / Linux / Windows 等系统跨平台使用，使用 C 语言编写，需要程序员自己管理线程的生命周期，使用难度较大，我们在 iOS 开发中几乎不使用 pthread，但是还是来可以了解一下的。

> 引自 百度百科   
>
> POSIX 线程（POSIX threads），简称 Pthreads，是线程的 POSIX 标准。该标准定义了创建和操纵线程的一整套 API。在类Unix操作系统（Unix、Linux、Mac OS X等）中，都使用 Pthreads 作为操作系统的线程。Windows 操作系统也有其移植版 pthreads-win32。
>
> 引自 维基百科
>
> POSIX 线程（英语：POSIX Threads，常被缩写 为 Pthreads）是 POSIX 的线程标准，定义了创建和操纵线程的一套 API。
实现 POSIX 线程标准的库常被称作 Pthreads，一般用于 Unix-like POSIX 系统，如 Linux、Solaris。但是 Microsoft Windows 上的实现也存在，例如直接使用 Windows API 实现的第三方库 pthreads-w32；而利用 Windows 的 SFU/SUA 子系统，则可以使用微软提供的一部分原生 POSIX API。


## pthread 使用方法

1. 首先要包含头文件`#import <pthread.h>`
2. 其次要创建线程，并开启线程执行任务

```
// 1. 创建线程: 定义一个pthread_t类型变量
pthread_t thread;
// 2. 开启线程: 执行任务
pthread_create(&thread, NULL, run, NULL);
// 3. 设置子线程的状态设置为 detached，该线程运行结束后会自动释放所有资源
pthread_detach(thread);
void * run(void *param)    // 新线程调用方法，里边为需要执行的任务
{
NSLog(@"%@", [NSThread currentThread]);
return NULL;
}
```

> - `pthread_create(&thread, NULL, run, NULL)`中各项参数含义：
> - 第一个参数`&thread`是线程对象，指向线程标识符的指针
> - 第二个是线程属性，可赋值`NULL`
> - 第三个`run`表示指向函数的指针(`run`对应函数里是需要在新线程中执行的任务)
> - 第四个是运行函数的参数，可赋值`NULL`

## pthread 其他相关方法

> - `pthread_create()` 创建一个线程
> - `pthread_exit()` 终止当前线程
> - `pthread_cancel()` 中断另外一个线程的运行
> - `pthread_join()` 阻塞当前的线程，直到另外一个线程运行结束
> - `pthread_attr_init()` 初始化线程的属性
> - `pthread_attr_setdetachstate()` 设置脱离状态的属性（决定这个线程在终止时是否可以被结合）
> - `pthread_attr_getdetachstate()` 获取脱离状态的属性
> - `pthread_attr_destroy()` 删除线程的属性
> - `pthread_kill()` 向线程发送一个信号


# NSThread

NSThread 是苹果官方提供的，使用起来比 pthread 更加面向对象，简单易用，可以直接操作线程对象。不过也需要需要程序员自己管理线程的生命周期(主要是创建)，我们在开发的过程中偶尔使用 NSThread。比如我们会经常调用`[NSThread currentThread]`来显示当前的进程信息。

## 1：NSThread创建线程

NSThread有三种创建方式：

- init方式
- detachNewThreadSelector创建好之后自动启动
- performSelectorInBackground创建好之后也是直接启动

```
/** 方法一 动态实例化，需要start */
NSThread *thread1 = [[NSThread alloc] initWithTarget:self selector:@selector(doSomething1:) object:@"NSThread1"];
// 线程加入线程池等待CPU调度，时间很快，几乎是立刻执行
thread1.threadPriority = 1;// 设置线程的优先级(0.0 - 1.0，1.0最高级)
[thread1 start];

/** 方法二 静态实例化，创建好之后自动启动 */
[NSThread detachNewThreadSelector:@selector(doSomething2:) toTarget:self withObject:@"NSThread2"];

/** 方法三 隐式实例化，直接启动 */
[self performSelectorInBackground:@selector(doSomething3:) withObject:@"NSThread3"];

- (void)doSomething1:(NSObject *)object {
    // 传递过来的参数
    NSLog(@"%@",object);
    NSLog(@"doSomething1：%@",[NSThread currentThread]);
}

- (void)doSomething2:(NSObject *)object {
    NSLog(@"%@",object);
    NSLog(@"doSomething2：%@",[NSThread currentThread]);
}

- (void)doSomething3:(NSObject *)object {
    NSLog(@"%@",object);
    NSLog(@"doSomething3：%@",[NSThread currentThread]);
}
```

## 2：NSThread的类方法

- 返回当前线程

```
// 当前线程
[NSThread currentThread];
NSLog(@"%@",[NSThread currentThread]);

// 如果number=1，则表示在主线程，否则是子线程
打印结果：<NSThread: 0x608000261380>{number = 1, name = main}
```

- 阻塞休眠

```
//休眠多久
[NSThread sleepForTimeInterval:2];
//休眠到指定时间
[NSThread sleepUntilDate:[NSDate date]];
```

- 类方法补充

```
//退出线程
[NSThread exit];
//判断当前线程是否为主线程
[NSThread isMainThread];
//判断当前线程是否是多线程
[NSThread isMultiThreaded];
//主线程的对象
NSThread *mainThread = [NSThread mainThread];
```

## 3：NSThread的一些属性

```
//线程是否在执行
thread.isExecuting;
//线程是否被取消
thread.isCancelled;
//线程是否完成
thread.isFinished;
//是否是主线程
thread.isMainThread;
//线程的优先级，取值范围0.0到1.0，默认优先级0.5，1.0表示最高优先级，优先级高，CPU调度的频率高
thread.threadPriority;
```

## 4：线程之间通信

在开发中，我们经常会在子线程进行耗时操作，操作结束后再回到主线程去刷新 UI。这就涉及到了子线程和主线程之间的通信。我们先来了解一下官方关于 NSThread 的线程间通信的方法。

```
// 在主线程上执行操作
- (void)performSelectorOnMainThread:(SEL)aSelector withObject:(id)arg waitUntilDone:(BOOL)wait;
- (void)performSelectorOnMainThread:(SEL)aSelector withObject:(id)arg waitUntilDone:(BOOL)wait modes:(NSArray<NSString *> *)array;
// equivalent to the first method with kCFRunLoopCommonModes

// 在指定线程上执行操作
- (void)performSelector:(SEL)aSelector onThread:(NSThread *)thr withObject:(id)arg waitUntilDone:(BOOL)wait modes:(NSArray *)array NS_AVAILABLE(10_5, 2_0);
- (void)performSelector:(SEL)aSelector onThread:(NSThread *)thr withObject:(id)arg waitUntilDone:(BOOL)wait NS_AVAILABLE(10_5, 2_0);

// 在当前线程上执行操作，调用 NSObject 的 performSelector:相关方法
- (id)performSelector:(SEL)aSelector;
- (id)performSelector:(SEL)aSelector withObject:(id)object;
- (id)performSelector:(SEL)aSelector withObject:(id)object1 withObject:(id)object2;
```

## 5：NSThread 线程安全和线程同步

### NSThread 非线程安全

```
/**
* 初始化火车票数量、卖票窗口(非线程安全)、并开始卖票
*/
- (void)initTicketStatusNotSave {
// 1. 设置剩余火车票为 50
self.ticketSurplusCount = 50;

// 2. 设置北京火车票售卖窗口的线程
self.ticketSaleWindow1 = [[NSThread alloc]initWithTarget:self selector:@selector(saleTicketNotSafe) object:nil];
self.ticketSaleWindow1.name = @"北京火车票售票窗口";

// 3. 设置上海火车票售卖窗口的线程
self.ticketSaleWindow2 = [[NSThread alloc]initWithTarget:self selector:@selector(saleTicketNotSafe) object:nil];
self.ticketSaleWindow2.name = @"上海火车票售票窗口";

// 4. 开始售卖火车票
[self.ticketSaleWindow1 start];
[self.ticketSaleWindow2 start];

}

/**
* 售卖火车票(非线程安全)
*/
- (void)saleTicketNotSafe {
while (1) {
//如果还有票，继续售卖
if (self.ticketSurplusCount > 0) {
self.ticketSurplusCount --;
NSLog(@"%@", [NSString stringWithFormat:@"剩余票数：%ld 窗口：%@", self.ticketSurplusCount, [NSThread currentThread].name]);
[NSThread sleepForTimeInterval:0.2];
}
//如果已卖完，关闭售票窗口
else {
NSLog(@"所有火车票均已售完");
break;
}
}
}
```

可以看到在不考虑线程安全的情况下，得到票数是错乱的，这样显然不符合我们的需求，所以我们需要考虑线程安全问题。

### NSThread 线程安全

线程安全解决方案：可以给线程加锁，在一个线程执行该操作的时候，不允许其他线程进行操作。iOS 实现线程加锁有很多种方式。`@synchronized`、 `NSLock`、`NSRecursiveLock`、`NSCondition`、`NSConditionLock`、`pthread_mutex`、`dispatch_semaphore`、`OSSpinLock`、`atomic(property) set/get`等等各种方式。为了简单起见，这里不对各种锁的解决方案和性能做分析，只用最简单的`@synchronized`来保证线程安全，从而解决线程同步问题。

```
/**
* 初始化火车票数量、卖票窗口(线程安全)、并开始卖票
*/
- (void)initTicketStatusSave {
// 1. 设置剩余火车票为 50
self.ticketSurplusCount = 50;

// 2. 设置北京火车票售卖窗口的线程
self.ticketSaleWindow1 = [[NSThread alloc]initWithTarget:self selector:@selector(saleTicketSafe) object:nil];
self.ticketSaleWindow1.name = @"北京火车票售票窗口";

// 3. 设置上海火车票售卖窗口的线程
self.ticketSaleWindow2 = [[NSThread alloc]initWithTarget:self selector:@selector(saleTicketSafe) object:nil];
self.ticketSaleWindow2.name = @"上海火车票售票窗口";

// 4. 开始售卖火车票
[self.ticketSaleWindow1 start];
[self.ticketSaleWindow2 start];

}

/**
* 售卖火车票(线程安全)
*/
- (void)saleTicketSafe {
while (1) {
// 互斥锁
@synchronized (self) {
//如果还有票，继续售卖
if (self.ticketSurplusCount > 0) {
self.ticketSurplusCount --;
NSLog(@"%@", [NSString stringWithFormat:@"剩余票数：%ld 窗口：%@", self.ticketSurplusCount, [NSThread currentThread].name]);
[NSThread sleepForTimeInterval:0.2];
}
//如果已卖完，关闭售票窗口
else {
NSLog(@"所有火车票均已售完");
break;
}
}
}
}
```

可以看出，在考虑了线程安全的情况下，加锁之后，得到的票数是正确的，没有出现混乱的情况。我们也就解决了多个线程同步的问题。


# GCD的使用

GCD（Grand Central Dispatch） 伟大的中央调度系统，是苹果为多核并行运算提出的C语言并发技术框架。

Grand Central Dispatch（GCD） 是 Apple 开发的一个多核编程的较新的解决方法。它主要用于优化应用程序以支持多核处理器以及其他对称多处理系统。它是一个在线程池模式的基础上执行的并发任务。在 Mac OS X 10.6 雪豹中首次推出，也可在 iOS 4 及以上版本使用。

## 1：GCD的特点

- GCD可用于多核的并行运算
- GCD会自动利用更多的CPU内核（比如双核、四核）
- GCD自动管理线程的生命周期（创建线程，调度任务，销毁线程等）
- 程序员只需要告诉 GCD 想要如何执行什么任务，不需要编写任何线程管理代码

## 2：GCD的基本概念

**任务（block）**：就是将要在线程中执行的代码，将这段代码用block封装好，然后将这个任务添加到指定的执行方式（同步执行和异步执行），等待CPU从队列中取出任务放到对应的线程中执行。

同步执行（sync）：
同步添加任务到指定的队列中，在添加的任务执行结束之前，会一直等待，直到队列里面的任务完成之后再继续执行。
只能在当前线程中执行任务，不具备开启新线程的能力。

异步执行（async）：
异步添加任务到指定的队列中，它不会做任何等待，可以继续执行任务。
可以在新的线程中执行任务，具备开启新线程的能力。

举个简单例子：你要打电话给小明和小白。

> 『同步执行』 就是：你打电话给小明的时候，不能同时打给小白。只有等到给小明打完了，才能打给小白（等待任务执行结束）。而且只能用当前的电话（不具备开启新线程的能力）。
>
> 『异步执行』 就是：你打电话给小明的时候，不用等着和小明通话结束（不用等待任务执行结束），还能同时给小白打电话。而且除了当前电话，你还可以使用其他一个或多个电话（具备开启新线程的能力）。

**队列（Dispatch Queue）**：这里的队列指执行任务的等待队列，即用来存放任务的队列。队列是一种特殊的线性表，采用 FIFO（先进先出）的原则，即新任务总是被插入到队列的末尾，而读取任务的时候总是从队列的头部开始读取。每读取一个任务，则从队列中释放一个任务。

在 GCD 中有两种队列：『串行队列』 和 『并发队列』。两者都符合 FIFO（先进先出）的原则。两者的主要区别是：执行顺序不同，以及开启线程数不同。

串行队列（Serial Dispatch Queue）：
每次只有一个任务被执行。让任务一个接着一个地执行。（只开启一个线程，一个任务执行完毕后，再执行下一个任务）

并发队列（Concurrent Dispatch Queue）：
可以让多个任务并发（同时）执行。（可以开启多个线程，并且同时执行任务）

注意：并发队列 的并发功能只有在异步（dispatch_async）方法下才有效。

## 3：队列的创建/获取方法

- 使用`dispatch_queue_create`来创建队列对象，传入两个参数，第一个参数表示队列的唯一标识符，可为空。第二个参数用来表示串行队列`（DISPATCH_QUEUE_SERIAL）`或并发队列`（DISPATCH_QUEUE_CONCURRENT）`。

```
// 串行队列
dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_SERIAL);
// 并发队列
dispatch_queue_t queue1 = dispatch_queue_create("test", DISPATCH_QUEUE_CONCURRENT);
```

GCD的队列还有另外两种：

- 主队列：主队列负责在主线程上调度任务，如果在主线程上已经有任务正在执行，主队列会等到主线程空闲后再调度任务。通常是返回主线程更新UI的时候使用`dispatch_get_main_queue()`.

```
 dispatch_async(dispatch_get_global_queue(0, 0), ^{
      // 耗时操作放在这里

      dispatch_async(dispatch_get_main_queue(), ^{
          // 回到主线程进行UI操作

      });
  });
```

- 全局并发队列：全局并发队列`dispatch_get_global_queue(0, 0)`就是一个并发队列，是为了让我们更方便的使用多线程。

```
//全局并发队列
dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
//全局并发队列的优先级
#define DISPATCH_QUEUE_PRIORITY_HIGH 2 // 高优先级
#define DISPATCH_QUEUE_PRIORITY_DEFAULT 0 // 默认（中）优先级
#define DISPATCH_QUEUE_PRIORITY_LOW (-2) // 低优先级
#define DISPATCH_QUEUE_PRIORITY_BACKGROUND INT16_MIN // 后台优先级
//iOS8开始使用服务质量，现在获取全局并发队列时，可以直接传0
dispatch_get_global_queue(0, 0);
```

## 4：同步/异步/任务、创建方式

同步（sync）使用dispatch_sync来表示。 异步（async）使用dispatch_async。 任务就是将要在线程中执行的代码，将这段代码用block封装好。 代码如下：

```
// 同步执行任务
dispatch_sync(dispatch_get_global_queue(0, 0), ^{
    // 任务放在这个block里
    NSLog(@"我是同步执行的任务");
});
// 异步执行任务
dispatch_async(dispatch_get_global_queue(0, 0), ^{
    // 任务放在这个block里
    NSLog(@"我是异步执行的任务");
});
```

## 5：GCD的使用

GCD 的使用步骤其实很简单，只有两步：

1. 创建一个队列（串行队列或并发队列）；
2. 将任务追加到任务的等待队列中，然后系统就会根据任务类型执行任务（同步执行或异步执行）。

由于有多种队列（串行/并发/主队列）和两种执行方式（同步/异步），所以他们之间可以有多种组合方式。

虽然使用 GCD 只需两步，但是既然我们有两种队列（串行队列 / 并发队列），两种任务执行方式（同步执行 / 异步执行），那么我们就有了四种不同的组合方式。这四种不同的组合方式是：

1. 同步执行 + 并发队列
2. 异步执行 + 并发队列
3. 同步执行 + 串行队列
4. 异步执行 + 串行队列

实际上，刚才还说了两种特殊队列：全局并发队列、主队列。全局并发队列可以作为普通并发队列来使用。但是主队列因为有点特殊，所以我们就又多了两种组合方式。这样就有六种不同的组合方式了。

1. 同步执行 + 主队列
2. 异步执行 + 主队列

- 串行同步 执行完一个任务，再执行下一个任务。不开启新线程。

```
/** 串行同步 */
- (void)syncSerial {

    NSLog(@"\n\n**************串行同步***************\n\n");

    // 串行队列
    dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_SERIAL);

    // 同步执行
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"串行同步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"串行同步2   %@",[NSThread currentThread]);
        }
    });
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"串行同步3   %@",[NSThread currentThread]);
        }
    });
}
```

输入结果为顺序执行，都在主线程：

```
串行同步1   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步1   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步1   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步2   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步2   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步2   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步3   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步3   <NSThread: 0x60000007c500>{number = 1, name = main}
串行同步3   <NSThread: 0x60000007c500>{number = 1, name = main}
```

- 串行异步 开启新线程，但因为任务是串行的，所以还是按顺序执行任务。

```
/** 串行异步 */
- (void)asyncSerial {

    NSLog(@"\n\n**************串行异步***************\n\n");

    // 串行队列
    dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_SERIAL);

    // 同步执行
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"串行异步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"串行异步2   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"串行异步3   %@",[NSThread currentThread]);
        }
    });
}
```

输入结果为顺序执行，有不同线程：

```
串行异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步2   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步2   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步2   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步3   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步3   <NSThread: 0x60000026d740>{number = 3, name = (null)}
串行异步3   <NSThread: 0x60000026d740>{number = 3, name = (null)
```

- 并发同步 因为是同步的，所以执行完一个任务，再执行下一个任务。不会开启新线程。

```
/** 并发同步 */
- (void)syncConcurrent {

    NSLog(@"\n\n**************并发同步***************\n\n");

    // 并发队列
    dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_CONCURRENT);

    // 同步执行
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"并发同步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"并发同步2   %@",[NSThread currentThread]);
        }
    });
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"并发同步3   %@",[NSThread currentThread]);
        }
    });
}
```

输入结果为顺序执行，都在主线程：

```
并发同步1   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步1   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步1   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步2   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步2   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步2   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步3   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步3   <NSThread: 0x60000007c500>{number = 1, name = main}
并发同步3   <NSThread: 0x60000007c500>{number = 1, name = main}
```

- 并发异步 任务交替执行，开启多线程。

```
/** 并发异步 */
- (void)asyncConcurrent {

    NSLog(@"\n\n**************并发异步***************\n\n");

    // 并发队列
    dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_CONCURRENT);

    // 同步执行
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"并发异步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"并发异步2   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"并发异步3   %@",[NSThread currentThread]);
        }
    });
}
```

输入结果为无序执行，有多条线程：

```
并发异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
并发异步2   <NSThread: 0x60000026dc80>{number = 4, name = (null)}
并发异步3   <NSThread: 0x60800026ab40>{number = 5, name = (null)}
并发异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
并发异步2   <NSThread: 0x60000026dc80>{number = 4, name = (null)}
并发异步3   <NSThread: 0x60800026ab40>{number = 5, name = (null)}
并发异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
并发异步2   <NSThread: 0x60000026dc80>{number = 4, name = (null)}
并发异步3   <NSThread: 0x60800026ab40>{number = 5, name = (null)}
```

- 主队列同步 如果在主线程中运用这种方式，则会发生死锁，程序崩溃。

```
/** 主队列同步 */
- (void)syncMain {

    NSLog(@"\n\n**************主队列同步，放到主线程会死锁***************\n\n");

    // 主队列
    dispatch_queue_t queue = dispatch_get_main_queue();

    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"主队列同步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"主队列同步2   %@",[NSThread currentThread]);
        }
    });
    dispatch_sync(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"主队列同步3   %@",[NSThread currentThread]);
        }
    });
}
```

**主队列同步造成死锁的原因**：

如果在主线程中运用主队列同步，也就是把任务放到了主线程的队列中。 而同步对于任务是立刻执行的，那么当把第一个任务放进主队列时，它就会立马执行。 可是主线程现在正在处理syncMain方法，任务需要等syncMain执行完才能执行。 syncMain执行到第一个任务的时候，又要等第一个任务执行完才能往下执行第二个和第三个任务。这样syncMain方法和第一个任务就开始了互相等待，形成了死锁。

- 主队列异步 在主线程中任务按顺序执行。

```
/** 主队列异步 */
- (void)asyncMain {

    NSLog(@"\n\n**************主队列异步***************\n\n");

    // 主队列
    dispatch_queue_t queue = dispatch_get_main_queue();

    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"主队列异步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"主队列异步2   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"主队列异步3   %@",[NSThread currentThread]);
        }
    });
}
```

输入结果为在主线程中按顺序执行：

```
主队列异步1   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步1   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步1   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步2   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步2   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步2   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步3   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步3   <NSThread: 0x60000007c500>{number = 1, name = main}
主队列异步3   <NSThread: 0x60000007c500>{number = 1, name = main}
```

- GCD线程之间的通讯

开发中需要在主线程上进行UI的相关操作，通常会把一些耗时的操作放在其他线程，比如说图片文件下载等耗时操作。 当完成了耗时操作之后，需要回到主线程进行UI的处理，这里就用到了线程之间的通讯。

```
- (IBAction)communicationBetweenThread:(id)sender {
    // 异步
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        // 耗时操作放在这里，例如下载图片。（运用线程休眠两秒来模拟耗时操作）
        [NSThread sleepForTimeInterval:2];
        NSString *picURLStr = @"http://www.bangmangxuan.net/uploads/allimg/160320/74-160320130500.jpg";
        NSURL *picURL = [NSURL URLWithString:picURLStr];
        NSData *picData = [NSData dataWithContentsOfURL:picURL];
        UIImage *image = [UIImage imageWithData:picData];
        // 回到主线程处理UI
        dispatch_async(dispatch_get_main_queue(), ^{
            // 在主线程上添加图片
            self.imageView.image = image;
        });
    });
}
```

上面的代码是在新开的线程中进行图片的下载，下载完成之后回到主线程显示图片。

- GCD栅栏

当任务需要异步进行，但是这些任务需要分成两组来执行，第一组完成之后才能进行第二组的操作。这时候就用了到GCD的栅栏方法`dispatch_barrier_async`。

```
- (IBAction)barrierGCD:(id)sender {

    // 并发队列
    dispatch_queue_t queue = dispatch_queue_create("test", DISPATCH_QUEUE_CONCURRENT);

    // 异步执行
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"栅栏：并发异步1   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"栅栏：并发异步2   %@",[NSThread currentThread]);
        }
    });

    dispatch_barrier_async(queue, ^{
        NSLog(@"------------barrier------------%@", [NSThread currentThread]);
        NSLog(@"******* 并发异步执行，但是34一定在12后面 *********");
    });

    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"栅栏：并发异步3   %@",[NSThread currentThread]);
        }
    });
    dispatch_async(queue, ^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"栅栏：并发异步4   %@",[NSThread currentThread]);
        }
    });
}
```

上面代码的打印结果如下，开启了多条线程，所有任务都是并发异步进行。但是第一组完成之后，才会进行第二组的操作。

```
栅栏：并发异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
栅栏：并发异步2   <NSThread: 0x60000026e480>{number = 6, name = (null)}
栅栏：并发异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
栅栏：并发异步2   <NSThread: 0x60000026e480>{number = 6, name = (null)}
栅栏：并发异步1   <NSThread: 0x60000026d740>{number = 3, name = (null)}
栅栏：并发异步2   <NSThread: 0x60000026e480>{number = 6, name = (null)}
 ------------barrier------------<NSThread: 0x60000026e480>{number = 6, name = (null)}
******* 并发异步执行，但是34一定在12后面 *********
栅栏：并发异步4   <NSThread: 0x60000026d740>{number = 3, name = (null)}
栅栏：并发异步3   <NSThread: 0x60000026e480>{number = 6, name = (null)}
栅栏：并发异步4   <NSThread: 0x60000026d740>{number = 3, name = (null)}
栅栏：并发异步3   <NSThread: 0x60000026e480>{number = 6, name = (null)}
栅栏：并发异步4   <NSThread: 0x60000026d740>{number = 3, name = (null)}
栅栏：并发异步3   <NSThread: 0x60000026e480>{number = 6, name = (null)}
```

- GCD延时执行

当需要等待一会再执行一段代码时，就可以用到这个方法了：dispatch_after。

```
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(5.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
    // 5秒后异步执行
    NSLog(@"我已经等待了5秒！");
});
```

- GCD实现代码只执行一次

使用dispatch_once能保证某段代码在程序运行过程中只被执行1次。可以用来设计单例。

```
static dispatch_once_t onceToken;
dispatch_once(&onceToken, ^{
    NSLog(@"程序运行过程中我只执行了一次！");
});
```

- GCD快速迭代

GCD有一个快速迭代的方法dispatch_apply，dispatch_apply可以同时遍历多个数字。

```
- (IBAction)applyGCD:(id)sender {

    NSLog(@"\n\n************** GCD快速迭代 ***************\n\n");

    // 并发队列
    dispatch_queue_t queue = dispatch_get_global_queue(0, 0);

    // dispatch_apply几乎同时遍历多个数字
    dispatch_apply(7, queue, ^(size_t index) {
        NSLog(@"dispatch_apply：%zd======%@",index, [NSThread currentThread]);
    });
}
```

打印结果如下：

```
dispatch_apply：0======<NSThread: 0x60000007c500>{number = 1, name = main}
dispatch_apply：1======<NSThread: 0x60000007c500>{number = 1, name = main}
dispatch_apply：2======<NSThread: 0x60000007c500>{number = 1, name = main}
dispatch_apply：3======<NSThread: 0x60000007c500>{number = 1, name = main}
dispatch_apply：4======<NSThread: 0x60000007c500>{number = 1, name = main}
dispatch_apply：5======<NSThread: 0x60000007c500>{number = 1, name = main}
dispatch_apply：6======<NSThread: 0x60000007c500>{number = 1, name = main}
```

通常我们会用 for 循环遍历，但是 GCD 给我们提供了快速迭代的方法 `dispatch_apply。dispatch_apply` 按照指定的次数将指定的任务追加到指定的队列中，并等待全部队列执行结束。
如果是在串行队列中使用 `dispatch_apply`，那么就和 `for` 循环一样，按顺序同步执行。但是这样就体现不出快速迭代的意义了。

我们可以利用并发队列进行异步执行。比如说遍历 0~5 这 6 个数字，`for` 循环的做法是每次取出一个元素，逐个遍历。`dispatch_apply` 可以 在多个线程中同时（异步）遍历多个数字。

还有一点，无论是在串行队列，还是并发队列中，`dispatch_apply` 都会等待全部任务执行完毕，这点就像是同步操作，也像是队列组中的 `dispatch_group_wait`方法。

```
/**
 * 快速迭代方法 dispatch_apply
 */
- (void)apply {
    dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);

    NSLog(@"apply---begin");
    dispatch_apply(6, queue, ^(size_t index) {
        NSLog(@"%zd---%@",index, [NSThread currentThread]);
    });
    NSLog(@"apply---end");
}
```

```
输出结果：
2019-08-08 15:05:04.715266+0800 YSC-GCD-demo[17771:4285619] apply—-begin
2019-08-08 15:05:04.715492+0800 YSC-GCD-demo[17771:4285619] 0—-{number = 1, name = main}
2019-08-08 15:05:04.715516+0800 YSC-GCD-demo[17771:4285722] 1—-{number = 3, name = (null)}
2019-08-08 15:05:04.715526+0800 YSC-GCD-demo[17771:4285720] 3—-{number = 5, name = (null)}
2019-08-08 15:05:04.715564+0800 YSC-GCD-demo[17771:4285721] 2—-{number = 7, name = (null)}
2019-08-08 15:05:04.715555+0800 YSC-GCD-demo[17771:4285719] 4—-{number = 6, name = (null)}
2019-08-08 15:05:04.715578+0800 YSC-GCD-demo[17771:4285728] 5—-{number = 4, name = (null)}
2019-08-08 15:05:04.715677+0800 YSC-GCD-demo[17771:4285619] apply—-end
```

因为是在并发队列中异步执行任务，所以各个任务的执行时间长短不定，最后结束顺序也不定。但是 apply---end 一定在最后执行。这是因为 dispatch_apply 方法会等待全部任务执行完毕。

- GCD队列组

异步执行几个耗时操作，当这几个操作都完成之后再回到主线程进行操作，就可以用到队列组了。 队列组有下面几个特点：

队列组示例代码：

```
- (void)testGroup {
    dispatch_group_t group =  dispatch_group_create();

    dispatch_group_async(group, dispatch_get_global_queue(0, 0), ^{
        NSLog(@"队列组：有一个耗时操作完成！");
    });

    dispatch_group_async(group, dispatch_get_global_queue(0, 0), ^{
        NSLog(@"队列组：有一个耗时操作完成！");
    });

    dispatch_group_notify(group, dispatch_get_main_queue(), ^{
        NSLog(@"队列组：前面的耗时操作都完成了，回到主线程进行相关操作");
    });
}
```

打印结果如下：

```
队列组：有一个耗时操作完成！
队列组：有一个耗时操作完成！
队列组：前面的耗时操作都完成了，回到主线程进行相关操作
```

- GCD 信号量：`dispatch_semaphore`

GCD 中的信号量是指 `Dispatch Semaphore`，是持有计数的信号。类似于过高速路收费站的栏杆。可以通过时，打开栏杆，不可以通过时，关闭栏杆。在 `Dispatch Semaphore` 中，使用计数来完成这个功能，计数小于 0 时等待，不可通过。计数为 0 或大于 0 时，计数减 1 且不等待，可通过。
`Dispatch Semaphore` 提供了三个方法：

> - `dispatch_semaphore_create`：创建一个 Semaphore 并初始化信号的总量
> - `dispatch_semaphore_signal`：发送一个信号，让信号总量加 1
> - `dispatch_semaphore_wait`：可以使总信号量减 1，信号总量小于 0 时就会一直等待（阻塞所在线程），否则就可以正常执行。

> 注意：信号量的使用前提是：想清楚你需要处理哪个线程等待（阻塞），又要哪个线程继续执行，然后使用信号量。

`Dispatch Semaphore` 在实际开发中主要用于：

- 保持线程同步，将异步执行任务转换为同步执行任务
- 保证线程安全，为线程加锁


**`Dispatch Semaphore` 线程同步**

我们在开发中，会遇到这样的需求：异步执行耗时任务，并使用异步执行的结果进行一些额外的操作。换句话说，相当于，将将异步执行任务转换为同步执行任务。比如说：AFNetworking 中 `AFURLSessionManager.m` 里面的 `tasksForKeyPath:` 方法。通过引入信号量的方式，等待异步执行任务结果，获取到 tasks，然后再返回该 tasks。

```
- (NSArray *)tasksForKeyPath:(NSString *)keyPath {
    __block NSArray *tasks = nil;
    dispatch_semaphore_t semaphore = dispatch_semaphore_create(0);
    [self.session getTasksWithCompletionHandler:^(NSArray *dataTasks, NSArray *uploadTasks, NSArray *downloadTasks) {
        if ([keyPath isEqualToString:NSStringFromSelector(@selector(dataTasks))]) {
            tasks = dataTasks;
        } else if ([keyPath isEqualToString:NSStringFromSelector(@selector(uploadTasks))]) {
            tasks = uploadTasks;
        } else if ([keyPath isEqualToString:NSStringFromSelector(@selector(downloadTasks))]) {
            tasks = downloadTasks;
        } else if ([keyPath isEqualToString:NSStringFromSelector(@selector(tasks))]) {
            tasks = [@[dataTasks, uploadTasks, downloadTasks] valueForKeyPath:@"@unionOfArrays.self"];
        }
        dispatch_semaphore_signal(semaphore);
    }];
    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
    return tasks;
}
```

下面，我们来利用 `Dispatch Semaphore` 实现线程同步，将异步执行任务转换为同步执行任务。

```
/**
 * semaphore 线程同步
 */
- (void)semaphoreSync {

    NSLog(@"currentThread---%@",[NSThread currentThread]);  // 打印当前线程
    NSLog(@"semaphore---begin");

    dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    dispatch_semaphore_t semaphore = dispatch_semaphore_create(0);

    __block int number = 0;
    dispatch_async(queue, ^{
        // 追加任务 1
        [NSThread sleepForTimeInterval:2];              // 模拟耗时操作
        NSLog(@"1---%@",[NSThread currentThread]);      // 打印当前线程

        number = 100;

        dispatch_semaphore_signal(semaphore);
    });

    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
    NSLog(@"semaphore---end,number = %zd",number);
}
```

输出结果：

```
2019-08-08 15:16:56.781543+0800 YSC-GCD-demo[17988:4325744] currentThread—-{number = 1, name = main}
2019-08-08 15:16:56.781698+0800 YSC-GCD-demo[17988:4325744] semaphore—-begin
2019-08-08 15:16:58.785232+0800 YSC-GCD-demo[17988:4325867] 1—-{number = 3, name = (null)}
2019-08-08 15:16:58.785432+0800 YSC-GCD-demo[17988:4325744] semaphore—-end,number = 100
```

从 `Dispatch Semaphore` 实现线程同步的代码可以看到：

semaphore---end 是在执行完 number = 100; 之后才打印的。而且输出结果 number 为 100。这是因为 异步执行 不会做任何等待，可以继续执行任务。
执行顺如下：

> 1. semaphore 初始创建时计数为 0。
> 2. 异步执行 将 任务 1 追加到队列之后，不做等待，接着执行 `dispatch_semaphore_wait` 方法，semaphore 减 1，此时 semaphore == -1，当前线程进入等待状态。
> 3. 然后，异步任务 1 开始执行。任务 1 执行到 `dispatch_semaphore_signal` 之后，总信号量加 1，此时 semaphore == 0，正在被阻塞的线程（主线程）恢复继续执行。
> 4. 最后打印 semaphore---end,number = 100。

这样就实现了线程同步，将异步执行任务转换为同步执行任务。

**`Dispatch Semaphore` 线程安全和线程同步（为线程加锁）**

**线程安全**：如果你的代码所在的进程中有多个线程在同时运行，而这些线程可能会同时运行这段代码。如果每次运行结果和单线程运行的结果是一样的，而且其他的变量的值也和预期的是一样的，就是线程安全的。

若每个线程中对全局变量、静态变量只有读操作，而无写操作，一般来说，这个全局变量是线程安全的；若有多个线程同时执行写操作（更改变量），一般都需要考虑线程同步，否则的话就可能影响线程安全。

**线程同步**：可理解为线程 A 和 线程 B 一块配合，A 执行到一定程度时要依靠线程 B 的某个结果，于是停下来，示意 B 运行；B 依言执行，再将结果给 A；A 再继续操作。

举个简单例子就是：两个人在一起聊天。两个人不能同时说话，避免听不清(操作冲突)。等一个人说完(一个线程结束操作)，另一个再说(另一个线程再开始操作)。

下面，我们模拟火车票售卖的方式，实现 NSThread 线程安全和解决线程同步问题。

场景：总共有 50 张火车票，有两个售卖火车票的窗口，一个是北京火车票售卖窗口，另一个是上海火车票售卖窗口。两个窗口同时售卖火车票，卖完为止。

**非线程安全（不使用 SEMAPHORE）**

```
/**
 * 非线程安全：不使用 semaphore
 * 初始化火车票数量、卖票窗口（非线程安全）、并开始卖票
 */
- (void)initTicketStatusNotSave {
    NSLog(@"currentThread---%@",[NSThread currentThread]);  // 打印当前线程
    NSLog(@"semaphore---begin");

    self.ticketSurplusCount = 50;

    // queue1 代表北京火车票售卖窗口
    dispatch_queue_t queue1 = dispatch_queue_create("net.bujige.testQueue1", DISPATCH_QUEUE_SERIAL);
    // queue2 代表上海火车票售卖窗口
    dispatch_queue_t queue2 = dispatch_queue_create("net.bujige.testQueue2", DISPATCH_QUEUE_SERIAL);

    __weak typeof(self) weakSelf = self;
    dispatch_async(queue1, ^{
        [weakSelf saleTicketNotSafe];
    });

    dispatch_async(queue2, ^{
        [weakSelf saleTicketNotSafe];
    });
}

/**
 * 售卖火车票（非线程安全）
 */
- (void)saleTicketNotSafe {
    while (1) {

        if (self.ticketSurplusCount > 0) {  // 如果还有票，继续售卖
            self.ticketSurplusCount--;
            NSLog(@"%@", [NSString stringWithFormat:@"剩余票数：%d 窗口：%@", self.ticketSurplusCount, [NSThread currentThread]]);
            [NSThread sleepForTimeInterval:0.2];
        } else { // 如果已卖完，关闭售票窗口
            NSLog(@"所有火车票均已售完");
            break;
        }

    }
}
```

输出结果（部分）：

```
2019-08-08 15:21:39.772655+0800 YSC-GCD-demo[18071:4340555] currentThread—-{number = 1, name = main}
2019-08-08 15:21:39.772790+0800 YSC-GCD-demo[18071:4340555] semaphore—-begin
2019-08-08 15:21:39.773101+0800 YSC-GCD-demo[18071:4340604] 剩余票数：48 窗口：{number = 4, name = (null)}
2019-08-08 15:21:39.773115+0800 YSC-GCD-demo[18071:4340605] 剩余票数：49 窗口：{number = 3, name = (null)}
2019-08-08 15:21:39.975041+0800 YSC-GCD-demo[18071:4340605] 剩余票数：47 窗口：{number = 3, name = (null)}
2019-08-08 15:21:39.975037+0800 YSC-GCD-demo[18071:4340604] 剩余票数：47 窗口：{number = 4, name = (null)}
2019-08-08 15:21:40.176567+0800 YSC-GCD-demo[18071:4340604] 剩余票数：46 窗口：{number = 4, name = (null)}
```

可以看到在不考虑线程安全，不使用 semaphore 的情况下，得到票数是错乱的，这样显然不符合我们的需求，所以我们需要考虑线程安全问题。

**线程安全（使用 SEMAPHORE 加锁）**

```
/**
 * 线程安全：使用 semaphore 加锁
 * 初始化火车票数量、卖票窗口（线程安全）、并开始卖票
 */
- (void)initTicketStatusSave {
    NSLog(@"currentThread---%@",[NSThread currentThread]);  // 打印当前线程
    NSLog(@"semaphore---begin");

    semaphoreLock = dispatch_semaphore_create(1);

    self.ticketSurplusCount = 50;

    // queue1 代表北京火车票售卖窗口
    dispatch_queue_t queue1 = dispatch_queue_create("net.bujige.testQueue1", DISPATCH_QUEUE_SERIAL);
    // queue2 代表上海火车票售卖窗口
    dispatch_queue_t queue2 = dispatch_queue_create("net.bujige.testQueue2", DISPATCH_QUEUE_SERIAL);

    __weak typeof(self) weakSelf = self;
    dispatch_async(queue1, ^{
        [weakSelf saleTicketSafe];
    });

    dispatch_async(queue2, ^{
        [weakSelf saleTicketSafe];
    });
}

/**
 * 售卖火车票（线程安全）
 */
- (void)saleTicketSafe {
    while (1) {
        // 相当于加锁
        dispatch_semaphore_wait(semaphoreLock, DISPATCH_TIME_FOREVER);

        if (self.ticketSurplusCount > 0) {  // 如果还有票，继续售卖
            self.ticketSurplusCount--;
            NSLog(@"%@", [NSString stringWithFormat:@"剩余票数：%d 窗口：%@", self.ticketSurplusCount, [NSThread currentThread]]);
            [NSThread sleepForTimeInterval:0.2];
        } else { // 如果已卖完，关闭售票窗口
            NSLog(@"所有火车票均已售完");

            // 相当于解锁
            dispatch_semaphore_signal(semaphoreLock);
            break;
        }

        // 相当于解锁
        dispatch_semaphore_signal(semaphoreLock);
    }
}
```

输出结果为：

```
2019-08-08 15:23:58.819891+0800 YSC-GCD-demo[18116:4348091] currentThread—-{number = 1, name = main}
2019-08-08 15:23:58.820041+0800 YSC-GCD-demo[18116:4348091] semaphore—-begin
2019-08-08 15:23:58.820305+0800 YSC-GCD-demo[18116:4348159] 剩余票数：49 窗口：{number = 3, name = (null)}
2019-08-08 15:23:59.022165+0800 YSC-GCD-demo[18116:4348157] 剩余票数：48 窗口：{number = 4, name = (null)}
2019-08-08 15:23:59.225299+0800 YSC-GCD-demo[18116:4348159] 剩余票数：47 窗口：{number = 3, name = (null)}
…
2019-08-08 15:24:08.355977+0800 YSC-GCD-demo[18116:4348157] 剩余票数：2 窗口：{number = 4, name = (null)}
2019-08-08 15:24:08.559201+0800 YSC-GCD-demo[18116:4348159] 剩余票数：1 窗口：{number = 3, name = (null)}
2019-08-08 15:24:08.759630+0800 YSC-GCD-demo[18116:4348157] 剩余票数：0 窗口：{number = 4, name = (null)}
2019-08-08 15:24:08.965100+0800 YSC-GCD-demo[18116:4348159] 所有火车票均已售完
2019-08-08 15:24:08.965440+0800 YSC-GCD-demo[18116:4348157] 所有火车票均已售完
```

可以看出，在考虑了线程安全的情况下，使用 `dispatch_semaphore`机制之后，得到的票数是正确的，没有出现混乱的情况。我们也就解决了多个线程同步的问题。


# NSOperation的使用

## 1：NSOperation简介

`NSOperation`是基于GCD之上的更高一层封装，`NSOperation`需要配合`NSOperationQueue`来实现多线程。

`NSOperation`、`NSOperationQueue` 是苹果提供给我们的一套多线程解决方案。实际上 `NSOperation`、`NSOperationQueue` 是基于 GCD 更高一层的封装，完全面向对象。但是比 GCD 更简单易用、代码可读性也更高。

为什么要使用 `NSOperation`、`NSOperationQueue`？

1. 可添加完成的代码块，在操作完成后执行。
2. 添加操作之间的依赖关系，方便的控制执行顺序。
3. 设定操作执行的优先级。
4. 可以很方便的取消一个操作的执行。
5. 使用 KVO 观察对操作执行状态的更改：`isExecuteing`、`isFinished`、`isCancelled`。

既然是基于 GCD 的更高一层的封装。那么，GCD 中的一些概念同样适用于 `NSOperation`、`NSOperationQueue`。在 `NSOperation`、`NSOperationQueue` 中也有类似的任务（操作）和队列（操作队列）的概念。

- 操作（Operation）：

1. 执行操作的意思，换句话说就是你在线程中执行的那段代码。
2. 在 GCD 中是放在 block 中的。在 NSOperation 中，我们使用 NSOperation 子类 NSInvocationOperation、NSBlockOperation，或者自定义子类来封装操作。

- 操作队列（Operation Queues）：

1. 这里的队列指操作队列，即用来存放操作的队列。不同于 GCD 中的调度队列 FIFO（先进先出）的原则。NSOperationQueue 对于添加到队列中的操作，首先进入准备就绪的状态（就绪状态取决于操作之间的依赖关系），然后进入就绪状态的操作的开始执行顺序（非结束执行顺序）由操作之间相对的优先级决定（优先级是操作对象自身的属性）。
2. 操作队列通过设置最大并发操作数（maxConcurrentOperationCount）来控制并发、串行。
3. NSOperationQueue 为我们提供了两种不同类型的队列：主队列和自定义队列。主队列运行在主线程之上，而自定义队列在后台执行。

NSOperation实现多线程的步骤如下：

> 1. 创建任务：先将需要执行的操作封装到NSOperation对象中。
> 2. 创建队列：创建NSOperationQueue。
> 3. 将任务加入到队列中：将NSOperation对象添加到NSOperationQueue中。

需要注意的是，NSOperation是个抽象类，实际运用时中需要使用它的子类，有三种方式：

> 1. 使用子类NSInvocationOperation
> 2. 使用子类NSBlockOperation
> 3. 定义继承自NSOperation的子类，通过实现内部相应的方法来封装任务。

## 2：NSOperation的三种创建方式

- NSInvocationOperation的使用 创建NSInvocationOperation对象并关联方法，之后start。

```
- (void)testNSInvocationOperation {
    // 创建NSInvocationOperation
    NSInvocationOperation *invocationOperation = [[NSInvocationOperation alloc] initWithTarget:self selector:@selector(invocationOperation) object:nil];
    // 开始执行操作
    [invocationOperation start];
}

- (void)invocationOperation {
    NSLog(@"NSInvocationOperation包含的任务，没有加入队列========%@", [NSThread currentThread]);
}
```

打印结果如下，得到结论：程序在主线程执行，没有开启新线程。 这是因为NSOperation多线程的使用需要配合队列NSOperationQueue，后面会讲到NSOperationQueue的使用。

```
NSInvocationOperation包含的任务，没有加入队列========<NSThread: 0x6000000783c0>{number = 1, name = main}

```

- NSBlockOperation的使用 把任务放到NSBlockOperation的block中，然后start。

```
- (void)testNSBlockOperation {
    // 把任务放到block中
    NSBlockOperation *blockOperation = [NSBlockOperation blockOperationWithBlock:^{
        NSLog(@"NSBlockOperation包含的任务，没有加入队列========%@", [NSThread currentThread]);
    }];

    [blockOperation start];
}
```

执行结果如下，可以看出：主线程执行，没有开启新线程。 同样的，NSBlockOperation可以配合队列NSOperationQueue来实现多线程。

```
NSBlockOperation包含的任务，没有加入队列========<NSThread: 0x6000000783c0>{number = 1, name = main}
```

但是NSBlockOperation有一个方法`addExecutionBlock:`，通过这个方法可以让NSBlockOperation实现多线程。

```
- (void)testNSBlockOperationExecution {
    NSBlockOperation *blockOperation = [NSBlockOperation blockOperationWithBlock:^{
        NSLog(@"NSBlockOperation运用addExecutionBlock主任务========%@", [NSThread currentThread]);
    }];

    [blockOperation addExecutionBlock:^{
        NSLog(@"NSBlockOperation运用addExecutionBlock方法添加任务1========%@", [NSThread currentThread]);
    }];
    [blockOperation addExecutionBlock:^{
        NSLog(@"NSBlockOperation运用addExecutionBlock方法添加任务2========%@", [NSThread currentThread]);
    }];
    [blockOperation addExecutionBlock:^{
        NSLog(@"NSBlockOperation运用addExecutionBlock方法添加任务3========%@", [NSThread currentThread]);
    }];

    [blockOperation start];
}
```

执行结果如下，可以看出，NSBlockOperation创建时block中的任务是在主线程执行，而运用`addExecutionBlock`加入的任务是在子线程执行的。

```
NSBlockOperation运用addExecutionBlock========<NSThread: 0x60800006ccc0>{number = 1, name = main}
addExecutionBlock方法添加任务1========<NSThread: 0x60800007ec00>{number = 3, name = (null)}
addExecutionBlock方法添加任务3========<NSThread: 0x6000002636c0>{number = 5, name = (null)}
addExecutionBlock方法添加任务2========<NSThread: 0x60800007e800>{number = 4, name = (null)}
```

- 运用继承自NSOperation的子类

首先我们定义一个继承自NSOperation的类，然后重写它的main方法，之后就可以使用这个子类来进行相关的操作了。

```
/*******************"WHOperation.h"*************************/

#import <Foundation/Foundation.h>

@interface WHOperation : NSOperation

@end

/*******************"WHOperation.m"*************************/

#import "WHOperation.h"

@implementation WHOperation

- (void)main {
    for (int i = 0; i < 3; i++) {
        NSLog(@"NSOperation的子类WHOperation======%@",[NSThread currentThread]);
    }
}

@end

/*****************回到主控制器使用WHOperation**********************/

- (void)testWHOperation {
    WHOperation *operation = [[WHOperation alloc] init];
    [operation start];
}
```

运行结果如下，依然是在主线程执行。

```
SOperation的子类WHOperation======<NSThread: 0x608000066780>{number = 1, name = main}
NSOperation的子类WHOperation======<NSThread: 0x608000066780>{number = 1, name = main}
NSOperation的子类WHOperation======<NSThread: 0x608000066780>{number = 1, name = main}
```

所以，NSOperation是需要配合队列NSOperationQueue来实现多线程的。下面就来说一下队列NSOperationQueue。

## 3：队列NSOperationQueue

NSOperationQueue只有两种队列：主队列、其他队列。其他队列包含了串行和并发。

主队列的创建如下，主队列上的任务是在主线程执行的。

```
NSOperationQueue *mainQueue = [NSOperationQueue mainQueue];
```

其他队列（非主队列）的创建如下，加入到‘非队列’中的任务默认就是并发，开启多线程。

```
NSOperationQueue *queue = [[NSOperationQueue alloc] init];
```

注意：

1. 非主队列（其他队列）可以实现串行或并行。
2. 队列NSOperationQueue有一个参数叫做最大并发数：`maxConcurrentOperationCount`。
3. `maxConcurrentOperationCount`默认为-1，直接并发执行，所以加入到‘非队列’中的任务默认就是并发，开启多线程。
4. 当`maxConcurrentOperationCount`为1时，则表示不开线程，也就是串行。
5. 当`maxConcurrentOperationCount`大于1时，进行并发执行。
6. 系统对最大并发数有一个限制，所以即使程序员把`maxConcurrentOperationCount`设置的很大，系统也会自动调整。所以把最大并发数设置的很大是没有意义的。

## 4：NSOperation + NSOperationQueue

把任务加入队列，这才是NSOperation的常规使用方式。

- `addOperation`添加任务到队列

先创建好任务，然后运用`- (void)addOperation:(NSOperation *)op` 方法来吧任务添加到队列中，示例代码如下：

```
- (void)testOperationQueue {
    // 创建队列，默认并发
    NSOperationQueue *queue = [[NSOperationQueue alloc] init];

    // 创建操作，NSInvocationOperation
    NSInvocationOperation *invocationOperation = [[NSInvocationOperation alloc] initWithTarget:self selector:@selector(invocationOperationAddOperation) object:nil];
    // 创建操作，NSBlockOperation
    NSBlockOperation *blockOperation = [NSBlockOperation blockOperationWithBlock:^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"addOperation把任务添加到队列======%@", [NSThread currentThread]);
        }
    }];

    [queue addOperation:invocationOperation];
    [queue addOperation:blockOperation];
}

- (void)invocationOperationAddOperation {
    NSLog(@"invocationOperation===aaddOperation把任务添加到队列====%@", [NSThread currentThread]);
}
```

运行结果如下，可以看出，任务都是在子线程执行的，开启了新线程！

```
invocationOperation===addOperation把任务添加到队列====<NSThread: 0x60800026ed00>{number = 4, name = (null)}
addOperation把任务添加到队列======<NSThread: 0x60800026e640>{number = 3, name = (null)}
addOperation把任务添加到队列======<NSThread: 0x60800026e640>{number = 3, name = (null)}
addOperation把任务添加到队列======<NSThread: 0x60800026e640>{number = 3, name = (null)}
```

- `addOperationWithBlock`添加任务到队列

这是一个更方便的把任务添加到队列的方法，直接把任务写在block中，添加到任务中。

```
- (void)testAddOperationWithBlock {
    // 创建队列，默认并发
    NSOperationQueue *queue = [[NSOperationQueue alloc] init];

    // 添加操作到队列
    [queue addOperationWithBlock:^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"addOperationWithBlock把任务添加到队列======%@", [NSThread currentThread]);
        }
    }];
}
```

运行结果如下，任务确实是在子线程中执行。

```
addOperationWithBlock把任务添加到队列======<NSThread: 0x6000000752c0>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列======<NSThread: 0x6000000752c0>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列======<NSThread: 0x6000000752c0>{number = 3, name = (null)}
```

- 运用最大并发数实现串行

上面已经说过，可以运用队列的属性`maxConcurrentOperationCount`（最大并发数）来实现串行，值需要把它设置为1就可以了，下面我们通过代码验证一下。

```
- (void)testMaxConcurrentOperationCount {
    // 创建队列，默认并发
    NSOperationQueue *queue = [[NSOperationQueue alloc] init];

    // 最大并发数为1，串行
    queue.maxConcurrentOperationCount = 1;

    // 最大并发数为2，并发
//    queue.maxConcurrentOperationCount = 2;

    // 添加操作到队列
    [queue addOperationWithBlock:^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"addOperationWithBlock把任务添加到队列1======%@", [NSThread currentThread]);
        }
    }];

    // 添加操作到队列
    [queue addOperationWithBlock:^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"addOperationWithBlock把任务添加到队列2======%@", [NSThread currentThread]);
        }
    }];

    // 添加操作到队列
    [queue addOperationWithBlock:^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"addOperationWithBlock把任务添加到队列3======%@", [NSThread currentThread]);
        }
    }];
}
```

运行结果如下，当最大并发数为1的时候，虽然开启了线程，但是任务是顺序执行的，所以实现了串行。 你可以尝试把上面的最大并发数变为2，会发现任务就变成了并发执行。

```
addOperationWithBlock把任务添加到队列1======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列1======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列1======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列2======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列2======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列2======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列3======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列3======<NSThread: 0x608000068980>{number = 3, name = (null)}
addOperationWithBlock把任务添加到队列3======<NSThread: 0x608000068980>{number = 3, name = (null)}
```

## 5：NSOperation的操作依赖

NSOperation有一个非常好用的方法，就是操作依赖。可以从字面意思理解：某一个操作（operation2）依赖于另一个操作（operation1），只有当operation1执行完毕，才能执行operation2。

```
- (void)testAddDependency {

    // 并发队列
    NSOperationQueue *queue = [[NSOperationQueue alloc] init];

    // 操作1
    NSBlockOperation *operation1 = [NSBlockOperation blockOperationWithBlock:^{
        for (int i = 0; i < 3; i++) {
            NSLog(@"operation1======%@", [NSThread  currentThread]);
        }
    }];

    // 操作2
    NSBlockOperation *operation2 = [NSBlockOperation blockOperationWithBlock:^{
        NSLog(@"****operation2依赖于operation1，只有当operation1执行完毕，operation2才会执行****");
        for (int i = 0; i < 3; i++) {
            NSLog(@"operation2======%@", [NSThread  currentThread]);
        }
    }];

    // 使操作2依赖于操作1
    [operation2 addDependency:operation1];

    // 把操作加入队列
    [queue addOperation:operation1];
    [queue addOperation:operation2];
}
```

运行结果如下，操作2总是在操作1之后执行，成功验证了上面的说法。

```
operation1======<NSThread: 0x60800026dec0>{number = 3, name = (null)}
operation1======<NSThread: 0x60800026dec0>{number = 3, name = (null)}
operation1======<NSThread: 0x60800026dec0>{number = 3, name = (null)}
****operation2依赖于operation1，只有当operation1执行完毕，operation2才会执行****
operation2======<NSThread: 0x60800026dc80>{number = 4, name = (null)}
operation2======<NSThread: 0x60800026dc80>{number = 4, name = (null)}
operation2======<NSThread: 0x60800026dc80>{number = 4, name = (null)}
```

## 6：NSOperation、NSOperationQueue 线程间的通信

在 iOS 开发过程中，我们一般在主线程里边进行 UI 刷新，例如：点击、滚动、拖拽等事件。我们通常把一些耗时的操作放在其他线程，比如说图片下载、文件上传等耗时操作。而当我们有时候在其他线程完成了耗时操作时，需要回到主线程，那么就用到了线程之间的通讯。

```
/**
 * 线程间通信
 */
- (void)communication {

    // 1.创建队列
    NSOperationQueue *queue = [[NSOperationQueue alloc]init];

    // 2.添加操作
    [queue addOperationWithBlock:^{
        // 异步进行耗时操作
        for (int i = 0; i < 2; i++) {
            [NSThread sleepForTimeInterval:2]; // 模拟耗时操作
            NSLog(@"1---%@", [NSThread currentThread]); // 打印当前线程
        }

        // 回到主线程
        [[NSOperationQueue mainQueue] addOperationWithBlock:^{
            // 进行一些 UI 刷新等操作
            for (int i = 0; i < 2; i++) {
                [NSThread sleepForTimeInterval:2]; // 模拟耗时操作
                NSLog(@"2---%@", [NSThread currentThread]); // 打印当前线程
            }
        }];
    }];
}

```
通过线程间的通信，先在其他线程中执行操作，等操作执行完了之后再回到主线程执行主线程的相应操作。

## 7：NSOperation、NSOperationQueue 线程同步和线程安全

### NSOperation、NSOperationQueue 非线程安全

```
/**
 * 非线程安全：不使用 NSLock
 * 初始化火车票数量、卖票窗口(非线程安全)、并开始卖票
 */
- (void)initTicketStatusNotSave {
    NSLog(@"currentThread---%@",[NSThread currentThread]); // 打印当前线程

    self.ticketSurplusCount = 50;

    // 1.创建 queue1,queue1 代表北京火车票售卖窗口
    NSOperationQueue *queue1 = [[NSOperationQueue alloc] init];
    queue1.maxConcurrentOperationCount = 1;

    // 2.创建 queue2,queue2 代表上海火车票售卖窗口
    NSOperationQueue *queue2 = [[NSOperationQueue alloc] init];
    queue2.maxConcurrentOperationCount = 1;

    // 3.创建卖票操作 op1
    __weak typeof(self) weakSelf = self;
    NSBlockOperation *op1 = [NSBlockOperation blockOperationWithBlock:^{
        [weakSelf saleTicketNotSafe];
    }];

    // 4.创建卖票操作 op2
    NSBlockOperation *op2 = [NSBlockOperation blockOperationWithBlock:^{
        [weakSelf saleTicketNotSafe];
    }];

    // 5.添加操作，开始卖票
    [queue1 addOperation:op1];
    [queue2 addOperation:op2];
}

/**
 * 售卖火车票(非线程安全)
 */
- (void)saleTicketNotSafe {
    while (1) {

        if (self.ticketSurplusCount > 0) {
            //如果还有票，继续售卖
            self.ticketSurplusCount--;
            NSLog(@"%@", [NSString stringWithFormat:@"剩余票数:%d 窗口:%@", self.ticketSurplusCount, [NSThread currentThread]]);
            [NSThread sleepForTimeInterval:0.2];
        } else {
            NSLog(@"所有火车票均已售完");
            break;
        }
    }
}
```

可以看到：在不考虑线程安全，不使用 NSLock 情况下，得到票数是错乱的，这样显然不符合我们的需求，所以我们需要考虑线程安全问题。

### NSOperation、NSOperationQueue 线程安全

线程安全解决方案：可以给线程加锁，在一个线程执行该操作的时候，不允许其他线程进行操作。iOS 实现线程加锁有很多种方式。@synchronized、 NSLock、NSRecursiveLock、NSCondition、NSConditionLock、pthread_mutex、dispatch_semaphore、OSSpinLock、atomic(property) set/ge等等各种方式。这里我们使用 NSLock 对象来解决线程同步问题。NSLock 对象可以通过进入锁时调用 lock 方法，解锁时调用 unlock 方法来保证线程安全。

```
/**
 * 线程安全：使用 NSLock 加锁
 * 初始化火车票数量、卖票窗口(线程安全)、并开始卖票
 */

- (void)initTicketStatusSave {
    NSLog(@"currentThread---%@",[NSThread currentThread]); // 打印当前线程

    self.ticketSurplusCount = 50;

    self.lock = [[NSLock alloc] init];  // 初始化 NSLock 对象

    // 1.创建 queue1,queue1 代表北京火车票售卖窗口
    NSOperationQueue *queue1 = [[NSOperationQueue alloc] init];
    queue1.maxConcurrentOperationCount = 1;

    // 2.创建 queue2,queue2 代表上海火车票售卖窗口
    NSOperationQueue *queue2 = [[NSOperationQueue alloc] init];
    queue2.maxConcurrentOperationCount = 1;

    // 3.创建卖票操作 op1
    __weak typeof(self) weakSelf = self;
    NSBlockOperation *op1 = [NSBlockOperation blockOperationWithBlock:^{
        [weakSelf saleTicketSafe];
    }];

    // 4.创建卖票操作 op2
    NSBlockOperation *op2 = [NSBlockOperation blockOperationWithBlock:^{
        [weakSelf saleTicketSafe];
    }];

    // 5.添加操作，开始卖票
    [queue1 addOperation:op1];
    [queue2 addOperation:op2];
}

/**
 * 售卖火车票(线程安全)
 */
- (void)saleTicketSafe {
    while (1) {

        // 加锁
        [self.lock lock];

        if (self.ticketSurplusCount > 0) {
            //如果还有票，继续售卖
            self.ticketSurplusCount--;
            NSLog(@"%@", [NSString stringWithFormat:@"剩余票数:%d 窗口:%@", self.ticketSurplusCount, [NSThread currentThread]]);
            [NSThread sleepForTimeInterval:0.2];
        }

        // 解锁
        [self.lock unlock];

        if (self.ticketSurplusCount <= 0) {
            NSLog(@"所有火车票均已售完");
            break;
        }
    }
}
```

可以看出：在考虑了线程安全，使用 NSLock 加锁、解锁机制的情况下，得到的票数是正确的，没有出现混乱的情况。我们也就解决了多个线程同步的问题。


## 8：NSOperation、NSOperationQueue 常用属性和方法归纳

### NSOperation 常用属性和方法

1. 取消操作方法
- `- (void)cancel;` 可取消操作，实质是标记 `isCancelled` 状态。
2. 判断操作状态方法
- `- (BOOL)isFinished;` 判断操作是否已经结束。
- `- (BOOL)isCancelled;` 判断操作是否已经标记为取消。
- `- (BOOL)isExecuting;` 判断操作是否正在在运行。
- `- (BOOL)isReady;` 判断操作是否处于准备就绪状态，这个值和操作的依赖关系相关。
3. 操作同步
- `- (void)waitUntilFinished;` 阻塞当前线程，直到该操作结束。可用于线程执行顺序的同步。
- `- (void)setCompletionBlock:(void (^)(void))block;` `completionBlock` 会在当前操作执行完毕时执行 `completionBlock`。
- `- (void)addDependency:(NSOperation *)op;` 添加依赖，使当前操作依赖于操作 op 的完成。
- `- (void)removeDependency:(NSOperation *)op;` 移除依赖，取消当前操作对操作 op 的依赖。
- `@property (readonly, copy) NSArray<NSOperation *> *dependencies;` 在当前操作开始执行之前完成执行的所有操作对象数组。

### NSOperationQueue 常用属性和方法

1. 取消/暂停/恢复操作
- `- (void)cancelAllOperations;` 可以取消队列的所有操作。
- `- (BOOL)isSuspended;` 判断队列是否处于暂停状态。 YES 为暂停状态，NO 为恢复状态。
- `- (void)setSuspended:(BOOL)b;` 可设置操作的暂停和恢复，YES 代表暂停队列，NO 代表恢复队列。
2. 操作同步
- `- (void)waitUntilAllOperationsAreFinished;` 阻塞当前线程，直到队列中的操作全部执行完毕。
3. 添加/获取操作
- `- (void)addOperationWithBlock:(void (^)(void))block;` 向队列中添加一个 NSBlockOperation 类型操作对象。
- `- (void)addOperations:(NSArray *)ops waitUntilFinished:(BOOL)wait;` 向队列中添加操作数组，wait 标志是否阻塞当前线程直到所有操作结束
- `- (NSArray *)operations;` 当前在队列中的操作数组（某个操作执行结束后会自动从这个数组清除）。
- `- (NSUInteger)operationCount;` 当前队列中的操作数。
4. 获取队列
- `+ (id)currentQueue;` 获取当前队列，如果当前线程不是在 NSOperationQueue 上运行则返回 nil。
- `+ (id)mainQueue;` 获取主队列。

注意：

1. 这里的暂停和取消（包括操作的取消和队列的取消）并不代表可以将当前的操作立即取消，而是当当前的操作执行完毕之后不再执行新的操作。
2. 暂停和取消的区别就在于：暂停操作之后还可以恢复操作，继续向下执行；而取消操作之后，所有的操作就清空了，无法再接着执行剩下的操作。


# 参考文章

[iOS 多线程：『GCD』详尽总结](https://bujige.net/blog/iOS-Complete-learning-GCD.html)

[iOS 多线程详解](https://imlifengfeng.github.io/article/533/)

[谈 iOS 多线程（NSThread、NSOperation、GCD）编程](https://github.com/minggo620/iOSMutipleThread)

[iOS 多线程 WHMultiThreadDemo](https://www.fivehow.com/ios/2017-07-06-iOS多线程.html)
