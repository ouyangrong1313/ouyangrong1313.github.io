---
title: 深入理解 iOS 内存管理（Memory Management）
author: Ouyang Rong
date: 2021-09-18 18:11:00 +0800
categories: [iOS, 内存管理]
tags: [ARC, MRC]
---

# 前言

苹果在 2011 年的时候，在 WWDC 大会上提出了自动的引用计数（ARC）。ARC 背后的原理是依赖编译器的静态分析能力，通过在编译时找出合理的插入引用计数管理代码，从而彻底解放程序员。

在 ARC 刚刚出来的时候，业界对此黑科技充满了怀疑和观望，加上现有的 MRC 代码要做迁移本来也需要额外的成本，所以 ARC 并没有被很快接受。直到 2013 年左右，苹果认为 ARC 技术足够成熟，直接将 macOS（当时叫 OS X）上的垃圾回收机制废弃，从而使得 ARC 迅速被接受。

2014 年的 WWDC 大会上，苹果推出了 Swift 语言，而该语言仍然使用 ARC 技术，作为其内存管理方式。-- [Automatic Reference Counting](https://docs.swift.org/swift-book/LanguageGuide/AutomaticReferenceCounting.html)

![内存管理](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86.png)


内存管理不是iOS特有，几乎所有程序员都会遇到内存管理的问题。内存分栈区和堆区，栈区靠操作系统申请释放无需程序员关心，需要关心的是堆区内存的申请和释放。

原理说起来很容易就是申请和释放要配对出现，常见有三种释放内存的方式：

- 显式释放内存：C的free，C++的delete
- 基于引用计数释放内存：C++的Smart Pointer，Objective-C
- 垃圾回收：Java，C#

iOS一直不支持垃圾回收（OS X曾短暂支持过现已废弃），只支持引用计数方式管理内存，从早期的MRC演进到了现在的ARC。


# Heap(堆)和stack(栈)

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%A0%86%E5%92%8C%E6%A0%88.png)

栈里面存放的是值类型，堆里面存放的是对象类型。对象的引用计数是在堆内存中操作的。

## 堆是什么


> 引自维基百科堆（英语：Heap）是计算机科学中一类特殊的数据结构的统称。堆通常是一个可以被看做一棵树的数组对象。在队列中，调度程序反复提取队列中第一个作业并运行，因为实际情况中某些时间较短的任务将等待很长时间才能结束，或者某些不短小，但具有重要性的作业，同样应当具有优先权。堆即为解决此类问题设计的一种数据结构。

> 堆(Heap)又被为优先队列(priority queue)。尽管名为优先队列，但堆并不是队列。回忆一下，在队列中，我们可以进行的限定操作是dequeue和enqueue。dequeue是按照进入队列的先后顺序来取出元素。而在堆中，我们不是按照元素进入队列的先后顺序取出元素的，而是按照元素的优先级取出元素。

这就好像候机的时候，无论谁先到达候机厅，总是头等舱的乘客先登机，然后是商务舱的乘客，最后是经济舱的乘客。每个乘客都有头等舱、商务舱、经济舱三种个键值(key)中的一个。头等舱->商务舱->经济舱依次享有从高到低的优先级。

总的来说，堆是一种数据结构，数据的插入和删除是根据优先级定的，他有几个特性：

- 任意节点的优先级不小于它的子节点
- 每个节点值都小于或等于它的子节点
- 主要操作是插入和删除最小元素(元素值本身为优先级键值，小元素享有高优先级)

举个例子，就像叠罗汉，体重大(优先级低、值大)的站在最下面，体重小的站在最上面(优先级高，值小)。 为了让堆稳固，我们每次都让最上面的参与者退出堆，也就是每次取出优先级最高的元素。

## 栈是什么

> 引自维基百科栈是计算机科学中一种特殊的串列形式的抽象资料型别，其特殊之处在于只能允许在链接串列或阵列的一端（称为堆叠顶端指标，英语：top）进行加入数据（英语：push）和输出数据（英语：pop）的运算。另外栈也可以用一维数组或连结串列的形式来完成。堆叠的另外一个相对的操作方式称为伫列。
> 由于堆叠数据结构只允许在一端进行操作，因而按照后进先出（LIFO, Last In First Out）的原理运作。

举个例子，一把54式手枪的子弹夹，你往里面装子弹，最先射击出来的子弹肯定是最后装进去的那一个。 这就是栈的结构，后进先出。

栈中的每个元素称为一个frame。而最上层元素称为top frame。栈只支持三个操作， pop, top, push。

- pop取出栈中最上层元素(8)，栈的最上层元素变为早先进入的元素(9)。
- top查看栈的最上层元素(8)。
- push将一个新的元素(5)放在栈的最上层。

栈不支持其他操作。如果想取出元素12, 必须进行3次pop操作。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E6%A0%88%E7%9A%84%E6%93%8D%E4%BD%9C.png)

## 内存分配中的栈和堆

**堆栈空间分配**

> 栈（操作系统）：由操作系统自动分配释放 ，存放函数的参数值，局部变量的值等。其操作方式类似于数据结构中的栈。
> 堆（操作系统）： 一般由程序员分配释放， 若程序员不释放，程序结束时可能由OS回收，分配方式倒是类似于链表。

**堆栈缓存方式**

> 栈使用的是一级缓存， 他们通常都是被调用时处于存储空间中，调用完毕立即释放。
> 堆则是存放在二级缓存中，生命周期由虚拟机的垃圾回收算法来决定（并不是一旦成为孤儿对象就能被回收）。所以调用这些对象的速度要相对来得低一些。

一般情况下程序存放在Rom（只读内存，比如硬盘）或Flash中，运行时需要拷到RAM（随机存储器RAM）中执行，RAM会分别存储不同的信息，如下图所示：

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%A0%86%E6%A0%88%E7%BC%93%E5%AD%98%E6%96%B9%E5%BC%8F.jpg)

内存中的栈区处于相对较高的地址以地址的增长方向为上的话，栈地址是向下增长的。

栈中分配局部变量空间，堆区是向上增长的用于分配程序员申请的内存空间。另外还有静态区是分配静态变量，全局变量空间的；只读区是分配常量和程序代码空间的；以及其他一些分区。

也就是说，在iOS中，我们的值类型是放在栈空间的，内存分配和回收不需要我们关系，系统会帮我处理。在堆空间的对象类型就要有程序员自己分配，自己释放了。

# 引用计数

## 引用计数是什么

> 引自维基百科引用计数是计算机编程语言中的一种内存管理技术，是指将资源（可以是对象、内存或磁盘空间等等）的被引用次数保存起来，当被引用次数变为零时就将其释放的过程。使用引用计数技术可以实现自动资源管理的目的。同时引用计数还可以指使用引用计数技术回收未使用资源的垃圾回收算法。
> 当创建一个对象的实例并在堆上申请内存时，对象的引用计数就为1，在其他对象中需要持有这个对象时，就需要把该对象的引用计数加1，需要释放一个对象时，就将该对象的引用计数减1，直至对象的引用计数为0，对象的内存会被立刻释放。

正常情况下，当一段代码需要访问某个对象时，该对象的引用的计数加1；当这段代码不再访问该对象时，该对象的引用计数减1，表示这段代码不再访问该对象；当对象的引用计数为0时，表明程序已经不再需要该对象，系统就会回收该对象所占用的内存。

