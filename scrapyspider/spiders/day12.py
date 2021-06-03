import time
import execjs
import requests
import base64
def get_page(page_num,parameters):
    url='http://match.yuanrenxue.com/api/match/12?page={}&m={}'.format(page_num,parameters)
    headers={
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/12',
        'User-Agent': 'yuanrenxue.project',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response=requests.get(url=url,headers=headers)
    return response.json()
sum_num=0
for page_num in range(1,6):
    name='yuanrenxue' + str(page_num)
    m=base64.b64encode(name.encode())
    m=str(m,'utf-8')
    res=get_page(page_num,m)
    data=[a['value'] for a in res['data']]
    sum_num+=sum(data)
print(sum_num)
