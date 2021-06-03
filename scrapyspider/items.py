# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from  itemloaders.processors import MapCompose,TakeFirst,Identity
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
def add_jobble(value):
    return value+'  -  jobble'
def add_test(value):
    return value+'  - test '
def data_cnvert(value):
    match_re=re.match(".*?(\d+.*)",value)
    if match_re:
        return match_re.group(1)
    else:
        return '1970-07-01'

class JobBobbleArticleItem(scrapy.Item):
    title=scrapy.Field()
    create_date=scrapy.Field(
        output_processor=MapCompose(data_cnvert)
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=Identity()
    )
    front_image_path=scrapy.Field()
    praise_nums=scrapy.Field()
    comment_nums=scrapy.Field()
    fav_nums=scrapy.Field()
    content=scrapy.Field()
def Remove_Splash(value):
    return value.replace("/","");
def handle_jobaddr(value):
    addr_list=value.split('\n');
    addr_list=[item.strip() for item in addr_list if item.strip()!='查看地图']
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
class LagouJobItem(scrapy.Item):
    title=scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    salary_min=scrapy.Field()
    job_city=scrapy.Field(
        input_processor=MapCompose(Remove_Splash)
    )
    work_years=scrapy.Field()
    degree_need=scrapy.Field()
    job_type=scrapy.Field()
    publish_time=scrapy.Field()
    job_advantages=scrapy.Field()
    job_desc=scrapy.Field(

    )
    job_addr=scrapy.Field(
        input_processor=MapCompose(remove_tags,handle_jobaddr)
    )
    crawl_time=scrapy.Field()