- 当程序调用方法名以alloc、new、copy、mutableCopy开头的方法来创建对象时，该对象的引用计数加1。
- 程序调用对象的retain方法时，该对象的引用计数加1。
- 程序调用对象的release方法时，该对象的引用计数减1。

**NSObject 中提供了有关引用计数的如下方法：**

- retain：将该对象的引用计数器加1。
- release：将该对象的引用计数器减1。
- autorelease：不改变该对象的引用计数器的值，只是将对象添加到自动释放池中。
- retainCount：返回该对象的引用计数的值。

引用计数（Reference Count）是一个简单而有效的管理对象生命周期的方式。当我们创建一个新对象的时候，它的引用计数为 1，当有一个新的指针指向这个对象时，我们将其引用计数加 1，当某个指针不再指向这个对象是，我们将其引用计数减 1，当对象的引用计数变为 0 时，说明这个对象不再被任何指针指向了，这个时候我们就可以将对象销毁，回收内存。由于引用计数简单有效，除了 Objective-C 和 Swift 语言外，微软的 COM（Component Object Model ）、C++11（C++11 提供了基于引用计数的智能指针 share_prt）等语言也提供了基于引用计数的内存管理方式。

![引用计数](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%BC%95%E7%94%A8%E8%AE%A1%E6%95%B0.jpg)

为了更形象一些，我们再来看一段 Objective-C 的代码。新建一个工程，因为现在默认的工程都开启了自动的引用计数 ARC（Automatic Reference Count)，我们先修改工程设置，给 AppDelegate.m 加上 -fno-objc-arc 的编译参数（如下图所示），这个参数可以启用手工管理引用计数的模式。

![手动内存管理配置](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E6%89%8B%E5%8A%A8%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86%E9%85%8D%E7%BD%AE.png)

然后，我们在中输入如下代码，可以通过 Log 看到相应的引用计数的变化。


```
- (BOOL)application:(UIApplication *)application
       didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    NSObject *object = [[NSObject alloc] init];
    NSLog(@"Reference Count = %u", [object retainCount]);
    NSObject *another = [object retain];
    NSLog(@"Reference Count = %u", [object retainCount]);
    [another release];
    NSLog(@"Reference Count = %u", [object retainCount]);
    [object release];
    // 到这里时，object 的内存被释放了
    return YES;
}
```

运行结果：

```
Reference Count = 1
Reference Count = 2
Reference Count = 1

```

对 Linux 文件系统比较了解的同学可能发现，引用计数的这种管理方式类似于文件系统里面的硬链接。在 Linux 文件系统中，我们用 ln 命令可以创建一个硬链接（相当于我们这里的 retain)，当删除一个文件时（相当于我们这里的 release)，系统调用会检查文件的 link count 值，如果大于 1，则不会回收文件所占用的磁盘区域。直到最后一次删除前，系统发现 link count 值为 1，则系统才会执行直正的删除操作，把文件所占用的磁盘区域标记成未用。

## 引用计数内存管理的思考方式

看到“引用计数”这个名称，我们便会不自觉地联想到“某处有某物多少多少”而将注意力放到计数上。但其实，更加客观、正确的思考方式：

- 自己生成的对象，自己持有。
- 非自己生成的对象，自己也能持有。
- 不再需要自己持有的对象时释放。
- 非自己持有的对象无法释放。

引用计数式内存管理的思考方式仅此而已。按照这个思路，完全不必考虑引用计数。
上文出现了“生成”、“持有”、“释放”三个词。而在Objective-C内存管理中还要加上“废弃”一词。各个词标书的Objective-C方法如下表。

对象操作 | Objective-C方法
---|---
生成并持有对象 | alloc/new/copy/mutableCopy等方法
持有对象 | retain方法
释放对象 | release方法
废弃对象 | dealloc方法

这些有关Objective-C内存管理的方法，实际上不包括在该语言中，而是包含在Cocoa框架中用于macOS、iOS应用开发。Cocoa框架中Foundation框架类库的NSObject类担负内存管理的职责。Objective-C内存管理中的alloc/retain/release/dealloc方法分别指代NSObject类的alloc类方法、retain实例方法、release实例方法和dealloc实例方法。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-Cocoa%E6%A1%86%E6%9E%B6.jpg)

Cocoa框架、Foundation框架和NSObject类的关系

## 我们为什么需要引用计数?

从上面那个简单的例子中，我们还看不出来引用计数真正的用处。因为该对象的生命期只是在一个函数内，所以在真实的应用场景下，我们在函数内使用一个临时的对象，通常是不需要修改它的引用计数的，只需要在函数返回前将该对象销毁即可。

引用计数真正派上用场的场景是在面向对象的程序设计架构中，用于对象之间传递和共享数据。我们举一个具体的例子：

假如对象 A 生成了一个对象 M，需要调用对象 B 的某一个方法，将对象 M 作为参数传递过去。在没有引用计数的情况下，一般内存管理的原则是 “谁申请谁释放”，那么对象 A 就需要在对象 B 不再需要对象 M 的时候，将对象 M 销毁。但对象 B 可能只是临时用一下对象 M，也可能觉得对象 M 很重要，将它设置成自己的一个成员变量，那这种情况下，什么时候销毁对象 M 就成了一个难题。

![引用计数-传递对象1](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%BC%95%E7%94%A8%E8%AE%A1%E6%95%B0-%E4%BC%A0%E9%80%92%E5%AF%B9%E8%B1%A11.jpg)

对于这种情况，有一个暴力的做法，就是对象 A 在调用完对象 B 之后，马上就销毁参数对象 M，然后对象 B 需要将参数另外复制一份，生成另一个对象 M2，然后自己管理对象 M2 的生命期。但是这种做法有一个很大的问题，就是它带来了更多的内存申请、复制、释放的工作。本来一个可以复用的对象，因为不方便管理它的生命期，就简单的把它销毁，又重新构造一份一样的，实在太影响性能。如下图所示：

![引用计数-传递对象2](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%BC%95%E7%94%A8%E8%AE%A1%E6%95%B0-%E4%BC%A0%E9%80%92%E5%AF%B9%E8%B1%A12.jpg)

我们另外还有一种办法，就是对象 A 在构造完对象 M 之后，始终不销毁对象 M，由对象 B 来完成对象 M 的销毁工作。如果对象 B 需要长时间使用对象 M，它就不销毁它，如果只是临时用一下，则可以用完后马上销毁。这种做法看似很好地解决了对象复制的问题，但是它强烈依赖于 AB 两个对象的配合，代码维护者需要明确地记住这种编程约定。而且，由于对象 M 的申请是在对象 A 中，释放在对象 B 中，使得它的内存管理代码分散在不同对象中，管理起来也非常费劲。如果这个时候情况再复杂一些，例如对象 B 需要再向对象 C 传递对象 M，那么这个对象在对象 C 中又不能让对象 C 管理。所以这种方式带来的复杂性更大，更不可取。

![引用计数-传递对象3](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%BC%95%E7%94%A8%E8%AE%A1%E6%95%B0-%E4%BC%A0%E9%80%92%E5%AF%B9%E8%B1%A13.jpg)


