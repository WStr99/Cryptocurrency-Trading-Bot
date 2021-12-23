from DataReader import DataReader
from binance.client import Client
from binance.enums import *

class Trader:

    def __init__(self):
        self.client = Client('Binance API Keys') #Private API Keys
        self.ticker = 'BTCUSDT'
        self.quantity = 0
        #self.amount

    def setTicker(self, ticker):
        self.ticker = ticker

    def setQuantity(self, quantity):
        self.quantity = quantity

    #Margin buy
    def marginBuy(self):
        order = client.create_margin_order(
        symbol = self.ticker,
        side = SIDE_BUY,
        type = MARKET,
        quantity = self.quantity,
        price = '')

    #Margin sell
    def marginSell(self):
        order = client.create_margin_order(
        symbol = self.ticker,
        side = SIDE_BUY,
        type = MARKET,
        quantity = self.quantity,
        price = '')
