# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from seekingservice.items import SeekingserviceItem
import json


class SeekingserviceSpiderSpider(scrapy.Spider):
    name = 'seekingservice_spider'
    allowed_domains = ['serviceseeking.com.au']
    seekservice_urls = 'http://serviceseeking.com.au'
    start_urls = seekservice_urls + '/plumbers/nsw/'
    # start_urls = []

    # def __init__(self, category=None, area=None, *args, **kwargs):
    #     super(SeekingserviceSpiderSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = [
    #         'http://serviceseeking.com.au/%s/nsw/%s' % (category, area)]

    def start_requests(self):
        yield Request(url=self.start_urls, callback=self.parse_area)

    def parse_area(self, response):
        cols = response.xpath(
            '//div[@class="bg"]//div[1]//div[1]')
        areas = cols.css(
            'a::attr(href)').getall()
        for area in areas:
            if area == '/plumbers/nsw/sydney' or area == '/plumbers/nsw/blacktown':
                continue
            else:
                area_url = self.seekservice_urls + area
                yield Request(url=area_url, callback=self.parse_urleverypage, meta={'area_url': area_url})

    def parse_urleverypage(self, response):
        nums = response.xpath(
            '//span[@class="matched-businesses-count"]//text()').get()
        pages = int(nums)//10
        rest = int(nums) % 10

        if rest == 0:
            pages = pages + 1
        else:
            pages = pages + 2

        for i in range(1, pages):
            page_url = response.meta['area_url'] + "?page=" + str(i)
            print(page_url)
            yield Request(url=page_url, callback=self.parse_basicinfo)

    def parse_basicinfo(self, response):
        for mbm in response.css('[class=mbd-card]'):
            mbdcard = mbm.css(
                'div.card.card-flat.card-spread-none.mt8.sm-mt16 > div.card-content.card-pad-md.visible-xs:nth-child(2)')

            if mbdcard.get() is None:
                # print('mbdcard is pro')
                mbdcard = mbm.css(
                    'div.card.card-flat.card-spread-none.mt8.sm-mt16.pro-business div.card-content.card-pad-md.visible-xs:nth-child(3)')

            url = mbdcard.css('a::attr(href)').get()
            # print(url)
            info = mbdcard.css(
                'div.mb20:nth-child(2) div.row div.mt10 div.col-xs-6.pr8:nth-child(1) > div:nth-child(1)::attr(data-react-props)').get()

            cellphone = ""
            if info is not None:
                de = json.loads(info)
                # print(de['business']['mobile_phone'])
                cellphone = de['business']['mobile_phone']

            suburl = self.seekservice_urls + url[1:]

            yield Request(url=suburl, callback=self.parse_moreinfo, meta={'cellphone': cellphone})

    def parse_moreinfo(self, response):
        item = SeekingserviceItem()
        bio = response.xpath(
            '//div[@class = "bio-text col-xs-12 col-sm-8 col-md-12"]')
        company_name = bio.xpath(
            '//div[@class="font-21 bold pb4 mt16 sm-mt0 text-copy-2"]//text()').get()
        # print(company_name)

        cellphone = ""
        if response.meta['cellphone'] is not "":
            cellphone = response.meta['cellphone']
        else:
            info = bio.xpath(
                '//div[@class="row"]/div[@class="col-xs-12 mt16"]/div[2]/@data-react-props').get()
            try:
                if info is not None:
                    js = json.loads(info)
                    cellphone = js['contactPhone']
            except Exception as ex:
                print(ex)
                return

        owner = bio.xpath(
            '//div[@class="row mt20"]/div[2]/div//text()').get()

        address = bio.xpath(
            '//div[@class="row"]/div[@class="col-xs-10"]/div//text()').get()

        item['company_name'] = company_name
        item['owner'] = owner
        item['cellphone'] = cellphone
        item['address'] = address

        yield item
