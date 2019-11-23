# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import psycopg2


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['cellphone'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['cellphone'])
            return item


class SeekingservicePipeline(object):
    def open_spider(self, spider):
        hostname = '3.106.116.122'
        username = 'postgres'
        password = '123456'  # your password
        database = 'seekingservice'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if item['cellphone'] is "":
            raise DropItem(
                "Duplicate item found: %s because no cellphone" % item)
        else:
            try:
                self.cur.execute("insert into seekingservice(company_name, owner, cellphone, address, category) values(%s,%s,%s,%s,%s)",
                                 (item['company_name'], item['owner'], item['cellphone'], item['address'], item['category']))
                self.connection.commit()
            except Exception as ex:
                print("Error: rolllllllllllback  " + str(ex))
                self.cur.execute("rollback")
            return item
