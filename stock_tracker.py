# pylint: disable=too-many-instance-attributes
"""All the logic for Generating the stock and storing it's history"""

from itertools import islice
import statistics

INITIAL_VALUE = 1000
TOTAL_STOCKS = 1000


class NoStock(Exception):
    """exception raised when there isn't a stock"""


class StockTracker:
    """iterator that changes the stock price base on its supply and demand"""

    def __init__(
        self,
        initial_value=INITIAL_VALUE,
        total_stocks=TOTAL_STOCKS,
        initial_sell_count=TOTAL_STOCKS,
    ):
        self._price = initial_value
        self._total_stocks = total_stocks
        self._sell_count = initial_sell_count
        self._buy_count = 0

    def buy_stock(self, count: int) -> int:
        """buys as many stocks as specifies
        if there aren't that many stocks available
            - it returns the number of stocks bought
        """
        self._buy_count += count
        return count

    def sell_stock(self, count: int):
        """increases the number of stocks being sold by the number specified"""
        self._sell_count += count

    @property
    def price(self):
        """the current price of the stocks"""
        return self._price

    @property
    def sell_count(self):
        """the current number of stocks being sold right now"""
        return self._sell_count

    @property
    def buy_count(self):
        """the current number of stocks being bought right now"""
        return self._buy_count

    def __iter__(self):
        return self

    def __next__(self):
        return self._price


def main():
    """function to run if this is the file run"""
    stocks = StockTracker(100)
    history = list(islice(stocks, 1000))
    mean = statistics.mean(history)
    print(f"next history: {mean}")
    history = list(islice(stocks, 1000))
    mean = statistics.mean(history)
    print(f"next history: {mean}")


if __name__ == '__main__':
    main()
