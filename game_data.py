"""the game data including the stock data and others :)"""
from stock_generator import stock_history
import copy
import csv


class StockData:
    def __init__(self, history_size=500, start_price=500):
        self.stock_generator = stock_history(history_size, start_price)
        self.stock_price = next(self.stock_generator)

    def update_price(self):
        self.stock_price = next(self.stock_generator)

    def get_price(self):
        return self.stock_price


class Player:
    def __init__(self, stock, name="default-name", wallet=5000, stocks_held=0, score=None):

        # maybe not have Player have a stock.... don't know what to do here
        self.stock = stock

        self.name = name
        self.wallet = wallet
        self.stocks_held = stocks_held
        self.score = copy.copy(wallet) # this is sus

    def buy(self, get_input, no_funds):
        desired_stocks = get_input()
        if self.check_funds(desired_stocks):
            self.wallet -= (desired_stocks * self.stock.stock_price)
            self.stocks_held += desired_stocks
            no_funds.config(text="") # TODO MAYBE DO ALL THE NO_FUNDS STUFF WITHIN check_funds?

        else:
            print("You can't afford to buy that many stocks.")
            no_funds.config(text="Insufficent Funds")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
            return no_funds

    def sell(self, get_input, no_funds):
        desired_stocks = get_input()
        if desired_stocks <= self.stocks_held:
            self.wallet += (desired_stocks * self.stock.stock_price)
            self.stocks_held -= desired_stocks
            no_funds.config(text="")

        else:
            print("You are trying to sell too many stocks.")
            no_funds.config(text="Insufficent Stock Amount")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
            return int(1)

    def check_funds(self, desired_stocks):
        stock_price = self.stock.get_price()
        return (desired_stocks * stock_price) < self.wallet
    
    def calc_score(self):
        # maybe do this within the updater in UVStocks.py..... TODO Decide what to do
        self.score = self.wallet + (self.stock.get_price() * self.stocks_held)
        return self.score



