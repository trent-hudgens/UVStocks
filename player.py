import copy
import csv
import os

from stock_tracker import StockTracker

class BasePlayer:
    def __init__(self, stock, wallet=5000, name=None, stocks_held=0):
        # maybe not have Player have a stock.... don't know what to do here
        self.stock = stock
        self.wallet = wallet
        self.name = name
        self.stocks_held = stocks_held
        self.score = copy.copy(wallet)  # this is sus
    
    def buy(self):
        pass
    def sell(self):
        pass

class AI(BasePlayer):
    '''stripped down version of Player - no need to validate input, add score to leaderboard, etc'''
    def buy(self, desired_stocks):
        # buy the stock
        self.wallet -= (desired_stocks * self.stock.price)
        self.stocks_held += desired_stocks
        self.stock.buy_stock(desired_stocks)

    def sell(self, desired_stocks):
        self.wallet += (desired_stocks * self.stock.price)
        self.stocks_held -= desired_stocks
        self.stock.sell_stock(desired_stocks)

class Player(BasePlayer):
    def buy(self, get_input, no_funds):

        desired_stocks = self.check_valid_input(get_input, no_funds)

        if desired_stocks == None:
            return
        elif not self.check_funds(desired_stocks):
            print("You can't afford to buy that many stocks.")
            no_funds.config(text="Insufficent Funds")
            return
        elif desired_stocks > self.stock.sell_count: # TODO JARED 
            print("There aren't enough stocks for sale on the market right now.")
            no_funds.config(text="There aren't enough stocks for sale on the market right now.")
            return

        # buy the stock
        self.wallet -= (desired_stocks * self.stock.price)
        self.stocks_held += desired_stocks

        self.record_action("Buy", desired_stocks)
        self.update_leaderboards()
        self.stock.buy_stock(desired_stocks)

        no_funds.config(text="")  # TODO MAYBE DO ALL THE NO_FUNDS STUFF WITHIN check_funds?

    def sell(self, get_input, no_funds):

        desired_stocks = self.check_valid_input(get_input, no_funds)

        if desired_stocks == None:
            return
        elif desired_stocks > self.stocks_held:
            print("You are trying to sell too many stocks.")
            no_funds.config(text="Insufficent Stock Amount")
            return

        # sell the stock
        self.wallet += (desired_stocks * self.stock.price)
        self.stocks_held -= desired_stocks

        self.record_action("Sell", desired_stocks)
        self.update_leaderboards()
        self.stock.sell_stock(desired_stocks)

        no_funds.config(text="")

    def check_valid_input(self, get_input, no_funds):
        try:
            desired_stocks = int(get_input())
        except ValueError:
            no_funds.config(text="You can only use numbers")
            return

        if desired_stocks < 0:
            no_funds.config(text="You can only use positive numbers")
        
        return desired_stocks

    def check_funds(self, desired_stocks):
        price = self.stock.price
        return (desired_stocks * price) < self.wallet

    def calc_score(self):
        # maybe do this within the updater in UVStocks.py..... TODO Decide what to do
        self.score = self.wallet + (self.stock.price * self.stocks_held)
        return round(self.score)  # SCORE IS ALWAYS A WHOLE NUMBER?????? ASK CUSTOMER ABOUT THIS

    def record_action(self, action, desired_stocks):
        """updates the user record csv file with their latest validated buy/sell action."""
        # headers: ['Action', 'Score', 'Wallet', 'Current Stock Price', 'Stocks bought']
        score = self.calc_score()
        wallet = round(self.wallet, 2)
        price = round(self.stock.price, 2)
        headers = [action, score, wallet, price, desired_stocks]

        # append new action to 
        with open(f'Records/records_of_{self.name}.csv', 'a', newline='')as file:  # MAYBE 'w'
            write_in_file = csv.writer(file)
            write_in_file.writerow(headers)

    def update_leaderboards(self):
        """updates the leaderboards with the user's last score."""

        # create list of tuples that represent leaderboard
        # add the current user's latest score to the list
        with open("leaderboards.csv", 'r') as readerObj:
            next(readerObj)
            csv_reader = csv.reader(readerObj)
            tuplesList = list(map(tuple, csv_reader))

            user_leaderboard_entry = (str(self.name), str(round(self.score)))
            [tuplesList.pop(tuplesList.index(entry)) for entry in tuplesList if entry[0] == user_leaderboard_entry[0]]
            tuplesList.append(user_leaderboard_entry)

            sortedTuples = sorted(tuplesList, key=lambda x: x[1], reverse=True)
            readerObj.close()

        # write new leaderboard
        header = ['Name', 'Score']
        with open("leaderboards.csv", 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            for i in range(0, len(sortedTuples)):
                csvwriter.writerow(sortedTuples[i])
