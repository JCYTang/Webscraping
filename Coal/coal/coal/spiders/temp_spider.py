import scrapy
from coal.gladstone_items import CoalItem, CoalItemLoader
from datetime import datetime, timedelta
from dateutil import rrule
import calendar
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TempSpider(scrapy.Spider):
    name = 'temp'
    start = datetime(2016,8,28)
    end = datetime(2020,2,28)
    start_urls=[]
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        mth_end = dt.replace(day=1) - timedelta(days=1)
        start_urls.append('http://content1.gpcl.com.au/viewcontent/CargoComparisonsSelection/CargoOriginDestination.aspx' +
        '?View=C&Durat=M&Key=' + dt.strftime('%Y%m'))


    def parse(self, response):
        # heading = response.xpath('//h1/text()').extract()
        month = int(response.url[-2:])
        year = int(response.url[-6:-2])
        day = calendar.monthrange(year, month)[1]
        l = CoalItemLoader(item=CoalItem(), selector=response)
        l.add_value('port', 'Gladstone')
        l.add_value('date', datetime(year, month, day).strftime('%d/%m/%Y'))
        l.add_xpath('coal', '//td//text()')
        yield l.load_item()

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    Nqbp_Crawler = process.create_crawler(TempSpider)
    process.crawl(Nqbp_Crawler)
    process.start() # the script will block here until the crawling is finished