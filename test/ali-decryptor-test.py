# -*- coding: utf-8 -*-
import os
import sys
import logging
import inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from m3u8downloader.downloader import M3U8Downloader
from keydecryptor.ali import AliKeyDecryptor

def decryptTS(tsfile, resultfile):
    video = None
    key = None
    iv = None

    with open(os.path.join(".", tsfile), 'rb') as f:
        video = f.read()

    key_file_name = tsfile + ".key"
    with open(os.path.join(".", key_file_name), 'rb') as f:
        key = f.read()

    key = AliKeyDecryptor().decrypt(key)

    iv_file_name = tsfile + ".iv"
    with open(os.path.join(".", iv_file_name), 'rb') as f:
        iv = f.read()

    result = downloader.decrypt(key, iv, video)
    with open(os.path.join(".", resultfile), 'wb') as f:
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

    file_name = "ali-ts/e_20170519032524-ggauw1x00qo0okgk-conv_hd_seg_0.ts"
    r1 = "ali-ts/intro.ts"
    decryptTS(file_name, result_name)

    file_name = "ali-ts/e_20170630095028-3xsfwyxw20cgwws8-conv_hd_seg_0.ts"
    r2 = "ali-ts/0.ts"
    decryptTS(file_name, result_name)

    file_name = "ali-ts/e_20170630095028-3xsfwyxw20cgwws8-conv_hd_seg_1.ts"
    r3 = "ali-ts/1.ts"
    decryptTS(file_name, result_name)

    downloader.combineTS([r1, r2, r3], "long.ts")

    