---
title: iOS SDWebImage 源码分析
author: Ouyang Rong
date: 2022-09-21 19:37:00 +0800
categories: [iOS, 源码学习]
tags: [图片, SDWebImage, 多线程]
---


# 类的介绍（SDWebImage 3.8.1）

- NSData+ImageContentType  通过 Image data 判断当前图片的格式

- SDImageCache  缓存，定义了 Disk 和 memory 二级缓存（NSCache）负责管理 cache 单例

- SDWebImageCompat  保证不同平台/版本/屏幕等兼容性的宏定义和内联图片缩放

- SDWebImageDecoder  图片解压缩，内部只有一个接口

- SDWebImageDownloader  单例，异步图片下载管理，管理下载队列，管理 operation，管理网络请求，处理结果和异常，存放网络请求回调的 block，数据结构大概是 `{"url":[{"progress":"progressBlock"},{"complete":"completeBlock"}]}`

- SDWebImageDownloaderOperation  实现了异步下载图片的 NSOperation，网络请求给予 NSURLSession 代理下载，自定义的 Operation 任务对象，需要手动实现 `start` `cancel` 等方法

- SDWebImageManager  单例，核心管理类，主要对缓存管理 + 下载管理进行了封装，主要接口 `downloadImageWithURL`

- SDWebImageOperation  operation 协议，只定义了 cancel operation 这一接口

- SDWebImagePrefetcher  低优先级情况下预先下载图片，对 SDWebImageViewManager 进行简单封装

- MKAnnotationView+WebCache  为 MKAnnotationView 异步加载图片

- UIButton+WebCache  为 UIButton 异步加载图片

- UIImage+GIF  将 Image data 转换成指定格式图片

- UIImage+MultiFormat  将 image data 转换成指定格式图片

- UIImageView+HighlightedWebCache  为 UIImageView 异步加载图片

- UIImageView+WebCache  为 UIImageView 异步加载图片

- UIView+WebCacheOperation  保存当前 MKAnnotationView / UIButton / UIImageView 异步下载图片的 operations


# 核心类调用代码逻辑

## 第一步（外部控件）

直接调用 SDWebImage 设置网络图片的公开方法


```
    __weak typeof(self) weakSelf = self;
    [self.imageView sd_setImageWithURL:[NSURL URLWithString:@"http://cdn.duitang.com/uploads/item/201111/08/20111108113800_wYcvP.thumb.600_0.jpg"] placeholderImage:nil completed:^(UIImage *image, NSError *error, SDImageCacheType cacheType, NSURL *imageURL) {

        if (image && cacheType == SDImageCacheTypeNone)
        {
            weakSelf.imageView.alpha = 0;
            [UIView animateWithDuration:1.0f animations:^{
                weakSelf.imageView.alpha = 1.f;
            }];
        }
        else
        {
            weakSelf.imageView.alpha = 1.0f;
        }

    }];
```

## 第二步（UIImageView + WebCache）

```
// 以上所有的调用方法，最终都是进入这个方法进行图片的加载
// url 加载的图片
// placeholder 占位图
// options 下载图片的各种花式设置。一般使用的是 SDWebImageRetryFailed | SDWebImageLowPriority。
- (void)sd_setImageWithURL:(NSURL *)url placeholderImage:(UIImage *)placeholder options:(SDWebImageOptions)options progress:(SDWebImageDownloaderProgressBlock)progressBlock completed:(SDWebImageCompletionBlock)completedBlock {
    // 取消当前的下载操作。如果不取消，那么当tableView滑动的时候，当前cell的imageView会一直去下载图片，然后优先显示下载完成的图片，直接错乱
    [self sd_cancelCurrentImageLoad];
    {......省略一段代码}
    // 判断是否存在
    if (url) {
        {......省略一段代码}
        __weak __typeof(self) wself = self;
        // 关键类 SDWebImageManager 来处理图片下载
        // 下载有三层：1.当前manager调用下载；2.从缓存中获取，hit失败用SDWebImageDownloader对象调用下载；3.用继承于NSOperation的SDWebImageDownloaderOperation对象里NSURLSession的下载图片代理里面进行操作
        id <SDWebImageOperation> operation = [SDWebImageManager.sharedManager downloadImageWithURL:url options:options progress:progressBlock completed:^(UIImage *image, NSError *error, SDImageCacheType cacheType, BOOL finished, NSURL *imageURL) {
            [wself removeActivityIndicator];
            if (!wself) return;
            dispatch_main_sync_safe(^{
                if (!wself) return;
                // 设置了SDWebImageAvoidAutoSetImage 默认不会将UIImage添加进UIImageView对象里面，而放置在conpleteBlock里面交由调用方自己处理，做个滤镜或者淡入淡出什么的
                if (image && (options & SDWebImageAvoidAutoSetImage) && completedBlock)
                {
                    completedBlock(image, error, cacheType, url);
                    return;
                }
                else if (image) {
                    wself.image = image;
                    [wself setNeedsLayout];
                } else {
                    if ((options & SDWebImageDelayPlaceholder)) {
                        wself.image = placeholder;
                        [wself setNeedsLayout];
                    }
                }
                // 这里是最终回调出去的block
                if (completedBlock && finished) {
                    completedBlock(image, error, cacheType, url);
                }
            });
        }];
        // 保存本次operation，如果发生多次图片请求可以用来取消
        // 先取消当前UIImageView正在下载的任务，然后在保存operations
        // 也就是说当动态绑定的字典里面的key value对应一个图片下载，单个图片value数组就是0，不然就是多个，下载完就会根据key移除（？）
        [self sd_setImageLoadOperation:operation forKey:@"UIImageViewImageLoad"];
    } else {
        dispatch_main_async_safe(^{
            [self removeActivityIndicator];
            if (completedBlock) {
                NSError *error = [NSError errorWithDomain:SDWebImageErrorDomain code:-1 userInfo:@{NSLocalizedDescriptionKey : @"Trying to load a nil url"}];
                completedBlock(nil, error, SDImageCacheTypeNone, url);
            }
        });
    }
}
```

这里首先会调用 `sd_cancelCurrentImageLoad` 方法，为什么会这样呢？

例如：一个 imageView 请求了两张图片 —— 1.png 和 2.png，但我们只希望显示 2.png，所以需要取消 1.png 的请求。原因有两点：
1. 在异步请求中（先后顺序不定），有可能 1.png 会在 2.png 后面获取到，会覆盖掉 2.png
2. 减少网络请求，网络请求是一个很耗时的操作

## 第三步（SDWebImageManager）

这一步的重点就是会启用 SDWebImageManager 管理单例，调用这个方法进行网络请求：

```
- (id <SDWebImageOperation>)downloadImageWithURL:(NSURL *)url
                                         options:(SDWebImageOptions)options
                                        progress:(SDWebImageDownloaderProgressBlock)progressBlock
                                       completed:(SDWebImageCompletionWithFinishedBlock)completedBlock

```

