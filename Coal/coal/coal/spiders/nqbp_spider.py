import scrapy
from coal.nqbp_items import CoalItem, CoalItemLoader, end_of_prev_mth


class NqbpSpider(scrapy.Spider):
    name = 'nqbp'
    start_urls = [
        'https://nqbp.com.au/trade/throughputs'
    ]

    def parse(self, response):
        ports = response.xpath('//li[contains(@class, "content-tabs__item")]')
        fiscal_years = ports[0].xpath('.//thead/tr/th/text()').extract()
        if end_of_prev_mth.month >= 7:
            current_fy = str(end_of_prev_mth.year) + '-' + str(end_of_prev_mth.year+1)[2:]
        else:
            current_fy = str(end_of_prev_mth.year-1) + '-' + str(end_of_prev_mth.year)[2:]
        if current_fy in fiscal_years:
            for port in ports:
                port_name = port.xpath('.//span[@class="content-tab__header-label"]/text()').extract_first()
                if port_name == 'Abbot Point':
                    l = CoalItemLoader(item=CoalItem(), selector=port)
                    l.add_value('port', port_name)
                    l.add_value('date', end_of_prev_mth.strftime('%d/%m/%Y'))
                    l.add_xpath('coal', './/tbody//td/text()')
                    l.add_value('state', 'QLD')
                    yield l.load_item()

                elif port_name == 'Hay Point':
                    # this tab has coal data for 2 terminals one on top of another
                    terminals = port.xpath('.//h3/text()').extract()
                    for terminal_num, terminal in enumerate(terminals):
                        l = CoalItemLoader(item=CoalItem(), selector=port)
                        l.add_value('port', terminal)
                        l.add_value('date', end_of_prev_mth.strftime('%d/%m/%Y'))
                        l.add_xpath('coal', './/h3[' + str(terminal_num+1) + ']/following::td/text()')
                        l.add_value('state', 'QLD')
                        yield l.load_item()