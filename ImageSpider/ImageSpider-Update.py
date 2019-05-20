#-*- coding:utf-8 -*-
# python3

import os
import re
import requests
import threading
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from collections import deque

class ImageSpider:
    def __init__(self):
        self.init_url = r'http://www.mzitu.com/all/'
        self.model_count = 0
        self.deque_model_urls = deque()
        self.deque_model_title = deque()
        self.file_handled_path = r'HandledUrls.txt'
        self.handled_urls = list()

    def read_file(self, file):
        print('正在加载已经下载的url列表...')
        if os.path.exists(self.file_handled_path):
            with open(self.file_handled_path, 'r') as f_read:
                file_content = f_read.readlines()
                self.handled_urls = [line.strip().replace('\n', '') for line in file_content]
    
    def write_file(self, file, content):
        lock = threading.Lock()
        lock.acquire()#锁住
        file.write(content)
        file.flush()
        file.close()
        lock.release()#解锁

    def is_handled_urls(self, url):
        if url in self.handled_urls:
            return True
        else:
            return False

    def get_models_url(self):
        print('正在分析最新的url...')
        soup = BeautifulSoup(requests.get(self.init_url).text, 'html.parser')
        items = re.findall(re.compile('<a href="(.*?)" target="_blank">(.*?)</a>', re.S), str(soup.select('body > div.main > div.main-content > div.all')))
        i = 0
        for item in items:
            if item[0][len(item[0]) - 1] >= '0' and item[0][len(item[0]) - 1] <= '9':
                if not self.is_handled_urls(item[0]):
                    try:
                        title = item[1].encode('utf-8').decode('utf-8')
                        # print(title)
                    except:
                        continue
                    self.deque_model_urls.append(item[0])
                    self.deque_model_title.append(item[1])
                    self.model_count += 1
        print('准备开始逐个url进行爬取...')

    def get_single_model(self, url, title):
        folder_dir = 'girls\\' + title + '\\'
        if self.make_model_dir(folder_dir):
            image_count = self.get_pic_count(url)
            for index in range(1, image_count + 1):
                image_page_url = url + '/' + str(index)
                soup = BeautifulSoup(requests.get(image_page_url).text, 'html.parser')
                image_url = re.findall(re.compile('src="(.*?)"/>', re.S), str(soup.select('body > div.main > div.content > div.main-image > p > a > img')))[0]
                image_name = image_url.split('/')[len(image_url.split('/')) - 1]
                image_file_dir = folder_dir + image_name
                image_file = open(image_file_dir, 'wb')
                self.write_file(image_file, requests.get(image_url).content)
            f_write = open(self.file_handled_path, 'a')
            self.write_file(f_write, url + '\n')
            print('【' + title + '】下共' + str(image_count) + '张照片全部下载完成!')

    def get_pic_count(self, url):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        items = re.findall(re.compile('<span>(.*?)</span>', re.S), str(soup.select('body > div.main > div.content > div.pagenavi')))
        return int(items[len(items) - 2])

    def make_model_dir(self, folder_dir):
        try:
            isExists = os.path.exists(folder_dir)
            if not isExists:
                os.makedirs(folder_dir)
            return True
        except:
            return False

    def main(self):
        self.read_file(self.file_handled_path)
        self.get_models_url()
        # self.get_single_model(self.deque_model_urls.popleft(), self.deque_model_title.popleft())
        p = Pool(4)
        for i in range(self.model_count):
            p.apply_async(self.get_single_model, args=(self.deque_model_urls.popleft(), self.deque_model_title.popleft()))
        p.close()
        p.join()
        print('处理结束，请查看源程序所在文件夹下的girls文件夹!')
        

# 박시현
if __name__ == '__main__':
    time1 = time.time()
    imagespider = ImageSpider()
    imagespider.main()
    timespan = time.time() - time1
    hour = timespan // 3600
    minute = (timespan - 3600 * hour) // 60
    second = int((timespan - 3600 * hour - 60 * minute))
    print('本次任务花费时间: %d:%d:%d.' % (hour, minute, second))
