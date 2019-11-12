#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
import xlrd
import urllib.request

fileName = sys.argv[1]
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

# Give the location of the file
loc = ("/Users/jiapeter/python/linkdin/" + fileName)

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for i in range(1, sheet.nrows):
    linkdinUrl = sheet.cell_value(i, 3)
    print(linkdinUrl)
    requst = urllib.request.Request(
        url=linkdinUrl, headers=headers)

    try:
        page = urllib.request.urlopen(requst)
    except Exception as ex:
        print(str(ex))
        continue

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    address = soup.findAll('li', attrs={
        'class': 't-16 t-black t-normal inline-block'})
    print(address)

# print(sheet.ncols)
