---
title: Runloop 总结梳理
author: Ouyang Rong
date: 2021-11-10 18:11:00 +0800
categories: [iOS, Runloop]
tags: [Objective-C, Runloop]
---

# RunLoop概念

## RunLoop介绍

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/RunLoop-%E6%9E%B6%E6%9E%84%E5%9B%BE.jpg)

RunLoop 是什么？RunLoop 顾名思义就是一种循环，只不过它这种循环比较高级。一般的 while 循环会导致 CPU 进入忙等待状态，而 RunLoop 则是一种“闲”等待，这部分可以类比 Linux 下的 epoll。当没有事件时，RunLoop 会进入休眠状态；当有事件发生时，RunLoop 会去找对应的 Handler 处理事件。RunLoop 可以让线程在需要做事的时候忙起来，不需要的话就让线程休眠。

从代码上看，RunLoop其实就是一个对象，它的结构如下：

```
struct __CFRunLoop {
    CFRuntimeBase _base;
    pthread_mutex_t _lock;  /* locked for accessing mode list */
    __CFPort _wakeUpPort;   // used for CFRunLoopWakeUp 内核向该端口发送消息可以唤醒runloop
    Boolean _unused;
    volatile _per_run_data *_perRunData; // reset for runs of the run loop
    pthread_t _pthread;             //RunLoop对应的线程
    uint32_t _winthread;
    CFMutableSetRef _commonModes;    //存储的是字符串，记录所有标记为common的mode
    CFMutableSetRef _commonModeItems;//存储所有commonMode的item(source、timer、observer)
    CFRunLoopModeRef _currentMode;   //当前运行的mode
    CFMutableSetRef _modes;          //存储的是CFRunLoopModeRef
    struct _block_item *_blocks_head;//doblocks的时候用到
    struct _block_item *_blocks_tail;
    CFTypeRef _counterpart;
};
```

可见，一个RunLoop对象，主要包含了一个线程，若干个Mode，若干个commonMode，还有一个当前运行的Mode。

## RunLoop与线程

当我们需要一个常驻线程，可以让线程在需要做事的时候忙起来，不需要的话就让线程休眠。我们就在线程里面执行下面这个代码，一直等待消息，线程就不会退出了。

```
do {
   //获取消息
   //处理消息
} while (消息 ！= 退出)
```

上面的这种循环模型被称作 Event Loop，事件循环模型在众多系统里都有实现，RunLoop 实际上就是一个对象，这个对象管理了其需要处理的事件和消息，并提供了一个入口函数来执行上面 Event Loop 的逻辑。线程执行了这个函数后，就会一直处于这个函数内部 "接受消息->等待->处理" 的循环中，直到这个循环结束（比如传入 quit 的消息），函数返回。

下图描述了Runloop运行流程（基本描述了上面Runloop的核心流程，当然可以查看官方[The Run Loop Sequence of Events](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/RunLoopManagement/RunLoopManagement.html#//apple_ref/doc/uid/10000057i-CH16-SW23)描述）：

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/Runloop-%E8%BF%90%E8%A1%8C%E6%B5%81%E7%A8%8B.png)

整个流程并不复杂（需要注意的就是_黄色_区域的消息处理中并不包含source0，因为它在循环开始之初就会处理），整个流程其实就是一种Event Loop的实现，其他平台均有类似的实现，只是这里叫做RunLoop。

RunLoop与线程的关系如下图：

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/RunLoop-%E7%BA%BF%E7%A8%8B.jpg)

图中展现了 Runloop 在线程中的作用：从 input source 和 timer source 接受事件，然后在线程中处理事件。

Runloop 和线程是绑定在一起的。每个线程（包括主线程）都有一个对应的 Runloop 对象。我们并不能自己创建 Runloop 对象，但是可以获取到系统提供的 Runloop 对象。

主线程的 Runloop 会在应用启动的时候完成启动，其他线程的 Runloop 默认并不会启动，需要我们手动启动。

## RunLoop Mode

Mode可以视为事件的管家，一个Mode管理着各种事件，它的结构如下：

```
struct __CFRunLoopMode {
    CFRuntimeBase _base;
    pthread_mutex_t _lock;  /* must have the run loop locked before locking this */
    CFStringRef _name;   //mode名称
    Boolean _stopped;    //mode是否被终止
    char _padding[3];
    //几种事件
    CFMutableSetRef _sources0;  //sources0
    CFMutableSetRef _sources1;  //sources1
    CFMutableArrayRef _observers; //通知
    CFMutableArrayRef _timers;    //定时器
    CFMutableDictionaryRef _portToV1SourceMap; //字典  key是mach_port_t，value是CFRunLoopSourceRef
    __CFPortSet _portSet; //保存所有需要监听的port，比如_wakeUpPort，_timerPort都保存在这个数组中
    CFIndex _observerMask;
#if USE_DISPATCH_SOURCE_FOR_TIMERS
    dispatch_source_t _timerSource;
    dispatch_queue_t _queue;
    Boolean _timerFired; // set to true by the source when a timer has fired
    Boolean _dispatchTimerArmed;
#endif
#if USE_MK_TIMER_TOO
    mach_port_t _timerPort;
    Boolean _mkTimerArmed;
#endif
#if DEPLOYMENT_TARGET_WINDOWS
    DWORD _msgQMask;
    void (*_msgPump)(void);
#endif
    uint64_t _timerSoftDeadline; /* TSR */
    uint64_t _timerHardDeadline; /* TSR */
};
```

一个CFRunLoopMode对象有一个name，若干source0、source1、timer、observer和若干port，可见事件都是由Mode在管理，而RunLoop管理Mode。

从源码很容易看出，Runloop总是运行在某种特定的CFRunLoopModeRef下（每次运行**__CFRunLoopRun()函数时必须指定Mode）。而通过CFRunloopRef对应结构体的定义可以很容易知道每种Runloop都可以包含若干个Mode，每个Mode又包含Source/Timer/Observer。每次调用Runloop的主函数__CFRunLoopRun()时必须指定一种Mode，这个Mode称为 _currentMode**，当切换Mode时必须退出当前Mode，然后重新进入Runloop以保证不同Mode的Source/Timer/Observer互不影响。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/RunLoop-Model.png)

如图所示，Runloop Mode 实际上是 Source，Timer 和 Observer 的集合，不同的 Mode 把不同组的 Source，Timer 和 Observer 隔绝开来。Runloop 在某个时刻只能跑在一个 Mode 下，处理这一个 Mode 当中的 Source，Timer 和 Observer。

苹果文档中提到的 Mode 有五个，分别是：

- NSDefaultRunLoopMode
- NSConnectionReplyMode
- NSModalPanelRunLoopMode
- NSEventTrackingRunLoopMode
- NSRunLoopCommonModes

iOS 中公开暴露出来的只有 NSDefaultRunLoopMode 和 NSRunLoopCommonModes。 NSRunLoopCommonModes 实际上是一个 Mode 的集合，默认包括 NSDefaultRunLoopMode 和 NSEventTrackingRunLoopMode（注意：并不是说 Runloop 会运行在 kCFRunLoopCommonModes 这种模式下，而是相当于分别注册了 NSDefaultRunLoopMode 和 UITrackingRunLoopMode。当然你也可以通过调用 CFRunLoopAddCommonMode() 方法将自定义 Mode 放到 kCFRunLoopCommonModes 组合）。

五种Mode的介绍如下图：

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/Runloop-%E4%BA%94%E7%A7%8DMode.png)

## RunLoop Source

Run Loop Source分为Source、Observer、Timer三种，他们统称为ModeItem。

### CFRunLoopSource

根据官方的描述，CFRunLoopSource是对input sources的抽象。CFRunLoopSource分source0和source1两个版本，它的结构如下：

```
struct __CFRunLoopSource {
    CFRuntimeBase _base;
    uint32_t _bits; //用于标记Signaled状态，source0只有在被标记为Signaled状态，才会被处理
    pthread_mutex_t _lock;
    CFIndex _order;         /* immutable */
    CFMutableBagRef _runLoops;
    union {
        CFRunLoopSourceContext version0;     /* immutable, except invalidation */
        CFRunLoopSourceContext1 version1;    /* immutable, except invalidation */
    } _context;
};
```

source0是App内部事件，由App自己管理的UIEvent、CFSocket都是source0。当一个source0事件准备执行的时候，必须要先把它标记为signal状态，以下是source0的结构体：

```
typedef struct {
    CFIndex version;
    void *  info;
    const void *(*retain)(const void *info);
    void    (*release)(const void *info);
    CFStringRef (*copyDescription)(const void *info);
    Boolean (*equal)(const void *info1, const void *info2);
    CFHashCode  (*hash)(const void *info);
    void    (*schedule)(void *info, CFRunLoopRef rl, CFStringRef mode);
    void    (*cancel)(void *info, CFRunLoopRef rl, CFStringRef mode);
    void    (*perform)(void *info);
} CFRunLoopSourceContext;
```

source0是非基于Port的。只包含了一个回调（函数指针），它并不能主动触发事件。使用时，你需要先调用 CFRunLoopSourceSignal(source)，将这个 Source 标记为待处理，然后手动调用 CFRunLoopWakeUp(runloop) 来唤醒 RunLoop，让其处理这个事件。

source1由RunLoop和内核管理，source1带有mach_port_t，可以接收内核消息并触发回调，以下是source1的结构体：

```
typedef struct {
    CFIndex version;
    void *  info;
    const void *(*retain)(const void *info);
    void    (*release)(const void *info);
    CFStringRef (*copyDescription)(const void *info);
    Boolean (*equal)(const void *info1, const void *info2);
    CFHashCode  (*hash)(const void *info);
#if (TARGET_OS_MAC && !(TARGET_OS_EMBEDDED || TARGET_OS_IPHONE)) || (TARGET_OS_EMBEDDED || TARGET_OS_IPHONE)
    mach_port_t (*getPort)(void *info);
    void *  (*perform)(void *msg, CFIndex size, CFAllocatorRef allocator, void *info);
#else
    void *  (*getPort)(void *info);
    void    (*perform)(void *info);
#endif
} CFRunLoopSourceContext1;
```

