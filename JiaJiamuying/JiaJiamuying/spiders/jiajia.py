# -*- coding: utf-8 -*-
import scrapy,json
import time
from JiaJiamuying.items import JiajiamuyingItem

class JiajiaSpider(scrapy.Spider):
    name = 'jiajia'
    allowed_domains = ['sz.jjys168.com']
    start_urls = ['http://sz.jjys168.com/api/?page=%s&force_desc=1&methodName=YuesaoIndex&size=20'%(i) for i in range(1,13)]
    # http://sz.jjys168.com/api/?page=39&force_desc=1&methodName=YuesaoIndex&size=6

    def parse(self, response):
        # item = JiajiamuyingItem()
        node_list = json.loads(response.text)['data']['data']
        for node in node_list:
            item = JiajiamuyingItem()
            item['name'] = node['nickname']
            id = node['id']
            url = 'http://sz.jjys168.com/api/?methodName=YuesaoCommentList&yuesao_id=' + str(id)
            yield scrapy.Request(url,callback=self.parse_detail,meta={'item':item})

    def parse_detail(self,response):
        item = response.meta['item']
        node_list = json.loads(response.text)['data']['data']
        pingjia = []
        if len(node_list) > 0:
            for node in node_list:
                temp = {}
                temp['name'] = node['username']

                timestamp= int(node['time'])
                # 转换成localtime
                time_local = time.localtime(timestamp)
                # 转换成新的时间格式(2016-05-05 20:28:54)
                temp['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

                temp['score'] = node['score']
                temp['content'] = node['detail']

                pingjia.append(temp)
        item['pingjia'] = pingjia

        print(item['name'])
        yield item

