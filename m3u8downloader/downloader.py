# -*- coding: utf-8 -*-
import os
import re
import sys
import logging
import requests
from keydecryptor.ali import AliKeyDecryptor
from Crypto.Cipher import AES

class M3U8Downloader(object):
    logger = None
    headers = None
    session = None

    def __init__(self, logger, headers=None):
        self.logger = logger
        self.session = requests.Session()

    def setHeaders(self, headers):
        self.headers = headers

    def downloadM3U8(self, m3u8URL, bandwith=None):
        try:
            req = self.session.get(m3u8URL, headers=self.headers)
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
                        self.logger.info("Find {} m3u8 file for bandwidth {}".format(currentName, currentBW))
                        m3u8List[currentBW] = line
                        currentM3U8URL = line
                    else:
                        self.logger.info("ignore: " + line)

                if bandwith is not None:
                    for key in m3u8List.keys():
                        if int(key) > bandwith:
                            currentM3U8URL = m3u8List[key]
                
                #download the real m3u8
                req = self.session.get(currentM3U8URL, headers=self.headers)
                req.raise_for_status()
                req.encoding = req.apparent_encoding
                return req.text
            else:
                return req.text
        except Exception as e:
            print(e)

    def downloadTS(self, m3u8, folderName, numberOfKeys=10000, numberOfIVs=10000, numberOfTSs=10000):
        try:
            # req = self.session.get(url, headers=headers)
            # req.raise_for_status()
            # req.encoding = req.apparent_encoding
            # print(req.text)

            content = m3u8.split('\n')
            currentKey = None
            currentIV = None

            keyNo = 0
            viNo = 0
            tsNo = 0

            for line in content:
                if line[:10] == "#EXT-X-KEY":
                    if keyNo < numberOfKeys:
                        keyNo = keyNo + 1
                        reg = r"URI=\"([^\"].*?)\""
                        result = re.findall(reg, line)
                        if len(result) > 0:
                            keyURL = result[0]
                            req = self.session.get(keyURL, headers=self.headers)
                            req.raise_for_status()
                            currentKey = req.content

                    if viNo < numberOfIVs:
                        viNo = viNo + 1
                        reg = r"IV=0x(.*)"
                        result = re.findall(reg, line)
                        if len(result) > 0:
                            currentIV = result[0]
                elif len(line) > 0 and line[:1] != "#":
                    if tsNo < numberOfTSs:
                        tsNo = tsNo + 1
                        url = line
                        req = self.session.get(url, headers=self.headers)
                        req.raise_for_status()
                        file_name = url.split('/')[-1].split('?')[0]
                        with open(os.path.join(folderName, file_name), 'wb') as f:
                            f.write(req.content)

                        key_file_name = file_name + ".key"
                        with open(os.path.join(folderName, key_file_name), 'wb') as f:
                            f.write(currentKey)

                        iv_file_name = file_name + ".iv"
                        vi = bytes.fromhex(currentIV)
                        with open(os.path.join(folderName, iv_file_name), 'wb') as f:
                            f.write(vi)
                elif line[:1] == "#EXT-X-ENDLIST":
                    self.logger.info("Reach m3u8 end!")
                    break
                else:
                    self.logger.info("skip: " + line)
        except Exception as e:
            self.logger.error(e)

    def decrypt(self, key, iv, content):
        self.logger.info("Start decrypting...")
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        result = cryptor.decrypt(content)
        return result

    def combineTS(self, tsList, fileName):
        self.logger.info("Start combining {} ts files".format(len(tsList)))
        outfile = open(fileName, 'wb')
        for i in tsList:
            infile = open(i, 'rb')
            outfile.write(infile.read())
            infile.close()
        outfile.close()