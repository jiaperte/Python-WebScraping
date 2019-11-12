
#!/usr/bin/env python3


# import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
import xlwt

servicexls = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = servicexls.add_sheet('51service', cell_overwrite_ok=True)


# specify the url
urlPrefix = 'http://www.51service.com.au/index.php?route=product/category&path=105_114'

rows = []
rows.append(['Service Name', 'Phone'])

# query the website and return the html to the variable 'page'
for i in range(1, 2):
    page = urllib.request.urlopen(urlPrefix + "&page=" + str(i))
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # print(soup.prettify())

    # find results within div
    itemsOfPerPage = soup.findAll('div', attrs={
        'class': 'product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12'})

    for result in itemsOfPerPage:
        #print(result.div.h4.p.a.text + " " + result.div.div.p.text)
        rows.append([result.div.h4.p.a.text, result.div.div.p.text])

# with open('51service.csv', 'w', newline='') as f_output:
#     csv_output = csv.writer(f_output)
#     csv_output.writerows(rows)

for i, l in enumerate(rows):
    for j, col in enumerate(l):
        # print(col)
        sheet.write(i, j, col)

servicexls.save('/Users/jiapeter/python/51service_test.xls')
