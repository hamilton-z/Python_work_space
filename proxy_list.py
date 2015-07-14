#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'hamilton'

import urllib,urllib2
import BeautifulSoup
import re
import os

url = 'http://pachong.org/'

headers = {
            'Accept':'text/html, application/xhtml+xml, */*',
            'Referer':'http://cn.bing.com/search?q=%E4%BB%A3%E7%90%86%E6%9C%8D%E5%8A%A1%E5%99%A8&src=IE-TopResult&FORM=IETR02&conversationid=&pc=EUPP_',
            'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.5',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding':'gzip, deflate',
            'Host':'pachong.org',
            'Connection':'Keep-Alive'
          }

req = urllib2.Request(url,headers)
res = urllib2.urlopen(url,timeout=5)
html = res.read()
soup = BeautifulSoup.BeautifulSoup(html)
rsp = soup.findAll('td',text=re.compile('\d+\.\d+\.\d+\.\d+'))
calc = soup.find('script',text=re.compile('\d+'))
result = calc.replace('var ','').split(';')
for rl in result:
    print os.popen(rl)
# rsp1 = soup.find_all('tr',{'class':'even'})
# print rsp