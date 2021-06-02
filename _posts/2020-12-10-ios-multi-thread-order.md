---
title: 用多线程控制程序执行顺序
author: Ouyang Rong
date: 2020-12-10 16:14:00 +0800
categories: [iOS, 多线程]
tags: [GCD, 信号量]
---


# 一、按顺序多次从一个接口请求数据


```
//按顺序请求语数英三门学科的数据；
- (void)getAllSubjectHomeworkData {
    if (self.subjectCountData.list.count == 0) {
        return;
    }
    dispatch_queue_t queueUploadBegin = dispatch_queue_create("com.getAllSubjectHomeworkData.subsystem.tast", DISPATCH_QUEUE_SERIAL);
    dispatch_semaphore_t semaphoreBegin = dispatch_semaphore_create(1); //设置信号总量为1，保证只有一个进程执行；
    for (NSInteger i = 0; i < self.subjectCountData.list.count; i ++) {
        SSTSubjectCountModel *subModel = self.subjectCountData.list[i];
        [subModel.homeworkListModel.list removeAllObjects]; //先清空数据；
        NSInteger pageNO = 1;
        NSInteger pageSize = subModel.workCount;
        NSString *subjectName = subModel.subject;
        if (pageSize > 0) {
            dispatch_async(queueUploadBegin, ^{
                dispatch_semaphore_wait(semaphoreBegin, DISPATCH_TIME_FOREVER); //等待信号量
                NSString *classId = [[NSUserDefaults standardUserDefaults] objectForKey:kCorrectClassId];
                NSDictionary *params = @{@"pageNo":@(pageNO),@"pageSize":@(pageSize),@"type":@"0",@"subject":subjectName.length>0?subjectName:@"", @"classId":classId.length?classId:@""};
                WEAKSELF(weakSelf);
                NSLog(@" --- 正在请求%@科目的数据 --- ",subjectName);
                [XWHttpClient xw_postWithUrlString:AppendURL(kHomeworkList) Params:params DefaultHUD:NO SuccessBlock:^(id returnValue) {
                    SSTCorrectHomeworkListModel *tempModel = [SSTCorrectHomeworkListModel mj_objectWithKeyValues:DicGetValue(returnValue, @"data")];
                    subModel.homeworkListModel = tempModel;
                    dispatch_semaphore_signal(semaphoreBegin);
                    if (i == weakSelf.subjectCountData.list.count - 1) {
                        dispatch_async(dispatch_get_main_queue(), ^{
                            NSLog(@" --- 全部学科的数据请求完毕 --- ");
                        });
                    }
                } ErrorBlock:^(id errorCode) {
                    dispatch_semaphore_signal(semaphoreBegin);
                } FailureBlock:^(id failureInfo) {
                    dispatch_semaphore_signal(semaphoreBegin);
                }];
            });
        }
    }
}
```


# 二、按顺序添加多个View


```
- (void)createLocationViews {
    dispatch_queue_t queueUploadBegin = dispatch_queue_create("com.createLocationViews.subsystem.tast", DISPATCH_QUEUE_SERIAL);
    dispatch_semaphore_t semaphoreBegin = dispatch_semaphore_create(1); //设置信号总量为1，保证只有一个进程执行；
    __block ViewController *weakSelf = self;
    for (NSInteger i = 0; i < self.loacationArr.count; i ++) {
        LocationModel *subModel = self.loacationArr[i];
        dispatch_async(queueUploadBegin, ^{
            dispatch_semaphore_wait(semaphoreBegin, DISPATCH_TIME_FOREVER); //等待信号量；
            dispatch_time_t delayTime = dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.5*NSEC_PER_SEC));
            dispatch_after(delayTime, dispatch_get_main_queue(), ^{
                NSLog(@" --- 添加 locationView 第 %ld 个 --- ", i);
                UIView *locationView = [[UIView alloc] initWithFrame:CGRectMake(subModel.location_X, subModel.location_Y, 30, 30)];
                locationView.backgroundColor = [weakSelf randomColor];
                locationView.layer.cornerRadius = 15;
                locationView.layer.masksToBounds = YES;
                locationView.alpha = 0.0;
                [weakSelf.view addSubview:locationView];
                [UIView animateWithDuration:0.5 animations:^{
                    locationView.alpha = 1.0;
                    dispatch_semaphore_signal(semaphoreBegin);
                    if (i == weakSelf.loacationArr.count - 1) {
                        NSLog(@" --- locationView 添加完毕 --- ");
                    }
                }];
            });

        });
    }
}
```


**参考文章**：

[iOS多个网络请求完成后执行下一步](https://www.jianshu.com/p/fb4fb80aefb8)
