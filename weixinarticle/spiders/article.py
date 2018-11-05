# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from weixinarticle.items import WeixinarticleItem


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['sogou.com']
    start_urls = ['https://mp.weixin.qq.com/s?timestamp=1540881747&src=3&ver=1&signature=ysFzl4bM*PNMMoPKCbw9Ypk1yOoVtAJmJcJRzswEcunhPekfSe-SE1RoR8OOVDwaWpCpayNpRxT4B4itzp3YQKi*caQ8T8qYNZwltDeutPbbbk6ncQX--KAyp1vu*pkfd1LqF1YysL3YrqxznsBxfziFF7P4DkQ5sG8IkXZ9Sw4=']
    my_start_urls = 'https://mp.weixin.qq.com/s?timestamp=1540881747&src=3&ver=1&signature=ysFzl4bM*PNMMoPKCbw9Ypk1yOoVtAJmJcJRzswEcunhPekfSe-SE1RoR8OOVDwaWpCpayNpRxT4B4itzp3YQKi*caQ8T8qYNZwltDeutPbbbk6ncQX--KAyp1vu*pkfd1LqF1YysL3YrqxznsBxfziFF7P4DkQ5sG8IkXZ9Sw4='
    scrapyrt_urls = ''

    def modify_realtime_request(self,request):
        """如果在http接口中未传递url参数则不会调用该函数"""
        print(request.__dict__)
        url = request.__dict__['_url']
        url = 'https://' + url.replace(':','&')
        print('url:' + url)
        self.scrapyrt_urls = url
        """这样做才能支持请求转发"""
        request.__dict__['_url'] = url
        print('request.__dict__[_url]:' + request.__dict__['_url'])
        # yield SplashRequest(url=url,callback=self.scrapyrt_parse)
        return request

    def start_requests(self):
        yield SplashRequest(url=self.my_start_urls,callback=self.scrapyrt_parse)

    def parse(self, response):
        for i in range(5):
            print('-----------1-----------')
        """请求转发"""
        print('response.url:' + response.url)
        yield SplashRequest(url=response.url,callback=self.scrapyrt_parse)

    def scrapyrt_parse(self, response):
        for i in range(5):
            print('-----------2-----------')
        Item = WeixinarticleItem()
        article = ''.join(response.xpath('//div[@id="js_content"]//span//text()').extract()).strip()
        Item['url'] = response.url
        Item['content'] = article
        yield Item
        if article:
            print(article)
        else:
            for i in range(10):
                print('----------------文章为空---------------')



