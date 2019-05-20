#-*- coding=utf-8 -*-
import re
import requests
import bs4
import xlwt
import xlrd
import random
from collections import deque
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#获取对应URL内符合条件的items
def getUrlData(url, className, pattern):
    req = requests.get(url,headers = headers)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    target = soup.find_all('div', class_=className)
    items = re.findall(pattern, str(target))
    return items

#获取对应URL内符合条件的items
def getWeatherUrlData(url, className, pattern):
    req = requests.get(url,headers = headers)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    target = soup.find_all('div', class_=className)
    target = str(target).replace(' ', '').replace('\n', '').replace('\r', '')
    # print(target)
    items = re.findall(pattern, str(target))
    return items

#获取已按时间排序的每天天气记录
def getMonthWeatherList(url, className, pattern):
    dic = dict()
    # 没有获取到数据
    items = getWeatherUrlData(url, className, pattern)
    # print('----------------------')
    # print(items)
    for item in items:
        dic[item[0]] = item[1] + '&' + item[2] + '&' + item[3] + '&'  + item[4] + '&' + item[5]
    ordDic = OrderedDict(sorted(dic.items(), key=lambda x: x[0], reverse=True))
    # print(ordDic)
    return ordDic

# 全局变量
global headers
global indexUrl
global colCount
global CityList

# 初始化数据
headers = {
    'Accept' : 'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, sdch, br',
    'Accept-Language' : 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Connection': 'Keep-Alive',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}
indexUrl = 'http://lishi.tianqi.com/'
colCount = ('日期','最高气温','最低气温','天气','风向','风力')
CityList = {
    '上海': deque(),
    '荆州': deque(),
    '徐州': deque(),
    '南昌': deque(),
    '北京': deque()
}

# 获取城市的天气网址
patternCities = re.compile('.href="(.*?)".*?>(.*?)</a></li>')
cityItems = getUrlData(indexUrl, 'box-base', patternCities)
count = 0
for cityItem in cityItems:
    count += 1
    if cityItem[1] in CityList:
        patternMonthlyItems = re.compile('.href="(.*?)"')
        weatherItems = getUrlData(cityItem[0], 'tqtongji1', patternMonthlyItems)
        for weatherItem in weatherItems:
            CityList[cityItem[1]].append(weatherItem)
            # print(cityItem[1] + ':' + weatherItem)

#准备Excel文件
classNameWeatherItems = 'tqtongji2'
patternWeatherItems = re.compile('<ul><li><a.*?>(.*?)</a>.*?<li>(.*?)</li><li>(.*?)</li><li>(.*?)</li><li>(.*?)</li><li>(.*?)</li>')
ExcelFile=xlwt.Workbook()
for city in CityList:
    print('city = ' + city)
    rowIndex = 0
    print('rowIndex = ' + str(rowIndex))
    sheet=ExcelFile.add_sheet(city)
    while True:
        try:
            url = CityList[city].popleft()
            # print(url)
        except:
            print('**************************')
            break
        print(url)
        if rowIndex == 0:
            for col in range(0,len(colCount)):
                sheet.write(rowIndex,col,colCount[col])
            rowIndex += 1
        
        weatherData = getMonthWeatherList(url, classNameWeatherItems, patternWeatherItems)
        for item in weatherData:
            listItem = weatherData[item].split('&')
            listItem = [item] + listItem
            print('listItem = ' + str(listItem))
            for col in range(0,len(colCount)):
                print('rowIndex = ' + str(rowIndex))
                print('col = ' + str(col))
                print('listItem[col] = ' + listItem[col])
                if col == 1 | col == 2:
                    sheet.write(rowIndex,col,int(listItem[col]))
                else:
                    sheet.write(rowIndex,col,listItem[col])
            rowIndex += 1

ExcelFile.save('WeatherInfo.xls')
