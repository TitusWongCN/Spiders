import requests

s = requests.session()
# step1
step1_url = r'http://121.192.177.40/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': '121.192.177.40',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
}
response = s.get(step1_url, headers=headers)
cookies = {}
for key, value in response.cookies.items():
    cookies[key] = value
print(cookies)

# step2
step2_url = r'http://open.xmu.edu.cn/Login?ReturnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode'
headers = {
    'Referer': 'http://121.192.177.40/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
}
response = s.get(step2_url, headers=headers)
token = response.text.split('__RequestVerificationToken')[1].split('value="')[1].split('" />')[0]
token_cookie = response.cookies['__RequestVerificationToken']
print(token)
print(token_cookie)

#step3
step3_url = r'http://open.xmu.edu.cn/Login?ReturnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '192',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__RequestVerificationToken={}'.format(token_cookie),
    'Host': 'open.xmu.edu.cn',
    'Origin': 'http://open.xmu.edu.cn',
    'Referer': 'http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
}
data = {
    '__RequestVerificationToken': token,
    'UserName': '20520160154055',
    'Password': '091218',
    'RememberMe': 'false',
}
response = s.post(step3_url, headers=headers, data=data)
print(response.text)
for a in response.cookies.items():
    print(a)
aspx_cookie = response.cookies['.ASPXAUTH']
print(aspx_cookie)

#step4
step4_url = r'http://open.xmu.edu.cn/oauth2/authorize?client_id=1089&response_type=code'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '__RequestVerificationToken={}; .ASPXAUTH={}'.format(token_cookie, aspx_cookie),
    'Host': 'open.xmu.edu.cn',
    'Referer': 'http://open.xmu.edu.cn/Login?returnUrl=http%3A%2F%2Fopen.xmu.edu.cn%2Foauth2%2Fauthorize%3Fclient_id%3D1089%26response_type%3Dcode',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
}
result = s.get(step4_url, headers=headers)
location = result.headers['Location']
print(location)

#step5
step5_url = location