这个管理类有两个得力的手下

一个是 SDImageCache 专门管理缓存

- NSCache 负责内存缓存，用法和 NSDictionary 基本一样
- 磁盘缓存用 NSFileManager 写文件的方式完成

> 注：
> 1. NSCache 具有自动删除的功能，以减少系统占用的内存，还能设置内存临界值
> 2. NSCache 是线程安全的，不需要加线程锁
> 3. 键对象不会像 NSMutableDictionary 中那样被复制（键不需要实现 NSCopying 协议）

```
// 从imageCache中寻找图片
// 每次向SDWebImageCache索取图片的时候，会先根据图片URL对应的key值先检查内存中是否有对应的图片。如果有则直接返回；如果没有则在ioQueue中去硬盘中查找。其中文件名是是根据URL生成的MD5值，找到之后先将图片缓存在内存中，然后再把图片返回。
- (NSOperation *)queryDiskCacheForKey:(NSString *)key done:(SDWebImageQueryCompletedBlock)doneBlock {
    if (!doneBlock) {
        return nil;
    }

    if (!key) {
        doneBlock(nil, SDImageCacheTypeNone);
        return nil;
    }

    // First check the in-memory cache...
    // 1. 先去内存层面查找
    UIImage *image = [self imageFromMemoryCacheForKey:key];
    if (image) {
        doneBlock(image, SDImageCacheTypeMemory);
        return nil;
    }

    // 如果在内存没找到
    // 2. 如果内存中没有，则在磁盘中查找。如果找到，则将其放到内存缓存，并调用doneBlock回调
    NSOperation *operation = [NSOperation new];
    dispatch_async(self.ioQueue, ^{
        if (operation.isCancelled) {
            return;
        }
    // 创建自动释放池，内存即时释放
    // 如果你的应用程序或者线程是要长期运行的并且有可能产生大量autoreleased对象, 你应该使用autorelease pool blocks
        @autoreleasepool {
            // 从硬盘拿，拿到了根据字段存入内存
            UIImage *diskImage = [self diskImageForKey:key];
            if (diskImage && self.shouldCacheImagesInMemory) {
                // 像素
                NSUInteger cost = SDCacheCostForImage(diskImage);
                // 缓存到NSCache中
                [self.memCache setObject:diskImage forKey:key cost:cost];
            }

            dispatch_async(dispatch_get_main_queue(), ^{
                doneBlock(diskImage, SDImageCacheTypeDisk);
            });
        }
    });

    return operation;
}
```

**知识点**：

这里开了异步串行队列去 Disk 中查找，保证不阻塞主线程，而且开了 autorelease pool 以降低内存暴涨问题，能得到及时释放，如果能取到，首先缓存到内存中然后再回调。

如果内存和磁盘中都取不到图片，就会让 SDWebImageManager 的另一个手下 SDWebImageDownloader 去下载图片。

这货也是一个单例，专门负责图片的下载，下载操作都是放在 NSOperationQueue 中完成的。

```
// 下载图片的最终方法实现
- (id <SDWebImageOperation>)downloadImageWithURL:(NSURL *)url
                                         options:(SDWebImageOptions)options
                                        progress:(SDWebImageDownloaderProgressBlock)progressBlock
                                       completed:(SDWebImageCompletionWithFinishedBlock)completedBlock {
    {......}
    // 根据URL生成对应的key  没有特殊处理为[self absoluteString]
    NSString *key = [self cacheKeyForURL:url];

    // 前面的操作主要作了如下处理：
    // 1. 判断url的合法性
    // 2. 创建SDWebImageCombinedOperation对象
    // 3. 查看url是否是之前下载失败过的
    // 去imageCache中寻找图片
    operation.cacheOperation = [self.imageCache queryDiskCacheForKey:key done:^(UIImage *image, SDImageCacheType cacheType) {
        if (operation.isCancelled) {
            @synchronized (self.runningOperations) {
                [self.runningOperations removeObject:operation];
            }
            return;
        }
        // 如果图片没有找到或者是SDWebImageRefreshCached就从网络上下载图片
        if ((!image || options & SDWebImageRefreshCached) && (![self.delegate respondsToSelector:@selector(imageManager:shouldDownloadImageForURL:)] || [self.delegate imageManager:self shouldDownloadImageForURL:url])) {
            if (image && options & SDWebImageRefreshCached) {
                dispatch_main_sync_safe(^{
                    // 如果图片存在cache中，但是options还是SDWebImageRefreshCached 通知cache去重新刷新缓存图片
                    completedBlock(image, nil, cacheType, YES, url);
                });
            }
            // 设置下载选项属性
            {......}
            // 开启下载
            // 这里的两个回调都是从DownloaderOperation里面出来的，progressBlock是不要取到的，直接在最外层调用的地方处理，完成的话需要进行cache，因此要在这里处理回调，处理完再回调出去
            id <SDWebImageOperation> subOperation = [self.imageDownloader downloadImageWithURL:url options:downloaderOptions progress:progressBlock completed:^(UIImage *downloadedImage, NSData *data, NSError *error, BOOL finished) {
                // 上面的是weak的这里设置成strong 避免被释放掉了
                __strong __typeof(weakOperation) strongOperation = weakOperation;
                if (!strongOperation || strongOperation.isCancelled) {
                    // Do nothing if the operation was cancelled
                    // See #699 for more details
                    // if we would call the completedBlock, there could be a race condition between this block and another completedBlock for the same object, so if this one is called second, we will overwrite the new data
                }
                else if (error) {
                    // 如果出错，则调用完成回调，并将url放入下载挫败url数组中
                    dispatch_main_sync_safe(^{
                        if (strongOperation && !strongOperation.isCancelled) {
                            completedBlock(nil, error, SDImageCacheTypeNone, finished, url);
                        }
                    });
                    if (error.code != NSURLErrorNotConnectedToInternet
                        && error.code != NSURLErrorCancelled
                        && error.code != NSURLErrorTimedOut
                        && error.code != NSURLErrorInternationalRoamingOff
                        && error.code != NSURLErrorDataNotAllowed
                        && error.code != NSURLErrorCannotFindHost
                        && error.code != NSURLErrorCannotConnectToHost) {
                        @synchronized (self.failedURLs) {
                            [self.failedURLs addObject:url];
                        }
                    }
                }
                else {
                    // 当重新下载的时候能获取到了，那么久把他从之前的failURL里面移除
                    if ((options & SDWebImageRetryFailed)) {
                        @synchronized (self.failedURLs) {
                            [self.failedURLs removeObject:url];
                        }
                    }
                    // 是否硬盘缓存
                    BOOL cacheOnDisk = !(options & SDWebImageCacheMemoryOnly);
                    if (options & SDWebImageRefreshCached && image && !downloadedImage) {
                        // Image refresh hit the NSURLCache cache, do not call the completion block
                    }
                    else if (downloadedImage && (!downloadedImage.images || (options & SDWebImageTransformAnimatedImage)) && [self.delegate respondsToSelector:@selector(imageManager:transformDownloadedImage:withURL:)]) {
                        // 在全局队列中并行处理图片的缓存
                        // 首先对图片做个转换操作，该操作是代理对象实现的
                        // 然后对图片做缓存处理
                        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_HIGH, 0), ^{
                            UIImage *transformedImage = [self.delegate imageManager:self transformDownloadedImage:downloadedImage withURL:url];
                            if (transformedImage && finished) {
                                BOOL imageWasTransformed = ![transformedImage isEqual:downloadedImage];
                                // 二级缓存起来
                                [self.imageCache storeImage:transformedImage recalculateFromImage:imageWasTransformed imageData:(imageWasTransformed ? nil : data) forKey:key toDisk:cacheOnDisk];
                            }
                            dispatch_main_sync_safe(^{
                                if (strongOperation && !strongOperation.isCancelled) {
                                    completedBlock(transformedImage, nil, SDImageCacheTypeNone, finished, url);
                                }
                            });
                        });
                    }
                    else {
                        // 下载完成后之后，先cache起来 内存缓存和磁盘缓存都要考虑
                        if (downloadedImage && finished) {
                            [self.imageCache storeImage:downloadedImage recalculateFromImage:NO imageData:data forKey:key toDisk:cacheOnDisk];
                        }
                        dispatch_main_sync_safe(^{
                            if (strongOperation && !strongOperation.isCancelled) {
                                completedBlock(downloadedImage, nil, SDImageCacheTypeNone, finished, url);
                            }
                        });
                    }
                }
                // 完成之后也要移除掉
                if (finished) {
                    @synchronized (self.runningOperations) {
                        if (strongOperation) {
                            [self.runningOperations removeObject:strongOperation];
                        }
                    }
                }
            }];
            operation.cancelBlock = ^{
                [subOperation cancel];
                @synchronized (self.runningOperations) {
                    __strong __typeof(weakOperation) strongOperation = weakOperation;
                    if (strongOperation) {
                        [self.runningOperations removeObject:strongOperation];
                    }
                }
            };
        }
        else if (image) {
            // 如果图片存在，直接返回
            dispatch_main_sync_safe(^{
                __strong __typeof(weakOperation) strongOperation = weakOperation;
                if (strongOperation && !strongOperation.isCancelled) {
                    completedBlock(image, nil, cacheType, YES, url);
                }
            });
            @synchronized (self.runningOperations) {
                [self.runningOperations removeObject:operation];
            }
        }
        else {
            // 如果没有cacahe，而且没实现代理下载，直接返回nil
            // Image not in cache and download disallowed by delegate
            dispatch_main_sync_safe(^{
                __strong __typeof(weakOperation) strongOperation = weakOperation;
                if (strongOperation && !weakOperation.isCancelled) {
                    completedBlock(nil, nil, SDImageCacheTypeNone, YES, url);
                }
            });
            // 移除
            @synchronized (self.runningOperations) {
                [self.runningOperations removeObject:operation];
            }
        }
    }];
    return operation;
}
```

