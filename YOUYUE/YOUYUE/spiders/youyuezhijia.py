# -*- coding: utf-8 -*-
import scrapy
from YOUYUE.items import YouyueItem

class YouyuezhijiaSpider(scrapy.Spider):
    name = 'youyuezhijia'
    allowed_domains = ['m.5258.cn']
    start_urls = ['http://m.5258.cn/HardyList.aspx']

    def parse(self, response):
        item = YouyueItem()
        node_list = response.xpath('//*[@id="list04"]/li')
        # print(len(node_list))
        for node in node_list:
            url = 'http://m.5258.cn/' + node.xpath('./em/a/@href').extract()[0]
            # 'http://m.5258.cn/Hardy.aspx?id=9'
            yield scrapy.Request(url,self.parse_detail,meta={'item':item})



    def parse_detail(self,response):
        item = response.meta['item']
        pj_list = response.xpath('//*[@id="ul_KeHuPJ"]/li')
        # print(len(pj_list))
        pingjia = []
        for pj in pj_list:
            temp = {}
            temp['content'] = pj.xpath('./div[@class="pfdiv"]/text()').extract()[0]
            temp['time'] = pj.xpath('./div[@class="khmc"/span[2]/text()').extract()[0].split(' ')[0]
            temp['name'] = pj.xpath('./div[@class="khmc"]/span[1]/text()').extract()[0]
            temp['score'] = 5
            pingjia.append(temp)

        print(item)

