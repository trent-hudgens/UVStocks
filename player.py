import copy
import csv
# from os.path import exists


class Player:
    def __init__(self, stock, name=None, wallet=5000, stocks_held=0, score=None):

        # maybe not have Player have a stock.... don't know what to do here
        self.stock = stock
        self.wallet = wallet
        self.name = name
        self.stocks_held = stocks_held
        self.score = copy.copy(wallet)  # this is sus

    def buy(self, get_input, no_funds):
        desired_stocks = get_input()
        if self.check_funds(desired_stocks):
            self.wallet -= (desired_stocks * self.stock.stock_price)
            self.stocks_held += desired_stocks
            no_funds.config(text="")  # TODO MAYBE DO ALL THE NO_FUNDS STUFF WITHIN check_funds?
    
            self.record_action("Buy", desired_stocks)

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

            self.record_action("Sell", desired_stocks)

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
        return round(self.score) # SCORE IS ALWAYS A WHOLE NUMBER?????? ASK CUSTOMER ABOUT THIS
    
    def record_action(self, action, desired_stocks):
        '''updates the user record csv file with their latest validated buy/sell action.'''
        # headers: ['Action', 'Score', 'Wallet', 'Current Stock Price', 'Stocks bought']
        score = self.calc_score()
        wallet = round(self.wallet, 2)
        price = round(self.stock.get_price(), 2)
        headers = [action, score, wallet, price, desired_stocks]
        
        # append new action to 
        with open(f'Records/records_of_{self.name}.csv', 'a', newline='')as file: # MAYBE 'w'
            write_in_file = csv.writer(file)
            write_in_file.writerow(headers)