所以引用计数很好的解决了这个问题，在参数 M 的传递过程中，哪些对象需要长时间使用这个对象，就把它的引用计数加 1，使用完了之后再把引用计数减 1。所有对象都遵守这个规则的话，对象的生命期管理就可以完全交给引用计数了。我们也可以很方便地享受到共享对象带来的好处。


# MRC

MRC（Manual Retain Count）手动引用计数，顾名思义就是程序员需要自己确保对象的retain与release的成对出现。对象创建好之后引用计数为1，哪天引用计数为0了，对象就会被销毁内存将被回收。

用alloc，allocWithZone，copy，copyWithZone，mutableCopy，mutableCopyWithZone方法创建的对象，会retain持有该对象。

也可以用retain方法持有别人创建的对象。

当不需要这些对象时，可以用release，autorelease来释放内存。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-MRC1.png)

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-MRC2.png)

引用计数也会出现两个对象直接或间接地互相持有对方，甚至自己持有自己的引用，导致Retain Cycle。解决方式有两种：

对于类属性property：声明时设为assign，要释放时手动置为nil

```
@property (nonatomic, assign) NSObject *parent;

```

对于block：用__block修饰符来修饰使用到的变量


顾名思义，MRC就是调用Objective-C的方法(alloc/new/copy/mutableCopy/retain/release等)实现引用计数的增加和减少。

下面通过Objective-C的方法实现内存管理的思考方式。

## 自己生成的对象，自己持有

使用以下名称开头的方法名意味着自己生成的对象只有自己持有：

- alloc
- new
- copy
- mutableCopy

### alloc的实现

```
// 自己生成并持有对象
id obj = [[NSObject alloc] init];
```

使用NSObject类的alloc方法就能自己生成并持有对象。指向生成并持有对象的指针被赋给变量obj。

### new的实现

```
// 自己生成并持有对象
id obj = [NSObject new];
```
[NSObject new]与[[NSObject alloc] init]是完全一致的。

### copy的实现

copy方法利用基于NSCopying方法约定，由各类实现的copyWithZone:方法生成并持有对象的副本。

```
#import "ViewController.h"

@interface Person: NSObject<NSCopying>

@property (nonatomic, strong) NSString *name;

@end

@implementation Person

- (id)copyWithZone:(NSZone *)zone {
    Person *obj = [[[self class] allocWithZone:zone] init];
    obj.name = self.name;
    return obj;
}

@end

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    //alloc生成并持有对象
    Person *p = [[Person alloc] init];
    p.name = @"testname";

    //copy生成并持有对象
    id obj = [p copy];

    //打印对象
    NSLog(@"p对象%@", p);
    NSLog(@"obj对象%@", obj);
}

@end

```

```
打印结果：
2018-03-28 23:01:32.321661+0800 ocram[4466:1696414] p对象<Person: 0x1c0003320>
2018-03-28 23:01:32.321778+0800 ocram[4466:1696414] obj对象<Person: 0x1c0003370>

```

从打印可以看到obj是p对象的副本。两者的引用计数都是1。

> 说明：在- (id)copyWithZone:(NSZone *)zone方法中，一定要通过[self class]方法返回的对象调用allocWithZone:方法。因为指针可能实际指向的是Person的子类。这种情况下，通过调用[self class]，就可以返回正确的类的类型对象。

### mutableCopy的实现

与copy方法类似，mutableCopy方法利用基于NSMutableCopying方法约定，由各类实现的mutableCopyWithZone:方法生成并持有对象的副本。

```
#import "ViewController.h"

@interface Person: NSObject<NSMutableCopying>

@property (nonatomic, strong) NSString *name;

@end

@implementation Person

- (id)mutableCopyWithZone:(NSZone *)zone {
    Person *obj = [[[self class] allocWithZone:zone] init];
    obj.name = self.name;
    return obj;
}

@end

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    //alloc生成并持有对象
    Person *p = [[Person alloc] init];
    p.name = @"testname";

    //copy生成并持有对象
    id obj = [p mutableCopy];

    //打印对象
    NSLog(@"p对象%@", p);
    NSLog(@"obj对象%@", obj);
}

@end
```

> 打印结果：
> 2018-03-28 23:08:17.382538+0800 ocram[4476:1699096] p对象<Person: 0x1c4003c20>
> 2018-03-28 23:08:17.382592+0800 ocram[4476:1699096] obj对象<Person: 0x1c4003d70>

从打印可以看到obj是p对象的副本。两者的引用计数都是1。

copy和mutableCopy的区别在于，copy方法生成不可变更的对象，而mutableCopy方法生成可变更的对象。

## 浅拷贝和深拷贝

既然讲到copy和mutableCopy，那就要谈一下深拷贝和浅拷贝的概念和实践。

### 什么是浅拷贝、深拷贝？

> 简单理解就是，浅拷贝是拷贝了指向对象的指针， 深拷贝不但拷贝了对象的指针，还在系统中再分配一块内存，存放拷贝对象的内容。

- 浅拷贝：浅拷贝就是对内存地址的复制，让目标对象指针和源对象指向同一片内存空间，当内存销毁的时候，指向这片内存的几个指针需要重新定义才可以使用，要不然会成为野指针。浅拷贝就是拷贝指向原来对象的指针，使原对象的引用计数+1，可以理解为创建了一个指向原对象的新指针而已，并没有创建一个全新的对象。
- 深拷贝：深拷贝是指拷贝对象的具体内容，而内存地址是自主分配的，拷贝结束之后，两个对象虽然存的值是相同的，但是内存地址不一样，两个对象也互不影响，互不干涉。深拷贝就是拷贝出和原来仅仅是值一样，但是内存地址完全不一样的新的对象，创建后和原对象没有任何关系。

**浅拷贝就是指针拷贝，深拷贝就是内容拷贝。本质区别在于：**
- 是否开启新的内存地址
- 是否影响内存地址的引用计数

#### 如何判断浅拷贝、深拷贝？

> 深浅拷贝取决于拷贝后的对象的是不是和被拷贝对象的地址相同，如果不同，则产生了新的对象，则执行的是深拷贝，如果相同，则只是指针拷贝，相当于retain一次原对象, 执行的是浅拷贝。
>

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E6%B7%B1%E6%B5%85%E6%8B%B7%E8%B4%9D.png)

**深拷贝和浅拷贝的判断要注意两点：**

- 源对象类型是否是可变的
- 执行的拷贝是copy还是mutableCopy

### 浅拷贝深拷贝的实现

- NSArray调用copy方法，浅拷贝

```
id obj = [NSArray array];
id obj1 = [obj copy];

NSLog(@"obj是%p", obj);
NSLog(@"obj1是%p", obj1);
```

> 打印结果：
> 2018-03-29 20:48:56.087197+0800 ocram[5261:2021415] obj是0x1c0003920
> 2018-03-29 20:48:56.087250+0800 ocram[5261:2021415] obj1是0x1c0003920

指针一样obj是浅拷贝。

- NSArray调用mutableCopy方法，深拷贝

```
id obj = [NSArray array];
id obj1 = [obj mutableCopy];

NSLog(@"obj是%p", obj);
NSLog(@"obj1是%p", obj1);
```

> 打印结果：
> 2018-03-29 20:42:16.508134+0800 ocram[5244:2018710] obj是0x1c00027d0
> 2018-03-29 20:42:16.508181+0800 ocram[5244:2018710] obj1是0x1c0453bf0

