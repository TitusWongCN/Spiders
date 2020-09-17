from selenium import webdriver
import time
from apscheduler.schedulers.background import BackgroundScheduler

_desc_ = '''
****************************************************************
     本软件仅供学习和交流，请勿滥用，更请不要外传，谢谢！   
----------------------------------------------------------------
---->  软件将会按照预设的时间和规则自动执行任务，请耐心等待！
---->  如果需要远程关机，请在本窗口输入：shutdown然后回车
---->  有任何问题请及时联系公众号：TitusCosmos！
****************************************************************
'''


def run(chrome, target_dates, target_times):
    print(f"当前时间为：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
    print(f'即将自动登录...')
    chrome.find_element_by_id('login-username').send_keys('20520160154055')
    chrome.find_element_by_id('login-password').send_keys('091218')
    chrome.find_element_by_id('LoginButton').click()
    while True:
        cur_hour = time.strftime('%H', time.localtime(time.time()))
        if cur_hour != '23':
            time.sleep(0.5)
        else:
            break
    print('已成功登录！')
    print(f"当前时间为：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
    for date, timestamp in zip(target_dates, target_times):
        print(f'即将自动预约时间段：{date[0]} {timestamp[0]}~{date[1]} {timestamp[1]}...')
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
        print(f'本时间段预约结束！')
        print(f"当前时间为：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
    time.sleep(2)
    print('此次预约已经全部完成，请点击谷歌浏览器查看！')
    chrome.get('http://121.192.177.40/lfsms/personbook/time?f=book&c=lfsmspersonbooktime')

if __name__ == '__main__':
    print(_desc_)
    print(f"当前时间为：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
    cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(f'当前日期为：{cur_date}')
    target_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 7*24*60*60))
    print(f'要预约的日期为：{target_date}')
    target_next_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 8*24*60*60))
    target_times = [('22:30:00', '00:00:00'), ]
    for target_time in target_times:
        print(f'要预约的时间段为：{target_time[0]} ~ {target_time[1]}')
    target_dates = [(target_date, target_next_date), ]
    js_target_datetime = '$("#startTime").val("{{startTime}}");$("#endTime").val("{{endTime}}");$("#FC-Form").submit();'
    print(f'正在打开浏览器...')
    print(f'程序将在临近23:00:00时自动登录，请勿关闭本窗口和浏览器窗口！')
    chrome = webdriver.Chrome(executable_path=r'./chromedriver.exe')
    chrome.get('http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode')
    login_timestamp = time.mktime(time.strptime(f'{cur_date} 22:55:00', '%Y-%m-%d %H:%M:%S'))
    if time.time() > login_timestamp:
        run(chrome, target_dates, target_times)
    else:
        scheduler = BackgroundScheduler()
        scheduler.add_job(run, 'date', run_date=f'{cur_date} 22:55:00', args=(chrome, target_dates, target_times))
        scheduler.start()
    while True:
        cmd = input('请输入特定命令来执行: ')
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
