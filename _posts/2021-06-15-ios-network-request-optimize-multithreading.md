---
title: 多线程 - 重复网络请求优化
author: Ouyang Rong
date: 2021-06-15 16:14:00 +0800
categories: [iOS, 网络]
tags: [AFNetworking]
---

# 问题分析

一个页面，可以通过点击不同的模块获取相应的数据。但是，当用户频繁点击的时候，有的模块网络请求数据返回会比较慢，这个时候返回的数据就会覆盖当前模块的数据。

# 解决方法

## 加锁处理

切换模块时，会对同一个API进行多次请求，但因为调用的接口都是一样的，所以最好就是加上锁，防止重复请求造成网络资源浪费。

```
 @synchronized (self) {//加锁，避免数组重复创建添加等问题
         static NSMutableArray * successBlocks;//用数组保存回调
         static NSMutableArray * failureBlocks;
         static dispatch_once_t onceToken;
         dispatch_once(&onceToken, ^{//仅创建一次数组
            successBlocks = [NSMutableArray new];
            failureBlocks = [NSMutableArray new];
         });
         if (success) {//每调用一次此函数，就把回调加进数组中
            [successBlocks addObject:success];
         }
         if (failure) {
            [failureBlocks addObject:failure];
         }

         static BOOL isProcessing = NO;
         if (isProcessing == YES) {//如果已经在请求了，就不再发出新的请求
            return;
         }
         isProcessing = YES;
         [self callerPostTransactionId:transactionId parameters:dic showActivityIndicator:showActivityIndicator showErrorAlterView:showErrorAlterView success:^(id responseObject) {
            @synchronized (self) {//网络请求的回调也要加锁，这里是另一个线程了
               for (successBlock eachSuccess in successBlocks) {//遍历回调数组，把结果发给每个调用者
                  eachSuccess(responseObject);
               }
               [successBlocks removeAllObjects];
               [failureBlocks removeAllObjects];
               isProcessing = NO;
            }
         } failure:^(id data) {
            @synchronized (self) {
               for (failureBlock eachFailure in failureBlocks) {
                  eachFailure(data);
               }
               [successBlocks removeAllObjects];
               [failureBlocks removeAllObjects];
               isProcessing = NO;
            }
         }];
      }
```

## 取消请求

取消全部请求：

```
[manager.operationQueue cancelAllOperations];
```

取消单个请求，以post请求为例：

```
AFHTTPRequestOperation *post =[manager POST:nil parameters:nil success:^(AFHTTPRequestOperation *operation, id responseObject) {
    //doing something
} failure:^(AFHTTPRequestOperation *operation, NSError *error) {
    // error handling.
}];
//Cancel operation
[post cancel];
```

AFNetworking取消正在进行的网络请求：

```
//单例模式
+ (HttpManager *)sharedManager
{
  static dispatch_once_t once;
  dispatch_once(&once, ^{
    httpManager = [[HttpManager alloc] init];
  });
  return httpManager;
}

//网络类初始化
- (id)init{
  self = [super init];
  if(self)
  {
    manager = [AFHTTPSessionManager manager];
    manager.requestSerializer = [AFJSONRequestSerializer serializer];
    manager.responseSerializer = [AFHTTPResponseSerializer serializer];
  }
  return self;
}
```

```
[[HttpManager sharedManager] dataFromWithBaseURL:BaseURL path:url method:@"POST" timeInterval:10 params:parmas success:^(NSURLRequest *request, NSURLResponse *response, id JSON) {

} failure:^(NSURLRequest *request, NSURLResponse *response, NSError *error, id JSON) {

} error:^(id JSON) {

} finish:^(id JSON) {

}];
```

取消正在进行的网络请求

```
- (void)cancelRequest
{
  if ([manager.tasks count] > 0) {
    NSLog(@"返回时取消网络请求");
    [manager.tasks makeObjectsPerformSelector:@selector(cancel)];
    //NSLog(@"tasks = %@",manager.tasks);
  }
}

```

同一个请求多次请求时，短时间忽略相同的请求

> 当进行刷新操作时，如果在请求还没有返回之前，一直在刷新操作，不管是狂点还是乱点。那么第一个请求发出后，短时间内可以不进行重复请求。

同一个请求多次请求时，取消之前发出的请求

> 如果是在搜索操作，那么每次输入关键字的时候，之前发出的请求可以取消，仅仅显示最后的请求结果。
> 采用的方法为创建一个BaseViewModel，所有的请求操作继承BaseViewModel，在发起请求之前进行一次判断。

