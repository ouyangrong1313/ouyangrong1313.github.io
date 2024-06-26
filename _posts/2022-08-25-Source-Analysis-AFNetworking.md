---
title: AFNetworking 源码分析
author: Ouyang Rong
date: 2022-08-25 14:21:00 +0800
categories: [iOS, 源码学习]
tags: [网络, AFNetworking, HTTPS]
---


# 一、架构

AFNetworking 一共分为 5 个模块，2 个核心模块和 3 个辅助模块：

## Core

### NSURLSession（网络通信模块）

- AFURLSessionManager（封装 NSURLSession）
- AFHTTPSessionManager（继承自 AFURLSessionManager，实现了 HTTP 请求相关的配置）

### Serialization

- AFURLRequestSerialization（请求参数序列化）
    - AFHTTPRequestSerializer
    - AFJSONRequestSerializer
    - AFPropertyListRequestSerializer
- AFURLResponseSerialization（验证返回数据和反序列化）
    - AFHTTPResponseSerializer
    - AFJSONResponseSerializer
    - AFXMLParserResponseSerializer
    - AFXMLDocumentResponseSerializer (Mac OS X)
    - AFPropertyListResponseSerializer
    - AFImageResponseSerializer
    - AFCompoundResponseSerializer

## Additional Functionality

### Security（网络通信安全策略模块）

### Reachability（网络状态监听模块）

### UIKit（对 iOS 系统 UI 控件的扩展）


# 二、核心逻辑

先来看一下如何使用 AFNetworking 发送一个 GET 请求：

```
NSURL *url = [[NSURL alloc] initWithString:@"https://news-at.zhihu.com"];
AFHTTPSessionManager *manager = [[AFHTTPSessionManager alloc] initWithBaseURL:url];
[manager GET:@"api/4/news/latest" parameters:nil progress:nil
    success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
        NSLog(@"%@" ,responseObject);
    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
        NSLog(@"%@", error);
    }];
```

首先使用一个 URL，通过调用 `-initWithBaseURL:` 方法创建了一个 AFHTTPSessionManager 的实例，然后再调用 `-GET:parameters:progress:success:failure:` 方法发起请求。

## `-initWithBaseURL:` 方法的调用栈如下：

```
- [AFHTTPSessionManager initWithBaseURL:]
    - [AFHTTPSessionManager initWithBaseURL:sessionConfiguration:]
        - [AFURLSessionManager initWithSessionConfiguration:]
            - [NSURLSession sessionWithConfiguration:delegate:delegateQueue:]
            - [AFJSONResponseSerializer serializer] // 负责序列化响应
            - [AFSecurityPolicy defaultPolicy] // 负责身份认证
            - [AFNetworkReachabilityManager sharedManager] // 查看网络连接情况
            - [AFHTTPRequestSerializer serializer] // 负责序列化请求
            - [AFJSONResponseSerializer serializer] // 负责序列化响应
```

AFURLSessionManager 是 AFHTTPSessionManager 的父类， AFURLSessionManager 负责创建和管理 NSURLSession 的实例，管理 AFSecurityPolicy 和初始化 AFNetworkReachabilityManager，来保证请求的安全和查看网络连接情况，它有一个 AFJSONResponseSerializer 的实例来序列化 HTTP 响应。

AFHTTPSessionManager 有着自己的 AFHTTPRequestSerializer 和 AFJSONResponseSerializer 来管理请求和响应的序列化，同时依赖父类实现发出 HTTP 请求、管理 Session 这一核心功能。

## `-GET:parameters:progress:success:failure:` 方法的调用栈：

```
 - [AFHTTPSessionManager GET:parameters:process:success:failure:]
    - [AFHTTPSessionManager dataTaskWithHTTPMethod:parameters:uploadProgress:downloadProgress:success:failure:] // 返回一个 NSURLSessionDataTask 对象
        - [AFHTTPRequestSerializer requestWithMethod:URLString:parameters:error:] // 返回 NSMutableURLRequest
        - [AFURLSessionManager dataTaskWithRequest:uploadProgress:downloadProgress:completionHandler:] 返回一个 NSURLSessionDataTask 对象
            - [NSURLSession dataTaskWithRequest:] 返回一个 NSURLSessionDataTask 对象
            - [AFURLSessionManager addDelegateForDataTask:uploadProgress:downloadProgress:completionHandler:]
                - [AFURLSessionManagerTaskDelegate init]
                - [AFURLSessionManager setDelegate:forTask:] // 为每个 task 创建一个对应的 delegate
    - [NSURLSessionDataTask resume]
```

发送请求的核心在于创建和启动一个 data task，AFHTTPSessionManager 只是提供了 HTTP 请求的接口，内部最终还是调用了父类 AFURLSessionManager 来创建 data task（其实也就是通过 NSURLSession 创建的 task），AFURLSessionManager 中会为每个 task 创建一个对应的 AFURLSessionManagerTaskDelegate 对象，用来处理回调。

在请求发起时有一个序列化的工具类 AFHTTPRequestSerializer 来处理请求参数。

## 请求回调时的方法调用栈：

```
- [AFURLSessionManager  URLSession:task:didCompleteWithError:]
  - [AFURLSessionManagerTaskDelegate URLSession:task:didCompleteWithError:]
    - [AFJSONResponseSerializer responseObjectForResponse:data:error:]  // 解析 JSON 数据
      - [AFHTTPResponseSerializer validateResponse:data:]  // 验证数据
    - [AFURLSessionManagerTaskDelegate URLSession:task:didCompleteWithError:]_block_invoke_2.150
      - [AFHTTPSessionManager dataTaskWithHTTPMethod:URLString:parameters:uploadProgress:downloadProgress:success:failure:]_block_invoke
```

