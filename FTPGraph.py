from __future__ import absolute_import
import bokeh.sampledata
import yaml
import csv
from builtins import list
import time
import datetime
import random
import sys

from bokeh.plotting import figure, output_file, show
from bokeh.io import export_png
from bokeh.layouts import row, column
from numpy.lib.function_base import append
from test.datetimetester import HOUR, DAY
from bokeh.colors.groups import green
from cmath import pi
from bokeh.models.annotations import Label, LabelSet
from bokeh.plotting.figure import FigureOptions
from bokeh.models.tickers import AdaptiveTicker, ONE_MINUTE, ONE_SECOND, Ticker
from bokeh.core.properties import Instance
from bokeh.models.renderers import GuideRenderer
from bokeh.models.grids import Grid

serverlist = 'RadarOrigin EuroLA EuroS GRAPES_GFS cma7d3h cma7d12h GRAPES_MESO HDland HDair HSD NW124/rgwst NW124/rnwst NW124/SURF_CHN_MUL_DAY NW124/ghwst NW124/rtemp.ch NW124/rtemp.glb NW124/rloct NW124/SURF_CHN_5MIN NW124/RADA_L2_UFMT NW127/rgwst NW127/rnwst NW127/SURF_CHN_MUL_DAY NW127/ghwst NW127/rtemp.ch NW127/rtemp.glb NW127/rloct NW127/SURF_CHN_5MIN NW127/GRAPES_GFS NW127/cma7d3h NW127/cma7d12h DMZ52 NW128/EuroLA NW128/EuroS NW128/GRAPES_MESO NW128/HDland NW128/HDair'
#serverlist = 'RadarOrigin'
blankindex = serverlist.find(' ')
blank = []
blank.append(-1)
while blankindex != -1:
    blank.append(blankindex)
    blankindex = serverlist.find(' ', blankindex+1)
blankdivide = []
for i in range(0, len(blank)-1):
    blankdivide.append(serverlist[blank[i]+1:blank[i+1]])
blankdivide.append(serverlist[blank[len(blank)-1]+1:])
today=datetime.datetime.today()
oneday=datetime.timedelta(days=1)
yesterday=today-3*oneday
filename = str(yesterday.strftime('%Y%m%d'))
time = str(yesterday.strftime('%Y-%m-%d'))
alrexp = []
class timelistgraph(object):
    days = 0
    date = []
    filename = []
    time = []
    color = []

    def __init__(self,number):
        self.days = number
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        self.color.append("#DC143C")
        self.color.append("#FF8C00")
        self.color.append("#FFD700")
        self.color.append("#006400")
        self.color.append("#0033FF")
        self.color.append("#003399")
        self.color.append("#9400D3")
        for i in range(0,self.days+1):
            day = today-i*oneday
            filename = str(day.strftime('%Y%m%d'))
            time = str(day.strftime('%Y-%m-%d'))
            self.date.append(day)
            self.filename.append(filename)
            self.time.append(time)
            print(time)
colorlist = []
colorlist.append("#DC143C")
colorlist.append("#FF8C00")
colorlist.append("#FFD700")
colorlist.append("#006400")
colorlist.append("#0033FF")
colorlist.append("#003399")
colorlist.append("#9400D3")
def drawline(p,servername,i,legendname,filename1):
    csv_reader = csv.reader(open('D:\\CSVFiles\\' + filename1 + '\\Python\\' + servername +'.csv', 'r'))
    a = 0
    list1=[]
    list2=[]
    list3=[]
    for row in csv_reader:
        a+=1
        if a>1:
            a1 = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            if a == 2:
                nowtime = a1.strftime('%Y-%m-%d')
            #oneday=datetime.timedelta(days=1)
            #day = a1 + i*oneday
            list1.append(a1)
            list2.append(int(row[1]))
            list3.append(float(row[2]))
    p.line(list1,list2,color=colorlist[i],line_width=2,alpha = 1, legend = legendname)
