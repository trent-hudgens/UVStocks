def buy(wallet_amount, stock_data, entryVal, stocks_owned):
    try:
        total = stock_data * entryVal
        if total > wallet_amount:
            return 1, wallet_amount, stocks_owned

        else:
            updatedWallet = wallet_amount - total
            updatedStocks = stocks_owned + 1
            return 0, updatedWallet, updatedStocks
    except:
        return print("Something went wrong try again")


def sell(stock_data):
    '''
    TODO JOSUE/KYLER/DAVID: use this to build your buy/sell functions. For now it just prints the current stock price.
    the first argument must be stock_data, an instantiation of the StockData class.
    '''
    print("You sold x amount of stock")
    # return lambda : None

# def buy(currPrice, buyStocks, wallet, numStocks):
#     '''placeholder for button commands.'''
#     try : 
#         checkNum = float(buyStocks)
#         checkPrice = float(currPrice)
#         total = checkPrice * checkNum
#         if total > wallet:
#             return print("Not suficient founds")
#         else:
#             return wallet - total, numStocks + buyStocks

#     except:
#         return print("Something went wrong try again")

# def sell(currPrice, sellStocks, wallet, numStocks):
#     '''placeholder for button commands.'''
#     try :
#         if sellStocks < numStocks:
#             return print("You don't possess enough shares to execute this action" )

#         checkNum = float(sellStocks)
#         checkPrice = float(currPrice)
#         total = checkPrice * checkNum
#         if total > wallet:
#             return print("Not suficient founds")
#         else:
#             return wallet + total, numStocks - sellStocks
