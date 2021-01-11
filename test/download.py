# -*- coding: utf-8 -*-

import logging
import traceback
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from m3u8downloader.downloader import M3U8Downloader

log = logging.getLogger()
downloader = M3U8Downloader(log)

# set proxy
# downloader.setProxy({
#         'http': 'http://127.0.0.1:58591',
#         'https': 'http://127.0.0.1:58591',
#     }
# )

# downloader.setHeaders({
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6,zh;q=0.5",
#     "Cache-Control": "no-cache",
#     "Connection": "keep-alive",
#     "Pragma": "no-cache",

#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-site",
#     "Host":"devstreaming-cdn.apple.com",
#     "Origin":"https://developer.apple.com",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
#     "Referer" : "https://developer.apple.com/videos/play/wwdc2017/515/",
# })

# set the m3u8 url
m3u8URL = "https://devstreaming-cdn.apple.com/videos/wwdc/2017/515vy4sl7iu70/515/hls_vod_mvp.m3u8"
# download m3u8 data
m3u8 = downloader.downloadM3U8(m3u8URL)
# get ts video list
ts_list = downloader.parseTS(m3u8)
log.info("Found {} ts videos".format(len(ts_list)))
# save all ts videos in tmp file
tsFileList = []
currentFolder = os.path.dirname(os.path.realpath(__file__))
# you can change the start index for continuous downloading. E.g. ts_list[11:0]
for item in ts_list[0:]:
    if 'ts' in item:
        ts = downloader.download(item['ts'])
        filename = item['ts'].split("/")[-1].split(".ts")[0]
        try:
            result = downloader.saveToFile(ts, filename + ".ts", os.path.join(currentFolder, "tmp"))
            tsFileList.append(result)
        except:
            traceback.print_exc()
# combine all small ts video segments into a full video file one.ts
fullTSFile = os.path.join(currentFolder, "one.ts")
downloader.combineTS(tsFileList, fullTSFile)

# in the end, we will get one.ts video file and we can use FFmpeg to convert ts to mp4. 