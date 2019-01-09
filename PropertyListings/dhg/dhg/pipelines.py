import turbodbc
import pandas as pd
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
import pprint

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SQLPipeline(object):

    def __init__(self):

        datestamp = datetime.today().strftime('%Y%m%d')
        self.csvfile = 'dhg_' + datestamp + '.csv'

    def process_item(self, item, spider):

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.insert_into_database()
        self.send_email(spider)

    def insert_into_database(self):
        '''open csv file with saved data
           insert into dataframe and remove duplicates
           insert from dataframe to database'''

        server = 'imlvs03\sql2005'
        database = 'DW_Development'
        driver = '{ODBC Driver 13 for SQL Server}'
        user = 'DWUser'
        password = 'gI7T@JD0rEdsF'
        conn = turbodbc.connect(uid=user, pwd=password, driver=driver, server=server, database=database)
        cur = conn.cursor()
        df = pd.read_csv(self.csvfile, na_filter=False)
        df.drop_duplicates(subset=['url'], inplace=True)
        sql = 'INSERT PropertyListings (date, url, ad_type, address_line_1, suburb, state, postcode) VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.executemany(sql, df.values.tolist())
        conn.commit()
        conn.close()

    def send_email(self, spider):

        # django settings for email
        host = 'smtp.gmail.com'
        port = 587
        username = 'JTang.IML@gmail.com'
        password = 'IMLpassword'
        if not settings.configured:
            settings.configure(EMAIL_HOST=host, EMAIL_PORT=port, EMAIL_HOST_USER=username, EMAIL_HOST_PASSWORD=password)

        toaddr = ['jeremy.tang@iml.com.au']
        fromaddr = 'JTang.IML@gmail.com'
        subject = 'Domain Scrape'
        body = pprint.pformat(spider.crawler.stats.get_stats())
        email = EmailMessage(subject=subject, from_email=fromaddr, to=toaddr, body=body)
        email.attach_file(spider.log_file)
        email.send()

