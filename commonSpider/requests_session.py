
import time
import requests

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

def gethtml(url):
    i = 0
    while i < 3:
        try:
            html = requests.get(url, timeout=5).text
            return html
        except requests.exceptions.RequestException:
            i += 1

url_login = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/'
url_login = 'http://192.168.43.249:8000/article/'

session = requests.Session()
s = session.get(url_login, headers=headers)
r = requests.get(url_login, headers=headers)
for k, v in s.headers.items():
    print('{}:{}'.format(k, v))
print('&'*20)
for k, v in r.headers.items():
    print('{}:{}'.format(k, v))



# session.post(url_login, data={'csrfmiddlewaretoken': token, 'username': 'xx', 'password': 'xx'})

print(time.strftime('%Y-%m-%d %H:%M:%S'))


