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
        "Cookie" : "cna=eURhFFP34iACAWVZQAZmiTUm; aliyun_choice=CN; t=e90dd500dc116e58597c00dfa9b3f76c; _tb_token_=f55e53a3eb058; cookie2=157ad0cd3c205e5a67b1c49dc51bb44d; cnz=UVRhFB75DC0CAQZAWWWROJE+; _ga=GA1.2.1896326308.1541040007; cart_delivery_guide_done=true; login_aliyunid_token=\"u3hps+Esh9i49JNPFvJIFn+7BRULA/wQlLY1EIspjRY=\"; CONSOLE_TOPBAR_HIDE_CLOUDSHELL_TIPS=true; beforeRegionId=cn-hangzhou; UM_distinctid=16a85a5f06a402-07f01748500489-e323069-144000-16a85a5f06b3bb; CLOSE_HELP_GUIDE=true; ping_test=true; UC-XSRF-TOKEN=b6d3066b-7f91-435f-ad31-296bdc29d3b8; CLOSE_HELP_GUIDE_V2=true; _hvn_login=6; login_aliyunid_pk=1754515694483538; aliyungf_tc=AQAAANL1dgVdmAUA62n+K0K/xIqH8UZm; PHPSESSID=okspu34rvq2mnpvtpukfoei5u0; onIn=true; activeRegionId=cn-shanghai; currentRegionId=cn-shanghai; consoleRecentVisit=domain%2Cecs%2Csas%2Cswas%2Coss; FECS-XSRF-TOKEN=5f6f9e53-de7b-4b4e-9b00-cab75f1d7dc5; FECS-UMID=%7B%22token%22%3A%22Yc50ff787635383346537ab9009440c8d%22%2C%22timestamp%22%3A%227828290956545B4853406574%22%7D; acw_tc=781bad3615614363394391271e284234d2844c5403e7e884e75cc85527ea3d; aliyun_lang=zh; CNZZDATA1261859658=1462138717-1558676430-https%253A%252F%252Fmail.aliyun.com%252F%7C1561543810; csg=02df226e; login_aliyunid=\"leo.jame****@gmail.com\"; login_aliyunid_ticket=ajmP*pAUFof_BNpwU_TOTNChZBoeM1KJexdfb9zhYnsN5Zos6qISCrRt7mGxbigG2Cd4fWaCmBZHIzsgdZq64XXWQgyKFeuf0vpmV*s*CT58JlM_1t$w3QH$FQIF3nXy7JCQIxqLM3V0mPTq*gzMlnPB0; login_aliyunid_luid=BG+34l5a1uYaa6292dce23f22675be98b10cd9670c8+KaVsX8Up2WBhxPOr0K5p3swcSBLrNUeiBLI8GlH2; login_aliyunid_csrf=_csrf_tk_1550861547594039; login_aliyunid_suid=\"8qBvdkgcdp9fJUBQSu0VgQPD/oTUeA/xjoTe/wQg/ds1p5W6Njk=\"; login_aliyunid_abi=\"BG+St3yY04db1a853b69afee370e9058a47bc226b76++LcMLHNsU2FwLpndiV0asCDxNvoQDP8x3FLFQEhIiKAqtozSJMk=\"; login_aliyunid_pks=\"BG+a2ReCfc1WtcassM1ptZmYruqebBilZ3UakSvyuWVDfM=\"; hssid=1FTwp_EISyb5-Yff6vH4lOw1; hsite=6; aliyun_country=CN; aliyun_site=CN; SERVERID=86285cb7834741ef479b520996bf1c3b|1561547758|1561547748; l=bBOX6mNnvo3DgDaoKOCanurza77OSIRYSuPzaNbMi_5dJ1Y_w1bOkxVYcev6Vf5R_tYB4G2npwy9-etki; isg=BAYG6pPzpwIf93L7Q7XJhiUqV_yIZ0ohyl-FGPAv8ikE86YNWPeaMeyBz2ea3kI5"
    })

    m3u8URL = "https://edu.aliyun.com/hls/2452/playlist/QqgxbJr47JFs8Wy3te1WQH8gs27UwkwS.m3u8?courseId=137"
    m3u8 = downloader.downloadM3U8(m3u8URL)

    currentFolder = os.path.dirname(os.path.realpath(__file__))
    downloader.downloadTS(m3u8, os.path.join(currentFolder, "tmp"), numberOfKeys=2, numberOfIVs=10, numberOfTSs=10)