Source1除了包含回调指针外包含一个mach port，Source1可以监听系统端口和通过内核和其他线程通信，接收、分发系统事件，它能够主动唤醒RunLoop(由操作系统内核进行管理，例如CFMessagePort消息)。官方也指出可以自定义Source，因此对于CFRunLoopSourceRef来说它更像一种协议，框架已经默认定义了两种实现，如果有必要开发人员也可以自定义，详细情况可以查看[官方文档](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/RunLoopManagement/RunLoopManagement.html)。

### CFRunLoopObserver

CFRunLoopObserver是观察者，可以观察RunLoop的各种状态，并抛出回调。

```
struct __CFRunLoopObserver {
    CFRuntimeBase _base;
    pthread_mutex_t _lock;
    CFRunLoopRef _runLoop;
    CFIndex _rlCount;
    CFOptionFlags _activities;      /* immutable */
    CFIndex _order;         /* immutable */
    CFRunLoopObserverCallBack _callout; /* immutable */
    CFRunLoopObserverContext _context;  /* immutable, except invalidation */
};
```

CFRunLoopObserver可以观察的状态有如下6种:

```
/* Run Loop Observer Activities */
typedef CF_OPTIONS(CFOptionFlags, CFRunLoopActivity) {
    kCFRunLoopEntry = (1UL << 0), //即将进入run loop
    kCFRunLoopBeforeTimers = (1UL << 1), //即将处理timer
    kCFRunLoopBeforeSources = (1UL << 2),//即将处理source
    kCFRunLoopBeforeWaiting = (1UL << 5),//即将进入休眠
    kCFRunLoopAfterWaiting = (1UL << 6),//被唤醒但是还没开始处理事件
    kCFRunLoopExit = (1UL << 7),//run loop已经退出
    kCFRunLoopAllActivities = 0x0FFFFFFFU
};
```

Runloop 通过监控 Source 来决定有没有任务要做，除此之外，我们还可以用 Runloop Observer 来监控 Runloop 本身的状态。 Runloop Observer 可以监控上面的 Runloop 事件，具体流程如下图。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/Runloop-Observer.png)

### CFRunLoopTimer

CFRunLoopTimer是定时器，可以在设定的时间点抛出回调，它的结构如下：

```
struct __CFRunLoopTimer {
    CFRuntimeBase _base;
    uint16_t _bits;  //标记fire状态
    pthread_mutex_t _lock;
    CFRunLoopRef _runLoop;        //添加该timer的runloop
    CFMutableSetRef _rlModes;     //存放所有 包含该timer的 mode的 modeName，意味着一个timer可能会在多个mode中存在
    CFAbsoluteTime _nextFireDate;
    CFTimeInterval _interval;     //理想时间间隔  /* immutable */
    CFTimeInterval _tolerance;    //时间偏差      /* mutable */
    uint64_t _fireTSR;          /* TSR units */
    CFIndex _order;         /* immutable */
    CFRunLoopTimerCallBack _callout;    /* immutable */
    CFRunLoopTimerContext _context; /* immutable, except invalidation */
};
```

