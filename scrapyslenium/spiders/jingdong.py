# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapyslenium.items import ProductItem
from urllib.parse import quote


class JingdongSpider(Spider):
    name = 'jingdong'
    allowed_domains = ['www.jingdong.com']
    # start_urls = ['https://www.jingdong.com/']
    base_url = "https://search.jd.com/Search?keyword="
    def start_requests(self):
        for keyword in self.settings.get("KEYWORDS"):
            for page in range(1, self.settings.get("MAX_PAGE"+1)):
                url = self.base_url + quote(keyword)
                # 每次搜索的url相同，可用meta 参数传递分页页码
                # dont_filter 不去重
                yield Request(url=url, callback=self.parse, meta={"page": page}, dont_filter=True)

    def parse(self, response):
        products = response.xpath("//*[@id='J_goodsList']/ul/li")
        for product in products:
            item = ProductItem()
            # item["price"] = 