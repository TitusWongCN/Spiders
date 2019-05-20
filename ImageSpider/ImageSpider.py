#-*- coding = utf-8 -*-
import os
import re
import urllib
import urllib.request

class Spider:
	def __init__(self):
		self.site = 'http://www.mzitu.com/'
		self.errorInfo = '*******************************************************************\n'
		self.programStatus = '*******************************************************************\n'

	#获取url对应的网页内容
	def getPage(self, url):
		self.errorInfo += 'Program run in Spider.getPage()\n'
		self.programStatus += '正在抓取[' + url + ']的网页内容...\n'
		print('正在抓取[' + url + ']的网页内容...')
		try:
			print(r'response = urllib.request.urlopen(url, timeout = 30)')
			response = urllib.request.urlopen(url, timeout = 30)
			print("htmlData = response.read().decode('utf-8')")
			htmlData = response.read().decode('utf-8')
			return htmlData
		except Exception as e:
			self.errorInfo += '[ErrorInfo]-[getPage]-[url]:' + url + '\n'
			return ''

	#获取首页的页数
	def getPageCount(self, url):
		self.errorInfo += 'Program run in Spider.getPageCount()\n'
		self.programStatus += '正在通过[' + url +']获取页面总数量...\n'
		print('正在通过[' + url +']获取页面总数量...')
		returnValue = ''
		try:
			reStr = '</span>([0-9]{1,4})<span class="meta-nav screen-reader-text"></span></a>.<a class="next page-numbers"'
			htmlData = self.getPage(url)
			pattern = re.compile(reStr, re.S)
			items = re.findall(pattern, htmlData)
			returnValue = '[items:][type]' + str(type(items)) + '[Value]:' + str(items)
			return items[0]
		except:
			self.errorInfo += '[ErrorInfo]-[getPageCount]-[url]:' + url + '\n'
			self.errorInfo += '[ValueInfo]-[getPageCount]-[returnValue]:' + returnValue + '\n'
			return ''

	#获取首页所有页中所有Girl对应的网址
	def getGirlUrlList(self):
		self.errorInfo += 'Program run in Spider.getGirlUrlList()\n'
		self.programStatus += '正在获取所有Model的个人主页...\n'
		print('正在获取所有Model的个人主页...')
		index = 1
		urlList = []
		print('************************ index = ' + str(index) + ' ****************************')
		try:
			count = self.getPageCount(self.site)
			if count != '':
				self.programStatus += '网站页面总数量为' + count + '\n'
				print('网站页面总数量为' + count)
				while index <= int(count):
					if index == 1:
						url = self.site
					else:
						url = self.site + 'page/' + str(index)
					index += 1
					print('************************ index = ' + str(index) + ' ****************************')
					htmlData = self.getPage(url)
					if htmlData == '':
						index += 1
						continue
					reStr = '<li><a href="(.*?)"|"_blank" href="(.*?)"|<dd.*?><a href="(.*?)"'
					pattern = re.compile(reStr, re.S)
					items = re.findall(pattern, htmlData)
					for item in items:
						if item[0] != '' and item[0] not in urlList:
							urlList.append(item[0])
						elif item[1] != '' and item[1] not in urlList:
							urlList.append(item[1])
						elif item[2] != '' and item[2] not in urlList:
							urlList.append(item[2])
		except Exception as e:
			self.errorInfo += '[ErrorInfo]-[getGirlUrlList]\n'
			if index == count:
				return urlList
		return urlList

	#获取每一个Girl的照片数量
	def getImageNum(self, url):
		self.errorInfo += 'Program run in Spider.getImageNum()\n'
		self.programStatus += '正在获取TA的照片的总数量...\n'
		print('正在获取TA的照片的总数量...')
		returnValue = ''
		try:
			reStr = '<span>([0-9]{1,2})</span>'
			htmlData = self.getPage(url)
			pattern = re.compile(reStr, re.S)
			items = re.findall(pattern, htmlData)
			returnValue = '[items:][type]' + str(type(items)) + '[Value]:' + str(items)
			return items[4]
		except:
			self.errorInfo += '[ErrorInfo]-[getImageNum]-[url]:' + url + '\n'
			self.errorInfo += '[ValueInfo]-[getImageNum]-[returnValue]:' + returnValue + '\n'
			return ''

	#获取每一个Girl的照片集名称
	def getImageTitle(self, url):
		self.errorInfo += 'Program run in Spider.getImageTitle()\n'
		self.programStatus += '正在获取当前Model的相册名称...\n'
		print('正在获取当前Model的相册名称...')
		returnValue = ''
		try:
			reStr = '<h2 class="main-title">(.*?)</h2>'
			htmlData = self.getPage(url)
			pattern = re.compile(reStr, re.S)
			items = re.findall(pattern, htmlData)
			returnValue = '[items:][type]' + str(type(items)) + '[Value]:' + str(items)
			return items[0]
		except:
			self.errorInfo += '[ErrorInfo]-[getImageTitle]-[url]:' + url + '\n'
			self.errorInfo += '[ValueInfo]-[getImageTitle]-[returnValue]:' + returnValue + '\n'
			return ''

	#获取特定Girl的所有图片路径
	def getSpecificGirlImagePathList(self, url):
		self.errorInfo += 'Program run in Spider.getSpecificGirlImagePathList()\n'
		self.programStatus += '正在获取这个Model所有照片的路径...\n'
		print('正在获取这个Model所有照片的路径...')
		index = 1
		SpecificGirlImagePathList = []
		reStr = '<img src="(.*?)"'
		pattern = re.compile(reStr, re.S)
		try:
			count = self.getImageNum(url)
			if count != '':
				self.programStatus += 'TA总共有[' + count + ']张照片.\n'
				print('TA总共有[' + count + ']张照片.')
				count = int(count)
				while index <= count:
					if index == 1:
						target = url
					else:
						target = url + '/' + str(index)
						print(target)
					self.programStatus += '正在抓取第[' + str(index) + ']条路径...\n'
					print('正在抓取第[' + str(index) + ']条路径...')
					index += 1
					htmlData = self.getPage(target)
					items = re.findall(pattern, htmlData)
					for item in items:
						if item not in SpecificGirlImagePathList:
							SpecificGirlImagePathList.append(item)
			return SpecificGirlImagePathList
		except:
			self.errorInfo += '[ErrorInfo]-[getSpecificGirlImagePathList]-[url]:' + url + '\n'
			self.errorInfo += '[ValueInfo]-[getSpecificGirlImagePathList]-[returnValue]:' + returnValue + '\n'
			return []

	#创建新目录
	def mkdir(self, path):
		self.errorInfo += 'Program run in Spider.mkdir()\n'
		try:
			path = path.strip()
			isExists=os.path.exists(path)
			if not isExists:
				self.programStatus += '正在创建该Model的个人文件夹：[' + path + ']...\n'
				print('正在创建该Model的个人文件夹：[' + path + ']...')
				# 创建目录操作函数
				os.makedirs(path)
				return True
			else:
				self.programStatus += '创建该Model的个人文件夹：[' + path + ']时发现文件夹已存在.\n'
				print('创建该Model的个人文件夹：[' + path + ']时发现文件夹已存在.')
				return True
		except:
			self.errorInfo += '[ErrorInfo]-[mkdir]-[path]:' + path + '\n'
			self.errorInfo += '[ValueInfo]-[mkdir]-[returnValue]:' + str(False) + '\n'
			return False

	#存储图片----嘿嘿嘿嘿
	def saveImages(self):
		self.errorInfo += 'Program run in Spider.saveImages()\n'
		urlList = self.getGirlUrlList()
		index = 1
		for url in urlList:
			self.programStatus += '正在处理第[' + str(index) + ']个Model的数据...\n'
			print('正在处理第[' + str(index) + ']个Model的数据...')
			SpecificGirlImagePathList = self.getSpecificGirlImagePathList(url)
			index += 1
			if SpecificGirlImagePathList == []:
				continue
			
			title = self.getImageTitle(url)
			if title == '':
				continue
			try:
				pattern = re.compile('[\u4e00-\u9fa5]', re.S)
				items = re.findall(pattern, title)
				title = ''
				for item in items:
					title += item
			except:
				self.errorInfo += '[ErrorInfo]-[saveImages-[1]]-[title]:' + title + '\n'
				continue
			self.programStatus += 'TA的个人相册名称为：[' + title + '].\n'
			print('TA的个人相册名称为：[' + title + '].')
			path = '.\\girls\\' + title
			if not self.mkdir(path):
				continue
			imageIndex = 1
			for imagePath in SpecificGirlImagePathList:
				self.programStatus += '正在抓取TA的第[' + str(imageIndex) + ']张照片,路径为：[' + imagePath + '].\n'
				print('正在抓取TA的第[' + str(imageIndex) + ']张照片,路径为：[' + imagePath + '].')
				names = imagePath.split('/')
				imageName = names[len(names)-1]
				try:
					response = urllib.request.urlopen(imagePath, timeout = 30)
					htmlData = response.read()
					with open(path + '\\' + imageName, 'wb') as f:
						f.write(htmlData)
					self.programStatus += '第[' + str(imageIndex) + ']张照片抓取完成.\n'
					print('第[' + str(imageIndex) + ']张照片抓取完成.')
					imageIndex += 1
				except:
					self.errorInfo += '[ErrorInfo]-[saveImages-[2]]-[imagePath]:' + imagePath + '-[imageName]:' + imageName + '\n'
					continue

	def saveInfos(self):
		with open('ErrorInfo.txt', 'a') as fError:
			fError.write(self.errorInfo)
		with open('ProgramStatus.txt', 'a') as fStatus:
			fStatus.write(self.programStatus)

spider = Spider()
spider.saveImages()
spider.saveInfos()