另外根据[官方文档](https://developer.apple.com/documentation/corefoundation/cfrunlooptimer?language=objc)的描述，CFRunLoopTimer和NSTimer是[toll-free bridged](https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFDesignConcepts/Articles/tollFreeBridgedTypes.html#//apple_ref/doc/uid/TP40010677)的，可以相互转换。

> CFRunLoopTimer is “toll-free bridged” with its Cocoa Foundation counterpart, NSTimer. This means that the Core Foundation type is interchangeable in function or method calls with the bridged Foundation object.

所以CFRunLoopTimer具有以下特性：

- CFRunLoopTimer 是定时器，可以在设定的时间点抛出回调
- CFRunLoopTimer和NSTimer是toll-free bridged的，可以相互转换


# RunLoop实现

下面从以下3个方面介绍RunLoop的实现。

- 获取RunLoop
- 添加Mode
- 添加Run Loop Source

## 获取RunLoop

从苹果开放的API来看，不允许我们直接创建RunLoop对象，只能通过以下几个函数来获取RunLoop:

- CFRunLoopRef CFRunLoopGetCurrent(void)
- CFRunLoopRef CFRunLoopGetMain(void)
- +(NSRunLoop *)currentRunLoop
- +(NSRunLoop *)mainRunLoop

前两个是Core Foundation中的API，后两个是Foundation中的API。

那么RunLoop是什么时候被创建的呢？

我们从下面几个函数内部看看。

### CFRunLoopGetCurrent

```
//取当前所在线程的RunLoop
CFRunLoopRef CFRunLoopGetCurrent(void) {
    CHECK_FOR_FORK();
    CFRunLoopRef rl = (CFRunLoopRef)_CFGetTSD(__CFTSDKeyRunLoop);
    if (rl) return rl;
    //传入当前线程
    return _CFRunLoopGet0(pthread_self());
}
```

在`CFRunLoopGetCurrent`函数内部调用了`_CFRunLoopGet0()`，传入的参数是当前线程`pthread_self()`。这里可以看出，`CFRunLoopGetCurrent`函数必须要在线程内部调用，才能获取当前线程的RunLoop。也就是说子线程的RunLoop必须要在子线程内部获取。

### CFRunLoopGetMain

```
//取主线程的RunLoop
CFRunLoopRef CFRunLoopGetMain(void) {
    CHECK_FOR_FORK();
    static CFRunLoopRef __main = NULL; // no retain needed
    //传入主线程
    if (!__main) __main = _CFRunLoopGet0(pthread_main_thread_np()); // no CAS needed
    return __main;
}
```

在`CFRunLoopGetMain`函数内部也调用了`_CFRunLoopGet0()`，传入的参数是主线程`pthread_main_thread_np()`。可以看出，`CFRunLoopGetMain()`不管在主线程还是子线程中调用，都可以获取到主线程的RunLoop。

### CFRunLoopGet0

前面两个函数都是使用了CFRunLoopGet0实现传入线程的函数，下面看下CFRunLoopGet0的结构是咋样的。

```
static CFMutableDictionaryRef __CFRunLoops = NULL;
static CFSpinLock_t loopsLock = CFSpinLockInit;

// t==0 is a synonym for "main thread" that always works
//根据线程取RunLoop
CF_EXPORT CFRunLoopRef _CFRunLoopGet0(pthread_t t) {
    if (pthread_equal(t, kNilPthreadT)) {
        t = pthread_main_thread_np();
    }
    __CFSpinLock(&loopsLock);
    //如果存储RunLoop的字典不存在
    if (!__CFRunLoops) {
        __CFSpinUnlock(&loopsLock);
        //创建一个临时字典dict
        CFMutableDictionaryRef dict = CFDictionaryCreateMutable(kCFAllocatorSystemDefault, 0, NULL, &kCFTypeDictionaryValueCallBacks);
        //创建主线程的RunLoop
        CFRunLoopRef mainLoop = __CFRunLoopCreate(pthread_main_thread_np());
        //把主线程的RunLoop保存到dict中，key是线程，value是RunLoop
        CFDictionarySetValue(dict, pthreadPointer(pthread_main_thread_np()), mainLoop);
        //此处NULL和__CFRunLoops指针都指向NULL，匹配，所以将dict写到__CFRunLoops
        if (!OSAtomicCompareAndSwapPtrBarrier(NULL, dict, (void * volatile *)&__CFRunLoops)) {
            //释放dict
            CFRelease(dict);
        }
        //释放mainrunloop
        CFRelease(mainLoop);
        __CFSpinLock(&loopsLock);
    }
    //以上说明，第一次进来的时候，不管是getMainRunloop还是get子线程的runloop，主线程的runloop总是会被创建
    //从字典__CFRunLoops中获取传入线程t的runloop
    CFRunLoopRef loop = (CFRunLoopRef)CFDictionaryGetValue(__CFRunLoops, pthreadPointer(t));
    __CFSpinUnlock(&loopsLock);
    //如果没有获取到
    if (!loop) {
        //根据线程t创建一个runloop
        CFRunLoopRef newLoop = __CFRunLoopCreate(t);
        __CFSpinLock(&loopsLock);
        loop = (CFRunLoopRef)CFDictionaryGetValue(__CFRunLoops, pthreadPointer(t));
        if (!loop) {
            //把newLoop存入字典__CFRunLoops，key是线程t
            CFDictionarySetValue(__CFRunLoops, pthreadPointer(t), newLoop);
            loop = newLoop;
        }
        // don't release run loops inside the loopsLock, because CFRunLoopDeallocate may end up taking it
        __CFSpinUnlock(&loopsLock);
        CFRelease(newLoop);
    }
    //如果传入线程就是当前线程
    if (pthread_equal(t, pthread_self())) {
        _CFSetTSD(__CFTSDKeyRunLoop, (void *)loop, NULL);
        if (0 == _CFGetTSD(__CFTSDKeyRunLoopCntr)) {
            //注册一个回调，当线程销毁时，销毁对应的RunLoop
            _CFSetTSD(__CFTSDKeyRunLoopCntr, (void *)(PTHREAD_DESTRUCTOR_ITERATIONS-1), (void (*)(void *))__CFFinalizeRunLoop);
        }
    }
    return loop;
}
```

这段代码可以得出以下结论：

- RunLoop和线程的一一对应的，对应的方式是以key-value的方式保存在一个全局字典中
- 主线程的RunLoop会在初始化全局字典时创建
- 子线程的RunLoop会在第一次获取的时候创建，如果不获取的话就一直不会被创建
- RunLoop会在线程销毁时销毁

## 添加Mode

在Core Foundation中，针对Mode的操作，苹果只开放了以下3个API（Cocoa中也有功能一样的函数，不再列出）:

- CFRunLoopAddCommonMode(CFRunLoopRef rl, CFStringRef mode)
- CFStringRef CFRunLoopCopyCurrentMode(CFRunLoopRef rl)
- CFArrayRef CFRunLoopCopyAllModes(CFRunLoopRef rl)

> CFRunLoopAddCommonMode
> Adds a mode to the set of run loop common modes.
> 向当前RunLoop的common modes中添加一个mode。
> CFRunLoopCopyCurrentMode
> Returns the name of the mode in which a given run loop is currently running.
> 返回当前运行的mode的name
> CFRunLoopCopyAllModes
> Returns an array that contains all the defined modes for a CFRunLoop object.
> 返回当前RunLoop的所有mode

我们没有办法直接创建一个CFRunLoopMode对象，但是我们可以调用CFRunLoopAddCommonMode传入一个字符串向RunLoop中添加Mode，传入的字符串即为Mode的名字，Mode对象应该是此时在RunLoop内部创建的。下面来看一下源码。

### CFRunLoopAddCommonMode

```
void CFRunLoopAddCommonMode(CFRunLoopRef rl, CFStringRef modeName) {
    CHECK_FOR_FORK();
    if (__CFRunLoopIsDeallocating(rl)) return;
    __CFRunLoopLock(rl);
    //看rl中是否已经有这个mode，如果有就什么都不做
    if (!CFSetContainsValue(rl->_commonModes, modeName)) {
        CFSetRef set = rl->_commonModeItems ? CFSetCreateCopy(kCFAllocatorSystemDefault, rl->_commonModeItems) : NULL;
        //把modeName添加到RunLoop的_commonModes中
        CFSetAddValue(rl->_commonModes, modeName);
        if (NULL != set) {
            CFTypeRef context[2] = {rl, modeName};
            /* add all common-modes items to new mode */
            //这里调用CFRunLoopAddSource/CFRunLoopAddObserver/CFRunLoopAddTimer的时候会调用
            //__CFRunLoopFindMode(rl, modeName, true)，CFRunLoopMode对象在这个时候被创建
            CFSetApplyFunction(set, (__CFRunLoopAddItemsToCommonMode), (void *)context);
            CFRelease(set);
        }
    } else {
    }
    __CFRunLoopUnlock(rl);
}
```

可以看得出：

- modeName不能重复，modeName是mode的唯一标识符
- RunLoop的_commonModes数组存放所有被标记为common的mode的名称
- 添加commonMode会把commonModeItems数组中的所有source同步到新添加的mode中
- CFRunLoopMode对象在CFRunLoopAddItemsToCommonMode函数中调用CFRunLoopFindMode时被创建

### CFRunLoopCopyCurrentMode和CFRunLoopCopyAllModes

CFRunLoopCopyCurrentMode和CFRunLoopCopyAllModes的内部逻辑比较简单，直接取RunLoop的`_currentMode`和`_modes`返回，就不贴源码了。

## 添加Run Loop Source（ModeItem）

我们可以通过以下接口添加/移除各种事件:

- void CFRunLoopAddSource(CFRunLoopRef rl, CFRunLoopSourceRef source, CFStringRef mode)
- void CFRunLoopRemoveSource(CFRunLoopRef rl, CFRunLoopSourceRef source, CFStringRef mode)
- void CFRunLoopAddObserver(CFRunLoopRef rl, CFRunLoopObserverRef observer, CFStringRef mode)
- void CFRunLoopRemoveObserver(CFRunLoopRef rl, CFRunLoopObserverRef observer, CFStringRef * mode)
- void CFRunLoopAddTimer(CFRunLoopRef rl, CFRunLoopTimerRef timer, CFStringRef mode)
- void CFRunLoopRemoveTimer(CFRunLoopRef rl, CFRunLoopTimerRef timer, CFStringRef mode)

### CFRunLoopAddSource

CFRunLoopAddSource的代码结构如下：

```
//添加source事件
void CFRunLoopAddSource(CFRunLoopRef rl, CFRunLoopSourceRef rls, CFStringRef modeName) {    /* DOES CALLOUT */
    CHECK_FOR_FORK();
    if (__CFRunLoopIsDeallocating(rl)) return;
    if (!__CFIsValid(rls)) return;
    Boolean doVer0Callout = false;
    __CFRunLoopLock(rl);
    //如果是kCFRunLoopCommonModes
    if (modeName == kCFRunLoopCommonModes) {
        //如果runloop的_commonModes存在，则copy一个新的复制给set
        CFSetRef set = rl->_commonModes ? CFSetCreateCopy(kCFAllocatorSystemDefault, rl->_commonModes) : NULL;
       //如果runl _commonModeItems为空
        if (NULL == rl->_commonModeItems) {
            //先初始化
            rl->_commonModeItems = CFSetCreateMutable(kCFAllocatorSystemDefault, 0, &kCFTypeSetCallBacks);
        }
        //把传入的CFRunLoopSourceRef加入_commonModeItems
        CFSetAddValue(rl->_commonModeItems, rls);
        //如果刚才set copy到的数组里有数据
        if (NULL != set) {
            CFTypeRef context[2] = {rl, rls};
            /* add new item to all common-modes */
            //则把set里的所有mode都执行一遍__CFRunLoopAddItemToCommonModes函数
            CFSetApplyFunction(set, (__CFRunLoopAddItemToCommonModes), (void *)context);
            CFRelease(set);
        }
        //以上分支的逻辑就是，如果你往kCFRunLoopCommonModes里面添加一个source，那么所有_commonModes里的mode都会添加这个source
    } else {
        //根据modeName查找mode
        CFRunLoopModeRef rlm = __CFRunLoopFindMode(rl, modeName, true);
        //如果_sources0不存在，则初始化_sources0，_sources0和_portToV1SourceMap
        if (NULL != rlm && NULL == rlm->_sources0) {
            rlm->_sources0 = CFSetCreateMutable(kCFAllocatorSystemDefault, 0, &kCFTypeSetCallBacks);
            rlm->_sources1 = CFSetCreateMutable(kCFAllocatorSystemDefault, 0, &kCFTypeSetCallBacks);
            rlm->_portToV1SourceMap = CFDictionaryCreateMutable(kCFAllocatorSystemDefault, 0, NULL, NULL);
        }
        //如果_sources0和_sources1中都不包含传入的source
        if (NULL != rlm && !CFSetContainsValue(rlm->_sources0, rls) && !CFSetContainsValue(rlm->_sources1, rls)) {
            //如果version是0，则加到_sources0
            if (0 == rls->_context.version0.version) {
                CFSetAddValue(rlm->_sources0, rls);
                //如果version是1，则加到_sources1
            } else if (1 == rls->_context.version0.version) {
                CFSetAddValue(rlm->_sources1, rls);
                __CFPort src_port = rls->_context.version1.getPort(rls->_context.version1.info);
                if (CFPORT_NULL != src_port) {
                    //此处只有在加到source1的时候才会把souce和一个mach_port_t对应起来
                    //可以理解为，source1可以通过内核向其端口发送消息来主动唤醒runloop
                    CFDictionarySetValue(rlm->_portToV1SourceMap, (const void *)(uintptr_t)src_port, rls);
                    __CFPortSetInsert(src_port, rlm->_portSet);
                }
            }
            __CFRunLoopSourceLock(rls);
            //把runloop加入到source的_runLoops中
            if (NULL == rls->_runLoops) {
                rls->_runLoops = CFBagCreateMutable(kCFAllocatorSystemDefault, 0, &kCFTypeBagCallBacks); // sources retain run loops!
            }
            CFBagAddValue(rls->_runLoops, rl);
            __CFRunLoopSourceUnlock(rls);
            if (0 == rls->_context.version0.version) {
                if (NULL != rls->_context.version0.schedule) {
                    doVer0Callout = true;
                }
            }
        }
        if (NULL != rlm) {
            __CFRunLoopModeUnlock(rlm);
        }
    }
    __CFRunLoopUnlock(rl);
    if (doVer0Callout) {
        // although it looses some protection for the source, we have no choice but
        // to do this after unlocking the run loop and mode locks, to avoid deadlocks
        // where the source wants to take a lock which is already held in another
        // thread which is itself waiting for a run loop/mode lock
        rls->_context.version0.schedule(rls->_context.version0.info, rl, modeName); /* CALLOUT */
    }
}
```

通过添加source的这段代码可以得出如下结论：

- 如果modeName传入kCFRunLoopCommonModes，则该source会被保存到RunLoop的_commonModeItems中
- 如果modeName传入kCFRunLoopCommonModes，则该source会被添加到所有commonMode中
- 如果modeName传入的不是kCFRunLoopCommonModes，则会先查找该Mode，如果没有，会创建一个
- 同一个source在一个mode中只能被添加一次

### CFRunLoopRemoveSource

remove操作和add操作的逻辑基本一致，很容易理解。

```
//移除source
void CFRunLoopRemoveSource(CFRunLoopRef rl, CFRunLoopSourceRef rls, CFStringRef modeName) { /* DOES CALLOUT */
    CHECK_FOR_FORK();
    Boolean doVer0Callout = false, doRLSRelease = false;
    __CFRunLoopLock(rl);
    //如果是kCFRunLoopCommonModes，则从_commonModes的所有mode中移除该source
    if (modeName == kCFRunLoopCommonModes) {
        if (NULL != rl->_commonModeItems && CFSetContainsValue(rl->_commonModeItems, rls)) {
            CFSetRef set = rl->_commonModes ? CFSetCreateCopy(kCFAllocatorSystemDefault, rl->_commonModes) : NULL;
            CFSetRemoveValue(rl->_commonModeItems, rls);
            if (NULL != set) {
                CFTypeRef context[2] = {rl, rls};
                /* remove new item from all common-modes */
                CFSetApplyFunction(set, (__CFRunLoopRemoveItemFromCommonModes), (void *)context);
                CFRelease(set);
            }
        } else {
        }
    } else {
        //根据modeName查找mode，如果不存在，返回NULL
        CFRunLoopModeRef rlm = __CFRunLoopFindMode(rl, modeName, false);
        if (NULL != rlm && ((NULL != rlm->_sources0 && CFSetContainsValue(rlm->_sources0, rls)) || (NULL != rlm->_sources1 && CFSetContainsValue(rlm->_sources1, rls)))) {
            CFRetain(rls);
            //根据source版本做对应的remove操作
            if (1 == rls->_context.version0.version) {
                __CFPort src_port = rls->_context.version1.getPort(rls->_context.version1.info);
                if (CFPORT_NULL != src_port) {
                    CFDictionaryRemoveValue(rlm->_portToV1SourceMap, (const void *)(uintptr_t)src_port);
                    __CFPortSetRemove(src_port, rlm->_portSet);
                }
            }
            CFSetRemoveValue(rlm->_sources0, rls);
            CFSetRemoveValue(rlm->_sources1, rls);
            __CFRunLoopSourceLock(rls);
            if (NULL != rls->_runLoops) {
                CFBagRemoveValue(rls->_runLoops, rl);
            }
            __CFRunLoopSourceUnlock(rls);
            if (0 == rls->_context.version0.version) {
                if (NULL != rls->_context.version0.cancel) {
                    doVer0Callout = true;
                }
            }
            doRLSRelease = true;
        }
        if (NULL != rlm) {
            __CFRunLoopModeUnlock(rlm);
        }
    }
    __CFRunLoopUnlock(rl);
    if (doVer0Callout) {
        // although it looses some protection for the source, we have no choice but
        // to do this after unlocking the run loop and mode locks, to avoid deadlocks
        // where the source wants to take a lock which is already held in another
        // thread which is itself waiting for a run loop/mode lock
        rls->_context.version0.cancel(rls->_context.version0.info, rl, modeName);   /* CALLOUT */
    }
    if (doRLSRelease) CFRelease(rls);
}
```

### 添加Observer和Timer

添加observer和timer的内部逻辑和添加source大体类似。

区别在于observer和timer只能被添加到一个RunLoop的一个或者多个mode中，比如一个timer被添加到主线程的RunLoop中，则不能再把该timer添加到子线程的RunLoop，而source没有这个限制，不管是哪个RunLoop，只要mode中没有，就可以添加。

这个区别在文章最开始的结构体中也可以发现，CFRunLoopSource结构体中有保存RunLoop对象的数组，而CFRunLoopObserver和CFRunLoopTimer只有单个RunLoop对象。


# RunLoop运行

在Core Foundation中我们可以通过以下2个API来让RunLoop运行：

- void CFRunLoopRun(void)

在默认的mode下运行当前线程的RunLoop。

- CFRunLoopRunResult CFRunLoopRunInMode(CFStringRef mode, CFTimeInterval seconds, Boolean returnAfterSourceHandled)

在指定mode下运行当前线程的RunLoop。

## CFRunLoopRun

```
//默认运行runloop的kCFRunLoopDefaultMode
void CFRunLoopRun(void) {   /* DOES CALLOUT */
    int32_t result;
    do {
        //默认在kCFRunLoopDefaultMode下运行runloop
        result = CFRunLoopRunSpecific(CFRunLoopGetCurrent(), kCFRunLoopDefaultMode, 1.0e10, false);
        CHECK_FOR_FORK();
    } while (kCFRunLoopRunStopped != result && kCFRunLoopRunFinished != result);
}
```

在CFRunLoopRun函数中调用了CFRunLoopRunSpecific函数，runloop参数传入当前RunLoop对象，modeName参数传入kCFRunLoopDefaultMode。验证了前面文档的解释。

## CFRunLoopRunInMode

```
SInt32 CFRunLoopRunInMode(CFStringRef modeName, CFTimeInterval seconds, Boolean returnAfterSourceHandled) {     /* DOES CALLOUT */
    CHECK_FOR_FORK();
    return CFRunLoopRunSpecific(CFRunLoopGetCurrent(), modeName, seconds, returnAfterSourceHandled);
}
```

在CFRunLoopRunInMode函数中也调用了CFRunLoopRunSpecific函数，runloop参数传入当前RunLoop对象，modeName参数继续传递CFRunLoopRunInMode传入的modeName。也验证了前面文档的解释。

这里还可以看出，虽然RunLoop有很多个mode，但是RunLoop在run的时候必须只能指定其中一个mode，运行起来之后，被指定的mode即为currentMode。

这2个函数都看不出来RunLoop是怎么run起来的。

接下来我们继续探索一下CFRunLoopRunSpecific函数里面都干了什么，看看RunLoop具体是怎么run的。

## CFRunLoopRunSpecific

```
/*
 * 指定mode运行runloop
 * @param rl 当前运行的runloop
 * @param modeName 需要运行的mode的name
 * @param seconds  runloop的超时时间
 * @param returnAfterSourceHandled 是否处理完事件就返回
 */
SInt32 CFRunLoopRunSpecific(CFRunLoopRef rl, CFStringRef modeName, CFTimeInterval seconds, Boolean returnAfterSourceHandled) {     /* DOES CALLOUT */
    CHECK_FOR_FORK();
    if (__CFRunLoopIsDeallocating(rl)) return kCFRunLoopRunFinished;
    __CFRunLoopLock(rl);
    //根据modeName找到本次运行的mode
    CFRunLoopModeRef currentMode = __CFRunLoopFindMode(rl, modeName, false);
    //如果没找到 || mode中没有注册任何事件，则就此停止，不进入循环
    if (NULL == currentMode || __CFRunLoopModeIsEmpty(rl, currentMode, rl->_currentMode)) {
        Boolean did = false;
        if (currentMode) __CFRunLoopModeUnlock(currentMode);
        __CFRunLoopUnlock(rl);
        return did ? kCFRunLoopRunHandledSource : kCFRunLoopRunFinished;
    }
    volatile _per_run_data *previousPerRun = __CFRunLoopPushPerRunData(rl);
    //取上一次运行的mode
    CFRunLoopModeRef previousMode = rl->_currentMode;
    //如果本次mode和上次的mode一致
    rl->_currentMode = currentMode;
    //初始化一个result为kCFRunLoopRunFinished
    int32_t result = kCFRunLoopRunFinished;

    // 1.通知observer即将进入runloop
    if (currentMode->_observerMask & kCFRunLoopEntry ) __CFRunLoopDoObservers(rl, currentMode, kCFRunLoopEntry);
    result = __CFRunLoopRun(rl, currentMode, seconds, returnAfterSourceHandled, previousMode);
    //10.通知observer已退出runloop
    if (currentMode->_observerMask & kCFRunLoopExit ) __CFRunLoopDoObservers(rl, currentMode, kCFRunLoopExit);

    __CFRunLoopModeUnlock(currentMode);
    __CFRunLoopPopPerRunData(rl, previousPerRun);
    rl->_currentMode = previousMode;
    __CFRunLoopUnlock(rl);
    return result;
}
```

通过CFRunLoopRunSpecific的内部逻辑，我们可以得出：

- 如果指定了一个不存在的mode来运行RunLoop，那么会失败，mode不会被创建，所以这里传入的mode必须是存在的
- 如果指定了一个mode，但是这个mode中不包含任何modeItem，那么RunLoop也不会运行，所以必须要传入至少包含一个modeItem的mode
- 在进入run loop之前通知observer，状态为kCFRunLoopEntry
- 在退出run loop之后通知observer，状态为kCFRunLoopExit

RunLoop的运行的最核心函数是`__CFRunLoopRun`，接下来我们分析`__CFRunLoopRun`的源码。

## __CFRunLoopRun

这段代码比较长,请做好心理准备，我已经加了比较详细的注释。本节开头的run loop运行步骤2~9步都在下面的代码中得到验证。

```
/**
 *  运行run loop
 *
 *  @param rl              运行的RunLoop对象
 *  @param rlm             运行的mode
 *  @param seconds         run loop超时时间
 *  @param stopAfterHandle true:run loop处理完事件就退出  false:一直运行直到超时或者被手动终止
 *  @param previousMode    上一次运行的mode
 *
 *  @return 返回4种状态
 */
static int32_t __CFRunLoopRun(CFRunLoopRef rl, CFRunLoopModeRef rlm, CFTimeInterval seconds, Boolean stopAfterHandle, CFRunLoopModeRef previousMode) {
    //获取系统启动后的CPU运行时间，用于控制超时时间
    uint64_t startTSR = mach_absolute_time();

    //如果RunLoop或者mode是stop状态，则直接return，不进入循环
    if (__CFRunLoopIsStopped(rl)) {
        __CFRunLoopUnsetStopped(rl);
        return kCFRunLoopRunStopped;
    } else if (rlm->_stopped) {
        rlm->_stopped = false;
        return kCFRunLoopRunStopped;
    }

    //mach端口，在内核中，消息在端口之间传递。 初始为0
    mach_port_name_t dispatchPort = MACH_PORT_NULL;
    //判断是否为主线程
    Boolean libdispatchQSafe = pthread_main_np() && ((HANDLE_DISPATCH_ON_BASE_INVOCATION_ONLY && NULL == previousMode) || (!HANDLE_DISPATCH_ON_BASE_INVOCATION_ONLY && 0 == _CFGetTSD(__CFTSDKeyIsInGCDMainQ)));
    //如果在主线程 && runloop是主线程的runloop && 该mode是commonMode，则给mach端口赋值为主线程收发消息的端口
    if (libdispatchQSafe && (CFRunLoopGetMain() == rl) && CFSetContainsValue(rl->_commonModes, rlm->_name)) dispatchPort = _dispatch_get_main_queue_port_4CF();

#if USE_DISPATCH_SOURCE_FOR_TIMERS
    mach_port_name_t modeQueuePort = MACH_PORT_NULL;
    if (rlm->_queue) {
        //mode赋值为dispatch端口_dispatch_runloop_root_queue_perform_4CF
        modeQueuePort = _dispatch_runloop_root_queue_get_port_4CF(rlm->_queue);
        if (!modeQueuePort) {
            CRASH("Unable to get port for run loop mode queue (%d)", -1);
        }
    }
#endif

    //GCD管理的定时器，用于实现runloop超时机制
    dispatch_source_t timeout_timer = NULL;
    struct __timeout_context *timeout_context = (struct __timeout_context *)malloc(sizeof(*timeout_context));

    //立即超时
    if (seconds <= 0.0) { // instant timeout
        seconds = 0.0;
        timeout_context->termTSR = 0ULL;
    }
    //seconds为超时时间，超时时执行__CFRunLoopTimeout函数
    else if (seconds <= TIMER_INTERVAL_LIMIT) {
        dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_HIGH, DISPATCH_QUEUE_OVERCOMMIT);
        timeout_timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, queue);
        dispatch_retain(timeout_timer);
        timeout_context->ds = timeout_timer;
        timeout_context->rl = (CFRunLoopRef)CFRetain(rl);
        timeout_context->termTSR = startTSR + __CFTimeIntervalToTSR(seconds);
        dispatch_set_context(timeout_timer, timeout_context); // source gets ownership of context
        dispatch_source_set_event_handler_f(timeout_timer, __CFRunLoopTimeout);
        dispatch_source_set_cancel_handler_f(timeout_timer, __CFRunLoopTimeoutCancel);
        uint64_t ns_at = (uint64_t)((__CFTSRToTimeInterval(startTSR) + seconds) * 1000000000ULL);
        dispatch_source_set_timer(timeout_timer, dispatch_time(1, ns_at), DISPATCH_TIME_FOREVER, 1000ULL);
        dispatch_resume(timeout_timer);
    }
    //永不超时
    else { // infinite timeout
        seconds = 9999999999.0;
        timeout_context->termTSR = UINT64_MAX;
    }

    //标志位默认为true
    Boolean didDispatchPortLastTime = true;
    //记录最后runloop状态，用于return
    int32_t retVal = 0;
    do {
        //初始化一个存放内核消息的缓冲池
        uint8_t msg_buffer[3 * 1024];
#if DEPLOYMENT_TARGET_MACOSX || DEPLOYMENT_TARGET_EMBEDDED || DEPLOYMENT_TARGET_EMBEDDED_MINI
        mach_msg_header_t *msg = NULL;
        mach_port_t livePort = MACH_PORT_NULL;
#elif DEPLOYMENT_TARGET_WINDOWS
        HANDLE livePort = NULL;
        Boolean windowsMessageReceived = false;
#endif
        //取所有需要监听的port
        __CFPortSet waitSet = rlm->_portSet;

        //设置RunLoop为可以被唤醒状态
        __CFRunLoopUnsetIgnoreWakeUps(rl);

        //2.通知observer，即将触发timer回调，处理timer事件
        if (rlm->_observerMask & kCFRunLoopBeforeTimers) __CFRunLoopDoObservers(rl, rlm, kCFRunLoopBeforeTimers);
        //3.通知observer，即将触发Source0回调
        if (rlm->_observerMask & kCFRunLoopBeforeSources) __CFRunLoopDoObservers(rl, rlm, kCFRunLoopBeforeSources);

        //执行加入当前runloop的block
        __CFRunLoopDoBlocks(rl, rlm);

        //4.处理source0事件
        //有事件处理返回true，没有事件返回false
        Boolean sourceHandledThisLoop = __CFRunLoopDoSources0(rl, rlm, stopAfterHandle);
        if (sourceHandledThisLoop) {
            //执行加入当前runloop的block
            __CFRunLoopDoBlocks(rl, rlm);
        }

        //如果没有Sources0事件处理 并且 没有超时，poll为false
        //如果有Sources0事件处理 或者 超时，poll都为true
        Boolean poll = sourceHandledThisLoop || (0ULL == timeout_context->termTSR);

        //第一次do..whil循环不会走该分支，因为didDispatchPortLastTime初始化是true
        if (MACH_PORT_NULL != dispatchPort && !didDispatchPortLastTime) {
#if DEPLOYMENT_TARGET_MACOSX || DEPLOYMENT_TARGET_EMBEDDED || DEPLOYMENT_TARGET_EMBEDDED_MINI
            //从缓冲区读取消息
            msg = (mach_msg_header_t *)msg_buffer;
            //5.接收dispatchPort端口的消息，（接收source1事件）
            if (__CFRunLoopServiceMachPort(dispatchPort, &msg, sizeof(msg_buffer), &livePort, 0)) {
                //如果接收到了消息的话，前往第9步开始处理msg
                goto handle_msg;
            }
#elif DEPLOYMENT_TARGET_WINDOWS
            if (__CFRunLoopWaitForMultipleObjects(NULL, &dispatchPort, 0, 0, &livePort, NULL)) {
                goto handle_msg;
            }
#endif
        }

        didDispatchPortLastTime = false;

        //6.通知观察者RunLoop即将进入休眠
        if (!poll && (rlm->_observerMask & kCFRunLoopBeforeWaiting)) __CFRunLoopDoObservers(rl, rlm, kCFRunLoopBeforeWaiting);
        //设置RunLoop为休眠状态
        __CFRunLoopSetSleeping(rl);
        // do not do any user callouts after this point (after notifying of sleeping)

        // Must push the local-to-this-activation ports in on every loop
        // iteration, as this mode could be run re-entrantly and we don't
        // want these ports to get serviced.

        __CFPortSetInsert(dispatchPort, waitSet);

        __CFRunLoopModeUnlock(rlm);
        __CFRunLoopUnlock(rl);

#if DEPLOYMENT_TARGET_MACOSX || DEPLOYMENT_TARGET_EMBEDDED || DEPLOYMENT_TARGET_EMBEDDED_MINI
#if USE_DISPATCH_SOURCE_FOR_TIMERS
        //这里有个内循环，用于接收等待端口的消息
        //进入此循环后，线程进入休眠，直到收到新消息才跳出该循环，继续执行run loop
        do {
            if (kCFUseCollectableAllocator) {
                objc_clear_stack(0);
                memset(msg_buffer, 0, sizeof(msg_buffer));
            }
            msg = (mach_msg_header_t *)msg_buffer;
            //7.接收waitSet端口的消息
            __CFRunLoopServiceMachPort(waitSet, &msg, sizeof(msg_buffer), &livePort, poll ? 0 : TIMEOUT_INFINITY);
            //收到消息之后，livePort的值为msg->msgh_local_port，
            if (modeQueuePort != MACH_PORT_NULL && livePort == modeQueuePort) {
                // Drain the internal queue. If one of the callout blocks sets the timerFired flag, break out and service the timer.
                while (_dispatch_runloop_root_queue_perform_4CF(rlm->_queue));
                if (rlm->_timerFired) {
                    // Leave livePort as the queue port, and service timers below
                    rlm->_timerFired = false;
                    break;
                } else {
                    if (msg && msg != (mach_msg_header_t *)msg_buffer) free(msg);
                }
            } else {
                // Go ahead and leave the inner loop.
                break;
            }
        } while (1);
#else
        if (kCFUseCollectableAllocator) {
            objc_clear_stack(0);
            memset(msg_buffer, 0, sizeof(msg_buffer));
        }
        msg = (mach_msg_header_t *)msg_buffer;
        __CFRunLoopServiceMachPort(waitSet, &msg, sizeof(msg_buffer), &livePort, poll ? 0 : TIMEOUT_INFINITY);
#endif


#elif DEPLOYMENT_TARGET_WINDOWS
        // Here, use the app-supplied message queue mask. They will set this if they are interested in having this run loop receive windows messages.
        __CFRunLoopWaitForMultipleObjects(waitSet, NULL, poll ? 0 : TIMEOUT_INFINITY, rlm->_msgQMask, &livePort, &windowsMessageReceived);
#endif

        __CFRunLoopLock(rl);
        __CFRunLoopModeLock(rlm);

        // Must remove the local-to-this-activation ports in on every loop
        // iteration, as this mode could be run re-entrantly and we don't
        // want these ports to get serviced. Also, we don't want them left
        // in there if this function returns.

        __CFPortSetRemove(dispatchPort, waitSet);


        __CFRunLoopSetIgnoreWakeUps(rl);

        // user callouts now OK again
        //取消runloop的休眠状态
        __CFRunLoopUnsetSleeping(rl);
        //8.通知观察者runloop被唤醒
        if (!poll && (rlm->_observerMask & kCFRunLoopAfterWaiting)) __CFRunLoopDoObservers(rl, rlm, kCFRunLoopAfterWaiting);

        //9.处理收到的消息
    handle_msg:;
        __CFRunLoopSetIgnoreWakeUps(rl);

#if DEPLOYMENT_TARGET_WINDOWS
        if (windowsMessageReceived) {
            // These Win32 APIs cause a callout, so make sure we're unlocked first and relocked after
            __CFRunLoopModeUnlock(rlm);
            __CFRunLoopUnlock(rl);

            if (rlm->_msgPump) {
                rlm->_msgPump();
            } else {
                MSG msg;
                if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE | PM_NOYIELD)) {
                    TranslateMessage(&msg);
                    DispatchMessage(&msg);
                }
            }

            __CFRunLoopLock(rl);
            __CFRunLoopModeLock(rlm);
            sourceHandledThisLoop = true;

            // To prevent starvation of sources other than the message queue, we check again to see if any other sources need to be serviced
            // Use 0 for the mask so windows messages are ignored this time. Also use 0 for the timeout, because we're just checking to see if the things are signalled right now -- we will wait on them again later.
            // NOTE: Ignore the dispatch source (it's not in the wait set anymore) and also don't run the observers here since we are polling.
            __CFRunLoopSetSleeping(rl);
            __CFRunLoopModeUnlock(rlm);
            __CFRunLoopUnlock(rl);

            __CFRunLoopWaitForMultipleObjects(waitSet, NULL, 0, 0, &livePort, NULL);

            __CFRunLoopLock(rl);
            __CFRunLoopModeLock(rlm);
            __CFRunLoopUnsetSleeping(rl);
            // If we have a new live port then it will be handled below as normal
        }


#endif
        if (MACH_PORT_NULL == livePort) {
            CFRUNLOOP_WAKEUP_FOR_NOTHING();
            // handle nothing
            //通过CFRunloopWake唤醒
        } else if (livePort == rl->_wakeUpPort) {
            CFRUNLOOP_WAKEUP_FOR_WAKEUP();
            //什么都不干，跳回2重新循环
            // do nothing on Mac OS
#if DEPLOYMENT_TARGET_WINDOWS
            // Always reset the wake up port, or risk spinning forever
            ResetEvent(rl->_wakeUpPort);
#endif
        }
#if USE_DISPATCH_SOURCE_FOR_TIMERS
        //如果是定时器事件
        else if (modeQueuePort != MACH_PORT_NULL && livePort == modeQueuePort) {
            CFRUNLOOP_WAKEUP_FOR_TIMER();
            //9.1 处理timer事件
            if (!__CFRunLoopDoTimers(rl, rlm, mach_absolute_time())) {
                // Re-arm the next timer, because we apparently fired early
                __CFArmNextTimerInMode(rlm, rl);
            }
        }
#endif
#if USE_MK_TIMER_TOO
        //如果是定时器事件
        else if (rlm->_timerPort != MACH_PORT_NULL && livePort == rlm->_timerPort) {
            CFRUNLOOP_WAKEUP_FOR_TIMER();
            // On Windows, we have observed an issue where the timer port is set before the time which we requested it to be set. For example, we set the fire time to be TSR 167646765860, but it is actually observed firing at TSR 167646764145, which is 1715 ticks early. The result is that, when __CFRunLoopDoTimers checks to see if any of the run loop timers should be firing, it appears to be 'too early' for the next timer, and no timers are handled.
            // In this case, the timer port has been automatically reset (since it was returned from MsgWaitForMultipleObjectsEx), and if we do not re-arm it, then no timers will ever be serviced again unless something adjusts the timer list (e.g. adding or removing timers). The fix for the issue is to reset the timer here if CFRunLoopDoTimers did not handle a timer itself. 9308754
           //9.1处理timer事件
            if (!__CFRunLoopDoTimers(rl, rlm, mach_absolute_time())) {
                // Re-arm the next timer
                __CFArmNextTimerInMode(rlm, rl);
            }
        }
#endif
        //如果是dispatch到main queue的block
        else if (livePort == dispatchPort) {
            CFRUNLOOP_WAKEUP_FOR_DISPATCH();
            __CFRunLoopModeUnlock(rlm);
            __CFRunLoopUnlock(rl);
            _CFSetTSD(__CFTSDKeyIsInGCDMainQ, (void *)6, NULL);
#if DEPLOYMENT_TARGET_WINDOWS
            void *msg = 0;
#endif
            //9.2执行block
            __CFRUNLOOP_IS_SERVICING_THE_MAIN_DISPATCH_QUEUE__(msg);
            _CFSetTSD(__CFTSDKeyIsInGCDMainQ, (void *)0, NULL);
            __CFRunLoopLock(rl);
            __CFRunLoopModeLock(rlm);
            sourceHandledThisLoop = true;
            didDispatchPortLastTime = true;
        } else {
            CFRUNLOOP_WAKEUP_FOR_SOURCE();
            // Despite the name, this works for windows handles as well
            CFRunLoopSourceRef rls = __CFRunLoopModeFindSourceForMachPort(rl, rlm, livePort);
            // 有source1事件待处理
            if (rls) {
#if DEPLOYMENT_TARGET_MACOSX || DEPLOYMENT_TARGET_EMBEDDED || DEPLOYMENT_TARGET_EMBEDDED_MINI
                mach_msg_header_t *reply = NULL;
                //9.2 处理source1事件
                sourceHandledThisLoop = __CFRunLoopDoSource1(rl, rlm, rls, msg, msg->msgh_size, &reply) || sourceHandledThisLoop;
                if (NULL != reply) {
                    (void)mach_msg(reply, MACH_SEND_MSG, reply->msgh_size, 0, MACH_PORT_NULL, 0, MACH_PORT_NULL);
                    CFAllocatorDeallocate(kCFAllocatorSystemDefault, reply);
                }
#elif DEPLOYMENT_TARGET_WINDOWS
                sourceHandledThisLoop = __CFRunLoopDoSource1(rl, rlm, rls) || sourceHandledThisLoop;
#endif
            }
        }
#if DEPLOYMENT_TARGET_MACOSX || DEPLOYMENT_TARGET_EMBEDDED || DEPLOYMENT_TARGET_EMBEDDED_MINI
        if (msg && msg != (mach_msg_header_t *)msg_buffer) free(msg);
#endif

        __CFRunLoopDoBlocks(rl, rlm);

        if (sourceHandledThisLoop && stopAfterHandle) {
            //进入run loop时传入的参数，处理完事件就返回
            retVal = kCFRunLoopRunHandledSource;
        }else if (timeout_context->termTSR < mach_absolute_time()) {
            //run loop超时
            retVal = kCFRunLoopRunTimedOut;
        }else if (__CFRunLoopIsStopped(rl)) {
            //run loop被手动终止
            __CFRunLoopUnsetStopped(rl);
            retVal = kCFRunLoopRunStopped;
        }else if (rlm->_stopped) {
            //mode被终止
            rlm->_stopped = false;
            retVal = kCFRunLoopRunStopped;
        }else if (__CFRunLoopModeIsEmpty(rl, rlm, previousMode)) {
            //mode中没有要处理的事件
            retVal = kCFRunLoopRunFinished;
        }
        //除了上面这几种情况，都继续循环
    } while (0 == retVal);

    if (timeout_timer) {
        dispatch_source_cancel(timeout_timer);
        dispatch_release(timeout_timer);
    } else {
        free(timeout_context);
    }

    return retVal;
}
```

## __CFRunLoopServiceMachPort

第7步调用了`__CFRunLoopServiceMachPort`函数，这个函数在Runloop中起到了至关重要的作用，下面给出了详细注释。

```
/**
 *  接收指定内核端口的消息
 *
 *  @param port        接收消息的端口
 *  @param buffer      消息缓冲区
 *  @param buffer_size 消息缓冲区大小
 *  @param livePort    暂且理解为活动的端口，接收消息成功时候值为msg->msgh_local_port，超时时为MACH_PORT_NULL
 *  @param timeout     超时时间，单位是ms，如果超时，则RunLoop进入休眠状态
 *
 *  @return 接收消息成功时返回true 其他情况返回false
 */
static Boolean __CFRunLoopServiceMachPort(mach_port_name_t port, mach_msg_header_t **buffer, size_t buffer_size, mach_port_t *livePort, mach_msg_timeout_t timeout) {
    Boolean originalBuffer = true;
    kern_return_t ret = KERN_SUCCESS;
    for (;;) {      /* In that sleep of death what nightmares may come ... */
        mach_msg_header_t *msg = (mach_msg_header_t *)*buffer;
        msg->msgh_bits = 0;  //消息头的标志位
        msg->msgh_local_port = port;  //源(发出的消息)或者目标(接收的消息)
        msg->msgh_remote_port = MACH_PORT_NULL; //目标(发出的消息)或者源(接收的消息)
        msg->msgh_size = buffer_size;  //消息缓冲区大小，单位是字节
        msg->msgh_id = 0;  //唯一id

        if (TIMEOUT_INFINITY == timeout) { CFRUNLOOP_SLEEP(); } else { CFRUNLOOP_POLL(); }

        //通过mach_msg发送或者接收的消息都是指针，
        //如果直接发送或者接收消息体，会频繁进行内存复制，损耗性能
        //所以XNU使用了单一内核的方式来解决该问题，所有内核组件都共享同一个地址空间，因此传递消息时候只需要传递消息的指针
        ret = mach_msg(msg,
                       MACH_RCV_MSG|MACH_RCV_LARGE|((TIMEOUT_INFINITY != timeout) ? MACH_RCV_TIMEOUT : 0)|MACH_RCV_TRAILER_TYPE(MACH_MSG_TRAILER_FORMAT_0)|MACH_RCV_TRAILER_ELEMENTS(MACH_RCV_TRAILER_AV),
                       0,
                       msg->msgh_size,
                       port,
                       timeout,
                       MACH_PORT_NULL);
        CFRUNLOOP_WAKEUP(ret);

        //接收/发送消息成功，给livePort赋值为msgh_local_port
        if (MACH_MSG_SUCCESS == ret) {
            *livePort = msg ? msg->msgh_local_port : MACH_PORT_NULL;
            return true;
        }

        //MACH_RCV_TIMEOUT
        //超出timeout时间没有收到消息，返回MACH_RCV_TIMED_OUT
        //此时释放缓冲区，把livePort赋值为MACH_PORT_NULL
        if (MACH_RCV_TIMED_OUT == ret) {
            if (!originalBuffer) free(msg);
            *buffer = NULL;
            *livePort = MACH_PORT_NULL;
            return false;
        }

        //MACH_RCV_LARGE
        //如果接收缓冲区太小，则将过大的消息放在队列中，并且出错返回MACH_RCV_TOO_LARGE，
        //这种情况下，只返回消息头，调用者可以分配更多的内存
        if (MACH_RCV_TOO_LARGE != ret) break;
        //此处给buffer分配更大内存
        buffer_size = round_msg(msg->msgh_size + MAX_TRAILER_SIZE);
        if (originalBuffer) *buffer = NULL;
        originalBuffer = false;
        *buffer = realloc(*buffer, buffer_size);
    }
    HALT;
    return false;
}
```

## 小结

RunLoop实际很简单，它是一个对象，它和线程是一一对应的，每个线程都有一个对应的RunLoop对象，主线程的RunLoop会在程序启动时自动创建，子线程需要手动获取来创建。

RunLoop运行的核心是一个do..while..循环，遍历所有需要处理的事件，如果有事件处理就让线程工作，没有事件处理则让线程休眠，同时等待事件到来。


# RunLoop应用

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/Runloop-Cocoa.jpg)

