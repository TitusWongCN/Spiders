# -*- coding=utf-8 -*-
# python3
import requests
from proxies import get_proxy
from urllib.parse import urlencode

proxy = get_proxy()
feidian_headers = {
    'Host': 'short-msg-ms.juejin.im',
    'Accept': '*/*',
    'Accept-Language': 'zh-Hans-CN;q=1',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Xitu/5.7.11 (iPhone; iOS 13.3.1; Scale/3.00)',
}
pageNum = 0
feidian_data = {
    'device_id': '6FE50943-F642-4C29-B2FD-3DC27058E746',
    'src': 'ios',
    'token': 'eyJhY2Nlc3NfdG9rZW4iOiJRSjFjdWs0UUtKQXBhSHV5IiwicmVmcmVzaF90b2tlbiI6ImIwVmZzdjI0czJKQ0Q1WUgiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ%3D%3D',
    'uid': '591c1dd9a22b9d0058400e24',
}
feidian_url = 'https://short-msg-ms.juejin.im/v1/getHotRecommendList?'
feidian_page_source = requests.get(feidian_url + urlencode(feidian_data), headers=feidian_headers, proxies=proxy, verify=False).text
print(feidian_page_source)
