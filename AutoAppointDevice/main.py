from selenium import webdriver
import time
from apscheduler.schedulers.background import BackgroundScheduler


def run(chrome, target_dates, target_times):
    chrome.find_element_by_id('login-username').send_keys('20520160154055')
    chrome.find_element_by_id('login-password').send_keys('******')
    chrome.find_element_by_id('LoginButton').click()
    for date, timestamp in zip(target_dates, target_times):
        time.sleep(0.5)
        print(date, timestamp)
        chrome.get('http://121.192.177.40/lfsms/personbook/timeadd?insid=65603&f=person&c=lfsmspersonbooktimeadd')
        chrome.execute_script(js_target_datetime.replace('{{startTime}}', f'{date[0]} {timestamp[0]}').replace('{{endTime}}', f'{date[1]} {timestamp[1]}'))
        sample_name = chrome.find_element_by_id('CAR_Tbookinghassample_SampleName')
        while not sample_name:
            sample_name = chrome.find_element_by_id('CAR_Tbookinghassample_SampleName')
            time.sleep(0.2)
        sample_name.send_keys('1234')
        sample_count = chrome.find_element_by_id('CAR_Tbookinghassample_SampleCount')
        sample_count.send_keys('1234')
        chrome.execute_script('$("#formId").submit();')
    print('DONE')

if __name__ == '__main__':
    cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    target_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 7*24*60*60))
    target_next_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 8*24*60*60))
    target_times = [('22:30:00', '00:00:00'), ]
    target_dates = [(target_date, target_next_date), ]
    js_target_datetime = '$("#startTime").val("{{startTime}}");$("#endTime").val("{{endTime}}");$("#FC-Form").submit();'
    chrome = webdriver.Chrome(executable_path=r'D:\Myprograms\chromedriver.exe')
    chrome.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode')
    scheduler = BackgroundScheduler()
    scheduler.add_job(run, 'date', run_date=f'{cur_date} 22:59:55', args=(chrome, target_dates, target_times))
    scheduler.start()
    while True:
        cmd = input('请输入特定命令来执行...\n')
        if cmd == 'shutdown':
            chrome.get('http://121.192.177.40/instrument/detail-65603.html')
            btn_shutdown = chrome.find_element_by_id('CAR_Tbookinghassample_SampleName')
            sample_name = chrome.find_element_by_xpath('/html/body/div[6]/div[2]/div[2]/a[2]')
            while not sample_name:
                sample_name = chrome.find_element_by_xpath('/html/body/div[6]/div[2]/div[2]/a[2]')
                time.sleep(0.2)
                if sample_name.text.replace(' ', '') == '远程关机':
                    chrome.execute_script('closeIns(this);')
                    print('已经成功关机！')
                    break
        else:
            print('输入的命令不正确！')

