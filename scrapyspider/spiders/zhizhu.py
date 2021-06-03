import random

import scrapy
import re
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import cv2
import numpy as np
import requests
from scrapy import Request
import re
from http import cookiejar


from PIL import Image
from io import BytesIO

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ZhihuSpider(scrapy.Spider):
    name="zhihu"
    allowed_domains=["www.zhihu.com"]
    start_urls=['https://www.zhihu.com/']
    def login(self):
        import time
        try:
            self.browser.maximize_window()
        except Exception as e:
            pass

    def change_size(self, file):
        image = cv2.imread(file, 1)  # 读取图片 image_name应该是变量
        #cv2.imwrite('2.jpg',image);
        img = cv2.medianBlur(image, 5)  # 中值滤波，去除黑色边际中可能含有的噪声干扰
        # print(img.shape)


        b = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)  # 调整裁剪效果

        binary_image = b[1]  # 二值图--具有三通道
        binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('2.jpg', binary_image);
        x, y = binary_image.shape
        edges_x = []
        edges_y = []
        for i in range(x):
            for j in range(y):
                if binary_image[i][j] == 255:
                    edges_x.append(i)
                    edges_y.append(j)

        left = min(edges_x)  # 左边界
        right = max(edges_x)  # 右边界
        width = right - left  # 宽度
        bottom = min(edges_y)  # 底部
        top = max(edges_y)  # 顶部
        height = top - bottom  # 高度
        pre1_picture = image[left:left + width, bottom:bottom + height]  # 图片截取
        # cv2.imwrite('2.jpg', pre1_picture);
        # print(pre1_picture.shape)
        return pre1_picture  # 返回图片数据

    def get_tracks(self, distance, seconds, ease_func):
        distance += 20
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            ease = ease_func
            offset = round(ease(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        tracks.extend([-3, -2, -3, -2, -2, -2, -2, -1, -0, -1, -1, -1])
        return tracks





    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)


    def start_requests(self):
        from selenium.webdriver.chrome.options import Options
        chrome_option=webdriver.ChromeOptions()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
        # prefs={"profile.managed_default_content_settings.images":2}
        # chrome_option.add_experimental_option("prefs",prefs)
        #--remote-debugging-port=9222

        browser=webdriver.Chrome(executable_path="D:/作业/chromedriver_win32/chromedriver.exe",chrome_options=chrome_option)
        browser.get("https://www.zhihu.com/signin")
        self.login()

        self.wait = WebDriverWait(browser,10)

        browser.find_element_by_css_selector('.SignFlow-tabs .SignFlow-tab:nth-child(2)').click()
        browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('13739049907')

        browser.find_element_by_css_selector('.SignFlow-password input').send_keys(Keys.CONTROL+'a')
        browser.find_element_by_css_selector('.SignFlow-password input').send_keys('2358132134cxx')
        browser.find_element_by_css_selector('.Button.SignFlow-submitButton.Button--primary.Button--blue').click()
        time.sleep(2)

        # iframe=browser.find_element_by_xpath('/html/body/div[4]/iframe')
        # browser.switch_to.frame(iframe)

        # element1=browser.find_element_by_tag_name('body')
        #
        # html=element1.get_attribute('innerHTML')
        bg_img_scr = browser.find_element_by_xpath('//img[@class="yidun_bg-img"]').get_attribute('src')


        front_img_src = browser.find_element_by_xpath('//img[@class="yidun_jigsaw"]').get_attribute('src')

        # 把图片下载到本地
        with open(r'bg.jpg', mode='wb') as f:
            f.write(requests.get(bg_img_scr).content)
            # f.close()
        with open(r'front.jpg', mode='wb') as f:
            f.write(requests.get(front_img_src).content)
            # f.close()
        bg = cv2.imread(r'bg.jpg')

        img_rgb = self.change_size('front.jpg')
        cv2.imwrite('1.jpg', img_rgb);
        img_rgb[np.where((img_rgb == [0,0,0]).all(axis=2))] = [255,255,255];
        cv2.imwrite('2.jpg',img_rgb)







        bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        front = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # h,w=front.shape[:-1]
        # front = 255 - front
        # front = front[front.any(1)]
        result = cv2.matchTemplate(bg, front, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(result >= threshold)
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2
        track=self.get_tracks((loc[1][0] + 7), 3, self.ease_out_quart)
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(browser).click_and_hold(slider).perform()
        while track:
            x = track.pop(0)
            ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.05)
        time.sleep(0.05)
        ActionChains(browser).release().perform()
        # index_max = np.argmax(result)
        # x, y = np.unravel_index(index_max, result.shape)
        # drop = browser.find_element_by_xpath('//div[@class="yidun_slide_indicator"]')
        # ActionChains(browser).drag_and_drop_by_offset(drop, xoffset=loc[1][0], yoffset=0).perform()

        # browser.switch_to.default_content()
        html2=browser.find_element_by_tag_name('body').get_attribute('innerHTML')
        browser.find_element_by_css_selector('#Popover1-toggle').send_keys('黄景瑜许魏洲')

        browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/header/div[1]/div[1]/div/form/div/div/label/button').click();
        time.sleep(2)
        for i in range(3):
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
        # post_nodes=browser.find_elements_by_css_selector('.Search-container h2')[:1]
        # for post_node in post_nodes:
        #     name=post_node.find_element_by_xpath('div/meta[2]').get_attribute('content')
        #     if '黄景瑜' in name and '许魏洲' in name:
        #         url=post_node.find_element_by_xpath('div/a').get_attribute('href')
        #         header={
        #             'Host':'www.zhihu.com',
        #             'accept - encoding':'gzip, deflate, br',
        #             'Referer':'https://www.zhihu.com/',
        #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        #                           '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        #         }
        #         yield Request(url, method='get', headers=header, callback=self.parse_detail)
        #         pass;
        pass;


    import matplotlib.pyplot as plt
    def parse_detail(self,response):
        div=response.css('div.QuestionFollowStatus')
        strong=div.css('strong::attr(title)').extract()
        follow_number=strong[0]
        answer_number=strong[1]
        answer_number1=response.css('a.QuestionMainAction.ViewAll-QuestionMainAction::text')[0].extract()
        answer_number=re.search('\d+\,\d+',answer_number1).group()
        answer_number=answer_number.replace(',','');
        pass;


# user_agent_list={
#    "Mozilla / 5.0(Linux;Android4.0.4;GalaxyNexusBuild / IMM76B) AppleWebKit / 535.19(KHTML, likeGecko) Chrome / 18.0.1025.133MobileSafari / 535.19",
#    "Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"
# }
# import random
# random_index=random.randint(0,len(user_agent_list)-1)
# random_agent=user_agent_list[random_index]




