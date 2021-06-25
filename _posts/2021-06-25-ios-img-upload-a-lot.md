---
title: 处理上传图片太多导致内存崩溃的问题
author: Ouyang Rong
date: 2021-06-25 16:14:00 +0800
categories: [iOS, 多线程]
tags: [UIImage, 内存]
---

# 问题分析

批量上传图片，当图片多了的时候，内存崩溃了。

> Message from debugger: Terminated due to memory issue


# 解决方法

创建队列，用信号量，实现图片一张一张上传。

```
static SSTUploadHomeworkPictureManager *manager = nil;
static dispatch_queue_t _queueUploadBegin = nil; // 创建串行队列 - 保证多次图片上传请求按顺序执行；
static dispatch_semaphore_t _semaphoreBegin = nil;
static dispatch_queue_t _queueSubmitBegin = nil;
static dispatch_semaphore_t _semaphoreSubmitBegin = nil;
```

```
+ (instancetype)shareManager{
    return [[self alloc] init];
}

- (instancetype)init{
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        manager = [super init];
        _queueUploadBegin = dispatch_queue_create("com.uploadHomeworkImageToOSS.subsystem.tast", DISPATCH_QUEUE_SERIAL);
        _semaphoreBegin = dispatch_semaphore_create(1); // 设置信号总量为1，保证只有一个进程执行
        _queueSubmitBegin = dispatch_queue_create("com.submitHomeworkImageToOSS.subsystem.tast", DISPATCH_QUEUE_SERIAL);
        _semaphoreSubmitBegin = dispatch_semaphore_create(1);
    });
    return manager;
}
```

```
-(void)submitHomewrokPhoto:(NSArray<SSTEditTaskSujectFinishedPictureModel *> *)imageModels withVipId:(NSString *)vipId subject:(NSString*)subject {
    self.imageCount = imageModels.count;
    dispatch_async(_queueSubmitBegin, ^{
        dispatch_semaphore_wait(_semaphoreSubmitBegin, DISPATCH_TIME_FOREVER);
        NSMutableArray *uploadPictures = [NSMutableArray array];
        dispatch_queue_t queueUploadImage = dispatch_queue_create("com.submitImageModel.subsystem.tast", DISPATCH_QUEUE_SERIAL);
        dispatch_semaphore_t semaphoreImage = dispatch_semaphore_create(1); // 设置信号总量为1，保证只有一个进程执行；
        for (NSInteger i = 0; i < imageModels.count; i ++) {
            SSTEditTaskSujectFinishedPictureModel *editPicture = [imageModels objectAtIndexCheck:i];
            dispatch_async(queueUploadImage, ^{
                dispatch_semaphore_wait(semaphoreImage, DISPATCH_TIME_FOREVER);
                editPicture.correctStatus = SSTHomeworkPictureStateUploading;
                editPicture.isLocalData = YES;
                editPicture.vipId = vipId;
                editPicture.course = subject;
                [self saveUploadingHomewrokPhoto:editPicture withVipId:vipId subject:subject];
                [uploadPictures addObject:editPicture];
                dispatch_semaphore_signal(semaphoreImage);
                if (i == self.imageCount - 1) {
                    [self uploadImageModelArr:uploadPictures originalPhoto:YES complete:^(SSTEditTaskSujectFinishedPictureModel * _Nonnull imageModel, AliOSSUploadImageState state) {                        
                        dispatch_semaphore_signal(_semaphoreSubmitBegin);
                    }];
                }
            });
        }
    });
}
```

