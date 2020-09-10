from selenium import webdriver
import time

chrome = webdriver.Chrome(executable_path=r'D:\Myprograms\chromedriver.exe')
chrome.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode')
chrome.find_element_by_id('login-username').send_keys('20520160154055')
chrome.find_element_by_id('login-password').send_keys('******')
chrome.find_element_by_id('LoginButton').click()

chrome.get('http://121.192.177.40/lfsms/personbook/timeadd?insid=65546&f=person&c=lfsmspersonbooktimeadd')

js = '$("#startTime").val("{{startTime}}");$("#endTime").val("{{endTime}}");$("#FC-Form").submit();'
js = js.replace('{{startTime}}', '2020-09-13 08:45:00').replace('{{endTime}}', '2020-09-13 09:00:00')

chrome.execute_script(js)

sample_name = chrome.find_element_by_id('CAR_Tbookinghassample_SampleName')
while not sample_name:
    sample_name = chrome.find_element_by_id('CAR_Tbookinghassample_SampleName')
    time.sleep(1)
sample_name.send_keys('1234')
sample_count = chrome.find_element_by_id('CAR_Tbookinghassample_SampleCount')
sample_count.send_keys('1234')

chrome.execute_script('$("#formId").submit();')

print('DONE')
