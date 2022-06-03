'''the game data including the stock data and others :)'''

from stock_generator import stock_history


class StockData:
    def __init__(self, history_size=500, start_price=1000):
        self.stock_generator = stock_history(history_size, start_price)
        self.stock_price = next(self.stock_generator)

    def update_price(self):
        self.stock_price = next(self.stock_generator)

    def get_price(self):
        return self.stock_price


if __name__ == "__main__":
    pass