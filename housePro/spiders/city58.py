# -*- coding: utf-8 -*-
import scrapy


class City58Spider(scrapy.Spider):
    name = 'city58'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://sz.58.com/chuzu/']

    def parse(self, response):
        res = response.text
        with open('./city58.html','w',encoding='utf-8') as f:
            f.write(res)
        print(res)