AFURLSessionManager 在代理方法中收到服务器返回数据的后，会交给 AFURLSessionManagerTaskDelegate 去处理，接着就是用 AFJSONResponseSerializer 去验证和解析 JSON 数据，最后再通过 block 回调的方式返回最终结果。


# 三、AFURLSessionManager

- 负责创建和管理 NSURLSession
- 管理 NSURLSessionTask
- 实现 NSURLSessionDelegate 等协议中的代理方法
- 使用 AFURLSessionManagerTaskDelegate 管理上传、下载进度，以及请求完成的回调
- 将整个请求流程相关的组件串联起来
- 负责整个请求过程的线程调度
- 使用 AFSecurityPolicy 验证 HTTPS 请求的证书

## 1. 线程

一般调用 AFNetworking 的请求 API 时，都是在主线程，也是主队列。然后直到调用 NSURLSession 的 `-resume` 方法，一直都是在主线程。

在 AFURLSessionManager 的初始化方法中，设置了 NSURLSession 代理回调线程的最大并发数为 1，因为就像 NSURLSession 的 `-sessionWithConfiguration:delegate:delegateQueue:` 方法的官方文档中所说的那样，所有的代理方法回调都应该在一个串行队列中，因为只有这样才能保证代理方法的回调顺序。

NSURLSession 代理方法回调是异步的，所以收到回调时的线程模式是“异步+串行队列”，这个时候可以理解为处于回调线程。

```
- (instancetype)initWithSessionConfiguration:(NSURLSessionConfiguration *)configuration {
    ...
    self.operationQueue = [[NSOperationQueue alloc] init];
    self.operationQueue.maxConcurrentOperationCount = 1;  // 代理回调线程最大并发数为 1
    // 初始化 NSURLSession 对象
    self.session = [NSURLSession sessionWithConfiguration:self.sessionConfiguration delegate:self delegateQueue:self.operationQueue];
    ...
    return self;
}
```

收到代理回调后，接着在 AFURLSessionManagerTaskDelegate 的 `-URLSession:task:didCompleteWithError:` 方法中，异步切换到 processing queue 进行数据解析，数据解析完成后再异步回到主队列或者自定义队列。

```
- (void)URLSession:(__unused NSURLSession *)session
              task:(NSURLSessionTask *)task
didCompleteWithError:(NSError *)error
{
    ...
    // 如果请求成功，则在一个 AF 的并行 queue 中，去做数据解析等后续操作
    dispatch_async(url_session_manager_processing_queue(), ^{
        NSError *serializationError = nil;
        responseObject = [manager.responseSerializer responseObjectForResponse:task.response data:data error:&serializationError];
        ...
        dispatch_group_async(manager.completionGroup ?: url_session_manager_completion_group(), manager.completionQueue ?: dispatch_get_main_queue(), ^{
            if (self.completionHandler) {
                self.completionHandler(task.response, responseObject, serializationError);
            }
            ...
        });
    });
    ...
}
```

## 2. AFURLSessionManagerTaskDelegate

AFURLSessionManager 中几乎实现了所有的 NSURLSession 相关的协议方法：

- NSURLSessionDelegate
- NSURLSessionTaskDelegate
- NSURLSessionDataDelegate
- NSURLSessionDownloadDelegate

AFURLSessionManager 把最核心的代理回调处理交给 AFURLSessionManagerTaskDelegate 类去实现了，AFURLSessionManagerTaskDelegate 可以根据对应的 task 去进行上传、下载进度回调和请求完成的回调处理：

```
- URLSession:task:didCompleteWithError:
- URLSession:dataTask:didReceiveData:
- URLSession:downloadTask:didFinishDownloadingToURL:
```

AFURLSessionManager 通过属性 `mutableTaskDelegatesKeyedByTaskIdentifier` （一个 NSDictionary 对象）来存储并管理每一个 NSURLSessionTask 所对应的 AFURLSessionManagerTaskDelegate，它以 taskIdentifier 为键存储 task。在请求最终完成后，又将 AFURLSessionManagerTaskDelegate 移除。

## 3. NSProgress

AFURLSessionManagerTaskDelegate 借助了 NSProgress 这个类来实现进度的管理，NSProgress 是 iOS 7 引进的一个用来管理任务进度的类，可以表示一个任务的进度信息，我们还可以对其进行开始、暂停、取消等操作，完整的对应了 task 的各种状态。

AFURLSessionManagerTaskDelegate 通过 KVO 监听 task 的进度更新，来同步更新 NSProgress 的进度数据。同时，还用 KVO 监听了 NSProgress 的 fractionCompleted 属性的变化，用来更新最外面的进度回调 block，回调时将这个 NSProgress 对象作为参数带过去。

另一方面，AFURLSessionManagerTaskDelegate 中还分别对下载和上传的 NSProgress 对象设置了开始、暂停、取消等操作的 handler，将 task 跟 NSProgress 的状态关联起来。这样一来，就可以通过控制 NSProgress 对象的这些操作就可以控制 task 的状态。

## 4. NSSecureCoding