指针不一样obj是深拷贝。

- NSMutableArray调用copy方法，深拷贝

```
id obj = [NSMutableArray array];
id obj1 = [obj copy];

NSLog(@"obj是%p", obj);
NSLog(@"obj1是%p", obj1);
```

> 打印结果：
> 2018-03-29 20:50:36.936054+0800 ocram[5265:2022249] obj是0x1c0443f90
> 2018-03-29 20:50:36.936097+0800 ocram[5265:2022249] obj1是0x1c0018580

指针不一样obj是深拷贝。

- 深拷贝的数组里面的元素依然是浅拷贝

```
id obj = [NSMutableArray arrayWithObject:@"test"];
id obj1 = [obj mutableCopy];

NSLog(@"obj是%p", obj);
NSLog(@"obj内容是%p", obj[0]);
NSLog(@"obj1是%p", obj1);
NSLog(@"obj1内容是%p", obj1[0]);
```

> 打印结果：
> 2018-03-29 20:55:18.196597+0800 ocram[5279:2025743] obj是0x1c0255120
> 2018-03-29 20:55:18.196647+0800 ocram[5279:2025743] obj内容是0x1c02551e0
> 2018-03-29 20:55:18.196665+0800 ocram[5279:2025743] obj1是0x1c0255210
> 2018-03-29 20:55:18.196682+0800 ocram[5279:2025743] obj1内容是0x1c02551e0

可以看到obj和obj1虽然指针是不一样的(深拷贝)，但是他们的元素的指针是一样的，所以数组里的元素依然是浅拷贝。

### 其他实现

使用上述使用一下名称开头的方法，下面名称也意味着自己生成并持有对象。

- allocMyObject
- newThatObject
- copyThis
- mutableCopyYourObject

使用驼峰拼写法来命名。

```
#import "ViewController.h"

@interface Person: NSObject

@property (nonatomic, strong) NSString *name;

+ (id)allocObject;

@end

@implementation Person

+ (id)allocObject {
    //自己生成并持有对象
    id obj = [[Person alloc] init];

    return obj;
}

@end

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    //取得非自己生成并持有的对象
    Person *p = [Person allocObject];
    p.name = @"testname";

    NSLog(@"p对象%@", p);
}

@end
```
> 打印结果： 2018-03-28 23:33:37.044327+0800 ocram[4500:1706677] p对象<Person: 0x1c0013770>

allocObject名称符合上面的命名规则，因此它与用alloc方法生成并持有对象的情况完全相同，所以使用allocObject方法也意味着“自己生成并持有对象”。

## 非自己生成的对象，自己也能持有

```
//非自己生成的对象，暂时没有持有
id obj = [NSMutableArray array];

//通过retain持有对象
[obj retain];
```

上述代码中NSMutableArray通过类方法array生成了一个对象赋给变量obj，但变量obj自己并不持有该对象。使用retain方法可以持有对象。

## 不再需要自己持有的对象时释放

自己持有的对象，一旦不再需要，持有者有义务释放该对象。释放使用release方法。

## 自己生成并持有对象的释放

```
// 自己生成并持有对象
id obj = [[NSObject alloc] init];

//释放对象
[obj release];
```

## 非自己生成的对象本身的释放

像调用[NSMutableArray array]方法使取得的对象存在，但自己并不持有对象，是如何实现的呢？

```
+ (id)array {
    //生成并持有对象
    id obj = [[NSMutableArray alloc] init];

    //使用autorelease不持有对象
    [obj autorelease];

    //返回对象
    return obj;
}
```

上例中，我们使用了autorelease方法。用该方法，可以使取得的对象存在，但自己不持有对象。autorelease提供这样的功能，使对象在超出指定的生存范围时能够自动并正确的释放(调用release方法)。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-autorelease.png)

在后面会对autorelease做更为详细的介绍。使用NSMutableArray类的array类方法等可以取得谁都不持有的对象，这些方法都是通过autorelease实现的。根据上文的命名规则，这些用来取得谁都不持有的对象的方法名不能以alloc/new/copy/mutableCopy开头，这点需要注意。

## 非自己持有的对象无法释放

对于用alloc/new/copy/mutableCopy方法生成并持有的对象，或是用retain方法持有的对象，由于持有者是自己，所以在不需要该对象时需要将其释放。而由此以外所得到的对象绝对不能释放。倘若在程序中释放了非自己所持有的对象就会造成崩溃。

```
// 自己生成并持有对象
id obj = [[NSObject alloc] init];

//释放对象
[obj release];

//再次释放已经非自己持有的对象，应用程序崩溃
[obj release];
```

释放了非自己持有的对象，肯定会导致应用崩溃。因此绝对不要去释放非自己持有的对象。


# AutoRelease

AutoRelease这个名字貌似有点歧义，感觉是将手动释放内存升级到自动释放内存。其实AutoRelease是为了解决延迟销毁对象的问题。

例如下面代码中，既不能在return前也不能在return后释放对象。

```
-(NSObject*)object {
    NSObject *o = [[NSObject alloc] init];
    // [o release];  // 这行代码究竟应该在return前执行还是return后执行呢？
    return o;
}
```
AutoRelease就是为了解决上述问题，可以延迟释放对象。

程序员可以手动调用autorelease方法，也可以用工厂方法的返回值（工厂方法默认使用了autorelease）。

```
// 和普通用[alloc init]方法创建的对象不同，工厂方法返回的对象默认使用了autorelease
+ (id)typeRemainderOfMethodName
+ (id)dataWithContentsOfURL:(NSURL *)url;
```

```
NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];  // 需要在AutoreleasePool里使用autorelease方法
...
NSObject *obj = [[NSObject alloc] init] autorelease];  // 方式一：手动调用autorelease方法
...
NSString *string;
char *cString = "Hello World";
string = [NSString stringWithUTF8String:cstring];  // 方式二：工厂方法的返回值会自动调用autorelease方法
...
[pool release];
```

其实程序员很少自己去手动创建AutoreleasePool，因为每个线程（包括主线程）都会拥有一个专属的NSRunLoop对象，并且会在有需要的时候自动创建。NSRunLoop对象的每个eventloop开始前，系统会自动创建一个AutoreleasePool，并在eventloop结束时drain。每一个线程都会维护自己的AutoreleasePool堆栈，即AutoreleasePool是与线程紧密相关的，每一个AutoreleasePool只对应一个线程。

善用AutoRelease可以解决一些内存峰值问题，例如下面循环结束前是不会自动触发autorelease的，导致循环次数很多时，内存占用率高：

```
// 会有内存峰值问题
for(int i=0; i<100; i++) {
    NSError *error;
    NSString *fileContents = [NSString stringWithContentsOfURL:urlArray[i]
                                      encoding:NSUTF8StringEncoding error:&error];
}

// 解决方式：
for(int i=0; i<100; i++) {
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];  // 每次循环都开启AutoreleasePool
    NSError *error;
    NSString *fileContents = [NSString stringWithContentsOfURL:urlArray[i]
                                      encoding:NSUTF8StringEncoding error:&error];
    [pool release]; // 每次循环结束就关闭AutoreleasePool
}
```

