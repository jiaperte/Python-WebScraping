# -*- coding: utf-8 -*-
#import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http.request import Request
from seekingservice.items import SeekingserviceItem
import json


class SeekingserviceSpiderSpider(RedisCrawlSpider):
    name = 'seekingservice_spider'
    allowed_domains = ['serviceseeking.com.au']
    seekservice_urls = 'http://serviceseeking.com.au'
    start_urls = seekservice_urls + '/builders/nsw/'
    category = ""

    cat_dict = {
        # 'Builders': ('duplex-builders', 'new-home-builders', 'pool-builders'),
        'Air Conditioning': ('car-air-conditioning', 'ducted-air-conditioning', 'air-conditioning-repair', 'air-conditioning-technicians', 'air-conditioner-installation'),
        'Architects': ('architectural-drafting', 'interior-architecture', 'landscape-architecture'),
        'Balustrades': ('balustrading'),
        'Bathroom Renovations': ('bathroom-design', 'bathroom-renovators', 'bathroom-tiling', 'bathroom-waterproofing'),
        'Bricklayer': ('bricklayers'),
        'Building Designers': ('building-designers'),
        'Building Inspections': ('building-inspection'),
        'Carpenter': ('carpenters'),
        'Carports': ('carport'),
        'Cladding': ('cladding', 'stone-cladding', 'timber-cladding'),
        'Concreting': ('concreters', 'concrete-slab', 'concrete-retaining-walls', 'concrete-resurfacing', 'concrete-repair', 'concrete-pumping', 'concrete-pavers', 'concrete-formwork', 'concrete-edging', 'concrete-driveway', 'concrete-cutting', 'concrete-cleaning', 'polished-concrete-floors', 'exposed-aggregate-concret'),
        'Decking': ('composite-decking', 'decking', 'timber-decking'),
        'Demolition': ('demolition-experts'),
        'Doors': ('pet-doors'),
        'Drafting': ('architectural-drafting', 'draftsman'),
        'Electricians': ('electricians', 'local-electricians'),
        'Excavation': ('excavation'),
        'Fencing': ('aluminium-fencing', 'bamboo-fencing', 'brush-fencing', 'colorbond-fencing', 'electric-fencing', 'pool-fencing', 'pvc-fencing', 'security-fencing', 'steel-fencing', 'timber-fencing', 'wire-fencing'),
        'Garages': ('garage-door-repair', 'garage-roller-door'),
        'Gardeners': ('gardeners', 'landscaping-and-gardening'),
        'Gas Fitters': ('ducted-gas-heating', 'gas-cooktop-installation', 'gas-fittings'),
        'Gutter Cleaning': ('gutter-cleaning'),
        'Guttering': ('guttering'),
        'Handyman': ('handymen'),
        'Interior Decorators': ('interior-decoration', 'interior-painting'),
        'Interior Designers': ('interior-design'),
        # 'Kitchens': ('flat-pack-kitchens', 'kitchen-installers', 'kitchen-renovations', 'kitchen-splashbacks', 'kitchen-tiling', 'painting-kitchen-cupboards')}
        'Landscapers': ('hard-landscaping', 'landscape-architecture', 'landscape-construction', 'landscape-solutions', 'landscaping-and-gardening', 'structural-landscaping'),
        'Painters': ('commercial-painters', 'painters'),
        'Pavers': ('concrete-pavers', 'paving', 'brick-paving', 'driveway-paving', 'outdoor-paving', 'paving-cleaning', 'pool-paving', 'sandstone-paving'),
        'Plastering': ('plaster-cornice', 'plaster-repair', 'plasterers'),
        'Pool Fencing': ('pool-fencing'),
        'Render': ('render-house'),
        'Rendering': ('cement-rendering'),
        'Retaining Walls': ('retaining-wall-experts', 'retaining-wall-construction', 'concrete-retaining-walls'),
        'Roof Repairs': ('roof-repairs'),
        'Roofing': ('colorbond-roofing'),
        'Shopfitters': ('shop-fitters', 'shop-fittings'),
        'Shower Screens': ('shower-screens'),
        'Solar Power': ('solar-panel-installation'),
        'Tiler': ('roof-tiler', 'roof-tiling', 'tilers', 'tile-resurfacing', 'tile-removal'),
        'Timber Flooring': ('timber-flooring'),
        'Wardrobes': ('walk-in-wardrobe', 'built-in-wardrobes'),
        'Waterproofing': ('waterproofing', 'bathroom-waterproofing')}

    def start_requests(self):
        cat_dict = self.cat_dict
        for cag in cat_dict:
            self.category = cag
            # print(self.category)
            url = ""
            if type(cat_dict[cag]) is str:
                url = self.seekservice_urls + "/" + cat_dict[cag] + "/nsw/"
                # print(url)
                yield Request(url=url, callback=self.parse_area)
            else:
                for subcat in cat_dict[cag]:
                    url = self.seekservice_urls + "/" + subcat + "/nsw/"
                    yield Request(url=url, callback=self.parse_area)
                    # print(url)

    def parse_area(self, response):
        cols = response.xpath(
            '//div[@class="bg"]//div[1]//div[1]')
        areas = cols.css(
            'a::attr(href)').getall()
        for area in areas:
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
            # print(page_url)
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
            info = mbdcard.css(
                'div.mb20:nth-child(2) div.row div.mt10 div.col-xs-6.pr8:nth-child(1) > div:nth-child(1)::attr(data-react-props)').get()

            cellphone = ""
            if info is not None:
                de = json.loads(info)
                # print(de['business']['mobile_phone'])
                cellphone = de['business']['mobile_phone']

            suburl = self.seekservice_urls + url
            # print(suburl)

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
        item['category'] = self.category

        # print(item['company_name'])
        # print(item['owner'])
        # print(item['cellphone'])
        # print(item['address'])
        # print(item['category'])

        yield item
