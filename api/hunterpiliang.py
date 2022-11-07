import sys
import requests
import base64
import re


def banner():
    print("""hunter api

  _    _ _    _ _   _ _______ ______ _____  
 | |  | | |  | | \ | |__   __|  ____|  __ \ 
 | |__| | |  | |  \| |  | |  | |__  | |__) |
 |  __  | |  | | . ` |  | |  |  __| |  _  / 
 | |  | | |__| | |\  |  | |  | |____| | \ \ 
 |_|  |_|\____/|_| \_|  |_|  |______|_|  \_\



e.g python hunter.py hunter语法 获取页码 每页个数
python hunter.py xxx.com 1 10
常用语法：①  domain.suffix="domain"
        ②  icp.name="企业名"
        ③  ip="xx.xx.xx.xx/24"
        ④  header.status_code="200"
        ⑤  cert.sha-1="be7605a3b72b60fcaa6c58b6896b9e2e7442ec50"
请求后的格式为：url ip port web_title domain
        """)


def request2():
    target = baseSearch(request1(sys.argv[1]))
    page = sys.argv[2]
    size = sys.argv[3]
    data1 = {"api_key": "d6d8129025e619efc374a1f5900ee4e6052fa38f92c3cf00b547a5b2e21ed7f2",
             "search": target,
             "page": page,
             "page_size": size,
             "start_time": "\"2022-10-01 00:00:00\"",
             "end_time": "\"2022-10-31 00:00:00\"",
             "is_web": "1"}
    url = "https://hunter.qianxin.com/api/search"
    res = requests.post(url, data=data1)
    for i in res.json().get('data').get('list'):
        result = []
        domain = i.get('domain')
        ip = i.get('ip')
        port = i.get('port')
        web_title = i.get('web_title')
        component = i.get('component')
        if component:
            for k in component:
                name = k.get('name')
                version = k.get('version')
                if len(version) == 0:
                    version = "null"
                result.append(f'{name}:{version}')
        print(f'{domain} {ip} {port} {web_title} {";".join(i for i in result)}')


def baseSearch(string1):
    if "," in string1:
        string = re.sub(r",", "\n", string1)
    return str(base64.b64encode(string.encode('utf8')), 'utf-8')


def request1(string):
    target = baseSearch(string)
    headers = {"Authorization": "Bearer 3QoML:b62f7674-e679-4d4f-b0f5-5dfc571b76d4"}
    re1 = "https://hunter.qianxin.com/api/search/batch?batch_search=%s&batch_search_type=1&" % (
        target)
    res = requests.get(re1, headers=headers)
    text = res.json().get('data')
    return text


if __name__ == "__main__":
    banner()
    request2()
