# pylint: disable=too-many-instance-attributes
"""All the logic for Generating the stock and storing it's history"""
INITIAL_VALUE = 1000
TOTAL_STOCKS = 1000
BASE_CHANGE = 100


class NoStock(Exception):
    """exception raised when there isn't a stock"""


class StockTracker:
    """iterator that changes the stock price base on its supply and demand"""

    def __init__(
        self,
        initial_value=INITIAL_VALUE,
        total_stocks=TOTAL_STOCKS,
        initial_sell_count=TOTAL_STOCKS,
        base_change=BASE_CHANGE,
    ):
        if total_stocks < initial_sell_count:
            raise NoStock
        self._price = initial_value
        self._total_stocks = total_stocks
        self._sell_count = initial_sell_count
        self._base_change = base_change
        self._future_sell_count = 0
        self._buy_count = 0

    def buy_stock(self, count: int) -> int:
        """buys as many stocks as specifies
        if there aren't that many stocks available
            - it returns the number of stocks bought
        """
        buy_count = min(self._buy_count + count, self._sell_count)
        ret = buy_count - self._buy_count
        self._buy_count = buy_count
        return ret

    def sell_stock(self, count: int) -> None:
        """increases the number of stocks being sold by the number specified"""
        self._future_sell_count += count
        if self._total_stocks < (self._sell_count + self._future_sell_count):
            raise NoStock

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

    def update_stock(self):
        """updates the stock information for one tick"""
        ratio = self._buy_count / self._sell_count
        # the ratio is between 0 and 1, so shift so half are below 0.5
        # when the ratio is low, it means the price goes down
        # when the ratio is high, it means the price goes up
        self._price += (ratio - .5) * self._base_change
        self._sell_count = self._future_sell_count + self._sell_count - self._buy_count


def main():
    """function to run if this is the file run"""


if __name__ == '__main__':
    main()
