import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class Supertrend:

    def __init__(self):
        self.multiplyer = 0
        self.periods = 0

    def setMultiplyer(self, multiplyer):
        self.multiplyer = multiplyer

    def setPeriods(self, periods):
        self.periods = periods

    #Supertrend calculation
    def calculateStupertrend(self, df):
        try:
            #data will be string if input by the user
            self.multiplyer = int(self.multiplyer)
            self.periods = int(self.periods)
        except ValueError as e:
            print("ERROR: Supertrend.calculateStupertrend: Invalid time-period value\n", e)
        else:
            try:
                #calculation of ATR
                df['H-L'] = abs(df['high'] - df['low'])
                df['H-PC'] = abs(df['high'] - df['close'].shift(1))
                df['L-PC'] = abs(df['low'] - df['close'].shift(1))
                df['TR'] = df[['H-L','H-PC','L-PC']].max(axis = 1)
                df['ATR'] = np.nan
                df.loc[self.periods - 1, 'ATR'] = df['TR'][:self.periods-1].mean() #.ix is deprecated from pandas verion- 0.19
                for i in range(self.periods, len(df)):
                    df['ATR'].iloc[i] = (df['ATR'].iloc[i-1] * (self.periods-1) + df['TR'].iloc[i])/self.periods

                #calculation upper and lower bands
                df['Upper Basic'] = (df['high'] + df['low'])/2 + (self.multiplyer * df['ATR'])
                df['Lower Basic'] = (df['high'] + df['low'])/2 - (self.multiplyer * df['ATR'])
                df['Upper Band'] = df['Upper Basic']
                df['Lower Band'] = df['Lower Basic']

                #calculation of upper basic
                for i in range(self.periods, len(df)):
                    if df['close'].iloc[i-1] <= df['Upper Band'].iloc[i-1]:
                        df['Upper Band'].iloc[i] = min(df['Upper Basic'].iloc[i], df['Upper Band'].iloc[i-1])
                    else:
                        df['Upper Band'].iloc[i] = df['Upper Basic'].iloc[i]

                #calculation of lower basic
                for i in range(self.periods, len(df)):
                    if df['close'].iloc[i-1] >= df['Lower Band'].iloc[i-1]:
                        df['Lower Band'].iloc[i] = max(df['Lower Basic'].iloc[i], df['Lower Band'].iloc[i-1])
                    else:
                        df['Lower Band'].iloc[i] = df['Lower Basic'].iloc[i]
                df['SuperTrend'] = np.nan

                #sets past Supertend equal to upper/lower band when it crosses the close price
                for i in df['SuperTrend']:
                    if df['close'].iloc[self.periods-1] <= df['Upper Band'].iloc[self.periods-1]:
                        df['SuperTrend'].iloc[self.periods-1] = df['Upper Band'].iloc[self.periods-1]
                    elif df['close'].iloc[self.periods-1] > df['Upper Band'].iloc[i]:
                        df['SuperTrend'].iloc[self.periods-1] = df['Lower Band'].iloc[self.periods-1]

                #sets Supertend equal to upper/lower band when it crosses the close price
                for i in range(self.periods, len(df)):
                    if df['SuperTrend'].iloc[i-1] == df['Upper Band'].iloc[i-1] and df['close'].iloc[i] <= df['Upper Band'].iloc[i]:
                        df['SuperTrend'].iloc[i] = df['Upper Band'].iloc[i]
                    elif df['SuperTrend'].iloc[i-1] == df['Upper Band'].iloc[i-1] and df['close'].iloc[i] >= df['Upper Band'].iloc[i]:
                        df['SuperTrend'].iloc[i]=df['Lower Band'].iloc[i]
                    elif df['SuperTrend'].iloc[i-1] == df['Lower Band'].iloc[i-1] and df['close'].iloc[i] >= df['Lower Band'].iloc[i]:
                        df['SuperTrend'].iloc[i] = df['Lower Band'].iloc[i]
                    elif df['SuperTrend'].iloc[i-1] == df['Lower Band'].iloc[i-1] and df['close'].iloc[i] <= df['Lower Band'].iloc[i]:
                        df['SuperTrend'].iloc[i] = df['Upper Band'].iloc[i]

                #cleaning data
                df = df.dropna()
                df.drop(["H-L", "H-PC", "L-PC", "TR", "ATR", "Upper Basic", "Lower Basic", "Upper Band", "Lower Band"], axis = 1, inplace = True) #returns dataframe
                df.reset_index(drop = True, inplace = True)
                return df
            except IndexError as e:
                pass
                print("ERROR: Supertrend.calculateStupertrend: Parameter value(s) may exceed size of data\n", e)
