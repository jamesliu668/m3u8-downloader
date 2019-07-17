# -*- coding: utf-8 -*-
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

    downloader = M3U8Downloader(log)
    # it's better to set the headers from your current browser here
    downloader.setHeaders({
        "Referer":"https://edu.aliyun.com/bundles/customweb/lib/cloud-player/1.1.37.3/player.html",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Cookie" : "UM_distinctid=16c0050ea12147-0694d8aa9d4bf3-37637c02-13c680-16c0050ea14bdb; cna=2Rm2FaEb7m8CAWdYLpvyfWFc; aliyungf_tc=AQAAAM7Uv1yb2wkAuO7gZcCBRtAiZ0vw; acw_tc=76b20f6515633734526586378e49fdb7809daadf74adcc58737436d604775c; PHPSESSID=mlu12u5rnti3mlncm6rq9scek4; aliyun_choice=CN; CNZZDATA1261859658=238142476-1563368812-%7C1563368812; ping_test=true; t=124b0ba48f9bf84ef3928932b7f61dde; _tb_token_=ea8de713e015a; cookie2=1d65e5fceeae49863e9c056ff29d3a5d; _hvn_login=6; csg=73b53f0c; login_aliyunid=\"leo.jame****@gmail.com\"; login_aliyunid_ticket=Xy7JCQIxqLM3O8mp*N_YGKVfoKSK3DW2D_c7pof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4ZWazmBdHI6sgXZqg4XFWQfyKpeu*0vCmV8s*MT5tJl3_1$$wIQHnFQ3F0; login_aliyunid_luid=\"BG+j9F5RQTL7c719ccb9eca531a4496581f48233c16+wm4UtOCGEcPMET01q7rl/Ejy1c5uSKIPAW9/V6gb\"; login_aliyunid_csrf=_csrf_tk_1189763373460557; login_aliyunid_suid=\"hNJ25YEvOYjKhJEVr0jeK1snPN4BwFCUgaizmeKeDc7imapzk0w=\"; login_aliyunid_abi=\"BG+0M45546Ya36670e00530014d60ec9f33fa75807a+Urzu25ed0+tbYUJeyu8zRz+MHEN5/u+dmWQBpfxv8Mc2mApZaU4=\"; login_aliyunid_pk=1754515694483538; login_aliyunid_pks=\"BG+q5iwXGGjt6e3yAVpVThsybuqebBilZ3UakSvyuWVDfM=\"; hssid=1XP9wZ0Y0xRWblyjmCsmcjA1; hsite=6; aliyun_country=CN; aliyun_site=CN; aliyun_lang=zh; l=cBgG52mHv7mOH1ntKOCNZuI8LN7OSIRvMuPRwCfXi_5BY1Y6XsQOkDcxWev6VfWd9Z8B40AqG929-etbiXLkyQwVCsJG.; isg=BMfHLUt8VnHKZdL9oj2th6HTVn1RZJrDr0XxXpm049Z9COfKoZwr_gVKroDzqHMm; SERVERID=e992f8bd1390dda7c0daa53775feaf93|1563373494|1563373490"
    })

    m3u8URL = "https://edu.aliyun.com/hls/2452/playlist/puxFOL9ZvbbriNqztkmpMiTdOR6jms9T.m3u8?courseId=137"
    m3u8 = downloader.downloadM3U8(m3u8URL)

    currentFolder = os.path.dirname(os.path.realpath(__file__))
    targetFolder = os.path.join(currentFolder, "tmp")
#    downloader.downloadTS(m3u8, os.path.join(currentFolder, "tmp"), numberOfKeys=2, numberOfIVs=10, numberOfTSs=10)
    ts_list = downloader.parseTS(m3u8, numberOfKeys=2, numberOfIVs=10, numberOfTSs=10)
    numOfKeys = 0
    numOfIV = 0
    numOfTS = 0
    for item in ts_list:
        if 'key' in item:
            filename = "{}".format(numOfKeys) + ".key"
            key = downloader.download(item['key'])
            downloader.saveToFile(key, filename, targetFolder)
            numOfKeys = numOfKeys + 1
        if 'iv' in item:
            filename = "{}".format(numOfIV) + ".iv"
            iv = bytes.fromhex(item['iv'])
            downloader.saveToFile(iv, filename,  targetFolder)
            numOfIV = numOfIV + 1
        if 'ts' in item:
            filename = "{}".format(numOfTS) + ".ts"
            ts = downloader.download(item['ts'])
            downloader.saveToFile(ts, filename,  targetFolder)
            numOfTS = numOfTS + 1