在开发过程中几乎所有的操作都是通过Call out进行回调的，无论是Observer的状态通知还是Timer、Source的处理，而系统在回调时通常使用如下几个函数进行回调，换句话说你的代码其实最终都是通过下面几个函数来负责调用的，即使你自己监听Observer也会先调用下面的函数然后间接通知你，所以在调用堆栈中经常看到这些函数：

```
    static void __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__();
    static void __CFRUNLOOP_IS_CALLING_OUT_TO_A_BLOCK__();
    static void __CFRUNLOOP_IS_SERVICING_THE_MAIN_DISPATCH_QUEUE__();
    static void __CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__();
    static void __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__();
    static void __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE1_PERFORM_FUNCTION__();

```

实际的代码块如下：

```
{
    /// 1. 通知Observers，即将进入RunLoop
    /// 此处有Observer会创建AutoreleasePool: _objc_autoreleasePoolPush();
    __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__(kCFRunLoopEntry);
    do {

        /// 2. 通知 Observers: 即将触发 Timer 回调。
        __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__(kCFRunLoopBeforeTimers);
        /// 3. 通知 Observers: 即将触发 Source (非基于port的,Source0) 回调。
        __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__(kCFRunLoopBeforeSources);
        __CFRUNLOOP_IS_CALLING_OUT_TO_A_BLOCK__(block);

        /// 4. 触发 Source0 (非基于port的) 回调。
        __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__(source0);
        __CFRUNLOOP_IS_CALLING_OUT_TO_A_BLOCK__(block);

        /// 6. 通知Observers，即将进入休眠
        /// 此处有Observer释放并新建AutoreleasePool: _objc_autoreleasePoolPop(); _objc_autoreleasePoolPush();
        __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__(kCFRunLoopBeforeWaiting);

        /// 7. sleep to wait msg.
        mach_msg() -> mach_msg_trap();

        /// 8. 通知Observers，线程被唤醒
        __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__(kCFRunLoopAfterWaiting);

        /// 9. 如果是被Timer唤醒的，回调Timer
        __CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__(timer);

        /// 9. 如果是被dispatch唤醒的，执行所有调用 dispatch_async 等方法放入main queue 的 block
        __CFRUNLOOP_IS_SERVICING_THE_MAIN_DISPATCH_QUEUE__(dispatched_block);

        /// 9. 如果如果Runloop是被 Source1 (基于port的) 的事件唤醒了，处理这个事件
        __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE1_PERFORM_FUNCTION__(source1);


    } while (...);

    /// 10. 通知Observers，即将退出RunLoop
    /// 此处有Observer释放AutoreleasePool: _objc_autoreleasePoolPop();
    __CFRUNLOOP_IS_CALLING_OUT_TO_AN_OBSERVER_CALLBACK_FUNCTION__(kCFRunLoopExit);
}
```

