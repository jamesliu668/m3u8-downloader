# -*- coding: utf-8 -*-
# python3
import os
import re
import sys
import logging
import requests
from urllib.parse import urlparse
from keydecryptor.ali import AliKeyDecryptor
from Crypto.Cipher import AES

class M3U8Downloader(object):
    logger = None
    headers = None
    session = None
    proxies = None
    rootURL = None

    def __init__(self, logger, headers=None):
        self.logger = logger
        self.session = requests.Session()

    def setHeaders(self, headers):
        self.headers = headers

    def setProxy(self, proxies):
        self.proxies = proxies

    # Download the real m3u8 real content. 
    # See: https://jmsliu.cn/others/m3u8%E6%B5%81%E8%A7%86%E9%A2%91%E6%95%B0%E6%8D%AE%E7%88%AC%E8%99%AB%E8%AF%A6%E8%A7%A3%E4%B8%80%EF%BC%9Am3u8%E8%A7%86%E9%A2%91%E6%96%87%E4%BB%B6%E8%AF%A6%E8%A7%A3.html#m3u8-file-level
    def downloadM3U8(self, m3u8URL):
        try:
            self.rootURL = m3u8URL
            req = self.session.get(m3u8URL, headers=self.headers, proxies=self.proxies)
            req.raise_for_status()
            req.encoding = req.apparent_encoding

            if req.text.find("#EXT-X-STREAM-INF") != -1:
                m3u8List = {}
                content = req.text.split('\n')
                currentBW = None
                currentName = None
                currentM3U8URL = None
                for line in content:
                    if line[:17] == "#EXT-X-STREAM-INF":
                        self.logger.debug(f"Find bandwidth definition {line}")
                        regex = re.compile(r"BANDWIDTH=(\d*)", re.DOTALL|re.UNICODE)
                        result = regex.findall(line)
                        if len(result) > 0:
                            currentBW = result[0]

                        currentName = "one"
                        regex = re.compile(r"NAME=(.*)", re.DOTALL|re.UNICODE)
                        result = regex.findall(line)
                        if len(result) > 0:
                            currentName = result[0]
                    elif len(line) > 0 and line[:1] != "#":
                        self.logger.debug(f"Find real m3u8 file {line}")
                        self.logger.info("Find {} m3u8 file for bandwidth {}".format(currentName, currentBW))
                        m3u8List[currentBW] = line
                        currentM3U8URL = line
                    else:
                        self.logger.debug("ignore: " + line)

                for key in m3u8List.keys():
                    self.logger.debug(f"Download bandwidth {key}bps m3u8: {m3u8List[key]}")
                    url = self.formatURL(m3u8List[key])
                    req = self.session.get(url, headers=self.headers, proxies=self.proxies)
                    req.raise_for_status()
                    m3u8List[key] = req.content
                
                return m3u8List
            else:
                m3u8List["index"] = req.content
                return m3u8List
        except Exception as e:
            print(e)

    def download(self, url):
        try:
            url = self.formatURL(url)
            req = self.session.get(url, headers=self.headers, proxies=self.proxies)
            req.raise_for_status()
            return req.content
        except Exception as e:
            self.logger.error(e)

    def parseTS(self, m3u8Content, numberOfKeys=sys.maxsize, numberOfIVs=sys.maxsize, numberOfTSs=sys.maxsize):
        try:
            content = m3u8Content.split('\n')
            currentKey = None
            currentIV = None

            keyNo = 0
            viNo = 0
            tsNo = 0

            results = []

            for line in content:
                if line[:10] == "#EXT-X-KEY":
                    self.logger.debug(f"Find key: {line}")
                    if keyNo < numberOfKeys:
                        keyNo = keyNo + 1
                        reg = r"URI=\"([^\"].*?)\""
                        result = re.findall(reg, line)
                        if len(result) > 0:
                            dic = {"key": result[0]}
                            results.append(dic)

                    if viNo < numberOfIVs:
                        viNo = viNo + 1
                        reg = r"IV=0x(.*)"
                        result = re.findall(reg, line)
                        if len(result) > 0:
                            dic = {"iv": result[0]}
                            results.append(dic)
                elif len(line) > 0 and line[:1] != "#":
                    self.logger.debug(f"Find ts: {line}")
                    if tsNo < numberOfTSs:
                        tsNo = tsNo + 1
                        dic = {"ts": line}
                        results.append(dic)
                elif line[:1] == "#EXT-X-ENDLIST":
                    self.logger.info("Reach m3u8 data end!")
                    break
                else:
                    self.logger.info("skip: " + line)
            return results
        except Exception as e:
            self.logger.error(e)

    def saveToFile(self, content, filename, folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        
        result = os.path.join(folderPath, filename)
        with open(result, 'wb') as f:
            f.write(content)

        return result

    def readFile(self, folderPath):
        if os.path.exists(folderPath):
            with open(folderPath, 'rb') as f:
                return f.read()

    def decrypt(self, key, iv, content):
        self.logger.info("Start decrypting...")
        cryptor = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        result = cryptor.decrypt(content)
        return result

    def combineTS(self, tsList, targetTSFileName):
        self.logger.info("Start combining {} ts files".format(len(tsList)))
        outfile = open(targetTSFileName, 'wb')
        for i in tsList:
            infile = open(i, 'rb')
            outfile.write(infile.read())
            infile.close()
        outfile.close()

    def formatURL(self, url):
        rootURLObj = urlparse(self.rootURL)
        url = url.strip()

        if url[:4] == "http":
            return url
        elif url[:2] == "//":
            return rootURLObj.scheme + ":" + url
        elif url[:2] == "..":
            count = url.count("../")
            spliturl = url.split("/")
            if count <= (len(spliturl) - count):
                newurl = rootURLObj.scheme + "://" + rootURLObj.netloc
                for i in range(count):
                    newurl = newurl + "/" + spliturl[i+count]
                for i in range(len(spliturl) - count*2):
                    newurl = newurl + "/" + spliturl[count*2+i]
                return newurl
            else:
                newurl= rootURLObj.scheme + "://" + rootURLObj.netloc + "/" + url.replace("../","")
                return newurl
        elif url[:1] == "/":
            return rootURLObj.scheme + "://" + rootURLObj.netloc + url
        else:
            # ./ or just index.html
            pre_url = self.rootURL[0: (len(self.rootURL) - self.rootURL[::-1].index('/'))]
            newurl = pre_url + url
            return newurl