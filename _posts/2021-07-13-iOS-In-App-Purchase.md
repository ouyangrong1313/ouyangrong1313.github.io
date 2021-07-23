---
title: 苹果内购
author: Ouyang Rong
date: 2021-07-13 10:57:00 +0800
categories: [iOS, 功能]
tags: [支付, In-App Purchase]
---

# 内购简介

IAP 全称：`In-App Purchase`，是指苹果 App Store 的应用内购买，是苹果为 App 内购买虚拟商品或服务提供的一套交易系统。

![内购导图](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E8%B4%AD%E5%AF%BC%E5%9B%BE.png)


# 适用范围

在 App 内需要付费使用的产品功能或虚拟商品/服务，如游戏道具、电子书、音乐、视频、订阅会员、App的高级功能等需要使用 IAP，而在 App 内购买实体商品（如淘宝购买手机）或者不在 App 内使用的虚拟商品（如充话费）或服务（如滴滴叫车）则不适用于 IAP。

简而言之，苹果规定：适用范围内的虚拟商品或服务，必须使用 IAP 进行购买支付，不允许使用支付宝、微信支付等其它第三方支付方式（包括Apple Pay），也不允许以任何方式（包括跳出App、提示文案等）引导用户通过应用外部渠道购买。


# 内购准备

### App 内集成内购代码之前需要先去开发账号的 iTunes Connect 后台填写银行账户信息、配置内购商品（包括产品ID、价格等），还需要配置沙盒账号用于 IAP 测试。

### 银行账户信息填写

### 配置内购商品

IAP 是一套商品交易系统，而非简单的支付系统，每一个购买项目都需要在开发者后台的 iTunes Connect 后台为 App 创建一个对应的商品，提交给苹果审核通过后，购买项目才会生效。


###### 新建内购商品有四种选择分别是：

- 消耗型项目：只可使用一次的产品，使用之后即失效，必须再次购买，如：游戏币、一次性虚拟道具等。
- 非消耗型项目：只需购买一次，不会过期或随着使用而减少的产品。如：电子书。
- 自动续期订阅：允许用户在固定时间段内购买动态内容的产品。除非用户选择取消，否则此类订阅会自动续期，如：Apple Music这类按月订阅的商品。
- 非续期订阅：允许用户购买有时限性服务的产品，此 App 内购买项目的内容可以是静态的。此类订阅不会自动续期。

一般情况下用的最多的是消耗型商品，根据 App 类型也会使用到非消耗型和自动续期订阅，以消耗型商品举例：

这里需要注意的是产品 ID 具有唯一性，建议使用项目的 Bundle Identidier 作为前缀后面拼接自定义的唯一的商品名或者ID（字母、数字）。

> 这里有个坑：一旦新建一个内购商品，它的产品ID将永远被占用，即使该商品已经被删除，已创建的内购商品除了产品 ID 之外的所有信息都可以修改，如果删除了一个内购商品，将无法再创建一个相同产品 ID 的商品，也意味着该产品 ID 永久失效，一般来说产品ID有特定的命名规则，如果命名规则下有某个产品 ID 永久失效，可能会导致整个产品ID命名规则都要修改，这里千万要注意！
>

另外内购商品的定价只能从苹果提供的价格等级去选择，这个价格等级是固定的，同一价格等级会对应各个国家的货币，也就是说内购商品的价格是根据 Apple ID 所在区域的货币进行结算的，比如：一个内购商品你选择等级1，那么这个商品在美区是 0.66 美元，在中区是 6 元人民币，在香港去是 8 港币，这些价格一般是固定的，除非某些货币出现大的变动（印象中有过一次卢布大跌，苹果调整过俄区的价格），价格等级表可以点击 `所有价格和货币` 查看。

另外要注意：苹果内购是需要抽取30%的分成，实际结算是分成之前需要先扣除交易税，不同地区交易税不同，具体分成数额参看价格表。

iOS 11 用户可以在 App Store 内 App 的下载页面内直接购买应用的内购商品，这项功能苹果称作做 `Promoting In-App Purchases`，如果你的 App 需要在 App Store 推广自己的内购商品，则需要在 `App Store 推广` 里上传推广用的图像，另外苹果也在 iOS11 SDK 里面新增了从 App Store 购买内购项目跳转到 App 的新方法。

###### iTunes Connect 后台选择 `用户和职能`，选择 `+` 添加测试账号。

**填写沙箱测试账号信息需要注意以下几点**：

