"""the game data including the stock data and others :)"""https://github.com/trent-hudgens/UVStocks/pull/16/conflict?name=game_data.py&ancestor_oid=aee5b76859a784ae7612b9822c79a64af6fed18e&base_oid=b0b84f3a2a9dd0dcbcd9ac56addefd705f1e6d60&head_oid=1f83dab3dff896172016a7c922a3726cf10a4384

from stock_generator import stock_history
import csv


class StockData:
    def __init__(self, history_size=500, start_price=1000):
        self.stock_generator = stock_history(history_size, start_price)
        self.stock_price = next(self.stock_generator)

    def update_price(self):
        self.stock_price = next(self.stock_generator)

    def get_price(self):
        return self.stock_price


class Player:
    def __init__(self, stock, name="defaultname", wallet=3000, stocks_held=0, score=3000):


        # maybe not have Player have a stock.... don't know what to do here
        self.stock = stock

        self.name = name
        self.wallet = wallet
        self.stocks_held = stocks_held
        self.score = score

        records = self.created_records(self.name)

    def buy(self, get_input):
        desired_stocks = get_input()
        if self.check_funds(desired_stocks):
            self.wallet -= (desired_stocks * self.stock.stock_price)
            self.stocks_held += desired_stocks
            # TODO RECALCULATE THE TOTAL SCORE
            self.update_score_record(self.name, desired_stocks, self.stock.stock_price, 'Buy')
        else:
            print("You can't afford to buy that many stocks.")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
    
    def sell(self, getInput):
        desired_stocks = getInput()
        else:
            print("You can't afford to buy that many stocks.")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)

    def sell(self, get_input):
        desired_stocks = get_input()
        Buy-Sell-Functionality-KD
        if desired_stocks <= self.stocks_held:
            self.wallet += (desired_stocks * self.stock.stock_price)
            self.stocks_held -= desired_stocks
            # TODO RECALCULATE THE TOTAL SCORE

            self.update_score_record(self.name, desired_stocks, self.stock.stock_price, 'Sell')
        else:
            print("You are trying to sell too many stocks.")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
    
    def check_funds(self, desired_stocks):
        stock_price = self.stock.get_price()
        return (desired_stocks * stock_price) < self.wallet

    def update_score_record(self, player, desire_stocks, stock_price, action):
        price = stock_price
        stocks_buyed = desire_stocks
        wallet = self.wallet
        # Todo update score or 
        score = wallet + (price * stocks_buyed)
        information = [score, price, stocks_buyed, wallet, action]
        with open(f'Buy_records_of_{player}.csv', 'a', newline='') as file:
        # writing the CSV file
            writer_obj = csv.writer(file)
            writer_obj.writerow(information)
            # file.write(information)

    def update_score(self, player, current_price):
        with open(f'Buy_records_of_{player.name}.csv', 'r')as file:
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
        header = ['Score' , 'Price', 'Stocks buyed', 'Wallet', 'Action']
        with open(f'Buy_records_of_{player}.csv', 'w', newline='')as file:
            # created a CSV file
            write_in_file = csv.writer(file)
            # write the header
            write_in_file.writerow(header)

    def get_score(self):
        return self.score
        

        else:
            print("You are trying to sell too many stocks.")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)

    def check_funds(self, desired_stocks):
        stock_price = self.stock.get_price()
        return (desired_stocks * stock_price) < self.wallet