## 第四步（SDWebImageDownloader）

```
- (id <SDWebImageOperation>)downloadImageWithURL:(NSURL *)url options:(SDWebImageDownloaderOptions)options progress:(SDWebImageDownloaderProgressBlock)progressBlock completed:(SDWebImageDownloaderCompletedBlock)completedBlock {
    __block SDWebImageDownloaderOperation *operation;
    __weak __typeof(self) wself = self;
    // 290行，同一个方法里面，进行urlCallBacks的组装
    // 该方法有点明白了，就是让同一个url值生成一个createCallBack --> 也就是只出来一个operation任务
    // wself.downloadQueue同一url只会加入一次，但是多次重复请求，urlcallbacks的url数组里面会有多个回调block，这个不影响，只要正真下载一次就好了，回调可以遍历，下面下载完都一直在遍历，没错，这就对了
    [self addProgressCallback:progressBlock completedBlock:completedBlock forURL:url createCallback:^{
        NSTimeInterval timeoutInterval = wself.downloadTimeout;
        if (timeoutInterval == 0.0) {
            timeoutInterval = 15.0;
        }
        // In order to prevent from potential duplicate caching (NSURLCache + SDImageCache) we disable the cache for image requests if told otherwise
        // 防止NSURLCache和SDImageCache重复缓存 如果没有明确告知需要缓存，则禁用图片请求的缓存操作
        // 1. 创建请求对象，并根据options参数设置其属性
        NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url cachePolicy:(options & SDWebImageDownloaderUseNSURLCache ? NSURLRequestUseProtocolCachePolicy : NSURLRequestReloadIgnoringLocalCacheData) timeoutInterval:timeoutInterval];
        request.HTTPShouldHandleCookies = (options & SDWebImageDownloaderHandleCookies);
        request.HTTPShouldUsePipelining = YES;
        // 设置http头部
        if (wself.headersFilter) {
            request.allHTTPHeaderFields = wself.headersFilter(url, [wself.HTTPHeaders copy]);
        }
        else {
            request.allHTTPHeaderFields = wself.HTTPHeaders;
        }
        // SDWebImageDownloaderOperation派生自NSOperation，负责图片下载工作
        // 2. 创建SDWebImageDownloaderOperation操作对象，并进行配置
        // SDWebImageDownloaderOperation class
        operation = [[wself.operationClass alloc] initWithRequest:request
                                                        inSession:self.session
                                                          options:options
                                                         progress:^(NSInteger receivedSize, NSInteger expectedSize) {
                                                             SDWebImageDownloader *sself = wself;
                                                             if (!sself) return;
                                                             __block NSArray *callbacksForURL;
                                                             // 3. 从管理器的callbacksForURL中找出该URL所有的进度处理回调并调用
                                                             // 这个barrierQueue是并发的，如果是get main queue的话就死锁了
                                                             // 我个人感觉去掉直接写也问题不大，不知道为什么这么写？？？反正是顺序执行
                                                             dispatch_sync(sself.barrierQueue, ^{
                                                                 // URLCallbacks是mutale字典对象
                                                                 callbacksForURL = [sself.URLCallbacks[url] copy];
                                                             });
                                                             // 进度正常，肯定有多个block
                                                             for (NSDictionary *callbacks in callbacksForURL) {
                                                                 dispatch_async(dispatch_get_main_queue(), ^{
                                                                     SDWebImageDownloaderProgressBlock callback = callbacks[kProgressCallbackKey];
                                                                     // 正在下载的时候回传已经收到的size和totalsize出去
                                                                     if (callback) callback(receivedSize, expectedSize);
                                                                 });
                                                             }
                                                         }
                                                        // 下载完之后会进到这个回调，然后我们用之前存起来的回调再回调出去
                                                        completed:^(UIImage *image, NSData *data, NSError *error, BOOL finished) {
                                                            SDWebImageDownloader *sself = wself;
                                                            if (!sself) return;
                                                            __block NSArray *callbacksForURL;
                                                            // 4. 从管理器的callbacksForURL中找出该URL所有的完成处理回调并调用，
                                                            // 如果finished为YES，则将该url对应的回调信息从URLCallbacks中删除
                                                            // 个人理解阻塞当前线程，而且barrierQueue也阻塞 那么当同一个URL完成的时候直接没了对象，重复下载也没用了
                                                            dispatch_barrier_sync(sself.barrierQueue, ^{
                                                                callbacksForURL = [sself.URLCallbacks[url] copy];
                                                                if (finished) {
                                                                    [sself.URLCallbacks removeObjectForKey:url];
                                                                }
                                                            });
                                                            // 这里一般只有一个，但是多次重复请求
                                                            for (NSDictionary *callbacks in callbacksForURL) {
                                                                SDWebImageDownloaderCompletedBlock callback = callbacks[kCompletedCallbackKey];
                                                                if (callback) callback(image, data, error, finished);
                                                            }
                                                        }
                                                        cancelled:^{
                                                            SDWebImageDownloader *sself = wself;
                                                            // 5. 取消操作将该url对应的回调信息从URLCallbacks中删除
                                                            // 阻塞barrierqueue
                                                            if (!sself) return;
                                                            dispatch_barrier_async(sself.barrierQueue, ^{
                                                                [sself.URLCallbacks removeObjectForKey:url];
                                                            });
                                                        }];
        // 是否需要解码
        operation.shouldDecompressImages = wself.shouldDecompressImages;
        if (wself.urlCredential) {
            operation.credential = wself.urlCredential;
        } else if (wself.username && wself.password) {
            operation.credential = [NSURLCredential credentialWithUser:wself.username password:wself.password persistence:NSURLCredentialPersistenceForSession];
        }
        if (options & SDWebImageDownloaderHighPriority) {
            operation.queuePriority = NSOperationQueuePriorityHigh;
        } else if (options & SDWebImageDownloaderLowPriority) {
            operation.queuePriority = NSOperationQueuePriorityLow;
        }
        // NSOperation Queue 增加一个对象
        // 6. 设置依赖
        // [operation2 addDependency:operation1];      任务二依赖任务一
        // [operation3 addDependency:operation2];      任务三依赖任务二
        // 7. 将操作加入到操作队列downloadQueue中
        [wself.downloadQueue addOperation:operation];
        // 如果不是FIFO 是 LIFO 队列设置依赖，后进来的成为上面的依赖
        if (wself.executionOrder == SDWebImageDownloaderLIFOExecutionOrder) {
            // Emulate LIFO execution order by systematically adding new operations as last operation's dependency
            // FIFO的话正常数组就问题
            // LIFO的话让之前的操作一次依赖最后一次进来的操作就行了
            [wself.lastAddedOperation addDependency:operation];
            wself.lastAddedOperation = operation;
        }
    }];
    return operation;
}
```

