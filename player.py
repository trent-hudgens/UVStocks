import copy
import csv
import os


class Player:
    def __init__(self, stock, name=None, wallet=5000, stocks_held=0, score=None):

        # maybe not have Player have a stock.... don't know what to do here
        self.stock = stock
        self.wallet = wallet
        self.name = name
        self.stocks_held = stocks_held
        self.score = copy.copy(wallet)  # this is sus

    def buy(self, get_input, no_funds):
        try:
            desired_stocks = int(get_input())
            if desired_stocks < 0:
                no_funds.config(text="You can only use positive numbers")
            else:
                if self.check_funds(desired_stocks):
                    self.wallet -= (desired_stocks * self.stock.stock_price)
                    self.stocks_held += desired_stocks
                    no_funds.config(text="")  # TODO MAYBE DO ALL THE NO_FUNDS STUFF WITHIN check_funds?

                    self.record_action("Buy", desired_stocks)
                    self.update_leaderboards()
                else:
                    print("You can't afford to buy that many stocks.")
                    no_funds.config(text="Insufficent Funds")
                    return no_funds
        except ValueError:
            no_funds.config(text="You can only use numbers")

    def sell(self, get_input, no_funds):
        try:
            desired_stocks = int(get_input())
            if desired_stocks < 0:
                no_funds.config(text="You can only use positive numbers")
            else:
                if desired_stocks <= self.stocks_held:
                    self.wallet += (desired_stocks * self.stock.stock_price)
                    no_funds.config(text="")
                    self.stocks_held -= desired_stocks

                    self.record_action("Sell", desired_stocks)
                    self.update_leaderboards()

                else:
                    print("You are trying to sell too many stocks.")
                    no_funds.config(text="Insufficent Stock Amount")
        except ValueError:
            no_funds.config(text="You can only use numbers")

    def check_funds(self, desired_stocks):
        stock_price = self.stock.get_price()
        return (desired_stocks * stock_price) < self.wallet

    def calc_score(self):
        # maybe do this within the updater in UVStocks.py..... TODO Decide what to do
        self.score = self.wallet + (self.stock.get_price() * self.stocks_held)
        return round(self.score)  # SCORE IS ALWAYS A WHOLE NUMBER?????? ASK CUSTOMER ABOUT THIS

    def record_action(self, action, desired_stocks):
        """updates the user record csv file with their latest validated buy/sell action."""
        # headers: ['Action', 'Score', 'Wallet', 'Current Stock Price', 'Stocks bought']
        score = self.calc_score()
        wallet = round(self.wallet, 2)
        price = round(self.stock.get_price(), 2)
        headers = [action, score, wallet, price, desired_stocks]

        # append new action to 
        with open(f'Records/records_of_{self.name}.csv', 'a', newline='')as file:  # MAYBE 'w'
            write_in_file = csv.writer(file)
            write_in_file.writerow(headers)

    def update_leaderboards(self):
        """updates the leaderboards with the user's last score."""

        # create leaderboard csv if it doesn't already exist
        header = ['Name', 'Score']
        if not os.path.exists('leaderboards.csv'):
            with open('leaderboards.csv', 'w', newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                for i in reversed(range(0, 10)):
                    csv_writer.writerow(("BLANK", int(0)))

        # create list of tuples that represent leaderboard
        with open("leaderboards.csv", 'r') as readerObj:
            next(readerObj)
            csv_reader = csv.reader(readerObj)
            tuplesList = list(map(tuple, csv_reader))

            user_leaderboard_entry = (str(self.name), str(round(self.score, 2)))
            [tuplesList.pop(tuplesList.index(entry)) for entry in tuplesList if entry[0] == user_leaderboard_entry[0]]
            tuplesList.append(user_leaderboard_entry)

            sortedTuples = sorted(tuplesList, key=lambda x: x[1])
            readerObj.close()

        # write new leaderboard
        with open("leaderboards.csv", 'w', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            for i in range(0, len(sortedTuples)):
                writer.writerow(sortedTuples[i])
