# -*- coding: utf-8 -*-
import json
import time
import scrapy
from housePro.items import beikeItem

class BeikeSpider(scrapy.Spider):
    name = 'beike'
    start_urls = ['https://sz.zu.ke.com/zufang/pg1/#contentList']

    page = 1
    url_list = 'https://sz.zu.ke.com/zufang/pg%d/#contentList'
    def parse(self, response):
        house_list = response.xpath('//*[@id="content"]/div[1]/div[1]/div')
        for house_detail in house_list:
            #名称
            title = house_detail.xpath('./a/@title').extract_first()
            #位置信息
            location_info = house_detail.xpath('./div/p[2]/a/text()').extract()
            location = ''.join(location_info)
            #价格
            priceText = house_detail.xpath('./div/span/em/text()').extract_first()
            #房子code
            houseCode = house_detail.xpath('@data-house_code').extract_first()
            try:
                price = int(priceText)
            except:
                price = int(priceText.split('-')[1])

            item = beikeItem()
            item['title'] = title
            item['location'] = location
            item['price'] = price
            item['houseCode'] = houseCode
            item['page'] = self.page
            item['longlatitude']='11111111111'
            # yield item
            # 将地址逆向编码转为经纬度,用高德地图
            location_url = 'https://restapi.amap.com/v3/geocode/geo?key=c60408aad757f65d5582e09bdb7a99be&address=%s'%'深圳'+location

            yield scrapy.Request(url=location_url, callback=self.longlatitudeParse,meta={'item':item},dont_filter=True)

        #其他页码的URL链接爬取
        if self.page < 101:
            if self.page % 2==0:
                print("休息5秒")
                time.sleep(5)
            self.page += 1
            next_url = self.url_list%self.page
            yield scrapy.Request(url=next_url,callback=self.parse)

    def longlatitudeParse(self,response):
        item = response.meta['item']

        result = json.loads(response.text)
        longlatitude = result['geocodes'][0]['location']
        item['longlatitude'] = longlatitude

        yield item


