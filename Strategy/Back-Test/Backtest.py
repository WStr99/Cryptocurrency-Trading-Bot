import pandas as pd
import datetime as dt
from binance.client import Client
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from binance.enums import *
import warnings
warnings.filterwarnings('ignore')

#Getting Data from Binance
def getData(ticker, interval, start):
    client = Client('gRlkn6fkjj7rD4i7eOtYIm4qDA0jhXT6uIjAEqR2EgLCI4jweygYlrtYi9vbuzhc','RN7Ye5lGUvsQwfNMdbLUr5Va0qwszFhZJnRQylb5HMSU6A4kgJ1AbwBNWaql021Z') #Private API Keys
    data = client.get_historical_klines(symbol=ticker, interval=interval, start_str=start + " UTC")
    DF = pd.DataFrame(data = data)
    DF.columns = ["date", "open", "high", "low", "close", "volume", "Close Time", "Quote", "Trade", "1", "2", "3"]
    DF.drop(["1","2","3","Quote","Trade","Close Time", "volume"],axis=1,inplace=True)
    DF["date"] = DF.date.astype(int)
    DF["open"] = DF.open.astype(float)
    DF["close"] = DF.close.astype(float)
    DF["low"] = DF.low.astype(float)
    DF["high"] = DF.high.astype(float)
    return DF

#Supertrend Calculation
def SuperTrend(DF,f,n): #df is the dataframe, n is the period, f is the factor.
    #Calculating Average True Ragnge
    df = DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs( df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1)
    df['ATR']=np.nan
    df.loc[n-1,'ATR']=df['TR'][:n-1].mean() #.ix is deprecated from pandas verion- 0.19
    for i in range(n,len(df)):
        df['ATR'][i]=(df['ATR'][i-1]*(n-1)+ df['TR'][i])/n

    #Calculating of SuperTrend
    df['Upper Basic']=(df['high']+df['low'])/2+(f*df['ATR'])
    df['Lower Basic']=(df['high']+df['low'])/2-(f*df['ATR'])
    df['Upper Band']=df['Upper Basic']
    df['Lower Band']=df['Lower Basic']
    for i in range(n,len(df)):
        if df['close'][i-1]<=df['Upper Band'][i-1]:
            df['Upper Band'][i]=min(df['Upper Basic'][i],df['Upper Band'][i-1])
        else:
            df['Upper Band'][i]=df['Upper Basic'][i]
    for i in range(n,len(df)):
        if df['close'][i-1]>=df['Lower Band'][i-1]:
            df['Lower Band'][i]=max(df['Lower Basic'][i],df['Lower Band'][i-1])
        else:
            df['Lower Band'][i]=df['Lower Basic'][i]
    df['SuperTrend']=np.nan
    for i in df['SuperTrend']:
        if df['close'][n-1]<=df['Upper Band'][n-1]:
            df['SuperTrend'][n-1]=df['Upper Band'][n-1]
        elif df['close'][n-1]>df['Upper Band'][i]:
            df['SuperTrend'][n-1]=df['Lower Band'][n-1]
    for i in range(n,len(df)):
        if df['SuperTrend'][i-1]==df['Upper Band'][i-1] and df['close'][i]<=df['Upper Band'][i]:
            df['SuperTrend'][i]=df['Upper Band'][i]
        elif  df['SuperTrend'][i-1]==df['Upper Band'][i-1] and df['close'][i]>=df['Upper Band'][i]:
            df['SuperTrend'][i]=df['Lower Band'][i]
        elif df['SuperTrend'][i-1]==df['Lower Band'][i-1] and df['close'][i]>=df['Lower Band'][i]:
            df['SuperTrend'][i]=df['Lower Band'][i]
        elif df['SuperTrend'][i-1]==df['Lower Band'][i-1] and df['close'][i]<=df['Lower Band'][i]:
            df['SuperTrend'][i]=df['Upper Band'][i]
    df = df.dropna()
    return df