AFNetworking 的大多数类都支持归档解档，但实现的是 NSSecureCoding 协议，而不是 NSCoding 协议，这两个协议的区别在于 NSSecureCoding 协议中定义的解码的方法是 `-decodeObjectOfClass:forKey:` 方法，而不是 `-decodeObjectForKey:`，这就要求解数据时要指定 Class。

## 5. _AFURLSessionTaskSwizzling

`_AFURLSessionTaskSwizzling` 的唯一作用就是将 NSURLSessionTask 的 `-resume` 和 `-suspend` 方法实现替换成自己的实现，`_AFURLSessionTaskSwizzling` 中这两个方法的实现是先调用原方法，然后再发出一个通知。


# 四、AFURLRequestSerialization

AFURLRequestSerialization 是一个抽象的协议，用于构建一个规范的 NSURLRequest。基于 AFURLRequestSerialization 协议，AFNetworking 提供了 3 中不同数据形式的序列化工具。

- AFHTTPRequestSerializer：普通的 HTTP 请求，默认数据格式是 `application/x-www-form-urlencoded`，也就是 key-value 形式的 url 编码字符串
- AFJSONRequestSerializer：参数格式是 json
- AFPropertyListRequestSerializer：参数格式是苹果的 plist 格式

AFHTTPRequestSerializer 主要实现了两个功能：

- 构建普通请求：格式化请求参数，生成 HTTP Header。
- 构建 multipart 请求，上传数据时会用到。

## 1. 构建普通请求

AFHTTPRequestSerializer 在构建普通请求时，做了以下几件事：

- 创建 NSURLRequest
- 设置 NSURLRequest 相关属性
- 设置 HTTP Method
- 设置 HTTP Header
- 序列化请求参数

```
- (NSMutableURLRequest *)requestWithMethod:(NSString *)method
                                 URLString:(NSString *)URLString
                                parameters:(id)parameters
                                     error:(NSError *__autoreleasing *)error
{
    NSParameterAssert(method);
    NSParameterAssert(URLString);

    NSURL *url = [NSURL URLWithString:URLString];

    NSParameterAssert(url);

    // 创建请求
    NSMutableURLRequest *mutableRequest = [[NSMutableURLRequest alloc] initWithURL:url];
    mutableRequest.HTTPMethod = method; // 设置 Method

    // 这里本来是直接把 self 的一些属性值直接传给 request 的，但是因为初始默认情况下，
    // 当前类中与 NSURLRequest 相关的那些属性值为 0，而导致外面业务方使用 NSURLSessionConfiguration 设置属性时失效，
    // 所以通过对这些属性添加了 KVO 监听判断是否有值来解决这个传值的有效性问题
    // 详见 https://github.com/AFNetworking/AFNetworking/commit/49f2f8c9a907977ec1b3afb182404ae0a6bce883
    for (NSString *keyPath in AFHTTPRequestSerializerObservedKeyPaths()) {
        if ([self.mutableObservedChangedKeyPaths containsObject:keyPath]) {
            [mutableRequest setValue:[self valueForKeyPath:keyPath] forKey:keyPath];
        }
    }

    // 设置 HTTP header；请求参数序列化，再添加到 query string 或者 body 中
    mutableRequest = [[self requestBySerializingRequest:mutableRequest withParameters:parameters error:error] mutableCopy];

    return mutableRequest;
}
```

AFNetworking 帮我们组装好了一些 HTTP 请求头，包括：

- `Content-Type`，请求参数类型
- `Accept-Language`，根据 `[NSLocale preferredLanguages]` 方法读取本地语言，告诉服务端自己能接受的语言。
- `User-Agent`
- `Authorization`，提供 Basic Auth 认证接口，帮我们把用户名密码做 base64 编码后放入 HTTP 请求头。

参数序列化流程大概是这样的：

- 用户传进来的数据，支持包含 NSArray，NSDictionary，NSSet 这三种数据结构。
- 先将每组 `key-value` 转成 AFQueryStringPair 对象的形式，保存到数组中（这样做的目的是因为最后可以根据不同的字符串编码生成对应的 `key=value` 字符串）
- 然后取出数组中的 AFQueryStringPair 对象，转成一个个 NSString 对象再保存到新数组中
- 最后再将这些 `key=value` 的字符串用 `&` 符号拼接起来

```
@{
     @"name"    : @"steve",
     @"phone"   : @{@"mobile": @"xx", @"home": @"xx"},
     @"families": @[@"father", @"mother"],
     @"nums"    : [NSSet setWithObjects:@"1", @"2", nil]
}
                    ||
                    \/
@[
     field: @"name",          value: @"steve",
     field: @"phone[mobile]", value: @"xx",
     field: @"phone[home]",   value: @"xx",
     field: @"families[]",    value: @"father",
     field: @"families[]",    value: @"mother",
     field: @"nums",          value: @"1",
     field: @"nums",          value: @"2",
]
                    ||
                    \/

@[
    @"name=steve",        // 注：实际代码中这里的 “=” 会被编码
    @"phone[mobile]=xx",
    @"phone[home]=xx",
    @"families[]=father",
    @"families[]=mother",
    @"nums=1",
    @"nums=2"
]
                    ||
                    \/

@"name=steve&phone[mobile]=xx&phone[home]=xx&families[]=father&families[]=mother&nums=1&nums=2"
```

请求参数序列化完成后，再根据不同的 HTTP 请求方法分别处理，对于 GET/HEAD/DELETE 方法，把参数直接加到 URL 后面，对于其他如 POST/PUT 等方法，把数据加到 body 上，并设好 HTTP 头中的 `Content-Type` 为 `application/x-www-form-urlencoded`，告诉服务端字符串的编码是什么。

