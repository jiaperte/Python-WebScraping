#!/usr/bin/env python3

import xlwt

auadsxls = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = auadsxls.add_sheet('auads_nsw', cell_overwrite_ok=True)
i = 0
for line in open("/Users/jiapeter/python/auads_nsw.txt", "r"):
    j = 0
    for item in line.split('\', \''):
        print(item)
        sheet.write(i, j, item)
        j += 1
    i += 1

# for i, l in enumerate(str1):
#     for j, col in enumerate(l):
#         print(col)
# sheet.write(i, j, col)

# print(str1)


auadsxls.save('/Users/jiapeter/python/auads_nsw.xls')