例如在控制器的`touchesBegan:`中打入断点查看堆栈（由于UIEvent是Source0，所以可以看到一个Source0的Call out函数`CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION`调用）：

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/Runloop-Call%20out%20Source0.png)

## NSTimer 与 GCD Timer、CADisplayLink

### NSTimer

前面一直提到Timer Source作为事件源，事实上它的上层对应就是NSTimer（其实就是CFRunloopTimerRef）这个开发者经常用到的定时器（底层基于使用mk_timer实现）。

NSTimer 其实就是 CFRunLoopTimerRef，他们之间是 toll-free bridged 的。一个 NSTimer 注册到 RunLoop 后，RunLoop 会为其重复的时间点注册好事件。例如 10:00, 10:10, 10:20 这几个时间点。RunLoop为了节省资源，并不会在非常准确的时间点回调这个Timer。Timer 有个属性叫做 Tolerance (宽容度)，标示了当时间点到后，容许有多少最大误差。由于 NSTimer 的这种机制，因此 NSTimer 的执行必须依赖于 RunLoop，如果没有 RunLoop，NSTimer 是不会执行的。

如果某个时间点被错过了，例如执行了一个很长的任务，则那个时间点的回调也会跳过去，不会延后执行。就比如等公交，如果 10:10 时我忙着玩手机错过了那个点的公交，那我只能等 10:20 这一趟了。

