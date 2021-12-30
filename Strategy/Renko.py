import pandas as pd
import numpy as np
import warnings
import math
warnings.filterwarnings('ignore')

class RenkoBars:

    def __init__(self):
        self.brickSize = 0

    def setBrickSize(self, brickSize):
        try:
            self.brickSize = float(brickSize)
        except ValueError:
            print("ERROR: RenkoBars.calculateRenko: Invalid value for Renko bars\n")

    def getBrickSize(self):
        return float(self.brickSize)

    #Renko calculation
    def calculateRenko(self, df0):
        #dropping date axis
        df0.drop("date", axis = 1, inplace = True)
        #If bricksize value is not a string
        if isinstance(self.brickSize, str) == False:
            df0["uptrend"] = 0
            df0["bar_num"] = 0
            #cannot change dataframe while iterating through it, so new dataframe is created which stores valid renko bricks.
            df = pd.DataFrame()
            #converts standard ohlc price data to renko price data
            df0["close"].iloc[0] = self.brickSize * round(df0["close"].iloc[0]/self.brickSize)
            df = df.append(df0.loc[0], ignore_index = True) #convert first element in dataframe
            for i in range(len(df0["close"])):
                if i > 0:
                    #If price is more than 1 bricksize > current brick, add new brick
                    if df0["close"].iloc[i] > (df["close"].iloc[-1] + self.brickSize):
                        df0["close"].iloc[i] = self.brickSize * math.floor(df0["close"].iloc[i]/self.brickSize)
                        df = df.append(df0.loc[i], ignore_index = True)
                    #If price is less than 1 bricksize < current brick, add new brick
                    elif df0["close"].iloc[i] < (df["close"].iloc[-1] - (self.brickSize*2)): #x2 brickSize because if bar[i] = 143 and price = 140.7, next bar should be 142 so add one then round up.
                        df0["close"].iloc[i] = self.brickSize * math.ceil(df0["close"].iloc[i]/self.brickSize)
                        df = df.append(df0.loc[i], ignore_index = True)

            #calculating open, high, and low
            duplicates = []
            for i in range(len(df["close"])):
                df["high"].iloc[i] = df["close"].iloc[i]
                df["low"].iloc[i] = df["close"].iloc[i] - self.brickSize
                df["open"].iloc[i] = df["close"].iloc[i] - self.brickSize
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
                    missingNum = abs(((df["close"].iloc[i] - df["close"].iloc[i-1]))/self.brickSize)
                    #if the difference between two numbers is > 1 renko bar this fills in the gaps
                    if df["close"].iloc[i] < (df["close"].iloc[i-1] - self.brickSize):
                        difference = self.brickSize
                        #If the gap to be filled is 4, it appends the number and increments it by the brick size 4 times
                        for j in range(int(missingNum - 1)):
                            df2 = df2.append(df.loc[i-1] - difference, ignore_index = True)
                            difference += self.brickSize
                        df2 = df2.append(df.loc[i], ignore_index = True)
                    elif df["close"].iloc[i] > (df["close"].iloc[i-1] + self.brickSize):
                        difference = self.brickSize
                        for j in range(int(missingNum - 1)):
                            df2 = df2.append(df.loc[i-1] + difference, ignore_index = True)
                            difference += self.brickSize
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
            return df2
        #error checking
        else:
            print("ERROR: RenkoBars.calculateRenko: Invalid value for Renko bars\n")

    #Adds new renko brick(s) to data.
    def addRenkoBrick(self, prevBrick, currentClose):
        #adding previous brick and current price to singtle dataframe
        df0 = pd.DataFrame()
        df0 = df0.append(prevBrick, ignore_index = True)
        df0 = df0.append(currentClose, ignore_index = True)

        #remove date column
        try:
            df0.drop("date", axis = 1, inplace = True)
        except KeyError:
            pass
        #set to true if the new price has moved enough to add a new renko brick
        addBar = False
        #cannot change dataframe while iterating through it, so new dataframe is created which stores valid renko bricks.
        df = pd.DataFrame()

        #converts standard ohlc price data to renko price data
        df = df.append(df0.loc[0], ignore_index = True) #convert first element in dataframe
        #if price is more than 1 bricksize > current brick, add new brick
        if df0["close"].iloc[1] > (df["close"].iloc[0] + self.brickSize):
            df0["close"].iloc[1] = self.brickSize * math.floor(df0["close"].iloc[1]/self.brickSize)
            df = df.append(df0.loc[1], ignore_index = True)
            addBar = True
        #if price is more than 1 bricksize < current brick, add new brick
        elif df0["close"].iloc[1] < (df["close"].iloc[0] - (self.brickSize * 2)): #x2 brickSize because if bar[i] = 143 and price = 140.7, next bar should be 142 so add one then round up.
            df0["close"].iloc[1] = self.brickSize * math.ceil(df0["close"].iloc[1]/self.brickSize)

            df = df.append(df0.loc[1], ignore_index = True)
            addBar = True
        else:
            addBar = False #if there is no new bar to add, end function

        if addBar == True:
            #calculating open, high, and low
            df["high"].iloc[1] = df["close"].iloc[1]
            df["low"].iloc[1] = df["close"].iloc[1] - self.brickSize
            df["open"].iloc[1] = df["close"].iloc[1] - self.brickSize

            #adding extra numbers in between
            df2 = pd.DataFrame()
            df2 = df2.append(df.loc[0], ignore_index = True)
            #adds the original, uncleaned, renko data
            #calculates the difference between two numbers to check if its greater than one renko bar
            missingNum = abs(((df["close"].iloc[1] - df["close"].iloc[0]))/self.brickSize)
            #if the difference between two numbers is > 1 renko bar this fills in the gaps
            if df["close"].iloc[1] < (df["close"].iloc[0] - self.brickSize):
                difference = self.brickSize
                #If the gap to be filled is 4, it appends the number and increments it by the brick size num 4 times
                for j in range(int(missingNum - 1)):
                    df2 = df2.append(df.loc[0] - difference, ignore_index = True)
                    difference += self.brickSize
                df2 = df2.append(df.loc[1], ignore_index = True)
            elif df["close"].iloc[1] > (df["close"].iloc[0] + self.brickSize):
                difference = self.brickSize
                for j in range(int(missingNum - 1)):
                    df2 = df2.append(df.loc[0] + difference, ignore_index = True)
                    difference += self.brickSize
                df2 = df2.append(df.loc[1], ignore_index = True)
            #Adds data if there were no gaps between numbers
            else:
                df2 = df2.append(df.loc[1], ignore_index = True)

            #calculates uptrend
            for i in range(len(df2["close"])):
                if i > 0:
                    if df2["close"].iloc[i] < df2["close"].iloc[i-1]:
                        df2["uptrend"].iloc[i] = False
                        df2["bar_num"].iloc[i] = -1
                    elif df2["close"].iloc[i] > df2["close"].iloc[i-1]:
                        df2["uptrend"].iloc[i] = True
                        df2["bar_num"].iloc[i] = 1

            #calculates bar number
            for i in range(len(df2["bar_num"])):
                if i > 0:
                    if df2["bar_num"].iloc[i] < 0 and df2["bar_num"].iloc[i-1] < 0:
                        df2["bar_num"].iloc[i] += df2["bar_num"].iloc[i-1]
                    #Adds negative bars when price increases by brickSize
                    elif df2["bar_num"].iloc[i] > 0 and df2["bar_num"].iloc[i-1] > 0:
                        df2["bar_num"].iloc[i] += df2["bar_num"].iloc[i-1]

            df2.drop(0, axis = 0 ,inplace = True)
            df2.reset_index(drop = True, inplace = True) #reset index
            #returns new renko brick(s)
            return df2

        #if no bricks are added, returns string "None"
        else:
            df["close"].iloc[0] = -1
            return df
