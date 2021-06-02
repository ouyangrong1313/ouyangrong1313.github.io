---
title: 图片转PDF
author: Ouyang Rong
date: 2021-01-11 16:14:00 +0800
categories: [iOS, UI]
tags: [UIWebView, PDF]
---


### 获取tableView截取的多张图片


```
-(NSArray *)imagesArrForTableView{
    //0.更新historyTableView的约束 选择学科的不能重复截图
     [self.historyTalbelView mas_updateConstraints:^(MASConstraintMaker *make) {
         make.top.mas_equalTo(self.view.mas_top);
     }];

     // 1.获取WebView的宽高
     CGSize boundsSize = self.historyTalbelView.bounds.size;
     //CGFloat boundsWidth = boundsSize.width;
     CGFloat boundsHeight = boundsSize.height;
     // 2.获取contentSize
     CGSize contentSize = self.historyTalbelView.contentSize;
     CGFloat contentHeight = contentSize.height;
     // 3.保存原始偏移量，便于截图后复位
     CGPoint offset = self.historyTalbelView.contentOffset;
     // 4.设置最初的偏移量为(0,0);
     [self.historyTalbelView setContentOffset:CGPointMake(0,0)];
     NSMutableArray *images = [NSMutableArray array];
     while (contentHeight > 0) {
         // 5.获取CGContext 5.获取CGContext
         if (contentHeight - boundsSize.height < 0) {
            UIGraphicsBeginImageContextWithOptions(CGSizeMake(boundsSize.width, boundsSize.height-80), NO, 0.0);
            CGContextRef ctx = UIGraphicsGetCurrentContext();
            // 6.渲染要截取的区域
            [self.view.layer renderInContext:ctx];
            UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
            UIGraphicsEndImageContext();
            // 7.截取的图片保存起来
            [images addObject:image];
         }else{
             UIGraphicsBeginImageContextWithOptions(boundsSize, NO, 0.0);
             CGContextRef ctx = UIGraphicsGetCurrentContext();
             // 6.渲染要截取的区域
             [self.view.layer renderInContext:ctx];
             UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
             UIGraphicsEndImageContext();
             // 7.截取的图片保存起来
             [images addObject:image];
      }

      CGFloat offsetY = self.historyTalbelView.contentOffset.y;
      [self.historyTalbelView setContentOffset:CGPointMake(0, offsetY + boundsHeight)];
      contentHeight -= boundsHeight;
     }
     // 8 tableView 恢复到之前的显示区域
     [self.historyTalbelView setContentOffset:offset];

//     CGFloat scale = [UIScreen mainScreen].scale;
//     CGSize imageSize = CGSizeMake(contentSize.width * scale,
//                                   (contentSize.height-80) * scale);
     // 9.根据设备的分辨率重新绘制、拼接成完整清晰图片
//     UIGraphicsBeginImageContext(imageSize);
//     [images enumerateObjectsUsingBlock:^(UIImage *image, NSUInteger idx, BOOL *stop) {
//         [image drawInRect:CGRectMake(0,scale * boundsHeight * idx,scale * image.size.width,scale * image.size.height)];
//     }];
//     UIImage *fullImage = UIGraphicsGetImageFromCurrentImageContext(); // 用这个方法是获取完整的tableView图片；
//     UIGraphicsEndImageContext();

     //10.更新historyTableView的约束
     [self.historyTalbelView mas_updateConstraints:^(MASConstraintMaker *make) {
            make.top.mas_equalTo(self.view.mas_top).offset(64);
     }];
     return images;
}

```

### 把多张图片转成PDF文件


