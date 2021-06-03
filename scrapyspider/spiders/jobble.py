import json

import scrapy
from urllib import parse
from scrapy import Request
import re

from scrapyspider import common
from scrapyspider.items import  JobBobbleArticleItem
from scrapyspider.items import ArticleItemLoader


import requests
from protego import Protego
class JobbleSpider(scrapy.Spider):
    name="jobble"
    allowed_domains=['news.cnblogs.com']
    start_urls=['http://news.cnblogs.com/']
    def parse(self,response):
        # url= response.xpath('//*[@id="entry_685742"]/div[2]/h2/a/@href').get()
        # pass;
        # url=response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        post_nodes=response.css('#news_list .news_block')

        for post_node in post_nodes:
            imgae_url=post_node.css('.entry_summary a img::attr(src)').extract_first("")
            if imgae_url.startswith('//'):
                imgae_url="https:"+imgae_url
            post_url=post_node.css('.news_entry a::attr(href)').extract_first("")
            url = parse.urljoin(response.url, post_url)
            yield Request(url, meta={"front_image_url":imgae_url},callback=self.parse_detail)
    #         # next_url=response.css('div.pager a:last-child::text').extract_first('');
    #         # if next_url=='Next >':
    #         #     next_url=response.css('div.pager a:last-child::attr(href)').extract_first("")
    #         #     yield Request(url=parse.urljoin(response.url, next_url),call_back=self.parse)
    #             #这里的解析函数是parse，因为这里是下一页的内容
    #     pass;
    def parse_detail(self,response):

        match_re=re.match(".*?(\d+)",response.url)

        if match_re:
            post_id = match_re.group(1)
            # article_item=JobBobbleArticleItem()
            # title = response.css('#news_title a::text').extract_first('')
            # create_date = response.css('#news_info .time::text').extract_first('')
            # match_re=re.match(".*?(\d+.*)",create_date)
            # if match_re:
            #     create_date=match_re.group(1)
            # content = response.css('#news_content').extract_first('')

            # article_item["title"]=title
            # article_item["create_date"]=create_date
            # article_item["content"] = content
            # article_item["url"]=response.url
            # if response.meta.get("front_image_url",""):
            #     article_item["front_image_url"] = ["https:"+response.meta.get("front_image_url")]
            # else:
            #     article_item["front_image_url"]=[]
            item_Loader=ArticleItemLoader(item=JobBobbleArticleItem(),response=response)
            item_Loader.add_css('title','#news_title a::text')
            item_Loader.add_css('create_date', '#news_info .time::text')
            item_Loader.add_css('content','#news_content')
            item_Loader.add_value("url",response.url)
            item_Loader.add_value("front_image_url",response.meta.get("front_image_url"))
            article_item=item_Loader.load_item()

            yield Request(url=parse.urljoin(response.url,"/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={"article_item":article_item},callback=self.parse_nums)
            pass;
    def parse_nums(self,response):
        article_item=response.meta.get("article_item")

        j_data = json.loads(response.text)
        praise_nums=j_data["DiggCount"]
        fav_nums=j_data["TotalView"]
        comment_nums=j_data["CommentCount"]
        article_item["praise_nums"] = praise_nums
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["url_object_id"] = common.get_md5(article_item["url"])
        yield article_item;