- 电子邮件不能是别人已经注册过 AppleID 的邮箱
- 电子邮箱可以不是真实的邮箱，但是必须符合邮箱格式
- App Store 地区的选择，测试的时候弹出的提示框以及结算的价格会按照沙箱账号选择的地区来，建议测试的时候新建几个不同地区的账号进行测试

**配置好测试账号之后，看一下沙箱账号测试的时候如何使用：**

- 首先沙箱测试账号必须在真机环境下进行测试，并且是 adhoc 证书或者 develop 证书签名的安装包，沙盒账号不支持直接从 App Store 下载的安装包
- 去真机的 App Store 退出真实的 Apple ID 账号，退出之后并不需要在App Store 里面登录沙箱测试账号
- 然后去 App 里面测试购买商品，会弹出登录框，选择 使用现有的 Apple ID，然后登录沙箱测试账号，登录成功之后会弹出购买提示框，点击 购买，然后会弹出提示框完成购买


# 税务信息

1. 登录 iTunes Connect

2. 协议、税务和银行业务


# 内购实现

**写代码之前先来了解对比一下 IPA 和支付宝支付，首先看支付宝的支付流程：**

- App 发起一笔支付交易，然后服务端根据支付宝的要求把订单信息进行加密签名
- 服务端把加密的交易信息返回给 App，App 拿到交易信息调用支付宝的 SDK，把支付信息给到支付宝的服务端验证
- 验证通过后，App 跳转到支付宝 App 或者网页版支付宝，用户使用支付宝进行支付
- 支付成功后从支付宝 App 跳转回到我们自己 APP，我们在 App 里处理回调结果刷新UI等
- 同时支付宝的服务器也会回调我们自己服务器，把收据传给服务器，支付宝服务器会一直回调我们的服务器直到我们的服务器确认收到收据
- 我们的服务器收到回调确认之后，确认订单支付成功
- 为了以防万一，App 上回调返回成功之后我们还需要去自己服务器验证是否真的支付成功（一切以服务器为准）

**微信支付和支付宝支付的流程是类似的，来看看 IAP 的支付流程：**

- App 发起一笔内购支付，然后服务端生成一个订单号并且返回给 App
- App 拿到交易订单之后调用 IPA 创建一个 IPA 交易，并且添加到支付队列
- 然后 IAP 会调用 Apple ID 支付页面等待用户确认支付，IPA 和苹果自己的 IPA 服务器通讯，回调购买成功，并且把收据写入 App 沙盒
- 然后 App 去沙盒获取收据并且上传到自己的服务器
- 服务器去 IAP 服务器查询收据的有效性并且对应到某个订单号，如果有效就通知 App，并且发放该内购商品，App 调用IAP 支付队列去结束该 IPA 交易

对比来看两者区别好像也不大，支付宝或者微信支付，一旦App 端支付成功，之后的验证工作就完全是我们的服务器和支付宝服务器之间的通讯了，服务端之间的通讯就保证了交易的可靠性，但是看看 IAP，同样的交易，服务端的验证却需要 App 端去驱动，由于 App 的网络环境比服务端复杂、用户操作的不确定性可能会导致 APP 无法正确的驱动服务端验证交易，另一方面 IAP 的服务器在美国，验证查询交易的延迟也很严重

**IAP 的代码看起来并不多流程也比较清晰，主要是下面几步：**

- 根据内购商品的产品 ID 初始化一个 `SKProductsRequest` 对象，调用该对象的 `start()` 方法进行内购商品的请求
- 把商品请求中获取到的 `SKProduct` 对象生成一个 `SKPayment` 对象，并把它压入到 `SKPaymentQueue` 支付队列中
- 然后从支付队列的代理方法 `func paymentQueue(_ queue: SKPaymentQueue`, `updatedTransactions transactions: [SKPaymentTransaction])` 里面获取到交易（transaction）的状态，交易完成后调用支付队列的 `finishTransaction()`完成内购支付

![内购流程形象图](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E8%B4%AD%E8%AF%B7%E6%B1%82%E5%BD%A2%E8%B1%A1%E5%9B%BE.png)

