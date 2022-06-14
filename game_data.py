"""the game data including the stock data and others :)"""

from stock_generator import stock_history


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

    
    def buy(self, getInput):
        desired_stocks = getInput()
        if self.check_funds(desired_stocks):
            self.wallet -= (desired_stocks * self.stock.stock_price)
            self.stocks_held += desired_stocks
            # TODO RECALCULATE THE TOTAL SCORE
        else:
            print("You can't afford to buy that many stocks.")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
    
    def sell(self, getInput):
        desired_stocks = getInput()
        if desired_stocks <= self.stocks_held:
            self.wallet += (desired_stocks * self.stock.stock_price)
            self.stocks_held -= desired_stocks
            # TODO RECALCULATE THE TOTAL SCORE
        else:
            print("You are trying to sell too many stocks.")
            # TODO MORE ERROR CHECKING (NEGATIVE NUMBERS ETC)
    
    def check_funds(self, desired_stocks):
        stock_price = self.stock.get_price()
        return (desired_stocks * stock_price) < self.wallet