## 2. 构建 multipart 请求


# 五、AFURLResponseSerialization

AFURLResponseSerialization 模块负责解析网络返回数据，检查数据是否合法，把服务器返回的 NSData 数据转成相应的对象。 AFURLResponseSerialization 模块包括一个协议、一个基类和多个解析特定格式数据的子类，用户可以很方便地继承基类 AFHTTPResponseSerializer 去解析更多的数据格式：

- AFURLResponseSerialization 协议，定义了解析响应数据的接口
- AFHTTPResponseSerializer，HTTP 请求响应数据解析器的基类
- AFJSONResponseSerializer，专门解析 JSON 数据的解析器
- 其他数据格式（XML、image、plist等）的响应解析器
- AFCompoundResponseSerializer，组合解析器，可以将多个解析器组合起来，以同时支持多种格式的数据解析

AFURLResponseSerialization 模块响应解析机制主要涉及到两个核心方法：

- AFHTTPResponseSerializer 中定义、实现的 `-validateResponse:data:error:` 方法
- AFURLResponseSerialization 协议定义的 `-responseObjectForResponse:data:error:` 方法

## 1. `-validateResponse:data:error:` 方法

AFHTTPResponseSerializer 作为解析器基类，提供了 `acceptableContentTypes` 和 `acceptableStatusCodes` 两个属性，并提供了 `acceptableStatusCodes` 的默认值，子类可以通过设置这两个属性的值来进行自定义配置。AFHTTPResponseSerializer 中的 `-validateResponse:data:error:` 方法会根据这两个属性值来判断响应的文件类型 `MIMEType` 和状态码 `statusCode` 是否合法。

 比如 AFJSONResponseSerializer 中设置了 `acceptableContentTypes` 的值为 `[NSSet setWithObjects:@"application/json", @"text/json", @"text/javascript", nil]`，如果服务器返回的 `Content-Type` 不是这三者之一，`-validateResponse:data:error:` 方法就会返回解析失败的错误信息。

## 2. `-responseObjectForResponse:data:error:` 方法

AFJSONResponseSerializer 等子类中实现的 `-responseObjectForResponse:data:error:` 方法会先调用 `-validateResponse:data:error:` 方法验证数据是否合法，拿到验证结果后，接着这里有个补充判断条件——如果是 content type 的错误就直接返回 nil，因为数据类型不符合要求，就没必要再继续解析数据了，如果是 status code 的错误就继续解析，因为数据本身没问题，而错误信息有可能就在返回的数据中，所以这种情况下会将 status code 产生的错误信息和解析后的数据一起“打包”返回。

AFJSONResponseSerializer 在解析数据后还提供了移除 NSNull 的功能，主要是为了防止服务端返回 null 时导致解析后的数据中有了脆弱的 NSNull，这样很容易导致崩溃。

```
- (id)responseObjectForResponse:(NSURLResponse *)response
                           data:(NSData *)data
                          error:(NSError *__autoreleasing *)error
{
    if (![self validateResponse:(NSHTTPURLResponse *)response data:data error:error]) {

        // 如果是 content type 的错误就直接返回，因为数据类型不符合要求
        // 如果是 status code 的错误就继续解析，因为错误信息有可能就在返回的数据中
        if (!error || AFErrorOrUnderlyingErrorHasCodeInDomain(*error, NSURLErrorCannotDecodeContentData, AFURLResponseSerializationErrorDomain)) {
            return nil;
        }
    }

    NSError *serializationError = nil;
    id responseObject = [NSJSONSerialization JSONObjectWithData:data options:self.readingOptions error:&serializationError];

    ...

    // 移除 NSNull（如果需要的话），默认是 NO
    if (self.removesKeysWithNullValues && responseObject) {
        responseObject = AFJSONObjectByRemovingKeysWithNullValues(responseObject, self.readingOptions);
    }

    ...

    return responseObject;
}
```


# 六、AFSecurityPolicy

几个关键字：HTTPS，TSL，SSL，SSL Pinning，非对称加密算法

## 1. 预备知识点

### 1.1 为什么要使用 HTTPS

因为直接使用 HTTP 请求，就会有可能遇到以下几个安全问题：

- 传输数据被窃听：HTTP 报文使用明文方式发送，而且 HTTP 本身不具备加密的功能，而互联网是由联通世界各个地方的网络设施组成，所有发送和接收经过某些设备的数据都可能被截获或窥视。
- 认证问题：
    - 无法确认你发送到的服务器就是真正的目标服务器（可能服务器是伪装的）
    - 无法确定返回的客户端是否是按照真实意图接收的客户端（可能是伪装的客户端）
    - 无法确定正在通信的对方是否具备访问权限（Web服务器上某些重要的信息，只想发给特定用户）
- 传输内容可能被篡改：请求或响应在传输途中，可能会被攻击者拦截并篡改内容，也就是所谓的中间人攻击（Man-in-the-Middle attack，MITM）。

### 1.2 HTTPS 的出现

HTTPS，也称作 HTTP over TLS，HTTPS 就是基于 TLS 的 HTTP 请求。TLS 是一种基于 TCP 的加密协议，它主要做了两件事：传输的两端可以互相验证对方的身份，以及验证后加密所传输的数据。

HTTPS 通过验证和加密两种手段的结合解决了上面 HTTP 所面临的 3 个安全问题。

