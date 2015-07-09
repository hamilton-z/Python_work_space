#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'hamilton'


import urllib2
import urllib
import re
import json

class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self,keyword):
        self.keyword = urllib.quote(keyword)
        self.product_pg = int()
        self.html = str()
        self.fhtml = str()
        self.purl = str()
        self.url = "http://search.jd.com/Search?keyword=%s&enc=utf-8" % self.keyword
        self.turl = "/Search?keyword=%s&enc=utf-8&qrst=1&ps=addr&rt=1&stop=1&cid3=655&click=3-655&psort=&page=" % self.keyword
        self.headers1 = {"GET":self.url,
            "Host":"search.jd.com",
            "Referer":"www.jd.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"}

        self.headers2 = {"GET":self.purl,
            "Accept":"text/html, application/xhtml+xml, */*",
            "Referer":self.url,
            "Accept-Language":"zh-Hans-CN,zh-Hans;q=0.5",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Accept-Encoding":"gzip, deflate",
            "Host":"search.jd.com",
            "Connection":"Keep-Alive",
            "Cache-Control":"no-cache"}

    def get_page(self):
        self.data = urllib.urlencode(self.headers1)
        self.req = urllib2.Request(self.url, self.data)
        self._response = urllib2.urlopen(self.req)
        self.fhtml = self._response.read()
        """
        获取页数
        """
        product_pg_re = re.compile(r'<span class="page-skip"><em>&nbsp;&nbsp;共(\d+?)页&nbsp;&nbsp;&nbsp;&nbsp;', re.S)
        self.p_page = str(re.findall(product_pg_re, self.fhtml)).strip('\[\'\'\]')


    def get_skuid(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        :return:
        """
        skuid_re = re.compile(r'li sku="(.*?)"', re.S)
        skuid = re.findall(skuid_re, self.html)
        return skuid

    def get_product(self):
        result = {}
        price = {}
        skuids2 = self.get_skuid()
        for sku in skuids2:
            product_page = urllib2.urlopen('http://item.jd.com/%s.html' %sku).read()
            name_re = re.compile(r'\<li\>\<img class=\'img-hover\' alt=\'(.*?)\'')
            _name = name_re.search(product_page).group().decode('GBK').encode('utf-8')
            product = str(_name[33:-1])

            url = 'http://p.3.cn/prices/mgets?skuIds=J_' + sku + '&type=1'
            try:
                price_json = json.load(urllib.urlopen(url))[0]
            except ValueError:
                price = 'web error 501'
            else:
                if price_json['p']:
                    price = price_json['p']
            result[product] = price.encode("utf-8")
        # print product,price,result.

        return result

    def total_pri(self):
        self.get_page()
        for self.i in range(int(self.p_page)):
            self.purl = self.url + self.turl+str(self.i)+"&click=0"
            self.data = urllib.urlencode(self.headers2)
            self.req = urllib2.Request(self.purl, self.data)
            self._response = urllib2.urlopen(self.req)
            self.html = self._response.read()
            self.result = self.get_product()

        return self.result


jp = JdPrice('苹果')
jdprice = jp.total_pri()
for key in jdprice.keys():
    print key,jdprice[key]
