#!/usr/bin/env python3

from linkedin_scraper import Person, actions
from selenium import webdriver
from parsel import Selector


driver = webdriver.Chrome()

email = "jiayong_2010@139.com"
password = "19870425"
# if email and password isnt given, it'll prompt in terminal
actions.login(driver, email, password)


driver.get("https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22au%3A4910%22%5D&keywords=it%20recruiter&origin=FACETED_SEARCH")
driver.page_source
sel = Selector(text=driver.page_source)
location = sel.xpath(
    '// *[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()

title = sel.xpath(
    '// *[starts-with(@class, "mt1 t-18 t-black t-normal")]/text()').extract_first()
