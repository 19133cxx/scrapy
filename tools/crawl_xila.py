import requests
from scrapy.selector import Selector
import pymssql

conn = pymssql.connect("127.0.0.1", database="Test", user="sa", password="123456")
cursor = conn.cursor()

#获取ip地址
def crawl_ips():
    header={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    for i in range(1,10):
        re=requests.get('http://www.xiladaili.com/gaoni/{0}'.format(i),headers=header)
        selector=Selector(re)
        all_trs=selector.css('.fl-table tbody tr')
        ip_list=[]
        for tr in all_trs:
            Ip_Address=tr.css('td:nth-child(1)::text').extract_first('')
            speed_str=tr.css('td:nth-child(5)::text').extract_first('')
            ip_list.append((Ip_Address,speed_str))
        for ip in ip_list:

            insert_sql = """insert into proxy_ip([Ip_Address],[speed_str]) values(%s, %s)
                   """
            params = (
               ip[0],ip[1])
            print(ip[0])
            cursor.execute(insert_sql, tuple(params))
            conn.commit()
        ip_list=[]


class Get_Ip(object):
    def delete(self,ip):
        delete_sql="delete * from proxy_ip where [Ip_Address]={0}".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True;
    def judge_ip(self,ip):
        http_url="http://www.baidu.com"
        proxy_url="https://{0}".format(ip)
        try:
            proxy_dict={
                'http':proxy_url,
                'https':proxy_url
            }
            response=requests.get(http_url,proxies=proxy_dict)
        except Exception as e:
            self.delete(ip)
            return False
        else:
            code=response.status_code
            if code>=200 and code<300:
                print("effective ip")
                return True;
            else:
                print('invalid')
                self.delete(ip)
                return False;

    def get_url(self):
        sql="select ip from [proxy_ip] order by rand() limit 1"
        result=cursor.execute(sql)

        for ip_info in cursor.fetchall():
            Ip_Address=ip_info[0]
            j_r=self.judge_ip(Ip_Address)
            if j_r:
                return Ip_Address
            else:
                return self.get_url()
# print(crawl_ips())
# # get_ip=Get_Ip()
# # get_ip.get_url()