### GCD Timer

GCD 则不同，GCD 的线程管理是通过系统来直接管理的。GCD Timer 是通过 dispatch port 给 RunLoop 发送消息，来使 RunLoop 执行相应的 block，如果所在线程没有 RunLoop，那么 GCD 会临时创建一个线程去执行 block，执行完之后再销毁掉，因此 GCD 的 Timer 是不依赖 RunLoop 的。

至于这两个 Timer 的准确性问题，如果不在 RunLoop 的线程里面执行，那么只能使用 GCD Timer，由于 GCD Timer 是基于 MKTimer(mach kernel timer)，已经很底层了，因此是很准确的。

如果在 RunLoop 的线程里面执行，由于 GCD Timer 和 NSTimer 都是通过 port 发送消息的机制来触发 RunLoop 的，因此准确性差别应该不是很大。如果线程 RunLoop 阻塞了，不管是 GCD Timer 还是 NSTimer 都会存在延迟问题。

### CADisplayLink

CADisplayLink是一个执行频率（fps）和屏幕刷新相同（可以修改preferredFramesPerSecond改变刷新频率）的定时器，它也需要加入到RunLoop才能执行。与NSTimer类似，CADisplayLink同样是基于CFRunloopTimerRef实现，底层使用mk_timer（可以比较加入到RunLoop前后RunLoop中timer的变化）。和NSTimer相比它精度更高（尽管NSTimer也可以修改精度），不过和NStimer类似的是如果遇到大任务它仍然存在丢帧现象。通常情况下CADisaplayLink用于构建帧动画，看起来相对更加流畅，而NSTimer则有更广泛的用处。

