from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from restaurantbot.items import RestaurantItem


class NYCListingSpider(CrawlSpider):
    name = 'nyc_listing_spider'

    # Use zagat.com to retrieve the main listings
    # (off https://www.zagat.com/c/new-york-city-ny/all-restaurants)
    allowed_domains = ['zagat.com']
    start_urls = ['https://www.zagat.com/c/new-york-city-ny/all-restaurants']
    DOWNLOAD_DELAY = 0.40

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/c/new-york-city-ny/[\w\d\-]+-restaurants')), follow=True),

        Rule(SgmlLinkExtractor(allow=(r'/r/[\w\d\-]+-new-york[\w\d\-]+')), callback='parse_item'),
    )

    # Elements of the address are divided
    # (inspect elements https://www.zagat.com/r/afghan-kebab-house-new-york2)
    location_xpaths = ['//*[@id="content"]/div[2]/div[2]/div[2]/p/strong/text()',
                       '//*[@id="content"]/div[2]/div[2]/div[2]/p/span[1]/text()',
                       '//*[@id="content"]/div[2]/div[2]/div[2]/p/span[2]/text()',
                       '//*[@id="content"]/div[2]/div[2]/div[2]/p/span[3]/text()']

    def parse_item(self, response):
        s = Selector(response)

        item = RestaurantItem()
        item['name'] = s.select('//*[@id="main-content-title"]/text()').extract()[0]
        item['cuisine'] = s.select('//*[@id="content"]/div[2]/span/a[1]/text()').extract()[0]

        location_items = [s.select(path).extract()[0] for path in self.location_xpaths]
        item['location'] = ", ".join(location_items)

        #item['hours'] = s.select().extract()
        item['menu_href'] = response.url + "/menu"
        return item
