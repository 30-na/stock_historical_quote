# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 23:32:10 2021

@author: msin2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stock_file_name = "HistoricalData_1613966841110.csv"
time_frame = 1000
df = pd.read_csv(stock_file_name, parse_dates=['Date'] )

df.columns = df.columns.str.strip()

date = df['Date']
close_p = pd.to_numeric(df['Close/Last'].str.strip().str.replace('$',''))
open_p = pd.to_numeric(df['Open'].str.strip().str.replace('$',''))
high_p = pd.to_numeric(df['High'].str.strip().str.replace('$',''))
low_p = pd.to_numeric(df['Low'].str.strip().str.replace('$',''))
volume = df['Volume']

#SPY_500 close price
spy_file_name = "HistoricalData_1613966910825.csv"
df = pd.read_csv(spy_file_name, parse_dates=['Date'] )
df.columns = df.columns.str.strip()
if isinstance(df['Close/Last'], str):
    spy_close = pd.to_numeric(df['Close/Last'].str.strip().str.replace('$',''))
else:
    spy_close = pd.to_numeric(df['Close/Last'])

#VIX close price
vix_file_name = "vixcurrent.csv"
df = pd.read_csv(vix_file_name, skiprows = 1 )
df.columns = df.columns.str.strip()
if isinstance(df['VIX Close'], str):
     vix_close = pd.to_numeric(df['VIX Close'].str.strip().str.replace('$',''))
else:
     vix_close = pd.to_numeric(df['VIX Close'])

#SOX close price
sox_file_name = "HistoricalData_1613968277121.csv"
df = pd.read_csv(sox_file_name, parse_dates=['Date'] )
df.columns = df.columns.str.strip()
if isinstance(df['Close/Last'], str):
    sox_close = pd.to_numeric(df['Close/Last'].str.strip().str.replace('$',''))
else:
    sox_close = pd.to_numeric(df['Close/Last'])

# Rolling Average: standard deviation different period time window
def STD(myList, timePeriod = 20):
    STD = []
    for i in range(len (myList) - timePeriod):
        STD.append(np.std(myList[i: (i + timePeriod) ]))
    return STD

def WPR(close_p, high_p, low_p, timePeriod = 14):
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
    for i in range (len(close_p) - timePeriod):
        highest_high = max(high_p[i : i + timePeriod])
        lowest_low = min(low_p[i : i + timePeriod])
        william_percent_range.append(1 - (highest_high - close_p[i]) / (highest_high - lowest_low))
    return william_percent_range


def MACD(close_p, timePeriodShort = 12, timePeriodLong = 26):
    '''
    Moving Average Convergence Divergence: a display trend following characteristic and momentum chararacteristic

    Parameters
    ----------
    close : TYPE
        DESCRIPTION.
    timePeriodShort : TYPE, optional
        DESCRIPTION. The default is 12.
    timePeriodLong : TYPE, optional
        DESCRIPTION. The default is 26.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    def EMA(close, timePeriod):
        EMA = []     
        sum = 0
        for j in range(1,(timePeriod+1) ):
            sum = close[len(close)-j] + sum
        EMA.append(sum/timePeriod)   
        for i in range ((timePeriod+1) , len(close) + 1):
            EMA.append( (close[len(close) - i])*(2/(timePeriod+1)) + (EMA[i-(timePeriod+1)])*(1 - ( 2/ (timePeriod+1) ) ) )  
        # reverce the EMA                
        EMA.reverse()      
        return EMA
    EMA_short = EMA(close_p, timePeriodShort)
    EMA_long = EMA(close_p, timePeriodLong)
    MACD = []    
    for i in range(len(EMA_long)):
        MACD.append( EMA_short[i] - EMA_long[i])
    return MACD

def TP(high, low, close):
    '''
    Typical Price = (TP) = (High + Low + Close)/3

    Parameters
    ----------
    high : TYPE
        DESCRIPTION.
    low : TYPE
        DESCRIPTION.
    close : TYPE
        DESCRIPTION.

    Returns
    -------
    typicalPrice : TYPE
        DESCRIPTION.

    '''
    typicalPrice = []
    for i in range(len(close)):
        typicalPrice.append ( ( high[i] + low[i] + close[i] ) / 3)
    return typicalPrice
 
def CCI(close, high, low, timePeriod = 20):
    '''
    Commodity Change: an identification of cyclinical trend

    Parameters
    ----------
    high : TYPE
        DESCRIPTION.
    low : TYPE
        DESCRIPTION.
    close : TYPE
        DESCRIPTION.
    timePeriod : TYPE, optional
        DESCRIPTION. The default is 20.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
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

def ATR(close, low, high, timePeriod = 14):
    '''
    Average True Range: a measurment of the volatility of price
    smoooting: SMA

    Parameters
    ----------
    close : TYPE
        DESCRIPTION.
    low : TYPE
        DESCRIPTION.
    high : TYPE
        DESCRIPTION.
    timePeriod : TYPE, optional
        DESCRIPTION. The default is 14.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
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
        mBand.append(np.mean(close[i : i + timePeriod]))
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
        MA.append(np.mean(close[i: i + timePeriod]))
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

def checking_plot(my_list):  
    x = date[1:90]
    y = my_list[1:90]
    plt.plot(x, y )
    plt.grid(True)
    plt.xlabel("date")
    plt.show()

# print(MA(close_p, 5))
# checking_plot(ROC(close_p))

df = {'date': date[:time_frame],
      'close_price': close_p[:time_frame],
      'volume': volume[:time_frame],
      'open_price': open_p[:time_frame],
      'high': high_p[:time_frame],
      'low': low_p[:time_frame],
      'RA_5': STD(close_p, 5)[:time_frame],
      'RA_10': STD(close_p, 10)[:time_frame],
      'MACD': MACD(close_p)[:time_frame],
      'CCI': CCI(close_p, high_p, low_p)[:time_frame],
      'ATR': ATR(close_p, low_p, high_p)[:time_frame],
      'BOLL_middle': middle_band(close_p)[:time_frame],
      'BOLL_upper': upper_band(close_p)[:time_frame],
      'BOLL_lower': lower_band(close_p)[:time_frame],
      'MA_5': MA(close_p, 5)[:time_frame],
      'MA_10': MA(close_p, 10)[:time_frame],
      'MTM_1': MTM (close_p, 30)[:time_frame],
      'MTM_3': MTM (close_p, 90)[:time_frame],
      'ROC': ROC(close_p, 90)[:time_frame],
      'WPR': WPR(close_p, high_p, low_p)[:time_frame],
      'SPY_500': spy_close[:time_frame],
      'VIX': vix_close[:time_frame],
      'SOX': sox_close[:time_frame]
                }
      
export_file = pd.DataFrame(df, columns= ['date','close_price', 'volume' , 'open_price',
                                          'high', 'low','RA_5','RA_10','MACD', 'CCI', 'ATR',
                                          'BOLL_middle','BOLL_upper', 'BOLL_lower', 'MA_5',
                                          'MA_10', 'MTM_1','MTM_3', 'ROC', 'WPR', 'SPY_500',
                                          'VIX', 'SOX'])
export_file.to_csv("input_features.csv", header = True, index = False )








