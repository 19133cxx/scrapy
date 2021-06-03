# import requests
#
# response=requests.get('https://quoteapi.bookwd.com/agr-service/combine-cars?userId=664450515&nonce=1619164412616 '
#                       , headers={
#                       "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
#                       "Referer":"https://quote.bookwd.com/agro-quote/car?t=1619165408772&env=miniprogram&app_type=101&app_version=19&token_info=%7B%22userId%22%3A664450515%2C%22token%22%3A%2229430cc5c80aaefb28865eb7f0eb988539bdb78e%22%2C%22startTime%22%3A1619163882%2C%22duration%22%3A7776000%7D&deviceId=b6f59662-9c85-0366-a6ff-6a8bd74c4e8c",
#                       "Content-Type":"application/x-www-form-urlencoded"
#
#                   },
#                     params={'rid':'664450515_1619166676152',
#                             'sessiontoken': '29430cc5c80aaefb28865eb7f0eb988539bdb78e',
#                             'appversion': '19',
#                             'userid': '664450515'
#                             })
# pass;
import time


import numpy as np
import execjs

import requests
def get_page(page_num,parameters):
    url='http://match.yuanrenxue.com/api/match/1?page={}&m={}'.format(page_num,parameters)
    headers={
        'Host':'match.yuanrenxue.com',
        'Referer':'http://match.yuanrenxue.com/match/1',
        'User-Agent':'yuanrenxue.project',
        'X-Requested-With':'XMLHttpRequest'
    }
    response=requests.get(url=url,headers=headers)
    return response.json()
def calculate_m_value():
    with open(r'day_01.js',encoding='utf-8',mode='r') as f:
        jsData=f.read();
        psd=execjs.compile(jsData).call('request')
        psd=psd.replace('丨','%E4%B8%A8')
        print('parameter is',psd)
        return psd

sum_num=0
index_num=0
for page_num in range(1,6):
    res=get_page(page_num,calculate_m_value())
    data=[a['value'] for a in res['data']]
    print(data)
    sum_num+=sum(data)
    index_num+=len(data)
    time.sleep(1)
print(index_num)
average=sum_num/index_num
print('The answer is:',average)
