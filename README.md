# Cryptocurrency-Trading-Bot
Bot programmed to automatically buy and sell cryptocurrencies.

The algorithm used by this bot is a simple technical trading strategy. Regular OHLC data is replaced by Renko brick data. The Supertrend indicator is then incorperated over the Renko data. This essentially makes the original Supertrend indicator more accurate, as the Renko chart cuts out much of the "noise" that one might see with a typical OHLC candlestick or line chart.  

Important:
- The Backtest runs with no issue. Use this program to test different settings
- Before running, make sure to include your unique Binance API Keys in both the DataReader and Trader classes.
- The Margin Trade/Sell methods are not fully functional. Review https://python-binance.readthedocs.io/en/latest/ to update the methods.

Known Issues:
1. Stop-Loss located in Signal.py does not trigger when the conditions should be met
2. At low Renko bar values, some bars will be missing
