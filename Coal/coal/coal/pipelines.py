from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
import pandas as pd
import os

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

fields_to_export = ['date', 'port', 'coal', 'state']
coal_csv = os.path.dirname(os.getcwd()) + '\\coal.csv'
items = []


class CoalPipeline(object):

    def open_spider(self, spider):
        self.file = open(coal_csv, 'ab')
        self.exporter = CsvItemExporter(file=self.file, include_headers_line=False)
        self.exporter.fields_to_export = fields_to_export
        self.df = pd.read_csv(coal_csv)

    def close_spider(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        if item['coal'] != '':
            if self.df[(self.df['date'] == item['date']) & (self.df['port'] == item['port'])].empty:
                self.exporter.start_exporting()
                self.exporter.export_item(item)
                items.append(item)
                return item

        raise DropItem
