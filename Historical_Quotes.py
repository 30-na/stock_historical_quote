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

# Rolling Average: standard deviation different period time window
def RA(close, timePeriod):
    RA = []
    for i in range(len(close) - timePeriod + 1):
        sum = 0
        for j in range(timePeriod):
            sum = close[i+j] + sum          
        RA.append(sum/timePeriod)
    return RA



# Moving Average Convergence Divergence: a display trend following characteristic and momentum chararacteristic
def MACD(close, timePeriodShort = 12, timePeriodLong = 26):
    def EMA(close, timePeriod):
        EMA = []     
        #the first day = a trailing 12 days average
        sum = 0
        for j in range(1,(timePeriod+1) ):
            sum = close[len(close)-j] + sum
        EMA.append(sum/timePeriod)   
        # EMA formula after the first day:
        for i in range ((timePeriod+1) , len(close) + 1):
            EMA.append( (close[len(close) - i])*(2/(timePeriod+1)) + (EMA[i-(timePeriod+1)])*(1 - ( 2/ (timePeriod+1) ) ) )  
        # reverce the EMA                
        EMA.reverse()      
        return EMA
    EMA_short = EMA(close, timePeriodShort)
    EMA_long = EMA(close, timePeriodLong)
    MACD = []    
    for i in range(len(EMA_long)):
        MACD[i] = EMA_short[i] - EMA_long[i]
    return MACD

# Commodity Change: an identification of cyclinical trend
def CCI(high, low, close, timePeriod = 20):
    constant = .015    
    #Typical Price = (TP) = (High + Low + Close)/3
    def TP(high, low, close):
        typicalPrice = []
        for i in range(len(close)):
            typicalPrice.append ( ( high[i] + low[i] + close[i] ) / 3)
        return typicalPrice
    #Simple Moving Average of Typical Price = (High + Low + Close)/3
    def SMA_TP(typicalPrice, timePeriod = 20):
        SMA = []
        for i in range((len(typicalPrice) - timePeriod) + 1):
            sum = 0
            for j in range(timePeriod):
                sum = typicalPrice[i+j] + sum          
            SMA.append(sum/timePeriod)
        return SMA
    # Mean Deviation
    def MD(typicalPrice, simpleMovingAverage, timePeriod = 20):
        MD = []
        for i in range(len(simpleMovingAverage)):
            sum = 0
            for j in range (timePeriod):
                sum = abs(simpleMovingAverage[i] - typicalPrice[i+j]) +  sum
            MD.append(sum/timePeriod)
        return MD
    # CCI = (Typical Price  -  Time Period SMA of TP) / (.015 x Mean Deviation)
    
    typicalPrice = TP (high, low, close)
    simpleMovingAverage  = SMA_TP (typicalPrice, timePeriod = 20)
    meanDeviation = MD (typicalPrice, simpleMovingAverage, timePeriod = 20)
    CCI = []
    for i in range(len(close) - timePeriod + 1):
        CCI.append ((typicalPrice[i] - simpleMovingAverage[i]) / (constant * meanDeviation[i]))
    return CCI    
print (CCI(high, low, close))       
        
        
    
    