```
- (void)uploadImageModelArr:(NSArray<SSTEditTaskSujectFinishedPictureModel *> *)imageModelArr originalPhoto:(BOOL)originalPhoto complete:(void(^)(SSTEditTaskSujectFinishedPictureModel *imageModel, AliOSSUploadImageState state))complete {
    NSLog(@" =========== uploadImageModelArr ========= start--%@",[NSThread currentThread]);
    dispatch_async(_queueUploadBegin, ^{
        //等待信号量
        dispatch_semaphore_wait(_semaphoreBegin, DISPATCH_TIME_FOREVER);
        //网络请求上传图片数据
        [XWHttpClient xw_postWithUrlString:HTTP_upload_getOssfsToken Params:nil DefaultHUD:NO SuccessBlock:^(id returnValue) {
            NSLog(@"  ----- getOssfsToken - returnValue： %@",returnValue);
            NSLog(@" =========== HTTP_upload_getOssfsToken ========= start--%@",[NSThread currentThread]);
            OssfsTokenModel *ossfsTokenModel = [OssfsTokenModel mj_objectWithKeyValues:DicGetValue(returnValue,@"data")];
            id<OSSCredentialProvider> credential = [[OSSStsTokenCredentialProvider alloc] initWithAccessKeyId:ossfsTokenModel.accessKeyId secretKeyId:ossfsTokenModel.accessKeySecret securityToken:ossfsTokenModel.securityToken];
            OSSClient *client = [[OSSClient alloc] initWithEndpoint:ossfsTokenModel.endpoint credentialProvider:credential];
            OSSPutObjectRequest *put = [OSSPutObjectRequest new];
            put.bucketName = ossfsTokenModel.bucket;
            NSOperationQueue *queue = [[NSOperationQueue alloc] init];
            queue.maxConcurrentOperationCount = imageModelArr.count;

            //创建串行队列
            dispatch_queue_t queueUpload = dispatch_queue_create("com.uploadLocalPicture.subsystem.tast", DISPATCH_QUEUE_SERIAL);
            //设置信号总量为1，保证只有一个进程执行
            dispatch_semaphore_t semaphore = dispatch_semaphore_create(1);

            for (int i = 0; i < imageModelArr.count; i ++) {
                SSTEditTaskSujectFinishedPictureModel *imageModel = imageModelArr[i];
                imageModel.index = i;
                dispatch_async(queueUpload, ^{
                    //等待信号量
                    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);

                    //处理耗时操作的代码块...
                    dispatch_async(dispatch_get_global_queue(0, 0), ^{
                        UIImage *image = imageModel.localImage;
                        if (image) { // image
                            NSBlockOperation *operation = [NSBlockOperation blockOperationWithBlock:^{
                            NSData *data;
                            NSData *data1 = UIImageJPEGRepresentation(image, 0.5);
                            float length1 = [data1 length] / 1024;
                            if (length1 < 400) {
                                data = data1; //UIImageJPEGRepresentation(image, 1);
                            }else {
                                if (originalPhoto) {
                                    data = UIImageJPEGRepresentation(image, 0.5); // 原图
                                }else {
                                    data = UIImageJPEGRepresentation(image, 0.3); // 再压缩一下
                                }
                            }
                            NSString *imageName = [NSString stringWithFormat:@"/iOS/%@%d.jpg",[SSUtility getTransactionID],i];  //加“i”防止数组图片重名
                            //imageModel.localPath = [NSString stringWithFormat:@"%@%d.jpg",[SSUtility getTransactionID],i]; // 用于本地保存，如果上传失败的话；
                            put.objectKey = [imageName substringFromIndex:1];
                            NSTimeInterval endTime = [[NSDate date] timeIntervalSince1970]*1000;// *1000 是精确到毫秒，不乘就是精确到秒
                            NSInteger uploadTime = endTime;
                            imageModel.derverFileId = imageModel.derverFileId.length?imageModel.derverFileId:[NSString stringWithFormat:@"%@-%zd",imageModel.vipId,uploadTime];
                            put.uploadingData = data;
                            put.uploadProgress = ^(int64_t bytesSent, int64_t totalByteSent, int64_t totalBytesExpectedToSend) {
                             NSLog(@" -- 这是第 %d 张图片 %@ 在上传--- bytesSent %lld, - totalByteSent %lld, - totalBytesExpectedToSend %lld", i,imageName,bytesSent, totalByteSent, totalBytesExpectedToSend);
                            };
                            NSString *paramBody = @"{\"vipId\":${x:vipId},\"courseName\":${x:courseName},\"derverFileId\":${x:derverFileId},\"fileKeys\":${x:fileKeys},\"questionRecommendRecordId\":${x:questionRecommendRecordId}}";
                            put.callbackParam = @{@"callbackUrl":[NSString stringWithFormat:@"%@%@?accessToken=%@",kUPLOAD_ADDRESS,HTTP_End_Path(HTTP_LibraryTeacher,@"uploadPicture"),[SSUtility getTeacherToken]],
                                                 @"callbackBody":paramBody,
                                             @"callbackBodyType":@"application/json"
                                                }; // library/V2
                            put.callbackVar = @{@"x:vipId":imageModel.vipId,
                                           @"x:courseName":imageModel.course,
                                             @"x:fileKeys":imageName,
                                         @"x:derverFileId":imageModel.derverFileId,
                            @"x:questionRecommendRecordId":imageModel.questionRecommendRecordId.length?imageModel.questionRecommendRecordId:@""};
                            OSSTask *putTask = [client putObject:put];
                            [putTask waitUntilFinished]; // 阻塞直到上传完成
                            [putTask continueWithBlock:^id(OSSTask *task) {
                                OSSPutObjectResult *result = (OSSPutObjectResult *)task.result;
                                NSLog(@"Result - requestId: %@,\n headerFields: %@,\n servercallback: %@",
                                            result.requestId,
                                            result.httpResponseHeaderFields,
                                            result.serverReturnJsonString);
                                NSDictionary *dataDict = [SSUtility dictionaryWithJsonString:result.serverReturnJsonString];
                                NSString *codeStr = dataDict[@"code"];
                                NSString *msgStr = dataDict[@"msg"];

                                // 还要从后台返回数据判断是否上服务器成功
                                if ([codeStr isEqualToString:@"999"]) {
                                    NSLog(@"upload object success!");
                                    // 删除上传中
                                    [[SSTUploadHomeworkPictureManager shareManager] deleteUploadingPhoto:imageModel withVipId:imageModel.vipId subject:imageModel.course];
                                    if (complete) {
                                        complete(imageModel ,AliOSSUploadImageSuccess);
                                    }
                                }else {
                                    NSLog(@"请求服务器失败：%@",msgStr.length?msgStr:task.error);
                                    dispatch_async(dispatch_get_main_queue(), ^{
                                        [[SSCustomAlertView alloc] setAlertViewTitle:@"" andMessage:msgStr ? msgStr : @"作业上传失败" andhideAlertViewTimeOut:kDefaultAlertTime];
                                    });
                                    imageModel.correctStatus = SSTHomeworkPictureStateUploadFail;
                                    [[SSTUploadHomeworkPictureManager shareManager] saveUploadFailurePhoto:imageModel withVipId:imageModel.vipId subject:imageModel.course];
                                    [[SSTUploadHomeworkPictureManager shareManager] deleteUploadingPhoto:imageModel withVipId:imageModel.vipId subject:imageModel.course];
                                    if (complete) {
                                        complete(imageModel ,AliOSSUploadImageFailed);
                                    }
                                }

                                dispatch_semaphore_signal(semaphore);
                                //最后一张上传完了，这个请求结束了；
                                if (imageModel == imageModelArr.lastObject) { //要是按顺序来的才能这么判断；
                                    NSLog(@" --- 网络请求上传图片数据 --- upload object finished!");
                                    dispatch_semaphore_signal(_semaphoreBegin);
                                }

                                task = [client presignPublicURLWithBucketName:ossfsTokenModel.bucket withObjectKey:put.objectKey];
                                return nil;
                            }];

                            }];

                            if (queue.operations.count != 0) {
                                [operation addDependency:queue.operations.lastObject];
                            }
                            [queue addOperation:operation];

                        }else { //没有图片，让线程继续执行；当做是失败；
                            imageModel.correctStatus = SSTHomeworkPictureStateUploadFail;
                            [[SSTUploadHomeworkPictureManager shareManager] saveUploadFailurePhoto:imageModel withVipId:imageModel.vipId subject:imageModel.course];
                            [[SSTUploadHomeworkPictureManager shareManager] deleteUploadingPhoto:imageModel withVipId:imageModel.vipId subject:imageModel.course];
                            dispatch_semaphore_signal(semaphore);
                            if (complete) {
                                 complete(imageModel ,AliOSSUploadImageFailed);
                            }
                        }

                    }); // 子线程操作

                }); // 等待信号量

            } // 遍历图片

            [queue waitUntilAllOperationsAreFinished];

        } ErrorBlock:^(id errorCode) {
            dispatch_semaphore_signal(_semaphoreBegin);
            for (SSTEditTaskSujectFinishedPictureModel *pictureImageModel in imageModelArr) { // 上传中的作业置为上传失败
                pictureImageModel.correctStatus = SSTHomeworkPictureStateUploadFail;
                [[SSTUploadHomeworkPictureManager shareManager] saveUploadFailurePhoto:pictureImageModel withVipId:pictureImageModel.vipId subject:pictureImageModel.course];
                [[SSTUploadHomeworkPictureManager shareManager] deleteUploadingPhoto:pictureImageModel withVipId:pictureImageModel.vipId subject:pictureImageModel.course];
                if (complete) {
                    complete(pictureImageModel ,AliOSSUploadImageFailed);
                }
            }
        } FailureBlock:^(id failureInfo) {
            dispatch_semaphore_signal(_semaphoreBegin);
            for (SSTEditTaskSujectFinishedPictureModel *pictureImageModel in imageModelArr) { // 上传中的作业置为上传失败
                pictureImageModel.correctStatus = SSTHomeworkPictureStateUploadFail;
                [[SSTUploadHomeworkPictureManager shareManager] saveUploadFailurePhoto:pictureImageModel withVipId:pictureImageModel.vipId subject:pictureImageModel.course];
                [[SSTUploadHomeworkPictureManager shareManager] deleteUploadingPhoto:pictureImageModel withVipId:pictureImageModel.vipId subject:pictureImageModel.course];
                if (complete) {
                    complete(pictureImageModel ,AliOSSUploadImageFailed);
                }
            }
        }];
    }); // 等待信号量

}
```