```
- (void)addProgressCallback:(SDWebImageDownloaderProgressBlock)progressBlock completedBlock:(SDWebImageDownloaderCompletedBlock)completedBlock forURL:(NSURL *)url createCallback:(SDWebImageNoParamsBlock)createCallback {
    // The URL will be used as the key to the callbacks dictionary so it cannot be nil. If it is nil immediately call the completed block with no image or data.
    if (url == nil) {
        if (completedBlock != nil) {
            completedBlock(nil, nil, nil, NO);
        }
        return;
    }
    // 1. 以dispatch_barrier_sync操作来保证同一时间只有一个线程能对URLCallbacks进行操作
    // 该属性是一个字典，key是图片的URL地址，value则是一个数组，包含每个图片的多组回调信息。由于我们允许多个图片同时下载，因此可能会有多个线程同时操作URLCallbacks属性。为了保证URLCallbacks操作(添加、删除)的线程安全性，SDWebImageDownloader将这些操作作为一个个任务放到barrierQueue队列中，并设置屏障来确保同一时间只有一个线程操作URLCallbacks属性
    // 这个写法阻塞当前线程  而且阻塞barrierQueue队列
    // 这句话表示每个URL下载只会出来一次creatBlock回调出去创建新的任务operation（最终要添加到queue的任务）
    dispatch_barrier_sync(self.barrierQueue, ^{
        BOOL first = NO;
        if (!self.URLCallbacks[url]) {
            // 当第一次进来下载的时候，我们平时外部都是传个completeblock，所以我们的urlcallbacks结构是{"url":[{"comolete":"completeBlock"}]}
            // 如果是多次重复下载同一URL图片，结构应该会变成
            // {"url":[{"comolete":"completeBlock"},{"comolete":"completeBlock"},{"comolete":"completeBlock"},{"comolete":"completeBlock"}]}
            self.URLCallbacks[url] = [NSMutableArray new];
            first = YES;
        }
        // Handle single download of simultaneous download request for the same URL
        // 2. 处理同一URL的同步下载请求的单个下载
        NSMutableArray *callbacksForURL = self.URLCallbacks[url];
        NSMutableDictionary *callbacks = [NSMutableDictionary new];
        if (progressBlock) callbacks[kProgressCallbackKey] = [progressBlock copy];
        if (completedBlock) callbacks[kCompletedCallbackKey] = [completedBlock copy];
        [callbacksForURL addObject:callbacks];
        self.URLCallbacks[url] = callbacksForURL;
        // 如果是第一次，那么回调出去下载
        if (first) {
            createCallback();
        }
    });
}
```

**知识点**：

1. 通过调用 `addProgressCallback:completeBlock:forURL:createBlock:` 来确保同一 `url` 只会下载一次

2. 通过继承 `NSOperation` 的 `SDWebImageDownloaderOperation` 进来初始化下载任务，这里的回调就是上面方法里面数据结构存储起来的所有回调的遍历执行
`progressBlock`，`completeBlock` 和 `cancelBlock` 都用到了 GCD  的 `barrier` 的方法，有时间慢慢再看看原理，先看基本介绍。

```
// 所有下载操作的网络响应序列化处理是放在一个自定义的并行调度队列中来处理的
// _barrierQueue = dispatch_queue_create("com.hackemist.SDWebImageDownloaderBarrierQueue", DISPATCH_QUEUE_CONCURRENT);

@property (SDDispatchQueueSetterSementics,nonatomic)dispatch_queue_t barrierQueue;

// func dispatch_barrier_async(_ queue: dispatch_queue_t, _ block: dispatch_block_t):

// 这个方法重点是你传入的 queue，当你传入的 queue 是通过 DISPATCH_QUEUE_CONCURRENT 参数自己创建的 queue 时，这个方法会阻塞这个 queue（注意是阻塞 queue，而不是阻塞当前线程），一直等到这个 queue 中排在它前面的任务都执行完成后才会开始执行自己，自己执行完毕后，再会取消阻塞，使这个 queue 中排在它后面的任务继续执行。

// 如果你传入的是其他的 queue，那么它就和 dispatch_async 一样了。

// func dispatch_barrier_sync(_ queue: dispatch_queue_t, _ block: dispatch_block_t):

// 这个方法的使用和上一个一样，传入自定义的并发队列（DISPATCH_QUEUE_CONCURRENT），它和上一个方法一样的阻塞 queue，不同的是这个方法还会阻塞当前线程。

// 如果你传入的是其他的 queue，那么它就和 dispatch_sync 一样了。
```

