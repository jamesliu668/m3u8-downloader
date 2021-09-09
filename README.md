# M3U8（TS）视频下载工具
本软件包可以方便的下载M3U8视频，支持加密的和非加密的TS文件下载，解密，和合并。

## 使用方法
使用以下命令下载本项目到本地：

```bash
git clone https://github.com/jamesliu668/m3u8-downloader.git
```

下载M3U8文件和TS文件

```bash
#下载m3u8视频流列表文件
python ./test/download.py download https://a.com/video/m3u8/index.m3u8
#下载m3u8视频流列表文件中的视频片段文件（可能加密）
python ./test/download.py parse ./test/tmp/index.m3u8 -r https://a.com/video/m3u8/index.m3u8
#解密视频片段文件，解密后的文件加前缀prefix_0.ts，避免覆盖原始文件。如果文件无加密，执行该命令不会生成prefix_0.ts文件
python ./test/download.py decrypt ./test/tmp/index.m3u8 -p prefix_
#合并片段文件，文件以prefix_作为前缀，例如prefix_0.ts。如果没有前缀，可以参略-p参数。
python ./test/download.py combine ./test/tmp/index.m3u8 -p prefix_ -d ./test/one.ts
```

## MacOS使用zip压缩视频
如果在MacOS中需要把视频打包压缩成zip文件，使用如下命令行：
```bash
zip -e one.zip ./test/one.ts
```

## MacOS中使用FFmpeg转换文件格式
如果想要将TS文件转换文件格式，比如转换为mp4。可以在Mac上安装FFmpeg并用最简单的方式做格式转换。如果对于编码有要求，还需要大家自己去网上搜索一下FFmpeg的相关参数。
```bash
#搜索ffmpeg
brew search ffmpeg
#安装ffmpeg
brew install ffmpeg
#视频格式转换
ffmpeg -i ./test/one.ts -c:v copy -c:a copy ./test/one.mp4
```

## 更多学习资料
关于更多的使用方法，可以参考`test`文件夹中的测试样例。另外，以下是几篇非常有用的文章：

[《M3U8视频文件详解》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a7%a3%e4%b8%80%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e6%96%87%e4%bb%b6%e8%af%a6%e8%a7%a3.html "M3U8视频文件详解")

[《M3U8视频网络数据分析与爬虫设计》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a7%a3%e4%ba%8c%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e7%bd%91%e7%bb%9c%e6%95%b0%e6%8d%ae%e5%88%86%e6%9e%90%e4%b8%8e%e7%88%ac.html "M3U8视频网络数据分析与爬虫设计")

[《M3U8视频网络数据爬虫实现》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a7%a3%e4%b8%89%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e7%bd%91%e7%bb%9c%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e5%ae%9e%e7%8e%b0.html "M3U8视频网络数据爬虫实现")

## 关于我们
如果大家对本项目有任何建议，想法或者问题，可以添加微信号：`fish_loves_cat`

或者扫码联系船长：

<img src="https://jmsliu.cn/wp-content/uploads/2019/06/qr.jpg" alt="fish_loves_cat" width="200" height="200">
