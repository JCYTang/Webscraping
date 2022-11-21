import scrapy
from coal.newcastle_items import CoalItem, CoalItemLoader
from coal.newcastle_items import end_of_prev_mth
import tabula


class NewcastleSpider(scrapy.Spider):
    name = 'newcastle'
    start_urls = [
        'https://www.portofnewcastle.com.au/about-our-port/'
    ]

    def parse(self, response):
        urls = response.xpath('//ul//li//a/@href[contains(., "uploads")]').extract()
        for url in urls:
            if end_of_prev_mth.strftime('%Y%m') in url:
                tables = tabula.read_pdf(url, pages=1)
                for table in tables[:-1]:
                    if 'Coal' in table.iloc[:, 0].to_list():
                        coal = table[table.iloc[:,0] == 'Coal'].iloc[0,1]
                        coal = str(coal).replace(',', '').strip()
                        l = CoalItemLoader(item=CoalItem())
                        l.add_value('port', 'Port of Newcastle')
                        l.add_value('date', end_of_prev_mth.strftime('%d/%m/%Y'))
                        l.add_value('coal', coal)
                        l.add_value('state', 'NSW')
                        yield l.load_item()


