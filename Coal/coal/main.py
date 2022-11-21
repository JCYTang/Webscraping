from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from coal.spiders.nqbp_spider import NqbpSpider
from coal.spiders.gladstone_spider import GladstoneSpider
from coal.spiders.newcastle_spider import NewcastleSpider
from coal.nqbp_items import end_of_prev_mth
from coal.pipelines import coal_csv, items
import pandas as pd
import win32com.client


def send_email(nqbp_scraped, gladstone_scraped):
    if nqbp_scraped or gladstone_scraped:
        website = ''
        if nqbp_scraped:
            website = website + '<a href=' + NqbpSpider.start_urls[0] +'>' + NqbpSpider.start_urls[0] + '</a><br>'
        if gladstone_scraped:
            website = website + '<a href=' + GladstoneSpider.start_urls[0] +'>' + GladstoneSpider.start_urls[0] + '</a><br>'
        df = pd.DataFrame(items, columns=['date', 'port', 'coal'])
        df['coal'] = df['coal'].astype(int).map("{:,}".format)

        Outlook = win32com.client.Dispatch("Outlook.Application")
        objMail = Outlook.CreateItem(0)
        objMail.To = 'tim.wood@iml.com.au; liam.cummins@iml.com.au; john.parathyras@iml.com.au'
        objMail.CC = 'jeremy.tang@iml.com.au'
        objMail.Subject = 'Coal Scrape ' + end_of_prev_mth.strftime('%b %Y')
        html = 'Dashboard Link: <br><a href=http://aud0100ck4:8082>http://aud0100ck4:8082</a><br><br>' + \
            'Coal ' + end_of_prev_mth.strftime('%b %Y') + ' throughput numbers are available at: <br>' + \
            website + '<br>' + 'Location of updated file:<br>' + \
            '<a href=W:\\RESEARCH\\Personal%20Folders\\Jeremy\\WebScraping\\Coal\\coal.csv>' + coal_csv + \
            '</a><br><br>' + df[df['date'] == end_of_prev_mth.strftime('%d/%m/%Y')].to_html(index=False)
        objMail.HTMLBody = html
        # objMail.Send()
        objMail.Display()


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    Nqbp_Crawler = process.create_crawler(NqbpSpider)
    Gladstone_Crawler = process.create_crawler(GladstoneSpider)
    Newcastle_Crawler = process.create_crawler(NewcastleSpider)
    process.crawl(Nqbp_Crawler)
    process.crawl(Gladstone_Crawler)
    process.crawl(Newcastle_Crawler)
    process.start() # the script will block here until the crawling is finished
    Nqbp_stats = Nqbp_Crawler.stats.get_stats()
    Gladstone_stats = Gladstone_Crawler.stats.get_stats()
    nqbp_scraped = 'item_scraped_count' in Nqbp_stats.keys()
    gladstone_scraped = 'item_scraped_count' in Gladstone_stats.keys()
    send_email(nqbp_scraped, gladstone_scraped)