# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import json
#
# class JiajiamuyingPipeline(object):
#     def open_spider(self, spider):
#         self.file = open('jiajiayuesao.json', 'w')
#
#     def process_item(self, item, spider):
#         str_data = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#         self.file.write(str_data)
#         return item
#
#     def close_spider(self, spider):
#         self.file.close()

import pymysql

class UrlPipeline(object):

    def __init__(self):
        try:
            self.db = pymysql.connect(host="127.0.0.1", user="root", passwd="mysql", port=3306, db="yuesao_info",  charset="utf8",use_unicode=True)
            self.cursor = self.db.cursor()
            print("Connect to db successfully!")

        except:
            print("Fail to connect to db!")

    def process_item(self, item, spider):
        try:
            # 插入数据
            # self.cursor.execute(
            #     "insert into yuesao(name,pingjia) values (%s,%s)",(item['name'],item['pingjia'][0]['content']))
            if item['pingjia']:
                u = 0
                for pingjia in item['pingjia']:
                    uname = pingjia['name']
                    content = pingjia['content']
                    time = pingjia['time']
                    score = pingjia['score']
                    param = (item['name'], uname,content, time, score,)
                    sql = "insert into yusao_pingjia_pingjia_info (name, uname,content, time, score) values(%s,%s,%s,%s,%s)"
                    self.cursor.execute(sql, param)
                    u = u + 1
                    # 提交sql语句
                    self.db.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item


def close_spider(self, spider):
        # self.db.commit()
        self.db.close
        print("Done")