# 错误示范

这种方法开辟子线程太多了，十分消耗内存，也会造成内存崩溃。

```
dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
    dispatch_async(queue, ^{
        NSMutableArray *uploadPictures = [NSMutableArray array];
        dispatch_group_t group = dispatch_group_create();
        for (SSTEditTaskSujectFinishedPictureModel *editPicture in imageModels) {
            dispatch_group_async(group, queue, ^{
                editPicture.correctStatus = SSTHomeworkPictureStateUploading;
                editPicture.isLocalData = YES;
                editPicture.vipId = vipId;
                editPicture.course = subject;
                NSLog(@" -- 上传 保存 作业 图片 当前线程 -- %@",[NSThread currentThread]);
                [self saveUploadingHomewrokPhoto:editPicture withVipId:vipId subject:subject];
                [uploadPictures addObject:editPicture];
            });
        }
        dispatch_group_wait(group, DISPATCH_TIME_FOREVER);
        dispatch_group_notify(group, queue, ^{
            if (uploadPictures.count > 0) {
                [self uploadImageModelArr:uploadPictures originalPhoto:YES complete:^(SSTEditTaskSujectFinishedPictureModel * _Nonnull imageModel, AliOSSUploadImageState state) {
                    SSLog(@" --- 作业上传 --- 完成 --- ");
                }];
            }
        });
    });
```


# 其他方法

![作业图片1](https://tva1.sinaimg.cn/large/008i3skNgy1gruny0r7atj30u00znwj0.jpg)

![作业图片2](https://tva1.sinaimg.cn/large/008i3skNgy1grunycb38aj60u01h3k0102.jpg)

![作业图片3](https://tva1.sinaimg.cn/large/008i3skNgy1grunyk1yo5j30u01a27ar.jpg)

![作业图片4](https://tva1.sinaimg.cn/large/008i3skNgy1grunz8u60wj30xc02cjrd.jpg)
