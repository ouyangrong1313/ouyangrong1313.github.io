---
title: 本地先下载PDF文件，再用WKWebView显示
author: Ouyang Rong
date: 2021-07-07 16:14:00 +0800
categories: [iOS, UI]
tags: [WKWebView, NSFileManager]
---

# 需求分析

项目中要用WKWebView显示PDF链接，发现用系统自带的缓存策略在网络差的时候，加载不出来。于是，为了更好的用户体验，还是自己做一个本地存储的逻辑。这样，无论网络好坏，只要本地下载了PDF文件就可以快速从本地加载出来。同时，还有另外一个问题，当跳到下一个页面再回来的时候，WebView变白了，又要重新加载数据，这个时候如果本地存储了PDF文件的话，页面显示出来就快很多。

# WKWebView自带缓存策略

```
-(WKWebView *)originWebView{
    if (!_originWebView) {
       WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
       //这个类主要用来做native与JavaScript的交互管理
       WKUserContentController * wkUController = [[WKUserContentController alloc] init];
       config.userContentController = wkUController;
       //禁止缩放
       NSString *js = @" $('meta[name=description]').remove(); $('head').append( '' );";
       WKUserScript *wkUScript = [[WKUserScript alloc] initWithSource:js injectionTime:WKUserScriptInjectionTimeAtDocumentEnd forMainFrameOnly:NO];
       [config.userContentController addUserScript:wkUScript];
       _originWebView = [[WKWebView alloc] initWithFrame:CGRectMake(0,0,kFullScreenWidth,kFullScreenHeight-kStatusBarAndNavigationBarHeight) configuration:config];
       _originWebView.backgroundColor = [UIColor generateDynamicColor:UIColorFromHex(COLOR_FFFFFF) darkColor:UIColorFromHex(COLOR_000000)];
       _originWebView.navigationDelegate = self;
       _originWebView.UIDelegate = self;
       _originWebView.navigationDelegate = self;
       _originWebView.scrollView.showsVerticalScrollIndicator = NO;
       _originWebView.scrollView.showsHorizontalScrollIndicator = NO;
    }
    return _originWebView;
}
```
```
[self loadRequestWithFileModel:self.fileModel.originQuestionPdfUrl wkWebView:self.originWebView];
```
```
-(void)loadRequestWithFileModel:(NSString*)fileUrl wkWebView:(WKWebView *)webView{
    NSString *pdfUrl =[NSString stringWithFormat:@"%@%@",kHOST_ADDRESS,fileUrl];
    NSString *encodedString = (NSString *)CFBridgingRelease(CFURLCreateStringByAddingPercentEscapes (kCFAllocatorDefault, (CFStringRef)pdfUrl,(CFStringRef) @"!NULL,'()*+,-./:;=?@_~%#[]", NULL, kCFStringEncodingUTF8));
    NSURL *filePath = [NSURL URLWithString:encodedString]; // NSURLRequestReturnCacheDataDontLoad  NSURLRequestReloadIgnoringLocalCacheData
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:filePath cachePolicy:NSURLRequestReturnCacheDataElseLoad timeoutInterval:10];
    [webView loadRequest:request];
}
```

# WKWebView自定义本地存储逻辑

