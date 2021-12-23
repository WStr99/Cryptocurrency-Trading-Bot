import datetime
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
import warnings
warnings.filterwarnings('ignore')

class DataReader:

    def __init__(self):
        self.ticker = "BTCUSDT"
        self.interval = "4h"
        self.start = "1 week ago UTC"
        self.client = Client('Binance API Keys') #Private API Keys

    def setTicker(self, ticker):
        self.ticker = ticker

    def getTicker(self):
        return self.ticker

    def setInterval(self, interval):
        self.interval = interval

    def setStartTime(self, start):
        self.start = start

    #Fetches data from binance, cleasn data, and returns it in a pandas dataframe
    def getData(self):
        try:
            #getting data
            Coin = self.client.get_historical_klines(symbol = self.ticker, interval = self.interval, start_str = self.start) ###error here
            df = pd.DataFrame(data = Coin)
        except BinanceAPIException as e:
            print("ERROR: DataReader.getData:", e.message)
        except AttributeError as e:
            print("ERROR: DataReader.getData: Invalid start-time\n", e)
        else:
            try:
                #cleaning data
                df.columns = ["date", "open", "high", "low", "close", "volume", "close time", "quote", "trade", "1", "2", "3"] #renaming columns
                df.drop(["1","2","3","quote","trade","close time", "volume"],axis = 1,inplace = True) #dropping unnecessary columns
                df["open"]= df.open.astype(float)
                df["close"] = df.close.astype(float)
                df["low"] = df.low.astype(float)
                df["high"] = df.high.astype(float)
                for i in range(len(df["date"])):
                    df["date"].iloc[i] = datetime.datetime.fromtimestamp(df["date"].iloc[i]/1000)
                return df
            except ValueError:
                print("ERROR: DataReader.getData: Timeframe incompatible with start-time")
