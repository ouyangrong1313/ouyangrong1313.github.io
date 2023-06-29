---
title: iOS开发-连续拍照异步按顺序批量上传图片
author: Ouyang Rong
date: 2023-06-29 13:38:00 +0800
categories: [iOS, 功能]
tags: [GCD, FMDB]
---

# 一、数据模型

```
@interface SSTEditTaskSujectFinishedPictureModel:NSObject

/**
 * 图片上传的日期
 */
@property (nonatomic,copy) NSString *uploadDate;

/**
 * 图片关联的科目
 */
@property (nonatomic,copy) NSString *course;

/**
 * 图片关联的学生
 */
@property (nonatomic,copy) NSString *vipId;

@property (nonatomic,copy) NSString *studentName;

/**
 * 图片id
 */
@property (nonatomic,copy) NSString *homeworkPictureId;

/**
 * 图片id 对比前后端的数据是否重复问题
 */
@property (nonatomic,copy) NSString *derverFileId;

@property (nonatomic,copy) NSString *timestampStr;

/**
 * 图片路径
 */
@property (nonatomic,copy) NSString *image;

@property (nonatomic,copy) NSString *originImageUrl;

@property (nonatomic,copy) NSString *originPictureUrl;

/**
 * 图片批注状态，0默认，1批注， 2补拍，3不全, 4模糊，5上传中(本地管理) ，6上传失败(本地管理) ，7未上传(本地管理)
 */
@property (nonatomic,assign) SSTHomeworkPictureState correctStatus;

/**
 * 图片的本地路径
*/
@property (nonatomic,copy) NSString *localPath;

/**
 * 本地上传的图片
*/
@property (nonatomic,strong) UIImage *localImage;

/**
 * 是否是本地 0:服务器 1：本地
 */
@property (nonatomic,assign)BOOL isLocalData;

/**
 * 序号
 */
@property (nonatomic,assign)int index;

/**
 * 推荐题目记录Id
 */
@property (nonatomic,copy) NSString *questionRecommendRecordId;

@end

```

# 二、本地数据管理

```
#import "DataBaseHelper.h"
#import "SSTEditTaskModel.h"
#define kHOMEWORKImage_TABLE_NAME @"HomeworkImageTable"

NS_ASSUME_NONNULL_BEGIN

@interface DataBaseHelper (ImageUpload)

/**
 *创建作业图片信息表
 */
-(void)creatHomeworkImageInfoTable;

/**
 *保存作业图片信息
 */
-(BOOL)saveHomeworkImageInfo:(SSTEditTaskSujectFinishedPictureModel *)imageModel;

/**
 * 获取所有的作业图片信息
 */
-(NSArray <SSTEditTaskSujectFinishedPictureModel *>*)getAllHomeworkImageModel;

/**
 * 删除作业图片信息
 */
-(BOOL)deleteHomeworkImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel;

-(BOOL)deleteHomeworkImageModelBeforeDate:(NSString *)date;

-(BOOL)updateImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel withImageModelKey:(NSString *)key andImageModelValue:(NSString *)value;

@end

NS_ASSUME_NONNULL_END

```

