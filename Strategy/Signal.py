from Queue import Queue
from DataReader import DataReader
from RecordTrades import RecordTrades
from DataReader import DataReader

class SignalScanner:

    def __init__(self, trade):
        self.position = ""
        self.priceEntered = 0
        self.numTrades = 0
        self.trade = trade

    #Adds a new column with past trade signals
    def addSignalCol(self, df): #Turn this into member variable
        df["Signal"] = 0
        for i in range(len(df["close"])):
            if df["SuperTrend"].iloc[i] < df["close"].iloc[i]: #and df["SuperTrend"].iloc[i-1] > df["close"].iloc[i-1]:
                df["Signal"].iloc[i] = 1
            elif df["SuperTrend"].iloc[i] > df["close"].iloc[i]:# and df["SuperTrend"].iloc[i-1] < df["close"].iloc[i-1]:
                df["Signal"].iloc[i] = -1

    #Returns most recet close price
    def getCurrentPrice(self, dataReader):
        try:
            dataReader.setStartTime("2 days ago") #shortens start-time to increase speed.
        except:
            print("ERROR: Interval cannot be larger than 1 day.")
        #returns the last column (most recent) of data. It will return the data every <x> seconds, which is how the queue updates.
        priceData = dataReader.getData()
        return priceData["close"].iloc[-1]

    #Checks if all conditions are met and calls the trade class to buy/sell
    def checkConditions(self, df, dataReader):
        recordTrade = RecordTrades()
        self.addSignalCol(df)
        signal = df["Signal"].iloc[-1]
        #checks for buy/sell conditions
        #buy or sell if there have been no previous numTrades
        if self.numTrades == 0:
            if signal == 1: #buy signal
                self.position = "Long" #saves new position
                self.trade.marginBuy() #calls trade class to communicate with exchange
                self.priceEntered = self.getCurrentPrice(dataReader) #saves price entered from trade
                recordTrade.recordLong(self.priceEntered, df) #records trade
                self.numTrades += 1
            elif signal == -1: #sell signal
                self.position = "Short"
                self.trade.marginSell()
                self.priceEntered = self.getCurrentPrice(dataReader)
                recordTrade.recordShort(self.priceEntered, df)
                self.numTrades += 1
        #if a previous trade has been made
        elif self.numTrades > 0:
            if self.position == "Short": #buy signal
                if signal == 1:
                    self.position = "Long"
                    self.trade.marginBuy() #executes twice to close previous position and open new one
                    self.trade.marginBuy()
                    self.priceEntered = self.getCurrentPrice(dataReader)
                    recordTrade.recordLong(self.priceEntered, df)
            elif self.position == "Long": #sell signal
                if signal == -1:
                    self.position = "Short"
                    self.trade.marginSell()
                    self.trade.marginSell()
                    self.priceEntered = self.getCurrentPrice(dataReader)
                    recordTrade.recordShort(self.priceEntered, df)
        #Stop/loss
        stopBuy = self.priceEntered + (self.priceEntered * 0.035)
        stopSell =  self.priceEntered - (self.priceEntered * 0.035)
        if self.numTrades > 0 and signal == -1 and self.getCurrentPrice(dataReader) > stopBuy: #when loss is greater than 1%
                if self.position == "Short":
                    self.trade.marginBuy()
                    self.trade.marginBuy()
                    recordTrade.recordStopLong(self.getCurrentPrice(dataReader))
        elif self.numTrades > 0 and signal == 1 and self.getCurrentPrice(dataReader) < stopSell:
                if self.position == "Long":
                    self.trade.marginSell()
                    self.trade.marginSell()
                    recordTrade.recordStopShort(self.getCurrentPrice(dataReader))
