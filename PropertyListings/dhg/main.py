from scrapy import cmdline
from datetime import datetime

# run the scrapy spider
# name must match property in the quotes_spider class
# save scraped data in a csv file

datestamp = datetime.today().strftime('%Y%m%d')
cmdline.execute(("scrapy crawl dhg -o dhg_" + datestamp + ".csv").split())