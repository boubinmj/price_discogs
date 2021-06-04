from price_discogs.items import PriceDiscogsItem
from scrapy import Spider, Request
import re

class PriceDiscogsSpider(Spider):
    name = "price_discogs_spider"
    allowed_urls = ['https://www.discogs.com/my']
    start_urls = ['https://www.discogs.com/sell/list?format=Vinyl&page=1']


    def parse(self, response):
        start_index = 1496243908
        duration = 100
        page_urls = [f'https://www.discogs.com/sell/list?format=Vinyl&page={i}' for i in range(1,2)]

        page_bottom = response.xpath('//div[@class="pagination bottom "]//strong[@class="pagination_total"]/text()').extract_first().strip()
        '1 – 25 of 42,580,313'
        groups = re.search('1 – (\d+) of (\d+)',page_bottom)
        per_page = groups.group(1)

        for url in page_urls:
            try:
                yield Request(url=url, callback=self.parse_results_page)
            except:
                continue

    def parse_results_page(self, response):

        album_urls = response.xpath('//a[@class="item_description_title"]/@href').extract()
        #print(album_urls)
        album_urls = ['https://www.discogs.com' + url for url in album_urls]

        #print(album_urls)

        for url in album_urls:
            yield Request(url=url, callback=self.parse_listing_page)

    def parse_listing_page(self, response):
        

        artist = response.xpath('//*[@id="profile_title"]/span[1]/span/a/text()').extract_first()
        year = response.xpath('.//div[@class="content"][4]/text()').extract_first().strip()
        currency = response.xpath('.//div[@class="content"][3]/text()').extract_first().strip()
        if(currency == 'US'):
            price = response.xpath('.//span[@class="price"]/text()').extract_first()
            shipping = response.xpath('.//span[@class="reduced"]/text()').extract_first().strip()
            # p = re.search('$(\d+)',price)
            # shp = re.search('+ $(\d+) shipping',shipping)
            # total_price = float(p.p(1)) + float(shp.shp(1))
        else:
            price = response.xpath('.//span[@class="muted"]/i/text()').extract_first()
            # p = re.search('(about $\d+ total)',price)
            # total_price = float(p.p(1))

        print(artist)
        print(year)
        print(currency)
        print(price)

        # item = PriceDiscogsItem()
        # item['']
