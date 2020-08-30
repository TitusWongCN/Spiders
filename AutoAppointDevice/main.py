# -*- coding=utf-8 -*-
# python37
import requests

url = r'http://121.192.177.40/lfsms/personbook/timeadd?insid=65546&f=person&c=lfsmspersonbooktimeadd'

headers = {
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Connection': 'keep-alive',
'Content-Length': '1334',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': '121.192.177.40',
'Origin': 'http://121.192.177.40',
'Referer': 'http://121.192.177.40/lfsms/personbook/timeadd?insid=65546&f=person&c=lfsmspersonbooktimeadd',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
}

cookies = {
    'CNZZDATA1277850985': '358178429-1598365423-%7C1598713171	',
    'PHPSESSID': 'rp20oodbrgn518b62pan5mql31',
    'UM_distinctid': '174260655b22bd-01a13496298562-67e153a-1fa400-174260655b3426	',
    'YII_CSRF_TOKEN': 'QUxYTmE0dVFta2FBU2VsQ293blVEZW1tUUpHTUZmZDKl8TJdc',
    'hidden': 'value',
}
cookie = ''
for name, value in cookies.items():
    cookie += '{0}={1};'.format(name, value)
cookie += '{0}={1};'.format('hidden', 'value')
headers['Cookie'] = cookies

data = {
'StartTime[DayDate]': '2020-08-30',
'StartTime[HourDate]': '20',
'StartTime[MinuteDate]': '15',
'EndTime[DayDate]': '2020-08-30',
'EndTime[HourDate]': '20',
'EndTime[MinuteDate]': '30',
'CAR_Tbookingrecord[BillingProFileId]': '2131967961',
'CAR_Tbookinghassample[SampleName]': '123',
'CAR_Tbookinghassample[SampleCount]': '456',
'CAR_Tbookinghassample[SampleDeliveryMan]': '',
'CAR_Tbookinghassample[SampleDeliveryTime]': '',
'CAR_Tbookinghassample[SamplePretreating]': '0',
'CAR_Tbookinghassample[SampleDetail]': '',
'CAR_Tbookingrecord[Comment]': '',
'CAR_TuserReport[subjectName]': '无',
'CAR_TuserReport[serviceContent]': '样品测试',
'CAR_TuserReport[serviceWay][]': '占用共享',
'CAR_TuserReport[serviceWay][]': '技术共享',
'CAR_TuserReport[subjectIncome][]': '国家自然科学基金',
'CAR_TuserReport[subjectArea][]': '化学',
'CAR_TuserReport[serviceType]': '内部用户',
'CAR_TuserReport[serviceDirection]': '科学研究',
'CAR_TuserReport[subjectContent]': '无',
'CAR_TuserReport[applicantUnit]': '厦门大学化学化工学院',
'CAR_TuserReport[record]': '无',
}

result = requests.post(url, data=data)
print(result)
print(result.json())

