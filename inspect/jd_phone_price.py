#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re

# class HTML_Tool:
#     # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
#     BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    
#     # 用非 贪婪模式 匹配 任意<>标签
#     EndCharToNoneRex = re.compile("<.*?>")

#     # 用非 贪婪模式 匹配 任意<p>标签
#     BgnPartRex = re.compile("<p.*?>")
#     CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
#     CharToNextTabRex = re.compile("<td>")

#     # 将一些html的符号实体转变为原始符号
#     replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),("\"&nbsp;"," ")]
    
#     def Replace_Char(self,x):
#         x = self.BgnCharToNoneRex.sub("",x)
#         x = self.BgnPartRex.sub("\n    ",x)
#         x = self.CharToNewLineRex.sub("\n",x)
#         x = self.CharToNextTabRex.sub("\t",x)
#         x = self.EndCharToNoneRex.sub("",x)

#         for t in self.replaceTab:
#             x = x.replace(t[0],t[1])  
#         return x  

class get_web:
    def __init__(self,keyword):
        self.keyword = keyword
        # self.myTool = HTML_Tool()


    def get_Data(self,url):

        headers = {
        			"GET":url,
        			"Host":"search.jd.com",	
        			"Referer":"www.jd.com",
        			"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        			}

        req = urllib2.Request(url)

        for key in headers:
        	req.add_header(key,headers[key])

        html = urllib2.urlopen(req).read()
        return html


    def page_counter(self,html):
        # 匹配 "共有<span class="red">12</span>页" 来获取一共有多少页
        myMatch = re.search(r'<span class="page-skip"><em>&nbsp;&nbsp;共(\d+?)页&nbsp;&nbsp;&nbsp;&nbsp;', html, re.S)
        if myMatch:  
            endPage = int(myMatch.group(1))
            print 'Total page is %d ' % endPage
        else:
            endPage = 0
            print 'Can not Get the total Pages'
        return endPage


    def deal(self,keyword):

        gjc = urllib.quote(self.keyword)

        url = "http://search.jd.com/Search?keyword="+gjc+"&enc=utf-8"

























    # def deal_data(self):
    #     if self.endPage:
    #         print endPage



# p = get.get_Data()
# print p
# p_id = re.findall(r'\<li sku=\"(.*?)\" \>',html)

# for i in p_id:
# 	p_name = re.findall('(.*?)<font class="skcolor_ljg">手机</font><font class=\'adwords\' id=\'AD_%s\'>' %i,html)
# 	if p_name:d
# 		p_price = re.findall(r'\<strong class\=\"J_%s\" data-price\=\"(.*?)\">' %i,html)
# 		# print("手机型号：%s,单价: %s元") % (p_name[0].strip(),p_price[0])
# 		print p_name[0].strip(),p_price[0]1