```
-(void)getDataWithPdfUrl:(NSString *)fileUrl isOrigin:(BOOL)isOrigin{
    //判断文件是否存在
    NSString *fileName = [[SSPDownloadPdfFileManager shareInstance] getFileNameWithFileUrl:fileUrl withPrintId:self.fileModel.printingId withSubject:self.fileModel.subject];
    if ([[SSPDownloadPdfFileManager shareInstance] isSavedFileToLocalWithFileName:fileName filePath:LOCAL_ERROROBOOK_PATH]) {
        NSURL *pdfUrl = [[SSPDownloadPdfFileManager shareInstance] getLocalFilePathWithfileName:fileName withLocalPath:LOCAL_ERROROBOOK_PATH];
        [self loadRequestWithFileUrl:pdfUrl isOrigin:isOrigin];
    }else{
        [self savePdfFileWithFileUrl:fileUrl isOrigin:isOrigin];//直接下载数据
    }
}

-(void)savePdfFileWithFileUrl:(NSString *)fileUrl isOrigin:(BOOL)isOrigin{
    NSString *fileName = [[SSPDownloadPdfFileManager shareInstance] getFileNameWithFileUrl:fileUrl withPrintId:self.fileModel.printingId withSubject:self.fileModel.subject];
    //文件路径存在 直接下载
    NSString *pdfUrl =[NSString stringWithFormat:@"%@%@",kHOST_ADDRESS,fileUrl];
    NSString *encodedString = (NSString *)CFBridgingRelease(CFURLCreateStringByAddingPercentEscapes (kCFAllocatorDefault, (CFStringRef)pdfUrl,(CFStringRef) @"!NULL,'()*+,-./:;=?@_~%#[]", NULL, kCFStringEncodingUTF8));
    [[SSPDownloadPdfFileManager shareInstance] downloadFileWithFileUrl:encodedString fileName:fileName filePath:LOCAL_ERROROBOOK_PATH downLoadSuccess:^(NSURLResponse * _Nonnull response, NSURL * _Nullable filePath) {
        [self loadRequestWithFileUrl:filePath isOrigin:isOrigin];
    } downLoadFail:^(NSURLResponse * _Nonnull response, NSError * _Nullable error) {

    } progress:^(NSProgress * _Nonnull downloadProgress) {

    }];
}

-(void)loadRequestWithFileUrl:(NSURL *)fileUrl isOrigin:(BOOL)isOrigin{
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:fileUrl];
    if (isOrigin) {
        [self.originWebView loadRequest:request];
    }else {
        [self.analysisWebView loadRequest:request];
    }
}
```
```
#define LOCAL_ERROROBOOK_PATH @"Documents/SharingSchool/ErrorBook"

-(NSString *)getFileNameWithFileUrl:(NSString *)fileUrl withPrintId:(NSString *)printId withSubject:(NSString *)subject{
    NSString *newFileUrl = [fileUrl stringByReplacingOccurrencesOfString:@"/" withString:@"_"];
    NSString *fileName = [NSString stringWithFormat:@"%@_%@_%@",subject,printId,newFileUrl];
    return fileName;
}

-(BOOL)isSavedFileToLocalWithFileName:(NSString *)fileName filePath:(NSString *)filePath{
    NSString *documentsDirectory = [NSHomeDirectory() stringByAppendingPathComponent:filePath];
    NSString *recordPath = [documentsDirectory stringByAppendingPathComponent:[NSString stringWithFormat:@"/%@",fileName]];
    if (![self creatFile:documentsDirectory]) {
        return NO;
    }
    NSFileManager *filemanager = [NSFileManager defaultManager];
    if ([filemanager fileExistsAtPath:recordPath]) {
        return YES;
    }
    return NO;
}

-(BOOL)creatFile:(NSString*)filePath{
    if (filePath.length==0) {
        return NO;
    }
    NSFileManager *fileManager = [NSFileManager defaultManager];
    if ([fileManager fileExistsAtPath:filePath]) {
        return YES;
    }
    NSError *error;
    BOOL isSuccess = [fileManager createDirectoryAtPath:filePath withIntermediateDirectories:YES attributes:nil error:&error]; // 在Documetnts目录中创建名为XXX的目录
    if (error) {
        NSLog(@"creat File Failed:%@",[error localizedDescription]);
    }
    if (!isSuccess) {
        return isSuccess;
    }
    isSuccess = [fileManager createFileAtPath:filePath contents:nil attributes:nil]; //在XXX目录里，创建文件XXX
    return isSuccess;
}

-(NSURL *)getLocalFilePathWithfileName:(NSString *)fileName withLocalPath:(NSString *)localPath{
    NSString *documentsDirectory = [NSHomeDirectory() stringByAppendingPathComponent:localPath];
    NSFileManager *filemanager = [NSFileManager defaultManager];
    NSArray *fileList = [filemanager subpathsOfDirectoryAtPath:documentsDirectory error:nil];
    if ([fileList containsObject:fileName]) {
        NSString *fileUrltemp = [NSString stringWithFormat:@"%@/%@", documentsDirectory,fileName];
        NSURL *url = [NSURL fileURLWithPath:fileUrltemp];
        return url;
    }
    return nil;
}

+ (BOOL)checkUrlWithString:(NSString *)url {
    NSString *regex =@"[a-zA-z]+://[^\\s]*";
    NSPredicate *urlTest = [NSPredicate predicateWithFormat:@"SELF MATCHES %@",regex];
    return [urlTest evaluateWithObject:url];
}

- (void)downloadFileWithFileUrl:(NSString *)requestURL
                      fileName:(NSString *)fileName
                      filePath:(NSString *)filePath
               downLoadSuccess:(DownLoadFileSuccessBlock)successBlcok
                  downLoadFail:(DownLoadFileFailureBlock)failureBlock
                      progress:(DownLoadFileProgressBlcok)progressBlock {
    AFURLSessionManager *manager = [[AFURLSessionManager alloc] initWithSessionConfiguration:[NSURLSessionConfiguration defaultSessionConfiguration]];
    /* 下载地址 qu*/
    NSURL *url;
    if ([SSUtility checkUrlWithString:requestURL]) {
        url = [NSURL URLWithString:requestURL];
    }else {
        url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@",kHOST_ADDRESS,requestURL]];
    }
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    /* 下载路径 */
    NSString *path = [NSHomeDirectory() stringByAppendingPathComponent:filePath];
    NSString *recordPath = [path stringByAppendingPathComponent:[NSString stringWithFormat:@"/%@",fileName]];
    //[NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) lastObject];
    if (![self creatFile:path]) {
        return;
    }
    NSURLSessionDownloadTask *downloadTask = [manager downloadTaskWithRequest:request progress:^(NSProgress * _Nonnull downloadProgress) {
        progressBlock(downloadProgress);
        SSLog(@"下载进度：%.0f％", downloadProgress.fractionCompleted * 100);
    } destination:^NSURL * _Nonnull(NSURL * _Nonnull targetPath, NSURLResponse * _Nonnull response) {
        dispatch_async(dispatch_get_main_queue(), ^{
            //如果需要进行UI操作，需要获取主线程进行操作
        });
        /* 设定下载到的位置 */
        return [NSURL fileURLWithPath:recordPath];
    } completionHandler:^(NSURLResponse * _Nonnull response, NSURL * _Nullable filePath, NSError * _Nullable error) {
        if(error){
            failureBlock(response,error);
        }else{
            successBlcok(response,filePath);
        }
    }];
    [downloadTask resume];
}
```

# NSFileManager常用的文件管理操作

- 创建目录 createDirectoryAtPath：
- 创建文件 createFileAtPath：
- 删除某个文件 removeItemAtPath:
- 检查某个文件是否存在 fileExistsAtPath:
- 检查文件是否可读 isReadableFileAtPath:
- 检查文件是否可写 isWritableFileAtPath:
- 取得文件属性 fileAttributesAtPath:
- 改变文件属性 changeAttributesAtPath:
- 从path代表的文件中读取数据 contentsAtPath
- 移动文件 movePath:toPath:handler:
- 复制文件 copyPath:toPath:handler:
