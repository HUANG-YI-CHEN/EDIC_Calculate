# -*- coding: utf-8 -*-
import os, sys
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

### System Subroutine ###
clear = lambda: os.system( 'cls' )
unicode_cmd = lambda: os.system( 'chcp 65001 &' )

### System Variable Settings ###
"""
_V -> V; _Q -> Q; oVFE -> V'; _Q2 -> Q'; _tFE -> tFE; _EC -> EC; _Pr -> Pr
math.pow(10,4) -> 10X10X10X10
math.sqrt(4) -> √4
2*3 - > 2X3
"""
ofilename = 'omap.csv' # orignal filename
nfilename = 'nmap.csv' # new filename
afilename = 'amap.csv' # all filename

svg_title = "The Title"
x_axis = "x-axis (V)" 
y_axis = "y-axis (Q)"
svg_filename = "svg.png"
svg_format = "png"

_V = []
_Q = []
_VFE = []
_VFEo = []
_Q2 = []

_tFE = 2.5*math.pow(10,-7)
_Ec = math.pow(10,6)
_Pr = 9*math.pow(10,-6)

### User Defined Subroutine ###
def is_number(num):
    try:
        float(num) # for int, long and float
    except ValueError:
        try:
            complex(num) # for complex
        except ValueError:
            return False
    return True

def nearest(myList, num):
    return min(myList, key=lambda x:abs(x-num))

def myfunc(voltage):
    voltage = voltage*1.6*math.pow(10,-19)
    voltage = _tFE*3*math.sqrt(3)/2*_Ec*voltage/_Pr*(1+math.pow(voltage,2)/math.pow(_Pr,2))
    # voltage = voltage*2
    return voltage

def transitionfunc():
    # open CSV file, and get V sets and Q sets
    with open(ofilename, mode='r', newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            if len(row) == 2:
                if is_number(row[0]) is True & is_number(row[1]) is True:
                    _V.append(float(row[0])) # V[i]
                    _Q.append(float(row[1])) # Q[i]    

    # compute new V sets and new Q sets    
    with open(nfilename, mode='w',newline='') as csv_file:
        fieldnames = ["Vo'", "V'", "Q'"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in _Q:
            convert_vo = myfunc(i)              # Vo'[i]
            convert_i = nearest(_V,convert_vo)  # V'[i]
            if convert_i in _V:
                _Vo = convert_vo                # Vo'[i]
                _Vi = convert_i                 # V'[i]
                _Qi = _Q[_V.index(convert_i)]   # Q'[i]
                _VFEo.append(_Vo)        
                _VFE.append(_Vi)
                _Q2.append(_Qi)               
                writer.writerow({"Vo'":_Vo, "V'":_Vi, "Q'":_Qi})    

    # write V sets, Q sets, V' sets , Q' sets    
    with open(afilename, mode='w',newline='') as csv_file:
        fieldnames = ["V", "Q", "Vo'", "V'", "Q'"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i,v in enumerate(_V):
            writer.writerow({"V":_V[i],"Q":_Q[i], "Vo'":_VFEo[i] ,"V'":_VFE[i],"Q'":_Q2[i]})   
    
    # compute draw pics
    plt.title(svg_title) 
    plt.xlabel(x_axis) 
    plt.ylabel(y_axis)

    plt.plot(_V,_Q,'rs')
    plt.plot(_VFE,_Q2,'bs')
    
    # plt.show()
    
    # plt.savefig(svg_filename, dpi=300, format=svg_format) 

def test():
    print("V:",_V,"\nQ:",_Q,"\n")
    print("Vo:",_VFEo,"\n")
    print("V':",_VFE,"\nQ':",_Q2,"\n")
    

### 主程式 ###
if __name__ == '__main__':
    unicode_cmd()
    clear()
    transitionfunc()
    # test()
