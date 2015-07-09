#!/usr/bin/env python
# -*- coding: utf-8 -*-

    #!/usr/bin/env python
# -*- coding: utf-8 -*-

方法一：通过京东移动商城（因为它没有把价格藏在js中）

# codeing=utf-8
import urllib.request
import re
#通过京东移动接口
url = 'http://item.jd.com/997951.html'#原本的网址
jdid = re.search(r'/(\d+)\.html',url).group(1)#原本的网址提取出商品ID，即997951


url = 'http://m.jd.com/product/'+str(jdid)+'.html'#转换成为移动商城的url
html = urllib.request.urlopen(url).read().decode('utf-8')#通过对源代码进行utf-8解码
aa = re.findall(r'<font color="red" style="font-family:Arial;font-weight:bold;font-size:18px">&.*</font>', html)[0]#这里使用的是findall，可以用别的

aa = re.findall(r'\d+\.\d+', aa)#有点多此一举，不过当时还不太熟悉re.search
print (aa[0])

方法二：通过京东商城的json文件查，具体如何获取，可以用火狐浏览器嗅出来



# codeing=utf-8
import urllib.request
import re
'''通过京东服务器查'''
url = 'http://item.jd.com/997951.html'
jdid = re.search(r'/(\d+)\.html', url).group(1)

url = 'http://p.3.cn/prices/get?skuid=J_' + \
 str(jdid) + '&type=1&area=19_1601_51091&callback=cnp'#这就是那个被藏起来的json文件，格式除了京东id部分其他都一样
#其实就是p.3.cn/prices/get?skuid=J_997951&type=1&area=19_1601_51091&callback=cnp
html = urllib.request.urlopen(url).read().decode('utf-8')
aa = re.search(r'"p":"(.*?)"', html).group(1)

print(aa)

