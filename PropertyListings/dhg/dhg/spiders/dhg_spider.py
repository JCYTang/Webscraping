import scrapy
import logging
from dhg.items import DHGProperty
from dhg.items import DHGPropertyLoader
from datetime import datetime


class DhgSpider(scrapy.Spider):
    name = "dhg"
    start_urls = [
        'https://www.domain.com.au/real-estate/buy/nsw/',
        'https://www.domain.com.au/real-estate/buy/vic/',
        'https://www.domain.com.au/real-estate/buy/qld/',
        'https://www.domain.com.au/real-estate/buy/wa/',
        'https://www.domain.com.au/real-estate/buy/sa/',
        'https://www.domain.com.au/real-estate/buy/tas/',
        'https://www.domain.com.au/real-estate/buy/act/',
        'https://www.domain.com.au/real-estate/buy/nt/'
    ]

    def __init__(self, *args, **kwargs):

        # set logging settings for scrapy
        # scrapy uses a python logging object

        self.date = datetime.today().strftime('%Y-%m-%d')
        self.log_file = 'dhg_log.txt'
        logger = logging.getLogger('scrapy')
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.FileHandler(self.log_file, mode='w'))
        super().__init__(*args, **kwargs)

    def parse(self, response):
        suburbs = response.xpath('//ul[@class="suburbs-list"]/li/a/@href').extract()
        for suburb in suburbs:
            yield response.follow(suburb, self.parse_suburb)

    def parse_suburb(self, response):
        listings = response.xpath('//div/ul/li[contains(@data-testid, "listing")]')
        for listing in listings:

            # don't scrape listing if it is an ad or project
            html_link = listing.xpath('.//@href').extract_first()
            ad_class = listing.xpath('.//div/@class').extract_first()
            if html_link is not None and 'project' not in ad_class:

                # use the custom item loader in items.py which specifies the input and output processors to use
                l = DHGPropertyLoader(item=DHGProperty(), selector=listing)
                l.add_value('date', self.date)
                l.add_xpath('url', '(.//@href)[1]')
                l.add_xpath('ad_type', '(.//div/@class)[1]')
                l.add_xpath('ad_type', '(.//div[contains(@class, "brand")]/@class)[1]')
                l.add_xpath('address_line_1', '(.//span[@class="address-line1"]/text()[1])')
                l.add_xpath('suburb', './/span[@itemprop="addressLocality"]/text()')
                l.add_xpath('state', './/span[@itemprop="addressRegion"]/text()')
                l.add_xpath('postcode', './/span[@itemprop="postalCode"]/text()')
                yield l.load_item()

        # only follow next page if number of listings are greater than 0
        if len(listings) > 0:
            next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_suburb)