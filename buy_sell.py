# as it stands the current buy ssell stuff only works when in the same module. this will be fixed when jared 
# and i implement the class for stock price stuff etc

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