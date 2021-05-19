# 测试工具
本测试工具包含在项目开发过程中和开发有的一些测试用例。

## download.py

普通的m3u8下载过程可以使用`download.py`直接下载。为了能够控制下载流程，该脚本通过命令行控制。例如：

```bash
python download.py download "https://devstreaming-cdn.apple.com/videos/wwdc/2017/515vy4sl7iu70/515/hls_vod_mvp.m3u8" #下载m3u8文件到本地，会在当前目录创建一个tmp文件夹，并把m3u8文件保存在tmp文件夹中
python download.py parse ./tmp/index.m3u8 -r "https://devstreaming-cdn.apple.com/videos/wwdc/2017/515vy4sl7iu70/515/hls_vod_mvp.m3u8" #下载index.m3u8中包含的key，iv和ts数据，并按照顺序从0-n保存。例如，0.key, 0.ts, 1.ts
python download.py decrypt ./tmp/index.m3u8 -p f #解密ts文件，目前只支持默认的AES解密。解密后的ts文件保存为带前缀的文件。例如：f_0.ts, f_1.ts
python download.py combine ./tmp/index.m3u8 -p f -d one.ts #把所有ts文件按照在index.m3u8中的顺序组合为一个one.ts文件。如果组合解密的文件，可以设置前缀确保脚本读取正确的文件。例如：f_0.ts, f_1.ts
```

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

```bash
ln -s qqvideolite /sdcard/Android/data/com.tencent.videolite.android/files/videos
python combine-ts.py ~/qqvideolite/r075832cr9b.322003.hls /sdcard/DCIM/result.ts
```

[《保存腾讯视频离线视频》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e5%a4%96%e4%bc%a0%e4%ba%8c%ef%bc%9a%e4%bf%9d%e5%ad%98%e8%85%be%e8%ae%af%e8%a7%86%e9%a2%91%e7%a6%bb%e7%ba%bf%e8%a7%86%e9%a2%91.html "保存腾讯视频离线视频")

## 关于我们
如果大家对本项目有任何建议，想法或者问题，可以添加微信号：`fish_loves_cat`

或者扫码联系船长：

<img src="https://jmsliu.cn/wp-content/uploads/2019/06/qr.jpg" alt="fish_loves_cat" width="200" height="200">