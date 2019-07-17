# -*- coding: utf-8 -*-
import os
import sys
import logging
import inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from m3u8downloader.downloader import M3U8Downloader
from keydecryptor.ali import AliKeyDecryptor

def decryptTS(keyFile, ivFile, tsFile, resultfile):
    video = None
    key = None
    iv = None

    with open(tsFile, 'rb') as f:
        video = f.read()

    with open(keyFile, 'rb') as f:
        key = f.read()

    key = AliKeyDecryptor().decrypt(key)

    with open(ivFile, 'rb') as f:
        iv = f.read()

    result = downloader.decrypt(key, iv, video)
    with open(resultfile, 'wb') as f:
        f.write(result)


if __name__ == '__main__':
    LOG_LEVEL = logging.INFO
    log = logging.getLogger()
    log.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    downloader = M3U8Downloader(log)

    currentFolder = os.path.dirname(os.path.realpath(__file__))
    ts = os.path.join(currentFolder, "ali-ts/0.ts")
    key = os.path.join(currentFolder, "ali-ts/0.key")
    iv = os.path.join(currentFolder, "ali-ts/0.iv")
    r0 = os.path.join(currentFolder, "ali-ts/r0.ts")
    decryptTS(key, iv, ts, r0)

    ts = os.path.join(currentFolder, "ali-ts/1.ts")
    key = os.path.join(currentFolder, "ali-ts/1.key")
    iv = os.path.join(currentFolder, "ali-ts/1.iv")
    r1 = os.path.join(currentFolder, "ali-ts/r1.ts")
    decryptTS(key, iv, ts, r1)

    ts = os.path.join(currentFolder, "ali-ts/2.ts")
    iv = os.path.join(currentFolder, "ali-ts/2.iv")
    r2 = os.path.join(currentFolder, "ali-ts/r2.ts")
    decryptTS(key, iv, ts, r2)

    ts = os.path.join(currentFolder, "ali-ts/3.ts")
    iv = os.path.join(currentFolder, "ali-ts/3.iv")
    r3 = os.path.join(currentFolder, "ali-ts/r3.ts")
    decryptTS(key, iv, ts, r3)

    ts = os.path.join(currentFolder, "ali-ts/4.ts")
    iv = os.path.join(currentFolder, "ali-ts/4.iv")
    r4 = os.path.join(currentFolder, "ali-ts/r4.ts")
    decryptTS(key, iv, ts, r4)

    ts = os.path.join(currentFolder, "ali-ts/5.ts")
    iv = os.path.join(currentFolder, "ali-ts/5.iv")
    r5 = os.path.join(currentFolder, "ali-ts/r5.ts")
    decryptTS(key, iv, ts, r5)

    ts = os.path.join(currentFolder, "ali-ts/6.ts")
    iv = os.path.join(currentFolder, "ali-ts/6.iv")
    r6 = os.path.join(currentFolder, "ali-ts/r6.ts")
    decryptTS(key, iv, ts, r6)

    ts = os.path.join(currentFolder, "ali-ts/7.ts")
    iv = os.path.join(currentFolder, "ali-ts/7.iv")
    r7 = os.path.join(currentFolder, "ali-ts/r7.ts")
    decryptTS(key, iv, ts, r7)

    ts = os.path.join(currentFolder, "ali-ts/8.ts")
    iv = os.path.join(currentFolder, "ali-ts/8.iv")
    r8 = os.path.join(currentFolder, "ali-ts/r8.ts")
    decryptTS(key, iv, ts, r8)

    ts = os.path.join(currentFolder, "ali-ts/9.ts")
    iv = os.path.join(currentFolder, "ali-ts/9.iv")
    r9 = os.path.join(currentFolder, "ali-ts/r9.ts")
    decryptTS(key, iv, ts, r9)

    finalVideo = os.path.join(currentFolder, "ali-ts/long.ts")
    downloader.combineTS([r0, r1, r2, r3, r4, r5, r6, r7, r8, r9], finalVideo)