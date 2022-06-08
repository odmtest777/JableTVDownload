#!/usr/bin/env python
# coding: utf-8

import requests
import os

def downloadCover(imageUrl,folderPath,fileName):
    respone = requests.get(imageUrl)
    with open(os.path.join(folderPath,fileName + '.jpg'),"wb")as f:
        f.write(respone.content)

    print('下载封面完成')