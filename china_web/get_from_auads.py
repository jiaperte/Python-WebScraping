
#!/usr/bin/env python3


# import libraries
from bs4 import BeautifulSoup
from multiprocessing import Pool
import urllib.request
import time
import xlwt
import requests


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r)
                     for i in range(2, len(encodedString), 2)])
    return email


auadsxls = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = auadsxls.add_sheet('auads', cell_overwrite_ok=True)

# specify the url
urlPrefix = 'https://auads.com.au/category/building/page/'
urlSuffix = "?lat=-33.876145&long=151.207652"
urllist = []

for i in range(1, 177):
    urlstr = urlPrefix + str(i) + urlSuffix
    urllist.append(urlstr)

rows = []
#rows.append(['Service Name', 'Phone', 'Email'])

# query the website and return the html to the variable 'page'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

itemurllist = []


def getUrlOfAd(urlsOfPage):

    requst = urllib.request.Request(
        url=urlsOfPage, headers=headers)

    try:
        page = urllib.request.urlopen(requst)
    except Exception as ex:
        print(str(ex))

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # print(soup.prettify())

    # find results within div
    itemsOfPerPage = soup.findAll('div', attrs={
        'class': 'col-md-12 col-xs-12 listed-header'})

    for result in itemsOfPerPage:
        # print(result.div.h4.p.a.text + " " + result.div.div.p.text)
        # rows.append([result.div.h4.p.a.text, result.div.div.p.text])
        # print(result.h4.a['href'])
        itemurllist.append(result.h4.a['href'])
    # return itemurllist


def getDetailOfAd(urlOfAd):
    serviceName = ""
    phone = ""
    email = ""

    requst = urllib.request.Request(
        url=urlOfAd, headers=headers)
    page = urllib.request.urlopen(requst)

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.find('span', itemprop='name')
    serviceName = name.text

    telephonelable = soup.find('a', itemprop='telephone')
    if(telephonelable):
        if hasattr(telephonelable, 'text'):
            phone = telephonelable.text

    emailspan = soup.find('span', itemprop='email')
    if(emailspan):
        if hasattr(emailspan, 'span'):
            email = cfDecodeEmail(emailspan.span['data-cfemail'])

    if len(serviceName) > 0 and (len(email) > 0 or len(phone) > 0):
        rows.append([serviceName, phone, email])

    return rows


for urlitem in urllist:
    getUrlOfAd(urlitem)

# print("finish get every url: " + str(len(itemurllist)))

# f = open("/Users/jiapeter/python/urllists.txt", "w+")
# for items in itemurllist:
#     f.writelines(items + "\n")
# f.close

# print('Scraping Start...')
# start_time = time.time()
# pool = Pool(2)
# results = pool.map(getDetailOfAd, itemurllist)
# end_time = time.time()
# print('Scraping finish...')
# print('lasts:', end_time-start_time)

# pool.close()
# pool.join()

# print("finish scrap, save start...")
# saveResult = []
# saveResult.append(['Service Name', 'Phone', 'Email'])

# for aa in results:
#     for bb in aa:
#         print(bb)
#         saveResult.append(bb)

# for i, l in enumerate(saveResult):
#     for j, col in enumerate(l):
#         sheet.write(i, j, col)

# auadsxls.save('/Users/jiapeter/python/auads.xls')
