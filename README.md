# M3U8（TS）视频下载工具
本软件包可以方便的下载M3U8视频，支持加密的和非加密的TS文件下载，解密，和合并。

## 使用方法
使用以下命令下载本项目到本地：

```bash
git clone https://github.com/jamesliu668/m3u8-downloader.git
```

在项目中import该工具包

```python
from m3u8downloader.downloader import M3U8Downloader
```

下载M3U8文件和TS文件

```python
log = logging.getLogger()
downloader = M3U8Downloader(log)
m3u8URL = "replace with your m3u8 file url"
m3u8 = downloader.downloadM3U8(m3u8URL)
downloader.downloadTS(m3u8, ".")
```

## 更多学习资料
关于更多的使用方法，可以参考`test`文件夹中的测试样例。另外，以下是几篇非常有用的文章：

[《M3U8视频文件详解》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a7%a3%e4%b8%80%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e6%96%87%e4%bb%b6%e8%af%a6%e8%a7%a3.html "M3U8视频文件详解")

[《M3U8视频网络数据分析与爬虫设计》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a7%a3%e4%ba%8c%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e7%bd%91%e7%bb%9c%e6%95%b0%e6%8d%ae%e5%88%86%e6%9e%90%e4%b8%8e%e7%88%ac.html "M3U8视频网络数据分析与爬虫设计")

[《M3U8视频网络数据爬虫实现》](https://jmsliu.cn/others/m3u8%e6%b5%81%e8%a7%86%e9%a2%91%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e8%af%a6%e8%a7%a3%e4%b8%89%ef%bc%9am3u8%e8%a7%86%e9%a2%91%e7%bd%91%e7%bb%9c%e6%95%b0%e6%8d%ae%e7%88%ac%e8%99%ab%e5%ae%9e%e7%8e%b0.html "M3U8视频网络数据爬虫实现")

## 关于我们
如果大家对本项目有任何建议，想法或者问题，可以添加微信号：`fish_loves_cat`

或者扫码加好友：

![fish_loves_cat][qrcode]

[qrcode]: https://jmsliu.cn/wp-content/uploads/2019/06/qr.jpeg "fish_loves_cat"
