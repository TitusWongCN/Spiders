# -*- coding : utf-8 -*-
import re
import urllib
import urllib.request
from collections import OrderedDict

#构建url连接头
conn = 'Keep-Alive'
acce = 'text/html, application/xhtml+xml, */*'
lang = 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'Connection': conn, 'Accept' : acce, 'Accept-Language' : lang, 'User-Agent' : user_agent}

#准备要写入信息的文件
page = 1
fContent = open('qsbk-content.txt', 'w')
dicAuthorArticleCount = {}
fAuthorArticleCount = open('qsbk-AuthorArticleCount.txt', 'w')

#开始循环读取
while page < 500:
    url = 'http://www.qiushibaike.com/hot/page/' + str(page) + '/'
    page += 1

    try:
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request, timeout = 2)
        htmlData = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        continue

    try:
        pAuthorContent = re.compile(r'<div.*?class="article .*?<h2>(.*?)</h2>.*?<span>(.*?)</span>', re.S)
        #pattern = re.compile(r'<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' +
                            #r'="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pAuthorContent, htmlData)
    
        for item in items:
            #print(item[0] + '\n' + item[1] + '\n' + item[2] + '\n' + item[3] + '\n')
            txt = '\n作者: ' + item[0] + '\n' + '内容: ' + item[1] + '\n' + '*****************************************************'
            print(txt)
            if item[0] not in dicAuthorArticleCount:
            	dicAuthorArticleCount[item[0]] = 1
            else:
            	dicAuthorArticleCount[item[0]] += 1
            fContent.write(txt)
    except:
        continue

#将段子内容写入文件，按照【作者\n内容\n】的格式
fContent.flush()
fContent.close()

#统计段子作者发帖次数
#排序
bar = OrderedDict(sorted(dicAuthorArticleCount.items(), key=lambda x: x[1], reverse=True))
#统计名词
index = 0
for item in bar:
	if index == 0:
		txt = '发帖冠军是：' + item + '，TA总共发表了' + str(bar[item]) + '个糗事！'
		print(txt)
		index += 1
		fAuthorArticleCount.write(txt + '\n')
		continue
	if index == 1:
		txt = '发帖季军是：' + item + '，TA总共发表了' + str(bar[item]) + '个糗事！'
		print(txt)
		index += 1
		fAuthorArticleCount.write(txt + '\n')
		continue
	if index == 2:
		txt = '发帖亚军是：' + item + '，TA总共发表了' + str(bar[item]) + '个糗事！'
		print(txt)
		fAuthorArticleCount.write(txt + '\n')
		break
#将所有作者输出
txt = '\n接下来是名次总榜：'
fAuthorArticleCount.write(txt + '\n\n')
print('\n接下来是名次总榜：\n')
for item in bar:
	txt = '用户名：' + item + '\n' + '次数：' + str(bar[item])
	print(txt)
	fAuthorArticleCount.write(txt + '\n')