import scrapy
from coal.gladstone_items import CoalItem, CoalItemLoader
from datetime import datetime
from coal.nqbp_items import end_of_prev_mth


class GladstoneSpider(scrapy.Spider):
    name = 'gladstone'
    start_urls = [
        'http://content3.gpcl.com.au/viewcontent/CargoComparisonsSelection/CargoOriginDestination.aspx' +
        '?View=C&Durat=M&Key=' + end_of_prev_mth.strftime('%Y%m')
    ]

    def parse(self, response):
        heading = response.xpath('//h1/text()').extract()
        if any(datetime.strftime(end_of_prev_mth, '%B') in h for h in heading):
                l = CoalItemLoader(item=CoalItem(), selector=response)
                l.add_value('port', 'Gladstone')
                l.add_value('date', end_of_prev_mth.strftime('%d/%m/%Y'))
                l.add_xpath('coal', '//td//text()')
                l.add_value('state', 'QLD')
                yield l.load_item()

