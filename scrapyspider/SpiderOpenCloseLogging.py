from scrapy import signals
from scrapy.exceptions import NotConfigured
class SpiderOpenCloseLogging(object):
    def __init__(self,item_count):
        self.item_count=item_count
        self.item_scraped=0
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            return NotConfigured
        item_count=crawler.settings.getint('MYEXT_ITEMCOUNT',1000)
        ext=cls(item_count)
        crawler.signals.connect(ext.spider_opened,signal=signals.spider_opened)
        crawler.singals.connect(ext.spider_closed,signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_scraped,signal=signals.item_scraped)

    def spider_opened(self,spider):
        spider.log("opened spider %s" % spider.name)
    def spider_closed(self,spider):
        spider.log("closed spider %s" % spider.name)
    def item_scraped(self,spider):
        self.items_scraped += 1
        if self.items_scraped % self.item_count == 0:
            spider.log("scraped %d items" % self.items_scraped)