# -*- coding: utf-8 -*-
import os
import sys
import logging
import inspect
import re
import hashlib
import copy
import base64
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from m3u8downloader.downloader import M3U8Downloader

def decryptTS(tsfile, resultfile, keyfile, ivfile):
    video = None
    key = None
    iv = None

    with open(tsfile, 'rb') as f:
        video = f.read()

    key_file_name = os.path.join(currentFolder, keyfile)
    with open(key_file_name, 'rb') as f:
        key = f.read()

    iv_file_name = os.path.join(currentFolder, ivfile)
    with open(iv_file_name, 'rb') as f:
        iv1 = f.read()

    video_id_name = os.path.join(currentFolder, "tmp1/video_id")
    with open(video_id_name, 'r') as f:
        video_id = f.read()

    body = getBody(video_id)
    json = decryptVideoJson(video_id, body)
    json = str(json, encoding = "utf8")
    regex = re.compile(r'seed_const":.*?,')
    seed_const = regex.findall(json)[0][12:-1]
    m2 = hashlib.md5()
    m2.update(seed_const.encode('utf-8'))
    i = m2.hexdigest()
    i = i[0:16]
    i = bytes(i, encoding="utf8")
    iv = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 7, 5, 3, 2, 1]
    iv = bytes(iv)
    key = downloader.decrypt(i, iv, key)[0:16]
    iv =[182, 225, 80, 143, 231, 211, 167, 164, 71, 64, 110, 174, 127, 230, 89, 117]
    iv = bytes(iv)
    result = downloader.decrypt(key, iv, video)
    with open(resultfile, 'wb') as f:
        f.write(result)

def b(e,t=None):
    if t == None or t.lower().replace(" ","").replace("-","") == "utf8":
        i = []
        r = 0
        while(r < len(e)):
            n = ord(e[r:r+1])
            if n == 37:
                n = hex(int(e[r:r+2]))
                i.append(n)
            else:
                i.append(n)
            r += 1
        return i
    elif t.lower() == "hex":
        i = []
        r = 0
        while (r < len(e)):
            n = ord(e[r:r + 1])
            n = hex(int(e[r:r + 2]))
            i.append(n)
            r += 1
        return i
    else:
        i = []
        return i
        
def funa(e):
    """两位16进制转10进制"""
    t = []
    i = 0
    dic = {"0":0,
           "1":1,
           "2":2,
           "3":3,
           "4":4,
           "5":5,
           "6":6,
           "7":7,
           "8":8,
           "9":9,
           "a":10,
           "b":11,
           "c":12,
           "d":13,
           "e":14,
           "f":15}
    while i < len(e):
        a = dic[e[i]]
        b = dic[e[i+1]]
        t.append(a*16+b)
        i += 2
    return t

# download video info and we will find the key which will be used to descrypt key for TS file
def getBody(video_id):
    content = downloader.download("https://player.polyv.net/secure/" + video_id + ".json")
    content = str(content)
    regex = re.compile(r'body": ".*"')
    content = regex.findall(content)[0][8:-1]
    return content

# decrypt the video info we will find the key which will be used to descrypt key for TS file
def decryptVideoJson(video_id, body):
    t = video_id
    m2 = hashlib.md5()
    m2.update(t.encode('utf-8'))
    i = m2.hexdigest()
    r = b(i[0:16])
    r = bytes(r)
    n = b(i[16:32])
    n = bytes(n)
    a = funa(body)
    a = bytes(a)
    result = downloader.decrypt(r,n,a)
    result = base64.b64decode(result)
    return result

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
    downloader.setHeaders({
        "Origin": "https://www.nowcoder.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer": "https://www.nowcoder.com/study/vod/1041/1/1"
    })

    currentFolder = os.path.dirname(os.path.realpath(__file__))
    keyfile = "tmp1/c7d3982d0d4360a289c58754dbdfd80f_2_0.key"
    ivfile = "tmp1/c7d3982d0d4360a289c58754dbdfd80f_2_0.iv"
    ls = []
    for filename in os.listdir(os.path.join(currentFolder, "tmp1")):
        if(filename.endswith(".ts")):
            file_name = os.path.join(currentFolder, "tmp1/"+filename)
            r1 = os.path.join(currentFolder, "10/"+filename)
            decryptTS(file_name, r1, keyfile, ivfile)
            ls.append(r1)

    downloader.combineTS(ls, "10.ts")