说到Objective-C内存管理，就不能不提autorelease。 顾名思义，autorelease就是自动释放。这看上去很像ARC，单实际上它更类似于C语言中自动变量（局部变量）的特性。

在C语言中，程序程序执行时，若局部变量超出其作用域，该局部变量将被自动废弃。

```
{
    int a;
}

//因为超出变量作用域，代码执行到这里，自动变量`a`被废弃，不可再访问。
```

autorelease会像C语言的局部变量那样来对待对象实例。当其超出作用域时，对象实例的release实例方法被调用。另外，同C语言的局部变量不同的是，编程人员可以设置变量的作用域。

autorelease的具体使用方法如下：

- 生成并持有NSAutoreleasePool对象。
- 调用已分配对象的autorelease实例方法。
- 废弃NSAutoreleasePool对象。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-NSAutoreleasePool.png)

```
NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];

id obj = [[NSObject alloc] init];

[obj autorelease];

[pool drain];
```

上述代码中最后一行的[pool drain]等同于[obj release]。

## autorelease实现

调用NSObject类的autorelease实例方法。


```
[obj autorelease];


```

调用autorelease方法的内部实现


```
- (id) autorelease {
    [NSAutoreleasePool addObject: self];
}


```

autorelease实例方法的本质就是调用NSAutoreleasePool对象的addObject类方法。

## autorelease注意

autorelease是NSObject的实例方法，NSAutoreleasePool也是继承NSObject的类。那能不能调用autorelease呢？


```
NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];

[pool release];


```

运行结果发生崩溃。通常在使用Objective-C，也就是Foundation框架时，无论调用哪一个对象的autorelease实例方法，实现上是调用的都是NSObject类的autorelease实例方法。但是对于NSAutoreleasePool类，autorelease实例方法已被该类重载，因此运行时就会出错。


# ARC

上面讲了“引用计数内存管理的思考方式”的本质部分在ARC中并没有改变。就像“自动引用计数”这个名称表示的那样，ARC只是自动地帮助我们处理“引用计数”的相关部分。


编译器在编译时会帮我们自动插入，包括 retain、release、copy、autorelease、autoreleasepool



## ARC有效的代码实现

### 所有权修饰符

Objective-C编程中为了处理对象，可将变量类型定义为id类型或各种对象类型。 ARC中，id类型和对象类其类型必须附加所有权修饰符。

- __strong修饰符
- __weak修饰符
- __unsafe_unretained修饰符
- __autoreleasing修饰符

### __strong修饰符

__strong修饰符是id类型和对象类型默认的所有权修饰符。也就是说，不写修饰符的话，默认对象前面被附加了__strong所有权修饰符。

```
id obj = [[NSObject alloc] init];
等同于
id __strong obj = [[NSObject alloc] init];
```

__strong修饰符的变量obj在超出其变量作用域时，即在该变量被废弃时，会释放其被赋予的对象。 __strong修饰符表示对对象的“强引用”。持有强引用的变量在超出其作用域时被废弃，随着强引用的失效，引用的对象会随之释放。


当然，__strong修饰符也可以用在Objective-C类成员变量和方法参数上。

```
@interface Test: NSObject
{
    id __strong obj_;
}

- (void)setObject:(id __strong)obj;

@end

@implementation Test

- (instancetype)init {
    self = [super init];
    return self;
}

- (void)setObject:(id __strong)obj {
    obj_ = obj
}

@end
```

无需额外的工作便可以使用于类成员变量和方法参数中。__strong修饰符和后面要讲的__weak修饰符和__autoreleasing修饰符一起，可以保证将附有这些修饰符的自动变量初始化为nil。

正如苹果宣称的那样，通过__strong修饰符再键入retain和release，完美地满足了“引用计数式内存管理的思考方式”。

### __weak修饰符

通过__strong修饰符并不能完美的进行内存管理，这里会发生“循环引用”的问题。

```
{
      id test0 = [[Test alloc] init];
      id test1 = [[Test alloc] init];
      [test0 setObject:test1];
      [test1 setObject:test0];
}
```

可以看到test0和tets1互相持有对方，谁也释放不了谁。

循环引用容易发生内存泄露。所谓内存泄露就是应当废弃的对象在超出其生命周期后继续存在。

__weak修饰符可以避免循环引用，与__strong修饰符相反，提供弱引用。弱引用不能持有对象实例，所以在超出其变量作用域时，对象即被释放。像下面这样将之前的代码修改，就可以避免循环引用了。

```
@interface Test: NSObject
{
    id __weak obj_;
}

- (void)setObject:(id __strong)obj;
```

使用__weak修饰符还有另外一个优点。在持有某对象的弱引用时，若该对象被废弃，则此弱引用将自动失效且处于nil赋值的状态(空弱引用)。

```
id __weak obj1 = nil;
{
    id __strong obj0 = [[NSObject alloc] init];

    obj1 = obj0;

    NSLog(@"%@", obj1);
}

NSLog(@"%@", obj1);
```

> 打印结果：
> 2018-03-30 21:47:50.603814+0800 ocram[51624:22048320] <NSObject: 0x60400001ac10>
> 2018-03-30 21:47:50.604038+0800 ocram[51624:22048320] (null)

可以看到因为obj0超出作用域就被释放了，弱引用也被至为nil状态。

### __unsafe_unretained修饰符

__unsafe_unretained修饰符是不安全的修饰符，尽管ARC式的内存管理是编译器的工作，但附有__unsafe_unretained修饰符的变量不属于编译器的内存管理对象。__unsafe_unretained和__weak一样不能持有对象。

```
id __unsafe_unretained obj1 = nil;
{
    id __strong obj0 = [[NSObject alloc] init];

    obj1 = obj0;

    NSLog(@"%@", obj1);
}

NSLog(@"%@", obj1);
```

```
打印结果： 2018-03-30 21:58:28.033250+0800 ocram[51804:22062885] <NSObject: 0x604000018e80>
```

可以看到最后一个打印没有打印出来，程序崩溃了。这是因为超出了作用域，obj1已经变成了一个野指针，然后我们去操作野指针的时候会发生崩溃。

所以在使用__unsafe_unretained修饰符时，赋值给__strong修饰符的变量时有必要确保被赋值的对象确实存在。

### __autoreleasing修饰符

在ARC中，我也可以使用autorelease功能。指定“@autoreleasepool块”来代替“NSAutoreleasePool类对象生成、持有以及废弃这一范围，使用附有__autoreleasing修饰符的变量替代autorelease方法。

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-autoreleasing%E4%BF%AE%E9%A5%B0%E7%AC%A6.jpg)

其实我们不用显示的附加 __autoreleasing修饰符，这是由于编译器会检查方法名是否以alloc/new/copy/mutableCopy开始，如果不是则自动将返回值的对象注册到autoreleasepool。

有时候__autoreleasing修饰符要和__weak修饰符配合使用。

```
id __weak obj1 = obj0;

id __autoreleasing tmp = obj1;
```

为什么访问附有__weak修饰符的变量时必须访问注册到autoreleasepool的对象呢？这是因为__weak修饰符只持有对象的弱引用，而在访问引用对象的过程中，该对象有可能被废弃。如果把访问的对象注册到autoreleasepool中，那么在@autoreleasepool块结束之前都能确保该对象存在。

### 属性与所有权修饰符的对应关系

