# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:31:30 2021

@author: msin2
"""
import csv
import numpy
import matplotlib.pyplot as plt

 


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

#Rolling Average: standard deviation different period time window
def STD(myList, timePeriod = 20):
    STD = []
    for i in range(len (myList) - timePeriod):
        STD.append(numpy.std(myList[i: (i + timePeriod) ]))
    return STD



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

#Typical Price = (TP) = (High + Low + Close)/3
def TP(high, low, close):
    typicalPrice = []
    for i in range(len(close)):
        typicalPrice.append ( ( high[i] + low[i] + close[i] ) / 3)
    return typicalPrice
    
# Commodity Change: an identification of cyclinical trend
def CCI(high, low, close, timePeriod = 20):
    constant = .015    
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
#https://www.investopedia.com/terms/m/movingaverage.asp
def MA(close, timePeriod):
    MA = []
    for i in range (len(close) - timePeriod):
        MA.append(numpy.mean(close[i: i + timePeriod]))
    return MA

# month momentum: the difference between current price and the price 1 or 3 month ago (trading day)
#https://www.investopedia.com/articles/technical/081501.asp
def MTM (close, timePeriod = 30):
    MTM = []
    for i in range(len(close) - timePeriod ):
        MTM.append( close[i] - close[i + timePeriod])
    return MTM

# price Rate Of Cahnge: ROC=((Closing Price p -  Closing Price p−n) / Closing Price p−n )*100
# https://www.investopedia.com/terms/p/pricerateofchange.asp
def ROC (close, timePeriod = 90):
    ROC = []
    for i in range (len(close) - timePeriod):
        ROC.append( ((close[i] - close[i + timePeriod]) / close[i + timePeriod] )*100 )
    return ROC

def BOLM(close, timePeriod = 20):
    '''
    middle band = simple moving average (SMA) of a security's price in typically last 20 days.
    SMA= (A1 + A2 + ... +An) / n 
    where:
    A=Average closing price in period n
    n=Number of time periods  (typically 20)
    https://www.investopedia.com/terms/b/bollingerbands.asp

    Parameters
    ----------
    close : (list)
        closing price.
    timePeriod : (integer), optional
        Number of time periods. The default is 20.

    Returns
    -------
    middle_band : (list)
        average out the closing prices for the first 20 days as the first data point.

    '''
    middle_band = []
    for i in range(len(close) - timePeriod):
        middle_band.append(numpy.mean(close[i : i + timePeriod]))
    return middle_band

def BOLU (close, high, low, timePeriod = 20):
    '''
    BOLU=MA(TP,n)+m∗σ[TP,n]
    where:
    MA=Moving average
    TP (typical price)=(High+Low+Close)÷3
    n=Number of days in smoothing period (typically 20)
    m=Number of standard deviations (typically 2)
    σ[TP,n]=Standard Deviation over last n periods of TP
​	https://www.investopedia.com/terms/b/bollingerbands.asp

    Parameters
    ----------
    close : (list)
        close/last price.
    high : (list)
        hige price.
    low : (list)
        low price.
    timePeriod : (integer) , optional
        Number of time periods. The default is 20.

    Returns
    -------
    upper_band : (list)
       Upper Bollinger Band 

    '''
    number_of_standard_deviation = 2
    upper_band = []
    typical_price = TP(high, low, close)
    simple_moving_average = BOLM(typical_price, timePeriod)
    standard_deviation = STD(typical_price, timePeriod)
    for i in range(len (simple_moving_average)):
        upper_band.append( simple_moving_average[i] + number_of_standard_deviation * (standard_deviation[i]) )
    return upper_band

def BOLD (close, high, low, timePeriod = 20):
    '''
    BOLD=MA(TP,n)−m∗σ[TP,n]
    where:
    MA=Moving average
    TP (typical price)=(High+Low+Close)÷3
    n=Number of days in smoothing period (typically 20)
    m=Number of standard deviations (typically 2)
    σ[TP,n]=Standard Deviation over last n periods of TP
​	https://www.investopedia.com/terms/b/bollingerbands.asp

    Parameters
    ----------
    close : (list)
        close/last price.
    high : (list)
        hige price.
    low : (list)
        low price.
    timePeriod : (integer) , optional
        Number of time periods. The default is 20.

    Returns
    -------
    lower_band : (list)
       Lower Bollinger Band  

    '''
    number_of_standard_deviation = 2
    lower_band = []
    typical_price = TP(high, low, close)
    simple_moving_average = BOLM(typical_price, timePeriod)
    standard_deviation = STD(typical_price, timePeriod)
    for i in range(len (simple_moving_average)):
        lower_band.append( simple_moving_average[i] - number_of_standard_deviation * (standard_deviation[i]) )
    return lower_band



def WPR(close, high, low, timePeriod = 14):
    '''
    Williams %R, also known as the Williams Percent Range, is a type of momentum indicator that moves between 0 and -100 and measures overbought and oversold levels.
    The Williams %R may be used to find entry and exit points in the market.
    It was developed by Larry Williams and it compares a stock’s closing price to the high-low range over a specific period, typically 14 days or periods.
    Wiliams %R= (Highest High−Close) / (Highest High−Lowest Low)	 
    where:
    Highest High=Highest price in the lookback
    period, typically 14 days.
    Close=Most recent closing price.
    Lowest Low=Lowest price in the lookback
    period, typically 14 days.
​	https://www.investopedia.com/terms/w/williamsr.asp
    
    Parameters
    ----------
    close : (list)
        close/last price.
    high : (list)
        hige price.
    low : (list)
        low price.
    timePeriod : (integer) , optional
        Number of time periods. The default is 14.

    Returns
    -------
    william_percent_range: (list)
        William Percent Range

    '''
    william_percent_range = []
    for i in range (len(close) - timePeriod):
        highest_high = max(high[i : i + timePeriod])
        lowest_low = min(low[i : i + timePeriod])
        # print(highest_high)
        # print(lowest_low)
        william_percent_range.append(1 - (highest_high - close[i]) / (highest_high - lowest_low))
    return william_percent_range


def checking_plot(my_list):
    
    x = date[1:90]
    y = my_list[1:90]
    x.reverse()
    y.reverse()
    plt.plot(x, y )
    plt.grid(True)
    plt.xlabel("date")
    plt.show()
# for i in range (100):
#     print (middle_band(close)[i] , upper_band(close)[i], lower_band(close)[i] )

checking_plot(WPR(close, high, low))








