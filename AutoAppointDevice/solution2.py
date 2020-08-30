from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import requests

chrome = webdriver.Chrome(executable_path=r'D:\Myprograms\chromedriver.exe')
chrome.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode')
chrome.find_element_by_id('login-username').send_keys('20520160154055')
chrome.find_element_by_id('login-password').send_keys('091218')
chrome.find_element_by_id('LoginButton').click()
# s = requests.Session()
# cookies = chrome.get_cookies()
# for cookie in cookies:
#     s.cookies.set(cookie['name'],cookie['value'])
# chrome.close()
# url = r'http://121.192.177.40/lfsms/personbook/timeadd?insid=65546&f=person&c=lfsmspersonbooktimeadd'
# headers = {
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     'Connection': 'keep-alive',
#     'Content-Length': '1334',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Host': '121.192.177.40',
#     'Origin': 'http://121.192.177.40',
#     'Referer': 'http://121.192.177.40/lfsms/personbook/timeadd?insid=65546&f=person&c=lfsmspersonbooktimeadd',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
# }
# data = {
#     'StartTime[DayDate]': '2020-09-06',
#     'StartTime[HourDate]': '22',
#     'StartTime[MinuteDate]': '00',
#     'EndTime[DayDate]': '2020-09-06',
#     'EndTime[HourDate]': '22',
#     'EndTime[MinuteDate]': '15',
#     'CAR_Tbookingrecord[BillingProFileId]': '2131967961',
#     'CAR_Tbookinghassample[SampleName]': '123',
#     'CAR_Tbookinghassample[SampleCount]': '456',
#     'CAR_Tbookinghassample[SampleDeliveryMan]': '',
#     'CAR_Tbookinghassample[SampleDeliveryTime]': '',
#     'CAR_Tbookinghassample[SamplePretreating]': '0',
#     'CAR_Tbookinghassample[SampleDetail]': '',
#     'CAR_Tbookingrecord[Comment]': '',
#     'CAR_TuserReport[subjectName]': '无',
#     'CAR_TuserReport[serviceContent]': '样品测试',
#     'CAR_TuserReport[serviceWay][]': '占用共享',
#     # 'CAR_TuserReport[serviceWay][]': '技术共享',
#     'CAR_TuserReport[subjectIncome][]': '国家自然科学基金',
#     'CAR_TuserReport[subjectArea][]': '化学',
#     'CAR_TuserReport[serviceType]': '内部用户',
#     'CAR_TuserReport[serviceDirection]': '科学研究',
#     'CAR_TuserReport[subjectContent]': '无',
#     'CAR_TuserReport[applicantUnit]': '厦门大学化学化工学院',
#     'CAR_TuserReport[record]': '无',
# }
# result = s.post(url, data=data, headers=headers)
# print(result)
# print(result.text)
# print(result.json())

chrome.get('http://121.192.177.40/lfsms/personbook/timeadd?insid=65546&f=person&c=lfsmspersonbooktimeadd')
# chrome.find_element_by_link_text('下一页').click()
chrome.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[92]/td[2]').click()
print('DONE')
