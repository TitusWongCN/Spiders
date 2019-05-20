#-*- coding=utf-8 -*-
import re
from lxml import etree
import requests
import bs4
import xlwt
import xlrd
import time
from collections import deque
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import multiprocessing

class StockPrice:
    def __init__(self):
        # 股票代码
        self.STOCKCODE = ''
        # For构造爬取地址
        # 上证指数为：http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html
        self.BASEURL = 'http://quotes.money.163.com/trade/lsjysj_'
        self.URLEXT = '.html'
        self.FILTER = '?year=*&season=#'
        # 沪市A股所有代号的网页
        self.ALLCODEURL = 'http://resource.emagecompany.com/publiccompanies/listedcompanies_shanghai.html'
        # 存储沪市A股所有代号
        self.CODELIST = deque()
        # 存储文件路径
        self.FILENAME = ''
        # 数据总列数
        self.ROWCOUNT = 0
        # headers
        self.headers = {
        'Accept' : 'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch, br',
        'Accept-Language' : 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Connection': 'Keep-Alive',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
        # years
        self.years = OrderedDict()

    def getUrl(self, *date):
        if len(date) == 0:
            url = self.BASEURL + self.STOCKCODE + self.URLEXT
        else:
            url = self.BASEURL + self.STOCKCODE + self.URLEXT + self.FILTER
            url = url.replace('*', str(date[0])).replace('#', str(date[1]))
        return url

    def getUrlData(self, *url):
        if len(url) == 0:
            url = self.getUrl()
            req = requests.get(url, headers = self.headers)
            soup = bs4.BeautifulSoup(req.text, 'lxml')
        else:
            req = requests.get(url[0], headers = self.headers)
            soup = bs4.BeautifulSoup(req.text, 'lxml')
        return soup

    def getCodeName(self):
        soup = self.getUrlData()
        htmlData = soup.find_all('span', class_ = 'name')
        pattern = re.compile('>(.*?)\s.*?<')
        items = re.findall(pattern, str(htmlData))
        # print(items)
        self.FILENAME = items[0] + '.xls'
        return items[0]

    def getAllCodeList(self):
        req = requests.get(self.ALLCODEURL, headers = self.headers)
        pattern = re.compile('x:num>(.*?)</TD>')
        items = re.findall(pattern, req.text)
        for item in items:
            if '6' in item:
                # print(item)
                self.CODELIST.append(item)

    def getTableHead(self):
        soup = self.getUrlData()
        htmlData = soup.find('tr', class_ = 'dbrow')
        pattern = re.compile('<th>(.*?)</th>')
        items = re.findall(pattern, str(htmlData))
        self.ROWCOUNT = len(items)
        return items

    def getYearQuarter(self):
        soup = self.getUrlData()
        htmlData = soup.find_all('form', id = 'date')
        pattern = re.compile('<option.*?>(.*?)</option>')
        items = re.findall(pattern, str(htmlData))
        # 记录当年有几个季度的数据
        curYearCount = 4
        curQuarter = deque()
        for item in items:
            if '2' in item:
                self.years[item] = deque('4321')
            else:
                curQuarter.append(str(curYearCount))
                curYearCount -= 1
        self.years[items[0]] = curQuarter
        # for item in years:
        #     print('years[' + item + ']:' + str(years[item]))

    def createXLS(self):
        excelFile = xlwt.Workbook()
        sheet = excelFile.add_sheet(self.getCodeName().replace('*','_'))
        tableHead = self.getTableHead()
        # print(tableHead)
        index = 0
        while index < len(tableHead):
            sheet.write(0,index,tableHead[index])
            index += 1
        return excelFile, sheet

    def getDataWriteXLS(self):
        excelFile, sheet = self.createXLS()
        self.getYearQuarter()
        allData = deque()
        colIndex = 1
        for operYear in self.years:
            print(operYear)
            while(True):
                try:
                    quarter = self.years[operYear].popleft()
                    url = self.getUrl(operYear, quarter)
                    # print(url)
                    soup = self.getUrlData(url)
                    htmlData = soup.find_all('table', class_ = 'table_bg001 border_box limit_sale')
                    pattern = re.compile('<td.*?>(.*?)</td>')
                    items = re.findall(pattern, str(htmlData))
                    for item in items:
                        allData.append(item)
                    # print(len(allData))
                    rowIndex = 0
                    while True:
                        try:
                            temp = allData.popleft()
                            # print(temp)
                            # sheet.put_cell(rowIndex, colIndex, 1, temp)
                            sheet.write(colIndex,rowIndex,temp)
                            rowIndex += 1
                            if rowIndex == self.ROWCOUNT:
                                rowIndex = 0
                                colIndex += 1
                                # print('***********************')
                            # print('colIndex:[' + str(colIndex) + '], rowIndex:[' + str(rowIndex) + ']: [' + temp + '].')
                        except:
                            break
                except:
                    break
        excelFile.save(self.FILENAME)

t_start = time.time()
stock = StockPrice()
stock.getAllCodeList()
# p = multiprocessing.Pool(10)
for code in stock.CODELIST:
    print(code)
    stock.STOCKCODE = code
    stock.getDataWriteXLS()
    # p.apply_async(stock.getDataWriteXLS)
# pool.close()
# pool.join()
# print(len(stock.CODELIST))
t_end = time.time()
t = t_end - t_start
print('总共花费时间:', str(t), 's')
