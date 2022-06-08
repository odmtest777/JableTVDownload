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

if len(sys.argv) == 1:
    print('请在启动参数中输入视频id')
    sys.exit()

pageUrl = "https://ppp.porn/v/"
videoCode = sys.argv[1]

res = requests.get(pageUrl + videoCode + '/')

title = re.findall("<h2 class=\"content-details__title\">(.+?)</h2>", res.text)[0]
imageUrl = re.findall("<video poster=\"(.+?)\"", res.text)[0]
m3u8url = re.findall("var stream = \'(.+?)\'", res.text)[0]
# print(m3u8url)
last_index = m3u8url.rfind('/')
downloadurl = m3u8url[:last_index + 1]
folderName = videoCode

# 建立資料夾
if not os.path.exists(folderName):
    os.makedirs(folderName)
folderPath = os.path.join(os.getcwd(), folderName)

headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96"',
    'Referer': 'https://ppp.porn/',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
}
respone = requests.get(m3u8url, headers=headers)

# 得到 m3u8 file裡的 URI和 IV
m3u8obj = m3u8.loads(respone.text)

# 儲存 ts網址 in tsList
tsList = []
for seg in m3u8obj.segments:
    tsUrl = downloadurl + seg.uri
    tsList.append(tsUrl)

# 開始爬蟲並下載mp4片段至資料夾
prepareCrawl('', folderPath, tsList)

# 合成mp4
mergeMp4(folderPath, tsList,title)

# 刪除子mp4
files = os.listdir(folderPath)
originFile = title + '.mp4'
for file in files:
    if file != originFile:
        os.remove(os.path.join(folderPath, file))

# 下载封面
respone = requests.get(imageUrl)
with open(os.path.join(folderPath,title + '.jpg'),"wb")as f:
    f.write(respone.content)

print('下载封面完成')