## AutoreleasePool

AutoreleasePool是另一个与RunLoop相关讨论较多的话题。其实从RunLoop源代码分析，AutoreleasePool与RunLoop并没有直接的关系，之所以将两个话题放到一起讨论最主要的原因是因为在iOS应用启动后会注册两个Observer管理和维护AutoreleasePool。不妨在应用程序刚刚启动时打印currentRunLoop可以看到系统默认注册了很多个Observer，其中有两个Observer的callout都是` _ wrapRunLoopWithAutoreleasePoolHandler`，这两个是和自动释放池相关的两个监听。

```
<CFRunLoopObserver 0x6080001246a0 [0x101f81df0]>{valid = Yes, activities = 0x1, repeats = Yes, order = -2147483647, callout = _wrapRunLoopWithAutoreleasePoolHandler (0x1020e07ce), context = <CFArray 0x60800004cae0 [0x101f81df0]>{type = mutable-small, count = 0, values = ()}}
<CFRunLoopObserver 0x608000124420 [0x101f81df0]>{valid = Yes, activities = 0xa0, repeats = Yes, order = 2147483647, callout = _wrapRunLoopWithAutoreleasePoolHandler (0x1020e07ce), context = <CFArray 0x60800004cae0 [0x101f81df0]>{type = mutable-small, count = 0, values = ()}}
```

第一个Observer会监听RunLoop的进入，它会回调objc_autoreleasePoolPush()向当前的AutoreleasePoolPage增加一个哨兵对象标志创建自动释放池。这个Observer的order是-2147483647优先级最高，确保发生在所有回调操作之前。

第二个Observer会监听RunLoop的进入休眠和即将退出RunLoop两种状态，在即将进入休眠时会调用`objc_autoreleasePoolPop()`和 `objc_autoreleasePoolPush()`根据情况从最新加入的对象一直往前清理直到遇到哨兵对象。而在即将退出RunLoop时会调用`objc_autoreleasePoolPop()`释放自动自动释放池内对象。这个Observer的order是2147483647，优先级最低，确保发生在所有回调操作之后。

主线程的其他操作通常均在这个AutoreleasePool之内（main函数中），以尽可能减少内存维护操作（当然你如果需要显式释放，例如循环时，可以自己创建AutoreleasePool否则一般不需要自己创建）。

其实在应用程序启动后系统还注册了其他Observer（例如即将进入休眠时执行注册回调`_UIGestureRecognizerUpdateObserver`用于手势处理、回调为`_ZN2CA11Transaction17observer_callbackEP19__CFRunLoopObservermPv`的Observer用于界面实时绘制更新）和多个Source1（例如context为CFMachPort的Source1用于接收硬件事件响应进而分发到应用程序一直到UIEvent）。

在主线程执行的代码，通常是写在诸如事件回调、Timer回调内的。这些回调会被 RunLoop 创建好的 AutoreleasePool 环绕着，所以不会出现内存泄漏，开发者也不必显示创建 Pool 了。

自动释放池的创建和释放，销毁的时机如下所示

- kCFRunLoopEntry; // 进入runloop之前，创建一个自动释放池
- kCFRunLoopBeforeWaiting; // 休眠之前，销毁自动释放池，创建一个新的自动释放池
- kCFRunLoopExit; // 退出runloop之前，销毁自动释放池

## 事件响应

苹果注册了一个 `Source1` (基于 `mach port` 的) 用来接收系统事件，其回调函数为 `__IOHIDEventSystemClientQueueCallback()`。

