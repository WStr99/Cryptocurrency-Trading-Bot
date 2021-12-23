import datetime

class RecordTrades:

    def __init__(self):
        self.fileName = "Results/Record.txt"

    #Records long
    def recordLong(self, currentPrice, df):
        record = open(self.fileName, "a")
        tradeOpen = str(currentPrice)
        timeOpen = str(datetime.datetime.now())
        record.write("Opening long at: ")
        record.write(tradeOpen)
        record.write(" on: ")
        record.write(timeOpen)
        record.write("\n")
        record.close()

    #Records short
    def recordShort(self, currentPrice, df):
        record = open(self.fileName, "a")
        tradeOpen = str(currentPrice)
        timeOpen = str(datetime.datetime.now())
        record.write("Opening short at: ")
        record.write(tradeOpen)
        record.write(" on: ")
        record.write(timeOpen)
        record.write("\n")
        record.close()

    #Records stop-long
    def recordStopLong(self, currentPrice):
        record = open(self.fileName, "a")
        tradeStop = str(currentPrice)
        timeStop = str(datetime.datetime.now())
        record.write("Stopping long at: ")
        record.write(tradeStop)
        record.write(" on: ")
        record.write(timeStop)
        record.write("\n")
        record.close()

    #Records stop-short
    def recordStopShort(self, currentPrice):
        record = open(self.fileName, "a")
        tradeStop = str(currentPrice)
        timeStop = str(datetime.datetime.now())
        record.write("Stopping short at: ")
        record.write(tradeStop)
        record.write(" on: ")
        record.write(timeStop)
        record.write("\n")
        record.close()
