'''the game data including the stock data and the user data'''

from stock_generator import stock_history


class StockData:
    def __init__(self, history_size=500, start_price=1000):
        self.stock_generator = stock_history(history_size, start_price)
        self.stock_price = next(self.stock_generator)

    def update_price(self):
        self.stock_price = next(self.stock_generator)

    def get_price(self):
        return self.stock_price

class UserData:
    def __init__(self, stock_data, name):
        self.name = name
        self.stock_data = stock_data

    def buy(self):
        '''TODO JOSUE/KYLER/DAVID: use this to build your buy/sell functions. For now it just prints the current stock price.'''
        print(f"{self.name} buys {self.stock_data.get_price()}")
        return lambda : None

    def sell(self):
        '''TODO JOSUE/KYLER/DAVID: use this to build your buy/sell functions. For now it just prints the current stock price.'''
        print(f"{self.name} sells {self.stock_data.get_price()}")
        return lambda : None


global_stock_data = StockData()

if __name__ == "__main__":
    user_1 = UserData(global_stock_data, "jared")
    user_2 = UserData(global_stock_data, "trent")

    for _ in range(10):
        user_1.sell()
        user_2.sell()
        global_stock_data.update_price()
