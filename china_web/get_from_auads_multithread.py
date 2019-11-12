
#!/usr/bin/env python3

from bs4 import BeautifulSoup
from multiprocessing import Pool
import urllib.request
import time
import xlwt
import threading
from queue import Queue
from lxml import etree
import requests


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r)
                     for i in range(2, len(encodedString), 2)])
    return email


auadsxls = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = auadsxls.add_sheet('auads', cell_overwrite_ok=True)


rows = []
# rows.append(['Service Name', 'Phone', 'Email'])


# def getDetailOfAd(urlOfAd):
#     serviceName = ""
#     phone = ""
#     email = ""

#     requst = urllib.request.Request(
#         url=urlOfAd, headers=headers)
#     page = urllib.request.urlopen(requst)

#     # parse the html using beautiful soup and store in variable 'soup'
#     soup = BeautifulSoup(page, 'html.parser')
#     name = soup.find('span', itemprop='name')
#     serviceName = name.text

#     telephonelable = soup.find('a', itemprop='telephone')
#     if(telephonelable):
#         if hasattr(telephonelable, 'text'):
#             phone = telephonelable.text

#     emailspan = soup.find('span', itemprop='email')
#     if(emailspan):
#         if hasattr(emailspan, 'span'):
#             email = cfDecodeEmail(emailspan.span['data-cfemail'])

#     if len(serviceName) > 0 and (len(email) > 0 or len(phone) > 0):
#         rows.append([serviceName, phone, email])

#     return rows


saveResult = []
saveResult.append(['Service Name', 'Phone', 'Email'])

# for aa in results:
#     for bb in aa:
#         print(bb)
#         saveResult.append(bb)

# for i, l in enumerate(saveResult):
#     for j, col in enumerate(l):
#         sheet.write(i, j, col)

# auadsxls.save('/Users/jiapeter/python/auads.xls')


class Crawl_thread(threading.Thread):

    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)  # 需要对父类的构造函数进行初始化
        self.thread_id = thread_id
        self.queue = queue  # 任务队列

    def run(self):

        #print('启动线程：', self.thread_id)
        self.crawl_spider()
        #print('退出了该线程：', self.thread_id)

    def crawl_spider(self):
        while True:
            if self.queue.empty():  # 如果队列为空，则跳出
                break
            else:
                page = self.queue.get()
                #print('当前工作的线程为：', self.thread_id, " 正在采集：", page)

                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
                    requst = urllib.request.Request(
                        url=page, headers=headers)
                    page = urllib.request.urlopen(requst)
                    soup = BeautifulSoup(page, 'html.parser')
                    # print(soup)
                    data_queue.put(soup)  # 将采集的结果放入data_queue中
                except Exception as e:
                    print('采集线程错误', e)


class Parser_thread(threading.Thread):

    def __init__(self, thread_id, queue, sheet, rowsNum):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
        self.sheet = sheet
        self.rowsNum = rowsNum

    def run(self):
        #print('启动线程：', self.thread_id)
        while not flag:
            try:
                item = self.queue.get(False)  # get参数为false时队列为空，会抛出异常
                if not item:
                    pass
                self.parse_data(item)
                self.queue.task_done()  # 每当发出一次get操作，就会提示是否堵塞
            except Exception as e:
                pass
        #print('退出了该线程：', self.thread_id)

    def parse_data(self, item):
        '''
        解析网页内容的函数
        : param item:
        : return:
        '''
        try:
            html = etree.HTML(str(item))
            serviceName = html.xpath(
                '//span[@itemprop="name"]/text()')  # 匹配所有段子内容
            try:
                # 糗事图片
                telephone = html.xpath('//a[@itemprop="telephone"]/text()')
                address = html.xpath('//span[@itemprop="address"]/text()')
                encryptedEmail = html.xpath('//span/attribute::data-cfemail')
                realEmail = ""
                email = ""
                if not encryptedEmail:
                    realEmail = ""
                else:
                    for ch in encryptedEmail:
                        email += ch
                    realEmail = cfDecodeEmail(email)
                result = []
                if not telephone and not realEmail:
                    pass
                else:
                    result = serviceName + telephone
                    result.append(realEmail)
                    result += address
                if not result:
                    pass
                else:
                    print(result)
                    #     for i, l in enumerate(result):
                    #         self.sheet.write(0, i, l)
                    #         self.rowsNum += 1

            except Exception as e:
                print('parse 2: ', e)

        except Exception as e:
            print('parse 1: ', e)


data_queue = Queue()  # 存放解析数据的queue
flag = False


def main():
    output = open('qiushi.json', 'a', encoding='utf-8')  # 将结果保存到一个json文件中
    auadsxls = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = auadsxls.add_sheet('auads', cell_overwrite_ok=True)
    pageQueue = Queue(1800)  # 任务队列，存放网页的队列
    f = open("/Users/jiapeter/python/urllists_90.txt", "r")
    txt = f.readlines()
    for page in txt:
        pageQueue.put(page)  # 构造任务队列
    f.close
    rowsNum = 0
    # 初始化采集线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']  # 总共构造3个爬虫线程
    for thread_id in crawl_name_list:
        thread = Crawl_thread(thread_id, pageQueue)  # 启动爬虫线程
        thread.start()  # 启动线程
        crawl_threads.append(thread)
    # 初始化解析线程
    parse_thread = []
    parser_name_list = ['parse_1', 'parse_2', 'parse_3']
    for thread_id in parser_name_list:
        thread = Parser_thread(thread_id, data_queue, sheet, rowsNum)
        thread.start()  # 启动线程
        parse_thread.append(thread)

    # 等待队列情况，先进行网页的抓取
    while not pageQueue.empty():  # 判断是否为空
        pass  # 不为空，则继续阻塞

    # 等待所有线程结束
    for t in crawl_threads:
        t.join()
    # 等待队列情况，对采集的页面队列中的页面进行解析，等待所有页面解析完成
    while not data_queue.empty():
        pass
    # 通知线程退出
    global flag
    flag = True
    for t in parse_thread:
        t.join()  # 等待所有线程执行到此处再继续往下执行

    print('退出主线程')
    output.close()
    # auadsxls.save('/Users/jiapeter/python/auads.xls')


if __name__ == '__main__':
    main()