3. 把 `createBlock` 里面的网络请求任务加入 `NSOperationQueue` 队列中，该队列有两个属性。

```
// 执行的下载顺序
typedef NS_ENUM(NSInteger, SDWebImageDownloaderExecutionOrder) {
    /**
     * Default value. All download operations will execute in queue style (first-in-first-out).
     * 默认是FIFO   以队列的方式，按照先进先出的顺序下载。这是默认的下载顺序
     */
    SDWebImageDownloaderFIFOExecutionOrder,
    /**
     * All download operations will execute in stack style (last-in-first-out).
     * 以栈的方式，按照后进先出的顺序下载。
     */
    SDWebImageDownloaderLIFOExecutionOrder
};
```

GCD 不能很好的设置依赖关系，而 NSOperation 能很好的实现，关键代码让上一次的任务依赖于最后进来的任务，就能实现LIFO。

```
[wself.lastAddedOperationaddDependency:operation];
```

## 第五步（SDWebImageDownloaderOperation）

这个类是继承 NSOperation 的，并且采用了 SDWebImageOperation 的代理（只有 `cancel` 方法），并且它只暴露了 `initWithRequest:inSession:options:progress:completed:canceled` 这个初始化方法来配置。

由于他是自定义的，那么就必须重写 `start` 方法，在该方法里面 SDWebImage 已经把 NSURLConnection 替换成了 NSURLSession 来进行网络请求的操作，简言之，只要实现 NSURLSession 的代理方法就能获取到下载数据。

这里主要看下一个不断接受 data 的代理回调：

```
- (void)URLSession:(NSURLSession *)session dataTask:(NSURLSessionDataTask *)dataTask didReceiveData:(NSData *)data {
    // 这个方法本身就已经是异步了
    // 2016-10-20 16:49:40.260 SDWebImageAnalyze[7098:374046] 我正在接受数据<NSThread: 0x608000260140>{number = 3, name = (null)}
    // 2016-10-20 16:49:40.261 SDWebImageAnalyze[7098:374032] 我正在接受数据<NSThread: 0x600000265980>{number = 5, name = (null)}
    // 2016-10-20 16:49:40.261 SDWebImageAnalyze[7098:374029] 我正在接受数据<NSThread: 0x600000077580>{number = 6, name = (null)}
    // 1. 附加数据
    [self.imageData appendData:data];
    if ((self.options & SDWebImageDownloaderProgressiveDownload) && self.expectedSize > 0 && self.completedBlock) {
        // The following code is from http://www.cocoaintheshell.com/2011/05/progressive-images-download-imageio/
        // Thanks to the author @Nyx0uf
        // Get the total bytes downloaded
        // 2. 获取已下载数据总大小
        const NSInteger totalSize = self.imageData.length;
        // Update the data source, we must pass ALL the data, not just the new bytes
        // 3. 更新数据源，我们需要传入所有数据，而不仅仅是新数据
        CGImageSourceRef imageSource = CGImageSourceCreateWithData((__bridge CFDataRef)self.imageData, NULL);
        // 4. 首次获取到数据时，从这些数据中获取图片的长、宽、方向属性值
        if (width + height == 0) {
            CFDictionaryRef properties = CGImageSourceCopyPropertiesAtIndex(imageSource, 0, NULL);
            if (properties) {
                NSInteger orientationValue = -1;
                CFTypeRef val = CFDictionaryGetValue(properties, kCGImagePropertyPixelHeight);
                if (val) CFNumberGetValue(val, kCFNumberLongType, &height);
                val = CFDictionaryGetValue(properties, kCGImagePropertyPixelWidth);
                if (val) CFNumberGetValue(val, kCFNumberLongType, &width);
                val = CFDictionaryGetValue(properties, kCGImagePropertyOrientation);
                if (val) CFNumberGetValue(val, kCFNumberNSIntegerType, &orientationValue);
                CFRelease(properties);
                // When we draw to Core Graphics, we lose orientation information,
                // which means the image below born of initWithCGIImage will be
                // oriented incorrectly sometimes. (Unlike the image born of initWithData
                // in didCompleteWithError.) So save it here and pass it on later.
                // 5. 当绘制到Core Graphics时，我们会丢失方向信息，这意味着有时候由initWithCGIImage创建的图片的方向会不对，所以在这边我们先保存这个信息并在后面使用。
                orientation = [[self class] orientationFromPropertyValue:(orientationValue == -1 ? 1 : orientationValue)];
            }
        }
        // 6. 图片还未下载完成
        if (width + height > 0 && totalSize < self.expectedSize) {
            // Create the image
            // 7. 使用现有的数据创建图片对象，如果数据中存有多张图片，则取第一张
            CGImageRef partialImageRef = CGImageSourceCreateImageAtIndex(imageSource, 0, NULL);
#ifdef TARGET_OS_IPHONE
            // Workaround for iOS anamorphic image
            // 8. 适用于iOS变形图像的解决方案。我的理解是由于iOS只支持RGB颜色空间，所以在此对下载下来的图片做个颜色空间转换处理。
            if (partialImageRef) {
                const size_t partialHeight = CGImageGetHeight(partialImageRef);
                CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
                CGContextRef bmContext = CGBitmapContextCreate(NULL, width, height, 8, width * 4, colorSpace, kCGBitmapByteOrderDefault | kCGImageAlphaPremultipliedFirst);
                CGColorSpaceRelease(colorSpace);
                if (bmContext) {
                    CGContextDrawImage(bmContext, (CGRect){.origin.x = 0.0f, .origin.y = 0.0f, .size.width = width, .size.height = partialHeight}, partialImageRef);
                    CGImageRelease(partialImageRef);
                    partialImageRef = CGBitmapContextCreateImage(bmContext);
                    CGContextRelease(bmContext);
                }
                else {
                    CGImageRelease(partialImageRef);
                    partialImageRef = nil;
                }
            }
#endif
             // 9. 对图片进行缩放、解码操作
            if (partialImageRef) {
                UIImage *image = [UIImage imageWithCGImage:partialImageRef scale:1 orientation:orientation];
                NSString *key = [[SDWebImageManager sharedManager] cacheKeyForURL:self.request.URL];
                UIImage *scaledImage = [self scaledImageForKey:key image:image];
                if (self.shouldDecompressImages) {
                    image = [UIImage decodedImageWithImage:scaledImage];
                }
                else {
                    image = scaledImage;
                }
                CGImageRelease(partialImageRef);
                dispatch_main_sync_safe(^{
                    if (self.completedBlock) {
                        self.completedBlock(image, nil, nil, NO);
                    }
                });
            }
        }
        CFRelease(imageSource);
    }
    if (self.progressBlock) {
        self.progressBlock(self.imageData.length, self.expectedSize);
    }
}
```

