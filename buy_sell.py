def buy(wallet_amount, stock_data, entry_val, stocks_owned):
    try:
        total = stock_data * entry_val
        if total > wallet_amount:
            return 1, wallet_amount, stocks_owned

        else:
            updatedWallet = wallet_amount - total
            updatedStocks = stocks_owned + entry_val
            return 0, updatedWallet, updatedStocks
    except:
        return print("Something went wrong try again")


# currently a copy of buy. about to fix it
def sell(wallet_amount, stock_data, entry_val, stocks_owned):
    try:
        total = stock_data * entry_val
        if stocks_owned < entry_val:
            print("not enough stocks")
            return 1, wallet_amount, stocks_owned
        else:
            updatedWallet = wallet_amount + total
            updatedStocks = stocks_owned - entry_val
            return 0, updatedWallet, updatedStocks
    except:
        return print("Something went wrong try again")
