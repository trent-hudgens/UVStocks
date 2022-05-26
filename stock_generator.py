"""All the logic for Generating the stock and storing it's history"""

from itertools import islice
from random import random
from statistics import NormalDist

STD_DEV = 10
INITIAL_VALUE = 1000

def calculate_stock_change(std_dev=STD_DEV):
    """randomly generates change in stock based on the provided std_dev

    Args:
        std_dev (float, optional): the Standard Deviation. Defaults to STD_DEV.

    Returns:
        float: the change in the stock value
    """
    distribution = NormalDist(0, std_dev)
    change = distribution.inv_cdf(random())
    return change


def stock_history(num_increments=60, stock_value=INITIAL_VALUE):
    """Generate stock history for the number of increments specified.
    (actually creates a generator)

    Args:
        num_seconds (int): the number of seconds to generate stock history for
        stock_value (float): the value of the stock at the start of the history

    Yields:
        float: the stock value after iteration
    """
    for _ in range(num_increments):
        yield stock_value
        stock_value += calculate_stock_change()


def infinite_stock_history(stock_value=INITIAL_VALUE):
    """Generates an infinite stock history

    Args:
        stock_value (float, optional): value of the stock at the start of the history.
            Defaults to INITIAL_VALUE.

    Yields:
        float: the stock value after each iteration
    """
    while True:
        yield stock_value
        stock_value += calculate_stock_change()

def stock_history_chunks(
    num_chunks = 60,
    chunk_size = 60,
    stock_value = INITIAL_VALUE,
):
    """Generates a Stock History using stock_history_in_secs

    Args:
        stock_value (float): initial value of the stock
        num_minutes (int, optional): number of minutes to generate the history for. Defaults to 60.
        chunk_size (int): the size of each chunk returned by the iterator

    Yields: list<int> | int
    """
    num_increments = num_chunks * chunk_size
    history = stock_history(num_increments, stock_value)
    for _ in range(0, num_chunks):
        yield list(islice(history, chunk_size))

def main():
    """function to run if this is the file run"""
    # you can use either of these in a loop like this:
    for chunk in stock_history_chunks(10, 5):
        print(f"chunk: {chunk}")
    # or this
    for (i, value) in enumerate(stock_history(10)):
        print(f"increment {i}: {value}")
    # you can also call next to get the next value
    history = stock_history(3)
    print(f"first {next(history)}")
    print(f"second {next(history)}")
    print(f"3rd {next(history)}")
    # if you call next to many times it will call a IterationStop error
    try:
        print(f"4th {next(history)}")
    except StopIteration:
        print("there isn't a 4th ")
    # to not have to deal with this you can use the infinite version
    history2 = infinite_stock_history()
    for _ in range(10000):
        next(history2)
    # but don't directly loop over it unless you break at some point, otherwise it will be infinite
    # you may also note that I didn't have to make a new stock_history()
        # call because the one above is still valid
    # you may need to run this a few times to see it list a lot if the stock ends to high
    for value in history2:
        print(f"value: {value}")
        if -500 > value or value > 2500:
            break # this is where I break out of the loop to prevent it from being infinite
    # you can use these with any of the iterator functions
    for int_value in map(int, stock_history(100)):
        print(f"int value: {int_value}")
    # if you want a list, just do it with list
    print(f"chunks: {list(stock_history_chunks(1000, 5, 10))}")


if __name__ == '__main__':
    main()