![](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E5%B1%9E%E6%80%A7%E4%BF%AE%E9%A5%B0%E7%AC%A6.png)

以上各种属性赋值给指定的属性中就相当于赋值给附加各属性对应的所有权修饰符的变量中。只有copy不是简单的赋值，它赋值的是通过NSCopying接口的copyWithZone：方法复制赋值源所生成的对象。

## ARC规则

在ARC有效的情况下编译源代码，必须遵守一定的规则。

不能使用retain/release/retainCount/autorelease

ARC有效时，实现retain/release/retainCount/autorelease会引起编译错误。代码会标红，编译不通过。

不能使用NSAllocateObject/NSDeallocateObject

alloc,new,copy,mutableCopy,init
以init开始的方法的规则要比alloc,new,copy,mutableCopy更严格。该方法必须是实例方法，并且要返回对象。返回的对象应为id类型或方法声明类的对象类型，抑或是该类的超类型或子类型。该返回对象并不注册到autoreleasepool上。基本上只是对alloc方法返回值的对象进行初始化处理并返回该对象。

```
//符合命名规则
- (id) initWithObject;

//不符合命名规则
- (void) initThisObject;
```

不要显式调用dealloc

当对象的引用计数为0，所有者不持有该对象时，该对象会被废弃，同时调用对象的dealloc方法。ARC会自动对此进行处理，因此不必书写[super dealloc]。

使用@autoreleasepool块替代NSAutoreleasePool

不能使用区域(NSZone)

对象型变量不能作为C语言结构体（struct、union）的成员

C语言结构体（struct、union）的成员中，如果存在Objective-C对象型变量，便会引起编译错误。

```
struct Data {
    NSMutableArray *array;
};
```

```
显示警告: ARC forbids Objective-C objects in struct
```

在C语言的规约上没有方法来管理结构体成员的生命周期。因为ARC把内存管理的工资分配给编译器，所以编译器必须能够知道并管理对象的生命周期。例如C语言的局部变量可使用该变量的作用域管理对象。但是对于C语言的结构体成员来说，这在标准上就是不可实现的。

要把对象类型添加到结构体成员中，可以强制转换为void *或是附加__unsafe_unretained修饰符。

```
struct Data {
    NSMutableArray __unsafe_unretained *array;
};
```

__unsafe_unretained修饰符的变量不属于编译器的内存管理对象。如果管理时不注意赋值对象的所有者，便可能遭遇内存泄露或者程序崩溃。

显示转换id和void *

在MRC时，将id变量强制转换void *变量是可以的。

```
id obj = [[NSObject alloc] init];

void *p = obj;

id o = p;

[o release];
```

但是在ARC时就会编译报错，id型或对象型变量赋值给void *或者逆向赋值时都需要进行特定的转换。如果只想单纯的赋值，则可以使用“__bridge转换”

__bridge转换中还有另外两种转换，分部是“__bridge_retained”和“__bridge_transfer转换”
__bridge_retained转换与retain类似，__bridge_transfer转换与release类似。

```
void *p = (__bridge_retained void *)[[NSObject alloc] init];
NSLog(@"class = %@", [(__bridge id)p class]);
(void)(__bridge_transfer id)p;
```

##  ARC内存的泄露和检测

### ARC内存泄露常见场景

#### 对象型变量作为C语言结构体（struct、union）的成员

```
struct Data {
    NSMutableArray __unsafe_unretained *array;
};
```

__unsafe_unretained修饰符的变量不属于编译器的内存管理对象。如果管理时不注意赋值对象的所有者，便可能遭遇内存泄露或者程序崩溃。

MRC需要程序员手动调用retain，release，autorelease，导致内存管理一直是开发的噩梦。

iOS 4.3版引入了ARC，它是Objective-C编译器的特性，而不是运行时特性或者垃圾回收机制。

ARC的内存管理机制与MRC手动机制差不多，只是不再需要手动调用retain，release，autorelease了，编译器会在在适当位置插入retain，release，autorelease。

但ARC仍旧有野指针问题，所以iOS 5版支持了week关键字，用week修饰的对象，在引用的对象被销毁后会自动置为nil。

所以现在的内存管理是：编译时ARC+运行时week搭配使用。

ARC里得到对象的方式：alloc，new，copy，mutableCopy，init

ARC里对象修饰符有四种：__strong，__weak，__unsafe_unretained，__autoreleasing

__strong：ARC里用strong强引来取代retain，持有对象，将对象引用计数+1，同时编译器会自动在不需要它的时候插入release代码。而且__strong是默认修饰符，所以写代码时不用显式地加上__strong修饰符：

```
// 声明变量时，ARC和MRC代码一样都是（ARC里 __strong 是默认修饰符，不用显式写）
id obj = [[NSObject alloc] init];

// ARC编译器会默认加上 __strong 的修饰符：
id __strong obj = [[NSObject alloc] init];

// 作用域里的ARC和MRC的代码不一样，ARC的代码：
{
  id __strong obj = [[NSObject alloc] init];
  // [obj release];  // ARC里不需要这行了，编译器会在作用域结束时自动插入这行代码
}

// 作用域里的MRC的代码
{
  idobj = [[NSObject alloc] init];
  [obj release];
}
```

__weak：不持有对象，所引用的对象计数不会加1。所引用的对象被销毁时会自动置为nil。常用于block, delegate, NSTimer，以解决循环引用带来的内存泄漏问题。

下面的写法是错误的：

```
// 会报错，不能将可以retain的对象赋值给weak修饰的变量
id __weak obj = [[xxx alloc] init];
```

weak与assign很像，区别是：weak不会产生野指针问题。因为weak修饰的对象释放后（引用计数器值为0），指针会自动被置nil，之后再向该对象发消息也不会崩溃，所以weak是安全的。assign通常用于修饰基础数据类型，此时与weak一样是安全的。assign也可以修饰对象，与weak一样不持有对象，所引用的对象计数不会加1。但会产生野指针问题，修饰的对象释放后，指针不会自动被置空，此时向对象发消息会崩溃，所以assign修饰对象是不安全的。

weak安全的原理，即当对象被销毁后，自动置为nil的原理：Runtime维护了一个weak表（其实就是个哈希表，Key是所指对象的地址，Value是Weak指针的地址的数组），用于存储指向某个对象的所有weak指针。当对象被回收的时候，会将所有Weak指针的值设为nil。（参照objc-weak.m）

__unsafe_unretained：不持有对象，所引用的对象被销毁时会自动置为nil。平时不常用，和__weak相似，__weak出现前是代替__weak的，即在iOS 4.3~5之间用于代替__weak去修饰对象的属性的。但有一种情况，在在C结构体里使用到Objective-C对象时，只能用它来修饰。

__autoreleasing：表明传引用的参数(id *)在返回时是autorelease的，效果同MRC下调用autorelease方法，即被修饰的对象会被加入autorelease pool。

```
@autoreleasepool {
    NSError *error;
    NSString *fileContents = [NSString stringWithContentsOfURL:url
                                       encoding:NSUTF8StringEncoding error:&error];  // 参数是autorelease的
    ...
}
```

ARC下同样会有Retain Cycle的问题，解决方法见下面。

# 循环引用

多个对象相互之间有strong引用，不能释放让系统回收。避免循环引用的方式：