**SDWebImageDecoder**

把请求回来的数据或者缓存到本地的图片资源都进行了异步解压缩。

**图片解压缩的原理**：

1. 假设我们使用 `+imageWithContentsOfFile:` 方法从磁盘中加载一张图片，这个时候的图片并没有解压缩；
2. 然后将生成的 `UIImage` 赋值给 `UIImageView`；
3. 接着一个隐式的 `CATransaction` 捕获到了 `UIImageView` 图层树的变化；
4. 在主线程的下一个 `run loop` 到来时，`Core Animation` 提交了这个隐式的 `transaction`，这个过程可能会对图片进行 `copy` 操作，而受图片是否字节对齐等因素的影响，这个 `copy` 操作可能会涉及以下部分或全部步骤：
    - 分配内存缓冲区用于管理文件 `IO` 和解压缩操作；
    - 将文件数据从磁盘读到内存中；
    - 将压缩的图片数据解码成未压缩的位图形式，这是一个非常耗时的 `CPU` 操作；
    - 最后 `Core Animation` 使用未压缩的位图数据渲染 `UIImageView` 的图层。

> 在上面的步骤中，我们提到了图片的解压缩是一个非常耗时的 CPU 操作，并且它默认是在主线程中执行的。那么当需要加载的图片比较多时，就会对我们应用的响应性造成严重的影响，尤其是在快速滑动的列表上，这个问题会表现得更加突出。
>

**图片解压缩的原因**：

1. 首先PNG和JPEG都是图片的压缩格式。PNG是无损压缩，支持alpha，而JPEG是有损压缩，可选1-100压缩比例

2. 例如你有一张PNG的图片20B，那么你对应的图片二进制数据也是20B的，解压缩后的图片就可能是几百几千B了

3. 具体计算公式就是 `像素宽*像素高*每个像素对应的字节`

4. 那么当你进行图片渲染的时候，必须得到解压缩后的原始像素数据，才能进行图形渲染

在 `SDWebImageDecoder` 这个文件中进行了强制解压缩，我们赋值给 `imageView` 的时候已经是解压缩的文件了，因此不会卡主主线程，不然默认是在主线程进行解压缩。

## 第六步（回调到SDWebImageManager存储图片，完成最终回调）

```
// 内存缓存或者磁盘缓存
- (void)storeImage:(UIImage *)image recalculateFromImage:(BOOL)recalculate imageData:(NSData *)imageData forKey:(NSString *)key toDisk:(BOOL)toDisk {
    if (!image || !key) {
        return;
    }
    // 内存缓存有必要的话
    if (self.shouldCacheImagesInMemory) {
        NSUInteger cost = SDCacheCostForImage(image);
        // 1. 内存缓存，将其存入NSCache中，同时传入图片的消耗值
        [self.memCache setObject:image forKey:key cost:cost];
    }
    // 硬盘缓存
    if (toDisk) {
        // 异步串行队列写入
        // 2. 如果确定需要磁盘缓存，则将缓存操作作为一个任务放入ioQueue中
        dispatch_async(self.ioQueue, ^{
            NSData *data = imageData;
            if (image && (recalculate || !data)) {
#if TARGET_OS_IPHONE
                // We need to determine if the image is a PNG or a JPEG
                // PNGs are easier to detect because they have a unique signature (http://www.w3.org/TR/PNG-Structure.html)
                // The first eight bytes of a PNG file always contain the following (decimal) values:
                // 137 80 78 71 13 10 26 10
                // If the imageData is nil (i.e. if trying to save a UIImage directly or the image was transformed on download)
                // and the image has an alpha channel, we will consider it PNG to avoid losing the transparency
                int alphaInfo = CGImageGetAlphaInfo(image.CGImage);
                BOOL hasAlpha = !(alphaInfo == kCGImageAlphaNone ||
                                  alphaInfo == kCGImageAlphaNoneSkipFirst ||
                                  alphaInfo == kCGImageAlphaNoneSkipLast);
                // 判断图片格式
                // 3. 需要确定图片是PNG还是JPEG。PNG图片容易检测，因为有一个唯一签名。PNG图像的前8个字节总是包含以下值：137 80 78 71 13 10 26 10
                // 在imageData为nil的情况下假定图像为PNG。我们将其当作PNG以避免丢失透明度。而当有图片数据时，我们检测其前缀，确定图片的类型
                BOOL imageIsPng = hasAlpha;
                // But if we have an image data, we will look at the preffix
                // 查看imagedata的的前缀是否是png的
                if ([imageData length] >= [kPNGSignatureData length]) {
                    imageIsPng = ImageDataHasPNGPreffix(imageData);
                }
                if (imageIsPng) {
                    data = UIImagePNGRepresentation(image);
                }
                else {
                    data = UIImageJPEGRepresentation(image, (CGFloat)1.0);
                }
#else
                data = [NSBitmapImageRep representationOfImageRepsInArray:image.representations usingType: NSJPEGFileType properties:nil];
#endif
            }
            [self storeImageDataToDisk:data forKey:key];
        });
    }
}
```

我们来看看磁盘缓存：

```
// 硬盘缓存方法
- (void)storeImageDataToDisk:(NSData *)imageData forKey:(NSString *)key {
    if (!imageData) {
        return;
    }
    // 是否根据路径存在文件，不存在就创建
    // 创建缓存文件并存储图片
    // 根据library/caches/default/com.hackemist.SDWebImageCache.default创建了文件夹
    if (![_fileManager fileExistsAtPath:_diskCachePath]) {
        [_fileManager createDirectoryAtPath:_diskCachePath withIntermediateDirectories:YES attributes:nil error:NULL];
    }
    // get cache Path for image key
    // /Users/mkjing/Library/Developer/CoreSimulator/Devices/7A62E354-CB88-4012-A119-7B64089B7171/data/Containers/Data/Application/E5275526-CD16-499D-B731-6D68938C04FB/Library/Caches/default/com.hackemist.SDWebImageCache.default
    // 该路径下面拼接图片的url路径
    // key是经过MD5加密的字符串
    NSString *cachePathForKey = [self defaultCachePathForKey:key];
    // transform to NSUrl
    NSURL *fileURL = [NSURL fileURLWithPath:cachePathForKey];
    // 保存文件到指定路径中
    // library/caches/default/com.hackemist.SDWebImageCache.default/文件名
    [_fileManager createFileAtPath:cachePathForKey contents:imageData attributes:nil];
    // disable iCloud backup
    if (self.shouldDisableiCloud) {
        [fileURL setResourceValue:[NSNumber numberWithBool:YES] forKey:NSURLIsExcludedFromBackupKey error:nil];
    }
}
```