### 1.3 SSL/TLS 协议

SSL（Secure Sockets Layer）：SSL 协议是一种数据加密协议，为了保证网络数据传输的安全性，网景公司设计了 SSL 协议用于对 HTTP 协议传输的数据进行加密，从而就诞生了 HTTPS。

TLS（Transport Layer Security）：TLS 协议是 SSL 协议的升级版。1999年，互联网标准化组织 ISOC 接替 NetScape 公司，发布了 SSL 的升级版 TLS 1.0版。

### 1.4 HTTPS 与 HTTP 的区别是什么？

 --- | HTTP | HTTPS
---|---|---
URL | `http://` 开头，并且默认使用端口 80 | `https://` 开头，并且默认使用端口 443
数据隐私性 | 明文传输，不加密传输数据 | 基于 TLS 的加密传输
身份认证 | 不认证 | 正式传输数据前会进行证书认证，第三方无法伪造服务端（客户端）身份
数据完整性 | 没有完整性校验过程 | 内容传输经过完整性校验

HTTP协议和安全协议（SSL/TLS）同属于应用层（OSI模型的最高层），具体来讲，安全协议（SSL/TLS）工作在 HTTP 之下，传输层之上：安全协议向运行 HTTP 的进程提供一个类似于 TCP 的套接字，供进程向其中注入报文，安全协议将报文加密并注入传输层套接字；或是从运输层获取加密报文，解密后交给对应的进程。严格地讲，HTTPS 并不是一个单独的协议，而是对工作在一加密连接（TLS或SSL）上的常规 HTTP 协议的称呼。

HTTPS 报文中的任何东西都被加密，包括所有报头和荷载（payload）。除了可能的选择密文攻击之外，一个攻击者所能知道的只有在两者之间有一连接这件事。

### 1.5 HTTPS 连接的建立过程

HTTPS在传输数据之前需要客户端与服务端之间进行一次握手，在握手过程中将确立双方加密传输数据的密码信息。（握手过程采用的非对称加密，正式传输数据时采用的是对称加密）

HTTPS 的认证有单向认证和双向认证，这里简单梳理一下客户端单向认证时的握手流程：

（1）客户端发起一个请求，服务端响应后返回一个证书，证书中包含一些基本信息和公钥。
（2）客户端里存有各个受信任的证书机构根证书，用这些根证书对服务端返回的证书进行验证，如果不可信任，则请求终止。 （3）如果证书受信任，或者是用户接受了不受信的证书，客户端会生成一串随机数的密码 random key，并用证书中提供的公钥加密，再返回给服务器。 （4）服务器拿到加密后的随机数，利用私钥解密，然后再用解密后的随机数 random key，对需要返回的数据加密，加密完成后将数据返回给客户端。            （5）最后用户拿到被加密过的数据，用客户端一开始生成的那个随机数 random key，进行数据解密。整个 TLS/SSL 握手过程完成。

完整的 HTTPS 连接的建立过程，包括下面三个步骤：

（1）TCP 协议的三次握手；
（2）TLS/SSL 协议的握手、密钥协商；
（3）使用共同约定的密钥开始通信。

### 1.6 HTTPS 传输时是如何验证证书的？怎样应对中间人伪造证书？

先来看看维基百科上对对称加密和非对称加密的解释：

> 对称密钥加密（英语：Symmetric-key algorithm）又称为对称加密、私钥加密、共享密钥加密，是密码学中的一类加密算法。这类算法在加密和解密时使用相同的密钥，或是使用两个可以简单地相互推算的密钥。实务上，这组密钥成为在两个或多个成员间的共同秘密，以便维持专属的通讯联系。与公开密钥加密相比，要求双方取得相同的密钥是对称密钥加密的主要缺点之一。

> 公开密钥加密（英语：public-key cryptography，又译为公开密钥加密），也称为非对称加密（asymmetric cryptography），一种密码学算法类型，在这种密码学方法中，需要一对密钥(其实这里密钥说法不好，就是“钥”)，一个是私人密钥，另一个则是公开密钥。这两个密钥是数学相关，用某用户密钥加密后所得的信息，只能用该用户的解密密钥才能解密。如果知道了其中一个，并不能计算出另外一个。因此如果公开了一对密钥中的一个，并不会危害到另外一个的秘密性质。称公开的密钥为公钥；不公开的密钥为私钥。

从上面可以看出非对称加密的特点：非对称加密有一对公钥私钥，用公钥加密的数据只能通过对应的私钥解密，用私钥加密的数据只能通过对应的公钥解密。这种加密是单向的。

#### （1）HTTPS 传输时是如何验证证书的呢？

我们以最简单的为例：一个证书颁发机构(CA)，颁发了一个证书 Cer，服务器用这个证书建立 HTTPS 连接，同时客户端在信任列表里有这个 CA 机构的根证书。

CA 机构颁发的证书 Cer 里包含有证书内容 Content，以及证书加密内容 Crypted Content（数字签名），这个加密内容 Crypted Content 就是用这个证书机构的私钥对内容 Content 加密的结果。

```
+-------------------+
|      Content      |
+-------------------+
|   Crypted Content |
+-------------------+
     证书 Cer
```

建立 HTTPS 连接时，服务端会把证书 Cer 返回给客户端，客户端系统里的 CA 机构根证书有这个 CA 机构的公钥，用这个公钥对证书 Cer 的加密内容 Crypted Content 解密得到 Content，跟证书 Cer 里的内容 Content 对比，若相等就通过验证。大概的流程如下：

