# -*- coding=utf-8 -*-
# python3
import requests
from proxies import get_proxy
from urllib.parse import urlencode

proxy = get_proxy()
feidian_headers = {
    'Host': 'short-msg-ms.juejin.im',
    'Connection': 'keep-alive',
    'Sec-Fetch-Mode': 'cors',
    'Origin': 'https://juejin.im',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Referer': 'https://juejin.im/pins/topic/5c106be9092dcb2cc5de7257',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
pageNum = 0
feidian_data = {
    'uid': '591c1dd9a22b9d0058400e24',
    'device_id': '1586439866682',
    'token': 'eyJhY2Nlc3NfdG9rZW4iOiJRSjFjdWs0UUtKQXBhSHV5IiwicmVmcmVzaF90b2tlbiI6ImIwVmZzdjI0czJKQ0Q1WUgiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ==',
    'src': 'web',
    'topicId': '5c106be9092dcb2cc5de7257',
    'page': str(pageNum),
    'pageSize': '20',
    'rankType': 'rank',
}
feidian_url = 'https://short-msg-ms.juejin.im/v1/pinList/topic?'
feidian_page_source = requests.get(feidian_url + urlencode(feidian_data), headers=feidian_headers, proxies=proxy, verify=False).text
print(feidian_page_source)

# comment_headers = {
# 'Host': 'hot-topic-comment-wrapper-ms.juejin.im',
# 'X-Juejin-Uid': '591c1dd9a22b9d0058400e24',
# 'Accept': '*/*',
# 'X-Juejin-Token': 'eyJhY2Nlc3NfdG9rZW4iOiJtSlozeUh1ZDdvMnF2OUlvIiwicmVmcmVzaF90b2tlbiI6InJDM2FaU0FsNWp3QXBBdUEiLCJ0b2tlbl90eXBlIjoibWFjIiwiZXhwaXJlX2luIjoyNTkyMDAwfQ==',
# 'X-Juejin-Client': '6FE50943-F642-4C29-B2FD-3DC27058E746',
# 'X-Juejin-Src': 'ios',
# 'User-Agent': 'Xitu/5.7.10 (iPhone; iOS 13.3.1; Scale/3.00)',
# 'Accept-Language': 'zh-Hans-CN;q=1',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Connection': 'keep-alive',
# }
#
# comment_id = '5e97300af265da1bac6088a5'
# comment_url = 'https://hot-topic-comment-wrapper-ms.juejin.im/v1/comments/{}?'.format(comment_id)
# pageNum = 1
# comment_data = {
#     'commentId': comment_id,
#     'pageNum': pageNum,
#     'pageSize': '20',
#     'rankType': 'time',
# }
# comment_page_source = requests.get(comment_url + urlencode(comment_data), headers=comment_headers, proxies=proxy, verify=False).text
# print(comment_page_source)
#