![内购业务逻辑图](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/%E5%86%85%E8%B4%AD%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

![内购流程](https://raw.githubusercontent.com/ouyangrong1313/MarkdownPhotos/master/img/20210714152826.png)

## 内购的核心流程：

①客户端发起支付订单

②客户端监听购买结果

③苹果回调订单购买成功时，客户端把苹果给的receipt_data和一些订单信息上报给服务器

④后台服务器拿receipt_data向苹果服务器校验

⑤苹果服务器向返回status结果，含义如下，其中为0时表示成功。

```
21000 App Store无法读取你提供的JSON数据
21002 收据数据不符合格式
21003 收据无法被验证
21004 你提供的共享密钥和账户的共享密钥不一致
21005 收据服务器当前不可用
21006 收据是有效的，但订阅服务已经过期。当收到这个信息时，解码后的收据信息也包含在返回内容中
21007 收据信息是测试用（sandbox），但却被发送到产品环境中验证
21008 收据信息是产品环境中使用，但却被发送到测试环境中验证
```

⑥服务器发现订单校验成功后，会把这笔订单存起来，transaction_id用MD5值映射下，保存到数据库，防止同一笔订单，多次发放内购商品。


# 避坑指南

1. 点击购买没有弹出输入账户密码框。

解决方法：到手机设置里面 iTunes Store 与 App Store 里面注销你原本的账号。

2. 运行程序的时候，账户中明明添加了商品，但是无法获得商品ID。

解决方法：Capabilities -> In-App Purchase 设置 ON。

3. 丢单处理

- 用户输入完 Apple ID 密码或者验证完指纹支付成功之后，网络突然中断导致 IAP 没有收到支付成功的通知，App 就无法在支付队列的代理方法中获取支付成功的通知，后续的发放内购商品也就不可能了
- App 在代理方法里收到了支付成功的通知，但是 App 上传交易收据到我们服务器去查询的时候如果查询失败，那么服务器就无法发放内购商品，因为这个行为是 App 驱动服务器的行为，这里有个坑就是支付队列的代理方法 func paymentQueue(_ queue: SKPaymentQueue, updatedTransactions transactions: [SKPaymentTransaction]) 需要下次 App 重新启动才会重新调用，这个时候我们 App 才能重新去驱动服务器查询交易，由于用户操作的不确定性，不知道什么时候用户才会重新打开App，发放内购商品的周期自然也不确定
- 之前有开发者反应，IAP 通知代理方法交易成功，但是沙盒里面取收据的时候发现为空，或者当前支付成功的订单并没有写入沙盒的收据，导致上传到服务器的收据查询不到结果
- 如果用户支付成功，收据也上传服务器成功，但是在服务器验证阶段用户删除了App，导致App 无法去处理这些没有被验证完的订单
- 如何处理越狱iOS手机内购的问题

以上问题都可能会导致用户支付成功了，却收不到我们发放的内购商品，统一起来称为：内购丢单

客户端必须要给服务器传的三个参数：receipt_data， product_id ，transaction_id

```
//该方法为监听内购交易结果的回调
- (void)paymentQueue:(SKPaymentQueue *)queue updatedTransactions:(NSArray<SKPaymentTransaction *> *)transactions
transactions 为一个数组 遍历就可以得到 SKPaymentTransaction 对象的元素transaction。然后从transaction里可以取到以下这两个个参数，product_id，transaction_id。另外从沙盒里取到票据信息receipt_data
我们先看怎么取到以上的三个参数
//获取receipt_data
NSData *data = [NSData dataWithContentsOfFile:[[[NSBundle mainBundle] appStoreReceiptURL] path]];
NSString * receipt_data = [data base64EncodedStringWithOptions:0];
//获取product_id
NSString *product_id = transaction.payment.productIdentifier;
//获取transaction_id
NSString * transaction_id = transaction.transactionIdentifier;
这是我们必须要传给服务器的三个字段。以上三个字段需要做好空值校验，避免崩溃。
下面我们来解释一下，为什么要给服务器传这三个参数。
receipt_data：这个不解释了 大家都懂 不传的话 服务器根本没法校验
product_id：这个也不用解释 内购产品编号 你不传的话 服务器不知道你买的哪个订单
transaction_id：这个是交易编号，是必须要传的。因为你要是防止越狱下内购被xx就必须要校验in_app这个参数。而这个参数的数组元素有可能为多个，你必须得找到一个唯一标示，才可以区分订单到底是那一笔。
```


# 后台处理

前面说到用户支付成功之后，我们拿到沙盒的收据信息去苹果的 IAP 服务器去验证，这里既可以直接在 App 端验证也可以让服务器去验证，实际上根据我的测试，App 端直接去IAP服务器验证比较快，毕竟中间少了很多步骤，但是考虑到越狱的 iOS 设备完全可以在系统层面跳过或者伪造收据，早期的 iOS 开发很多公司都是采用都是这种本地验证，但是现在基本都是通过后台验证的方式，具体的后台验证步骤如下：

- App端拿到沙盒的收据（receipt-data）,进行一次base64编码，上传给服务器
- 服务器拿到收据之后发到 IAP 服务器去验证，验证成功之后收据需要和自己的订单号进行映射并且记录在数据库，之后每次验证之前都需要先判断收据是否存在，防止 App 端重复上传相同的收据，重复发放内购商品
- 服务器发放内购商品，推送通知给用户等

由于 App 上线 App Store 之前我们是使用沙盒账号测试的，沙盒测试的收据验证也是要去沙盒收据的服务器验证。

- 沙盒环境验证服务器：https://sandbox.itunes.apple.com/verifyReceipt
- 正式环境验证服务器：https://buy.itunes.apple.com/verifyReceipt

而且苹果在上线审核的时候也是使用沙盒账号测试的，那如何识别App端发过来的收据是沙盒测试还是正式环境用户的购买呢？这里服务端就要采用双重验证，即先把收据拿到正式环境的验证地址去验证，如果苹果的正式环境验证服务器返回的状态码 status 为 21007，则说明当前收据是沙盒环境产生，则再连接一次沙盒环境服务器进行验证，这样不管是我们自己采用沙盒账号测试还是苹果审核人员采用沙盒账号进行审核、或者用户购买都可以保证收据正常的验证成功。

①先判重，避免重复分发内购商品。收到客户端上报的 transaction_id 后，直接MD5后去数据库查，能查到说明是重复订单，返回相应错误码给客户端，如果查不到，去苹果那边校验。

②服务器拿到苹果的校验结果后，首先判断订单状态是不是成功。

③如果订单状态成功在判断in_app这个字段有没有，没有直接就返回失败了。如果存在的话，遍历整个数组，通过客户端给的transaction_id 来比较，取到相同的订单时，对比一下bundle_id ，product_id 是不是正确的。

如果以上校验都正确就把这笔订单充值进去，给用户分发内购商品。

注意：一定要告诉后台，不论校验是否成功，只要客户端给服务器传了receipt_data等参数就一定要保存到数据库里。

## Tips

- iOS端传过来的苹果回调收据信息需base64加密，如果有严重的错误问题，注意收据信息的特殊符号替换，eg:"%2B"。
- 苹果内购订阅型验证服务器需多加共享密钥（由iOS开发人员提供给你）验证，如果是添加的公共秘钥，那么消耗型验证也需要加上秘钥验证。
- 苹果内购消耗型订单传过来的订单是在in_app数组里，而自动订阅型续订的最新数据都在latest_receipt_info数组里。

## 自动订阅续费

- 添加server to server 通知

latest_expired_receipt_info 用于自动续订。过期订阅的收据的JSON表示形式，仅当通知类型为RENEWAL或CANCEL或订阅过期且续订失败时返回。项目集成请看官网有介绍。

- 服务端server轮询要过期和过期的订单数据，主动向苹果服务器验证。


# GitHub Demo

[MQCCoder/XYIAPKit](https://github.com/MQCCoder/XYIAPKit)


# 参考文章

[App 内购买项目配置流程](https://help.apple.com/app-store-connect/#/devb57be10e7)

[iOS 内购（In-App Purchase）总结](https://www.gowhich.com/blog/1010)

[iOS开发支付篇——内购(IAP)详解](https://www.cnblogs.com/shoshana-kong/p/10991586.html)

[iOS内购全面实战](https://www.jianshu.com/p/2f98b7937b6f)

[iOS内购（IAP）自动续订订阅类型总结](https://www.jianshu.com/p/9531a85ba165)

[IOS 内购IAP 自动订阅收据验证文档服务端翻译](https://blog.csdn.net/qq_24909089/article/details/103202428)

[iOS内购（IAP）自动续订订阅类型服务端总结](https://blog.csdn.net/qq_23564667/article/details/105512349)

[springboot接入苹果内购](http://ifumei.cc/2019/12/24/iospay/)

[java(jfinal) 接入ios内购（连续包月订阅），服务端进行二次验证](https://www.xiaoxustudent.top/p/400)

[iOS 内购（In-App Purchase）总结](https://xiaovv.me/2018/05/03/My-iOS-In-App-Purchase-Summarize/)