```
#pragma mark - 忽略请求

/** 忽略请求，当请求的url和参数都是一样的时候，在短时间内不发起再次请求， 默认3秒 */
- (BOOL)ignoreRequestWithUrl:(NSString *)url params:(NSDictionary *)params;

/** 忽略请求，当请求的url和参数都是一样的时候，在短时间内不发起再次请求 */
- (BOOL)ignoreRequestWithUrl:(NSString *)url params:(NSDictionary *)params timeInterval:(NSTimeInterval)timeInterval;


#pragma mark - 取消之前的请求

/** 取消之前的同一个url的网络请求
 *  在failure分支中，判断如果是取消操作，那么不做任何处理
 *  在success和failure分支中，都要调用clearTaskSessionWithUrl:方法，进行内存释放
 */
- (void)cancelLastTaskSessionWithUrl:(NSString *)url currentTaskSession:(NSURLSessionTask *)task;

/** 清除url绑定的sessionTask */
- (void)clearTaskSessionWithUrl:(NSString *)url;
```

```
@property (nonatomic, strong) NSMutableDictionary *requestTimeMDic;
@property (nonatomic, strong) NSMutableDictionary *cancelTaskMDic;

- (BOOL)ignoreRequestWithUrl:(NSString *)url params:(NSDictionary *)params
{
    return [self ignoreRequestWithUrl:url params:params timeInterval:kRequestTimeInterval];
}

- (BOOL)ignoreRequestWithUrl:(NSString *)url params:(NSDictionary *)params timeInterval:(NSTimeInterval)timeInterval
{
    NSString *requestStr = [NSString stringWithFormat:@"%@%@", url, [params uq_URLQueryString]];
    NSString *requestMD5 = [NSString md5:requestStr];
    NSTimeInterval nowTime = [[NSDate date] timeIntervalSince1970];
    NSNumber *lastTimeNum = [self.requestTimeMDic objectForKey:requestMD5];
    WS(weakSelf);
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(timeInterval * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        // 超过忽略时间后，将值清空
        [weakSelf.requestTimeMDic removeObjectForKey:requestMD5];
    });
    if (timeInterval < (nowTime - [lastTimeNum doubleValue])) {
        if (0.01 > [lastTimeNum doubleValue]) {
            [self.requestTimeMDic setObject:@(nowTime) forKey:requestMD5];
        }
        return NO;
    } else {
        return YES;
    }
}

- (void)cancelLastTaskSessionWithUrl:(NSString *)url currentTaskSession:(NSURLSessionTask *)task
{
    NSURLSessionTask *lastSessionTask = [self.cancelTaskMDic objectForKey:url];
    if (nil == lastSessionTask) {
        [self.cancelTaskMDic setObject:task forKey:url];
        return;
    }
    [lastSessionTask cancel];
}

- (void)clearTaskSessionWithUrl:(NSString *)url
{
    [self.cancelTaskMDic removeObjectForKey:url];
}


#pragma mark - Remove Unused Things


#pragma mark - Private Methods


#pragma mark - Getter Methods

- (NSMutableDictionary *)requestTimeMDic
{
    if (nil == _requestTimeMDic) {
        _requestTimeMDic = [[NSMutableDictionary alloc] initWithCapacity:5];
    }
    return _requestTimeMDic;
}

- (NSMutableDictionary *)cancelTaskMDic
{
    if (nil == _cancelTaskMDic) {
        _cancelTaskMDic = [[NSMutableDictionary alloc] initWithCapacity:5];
    }
    return _cancelTaskMDic;
}
```

## PGNetworkHelper

[PGNetworkHelper](https://github.com/xiaozhuxiong121/PGNetworkHelper ) - PINCache作为AFNetworking缓存层，将AFNetworking请求的数据缓存起来，支持取消当前网络请求，以及取消所有的网络请求，除了常用的Get，Post方法，也将上传图片以及下载文件进行了封装，同样支持同步请求，使用方法极其简单。


# 参考文章

[iOS基础深入补完计划--多线程(面试题)汇总](https://www.jianshu.com/p/3d430c25dd65)

[iOS多线程及GCD相关总结](https://www.ktanx.com/blog/p/4784)

[iOS开发-多线程GCD](http://zhangzr.cn/2018/03/21/iOS开发-多线程GCD/)

[iOS 多线程的使用与总结](https://seinf.mobi/2019/04/03/ios-gcd-understanding/)

[AFNetWorking源码解析](http://tbfungeek.github.io/2019/11/30/AFNetWorking源码解析/)

[iOS 多线程总结 - 线程安全](http://tbfungeek.github.io/2019/08/14/iOS-多线程总结-锁/)

[iOS之多线程漫谈](https://segmentfault.com/a/1190000023613543)

[iOS 网络请求优化之取消请求](https://blog.csdn.net/u010960265/article/details/82905867)

[探秘AFNetworking](https://www.jianshu.com/p/a5dc05d93ff3)

[iOS 网络(3)——YTKNetwork](http://chuquan.me/2019/08/20/ios-network-ytknetwork/)

[开源一个封装AFNetworking的网络框架 - SJNetwork](https://knightsj.github.io/2017/12/27/开源一个封装AFNetworking的网络框架-SJNetwork/)
