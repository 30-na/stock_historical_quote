# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:31:30 2021

@author: msin2
"""
import csv
f = open('INTC_HistoricalQuotes.csv')
date = []
close = []
volume = []
open = []
high = []
low = []

csv_f = csv.reader(f)

# make a column
for row in csv_f:    
    date.append(row[0])
    close.append(row[1])
    volume.append(row[2])
    open.append(row[3])
    high.append(row[4])
    low.append(row[5])


# remove the $ sign and header 
def remove_header_turn_to_float(listName):
    listName.pop(0)
    i = 0
    while i < len(listName): 
        listName[i] = float ((listName[i])[2:len(listName[i])])
        i += 1 
    return listName

remove_header_turn_to_float(close)
remove_header_turn_to_float(open)
remove_header_turn_to_float(high)
remove_header_turn_to_float(low)

f.close()

# rolling average: standard deviation in 5 days windows
def RA_5(close):
    RA = []
    i = 0
    while i+4 < len(close):
        sum = 0
        for j in range(5):
            sum = close[i+j] + sum          
        RA.append(sum/5)
        i += 1 
    return RA


# rolling average: standard deviation in 5 days windows
def RA_10(close):
    RA = []
    i = 0
    while i+9 < len(close):
        sum = 0
        for j in range(10):
            sum = close[i+j] + sum
        RA.append(sum/10)
        i += 1
    return RA



#MACD moving average convergence divergence: a display trend following characteristic and momentum chararacteristic
def MACd(close):
    
    
    def EMA_12day(close):
        EMA = []
        #the first value = a trailing 12 days average
        sum = 0
        for j in range(1,13):
            sum = close[len(close)-j] + sum
        EMA.append(sum/12)
        # EMA formula:
        for i in range (13 , len(close))
            
        EMA.append(close)
        

print (close)
print (close[1])
print (close[len(close)-1])