```
#import "DataBaseHelper+ImageUpload.h"

@implementation DataBaseHelper (ImageUpload)

-(NSArray *)obtainTaskImageInfoTableField {
    NSArray *array = @[@"uploadDate",@"vipId",@"studentName",@"course",@"derverFileId",@"localPath",@"correctStatus",@"timestampStr"];
    return array;
}

/**
 * 创建作业图片的表
 */
-(void)creatHomeworkImageInfoTable{
    [[DataBaseHelper sharedInstance] DatabaseWithDBName:kHOMEWORKImage_TABLE_NAME];
    NSDictionary *dict = @{@"uploadDate":@(DBdatatypeNSString),
                           @"vipId":@(DBdatatypeNSString),
                           @"studentName":@(DBdatatypeNSString),
                           @"course":@(DBdatatypeNSString),
                           @"derverFileId":@(DBdatatypeNSString),
                           @"localPath":@(DBdatatypeNSString),
                           @"timestampStr":@(DBdatatypeNSString),
                           @"correctStatus":@(DBdatatypeInteger)};
    [self createTable:kHOMEWORKImage_TABLE_NAME WithKey:dict];
}

/**
 *保存作业图片信息
 */
-(BOOL)saveHomeworkImageInfo:(SSTEditTaskSujectFinishedPictureModel *)imageModel {
    NSDictionary *dict = @{@"uploadDate":imageModel.uploadDate,
                           @"vipId":imageModel.vipId,
                           @"studentName":imageModel.studentName,
                           @"course":imageModel.course,
                           @"derverFileId":imageModel.derverFileId,
                           @"localPath":imageModel.localPath,
                           @"timestampStr":imageModel.timestampStr,
                           @"correctStatus":@(imageModel.correctStatus)};
    BOOL insert = [self insertInTable:kHOMEWORKImage_TABLE_NAME WithKey:dict];
    SSLog(@"%@-%@图片数据保存%@",imageModel.uploadDate,imageModel.studentName,insert?@"成功":@"失败");
    if (insert) {
        [self saveUploadHomewrokPhoto:imageModel];
    }
    return insert;
}

/**
 * 获取所有的作业图片信息
 */
-(NSArray <SSTEditTaskSujectFinishedPictureModel *>*)getAllHomeworkImageModel {
    NSMutableArray *tempArray = [[NSMutableArray alloc] init];
    NSDictionary *keyDict = @{@"uploadDate":@(DBdatatypeNSString),
                           @"vipId":@(DBdatatypeNSString),
                           @"studentName":@(DBdatatypeNSString),
                           @"course":@(DBdatatypeNSString),
                           @"derverFileId":@(DBdatatypeNSString),
                           @"localPath":@(DBdatatypeNSString),
                           @"timestampStr":@(DBdatatypeNSString),
                           @"correctStatus":@(DBdatatypeInteger)};
    tempArray = [self selectInTable:kHOMEWORKImage_TABLE_NAME WithKey:keyDict orderKey:@"timestampStr" orderModel:@"DESC"];
    NSMutableArray *nodeArr = [NSMutableArray array];
    for (NSDictionary *nodeDict in tempArray) {
        SSTEditTaskSujectFinishedPictureModel *voice = [[SSTEditTaskSujectFinishedPictureModel alloc] init];
        voice.vipId = [nodeDict objectForKey:@"vipId"];
        voice.uploadDate = [nodeDict objectForKey:@"uploadDate"];
        voice.studentName = [nodeDict objectForKey:@"studentName"];
        voice.course = [nodeDict objectForKey:@"course"];
        voice.derverFileId = [nodeDict objectForKey:@"derverFileId"];
        voice.localPath = [nodeDict objectForKey:@"localPath"];
        voice.correctStatus = [[nodeDict objectForKey:@"correctStatus"] integerValue];
        voice.localImage = [nodeDict objectForKey:@"localImage"];
        voice.timestampStr = [nodeDict objectForKey:@"timestampStr"];
        voice.localImage = [self getHomeworkImageWithModel:voice];
        [nodeArr addObject:voice];
    }
     return nodeArr;
}

-(NSArray <SSTEditTaskSujectFinishedPictureModel *>*)getAllHomeworkImageModelBeforeDate:(NSString *)beforeDate {
    NSMutableArray *tempArray = [[NSMutableArray alloc] init];
    NSDictionary *keyDict = @{@"uploadDate":@(DBdatatypeNSString),
                           @"vipId":@(DBdatatypeNSString),
                           @"studentName":@(DBdatatypeNSString),
                           @"course":@(DBdatatypeNSString),
                           @"derverFileId":@(DBdatatypeNSString),
                           @"localPath":@(DBdatatypeNSString),
                           @"timestampStr":@(DBdatatypeNSString),
                           @"correctStatus":@(DBdatatypeInteger)};
    NSString *selectQuery = [NSString stringWithFormat:@"SELECT * FROM %@ WHERE uploadDate < ?",kHOMEWORKImage_TABLE_NAME]; // 查询语句
    tempArray = [self selectInTable:kHOMEWORKImage_TABLE_NAME withKey:keyDict andQuery:selectQuery whereCondition:beforeDate];
    
    NSMutableArray *nodeArr = [NSMutableArray array];
    for (NSDictionary *nodeDict in tempArray) {
        SSTEditTaskSujectFinishedPictureModel *voice = [[SSTEditTaskSujectFinishedPictureModel alloc] init];
        voice.vipId = [nodeDict objectForKey:@"vipId"];
        voice.uploadDate = [nodeDict objectForKey:@"uploadDate"];
        voice.studentName = [nodeDict objectForKey:@"studentName"];
        voice.course = [nodeDict objectForKey:@"course"];
        voice.derverFileId = [nodeDict objectForKey:@"derverFileId"];
        voice.localPath = [nodeDict objectForKey:@"localPath"];
        voice.correctStatus = [[nodeDict objectForKey:@"correctStatus"] integerValue];
        voice.localImage = [nodeDict objectForKey:@"localImage"];
        voice.timestampStr = [nodeDict objectForKey:@"timestampStr"];
        voice.localImage = [self getHomeworkImageWithModel:voice];
        [nodeArr addObject:voice];
    }
     return nodeArr;
}

/**
 * 删除作业图片信息
 */
-(BOOL)deleteHomeworkImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel {
    BOOL isDelete = [self deleteInTable:kHOMEWORKImage_TABLE_NAME withConditonKey:@"derverFileId" andConditonValue:imageModel.derverFileId];
    if (isDelete) {
        [self deleteUploadPhoto:imageModel];
    }
    return isDelete;
}

-(BOOL)deleteHomeworkImageModelBeforeDate:(NSString *)date{
    BOOL isAllDelete = YES;
    NSArray *imgModelArr = [self getAllHomeworkImageModelBeforeDate:date];
    for (SSTEditTaskSujectFinishedPictureModel *pModel in imgModelArr) {
        BOOL isDelete = [self deleteHomeworkImageModel:pModel];
        if (!isDelete) {
            isAllDelete = NO;
        }
    }
    return isAllDelete;
}

-(BOOL)updateImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel withImageModelKey:(NSString *)key andImageModelValue:(NSString *)value{
    BOOL isUpdate = [self updateInTable:kHOMEWORKImage_TABLE_NAME columnName:key newValue:value whereCondition:@"derverFileId" andConditionValue:imageModel.derverFileId];
    return isUpdate;
}

-(void)saveUploadHomewrokPhoto:(SSTEditTaskSujectFinishedPictureModel *)uploadImage{
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        UIImage *image = uploadImage.localImage;
        // 本地沙盒目录 + CheckHomewor + [NSDate nowDate]
        NSString *imgPath = [SSUtility getUploadHomeworkPhotoDirectoryWithSubject:uploadImage.course withDate:uploadImage.uploadDate vipId:uploadImage.vipId];
        NSString *localImagePath = [imgPath stringByAppendingFormat:@"%@",uploadImage.localPath];
        // 将取得的图片写入本地的沙盒中，其中0.5表示压缩比例，1表示不压缩，数值越小压缩比例越大
        BOOL success = [UIImageJPEGRepresentation(image,1) writeToFile:localImagePath atomically:YES];
        if (success){
            NSLog(@"上传中的作业写入本地成功");
        }
    });
}

-(UIImage*)getHomeworkImageWithModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel {
    NSString *imgPath = [SSUtility getUploadHomeworkPhotoDirectoryWithSubject:imageModel.course withDate:imageModel.uploadDate vipId:imageModel.vipId];
    NSString *localImagePath = [imgPath stringByAppendingFormat:@"%@",imageModel.localPath];
    NSData *imgData = [NSData dataWithContentsOfFile:localImagePath];
    UIImage *img = [UIImage imageWithData:imgData];
    return img;
}

/**
 * 删除作业图片
*/
-(void)deleteUploadPhoto:(SSTEditTaskSujectFinishedPictureModel *)uploadImage{
    // 本地沙盒目录 + CheckHomewor + [NSDate nowDate]
    NSString *imgPath = [SSUtility getUploadHomeworkPhotoDirectoryWithSubject:uploadImage.course withDate:uploadImage.uploadDate vipId:uploadImage.vipId];
    NSString *localImagePath = [imgPath stringByAppendingFormat:@"%@",uploadImage.localPath];
    if ([[NSFileManager defaultManager] removeItemAtPath:localImagePath error:nil]) {
        NSLog(@" --- 删除成功 --- %@",uploadImage.derverFileId);
    }else {
        NSLog(@" --- 删除失败 --- %@",uploadImage.derverFileId);
    }
}

@end

```

