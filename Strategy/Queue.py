import pandas as pd
class Queue:

    def __init__(self, df):
        self.df = df
        self.temp = []

    #Inserts element in front of queue  #if last 2 == current 2
    def enqueue(self, newBricks, brickSize):
        self.df = pd.concat([self.df, newBricks], ignore_index = True)
        #remove last element from queue
        if len(self.df["close"]) > 300: #keeps Queue from getting too large
            self.dequeue()

    def dequeue(self):
        self.df.drop(labels = 0, axis = 0, inplace = True)
        self.df.reset_index(drop = True, inplace = True) #reset index

    #Returns the first element in the queue without removing it
    def peek(self):
        return self.df.iloc[-1]

    #Returns dataframe inside queue
    def peekFull(self): #not a traditional queue function
        df = self.df.copy()
        return df

    #Returns size of dataframe
    def size(self):
        return self.df.shape

    #Checks if queue is empty
    def isEmpty(self):
        return len(self.df) == 0