```
       +-----------------------------------------------------+
       |           crypt with private key                    |
       |  Content ------------------------> Crypted Content  |
Server |                                                     |
       |                     证书 Cer                  　     |
       +-----------------------------------------------------+

                          ||        
                          ||
                          \/

       +-----------------------------------------------------+
       |                                                     |
       |               Content  &  Crypted Content           |
Client |                  |               |                  |
       |                  |  证书 Cer    　|            　    |
       +------------------|---------------|------------------+
        　　　　　　　　　　　 |　　　　　　　　　|
        　　　　　　　　　　　 |　　　　　　　　　| derypt with public key 　　
        　　　　　　　　　　　 |　　　　　　　　　|
        　　　　　　　　　　　 \/　　　　相等？  \/
        　　　　　　　　　Content　－－－－－－ Decrypted Content　　
        　　　　　　　　　
        　　　　　　　　　            　　　　　　
```

#### （2）怎样应对中间人伪造证书？

因为中间人不会有 CA 机构的私钥，即便伪造了一张证书，但是私钥不对，加密出来的内容也就不对，客户端也就无法通过 CA 公钥解密，所以伪造的证书肯定无法通过验证。

### 1.7 Certificate Pinning 是什么？

如果一个客户端通过 TLS 和服务器建立连接，操作系统会验证服务器证书的有效性（一般是按照X.509标准）。当然，有很多手段可以绕开这个校验，最直接的是在 iOS 设备上安装证书并且将其设置为可信的。这种情况下，实施中间人攻击也不是什么难事。不过通过 Certificate Pinning 可以解决这个问题。

> A client that does key pinning adds an extra step beyond the normal X.509 certificate validation.
>             —— Wikipedia：Certificate Pinning

Certificate Pinning，可以理解为证书绑定，有时候又叫 SSL Pinning，其实更准确的叫法应该是 Public Key Pinning（公钥绑定）。证书绑定是一种检测和防止“中间人攻击”的方式，客户端直接保存服务端的证书，当建立 TLS 连接后，应立即检查服务器的证书，不仅要验证证书的有效性，还需要确定证书是不是跟客户端本地的证书相匹配。考虑到应用和服务器需要同时升级证书的要求，这种方式比较适合应用在访问自家服务器的情况下。

#### 为什么直接对比就能保证证书没问题？

如果中间人从客户端取出证书，再伪装成服务端跟其他客户端通信，它发送给客户端的这个证书不就能通过验证吗？确实可以通过验证，但后续的流程走不下去，因为下一步客户端会用证书里的公钥加密，中间人没有这个证书的私钥就解不出内容，也就截获不到数据，这个证书的私钥只有真正的服务端有，中间人伪造证书主要伪造的是公钥。

#### 什么情况下需要使用 Certificate Pinning？

- 就像前面所说的，常规的验证方式并不能避免遭遇中间人攻击，因为如果所访问网站的证书是自制的，而且在客户端上通过手动安装根证书信任了，此时就很容易被恶意攻击了（还记得你访问 12306 时收到的证书验证提醒吗）。
- 如果服务端的证书是从受信任的的 CA 机构颁发的，验证是没问题的，但 CA 机构颁发证书比较昂贵，小企业或个人用户可能会选择自己颁发证书，这样就无法通过系统受信任的 CA 机构列表验证这个证书的真伪了。

## 2. AFSecurityPolicy 的实现

### 2.1 AFSecurityPolicy 的作用

NSURLConnection 和 NSURLSession 已经封装了 HTTPS 连接的建立、数据的加密解密功能，我们直接使用 NSURLConnection 或者 NSURLSession 也是可以访问 HTTPS 网站的，但 NSURLConnection 和 NSURLSession 并没有验证证书是否合法，无法避免中间人攻击。要做到真正安全通讯，需要我们手动去验证服务端返回的证书（系统提供了 `SecTrustEvaluate` 函数供我们验证证书使用）。

AFSecurityPolicy 帮我们封装了证书验证的逻辑，让用户可以轻易使用，除了在系统的信任机构列表里验证，还支持 SSL Pinning 方式的验证。

### 2.2 使用方法

如果是权威机构颁发的证书，不需要任何设置。
如果是自签名证书，但是不做证书绑定，直接按照下面的代码实现即可：

```
AFSecurityPolicy *securityPolicy = [AFSecurityPolicy policyWithPinningMode:AFSSLPinningModeNone];
// 允许无效证书（包括自签名证书），必须的
policy.allowInvalidCertificates = YES;
// 是否验证域名的CN字段
// 不是必须的，但是如果写YES，则必须导入证书。
policy.validatesDomainName = NO;
AFHTTPSessionManager *manager = [[AFHTTPSessionManager alloc] initWithBaseURL:[NSURL URLWithString:<#MyAPIBaseURLString#>]];
manager.securityPolicy = securityPolicy;
```

如果是自签名证书，而且还要做证书绑定，就需要把自签的服务端证书，或者自签的CA根证书导入到项目中（把 cer 格式的服务端证书放到 APP 项目资源里，AFSecurityPolicy 会自动寻找根目录下所有 cer 文件，当然你也可以自己读取），然后再选择验证证书或者公钥。

### 2.3 AFSecurityPolicy 的实现

在 AFURLSessionManager 中实现的 `-URLSession:didReceiveChallenge:completionHandler:` 方法中，根据 NSURLAuthenticationChallenge 对象中的 authenticationMethod，来决定是否需要验证服务器证书，如果需要验证，则借助 AFSecurityPolicy 来验证证书，验证通过则创建 NSURLCredential，并回调 handler：

