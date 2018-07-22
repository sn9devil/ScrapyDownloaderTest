# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from urllib.parse import urlencode

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {'cn': 'photography', 'listtype': 'new'}
        base_url = 'http://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        pass