for i in range(0, len(blankdivide)):
    if i in alrexp:
        break
    servername = ''
    if blankdivide[i].find('/') != -1:
        servername = blankdivide[i].replace('/', '_')
    else:
        servername = blankdivide[i]
    realservername = blankdivide[i]
    realservername1 = servername
    #titlename = "Daily Report for " + realservername + " at " + time
    timelist = timelistgraph(4)
    graph = []
    for j in range(1,len(timelist.date)):
        a1 = datetime.datetime.strptime(timelist.filename[j], '%Y%m%d')
        delta = today-a1
        if delta.days<1:
            break
        print(timelist.filename[j])
        null = figure(plot_width=2000, plot_height=500, x_axis_type="datetime")
        p = figure(plot_width=2000, plot_height=500, x_axis_type="datetime")
        titlename = "Daily Report for " + realservername + " at " + timelist.time[j]
        p.title.text = titlename
        p.title.align = 'center'
        p.xaxis.axis_label = 'Time'
        p.xaxis.axis_label_text_font_style = 'normal'
        p.xaxis.ticker =  AdaptiveTicker(mantissas=[1, 2, 5, 10, 15, 20, 30],base=60,min_interval=ONE_SECOND,max_interval=30*ONE_MINUTE,num_minor_ticks=3)
        p.xaxis.major_tick_in = 0
        p.xgrid[0].ticker = AdaptiveTicker(mantissas=[1, 2, 5, 10, 15, 20, 30],base=60,min_interval=ONE_SECOND,max_interval=30*ONE_MINUTE,num_minor_ticks=3)
        p.yaxis.axis_label = 'Filecount'
        p.yaxis.axis_label_text_font_style = 'normal'
        today=datetime.datetime.today()
        count = 0
        drawline(p,servername,3,blankdivide[i],timelist.filename[j])
        count-=1
        for k in range(i+1, len(blankdivide)):
            a1 = datetime.datetime.strptime(timelist.filename[j], '%Y%m%d')
            delta = today-a1
            if delta.days<1:
                break
            checkname = ''
            if blankdivide[i].find('/') != -1 or blankdivide[i].find('_') != -1:
                index1 = blankdivide[i].find('/')
                index2 = blankdivide[i].find('_')
                if index1 != -1:
                    checkname = blankdivide[i][index1+1:]
                else:
                    checkname = blankdivide[i][index2+1:]
            else:
                checkname = blankdivide[i]
            a = blankdivide[k].find(checkname)
            if a != -1:
                servername = ''
                if blankdivide[k].find('/') != -1:
                    servername = blankdivide[k].replace('/', '_')
                else:
                    servername = blankdivide[k]
                colornumber = 3 + count
                drawline(p,servername,colornumber,blankdivide[k],timelist.filename[j])
                count-=1
                alrexp.append(k)
        graph.append(p)
    '''
    a1 = datetime.datetime.strptime(timelist.filename[i], '%Y%m%d')
    delta = today-a1
    if delta.days<1:
        break
    '''
    '''
    csv_reader = csv.reader(open('D:\\CSVFiles\\' + filename + '\\Python\\' + servername +'.csv', 'r'))
    a = 0
    list1=[]
    list2=[]
    list3=[]
    for row in csv_reader:
        a+=1
        if a>1:
            a1 = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            if a == 2:
                nowtime = a1.strftime('%Y-%m-%d')
            oneday=datetime.timedelta(days=1)
            day = a1 + i*oneday
            list1.append(day)
            list2.append(int(row[1]))
            list3.append(float(row[2]))
    p.line(list1,list2,color="#006400",line_width=2,alpha = 1-0.1*(i-1))
    '''
    p1 = graph[0]
    p2 = graph[1]
    p3 = graph[2]
    p4 = graph[3]
    #show(row(p1,p2,p3,p4))
    export_png(column(p1,p2,p3,p4), filename = 'D:\\CSVFiles\\' + '\\PNG\\' + realservername1 +'.png')
    print(servername + ' Report Export Finished')
    graph = []
    p1 = null
    p2 = null
    p3 = null
    p4 = null
print('All Report Exported')
sys.exit(0)
