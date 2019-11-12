#!/usr/bin/env python3

from linkedin_scraper import Person, actions
from selenium import webdriver
from parsel import Selector
import sys
import xlwt
import xlrd

fileName = sys.argv[1]
# Give the location of the file
loc = ("/Users/jiapeter/python/linkdin/" + fileName)

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

filterSydney = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheetFiltered = filterSydney.add_sheet(
    'PM', cell_overwrite_ok=True)

driver = webdriver.Chrome()

email = "jiayong_2010@139.com"
password = "19870425"
# if email and password isnt given, it'll prompt in terminal
actions.login(driver, email, password)

rows = 0
for i in range(1, sheet.nrows):
    linkdinUrl = sheet.cell_value(i, 3)
    firstName = sheet.cell_value(i, 0)
    lastName = sheet.cell_value(i, 1)
    email = sheet.cell_value(i, 2)
    try:
        driver.get(linkdinUrl)
        driver.page_source
        sel = Selector(text=driver.page_source)
        location = sel.xpath(
            '// *[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()

        title = sel.xpath(
            '// *[starts-with(@class, "mt1 t-18 t-black t-normal")]/text()').extract_first()

        if "Sydney" in location and email:
            sheetFiltered.write(rows, 0, firstName + " " + lastName)
            sheetFiltered.write(rows, 1, email)
            sheetFiltered.write(rows, 2, title.strip())
            sheetFiltered.write(rows, 3, location.strip())
            sheetFiltered.write(rows, 4, linkdinUrl)
            rows += 1
    except Exception as ex:
        print("Now at:" + str(i))


# for i in range(0, 10):
#     sheetFiltered.write(rows, i, "absdd")
#     rows += 1


# sheetFiltered.write(0, 0, 1)
# sheetFiltered.write(0, 1, 2)
# sheetFiltered.write(1, 0, 3)
# sheetFiltered.write(1, 1, 4)

filterSydney.save(
    '/Users/jiapeter/python/linkdin/' + 'sydney/' + fileName.strip('.xlsx') + ".xls")