当一个硬件事件（触摸/锁屏/摇晃等）发生后，首先由 `IOKit.framework` 生成一个 `IOHIDEvent` 事件并由 `SpringBoard` 接收。这个过程的详细情况可以参考[这里](http://iphonedevwiki.net/index.php/IOHIDFamily)。`SpringBoard` 只接收按键（锁屏/静音等），触摸，加速，接近传感器等几种 `Event`，随后用 `mach port` 转发给需要的 App 进程。随后苹果注册的那个 `Source1` 就会触发回调，并调用 `_UIApplicationHandleEventQueue()` 进行应用内部的分发。

`_UIApplicationHandleEventQueue()` 会把 `IOHIDEvent` 处理并包装成 `UIEvent` 进行处理或分发，其中包括识别 `UIGesture`/处理屏幕旋转/发送给 `UIWindow` 等。通常事件比如 `UIButton` 点击、`touchesBegin/Move/End/Cancel` 事件都是在这个回调中完成的。

## 手势识别

当上面的 `_UIApplicationHandleEventQueue()` 识别了一个手势时，其首先会调用 `Cancel` 将当前的 `touchesBegin/Move/End` 系列回调打断。随后系统将对应的 `UIGestureRecognizer` 标记为待处理。
苹果注册了一个 `Observer` 监测 `BeforeWaiting` (Loop即将进入休眠) 事件，这个 `Observer` 的回调函数是 `_UIGestureRecognizerUpdateObserver()`，其内部会获取所有刚被标记为待处理的 `GestureRecognizer`，并执行 `GestureRecognizer` 的回调。
当有 `UIGestureRecognizer` 的变化（创建/销毁/状态改变）时，这个回调都会进行相应处理。

## UI更新

如果打印App启动之后的主线程RunLoop可以发现另外一个callout为`_ZN2CA11Transaction17observer_callbackEP19__CFRunLoopObservermPv`的Observer，这个监听专门负责UI变化后的更新，比如修改了frame、调整了UI层级（UIView/CALayer）或者手动设置了setNeedsDisplay/setNeedsLayout之后就会将这些操作提交到全局容器。而这个Observer监听了主线程RunLoop的即将进入休眠和退出状态，一旦进入这两种状态则会遍历所有的UI更新并提交进行实际绘制更新。

这个函数内部的调用栈大概是这样的：

```
_ZN2CA11Transaction17observer_callbackEP19__CFRunLoopObservermPv()
    QuartzCore:CA::Transaction::observer_callback:
        CA::Transaction::commit();
            CA::Context::commit_transaction();
                CA::Layer::layout_and_display_if_needed();
                    CA::Layer::layout_if_needed();
                        [CALayer layoutSublayers];
                            [UIView layoutSubviews];
                    CA::Layer::display_if_needed();
                        [CALayer display];
                            [UIView drawRect];
```

通常情况下这种方式是完美的，因为除了系统的更新，还可以利用`setNeedsDisplay`等方法手动触发下一次RunLoop运行的更新。但是如果当前正在执行大量的逻辑运算可能UI的更新就会比较卡，因此Facebook推出了`AsyncDisplayKit`来解决这个问题。[AsyncDisplayKit](https://github.com/facebookarchive/AsyncDisplayKit)其实是将UI排版和绘制运算尽可能放到后台，将UI的最终更新操作放到主线程（这一步也必须在主线程完成），同时提供一套类`UIView`或`CALayer`的相关属性，尽可能保证开发者的开发习惯。这个过程中`AsyncDisplayKit`在主线程RunLoop中增加了一个`Observer`监听即将进入休眠和退出RunLoop两种状态，收到回调时遍历队列中的待处理任务一一执行。

## NSURLConnection

一旦启动NSURLConnection以后就会不断调用delegate方法接收数据，这样一个连续的的动作正是基于RunLoop来运行。

一旦NSURLConnection设置了delegate会立即创建一个线程com.apple.NSURLConnectionLoader，同时内部启动RunLoop并在NSDefaultMode模式下添加4个Source0。其中CFHTTPCookieStorage用于处理cookie，CFMultiplexerSource负责各种delegate回调并在回调中唤醒delegate内部的RunLoop（通常是主线程）来执行实际操作。

早期版本的AFNetworking库也是基于NSURLConnection实现，为了能够在后台接收delegate回调AFNetworking内部创建了一个空的线程并启动了RunLoop，当需要使用这个后台线程执行任务时AFNetworking通过 `performSelector: onThread:` 将这个任务放到后台线程的RunLoop中。

当调用 `performSelector:onThread:` 时，实际上其会创建一个 Timer 加到对应的线程去，同样的，如果对应线程没有 RunLoop 该方法也会失效。

## GCD和RunLoop的关系

在RunLoop的源代码中可以看到用到了GCD的相关内容，但是RunLoop本身和GCD并没有直接的关系。当调用了`dispatch_async(dispatch_get_main_queue(), <#^(void)block#>)`时libDispatch会向主线程RunLoop发送消息唤醒RunLoop，RunLoop从消息中获取block，并且在`__CFRUNLOOP_IS_SERVICING_THE_MAIN_DISPATCH_QUEUE__`回调里执行这个block。不过这个操作仅限于主线程，其他线程dispatch操作是全部由libDispatch驱动的。

## 更多RunLoop的实践

### 滚动Scrollview导致定时器失效

在界面上有一个UIScrollview控件，如果此时还有一个定时器在执行一个事件，你会发现当你滚动Scrollview的时候，定时器会失效。

```
- (void)viewDidLoad {
    [super viewDidLoad];
    [self timer1];
    [self timer2];
}

//下面两种添加定时器的方法效果相同，都是在主线程中添加定时器
- (void)timer1 {
    NSTimer *timer = [NSTimer timerWithTimeInterval:2.0 target:self selector:@selector(run) userInfo:nil repeats:YES];
    [[NSRunLoop currentRunLoop] addTimer:timer forMode:NSRunLoopDefaultModes];
}

- (void)timer2 {
    [NSTimer scheduledTimerWithTimeInterval:2.0 target:self selector:@selector(run) userInfo:nil repeats:YES];
}
```

因为当你滚动Scrollview的时候，RunLoop会切换到UITrackingRunLoopMode 模式，而定时器运行在defaultMode下面，系统一次只能处理一种模式的RunLoop，所以导致defaultMode下的定时器失效。

解决方法：

- 把timer注册到NSRunLoopCommonModes，它包含了defaultMode和trackingMode两种模式。

```
[[NSRunLoop currentRunLoop] addTimer:timer forMode:NSRunLoopCommonModes];
```

- 使用GCD创建定时器，GCD创建的定时器不会受RunLoop的影响

```
    // 获得队列
    dispatch_queue_t queue = dispatch_get_main_queue();

    // 创建一个定时器(dispatch_source_t本质还是个OC对象)
    self.timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, queue);

    // 设置定时器的各种属性（几时开始任务，每隔多长时间执行一次）
    // GCD的时间参数，一般是纳秒（1秒 == 10的9次方纳秒）
    // 比当前时间晚1秒开始执行
    dispatch_time_t start = dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1.0 * NSEC_PER_SEC));

    //每隔一秒执行一次
    uint64_t interval = (uint64_t)(1.0 * NSEC_PER_SEC);
    dispatch_source_set_timer(self.timer, start, interval, 0);

    // 设置回调
    dispatch_source_set_event_handler(self.timer, ^{
        NSLog(@"------------%@", [NSThread currentThread]);

    });

    // 启动定时器
    dispatch_resume(self.timer);
```

### 图片下载

由于图片渲染到屏幕需要消耗较多资源，为了提高用户体验，当用户滚动Tableview的时候，只在后台下载图片，但是不显示图片，当用户停下来的时候才显示图片。

```
[self.imageView performSelector:@selector(setImage:) withObject:[UIImage imageNamed:@"imgName"] afterDelay:3.0 inModes:@[NSDefaultRunLoopMode]];
```

上面的代码可以达到如下效果：
用户点击屏幕，在主线程中，三秒之后显示图片，但是当用户点击屏幕之后，如果此时用户又开始滚动textview，那么就算过了三秒，图片也不会显示出来，当用户停止了滚动，才会显示图片。
这是因为限定了方法setImage只能在NSDefaultRunLoopMode 模式下使用。而滚动textview的时候，程序运行在tracking模式下面，所以方法setImage不会执行。

### 常驻线程

需要创建一个在后台一直存在的程序，来做一些需要频繁处理的任务。比如检测网络状态等。

默认情况一个线程创建出来，运行完要做的事情，线程就会消亡。而程序启动的时候，就创建的主线程已经加入到RunLoop，所以主线程不会消亡。

这个时候我们就需要把自己创建的线程加到RunLoop中来，就可以实现线程常驻后台。

```
- (void)viewDidLoad {
    [super viewDidLoad];

    self.thread = [[NSThread alloc] initWithTarget:self selector:@selector(run) object:nil];
    [self.thread start];
}

- (void)run
{
    NSLog(@"----------run----%@", [NSThread currentThread]);
    @autoreleasepool{
    /*如果不加这句，会发现runloop创建出来就挂了，因为runloop如果没有CFRunLoopSourceRef事件源输入或者定时器，就会立马消亡。
      下面的方法给runloop添加一个NSport，就是添加一个事件源，也可以添加一个定时器，或者observer，让runloop不会挂掉*/
    [[NSRunLoop currentRunLoop] addPort:[NSPort port] forMode:NSDefaultRunLoopMode];

    // 方法1 ,2，3实现的效果相同，让runloop无限期运行下去
    [[NSRunLoop currentRunLoop] run];
   }


    // 方法2
    [[NSRunLoop currentRunLoop] runMode:NSDefaultRunLoopMode beforeDate:[NSDate distantFuture]];

    // 方法3
    [[NSRunLoop currentRunLoop] runUntilDate:[NSDate distantFuture]];

    NSLog(@"---------");
}

- (void)test
{
    NSLog(@"----------test----%@", [NSThread currentThread]);
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self performSelector:@selector(test) onThread:self.thread withObject:nil waitUntilDone:NO];
}
```

```
- (void)viewDidLoad {
    [super viewDidLoad];

    self.thread = [[NSThread alloc] initWithTarget:self selector:@selector(run) object:nil];
    [self.thread start];
}
- (void)run
{
    [NSTimer scheduledTimerWithTimeInterval:2.0 target:self selector:@selector(test) userInfo:nil repeats:YES];
    [[NSRunLoop currentRunLoop] run];
}
```

如果没有实现添加NSPort或者NSTimer，会发现执行完run方法，线程就会消亡，后续再执行touchbegan方法无效。

我们必须保证线程不消亡，才可以在后台接受时间处理

RunLoop 启动前内部必须要有至少一个 Timer/Observer/Source，所以在 [runLoop run] 之前先创建了一个新的 NSMachPort 添加进去了。通常情况下，调用者需要持有这个 NSMachPort (mach_port) 并在外部线程通过这个 port 发送消息到 RunLoop 内；但此处添加 port 只是为了让 RunLoop 不至于退出，并没有用于实际的发送消息。

可以发现执行完了run方法，这个时候再点击屏幕，可以不断执行test方法，因为线程self.thread一直常驻后台，等待事件加入其中，然后执行。

### 观察事件状态，优化性能

假设我们想实现cell的高度缓存计算，因为“计算cell的预缓存高度”的任务需要在最无感知的时刻进行，所以应该同时满足：

- RunLoop 处于“空闲”状态 Mode
- 当这一次 RunLoop 迭代处理完成了所有事件，马上要休眠时

```
CFRunLoopRef runLoop = CFRunLoopGetCurrent();
CFStringRef runLoopMode = kCFRunLoopDefaultMode;
CFRunLoopObserverRef observer = CFRunLoopObserverCreateWithHandler
(kCFAllocatorDefault, kCFRunLoopBeforeWaiting, true, 0, ^(CFRunLoopObserverRef observer, CFRunLoopActivity _) {
    // TODO here
});
CFRunLoopAddObserver(runLoop, observer, runLoopMode);
在其中的 TODO 位置，就可以开始任务的收集和分发了，当然，不能忘记适时的移除这个 observer
```

为了优化程序启动速度，我们通过 CFRunLoopObserver 观察主线程是否处于空闲状态，只有主线程处于空闲状态的时候才执行某些低优先级的后台任务，从而避免 CPU 和内存资源被占用导致卡顿或者掉帧。


# 参考文章

[Run Loops - 官方文档](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Multithreading/RunLoopManagement/RunLoopManagement.html)

[iOS 线下分享《RunLoop》by 孙源@sunnyxx](https://v.youku.com/v_show/id_XODgxODkzODI0.html)

[深入理解 NSRunLoop - Jake Hao](https://www.jakehao.com/understanding-nsrunloop)

[iOS RunLoop 详解 - jackyshan](https://juejin.cn/post/6844903588712415239#heading-24)

[深入理解 RunLoop - ibireme](https://blog.ibireme.com/2015/05/18/runloop/)

[RunLoop - 怪兽](https://xiaopengmonsters.github.io/categories/RunLoop/)