# 三、图片异步上传逻辑

```
#import <Foundation/Foundation.h>
#import "SSTEditTaskModel.h"

NS_ASSUME_NONNULL_BEGIN

@interface SSImageUploadQueueManager : NSObject

@property (nonatomic, assign) BOOL isUploading;

+ (instancetype)shareManager;

- (void)enqueueImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel;

- (void)reUploadImageModelArr:(NSArray<SSTEditTaskSujectFinishedPictureModel *> *)imageModelArr;

- (void)deleteUpoadImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel;

- (void)setAllUploadImageModelState:(SSTHomeworkPictureState)state;

@end

NS_ASSUME_NONNULL_END

```

```
#import "SSImageUploadQueueManager.h"
#import <AliyunOSSiOS/OSSService.h>
#import "OssfsTokenModel.h"
#import "DataBaseHelper+ImageUpload.h"

static SSImageUploadQueueManager *_manager = nil;
static dispatch_queue_t _queueUploadBegin = nil; // 创建串行队列 - 保证多次图片上传请求按顺序执行；
static dispatch_semaphore_t _semaphoreBegin = nil;

@interface SSImageUploadQueueManager ()<NSCopying,NSMutableCopying>

@property (nonatomic, strong) NSMutableArray *uploadQueue;

@end

@implementation SSImageUploadQueueManager

+ (instancetype)shareManager {
    return [[self alloc] init];
}

- (instancetype)init {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _manager = [super init];
        _uploadQueue = [NSMutableArray array];
        _queueUploadBegin = dispatch_queue_create("com.uploadHomeworkImageToOSS.xiaodiandou.tast", DISPATCH_QUEUE_SERIAL);
        _semaphoreBegin = dispatch_semaphore_create(1); // 设置信号总量为1，保证只有一个进程执行
    });
    return _manager;
}

+ (id)allocWithZone:(struct _NSZone *)zone {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _manager = [super allocWithZone:zone];
    });
    return _manager;
}

- (nonnull id)copyWithZone:(NSZone *)zone {
    return _manager;
}

- (nonnull id)mutableCopyWithZone:(NSZone *)zone {
    return _manager;
}
// 只在拍照的时候，从这里添加；
- (void)enqueueImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel {
    [[DataBaseHelper sharedInstance] saveHomeworkImageInfo:imageModel];
    [self.uploadQueue addObject:imageModel];
    [self startUploadingIfIdle];
}

- (void)reUploadImageModelArr:(NSArray<SSTEditTaskSujectFinishedPictureModel *> *)imageModelArr {
    [self.uploadQueue addObjectsFromArray:imageModelArr];
    if (self.uploadQueue.count == imageModelArr.count) {
        [self uploadNextImageModel]; // 说明上传队列里，没有在上传的图片了，直接去上传
    }
}

- (void)deleteUpoadImageModel:(SSTEditTaskSujectFinishedPictureModel *)imageModel {
    // 定义一个标识符来查找的值
    NSString *targetIdentifier = imageModel.derverFileId;
    // 创建NSPredicate对象
    NSPredicate *predicate = [NSPredicate predicateWithFormat:@"derverFileId == %@", targetIdentifier];
    // 使用NSPredicate过滤NSArray
    NSArray *filteredArray = [self.uploadQueue filteredArrayUsingPredicate:predicate];
    // 检查是否有匹配的Model对象
    if (filteredArray.count > 0) {
        // 找到了匹配的Model对象
        for (SSTEditTaskSujectFinishedPictureModel *pModel in filteredArray) {
            [self.uploadQueue removeObject:pModel];
        }
    } else {
        // 没有找到匹配的Model对象
        NSLog(@" -- 没有找到匹配的Model对象 -- ");
    }
}

- (void)setAllUploadImageModelState:(SSTHomeworkPictureState)state {
    NSArray *uploadImgAllArr = [[DataBaseHelper sharedInstance] getAllHomeworkImageModel];
    for (SSTEditTaskSujectFinishedPictureModel *imageModel in uploadImgAllArr) {
        [[DataBaseHelper sharedInstance] updateImageModel:imageModel withImageModelKey:@"correctStatus" andImageModelValue:[NSString stringWithFormat:@"%ld",state]];
    }
}

- (SSTEditTaskSujectFinishedPictureModel *)dequeueImageModel {
    SSTEditTaskSujectFinishedPictureModel *imageModel = [self.uploadQueue firstObject];
    if (imageModel) {
        [self.uploadQueue removeObjectAtIndex:0];
    }
    return imageModel;
}

- (void)startUploadingIfIdle {
    if (self.uploadQueue.count == 1) {
        [self uploadNextImageModel];
    }
}

- (void)uploadNextImageModel {
    
    SSTEditTaskSujectFinishedPictureModel *imageModel = [self dequeueImageModel];
    if (imageModel) {
        // 执行上传操作，可以使用网络请求库（如NSURLSession）将图片上传到服务器
        // 在上传完成后的回调中，调用 [self uploadNextImage] 继续上传下一张图片
        // 在上传失败或取消时，可以根据需要进行错误处理或重试
        WS(weakSelf);
        self.isUploading = YES;
        dispatch_async(_queueUploadBegin, ^{
            //等待信号量
            dispatch_semaphore_wait(_semaphoreBegin, DISPATCH_TIME_FOREVER);
                NSString *accessToken = [[NSUserDefaults standardUserDefaults] objectForKey:kUserToken];
                NSString *urlString = [HTTP_upload_getOssfsToken stringByAppendingString:[NSString stringWithFormat:@"?accessToken=%@",accessToken]];

            //[[DataBaseHelper sharedInstance] updateImageModel:imageModel withImageModelKey:@"correctStatus" andImageModelValue:@"11"];

                [XWHttpClient xw_postWithUrlString:urlString Params:nil DefaultHUD:NO RepeatNum:1 TimeOutSecond:10 SuccessBlock:^(id returnValue) {
                    NSLog(@"  ----- getOssfsToken - returnValue： %@",returnValue);
                    //处理耗时操作的代码块...
                    dispatch_async(dispatch_get_global_queue(0, 0), ^{
                        OssfsTokenModel *ossfsTokenModel = [OssfsTokenModel mj_objectWithKeyValues:DicGetValue(returnValue,@"data")];
                        id<OSSCredentialProvider> credential = [[OSSStsTokenCredentialProvider alloc] initWithAccessKeyId:ossfsTokenModel.accessKeyId secretKeyId:ossfsTokenModel.accessKeySecret securityToken:ossfsTokenModel.securityToken];
                        OSSClient *client = [[OSSClient alloc] initWithEndpoint:ossfsTokenModel.endpoint credentialProvider:credential];
                        OSSPutObjectRequest * put = [OSSPutObjectRequest new];
                        put.bucketName = ossfsTokenModel.bucket;
                        NSString * uploadImgPath = ossfsTokenModel.uploadImgPath;
                        NSString * objectKeyStr = [uploadImgPath substringFromIndex:1]; //去掉图片路径的第一个斜杠
                        put.objectKey = objectKeyStr;
                        imageModel.localImage = [UIImage compressImage:imageModel.localImage toByte:800000];
                        NSData *imageData = UIImageJPEGRepresentation(imageModel.localImage, 1);
                        put.uploadingData = imageData; // UIImageJPEGRepresentation(img.localImage,1);
                        put.uploadProgress = ^(int64_t bytesSent, int64_t totalByteSent, int64_t totalBytesExpectedToSend) {
                            NSString *sendSize = [SSUtility transformedValue:[NSNumber numberWithUnsignedLongLong:totalByteSent]];
                            NSString *totalSize = [SSUtility transformedValue:[NSNumber numberWithUnsignedLongLong:totalBytesExpectedToSend]];
                            SSLog(@"上传图片大小为: %@ --- 已上传: %@",totalSize,sendSize);
                        };
                        if (imageModel.questionRecommendRecordId) { // kHOST_ADDRESS -> kUPLOAD_ADDRESS
                            NSString *paramBody = @"{\"vipId\":${x:vipId},\"costype\":${x:costype},\"derverFileId\":${x:derverFileId},\"fileKeys\":${x:fileKeys},\"courseName\":${x:courseName},\"questionRecommendRecordId\":${x:questionRecommendRecordId}}";
                            // 正确的
                            put.callbackParam = @{@"callbackUrl":[NSString stringWithFormat:@"%@/api/parents/xy/homework/uploadPictureNoSubject?accessToken=%@",kHOST_ADDRESS,[SSUtility getUserToken]],
                                                 @"callbackBody":paramBody,
                                             @"callbackBodyType":@"application/json"};
                            put.callbackVar = @{@"x:vipId":imageModel.vipId,
                                                @"x:costype":@"1",
                                                @"x:fileKeys":uploadImgPath,
                                                @"x:courseName":imageModel.course,
                                                @"x:derverFileId":imageModel.derverFileId,
                                                @"x:questionRecommendRecordId":imageModel.questionRecommendRecordId};
                        }else {
                            NSString *paramBody = @"{\"vipId\":${x:vipId},\"costype\":${x:costype},\"derverFileId\":${x:derverFileId},\"fileKeys\":${x:fileKeys},\"courseName\":${x:courseName}}";
                            // 正确的
                            put.callbackParam = @{@"callbackUrl":[NSString stringWithFormat:@"%@/api/parents/xy/homework/uploadPictureNoSubject?accessToken=%@",kHOST_ADDRESS,[SSUtility getUserToken]],
                                                 @"callbackBody":paramBody,
                                             @"callbackBodyType":@"application/json"};
                            put.callbackVar = @{@"x:vipId":imageModel.vipId,
                                                @"x:costype":@"1",
                                                @"x:fileKeys":uploadImgPath,
                                                @"x:courseName":imageModel.course,
                                                @"x:derverFileId":imageModel.derverFileId};
                        }
                        OSSTask * putTask = [client putObject:put];
                        [putTask waitUntilFinished]; // 阻塞直到上传完成
                        [putTask continueWithBlock:^id(OSSTask *task) {
                            OSSPutObjectResult *result = task.result;
                            NSLog(@"Result - requestId: %@, headerFields: %@, servercallback: %@",result.requestId,result.httpResponseHeaderFields,result.serverReturnJsonString);
                            NSDictionary *dataDict = [SSUtility dictionaryWithJsonString:result.serverReturnJsonString];
                            NSString *codeStr = dataDict[@"code"];
                            NSString *msgStr = dataDict[@"msg"];
                            if (!task.error) {
                                if ([codeStr isEqualToString:@"999"]) {
                                    imageModel.image = uploadImgPath; // callback 成功不用回调；
                                    NSString *imgUrl = [SSUtility getImageFullPathWithServerPath:uploadImgPath];
                                    [[SDImageCache sharedImageCache] storeImage:imageModel.localImage forKey:imgUrl completion:^{
                                        NSLog(@" --- &&&&&&&&&&&&&& --- 上传图片成功 --- 本地保存 --- ");
                                    }];
                                    // 上传成功后，删除本地图片数据
                                    [[DataBaseHelper sharedInstance] deleteHomeworkImageModel:imageModel];
//                                    if (successBlock) {
//                                        successBlock(dataDict);
//                                    }
                                    NSLog(@"upload object success!");
                                }else {
                                    dispatch_async(dispatch_get_main_queue(), ^{
                                        [[SSCustomAlertView alloc] setAlertViewTitle:@"" andMessage:msgStr ? msgStr : @"作业上传失败" andhideAlertViewTimeOut:kDefaultAlertTime];
                                    });
//                                    if (errorBlock) {
//                                        errorBlock(task.error);
//                                    }
                                    [[DataBaseHelper sharedInstance] updateImageModel:imageModel withImageModelKey:@"correctStatus" andImageModelValue:@"6"];
                                }
                            } else {
                                NSLog(@"upload object failed, error: %@" , task.error);
                                dispatch_async(dispatch_get_main_queue(), ^{
                                    [[SSCustomAlertView alloc] setAlertViewTitle:@"" andMessage:msgStr ? msgStr : @"作业上传失败" andhideAlertViewTimeOut:kDefaultAlertTime];
                                });
//                                if (errorBlock) {
//                                    errorBlock(task.error);
//                                }
                                [[DataBaseHelper sharedInstance] updateImageModel:imageModel withImageModelKey:@"correctStatus" andImageModelValue:@"6"];

                            }
                            [weakSelf uploadNextImageModel]; // 上传下一张
                            [[NSNotificationCenter defaultCenter] postNotificationName:kUploadImgSuccessNotificationName object:imageModel]; // 提示页面刷新
                            dispatch_semaphore_signal(_semaphoreBegin);
                            task = [client presignPublicURLWithBucketName:ossfsTokenModel.bucket withObjectKey:objectKeyStr];
                            return nil;
                        }];
                    });
                    
                } ErrorBlock:^(id errorCode) {
//                    if (errorBlock) {
//                        errorBlock(errorCode);
//                    }
                    [[DataBaseHelper sharedInstance] updateImageModel:imageModel withImageModelKey:@"correctStatus" andImageModelValue:@"6"];
                    [weakSelf uploadNextImageModel]; // 上传下一张
                    [[NSNotificationCenter defaultCenter] postNotificationName:kUploadImgSuccessNotificationName object:imageModel]; // 提示页面刷新
                    dispatch_semaphore_signal(_semaphoreBegin);
                } FailureBlock:^(id failureInfo) {
//                    if (failBlock) {
//                        failBlock(failureInfo);
//                    }
                    [[DataBaseHelper sharedInstance] updateImageModel:imageModel withImageModelKey:@"correctStatus" andImageModelValue:@"6"];
                    [weakSelf uploadNextImageModel]; // 上传下一张
                    [[NSNotificationCenter defaultCenter] postNotificationName:kUploadImgSuccessNotificationName object:imageModel]; // 提示页面刷新
                    dispatch_semaphore_signal(_semaphoreBegin);
                }];
        
        });

    }else { // 如果有imageModel
        self.isUploading = NO;
    }
    
}

@end

```

