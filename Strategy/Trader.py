from DataReader import DataReader
from binance.client import Client
from binance.enums import *

class Trader:

    def __init__(self):
        self.client = Client('Binance API Keys') #Private API Keys
        self.ticker = 'BTCUSDT'
        self.quantity = 0

    #Sets the amount of a given coin that the user wants to trade
    def setAmount(self, amount):
        self.amount = amount
    
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
