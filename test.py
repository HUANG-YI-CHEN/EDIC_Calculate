# encoding: utf-8
"""
This is a program for transferring function and drawing the values, which
transferred by function, SVG.
"""
import csv
import re

"""
Define Value : Voltage(V), Current(I)
"""
# rowdata = ['element1\t,0238.94', 'element2\t,2.3904', 'element3\t,0139847', 'element5']
rowdata = []
voltage = []
current = []
"""
Read file data
"""

with open('test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
    for row in spamreader:
        row_split = re.split(',', ''.join(row))
        rowdata.append(row_split)
        print(row_split)
    print(rowdata)
    # print(voltage)
    
# for i,x in enumerate(rowdata):
#     if ',' in x:
#         print(x[:x.index(',')])
#         print(i)
