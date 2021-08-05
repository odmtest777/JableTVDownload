# author: fox
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
import re
import urllib.request
import m3u8
import sys
from config import headers
from crawler import prepareCrawl
from merge import mergeMp4
from delete import deleteM3u8, deleteMp4

def str_cover_list(str):
    return list(str)

def get_ddCalcu(puData_url):
    params_dict = {}
    query_string = puData_url.split("?")[-1]
    for i in query_string.split("&"):
        temp = i.split("=")
        params_dict[temp[0]] = temp[1]
    puData_list = str_cover_list(params_dict['puData'])
    p = 0
    result = []
    while (2 * p) < len(puData_list):
        result.append(puData_list[len(puData_list) - p - 1])
        if p < len(puData_list) - p - 1:
            result.append(params_dict['puData'][p])
        if p == 1:
            result.append('e')
        if p == 2:
            result.append(str_cover_list(params_dict['timestamp'])[6])
        if p == 3:
            result.append(str_cover_list(params_dict['ProgramID'])[2])
        if p == 4:
            result.append(str_cover_list(params_dict['Channel_ID'])[len(str_cover_list(params_dict['Channel_ID'])) - 4])
        p += 1
    return ''.join(result)

# In[2]:

# 713573353
if len(sys.argv) == 1:
    print('请在启动参数中输入视频id')
    sys.exit()

m3u8ApiUrl = "https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId="
downloadurl = 'https://mgbs.vod.miguvideo.com/depository_yqv/asset{}media'
videoCode = sys.argv[1]

# In[3]:


# 建立資料夾
if not os.path.exists(videoCode):
    os.makedirs(videoCode)
folderPath = os.path.join(os.getcwd(), videoCode)


# In[4]:


# 得到 m3u8 網址
res = requests.get(m3u8ApiUrl + videoCode, headers=headers)
puData_url = res.json()['body']['urlInfo']['url']
ddCalcu = get_ddCalcu(puData_url)
m3u8url = f"{puData_url}&ddCalcu={ddCalcu}"


# 儲存 m3u8 file 至資料夾
m3u8file = os.path.join(folderPath, videoCode + '.m3u8')
urllib.request.urlretrieve(m3u8url, m3u8file)


# In[5]:


# 得到 m3u8 file裡的 URI和 IV
m3u8obj = m3u8.load(m3u8file)

# 儲存 ts網址 in tsList
_url  = re.findall("asset(.+?)media", puData_url)[0]
downloadurl = downloadurl.format(_url)
tsList = []
for seg in m3u8obj.segments:
    tsUrl = downloadurl + '/' + seg.uri
    tsList.append(tsUrl)

# In[7]:


# 刪除m3u8 file
deleteM3u8(folderPath)


# In[8]:


# 開始爬蟲並下載mp4片段至資料夾
prepareCrawl('', folderPath, tsList)


# In[9]:


# 合成mp4
mergeMp4(folderPath, tsList)


# In[10]:


# 刪除子mp4
deleteMp4(folderPath)