```
- (void)URLSession:(NSURLSession *)session
didReceiveChallenge:(NSURLAuthenticationChallenge *)challenge
 completionHandler:(void (^)(NSURLSessionAuthChallengeDisposition disposition, NSURLCredential *credential))completionHandler
{
    /*
     NSURLSessionAuthChallengeUseCredential：使用指定的证书
     NSURLSessionAuthChallengePerformDefaultHandling：默认方式处理
     NSURLSessionAuthChallengeCancelAuthenticationChallenge：取消整个请求
     NSURLSessionAuthChallengeRejectProtectionSpace：
     */

    NSURLSessionAuthChallengeDisposition disposition = NSURLSessionAuthChallengePerformDefaultHandling;
    __block NSURLCredential *credential = nil;

    if (self.sessionDidReceiveAuthenticationChallenge) {
        disposition = self.sessionDidReceiveAuthenticationChallenge(session, challenge, &credential);
    } else {

        // 此处服务器要求客户端的接收认证挑战方法是 NSURLAuthenticationMethodServerTrust，也就是说服务器端需要客户端验证服务器返回的证书信息
        if ([challenge.protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodServerTrust]) {

            // 客户端根据安全策略验证服务器返回的证书
            // AFSecurityPolicy 在这里的作用就是，使得在系统底层自己去验证之前，AF可以先去验证服务端的证书。如果通不过，则直接越过系统的验证，取消https的网络请求。否则，继续去走系统根证书的验证（？？）。
            if ([self.securityPolicy evaluateServerTrust:challenge.protectionSpace.serverTrust forDomain:challenge.protectionSpace.host]) {
                // 信任的话，就创建验证凭证去做系统根证书验证

                // 创建 NSURLCredential 前需要调用 SecTrustEvaluate 方法来验证证书，这件事情其实 AFSecurityPolicy 已经帮我们做了
                credential = [NSURLCredential credentialForTrust:challenge.protectionSpace.serverTrust];
                if (credential) {
                    disposition = NSURLSessionAuthChallengeUseCredential;
                } else {
                    disposition = NSURLSessionAuthChallengePerformDefaultHandling;
                }
            } else {
                // 不信任的话，就直接取消整个请求
                disposition = NSURLSessionAuthChallengeCancelAuthenticationChallenge;
            }
        } else {
            disposition = NSURLSessionAuthChallengePerformDefaultHandling;
        }
    }

    if (completionHandler) {
        // 疑问：这个 completionHandler 是用来干什么的呢？credential 又是用来干什么的呢？
        completionHandler(disposition, credential);
    }
}
```

而 AFSecurityPolicy 的核心就在于 `-evaluateServerTrust:forDomain:` 方法，该方法中主要做了四件事：

- 设置验证标准（`SecTrustSetPolicies`），为认证做准备
- 处理 SSLPinningMode 为 `AFSSLPinningModeNone` 的情况——如果允许无效的证书（包括自签名证书）就直接返回 YES，不允许的话就在系统的信任机构列表里验证服务端证书。
- 处理 SSLPinningMode 为 `AFSSLPinningModeCertificate` 的情况，认证证书——设置证书锚点->验证服务端证书->匹配服务端证书链
- 处理 SSLPinningMode 为 `AFSSLPinningModePublicKey` 的情况，认证公钥——匹配服务端证书公钥

