# 测试工具
本测试工具包含在项目开发过程中和开发有的一些测试用例。

## download
尝试下载apple的m3u8视频。主要步骤是：

1. 拷贝粘贴m3u8的视频链接
2. 下载m3u8的文件内容
3. 解析m3u8文件内容并获取TS文件播放列表
4. 保持所有的ts视频片段到tmp文件夹中
5. 合并所有的ts视频片段为一个完整的视频

这里需要注意的是Apple官方网站对于视频做了保护，现在这个视频已经无法正常下载了。目测应该需要动态的获取m3u8文件的地址。

## ali-downloader-test
阿里大学TS视频下载测试工具。可以根据以下步骤使用测试工具：

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

## newcoder-downloader-test
牛客网的TS视频下载测试工具。可以根据以下步骤使用测试工具：

1. 登陆牛客网找一个视频页面
2. 系统必须安装Selenium和Chrome WebDriver
3. 拷贝当前页面的Cookie信息，Referer和User-Agent
4. 拷贝当前页面URL

## newcoder-decryptor-test
牛客网的TS视频，以及密钥解密测试工具。 该测试工具主要：

1. 下载对应的视频信息
2. 解密视频信息
3. 从视频信息中获取加密密钥的密钥
4. 解密TS的加密密钥
5. 解密TS文件
6. 合并TS文件

## combine-ts
合并安卓平板电脑中腾讯视频极速版的离线视频文件。在安卓平板上安装腾讯视频极速版以后，下载需要看的视频。随后在平板电脑上安装Termux（虚拟Linux终端），并安装OpenSSH和Python。上传该项目后使用以下命令可以合并TS离线视频文件，并保存到相册文件夹中。

```
ln -s qqvideolite /sdcard/Android/data/com.tencent.videolite.android/files/videos
python combine-ts.py ~/qqvideolite/r075832cr9b.322003.hls /sdcard/DCIM/result.ts
```

[《保存腾讯视频离线视频》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e5%a4%96%e4%bc%a0%e4%ba%8c%ef%bc%9a%e4%bf%9d%e5%ad%98%e8%85%be%e8%ae%af%e8%a7%86%e9%a2%91%e7%a6%bb%e7%ba%bf%e8%a7%86%e9%a2%91.html "保存腾讯视频离线视频")

## 关于我们
如果大家对本项目有任何建议，想法或者问题，可以添加微信号：`fish_loves_cat`

或者扫码联系船长：

<img src="https://jmsliu.cn/wp-content/uploads/2019/06/qr.jpg" alt="fish_loves_cat" width="200" height="200">