## 第七步（SDWebImageCache的清理缓存策略）

在初始化的时候注册了几个通知：

```
        // 收到内存警告，清楚NSCache [self.memCache removeAllObject]
        [[NSNotificationCenter defaultCenter] addObserver:self
                                                 selector:@selector(clearMemory)
                                                     name:UIApplicationDidReceiveMemoryWarningNotification
                                                   object:nil];
        // 程序关闭时对硬盘文件做一些处理
        [[NSNotificationCenter defaultCenter] addObserver:self
                                                 selector:@selector(cleanDisk)
                                                     name:UIApplicationWillTerminateNotification
                                                   object:nil];
        // 程序进入后台是也对硬盘进行一些读写
        [[NSNotificationCenter defaultCenter] addObserver:self
                                                 selector:@selector(backgroundCleanDisk)
                                                     name:UIApplicationDidEnterBackgroundNotification
                                                   object:nil];
```

1. 当收到内存警告时，直接调用 NSCache 的 `removeAllObject` 的方法来清理 MemeryCache

2. 当程序退出时或进入后台，根据缓存策略来清理磁盘缓存

```
// 当程序退出或者推到后台的时候，会有缓存策略管理
// 接收到程序进入后台或者程序退出通知
// 调用该方法，然后先遍历所有缓存文件，记录过期的文件，计算缓存总文件大小
// 先删除过期的文件（默认一周）
// 如果设置最大缓存，而且已经缓存的文件大小超过这个预期值，把所有的文件按最后编辑的时间升序，然后一个个删除，当缓存低于临界就break
- (void)cleanDiskWithCompletionBlock:(SDWebImageNoParamsBlock)completionBlock {
    dispatch_async(self.ioQueue, ^{
        // diskCachePath
        // /Users/mkjing/Library/Developer/CoreSimulator/Devices/7A62E354-CB88-4012-A119-7B64089B7171/data/Containers/Data/Application/E5275526-CD16-499D-B731-6D68938C04FB/Library/Caches/default/com.hackemist.SDWebImageCache.default
        NSURL *diskCacheURL = [NSURL fileURLWithPath:self.diskCachePath isDirectory:YES];
        // 需要获取的属性列表 是否文件夹  最后一次编辑时间和文件大小（如有压缩，就是压缩后的）
        NSArray *resourceKeys = @[NSURLIsDirectoryKey, NSURLContentModificationDateKey, NSURLTotalFileAllocatedSizeKey];
        // This enumerator prefetches useful properties for our cache files.
        // 1. 该枚举器预先获取缓存文件的有用的属性 （根据存储的文件夹获取所有文件的枚举器）
        NSDirectoryEnumerator *fileEnumerator = [_fileManager enumeratorAtURL:diskCacheURL
                                                   includingPropertiesForKeys:resourceKeys
                                                                      options:NSDirectoryEnumerationSkipsHiddenFiles
                                                                 errorHandler:NULL];
        // 当前时间  2016-10-21 02:46:41 +0000
        // expirationDate  2016-10-14 02:46:11 +0000
        NSDate *expirationDate = [NSDate dateWithTimeIntervalSinceNow:-self.maxCacheAge];
        NSMutableDictionary *cacheFiles = [NSMutableDictionary dictionary];
        NSUInteger currentCacheSize = 0;
        // Enumerate all of the files in the cache directory.  This loop has two purposes:
        //
        //  1. Removing files that are older than the expiration date.
        //  2. Storing file attributes for the size-based cleanup pass.
        //  2. 枚举缓存文件夹中所有文件，该迭代有两个目的：移除比过期日期更老的文件；存储文件属性以备后面执行基于缓存大小的清理操作
        NSMutableArray *urlsToDelete = [[NSMutableArray alloc] init];
        for (NSURL *fileURL in fileEnumerator) {
            // 根据resourceKeys和路径获取到遍历文件的数据字典
            NSDictionary *resourceValues = [fileURL resourceValuesForKeys:resourceKeys error:NULL];
            // Skip directories.
            // 3. 跳过文件夹
            if ([resourceValues[NSURLIsDirectoryKey] boolValue]) {
                continue;
            }
            // Remove files that are older than the expiration date;
            // 4. 移除早于有效期的老文件 （根据最后一次编辑时间属性来判断）
            NSDate *modificationDate = resourceValues[NSURLContentModificationDateKey];// 获取文件编辑时间
            // 返回晚一点的date 如果是experiationDate ，说明该文件是要删除的
            if ([[modificationDate laterDate:expirationDate] isEqualToDate:expirationDate]) {
                [urlsToDelete addObject:fileURL];
                continue;
            }
            // Store a reference to this file and account for its total size.
            // 5. 存储文件的引用并计算所有文件的总大小，以备后用
            NSNumber *totalAllocatedSize = resourceValues[NSURLTotalFileAllocatedSizeKey];
            currentCacheSize += [totalAllocatedSize unsignedIntegerValue];
            // 把所有的文件都装进cachefile里面 根据fileURL定位
            [cacheFiles setObject:resourceValues forKey:fileURL];
        }
        // 移除过期的先
        for (NSURL *fileURL in urlsToDelete) {
            [_fileManager removeItemAtURL:fileURL error:nil];
        }
        // If our remaining disk cache exceeds a configured maximum size, perform a second
        // size-based cleanup pass.  We delete the oldest files first.
        // 6. 如果磁盘缓存的大小大于我们配置的最大大小，则执行基于文件大小的清理，我们首先删除最老的文件
        if (self.maxCacheSize > 0 && currentCacheSize > self.maxCacheSize) {
            // Target half of our maximum cache size for this cleanup pass.
            // 7. 以设置的最大缓存大小的一半作为清理目标
            const NSUInteger desiredCacheSize = self.maxCacheSize / 2;
            // Sort the remaining cache files by their last modification time (oldest first).
            // 从小到大排序，也就是最早的时间在最前面 升序// 8. 按照最后修改时间来排序剩下的缓存文件
            NSArray *sortedFiles = [cacheFiles keysSortedByValueWithOptions:NSSortConcurrent
                                                            usingComparator:^NSComparisonResult(id obj1, id obj2) {
                                                                return [obj1[NSURLContentModificationDateKey] compare:obj2[NSURLContentModificationDateKey]];
                                                            }];

            // Delete files until we fall below our desired cache size.
            // 9. 删除文件，直到缓存总大小降到我们期望的大小
            for (NSURL *fileURL in sortedFiles) {
                // 由于之前过期的一部分已经移除了，但是都加进了cacheFile里面，如果不能移除，我们已经过期删除了，直接跳过进行下一个
                // 移除成功，那么计算cacheFile大小
                if ([_fileManager removeItemAtURL:fileURL error:nil]) {
                    NSDictionary *resourceValues = cacheFiles[fileURL];
                    NSNumber *totalAllocatedSize = resourceValues[NSURLTotalFileAllocatedSizeKey];
                    currentCacheSize -= [totalAllocatedSize unsignedIntegerValue];
                    // 降到期望值以下就可以停了
                    if (currentCacheSize < desiredCacheSize) {
                        break;
                    }
                }
            }
        }
        if (completionBlock) {
            dispatch_async(dispatch_get_main_queue(), ^{
                completionBlock();
            });
        }
    });
}
```

