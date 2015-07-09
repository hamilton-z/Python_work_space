#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import json

class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """
    def __init__(self, url):
        self.url = url
        self.headers = {"GET":url,
            "Host":"search.jd.com",
            "Referer":"www.jd.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"            }
        self.data = urllib.urlencode(self.headers)
        self.req = urllib2.Request(self.url, self.data)
        self._response = urllib2.urlopen(self.req)
        self.html = self._response.read()
        self.p_name = {}


    def get_skuid(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        :return:
        """
        # print self.html
        skuid_re = re.compile(r'li sku="(.*?)"', re.S)
        # product_info_re = are.compile(r'(.*?)<font class="skcolor_ljg">手机</font>(.*?)<font class='adwords' id='AD_')
        skuid = re.findall(skuid_re, self.html)
        return skuid

    def get_pages(self):
        """
        获取页数
        """
        product_pg_re = re.compile(r'<span class="page-skip"><em>&nbsp;&nbsp;共(\d+?)页&nbsp;&nbsp;&nbsp;&nbsp;', re.S)
        product_pg = str(re.findall(product_pg_re, self.html)).strip('\[\'\'\]')
        return product_pg

    def get_product_price(self):
        """
        根据商品的skuid信息，请求获得商品price
        :return:
        """
        price = {}
        product= {}
        skuid = self.get_skuid()
        # print skuid
        for sku in skuid:
            # print sku
            url = 'http://p.3.cn/prices/mgets?skuIds=J_' + sku + '&type=1'
            price_json = json.load(urllib.urlopen(url))[0]
            # print price_json
            if price_json['p']:
                price[sku] = price_json['p']
            #获取产品名称及描述
            product_page = urllib.urlopen('http://item.jd.com/%s.html' %sku).read()
            name_re = re.compile(r'\<li\>\<img class=\'img-hover\' alt=\'(.*?)\'')
            _name = name_re.search(product_page).group().decode('GBK').encode('utf-8')
            product[sku] = _name[33:-1]
        return price,product

    def deal_page(self):
        # pages = self.get_pages()
        price = self.get_product_price()[0]
        product = self.get_product_price()[1]
        for sku in self.get_skuid():
           print product[sku],price[sku]

    def total_price(self):
        total = []
        pages = int(self.get_pages())
        for i in range(pages):
            purl =self.url + "#keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&ps=addr&rt=1&stop=1&cid3=655&click=3-655&psort=&page=" + str(1)
            self.html = urllib.urlopen(purl).read()
            total.append(self.deal_page())
        return total

gjc = urllib.quote('手机')
url = "http://search.jd.com/Search?keyword="+gjc+"&enc=utf-8"
jp = JdPrice(url)
jdprice = jp.total_price()



