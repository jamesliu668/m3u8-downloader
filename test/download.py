# -*- coding: utf-8 -*-
import argparse
import logging
import logging.handlers
import traceback
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from m3u8downloader.downloader import M3U8Downloader

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
logFolder = os.path.join(__location__, 'logs')

if not os.path.exists(logFolder):
    os.makedirs(logFolder)

logFileName = os.path.join(logFolder, 'm3u8.log')
log = logging.getLogger()
log.setLevel(logging.DEBUG)
fileHandler = logging.handlers.TimedRotatingFileHandler(logFileName, 'D', 1, 30)
fileHandler.suffix = "%Y%m%d.log"
formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
log.addHandler(handler)


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

if __name__ == '__main__':
    #读取命令行
    parser = argparse.ArgumentParser(description='Start Download M3U8')
    parser.add_argument('task', choices = ["download", "parse", "decrypt", "combine"], type = str, help='Download m3u8 file or parse m3u8 file.')
    parser.add_argument('path', type = str, help='url or file path')
    parser.add_argument('-r', type = str, dest='rootURL', help='root url of m3u8')
    parser.add_argument('-p', type = str, dest='prefix', default="",  help='The short ts file prefix. E.g. "z" for "z_0.ts"')
    parser.add_argument('-d', type = str, dest='finalPath', default="final.ts", help='The final long ts file path')
    args = parser.parse_args()

    # download m3u8 file
    if args.task == "download":
        m3u8URL = args.path
        m3u8FileName = m3u8URL.split("/")[-1]
        m3u8List = downloader.downloadM3U8(m3u8URL)
        if m3u8List and len(m3u8List) > 0:
            for key in m3u8List.keys():
                downloader.saveToFile(m3u8List[key], f"{key}.m3u8", os.path.join(__location__, "tmp"))

    # download all data in m3u8, including key, iv, and ts
    if args.task == "parse" and args.rootURL:
        filePath = args.path
        downloader.rootURL = args.rootURL
        m3u8 = downloader.readFile(filePath).decode('utf-8')
        ts_list = downloader.parseTS(m3u8)
        
        # you can change the start index for continuous downloading. E.g. ts_list[11:0]
        tsList = []

        index = 0
        for item in ts_list[0:]:
            log.debug(f"Download and save item@{index}")
            index += 1
            if 'ts' in item:
                ts = downloader.download(item['ts'])
                result = downloader.saveToFile(ts, f"{len(tsList)}.ts", os.path.join(__location__, "tmp"))
                tsList.append(result)

            if 'key' in item:
                key = downloader.download(item['key'])
                result = downloader.saveToFile(key, f"{len(tsList)}.key", os.path.join(__location__, "tmp"))

            if 'iv' in item:
                iv = downloader.download(item['iv'])
                result = downloader.saveToFile(iv, f"{len(tsList)}.iv", os.path.join(__location__, "tmp"))

    if args.task == "decrypt":
        prefix = args.prefix
        filePath = args.path
        m3u8 = downloader.readFile(filePath).decode('utf-8')
        ts_list = downloader.parseTS(m3u8)
        currentKey = None
        currentIv = None
        tsList = []
        for item in ts_list[0:]:
            if 'ts' in item:
                tsIndex = len(tsList)
                tsPath = os.path.join(__location__, "tmp", f"{tsIndex}.ts")
                ts = downloader.readFile(tsPath)

                keyPath = os.path.join(__location__, "tmp", f"{tsIndex}.key")
                key = downloader.readFile(keyPath)
                if key:
                    currentKey = key

                ivPath = os.path.join(__location__, "tmp", f"{tsIndex}.iv")
                iv = downloader.readFile(ivPath)
                if iv:
                    currentIv = iv

                if currentKey:
                    out = downloader.decrypt(currentKey, currentIv, ts)
                    tsPath = downloader.saveToFile(out, f"{prefix}{tsIndex}.ts", os.path.join(__location__, "tmp"))
                
                tsList.append(tsPath)



    if args.task == "combine":
        prefix = args.prefix if len(args.prefix) > 0 else ""
        fullFilePath = args.finalPath
        filePath = args.path
        m3u8 = downloader.readFile(filePath).decode('utf-8')
        ts_list = downloader.parseTS(m3u8)

        tsList = []
        for item in ts_list[0:]:
            if 'ts' in item:
                tsIndex = len(tsList)
                tsPath = os.path.join(__location__, "tmp", f"{prefix}{tsIndex}.ts")
                tsList.append(tsPath)

        downloader.combineTS(tsList, fullFilePath)