```
- (BOOL)evaluateServerTrust:(SecTrustRef)serverTrust
                  forDomain:(NSString *)domain
{
    /*
     AFSecurityPolicy 的四个主要属性：
     SSLPinningMode - 证书认证模式
     pinnedCertificates - 用来匹配服务端证书信息的证书，这些证书保存在客户端
     allowInvalidCertificates - 是否支持无效的证书（包括自签名证书）
     validatesDomainName - 是否去验证证书域名是否匹配


     SSLPinningMode 提供的三种证书认证模式：
     AFSSLPinningModeNone - 没有 SSL pinning
     AFSSLPinningModePublicKey - 用证书绑定方式验证，客户端要有服务端的证书拷贝，只是验证时只验证证书里的公钥，不验证证书的有效期等信息
     AFSSLPinningModeCertificate - 用证书绑定方式验证证书，需要客户端保存有服务端的证书拷贝，这里验证分两步，第一步验证证书的域名/有效期等信息，第二步是对比服务端返回的证书跟客户端返回的是否一致。

     */


    // 判断互相矛盾的情况：
    // 如果有域名，而且还要允许自签证书，同时还要验证域名的话，就一定要验证服务器返回的证书是否匹配客户端本地的证书了
    // 所以必须满足两个条件：A验证模式不能为 FSSLPinningModeNone；添加到项目里的证书至少 1 个。
    if (domain && self.allowInvalidCertificates && self.validatesDomainName && (self.SSLPinningMode == AFSSLPinningModeNone || [self.pinnedCertificates count] == 0)) {

        NSLog(@"In order to validate a domain name for self signed certificates, you MUST use pinning.");
        return NO;
    }

    // 为 serverTrust 设置 policy，也就是告诉客户端如何验证 serverTrust
    // 如果要验证域名的话，就以域名为参数创建一个 SecPolicyRef，否则会创建一个符合 X509 标准的默认 SecPolicyRef 对象
    NSMutableArray *policies = [NSMutableArray array];
    if (self.validatesDomainName) {
        [policies addObject:(__bridge_transfer id)SecPolicyCreateSSL(true, (__bridge CFStringRef)domain)];
    } else {
        [policies addObject:(__bridge_transfer id)SecPolicyCreateBasicX509()];
    }

    SecTrustSetPolicies(serverTrust, (__bridge CFArrayRef)policies);

    // 验证证书是否有效
    if (self.SSLPinningMode == AFSSLPinningModeNone) {
        // 如果不做证书绑定，就会跟浏览器一样在系统的信任机构列表里验证服务端返回的证书（如果是自己买的证书，就不需要绑定证书了，可以直接在系统的信任机构列表里验证就行了）
        // 如果允许无效的证书（包括自签名证书）就会直接返回 YES，不允许的话就会对服务端证书在系统的信任机构列表里验证。如果服务器证书无效，并且不允许无效证书，就会返回 NO

        return self.allowInvalidCertificates || AFServerTrustIsValid(serverTrust);

    } else if (!AFServerTrustIsValid(serverTrust) && !self.allowInvalidCertificates) {
        // 如果不是 AFSSLPinningModeNone，而且证书在系统的信任机构列表里验证失败，同时不允许无效的证书（包括自签名证书）时，直接返回评估失败
        // （如果是自签名的证书，验证时就需要做证书绑定，或者直接在系统的信任机构列表里中添加根证书）

        return NO;
    }

    // 根据 SSLPinningMode 对服务端返回的证书进行 SSL Pinning 验证，也就是说拿本地的证书和服务端证书进行匹配
    switch (self.SSLPinningMode) {
        case AFSSLPinningModeNone:
        default:
            return NO;
        case AFSSLPinningModeCertificate: {

            // 把证书 data 转成 SecCertificateRef 类型的数据，保证返回的证书都是 DER 编码的 X.509 证书
            NSMutableArray *pinnedCertificates = [NSMutableArray array];
            for (NSData *certificateData in self.pinnedCertificates) {
                [pinnedCertificates addObject:(__bridge_transfer id)SecCertificateCreateWithData(NULL, (__bridge CFDataRef)certificateData)];
            }

            // 1.
            // 将 pinnedCertificates 设置成需要参与验证的 Anchor Certificate（锚点证书，嵌入到操作系统中的根证书，也就是权威证书颁发机构颁发的自签名证书），通过 SecTrustSetAnchorCertificates 设置了参与校验锚点证书之后，假如验证的数字证书是这个锚点证书的子节点，即验证的数字证书是由锚点证书对应CA或子CA签发的，或是该证书本身，则信任该证书，具体就是调用 SecTrustEvaluate 来验证。
            SecTrustSetAnchorCertificates(serverTrust, (__bridge CFArrayRef)pinnedCertificates);

            // 自签证书在之前是验证通过不了的，在这一步，把我们自己设置的证书加进去之后，就能验证成功了。
            // 再去调用之前的 serverTrust 去验证该证书是否有效，有可能经过这个方法过滤后，serverTrust 里面的 pinnedCertificates 被筛选到只有信任的那一个证书
            if (!AFServerTrustIsValid(serverTrust)) {
                return NO;
            }

            // 注意，这个方法和我们之前的锚点证书没关系了，是去从我们需要被验证的服务端证书，去拿证书链。
            // 服务器端的证书链，注意此处返回的证书链顺序是从叶节点到根节点
            // obtain the chain after being validated, which *should* contain the pinned certificate in the last position (if it's the Root CA)
            NSArray *serverCertificates = AFCertificateTrustChainForServerTrust(serverTrust);

            for (NSData *trustChainCertificate in [serverCertificates reverseObjectEnumerator]) {
                // 如果我们的证书中，有一个和它证书链中的证书匹配的，就返回 YES
                if ([self.pinnedCertificates containsObject:trustChainCertificate]) {
                    return YES;
                }
            }

            return NO;
        }
        case AFSSLPinningModePublicKey: {
            NSUInteger trustedPublicKeyCount = 0;

            // 获取服务器证书公钥
            NSArray *publicKeys = AFPublicKeyTrustChainForServerTrust(serverTrust);

            // 判断自己本地的证书的公钥是否存在与服务器证书公钥一样的情况，只要有一组符合就为真
            for (id trustChainPublicKey in publicKeys) {
                for (id pinnedPublicKey in self.pinnedPublicKeys) {
                    if (AFSecKeyIsEqualToKey((__bridge SecKeyRef)trustChainPublicKey, (__bridge SecKeyRef)pinnedPublicKey)) {
                        trustedPublicKeyCount += 1;
                    }
                }
            }
            return trustedPublicKeyCount > 0;
        }
    }

    return NO;
}
```


# 参考文章

[AFNetworking 源码阅读](https://honglu.me/2016/01/11/AFNetworking%20源码阅读/)

[AFNetworking - 掘金文集](https://juejin.cn/tag/AFNetworking)

[iOS开发——AFNetworking源码（一）](https://blog.csdn.net/weixin_51638861/article/details/124933698?spm=1001.2014.3001.5501)

[iOS开发——AFNetworking源码（二）](https://blog.csdn.net/weixin_51638861/article/details/125053883)

[iOS-AFNetworking源码解读（一）](https://blog.csdn.net/Heyuan_Xie/article/details/107465152)

[AFNetworking(v3.1.0) 源码解析](https://juejin.cn/post/6844903718614204429)
