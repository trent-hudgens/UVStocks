import player


def ai_generator(stock):
    NUMBER_SIMULATED_AI = 100
    ai_list = [player.AI(stock=stock) for _ in range(NUMBER_SIMULATED_AI)]

    while True:
        for ai in ai_list:
            # either buy or sell
            if stock.price > ai.wallet and ai.stocks_held > 0:
                ai.sell(ai.stocks_held)
            elif stock.price < ai.wallet and stock.buy_count > 0:
                ai.buy(1)
        yield
