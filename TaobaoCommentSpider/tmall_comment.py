# -*- coding=utf-8 -*-
# python3
import requests
import re
import json
import xlwt
from proxies import get_proxy


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿


def process_comment_json(comment_data):
    result = []
    for rate in comment_data['rateDetail']['rateList']:
        username = rate['displayUserNick']
        rate_date = rate['rateDate']
        good_desc = rate['auctionSku']
        rate_comment = rate['rateContent']
        rate_pic = ','.join(rate['pics'])
        rate_video = ','.join(video['cloudVideoUrl'] for video in rate['videoList'])
        result.append([username, rate_date, good_desc, rate_comment, rate_pic, rate_video])
    return result


def get_comments(good_id):
    proxy = get_proxy()
    headers = {
        'cookie': 'cna=qMU/EQh0JGoCAW5QEUJ1/zZm; enc=DUb9Egln3%2Fi4NrDfzfMsGHcMim6HWdN%2Bb4ljtnJs6MOO3H3xZsVcAs0nFao0I2uau%2FbmB031ZJRvrul7DmICSw%3D%3D; lid=%E5%90%91%E6%97%A5%E8%91%B5%E7%9B%9B%E5%BC%80%E7%9A%84%E5%A4%8F%E5%A4%A9941020; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; x=__ll%3D-1%26_ato%3D0; t=2c579f9538646ca269e2128bced5672a; _m_h5_tk=86d64a702eea3035e5d5a6024012bd40_1551170172203; _m_h5_tk_enc=c10fd504aded0dc94f111b0e77781314; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTZ5bI3949Xhg%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByEzZ1MVSremcx%2BQ%3D&id2=UNcPuUTqrGd03w%3D%3D&nk2=F5RAQ19thpZO8A%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=tb51552614; _l_g_=Ug%3D%3D; ck1=""; unb=3778730506; lgc=tb51552614; cookie1=UUBZRT7oNe6%2BVDtyYKPVM4xfPcfYgF87KLfWMNP70Sc%3D; login=true; cookie17=UNcPuUTqrGd03w%3D%3D; cookie2=1843a4afaaa91d93ab0ab37c3b769be9; _nk_=tb51552614; uss=""; csg=b1ecc171; skt=503cb41f4134d19c; _tb_token_=e13935353f76e; x5sec=7b22726174656d616e616765723b32223a22393031623565643538663331616465613937336130636238633935313935363043493362302b4d46454e76646c7243692b34364c54426f4d4d7a63334f44637a4d4455774e6a7378227d; l=bBIHrB-nvFBuM0pFBOCNVQhjb_QOSIRYjuSJco3Wi_5Bp1T1Zv7OlzBs4e96Vj5R_xYB4KzBhYe9-etui; isg=BDY2WCV-dvURoAZdBw3uwj0Oh2yUQwE5YzQQ9qAfIpm149Z9COfKoZwV-_8q0HKp',
        'Referer': 'https://detail.tmall.com/item.htm?id={}'.format(good_id),
        'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    good_url = 'https://detail.tmall.com/item.htm?id={}'.format(good_id)
    good_page_source = requests.get(good_url, headers=headers, proxies=proxy, verify=False).text
    seller_id = re.findall(re.compile('"sellerId\":(.*?),\"'), good_page_source)[0]
    # print(seller_id)
    comment_base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}&currentPage={}&callback=jsonp1240'
    comment_url = comment_base_url.format(good_id, seller_id, 1)
    comment_data = requests.get(comment_url, headers=headers, proxies=proxy, verify=False).text
    comment_data = json.loads('('.join(comment_data.split('(')[1:])[:-1])
    results = [['昵称', '时间', '商品型号', '评论内容', '评论附图地址', '评论附视频地址'], ]
    results.extend(process_comment_json(comment_data))
    total_page_count = comment_data['rateDetail']['paginator']['lastPage']
    for page_index in range(1, total_page_count):
        comment_url = comment_base_url.format(good_id, seller_id, page_index + 1)
        comment_data = requests.get(comment_url, headers=headers, proxies=proxy, verify=False).text
        comment_data = json.loads('('.join(comment_data.split('(')[1:])[:-1])
        results.extend(process_comment_json(comment_data))
    write_excel_xls('./{}.xls'.format(good_id), good_id, results)


if __name__ == '__main__':
    get_comments('544116301715')
    # get_comments('613513501413')
