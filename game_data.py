"""the game data including the stock data and others :)"""
from stock_generator import stock_history
import copy
import csv
from os.path import exists


class StockData:
    def __init__(self, history_size=500, start_price=500):
        self.stock_generator = stock_history(history_size, start_price)
        self.stock_price = next(self.stock_generator)

    def update_price(self):
        self.stock_price = next(self.stock_generator)

    def get_price(self):
        return self.stock_price


class Player:
    def __init__(self, stock, name="Default", wallet=5000, stocks_held=0, score=None):

        # maybe not have Player have a stock.... don't know what to do here
        self.stock = stock
        self.wallet = wallet
        self.name = name
        self.stocks_held = stocks_held
        self.score = copy.copy(wallet)  # this is sus
        print(name)
        self.records = self.check_records(name)

    def setName(self, player_name):
        self.name = player_name

    def buy(self, get_input, no_funds):
        desired_stocks = get_input()
        if self.check_funds(desired_stocks):
            self.wallet -= (desired_stocks * self.stock.stock_price)
            self.stocks_held += desired_stocks
            no_funds.config(text="")  # TODO MAYBE DO ALL THE NO_FUNDS STUFF WITHIN check_funds?
            self.update_score_record(self.name, desired_stocks, self.stock.stock_price, 'Buy')

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
            self.update_score_record(self.name, desired_stocks, self.stock.stock_price, 'Sell')

        else:
            print("You are trying to sell too many stocks.")
            no_funds.config(text="Insufficent Stock Amount")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
            return int(1)

    def check_funds(self, desired_stocks):
        stock_price = self.stock.get_price()
        return (desired_stocks * stock_price) < self.wallet

    # def calc_score(self):
    #     # maybe do this within the updater in UVStocks.py..... TODO Decide what to do
    #     self.score = self.wallet + (self.stock.get_price() * self.stocks_held)
    #     return self.score

    def update_score_record(self, player, desire_stocks, stock_price, action):
        """This method append (in his/her records) the transaction made"""
        price = stock_price
        stocks_buyed = desire_stocks
        wallet = self.get_wallet()
        score = self.get_score()
        if wallet > score:
            score = wallet
        information = [score, price, stocks_buyed, wallet, action]
        with open(f'Records/records_of_{player}.csv', 'a', newline='') as file:
        # append to CSV file
            writer_obj = csv.writer(file)
            writer_obj.writerow(information)

    def update_score(self, player, current_price):
        with open(f'Records/records_of_{player.name}.csv', 'r')as file:
            lines = file.readlines()
            wallet = lines[-1].split(',')[-2]
            acumulative = 0
            if player.stocks_held > 0:
                index = 0
                for i in (range(player.stocks_held, 0, -1)) :
                    price = lines[-player.stocks_held + index].strip().split(',')[1]
                    amount_of_stocks = lines[-player.stocks_held + index].strip().split(',')[2]
                    acumulative += float(price) * float(amount_of_stocks)
                    index += 1
                market_price = player.stocks_held * current_price + player.wallet
                current_power = (float(wallet) + acumulative)
                
                if market_price > current_power:
                    adjustmet = market_price - current_power
                    player.score = current_power - adjustmet 
                else:
                    adjustmet = market_price - current_power
                    player.score = current_power + adjustmet
            else: 
                return player.wallet 
            return player.get_score()

    def created_records(self, player):
        """
        This method created the header of a csv file, the name of the file contain the name of the player.
        """
        header = ['Score' , 'Price', 'Stocks buyed', 'Wallet', 'Action']
        with open(f'Records/records_of_{player}.csv', 'w', newline='')as file:
            # created a CSV file
            write_in_file = csv.writer(file)
            # write the header
            write_in_file.writerow(header)

    def get_score(self):
        return self.score
    
    def get_wallet(self):
        return self.wallet

    def check_records(self, name):
        file_exists = exists(f"/Records/records_of_{name}.csv")
        if file_exists is False:
            self.records = self.created_records(name)
            


