import datetime
from unittest import signals

import scrapy
from pydispatch import dispatcher
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from scrapyspider.items import LagouJobItemLoader,LagouJobItem
from scrapyspider import common
from selenium.webdriver.chrome.options import Options
import  undetected_chromedriver as uc

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=(r'zhaopin/.*',)),follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),



    )


    # def clickOption(self,optionTitle) {
    #
    #     self.browser.find_element_by_xpath("//li[@class='multi-chosen']//span[contains(text(),'" + choseTitle + "')]"));
    # WebElement
    # optionElement = chosenElement.findElement(By.xpath("../a[contains(text(),'" + optionTitle + "')]"));
    # optionElement.click();
    # }



    def __init__(self):

        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser=webdriver.Chrome(executable_path="D:/作业/chromedriver_win32/chromedriver.exe",chrome_options=chrome_option)
        super(LagouSpider,self).__init__()
        self.url = 'https://passport.lagou.com/login/login.html'
        self.cookies_dict = {}
        self.cookies = []




    def parse_job(self,response):
        item_loader=LagouJobItemLoader(item=LagouJobItem(),response=response)
        item_loader.add_css('title','.job-name::attr(title)')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',common.get_md5(response.url))
        item_loader.add_css('salary_min','.job_request .salary::text')
        item_loader.add_xpath('job_city','//*[@class="job_request"]/h3/span[2]/text()')
        #span 从1 开始
        item_loader.add_xpath('work_years','//*[@class="job_request"]/h3/span[3]/text()')
        item_loader.add_xpath('degree_need', '//*[@class="job_request"]/h3/span[4]/text()')
        item_loader.add_xpath('job_type', '//*[@class="job_request"]/h3/span[5]/text()')
        item_loader.add_css('publish_time','.publish_time::text')
        item_loader.add_css('job_advantages','.job-advantage p::text')
        item_loader.add_css('job_desc','.job_bt div')
        item_loader.add_css('job_addr','.work_addr')
        item_loader.add_value('crawl_time',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


        item= item_loader.load_item();
        return  item





