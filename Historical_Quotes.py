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


## remove the $ sign and header 
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

high - low  
    