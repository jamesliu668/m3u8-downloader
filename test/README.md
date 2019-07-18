# 测试工具
本测试工具包含在项目开发过程中和开发有的一些测试用例。

## ali-downloader-test
阿里大学TS视频下载测试工具。可以使用以下步骤使用测试工具：

1. 登陆阿里大学找一个视频页面
2. 拷贝当前页面的Cookie信息
3. 拷贝视频的m3u8视频URL

这里需要注意的是，阿里大学的m3u8视频URL只能访问一次就会过期，所以在拷贝之前必须确保该URL没有使用过。具体步骤可以参考：


## ali-decryptor-test
阿里大学TS视频，以及密钥解密测试工具。 该测试工具主要：

1. 解密了0-9的TS视频
2. 将0-9的TS视频合并为一段长视频long.ts

大家可以使用以下命令将TS视频文件转换为MP4文件：
```
ffmpeg -y -i long.ts -c:v libx264 -c:a copy -bsf:a aac_adtstoasc long.mp4
```


## 关于我们
如果大家对本项目有任何建议，想法或者问题，可以添加微信号：`fish_loves_cat`

或者扫码联系船长：

<img src="https://jmsliu.cn/wp-content/uploads/2019/06/qr.jpg" alt="fish_loves_cat" width="200" height="200">