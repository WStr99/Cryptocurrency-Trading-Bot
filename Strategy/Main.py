import time
from DataReader import DataReader
from Supertrend import Supertrend
from Renko import RenkoBars
from Queue import Queue
from Signal import SignalScanner
from Trader import Trader
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#Main method
def main():

    #Retrives the most recent price data.
    def update(dataReader):
        try:
            dataReader.setStartTime("1 day ago") #shortens start-time to increase speed.
        except:
            print("ERROR: Interval cannot be larger than 1 day.")
        #returns the last column (most recent) of data. It will return the data every <x> seconds, which is how the queue updates.
        priceData = dataReader.getData()
        return priceData.iloc[-1]

    #instructional message to user
    print("--- Cryptocurrency Trading-bot ---\n")
    print("Type 'set' to set algorithm parameters\nType 'quit' to exit\n")

    #user choses to manually set parameters, use default parameters, or quit.
    control = True
    while control == True:
        userInput = input(str(">> ")) #prompts user for input.
        if userInput.lower() == "set":
            control = False
        elif userInput == "quit":
            return "Exiting Program......"
            exit()
        else:
            print("ERROR: Unrecognized command. Please try again.")

    #initializes objects to retrieve data, set parameters, and perform trades.
    dataReader = DataReader() #DataReader object to pull data from Binance.
    renko = RenkoBars() #Renko object to convert price data to renko bars.
    supertrend = Supertrend() #Supertrend object.
    trader = Trader() #Trader object to communicate with Bitfinex and perform trades.

    #prompts user in case they chose to manually set parameters.
    #prompts user for ticker that they want to trade with.
    ticker = input(str("Enter ticker: (Ex: 'BTCUSDT')\n>> "))
    dataReader.setTicker(ticker) #allows the user to pull data for the specific ticker they input.
    trader.setTicker(ticker) #tells the Trade class which ticker to trade with.
    trader.setQuantity(float(input("Enter amount you would you like to trade: (Ex: 0.05)\n>> "))) #sets the amount the user wants to trade with.
    dataReader.setInterval(input(str("Enter timeframe: (Ex: '1m, 1h, 1d')\n>> "))) #sets the interval time.
    dataReader.setStartTime(input("Enter start-time: (Ex: '1 week ago')\n>> ")) #sets the start time.
    renko.setBrickSize(input(str("Enter Renko Brick size: (Ex: '50')\n>> "))) #sets Renko brick size.
    supertrend.setMultiplyer(input(str("Enter ATR multiplyer: (Ex: '4')\n>> "))) #sets ATR multiplyer for Supertrend.
    supertrend.setPeriods(input(str("Enter time-periods for Supertrend: (Ex: '7')\n>> "))) #sets time period for Supertrend.
    trader.setAmount(float(input("Enter the amount you would like to trade: \n>> ")))

    #retrieves data and adds indicators now that parameters are set.
    priceData = dataReader.getData() #retreives data from Binance.
    renkoData = renko.calculateRenko(priceData) #converts data to renko.
    queue = Queue(renkoData) #converts data to queue.
    print("\n--- Strategy is Live ---")

    #scanner object to check if trade condition is met.
    scanner = SignalScanner(trader) #takes the trader object as a parameter in order to call trades from the scanner class.

    running = True
    while running == True:
        try:
            #retrieves most recent price data every <x> seconds.
            attempts = 0
            control = True
            #attempts to connect
            while control == True:
                if attempts < 200:
                    try:
                        #takes the current price & price of the last renko brick, converts current price to renko and adds are any missing bricks inbetween the two
                        prevBrick = queue.peek()
                        currentClose = update(dataReader)
                        newBricks = renko.addRenkoBrick(prevBrick, currentClose)
                        control = False
                    except KeyboardInterrupt:
                        queue.printToFile()
                        print("\n\nKeyboard exception received. Exiting.")
                        exit()
                    except:
                        #Throws connection error but attempts to connect again
                        time.sleep(5)
                        attempts += 1
                        print("Connection Error")
                        continue
                #if attempts exceed 200 (every 5 seconds), ends the program
                else:
                    print("Maximum number of connection attempts exceeded.")
                    # -- Close existing trade --
                    exit()

            #adds to queue if a new Renko brick(s) is formed.
            if newBricks["close"].iloc[0] != -1:# != "None":
                queue.enqueue(newBricks, renko.getBrickSize()) #takes in the renko object.
            #calculates indicators
            df = queue.peekFull()
            supertrend.calculateStupertrend(df)
            #plotting live renko data
            plt.style.use("seaborn-darkgrid")
            #plt.figure(figsize=(10,5))
            plt.plot(df["SuperTrend"], color = "royalblue", linewidth = 2) #also try color = tab:red
            for i in range(len(df["close"])):
                if df["uptrend"].iloc[i] == True:
                    plt.gca().add_patch(Rectangle((i, df["close"].iloc[i]-1), 1, renko.getBrickSize(), facecolor = 'forestgreen')) #edgecolor = black
                elif df["uptrend"].iloc[i] == False:
                    plt.gca().add_patch(Rectangle((i, df["close"].iloc[i]-1), 1, renko.getBrickSize(), facecolor = 'red'))
            plt.title(dataReader.getTicker())
            plt.xlabel("bars")
            plt.ylabel("price")
            plt.tight_layout()
            plt.draw()
            plt.pause(1)
            plt.clf()
            #scanner class scans data to check if trade condition is met.
            scanner.checkConditions(df, dataReader)
            time.sleep(60) #repeats once per minute
        except AttributeError:
            pass
        except KeyboardInterrupt:
            queue.printToFile()
            print("\n\nKeyboard exception received. Exiting.")
            exit()

if __name__ == "__main__":
    main()
