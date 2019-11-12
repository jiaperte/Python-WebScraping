
#!/usr/bin/env python3


# import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
import xlwt
import sys
import requests
import json


# specify the url
urlPrefix = 'http://www.sydneytoday.com/'

sheetName = {
    "装修建筑": "decoration_building",
    "Gyprock 间隔": "cyprock",
    "屋顶补漏": "roof_trap",
    "水管木工": "plumber",
    "厨房卫浴": "furniture",
    "电工维修": "electrician",
    "空调冷气": "conditioning",
    "修理安装": "repair-and-installation",
    "凉棚车库": "pergola",
    "泳池维护": "swimming",
    "门窗玻璃": "door_glass",
    "花园园艺": "weeding",
    "地板地毯": "flooring_carpet",
    "油漆": "paint",
    "窗帘布艺": "life",
    "除虫白蚁": "worming",
    "房产物业": "broker",
    "灯具": "lamps",
    "室内设计": "interior_design",
    "绿色能源": "green-energy"}


if len(sys.argv) < 2:
    print("Please input content to scrap")
    exit(1)
else:
    urlPrefix += str(sys.argv[1])


servicexls = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = servicexls.add_sheet(str(sys.argv[1]), cell_overwrite_ok=True)


#rows = []
#rows.append(['Service Name', 'Contract', 'Phone', 'Company Name'])
sheet.write(0, 0, "Service Name")
sheet.write(0, 1, "Contract")
sheet.write(0, 2, "Phone")
sheet.write(0, 3, "Company Name")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

i = 2
rowNum = 1
phoneSet = set()
while True:
    urlOfPage = urlPrefix + "?page=" + str(i)
    response = requests.get(urlOfPage)
    dictResponse = response.json()
    if dictResponse.get("status") == 200:
        rows = dictResponse.get("data").get("rows")

        for item in rows:
            if item["mobile"] in phoneSet:
                continue
            else:
                sheet.write(rowNum, 0, item["title"])
                sheet.write(rowNum, 1, item["contact"])
                sheet.write(rowNum, 2, item["mobile"])
                sheet.write(rowNum, 3, item["companyname"])
                phoneSet.add(item["mobile"])
            rowNum += 1

        hasMorePage = dictResponse.get("data").get("nopages")
        if hasMorePage == 0:
            print("total items:" + str(rowNum))
            break
        else:
            i += 1
    else:
        break

print("pages:" + str(i))

for i in sheetName:
    if str(sys.argv[1]) == sheetName[i]:
        file = i

fileName = "/Users/jiapeter/python/sydney_today//sydneytoday_" + \
    file + ".xls"
servicexls.save(fileName)