1.类属性：将strong改为weak引用

2.delegate循环引用：一般在声明delegate的时候都要使用弱引用weak，或者assign。（weak和assign的区别见上面，MRC的话只能用assign，在ARC的情况下最好使用weak。）

3.NSTimer循环引用：在控制器内，创建NSTimer作为其属性，由于定时器创建后也会强引用该控制器对象，这样该对象和定时器就相互循环引用了。需要我们手动断开循环引用：如果是不重复定时器，在回调方法里将定时器invalidate并置为nil。如果是重复定时器，在合适的位置将其invalidate并置为nil

4.block循环引用：block会持有block中的对象，如果此时block中的对象又持有了该block，则会造成循环引用。解决方式用__weak或@weakify配合@strongify来修饰：

```
// 错误代码，会有Retain Cycle的问题
@property (nonatomic, copy) void(^myBlock)(void);

- (void)test
{
    self.myBlock = ^{
        [self doSomething];  // self持有block的指针，block里又使用了self，形成了Retain Cycle
    };
}

// 解决方式1
@property (nonatomic, copy) void(^myBlock)(void);

- (void)test
{
    @weakify(self);
    self.myBlock = ^{
        @strongify(self);
        [self doSomething];
    };
}

// 解决方式2
@property (nonatomic, copy) void(^myBlock)(void);

- (void)test
{
    __weak typeof(self) weakSelf = self;
    self.myBlock = ^{
        [weakSelf doSomething];
    };
}
```

## 循环引用常见有三种现象：

- 两个对象互相持有对象，这个可以设置弱引用解决。

```
@interface Test: NSObject
{
    id __weak obj_;
}

- (void)setObject:(id __strong)obj;
```

- block持有self对象，这个要在block块外面和里面设置弱引用和强引用。

```
__weak __typeof(self) wself = self;
obj.block = ^{
    __strong __typeof(wself) sself = wself;

    [sself updateSomeThing];
}
```

- NSTimer的target持有self

NSTimer会造成循环引用，timer会强引用target即self，一般self又会持有timer作为属性，这样就造成了循环引用。
那么，如果timer只作为局部变量，不把timer作为属性呢？同样释放不了，因为在加入runloop的操作中，timer被强引用。而timer作为局部变量，是无法执行invalidate的，所以在timer被invalidate之前，self也就不会被释放。

## 单例属性不释放

严格来说这个不算是内存泄露，主要就是我们在单例里面设置一个对象的属性，因为单例是不会释放的，所以单例会有一直持有这个对象的引用。

```
[Instanse shared].obj = self;
```

可以看到单例持有了当前对象self，这个self就不会释放了。


# 关键字总结

上面关于关键字的说明有点零散，总结一下：

strong：指向并持有该对象，引用计数会加1。引用计数为0销毁，可以通过将变量强制赋值nil来进行销毁。

weak：指向但是并不持有该对象，引用计数不会加1。在Runtime中对该属性进行了相关操作，无需处理，可以自动销毁

assign：assign主要用于修饰基本数据类型，例如NSInteger，CGFloat，存储在栈中，内存不用程序员管理

copy：和strong类似，多用于修饰有可变类型的不可变对象上NSString，NSArray，NSDictionary上。例如

```
@property(nonatomic, strong) NSString *strongStr;
@property(nonatomic, copy) NSString *copyyStr;

// 当字符串是NSString时，由于是不可变字符串，所以，不管使用strong还是copy修饰，都是指向原来的对象，copy操作只是做了一次浅拷贝。
// 当字符串是NSMutableString时，strong只是将源字符串的引用计数加1，而copy则是对原字符串做了次深拷贝，从而生成了一个新的对象，并且copy的对象指向这个新对象。
// 即：如果字符串是NSMutableString，使用strong只会增加引用计数。但是copy会执行一次深拷贝，会造成不必要的内存浪费。而如果字符串是NSString时，strong和copy效果一样，就不会有这个问题。
// 但通常我们声明NSString时，也不希望它改变，所以建议使用copy，这样可以避免NSMutableString带来的错误。
```

__unsafe_unretain：类似于weak，但是当对象被释放后，指针本身并不会自动销毁，这也就造成了野指针，访问被释放的地址就会Crash，所以说它是不安全的。但__weak在指向的内存销毁后，可以将指针变量置为nil，这样更加安全。

atomic：这个属性是为了保证在多线程的情况下，编译器会自动生成一些互斥加锁的代码，避免该变量的读写不同步的问题。注意：atomic可以保证setter和getter存取的线程安全，但并不保证整个对象是线程安全的。例如，声明一个NSMutableArray的原子属性array，此时self.array和self.array = otherArray都是线程安全的。但是，使用[self.array objectAtIndex:index]就不是线程安全的，需要用锁来保证线程安全性。

nonatomic：如果该对象无需考虑多线程的情况，这个属性会让编译器少生成一些互斥代码，可以提高效率。但在多线程设置属性时非常容易产生crash，因为nonatomic的属性被赋值后会将oldValue释放，如果两个线程同时设置nonatomic的属性后，会释放两次oldValue导致crash。所以多线程时属性要用atomic修饰。


# ARC 下的内存管理问题

ARC 能够解决 iOS 开发中 90% 的内存管理问题，但是另外还有 10% 内存管理，是需要开发者自己处理的，这主要就是与底层 Core Foundation 对象交互的那部分，底层的 Core Foundation 对象由于不在 ARC 的管理下，所以需要自己维护这些对象的引用计数。

对于 ARC 盲目依赖的 iOS 新人们，由于不知道引用计数，他们的问题主要体现在：

1. 过度使用 block 之后，无法解决循环引用问题。
2. 遇到底层 Core Foundation 对象，需要自己手工管理它们的引用计数时，显得一筹莫展。


## 循环引用（Reference Cycle）问题

引用计数这种管理内存的方式虽然很简单，但是有一个比较大的瑕疵，即它不能很好的解决循环引用问题。如下图所示：对象 A 和对象 B，相互引用了对方作为自己的成员变量，只有当自己销毁时，才会将成员变量的引用计数减 1。因为对象 A 的销毁依赖于对象 B 销毁，而对象 B 的销毁与依赖于对象 A 的销毁，这样就造成了我们称之为循环引用（Reference Cycle）的问题，这两个对象即使在外界已经没有任何指针能够访问到它们了，它们也无法被释放。

![内存管理-循环引用1](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A81.jpg)

不止两对象存在循环引用问题，多个对象依次持有对方，形式一个环状，也可以造成循环引用问题，而且在真实编程环境中，环越大就越难被发现。下图是 4 个对象形成的循环引用问题。

![内存管理-循环引用2](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A82.png)

## 主动断开循环引用

解决循环引用问题主要有两个办法，第一个办法是我明确知道这里会存在循环引用，在合理的位置主动断开环中的一个引用，使得对象得以回收。如下图所示：

![内存管理-循环引用3](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A83.png)