```
- (NSString *)createPDF:(NSArray *)dataSource{

    NSString *path = [NSHomeDirectory() stringByAppendingPathComponent:[NSString stringWithFormat:@"%@/%@",LOCAL_ERROROBOOK_PATH,self.vipId]];
    NSString *pdfPath = [path stringByAppendingPathComponent:[NSString stringWithFormat:@"/%@", [self getFileName]]];
    if ([self creatFile:path]) {
        NSLog(@" --- 创建PDF路径成功 --- ");
    }
    // CGRectZero 表示默认尺寸，参数可修改，设置自己需要的尺寸
    UIGraphicsBeginPDFContextToFile(pdfPath, CGRectZero, NULL);

    CGRect  pdfBounds = UIGraphicsGetPDFContextBounds();
    CGFloat pdfWidth  = pdfBounds.size.width;
    CGFloat pdfHeight = pdfBounds.size.height;

    for (UIImage *image in dataSource) { // NSData * imageData in dataSource
        //UIImage *image = [UIImage imageWithData:imageData];
        // 绘制PDF
        UIGraphicsBeginPDFPage();
        CGFloat imageW = image.size.width;
        CGFloat imageH = image.size.height;
        if (imageW <= pdfWidth && imageH <= pdfHeight)
        {
            CGFloat originX = (pdfWidth - imageW) / 2;
            CGFloat originY = (pdfHeight - imageH) / 2;
            [image drawInRect:CGRectMake(originX, originY, imageW, imageH)];
        }
        else
        {
            CGFloat width,height;
            if ((imageW / imageH) > (pdfWidth / pdfHeight))
            {
                width  = pdfWidth;
                height = width * imageH / imageW;
            }
            else
            {
                height = pdfHeight;
                width = height * imageW / imageH;
            }
            [image drawInRect:CGRectMake((pdfWidth - width) / 2, (pdfHeight - height) / 2, width, height)];
        }
    }
    UIGraphicsEndPDFContext();
    return pdfPath;
}

/**
 * 文件名 2019.06.18 16:47-错误原题
 */
-(NSString *)getFileName{
    NSString *dateString = [NSDate getDateStringByDate:[NSDate date]];
    NSString *timeString = [NSDate getTimeWithSecondStringByDate:[NSDate date]];
    NSString *typeString = @"WeekStudyReport";
    NSString *fullFileName = [NSString stringWithFormat:@"%@ %@-%@-%@.pdf",dateString,timeString,typeString,self.selectSubjectName];
    return fullFileName;
}

/**
 * 创建文件路径
 */
-(BOOL)creatFile:(NSString*)filePath{
    if (filePath.length==0) {
        return NO;
    }
    NSFileManager *fileManager = [NSFileManager defaultManager];
    if ([fileManager fileExistsAtPath:filePath]) {
        return YES;
    }
    NSError *error;
    BOOL isSuccess = [fileManager createDirectoryAtPath:filePath withIntermediateDirectories:YES attributes:nil error:&error];
    if (error) {
        NSLog(@"creat File Failed:%@",[error localizedDescription]);
    }
    if (!isSuccess) {
        return isSuccess;
    }
    isSuccess = [fileManager createFileAtPath:filePath contents:nil attributes:nil];
    return isSuccess;
}

```

**相关文章参考**：

[将UIWebView显示的内容转为图片和PDF](https://esoftmobile.com/2013/06/10/convert-webview-to-image/)

将UIWebView分屏截取，然后将截取的图片拼接成一张图片。
```
- (UIImage *)imageRepresentation{
    CGSize boundsSize = self.bounds.size;
    CGFloat boundsWidth = self.bounds.size.width;
    CGFloat boundsHeight = self.bounds.size.height;

    CGPoint offset = self.scrollView.contentOffset;
    [self.scrollView setContentOffset:CGPointMake(0, 0)];

    CGFloat contentHeight = self.scrollView.contentSize.height;
    NSMutableArray *images = [NSMutableArray array];
    while (contentHeight > 0) {
        UIGraphicsBeginImageContext(boundsSize);
        [self.layer renderInContext:UIGraphicsGetCurrentContext()];
        UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
        UIGraphicsEndImageContext();
        [images addObject:image];

        CGFloat offsetY = self.scrollView.contentOffset.y;
        [self.scrollView setContentOffset:CGPointMake(0, offsetY + boundsHeight)];
        contentHeight -= boundsHeight;
    }
    [self.scrollView setContentOffset:offset];

    UIGraphicsBeginImageContext(self.scrollView.contentSize);
    [images enumerateObjectsUsingBlock:^(UIImage *image, NSUInteger idx, BOOL *stop) {
        [image drawInRect:CGRectMake(0, boundsHeight * idx, boundsWidth, boundsHeight)];
    }];
    UIImage *fullImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return fullImage;
}
```


将UIWebView从头，contentOffset = (0, 0)，开始截取webView.bounds.size.height高度的图片，然后将_webView可见区域下移继续截屏，这样将所有截取的图片按照顺序拼接，就能得到整个UIWebView显示内容的完整图片。


```
- (NSData *)PDFData{
    UIViewPrintFormatter *fmt = [self viewPrintFormatter];
    UIPrintPageRenderer *render = [[UIPrintPageRenderer alloc] init];
    [render addPrintFormatter:fmt startingAtPageAtIndex:0];
    CGRect page;
    page.origin.x=0;
    page.origin.y=0;
    page.size.width=600;
    page.size.height=768;

    CGRect printable=CGRectInset( page, 50, 50 );
    [render setValue:[NSValue valueWithCGRect:page] forKey:@"paperRect"];
    [render setValue:[NSValue valueWithCGRect:printable] forKey:@"printableRect"];

    NSMutableData * pdfData = [NSMutableData data];
    UIGraphicsBeginPDFContextToData( pdfData, CGRectZero, nil );

    for (NSInteger i=0; i < [render numberOfPages]; i++)
    {
        UIGraphicsBeginPDFPage();
        CGRect bounds = UIGraphicsGetPDFContextBounds();
        [render drawPageAtIndex:i inRect:bounds];

    }
    UIGraphicsEndPDFContext();
    return pdfData;
}
```
