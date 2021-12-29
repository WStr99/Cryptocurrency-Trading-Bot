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
            dataReader.setStartTime("1 day ago") #shortens start-time to increase speed.
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

        #if a previous trade has been made
        #Short position
        if self.position == "Short": #buy signal
            if signal == 1:
                self.position = "Long"
                if self.numTrades == 0: #only executes once if no previous trade
                    self.trade.marginBuy()
                elif self.numTrades > 0 :#executes twice to close previous position and open new one
                    self.trade.marginBuy()
                    self.trade.marginBuy()
                self.priceEntered = self.getCurrentPrice(dataReader)
                recordTrade.recordLong(self.priceEntered, df)
                self.numTrades += 1
        
        #Long position
        elif self.position == "Long": #sell signal
            if signal == -1:
                self.position = "Short"
                if self.numTrades == 0: #only executes once if no previous trade
                    self.trade.marginSell()
                elif self.numTrades > 0: #executes twice to close old position and open new one
                    self.trade.marginSell()
                    self.trade.marginSell()
                self.priceEntered = self.getCurrentPrice(dataReader)
                recordTrade.recordShort(self.priceEntered, df)
                self.numTrades += 1

        #Sets position if no trade has been executed yet
        #This is so program knows whether to look for a long or short
        if self.numTrades == 0:
            if signal == 1: #buy signal
                self.position = "Long" #saves new position
            elif signal == -1: #sell signal
                self.position = "Short"