主动断开循环引用这种方式常见于各种与 block 相关的代码逻辑中。例如在开源的 [YTKNetwork](https://github.com/yuantiku/YTKNetwork) 网络库中，网络请求的回调 block 是被持有的，但是如果这个 block 中又存在对于 View Controller 的引用，就很容易产生从循环引用，因为：

- Controller 持有了网络请求对象
- 网络请求对象持有了回调的 block
- 回调的 block 里面使用了 `self`，所以持有了 Controller

解决办法就是，在网络请求结束后，网络请求对象执行完 block 之后，主动释放对于 block 的持有，以便打破循环引用。相关的代码见：

```
// https://github.com/yuantiku/YTKNetwork/blob/master/YTKNetwork/YTKBaseRequest.m
// 第 147 行：
- (void)clearCompletionBlock {
    // 主动释放掉对于 block 的引用
    self.successCompletionBlock = nil;
    self.failureCompletionBlock = nil;
}
```

不过，主动断开循环引用这种操作依赖于程序员自己手工显式地控制，相当于回到了以前 “谁申请谁释放” 的内存管理年代，它依赖于程序员自己有能力发现循环引用并且知道在什么时机断开循环引用回收内存（这通常与具体的业务逻辑相关），所以这种解决方法并不常用，更常见的办法是使用弱引用 (weak reference) 的办法。

## 使用弱引用

弱引用虽然持有对象，但是并不增加引用计数，这样就避免了循环引用的产生。在 iOS 开发中，弱引用通常在 delegate 模式中使用。举个例子来说，两个 ViewController A 和 B，ViewController A 需要弹出 ViewController B，让用户输入一些内容，当用户输入完成后，ViewController B 需要将内容返回给 ViewController A。这个时候，View Controller 的 delegate 成员变量通常是一个弱引用，以避免两个 ViewController 相互引用对方造成循环引用问题，如下所示：

![内存管理-循环引用4](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A84.jpg)

## 弱引用的实现原理

弱引用的实现原理是这样，系统对于每一个有弱引用的对象，都维护一个表来记录它所有的弱引用的指针地址。这样，当一个对象的引用计数为 0 时，系统就通过这张表，找到所有的弱引用指针，继而把它们都置成 nil。

从这个原理中，我们可以看出，弱引用的使用是有额外的开销的。虽然这个开销很小，但是如果一个地方我们肯定它不需要弱引用的特性，就不应该盲目使用弱引用。举个例子，有人喜欢在手写界面的时候，将所有界面元素都设置成 weak 的，这某种程度上与 Xcode 通过 Storyboard 拖拽生成的新变量是一致的。但是我个人认为这样做并不太合适。因为：

1. 我们在创建这个对象时，需要注意临时使用一个强引用持有它，否则因为 weak 变量并不持有对象，就会造成一个对象刚被创建就销毁掉。
2. 大部分 ViewController 的视图对象的生命周期与 ViewController 本身是一致的，没有必要额外做这个事情。
3. 早先苹果这么设计，是有历史原因的。在早年，当时系统收到 Memory Warning 的时候，ViewController 的 View 会被 unLoad 掉。这个时候，使用 weak 的视图变量是有用的，可以保持这些内存被回收。但是这个设计已经被废弃了，替代方案是将相关视图的 CALayer 对应的 CABackingStore 类型的内存区会被标记成 volatile 类型。

## 使用 Xcode 检测循环引用

Xcode 的 Instruments 工具集可以很方便的检测循环引用。为了测试效果，我们在一个测试用的 ViewController 中填入以下代码，该代码中的 `firstArray` 和 `secondArray` 相互引用了对方，构成了循环引用。

```
- (void)viewDidLoad
{
    [super viewDidLoad];
    NSMutableArray *firstArray = [NSMutableArray array];
    NSMutableArray *secondArray = [NSMutableArray array];
    [firstArray addObject:secondArray];
    [secondArray addObject:firstArray];
}
```

在 Xcode 的菜单栏选择：Product -> Profile，然后选择 “Leaks”，再点击右下角的”Profile” 按钮开始检测。如下图：

![内存管理-检测循环引用1](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E6%A3%80%E6%B5%8B%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A81.jpg)

这个时候 iOS 模拟器会运行起来，我们在模拟器里进行一些界面的切换操作。稍等几秒钟，就可以看到 Instruments 检测到了我们的这次循环引用。Instruments 中会用一条红色的条来表示一次内存泄漏的产生。如下图所示：

![内存管理-检测循环引用2](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E6%A3%80%E6%B5%8B%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A82.jpg)

我们可以切换到 Leaks 这栏，点击”Cycles & Roots”，就可以看到以图形方式显示出来的循环引用。这样我们就可以非常方便地找到循环引用的对象了。

![内存管理-检测循环引用3](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E6%A3%80%E6%B5%8B%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A83.png)

## Core Foundation 对象的内存管理

下面我们就来简单介绍一下对底层 Core Foundation 对象的内存管理。底层的 Core Foundation 对象，在创建时大多以 XxxCreateWithXxx 这样的方式创建，例如：

```
// 创建一个 CFStringRef 对象
CFStringRef str= CFStringCreateWithCString(kCFAllocatorDefault, “hello world", kCFStringEncodingUTF8);

// 创建一个 CTFontRef 对象
CTFontRef fontRef = CTFontCreateWithName((CFStringRef)@"ArialMT", fontSize, NULL);
```

对于这些对象的引用计数的修改，要相应的使用 CFRetain 和 CFRelease 方法。如下所示：

```
// 创建一个 CTFontRef 对象
CTFontRef fontRef = CTFontCreateWithName((CFStringRef)@"ArialMT", fontSize, NULL);

// 引用计数加 1
CFRetain(fontRef);
// 引用计数减 1
CFRelease(fontRef);
```

对于 `CFRetain` 和 `CFRelease` 两个方法，读者可以直观地认为，这与 Objective-C 对象的 `retain` 和 `release` 方法等价。

所以对于底层 Core Foundation 对象，我们只需要延续以前手工管理引用计数的办法即可。

除此之外，还有另外一个问题需要解决。在 ARC 下，我们有时需要将一个 Core Foundation 对象转换成一个 Objective-C 对象，这个时候我们需要告诉编译器，转换过程中的引用计数需要做如何的调整。这就引入了 `bridge` 相关的关键字，以下是这些关键字的说明：

- `__bridge`: 只做类型转换，不修改相关对象的引用计数，原来的 Core Foundation 对象在不用时，需要调用 CFRelease 方法。
- `__bridge_retained`：类型转换后，将相关对象的引用计数加 1，原来的 Core Foundation 对象在不用时，需要调用 CFRelease 方法。
- `__bridge_transfer`：类型转换后，将该对象的引用计数交给 ARC 管理，Core Foundation 对象在不用时，不再需要调用 CFRelease 方法。
我们根据具体的业务逻辑，合理使用上面的 3 种转换关键字，就可以解决 Core Foundation 对象与 Objective-C 对象相对转换的问题了。


# 参考文章

[理解 iOS 的内存管理](https://blog.devtang.com/2016/07/30/ios-memory-management/)

[Objective-C 中的内存分配](https://hit-alibaba.github.io/interview/iOS/ObjC-Basic/MM.html)

[Inside Memory Management for iOS](https://zxfcumtcs.github.io/2015/09/03/MemoryManagement/)

[iOS 内存管理详解](https://juejin.cn/post/6844903585814151175)

[iOS 内存管理](https://zxljack.com/2020/04/ios-memory/)

[iOS 老生常谈内存管理：导读](https://juejin.cn/post/6844904129689714695)
