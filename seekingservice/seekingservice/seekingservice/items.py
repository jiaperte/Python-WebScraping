# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeekingserviceItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    owner = scrapy.Field()
    cellphone = scrapy.Field()
    address = scrapy.Field()
