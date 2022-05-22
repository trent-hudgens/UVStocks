"""All the logic for Generating the stock and storing it's history"""

from itertools import islice


def stock_history_in_secs(num_seconds=60):
    """Generate stock history for the number of seconds specified.
    (actually creates a generator)

    Args:
        num_seconds (int): the number of seconds to generate stock history for

    Yields:
        int: the stock value at the specified second
    """
    second = 0
    while second < num_seconds:
        yield second
        second += 1


def stock_history_in_min(num_minutes = 60, flat = False):
    """Generates a Stock History using stock_history_in_secs

    Args:
        num_minutes (int, optional): number of minutes to generate the history for. Defaults to 60.
        flat (bool, optional): determines type of each iteration.
            flat=True: a list of 60 stock_history_in_secs iterations
            flat=False: individual stock_history_in_secs iteration
            (Defaults to False).

    Yields: list<int> | int
    """
    num_seconds = num_minutes * 60
    sec_history = stock_history_in_secs(num_seconds)
    if not flat:
        for _ in range(0, num_seconds, 60):
            yield list(islice(sec_history, 60))
    else:
        for i in sec_history:
            yield i


def main():
    """function to run if this is the file run"""
    minute_history = list(stock_history_in_min(30))
    print(f"list: {minute_history}, length: {len(minute_history)}")
    print(f"flat minutes: {list(stock_history_in_min(2, True))}")

if __name__ == '__main__':
    main()
