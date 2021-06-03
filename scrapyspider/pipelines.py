# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import  JsonItemExporter
import pymssql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class ScrapyspiderPipeline:
#     def process_item(self, item, spider):
#         return item
# class JsonExporterPipeline(object):
#     def __init__(self):
#         self.file=open('article_export.json','wb')
#         self.exporter=JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
#         self.exporter.start_exporting()
#     def process_item(self,item,spider):
#         self.exporter.export_item(item)
#         return item
#     def spider_closed(self):
#         self.exporter.finish_exporting();
#         self.file.closed()
#
# class JsonWithEncodingPipeline(object):
#     def __init__(self):
#         self.file=codecs.open("article.json","a",encoding="utf-8")
#     def process_item(self,item,spider):
#         lines=json.dumps(dict(item),ensure_ascii=False)+"\n"
#         self.file.write(lines)
#         return item
#     def spider_closed(self):
#         self.file.closed()
# class ArticleImagePipeline(ImagesPipeline):
#     def item_completed(self, results, item, info):
#         image_file_path=""
#         if "front_image_url" in item:
#             for ok,value in results:
#                 image_file_path=value["path"]
#             item["front_image_path"]=image_file_path
#         return  item;
class SqlServerPipieLine(object):
    def __init__(self):
        self.conn=pymssql.connect("127.0.0.1",database="Test",user="sa",password="123456")
        self.cursor=self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = """insert into lagou_job( [url]
              ,[url_object_id]
              ,[title]
              ,[salary_min]
              ,[job_city]
              ,[work_years]
              ,[degree_need]
              ,[job_type]
              ,[publish_time]
              ,[job_advantages]
              ,[job_desc]
              ,[job_addr]
              ,[crawl_time]) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        params = (
         item.get('url',""), item.get('url_object_id',""),item.get('title',""), item.get('salary_min',""), item.get('job_city',""), item.get('work_years',""),
        item.get('degree_need',""), item.get('job_type',""), item.get('publish_time',""), item.get('job_advantages',""), item.get('job_desc',"").replace("'","''"),
        item.get('job_addr',""), item.get('crawl_time',""))
        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()

        # insert_sql="""insert into jobble_article(title,[url],[url_object_id],[front_image_url],[praise_nums],[comment_nums],[fav_nums],[content],[create_date])
        # values(%s, %s, %s, %s, %d, %d, %d, %s, %s)
        # """
        # params=list()
        # params.append(item.get("title",""))
        # params.append(item.get("url",""))
        # params.append(item.get("url_object_id",""))
        # if(item.get("front_image_url","")):
        #     params.append(item.get("front_image_url",""))
        # else:
        #     params.append("")
        # params.append(item.get("praise_nums",0))
        # params.append(item.get("comment_nums",0))
        # params.append(item.get("fav_nums",0))
        # params.append(item.get("content","").replace("'","''"))
        # params.append(item.get("create_date","1970-07-01"))
        # self.cursor.execute(insert_sql,tuple(params))
        # self.conn.commit()
        return item;




