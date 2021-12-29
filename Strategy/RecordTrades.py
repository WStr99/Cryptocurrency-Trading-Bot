import datetime
import smtplib
from email.message import EmailMessage

class RecordTrades:

    def __init__(self):
        self.fileName = "Record.txt"

    #Sends alerts when trade is executed
    def sendAlert(self, subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to
        user = "email to send alerts from"
        msg['from'] = user
        password = "application password"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()

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
        sendAlert("Trade Executed", "\nOpening long at: " + tradeOpen + " on: " + timeOpen, "email")
        sendAlert("Trade Executed", "\nOpening long at: " + tradeOpen + " on: " + timeOpen, "phone number")

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
        sendAlert("Trade Executed", "\nOpening short at: " + tradeOpen + " on: " + timeOpen, "email")
        sendAlert("Trade Executed", "\nOpening short at: " + tradeOpen + " on: " + timeOpen, "phone number")