3. 穿插一个clearDisk的方法，这个就不是什么策略了，直接是完全清掉磁盘缓存 clear 和 clean的区别吧

```
// 清理磁盘（完全清理）
// clear清理是通过删除路径文件夹，然后再创建的方式进行
- (void)clearDiskOnCompletion:(SDWebImageNoParamsBlock)completion
{
    // 异步自定义串行队列
    dispatch_async(self.ioQueue, ^{
        // 直接把文件夹移除
        [_fileManager removeItemAtPath:self.diskCachePath error:nil];
        [_fileManager createDirectoryAtPath:self.diskCachePath
                withIntermediateDirectories:YES
                                 attributes:nil
                                      error:NULL];
        if (completion) {
            dispatch_async(dispatch_get_main_queue(), ^{
                completion();
            });
        }
    });
}
```


# 知识点整理

1. 这里的 `Dispatch_barrier_async` 来确保线程安全操作，任务需要等待之前的任务执行完

2. 强大的 Block 回调和 Associated Objects — runtime

3. NSOperationQueue 和 NSOperation的特点，能取消操作，也能设置任务之间的依赖，相较于 GCD 来说更加的强大，AF 也是基于这个玩的，这样才可以完成 LIFO 的队列需求

4. NSCache 和 NSFileManager 的二级缓存操作

5. 缓存策略：默认超过一星期的清理掉，还能设置最大缓存数，根据文件的最后编辑时间进行升序，然后一个个删除，当低于临界的时候清理完成

6. 异步操作图片的处理，缩放和解压操作，还有图片的类型处理

7. 还有就是同一 URL 不会被多次下载的优化处理

8. 最后还是觉得封装和任务的分配都非常的清晰，值得学习


# 总结

1. 入口 UIImageView 调用方法 `sd_setImageWithURL: placeholderImage: options: progress:completed:` ，无论你调用哪个，最终都转换成该方法处理 url

2. 必须先删除该控件之前的下载任务，`sd_cancelCurrentImageLoad` 原因是当你网络不快的情况下，例如你一个屏幕能展示三个 cell，第一个 cell 由于网络问题不能立刻下完，那么用户就滑动了 tableView，第一个 cell 进去复用池，第五个出来的 cell 从复用池子拿，由于之前的下载还在，本来是应该显示第五个图片，但是 SDWebImage 的默认做法是立马把下载好的图片给 UIImageView，所以这时候会图片数据错乱的BUG

3. 有 placeHolder 先展示，然后启用 SDWebImageManager 单例 `downloadImageWithURLoptions:progress:completed:` 来处理图片下载

4. 先判断 url 的合法性，再创建 SDwebImageCombinedOperation 的 cache 任务对象，再查看 url 是否之前下载失败过，最后如果 url 为nil，则直接返回操作对象完成回调，如果都正常，那么就调用 SDWebImageManager 中的管理缓存类 SDImageCache 单例的方法 `queryDiskCacheForKey:done:` 查看是否有缓存

5. SDImageCache 内存缓存用的是 NSCache，Disk 缓存用的是 NSFileManager 的文件写入操作，那么查看缓存的时候是先去内存查找，这里的 key 都是经过 MD5 之后的字串，找到直接回调，没找到继续去磁盘查找，开异步串行队列去找，避免卡死主线程，启用 autoreleasepool 避免内存暴涨，查到了缓存到内存，然后回调

6. 如果都没找到，就调用 SDWebImageManager 中的管理下载类 SDWebImageDownloader 单例的方法 `downloadImageWithURL:options:progress:completed:completedBlock` 处理下载

7. 下载前调用 `addProgressCallback:completedBlock:forURL:createCallback:` 来保证统一 url 只会生成一个网络下载对象，多余的都只会用 URLCallbacks 存储传入的进度 Block 或者 CompleteBlock，因此下载结果返回的时候会进行遍历回调

8. 下载用 NSOperation 和 NSOperationQueue 来进行，SDwebImage 派生了一个 SDWebImageDownloaderOperation 负责图片的下载任务，调用 `initWithRequest:inSession:options:progress:completed:cancelled:`

9. 把返回的 SDWebImageDownloaderOperation 对象 add 到 NSOperationQueue，FIFO 队列就正常，如果是 LIFO 队列，就需要设置依赖，这也是 GCD 和 NSOperation 的区别，也是 NSOperation 的优点，让上一次的任务依赖于本次任务 `[wself.lastAddedOperationaddDependency:operation]`

10. 下载任务开始是用 NSURLSession 了，不用 NSURLConnetion 了，由于 SDwebImage 是自定义的 NSOperation 内部需要重写 start 方法，在该方法里面配置 Session，当 taskResume 的时候，根据设置的代理就能取到不同的回调参数 `didReceiveResponse` 能获取到响应的所有参数规格，例如总 size，`didReceiveData` 是一步步获取data，压缩解码回调 progressBlock, `didCompleteWithError` 全部完成回调，图片解码，回调 `completeBlock`

11. 图片的解码是在 SDWebImageDecoder 里面完成的，缩放操作是在 SDWebImageCompat 内完成的，代理方法里面本身就已经是异步了，而且解码操作加入了 `autoreleasepool` 减少内存峰值

12. 当在 SDWebImageDownloaderOperation 中 NSURLSession 完成下载之后或者中途回调到 SDWebImageDownloader 中，然后再回调到 SDWebImageManager，在 Manager 中二级缓存 image，然后继续回调出去到 UIImage + WebCache 中，最后把 Image 回调出去，在调用的控件中展示出来

13. SDImageCache 初始化的时候注册了几个通知，当内存警告的时候，程序进入后台或者程序杀死的时候根据策略清理缓存。内存警告：自动清除 NSCache 内存缓存；进入后台和程序杀死：清理过期的文件（默认一周），然后有个缓存期望值，对比已有文件的大小，先根据文件最后编辑时间升序排，把大于期望值大小的文件全部删掉

14. SDWebImagePrefetcher 这货还提供了预先下载图片


# 文章参考

[iOS 源码解析：SDWeblmage（上）](https://www.jianshu.com/p/4cfcbe27eb2e)

[iOS SDWebImage 实现机制及源码分析](https://blog.csdn.net/m0_52192682/article/details/124277172)

[iOS SDWebImage 源码学习](https://blog.csdn.net/weixin_52192405/article/details/124227144)

[iOS SDWebImage 优质源码解读笔记](https://blog.csdn.net/deft_mkjing/article/details/52900586)

[SDWebImage 实现分析](http://southpeak.github.io/2015/02/07/sourcecode-sdwebimage/)
