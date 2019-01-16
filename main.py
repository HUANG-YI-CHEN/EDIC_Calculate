# -*- coding: utf-8 -*-
import os, sys
import math
import csv
from decimal import (Decimal as dec, getcontext as gc)
import lib.config as cfg
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
cfg_parameter = cfg.Config().get('parameter')
gc().prec = int(cfg_parameter['f_len']) # set float precision
_tFE = eval(cfg_parameter['tfe'])
_Ec = eval(cfg_parameter['ec'])
_Pr = eval(cfg_parameter['pr'])

cfg_file = cfg.Config().get('file') # set float precision
dirsrcpath = cfg_file['src']
if cfg_file['src'] is '':
   dirsrcpath = cfg.Config().path+'src'+'\\'
dirdstpath = cfg_file['dst']
if cfg_file['dst'] is '':
   dirdstpath = cfg.Config().path+'dst'+'\\'
if not os.path.exists(dirdstpath):
    os.makedirs('dst')
ofilename = cfg_file['src_f_org']   # orignal filename
mfilename = cfg_file['src_f_map']   # map v-i filename
nfilename = cfg_file['dst_f_new']   # new filename(+)
dfilename = cfg_file['dst_f_new_d']  # new filename(-)
afilename = cfg_file['dst_f_all']   # all filename

cfg_graphic = cfg.Config().get('graphic')
svg_title = cfg_graphic['g_title']
x_axis = cfg_graphic['g_x_axis']
y_axis = cfg_graphic['g_y_axis']
svg_filename = cfg_graphic['g_name']
svg_format = cfg_graphic['g_fmt']
g_blue_style = int(cfg_graphic['g_blue_style'])
g_red_style = int(cfg_graphic['g_red_style'])
svg_filename = svg_filename+'.'+svg_format

_V = []
_Q = []
_Vmap = []
_Imap = []
_VFE = []
_VFEm = []
_VFEd = []
_VFEe = []
_I = []

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
    return min(myList, key=lambda x:abs(dec(str(x))-dec(str(num))))

def myfunc(charge):
    # charge = charge*1.6*math.pow(10,-19)
    # charge = _tFE*3*math.sqrt(3)/2*charge*_Ec/_Pr*(1+math.pow(charge,2)/math.pow(_Pr,2))
    charge = (dec(str(_tFE))*dec(str(3))*dec(str(math.sqrt(3)))/dec(str(2))*dec(str(charge))*dec(str(_Ec))/dec(str(_Pr))*
            (dec(str(1))+dec(str(math.pow(charge,2)))/dec(str(math.pow(_Pr,2)))))
    return charge

def transitionfunc():
    # open CSV file, and get V sets and Q sets
    with open(dirsrcpath+ofilename, mode='r', newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            if len(row) > 0:
                if is_number(row[0]) is True & is_number(row[1]) is True:
                    _V.append(float(row[0])) # V[i]
                    _Q.append(float(row[1])) # Q[i]

    # open CSV file, and get Vnew sets and Inew sets
    with open(dirsrcpath+mfilename, mode='r', newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            if len(row) > 0:
                if is_number(row[0]) is True & is_number(row[1]) is True:
                    _Vmap.append(float(row[0])) # Vnew[i]
                    _Imap.append(float(row[1])) # Inew[i]

    # compute new V' sets, and find mappped V sets and mapped I sets
    for i, v in enumerate(_Q):
        convert_vd = dec(str(myfunc(v)))
        convert_vo = dec(str(_V[i]))+dec(convert_vd)        # Vo'= V[i]+Vd'[i]
        convert_ve = dec(str(_V[i]))-dec(convert_vd)        # Ve'= V[i]-Vd'[i]
        convert_vn = nearest(_Vmap, convert_vo)             # Vnew'[i]
        if convert_vn in _Vmap:
            _Vd = convert_vd
            _Vo = convert_vo                                # Vo'[i]
            _Ve = convert_ve
            _Vn = convert_vn                                # Vnew'[i]
            _Ii = _Imap[_Vmap.index(_Vn)]                   # Inew'[i]
            _VFEd.append(_Vd)
            _VFEe.append(_Ve)
            _VFE.append(_Vo)
            _VFEm.append(_Vn)
            _I.append(_Ii)

    # write V sets, Q sets, V' sets , Q' sets
    try:
        with open(dirdstpath+nfilename, mode='w',newline='') as csv_file:
            fieldnames = ["V", "I'"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i,v in enumerate(_V):
                writer.writerow({"V":_V[i], "I'":_I[i]})
    except:
        print("The file is used by your system!\nYou must have to close it, and restart this program again .")

    # write V sets, Q sets, V' sets , Q' sets
    try:
        with open(dirdstpath+dfilename, mode='w',newline='') as csv_file:
            fieldnames = ["V", "I'"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i,v in enumerate(_V):
                writer.writerow({"V":_VFEe[i], "I'":_I[i]})
    except:
        print("The file is used by your system!\nYou must have to close it, and restart this program again .")

    # write V sets, Q sets, V' sets , Q' sets
    try:
        with open(dirdstpath+afilename, mode='w',newline='') as csv_file:
            fieldnames = ["V", "Q", "Vd", "Vo'", "Ve", "Vm'", "I'"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i,v in enumerate(_V):
                writer.writerow({"V":_V[i],"Q":_Q[i], "Vd":_VFEd[i], "Vo'":_VFE[i], "Ve":_VFEe[i], "Vm'":_VFEm[i], "I'":_I[i]})
    except:
        print("The file is used by your system!\nYou must have to close it, and restart this program again .")

    # draw pics
    g_V = [_Vmap, _V, _VFEe]
    g_I = [_Imap, _I, _I]
    g_colors = ['b','r']
    g_styles = ['^','s','-','--','-.','"']
    g_label = [ "V-I","V'-I'","V-I","V'-I'"]

    plt.style.use('seaborn-bright') # default, classic, bmh, seabom-bright
    fig, ax = plt.subplots(1, 4, figsize=(18,5.8), sharex=False, sharey=False)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)

    for i in range(1,5):
        ax[i-1].set_title(svg_title)
        ax[i-1].plot(g_V[0],g_I[0], g_styles[g_blue_style], color = g_colors[0], label = g_label[0])
        if i > 2:
            ax[i-1].plot(g_V[2],g_I[2], g_styles[g_red_style], color = g_colors[1], label = g_label[i-1])
        else:
            ax[i-1].plot(g_V[1],g_I[1], g_styles[g_red_style], color = g_colors[1], label = g_label[i-1])
        ax[i-1].set_xlabel(x_axis, color = 'black')
        ax[i-1].set_ylabel(y_axis, color = 'black')
        if i%2==0:
            ax[i-1].set_yscale('log')
        ax[i-1].legend(loc='upper left', shadow=True)
        ax[i-1].relim()
        ax[i-1].autoscale()
        for tick in ax[i-1].get_xticklabels():
            tick.set_rotation(45)
        for tick in ax[i-1].get_yticklabels():
            tick.set_rotation(45)

    plt.savefig(dirdstpath+svg_filename, format=svg_format)
    plt.show()
    print("Process successfully.")

def test():
    print(_tFE,_Ec,_Pr)
    print("V:",_V,"\nQ:",_Q,"\n")
    print("Vmap:",_Vmap,"\nImap:",_Imap,"\n")
    print("Vo:",_VFE,"\n")
    print("V':",_VFEm,"\nI':",_I,"\n")
    print("Vd':",_VFEd,"\n")

### 主程式 ###
if __name__ == '__main__':
    unicode_cmd()
    clear()
    transitionfunc()
    # test()