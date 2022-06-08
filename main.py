# author: fox
#!/usr/bin/env python
# coding: utf-8

import requests
import os
import re
import m3u8
import sys
from config import headers
from crawler import prepareCrawl
from merge import mergeMp4
from delete import deleteMp4
from cover import downloadCover

if len(sys.argv) == 1:
    print('请在启动参数中输入视频id')
    sys.exit()

pageUrl = "http://it6crh.jiuse701.com/video/view/"
videoCode = sys.argv[1]

res = requests.get(pageUrl + videoCode, headers=headers)

title = re.findall("<meta name=\"description\" content=\"(.+?)\"", res.text)[0]
imageUrl = re.findall("data-poster=\"(.+?)\"", res.text)[0]
m3u8url = re.findall("data-src=\"(.+?)\"", res.text)[0]
m3u8url = m3u8url.replace("amp;", "")
downloadurl = m3u8url.split('index')[0]

folderName = videoCode

# 建立資料夾
if not os.path.exists(folderName):
    os.makedirs(folderName)
folderPath = os.path.join(os.getcwd(), folderName)

respone = requests.get(m3u8url)

# 得到 m3u8 file裡的 URI和 IV
m3u8obj = m3u8.loads(respone.text)

# 儲存 ts網址 in tsList
tsList = []
for seg in m3u8obj.segments:
    tsUrl = downloadurl + seg.uri
    tsList.append(tsUrl)

# 第一个视频为图片
tsList = tsList[1:]

# 開始爬蟲並下載mp4片段至資料夾
prepareCrawl('', folderPath, tsList)

# 合成mp4
mergeMp4(folderPath, tsList,title)

# 刪除子mp4
deleteMp4(folderPath)

# 下载封面
downloadCover(imageUrl,folderPath,title)