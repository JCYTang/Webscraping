# -*- coding: utf-8 -*-

# Scrapy settings for coal project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'coal'

SPIDER_MODULES = ['coal.spiders']
NEWSPIDER_MODULE = 'coal.spiders'

# FEED_FORMAT = 'csv'
# FEED_URI = 'coal.csv'
# FEED_EXPORT_FIELDS = ['date', 'port', 'coal']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'coal (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'coal.middlewares.CoalSpiderMiddleware': 543,
#    'scrapy_deltafetch.DeltaFetch': 100,
#     'scrapy_crawl_once.CrawlOnceMiddleware': 100,
# }
# DELTAFETCH_ENABLED = True

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'coal.middlewares.CoalDownloaderMiddleware': 543,
#     'scrapy_crawl_once.CrawlOnceMiddleware': 50,
# }
# CRAWL_ONCE_ENABLED = True

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
# #    'scrapy.extensions.telnet.TelnetConsole': None,
   'scrapy.extensions.statsmailer.StatsMailer': 500,
}
STATSMAILER_RCPTS = ['jeremy.tang@iml.com.au']
MAIL_FROM = 'JTang.IML@gmail.com'
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USER = 'JTang.IML@gmail.com'
MAIL_PASS = 'IMLpassword'
# MAIL_TLS = True
MAIL_SSL = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'coal.pipelines.CoalPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
