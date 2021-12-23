# Cryptocurrency-Trading-Bot
 Cryptocurrency Trading Bot

The algorithm used by this program is a simple technical trading strategy. Regular OHLC data is replaced by Renko brick data. The Supertrend indicator is then incorporated over the Renko data. This essentially makes the original Supertrend indicator more accurate, as the Renko chart cuts out much of the "noise" that one might see with a typical OHLC candlestick or line chart.  

Once running, the program will prompt the user for their desired settings or allow them to chose pre-set default settings. The program will then output a live chart based on those setting parameters. The program will immediately enter a trade once run. The program will then output all trades to the Records.txt file, located in the Strategy folder. In this current state, all trades are Margin trades. This program should be in a position at all times, once the program closes a long position it will immediately enter a short position.

Use the Backtest program to test different settings. The lower the interval time, the more accurate the backtest will be to the algorithm's actual performance.

Important:
- This program will trade indefinitely. Once a trade is entered, the only way to stop trading is to terminate the program and close the position on the exchange website.
- Before running, make sure to include your unique Binance API Keys in both the DataReader and Trader classes.
- The Margin Buy/Sell methods are not fully functional. Review https://python-binance.readthedocs.io/en/latest/ to update the methods.

Known Issues:
1. Stop-Loss located in Signal.py does not trigger when the conditions should be met.
2. At low Renko bar values, some bars might be missing.

References:
- A portion of the Supertrend class was taken from a post on Stackoverflow.com which has since been deleted and I am unable to find the original creator. If you are able to find them, please message me.
