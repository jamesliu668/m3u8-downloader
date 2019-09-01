# -*- coding: utf-8 -*-
# 合并腾讯视频极速版离线TS文件

import os
import sys
import logging
import inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from m3u8downloader.downloader import M3U8Downloader

if __name__ == '__main__':
    LOG_LEVEL = logging.INFO
    log = logging.getLogger()
    log.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    if len(sys.argv) < 3:
        print("python combine-ts.py hls video.ts")
    else:
        downloader = M3U8Downloader(log)
        tsPath = sys.argv[1]
        tsFilePath = sys.argv[2]
        baseFolderName = tsPath.split("/")[-1]
        tsFileList = []
        moreFile = True
        index = 0
        while moreFile:
            tsFolder = baseFolderName + "_" + str(index)
            index = index + 30
            tsFolder = tsFolder + "_" + str(index - 1)
            tsFolder = os.path.join(tsPath, tsFolder)

            if os.path.exists(tsFolder):
                moreFile = True
                for i in range(index - 30, index):
                    ts = os.path.join(tsFolder, str(i) + ".ts")
                    if os.path.exists(ts):
                        tsFileList.append(ts)
            else:
                moreFile = False

        downloader.combineTS(tsFileList, tsFilePath)