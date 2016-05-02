# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 00:31:51 2014

@author: intel
"""

from scipy import random as rd
from xlrd import open_workbook as ow
from xlwt import Workbook
#import csv
def rand_arrange(c,fle='names.xls'):
    """n= Number of Students in a batch \n
    c= number of students in a group\n
    fle = name of students in excel csv format"""
    a=[]
    dic = {}
    namereader = ow(fle)
#    namereader = csv.reader(namedata)
    i = 1
#    rand_dic= {}
    s = namereader.sheets()[0]
#    for s in namereader.sheets():
    for rows in range(1,s.nrows):
        val=[]
        for cols in range(s.ncols):
            val.append(s.cell(rows,cols).value)
        dic[i]=val
        a.append(i)
        i+=1
    b=[]
    i=0
#    namewriter = csv.DictWriter(fle,fieldnames=['Sr.No.','names'])
#    writing in xls
    book = Workbook()
    sheet1 = book.add_sheet('result')
    sheet1.row(0).write(0,'Sr.no.')
    sheet1.row(0).write(1,'Roll No')
    sheet1.row(0).write(2,'Name')
    sheet1.row(0).write(3,'Group No.')
    sheet1.col(0).width = 2000
    sheet1.col(1).width = 4000
    sheet1.col(2).width = 5750
    sheet1.col(3).width = 2750
    while len(a)!=0:
        b.append(a.pop(rd.randint(len(a))))
        d=0
        for val in dic[b[i]]:
            sheet1.row(i+1).write(d,val)
            d += 1
        if i%c==0:
            e=i/c+1
#        sheet1.row(i+1).write(d,'Group %d'%(e))
        sheet1.row(i+1).write(d,e)
        i += 1
    book.save('result.xls')
#    return b
#print b

