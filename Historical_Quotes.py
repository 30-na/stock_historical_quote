# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:31:30 2021

@author: msin2
"""
import csv
import numpy
f = open('INTC_HistoricalQuotes.csv')
date = []
close = []
volume = []
open = []
high = []
low = []

csv_f = csv.reader(f)

for row in csv_f:    
    date.append(row[0])
    close.append(row[1])
    volume.append(row[2])
    open.append(row[3])
    high.append(row[4])
    low.append(row[5])

#Remove the headers
def remove_header(listName):
    listName.pop(0)
    return listName

remove_header(close)
remove_header(open)
remove_header(high)
remove_header(low)
remove_header(volume)

#remove the "$ " for each elements
def remove_sign(listName):
    i = 0
    while i < len(listName): 
        listName[i] = (listName[i])[2:len(listName[i])]
        i += 1 
    return listName

remove_sign(close)
remove_sign(open)
remove_sign(low)
remove_sign(high)

#turn to float 
def turn_to_float(listName):
    i = 0
    while i < len(listName): 
        listName[i] = float (listName[i])
        i += 1 
    return listName
turn_to_float(close)
turn_to_float(open)
turn_to_float(low)
turn_to_float(high)
turn_to_float(volume)

f.close()

# Rolling Average: standard deviation different period time window
# def RA(close, timePeriod):
#     RA = []
#     for i in range(len(close) - timePeriod + 1):
#         sum = 0
#         for j in range(timePeriod):
#             sum = close[i+j] + sum          
#         RA.append(sum/timePeriod)
#     return RA



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
        MACD.append( EMA_short[i] - EMA_long[i])
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
    #Simple Moving Average of Typical Price
    def SMA_TP(myList, timePeriod = 20):
        SMA = []
        for i in range((len(myList) - timePeriod) + 1):
            sum = 0
            for j in range(timePeriod):
                sum = myList[i+j] + sum          
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

# Average True Range: a measurment of the volatility of price
def ATR(close, low, high, timePeriod = 14):
    # true raneg
    def true_range(close, low , high):
        TR = []
        for i in range(len(close) - 1):
            TR.append( max( (high[i] - low[i]), abs(high[i] - close[i+1]), abs(low[i] - close[i +1])) )
        return TR
    TR = true_range(close, low, high)
    # Average True Range
    ATR = []
    for i in range(len(close) - timePeriod):
        sum = 0
        for j in range(timePeriod):
            sum = TR[i + j] + sum
        ATR.append(sum / timePeriod)
    return ATR

#Bollinger Band: two standard deviation from the moving average (Middle Band, Upper Band, Loewr Band)
# Middle band 20-day simple moving average (SMA)
def middle_band(close, timePeriod = 20):
    mBand = []
    for i in range(len(close) - timePeriod):
        mBand.append(numpy.mean(close[i : i + timePeriod]))
    return mBand
#standard deviation    
def STD(myList, timePeriod = 20):
    STD = []
    for i in range(len (myList) - timePeriod):
        STD.append(numpy.std(myList[i: (i + timePeriod) ]))
    return STD
#upper band = 20-day SMA + (20-day standard deviation of price x 2)
def upper_band(myList, timePeriod = 20):
    uBand = []
    simple_moving_average = middle_band(myList, timePeriod)
    standard_deviation = STD(myList, timePeriod)
    for i in range(len (simple_moving_average)):
        uBand.append( simple_moving_average[i] + (standard_deviation[i] * 2) )
    return uBand
#Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
def lower_band(myList, timePeriod = 20 ):
    lBand = []
    simple_moving_average = middle_band(myList, timePeriod)
    standard_deviation = STD(myList, timePeriod)
    for i in range(len (simple_moving_average)):
        lBand.append( simple_moving_average[i] - (standard_deviation[i] * 2) )
    return lBand

# Moving Average simple Moving Average
def moving_average(myList, timePeriod):
    MA = []
    for i in range (len(myList) - timePeriod):
        MA.append(numpy.mean(myList[i: i + timePeriod]))
    return MA


print (moving_average(close, 5))