# 四、拍照上传操作

```
    // 上传作业图片
    SSTEditTaskSujectFinishedPictureModel *subjectFinishPictureModel = [[SSTEditTaskSujectFinishedPictureModel alloc] init];
    NSTimeInterval endTime = [[NSDate date] timeIntervalSince1970]*1000;// *1000 是精确到毫秒，不乘就是精确到秒
    NSInteger uploadTime = endTime;
    NSString *localImagePath = [NSString stringWithFormat:@"%@-%zd.jpg",[SSUtility getUserVipId],uploadTime];
    subjectFinishPictureModel.course = self.subject;
    subjectFinishPictureModel.vipId = [SSUtility getUserVipId];
    //subjectFinishPictureModel.uploadDate = [NSDate getDate:[NSDate date] day:4]; // 测试
    subjectFinishPictureModel.uploadDate = [NSDate getDateStringWithNowDate:[NSDate date]];
    subjectFinishPictureModel.derverFileId = [NSString stringWithFormat:@"%@-%zd",[SSUtility getUserVipId],uploadTime];
    subjectFinishPictureModel.localPath = localImagePath;
    subjectFinishPictureModel.timestampStr = [NSString stringWithFormat:@"%zd",uploadTime];
    subjectFinishPictureModel.localImage = _photopImage;
    subjectFinishPictureModel.correctStatus = SSTHomeworkPictureStateUploading; // 上传中
    subjectFinishPictureModel.studentName = [SSUtility getUserCurrentChildName];
    //subjectFinishPictureModel.isLocalData = YES;
    //[[SSTUploadHomeworkPictureManager shareManager] saveUploadingHomewrokPhoto:subjectFinishPictureModel withVipId:self.vipId subject:self.courseName];

    [[SSImageUploadQueueManager shareManager] enqueueImageModel:subjectFinishPictureModel];

```

# 五、上传列表数据获取

```c
    NSArray *uploadImgAllArr = [[DataBaseHelper sharedInstance] getAllHomeworkImageModel];
    NSMutableArray *uploadImgErrorArr = [NSMutableArray array];
    for (SSTEditTaskSujectFinishedPictureModel *imageModel in uploadImgAllArr) {
        if (imageModel.correctStatus == SSTHomeworkPictureStateUploadFail) {
            [uploadImgErrorArr addObject:imageModel];
        }
    }
    [self.uploadImgArr removeAllObjects];
    [self.uploadImgArr addObjectsFromArray:uploadImgAllArr];
    [self.uploadImgErrorArr removeAllObjects];
    [self.uploadImgErrorArr addObjectsFromArray:uploadImgErrorArr];
    dispatch_async(dispatch_get_main_queue(), ^{
        self.rightBtn.hidden = uploadImgErrorArr.count > 0 ? NO : YES;
        [self.tableView reloadData];
    });

```
