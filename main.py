# coding:utf-8

import requests
import json
import os
import time
from bs4 import BeautifulSoup

headers = ({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'http://www.pixiv.net/'
})

index = requests.get("http://www.pixiv.net/")
indexSoup = BeautifulSoup(index.text, 'lxml')

table = indexSoup.find(id="init-config")
jsonText = table.attrs['value']

jsonData = json.loads(jsonText)

imgs = jsonData[u'pixivBackgroundSlideshow.illusts'][u'landscape']

for img in imgs:
    thisTitle = img['illust_title']
    print 'getting', thisTitle, '...',
    thisUrl = img['url']['1200x1200']

    # replace URL of 1200px compressed image to original image
    thisUrl = thisUrl.replace('img-master', 'img-original')
    thisUrl = thisUrl.replace('_master1200', '')

    # Assume original images are all JPEGs
    fileName = thisTitle + '.jpg'

    # Auto skip existed files. To override, remove this
    if os.path.exists(fileName):
        print 'skipped'
        continue

    thisImg = requests.get(thisUrl, headers=headers)

    # Wrong format
    if thisImg.status_code == 404:
        print '\n404 error, try another format...',
        # use PNG, that always helps
        thisUrl = thisUrl[:-4] + '.png'
        fileName = thisTitle + '.png'
        thisImg = requests.get(thisUrl, headers=headers)

    if thisImg.status_code == 200:
        f = open(thisTitle + '.jpg', 'wb')
        f.write(thisImg.content)
        f.close()
        print 'success'

    else:
        print 'Failed to get', thisTitle, 'from', thisUrl
        print 'Error:', thisImg.status_code

    time.sleep(1)
