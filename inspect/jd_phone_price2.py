#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import json
 
iphoneUrl = "http://search.jd.com/Search?keyword=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&enc=utf-8&qr=&qrst=UNEXPAND&as_key=title_key%2C%2C%E6%89%8B%E6%9C%BA&rt=1&stop=1&click=&psort=1&page=1"
headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0'}
headers2 = {"Host": "www.jd.com",
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
            "Accept": "text/plain"}
 
# 抓网页源码,并返回为str
def getHtmlSrc(url, headers):
    req = urllib2.Request(url,headers)
    res = urllib2.urlopen(url,timeout=5)
    htmlSrc = res.read()
    res.close
    return htmlSrc
 
# 把抓到的网页源码保存到txt文本中
# def saveHtmlSrc(url):
#         html = getHtmlSrc(url,headers2)
#         f = open('jd_iphone.txt','w')
#         f.write(html)
#         f.close()
 
# saveHtmlSrc(iphoneUrl)
 
fhtml = open('jd_iphone.txt','r')
localhtml = fhtml.read().replace("'",'"').replace(' ','')   # 将所有单引号转为双引号,且去掉全部空格
for sku in re.findall('<lisku="\d+">', localhtml):
    skuid = sku.split('"')[1]   # 取商品id
    # print skuid
    pname = re.findall('<fontclass="skcolor_ljg">苹果</font>.+?<fontclass="adwords"id="AD_%s">' % skuid, localhtml) # 正则取商品名称html
    if len(pname) > 0:
        # 利用正则来循环替换所有html标签,得到实际商品名称
        for r in re.findall('<.+?>', pname[0]):
            pname[0] = pname[0].replace(r, '')
        print pname[0]
 
    # 抓取价格
    priceUrl = 'http://p.3.cn/prices/get?skuid=J_%s' % skuid
    pricehtmlSrc = getHtmlSrc(priceUrl, headers1)
    # 判断抓到的内容是否有数据,有数据的话长度是超过5的,[{}]\n
    if len(pricehtmlSrc) > 5:
        pprice=json.loads(pricehtmlSrc)
        print pprice[0]['p']
    else:
        print '价格读取延时,内容为空: ',pricehtmlSrc, '点击此链接查看: ',priceUrl