#Renko Calculation
def Renko(df0, brickSize):
    df0["uptrend"] = 0
    df0["bar_num"] = 0
    #cannot change dataframe while iterating through it, so new dataframe is created which stores valid renko bricks.
    df = pd.DataFrame()
    #converts standard ohlc price data to renko price data
    df0["close"].iloc[0] = brickSize * math.floor(df0["close"].iloc[0]/brickSize)
    df = df.append(df0.loc[0], ignore_index = True) #convert first element in dataframe
    for i in range(len(df0["close"])):
        if i > 0:
            #If price is more than 1 bricksize > current brick, add new brick
            if df0["close"].iloc[i] > (df["close"].iloc[-1] + brickSize):
                df0["close"].iloc[i] = brickSize * math.floor(df0["close"].iloc[i]/brickSize)
                df = df.append(df0.loc[i], ignore_index = True)
            #If price is less than 1 bricksize < current brick, add new brick
            elif df0["close"].iloc[i] < (df["close"].iloc[-1] - (brickSize*2)):
                df0["close"].iloc[i] = brickSize * math.ceil(df0["close"].iloc[i]/brickSize)# + brickSize #plus brickSize because if bar[i] = 143 and price = 140.7, next bar should be 142 so add one then round up.
                df = df.append(df0.loc[i], ignore_index = True)
    #calculating open, high, and low
    duplicates = []
    for i in range(len(df["close"])):
        df["high"].iloc[i] = df["close"].iloc[i]
        df["low"].iloc[i] = df["close"].iloc[i] - brickSize
        df["open"].iloc[i] = df["close"].iloc[i] - brickSize
        if df["close"].iloc[i] == df["close"].iloc[i-1]:
             duplicates.append(i)
    #removing duplicates
    for i in duplicates:
        df.drop(i, inplace = True)
    #resetting index
    df.reset_index(drop = True, inplace = True) #reset index
    #adding extra numbers in between
    df2 = pd.DataFrame()
    for i in range(len(df["close"])):
        if i > 0:
            #adds the original, uncleaned, renko data
            #calculates the difference between two numbers to check if its greater than one renko bar
            missingNum = abs(((df["close"].iloc[i] - df["close"].iloc[i-1]))/brickSize)
            #if the difference between two numbers is > 1 renko bar this fills in the gaps
            if df["close"].iloc[i] < (df["close"].iloc[i-1] - brickSize):
                difference = brickSize
                #If the gap to be filled is 4, it appends the number and increments it by the bar num 4 times
                for j in range(int(missingNum - 1)):
                    df2 = df2.append(df.loc[i-1] - difference, ignore_index = True)
                    difference += brickSize
                df2 = df2.append(df.loc[i], ignore_index = True)
            elif df["close"].iloc[i] > (df["close"].iloc[i-1] + brickSize):
                difference = brickSize
                for j in range(int(missingNum - 1)):
                    df2 = df2.append(df.loc[i-1] + difference, ignore_index = True)
                    difference += brickSize
                df2 = df2.append(df.loc[i], ignore_index = True)
            #Adds data if there were no gaps between numbers
            else:
                df2 = df2.append(df.loc[i], ignore_index = True)
    #calculates uptrend
    for i in range(len(df2["close"])):
        if df2["close"].iloc[i] < df2["close"].iloc[i-1]:
            df2["uptrend"].iloc[i] = False
            df2["bar_num"].iloc[i] = -1
        elif df2["close"].iloc[i] > df2["close"].iloc[i-1]:
            df2["uptrend"].iloc[i] = True
            df2["bar_num"].iloc[i] = 1
    #calculates bar number
    for i in range(len(df2["bar_num"])):
        if df2["bar_num"].iloc[i] < 0 and df2["bar_num"].iloc[i-1] < 0:
            df2["bar_num"].iloc[i] += df2["bar_num"].iloc[i-1]
        #Adds negative bars when price increases by brickSize
        elif df2["bar_num"].iloc[i] > 0 and df2["bar_num"].iloc[i-1] > 0:
            df2["bar_num"].iloc[i] += df2["bar_num"].iloc[i-1]
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    return df2

#Backtesting
#Taking user input for backtest settings
ticker = input(str("Enter ticker (ex: BTCUSDT):\n>> "))
interval = input(str("Enter chart interval (ex: 1m, 1h, 1d):\n>> "))
start = input(str("Enter start time (ex: 1 week ago):\n>> "))
brickSize = float(input("Enter renko brick size:\n>> "))
atr_multiplyer = int(input("Enter ATR multiplyer (Ex: '4'):\n>> "))
st_periods = int(input("Enter time-periods for Supertrend (Ex: '7'):\n>> "))
funds = float(input("How much money would you like to start with?\n>> "))

#Create Renko/Supertrend dataframe
df0 = getData(ticker, interval, start)
renko_df = Renko(df0, brickSize)
st_df = SuperTrend(renko_df, atr_multiplyer, st_periods)

#Creating Signal column
st_df.reset_index(drop = True, inplace = True) #reset index
st_df.drop(["high", "low", "H-L", "H-PC", "L-PC", "TR", "ATR", "Upper Basic", "Lower Basic", "Upper Band", "Lower Band"], axis = 1, inplace = True)
st_df["Signal"] = 0
for i in range(len(st_df["close"])):
    if st_df["SuperTrend"].iloc[i] < st_df["close"].iloc[i]:
        st_df["Signal"].iloc[i] = 1
    elif st_df["SuperTrend"].iloc[i] > st_df["close"].iloc[i]:
        st_df["Signal"].iloc[i] = -1

starting_funds = funds
last_trade = 0

#Calculates return
for i in range(len(st_df["close"])):
    current_price = st_df["close"].iloc[i]
    if i > 1:
        #buy signal
        if st_df["Signal"].iloc[i] == 1 and st_df["Signal"].iloc[i-1] == -1:
            if last_trade > 0:
                profit = (last_trade - current_price)/last_trade
                funds -= (funds * 0.002) #Simulates fees
                funds += (funds * profit)
            print(funds)
            print("long at: ", current_price)
            last_trade = current_price
        #sell signal
        elif st_df["Signal"].iloc[i] == -1 and st_df["Signal"].iloc[i-1] == 1:
            if last_trade > 0:
                profit = (current_price - last_trade)/last_trade
                funds -= (funds * 0.002)
                funds += (funds * profit)
            print(funds)
            print("short at:", current_price)
            last_trade = current_price

#Returns performance data
print("Ending funds: ", round(funds, 5))
print("Percent return: ", round((((funds-starting_funds)/starting_funds)*100), 5))

#Plots strategy
plt.style.use('seaborn-darkgrid')
plt.figure(figsize=(10,5))
plt.plot(st_df["SuperTrend"])
#Plotting Renko Bars
for i in range(len(st_df["close"])):
    if st_df["uptrend"].iloc[i] == True:
        plt.gca().add_patch(Rectangle((i, st_df["close"].iloc[i]), 1, brickSize, facecolor='forestgreen')) #edgecolor = black
    elif st_df["uptrend"].iloc[i] == False:
        plt.gca().add_patch(Rectangle((i, st_df["close"].iloc[i]), 1, brickSize, facecolor='red'))
#Labeling graph
plt.xlabel("bars")
plt.ylabel("close (p)")
plt.show()
