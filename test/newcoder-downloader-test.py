# -*- coding: utf-8 -*-
import os
import sys
import logging
import inspect
import traceback
from bs4 import BeautifulSoup
import re
import urllib
from selenium import webdriver
from http.cookies import SimpleCookie

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from m3u8downloader.downloader import M3U8Downloader


def getKeyRequestParam(oriURL, headers):
    try:
        browser = webdriver.Chrome()
        cookie = headers["cookie"]
        simple_cookie = SimpleCookie(cookie)
        browser.get(oriURL)
        for item in simple_cookie:
            format_cookie = {}
            format_cookie['name'] = item
            format_cookie['value'] = simple_cookie[item].value
            browser.add_cookie(cookie_dict=format_cookie)

        browser.get(oriURL)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        titles = soup.select("body  script")
        str = titles[-2].get_text()
        browser.close()
        regex = re.compile(r"videoId: '.*'")
        videoId = regex.findall(str)[0][10:-1]
        regex = re.compile(r"videoPlaySafe: '.*'")
        videoPlaySafe = regex.findall(str)[0][16:-1]
        return videoId, videoPlaySafe
    except:
        traceback.print_exc()


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
    # it's better to set the headers from your current browser here
    downloader.setHeaders({
        "Origin":"https://www.nowcoder.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" : "https://www.nowcoder.com/study/vod/1041/1/1",
        "cookie":"NOWCODERCLINETID=7E576843AAD6A48C69C4FEC9C5D2784F; _ga=GA1.2.271210318.1552288354; NOWCODERUID=817D390DB96D8CAE2C9F7E1E554F6A28; gdxidpyhxdE=uGcyhoRXafAcuWdzdtT8vRBgDHVmvYC5AV82O5MCXuukixnAP%2B6pfRN3kHbWRKlICIEDCst7Za5I6ID%2BiEcuz7b2WEaIvIg1y4y9UpkaAE%2F0MQvys%5CZdf1Y0ovff398cpGkbSwnfLZ9GL1uogPjEkQG0JMkOHCpsr2pq8lTfOw8Jp5dI%3A1563357666843; _9755xjdesxxd_=32; gr_user_id=4505d2e5-9b6b-4064-a202-40e66dd0432b; c196c3667d214851b11233f5c17f99d5_gr_last_sent_cs1=113433790; grwng_uid=6097ead7-9a65-4d18-9b1e-2ad15975cd9b; c196c3667d214851b11233f5c17f99d5_gr_cs1=113433790; callBack=%2Fstudy%2Fvod%2F1041%2F10%2F1%3F; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1565079570,1565079677,1565079699,1565851742; t=EEB92FD2F4FE354737D792BDAF3B44E7; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1565851747; SERVERID=aff739a092fc0d444b24c3a30d4864b6|1565851784|1565851739"
    })

    catcount = 10
    # m3u8URL = "https://hls.videocc.net/c7d3982d0d/f/c7d3982d0d4360a289c58754dbdfd80f_2.m3u8?pid=1563756868775X1523162&device=desktop"
    oriURL = "https://www.nowcoder.com/study/vod/1041/10/1"
    videoId, keyRequestParam = getKeyRequestParam(oriURL,downloader.headers)
    m3u8URL = "https://hls.videocc.net/" + videoId[:catcount] + "/f/" + videoId[:-2] + "_2.m3u8?device=desktop"

    post_params = {
        "token": keyRequestParam
    }
    keyRequestParam = urllib.parse.urlencode(post_params)
    m3u8 = downloader.downloadM3U8(m3u8URL)

    currentFolder = os.path.dirname(os.path.realpath(__file__))
    ts_list = downloader.parseTS(m3u8, numberOfKeys=1, numberOfIVs=1)
    filename = "temp"
    for item in reversed(ts_list):
        if 'key' in item:
            key = item['key'].split(".net")[0] + ".net/playsafe" + item['key'].split(".net")[1]
            key = key + "?" + keyRequestParam
            key = downloader.download(key)
            downloader.saveToFile(key, filename + ".key", os.path.join(currentFolder, "tmp1"))
        if 'ts' in item:
            ts = downloader.download(item['ts'])
            filename = item['ts'].split("/")[-1].split(".ts")[0]
            try:
                downloader.saveToFile(ts, filename + ".ts", os.path.join(currentFolder, "tmp1"))
            except:
                traceback.print_exc()
        if 'iv' in item:
            iv = bytes.fromhex(item['iv'])
            downloader.saveToFile(iv, filename + ".iv", os.path.join(currentFolder, "tmp1"))
    with open(os.path.join(os.path.join(currentFolder, "tmp1"), "video_id"), 'w') as f:
        f.write(videoId)