import time
import execjs
import requests
def get_page(page_num,parameters):
    url='http://match.yuanrenxue.com/api/match/2?page={}'.format(page_num)
    headers={
        'Host':'match.yuanrenxue.com',
        'Referer':'http://match.yuanrenxue.com/match/2',
        'User-Agent':'yuanrenxue.project',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie':parameters
    }
    response=requests.get(url=url,headers=headers)
    return response.json()
def calculate_m_value():
    with open(r'day_02.js',encoding='utf-8',mode='r') as f:
        jsData=f.read();
        psd=execjs.compile(jsData).call('get_mvalue')
        print('parameter is',psd)
        return psd
sum_num=0
for page_num in range(1,6):
    p=calculate_m_value()
    res=get_page(page_num,p)
    data=[a['value'] for a in res['data']]
    print(data)
    sum_num+=sum(data)
print(sum_num)
