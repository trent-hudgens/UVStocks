from tkinter import *
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from game_data import StockData
from buy_sell import buy, sell


def command(f, *args, **kwargs):
    """allows passing of arguments when binding functions to tkinter buttons"""
    return lambda: f(*args, **kwargs)


def main():
    """main execution"""

    stock_data = StockData()
    # Initialize + configure the main window
    root = Tk()

    def quit_me():  # define quit behavior
        print('quit')
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", quit_me)
    root.title("UVStocks")
    # root.configure(bg="green",)

    # Build and place the logo frame
    logo_frm = Frame(root)
    logo_frm.pack()

    img = Image.open("images/UVStocks-logo.png")
    img = img.resize((200, 50))  # Resize image
    UVlogo = ImageTk.PhotoImage(img)
    Label(logo_frm, image=UVlogo).pack()

    # build and place the labels for cash, shares held, and current stock price
    cash_shares_frm = Frame(root)
    totalCash = Label(cash_shares_frm, text="Total Cash: xxx", fg="black", anchor="w")
    totalCash.pack(side=LEFT, padx=50)
    currentStockLabel = Label(cash_shares_frm, text="Current Stock Price: ", fg="black", anchor="w")
    currentStockLabel.pack(side=LEFT)
    totalStocks = Label(cash_shares_frm, text="Total Shares Held: xxx", fg="black", anchor="e")
    totalStocks.pack(side=RIGHT, padx=50)
    cash_shares_frm.pack()

    # Build and place the stock graph frame
    graph_frm = Frame(root)
    graph_frm.pack()

    fig = Figure(figsize=(5, 5), dpi=100)

    xs = []  # x axis data, should be dates/times eventually. left empty for now. TODO
    ys = []  # y axis data - will contain stock price values

    fig, ax = plt.subplots()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    def labelStockUpdater(stock_price):
        currentStockLabel.config(text="Current Stock Price: ")
        currentStockLabel.config(text=currentStockLabel.cget('text') + stock_price)

    def labelValUpdater(curr_cash_amount, amount_stocks):
        totalCash.config(text="Total Cash: ")
        totalStocks.config(text="Total Stocks Held: ")
        totalCash.config(text=totalCash.cget('text') + curr_cash_amount)
        totalStocks.config(text=totalStocks.cget('text') + amount_stocks)

    labelValUpdater(str(wallet_amount), str(stocks_held))

    def animate(i, x_axis, y_axis, ax):
        """animate function to be called repeatedly to update the graph"""
        # global stock_data
        stock_data.update_price()  # UPDATES THE GLOBAL STOCK PRICE
        print(stock_data.stock_price)  # DEBUG. prints stock price every time it updates
        y_axis.append(stock_data.stock_price)

        ax.clear()
        y_axis = y_axis[-25:]  # only show the last 25 values
        # ax.set_ylim(700,1300) # configuration of the graph goes here
        ax.plot(y_axis)

        labelStockUpdater(str(round(stock_data.stock_price, 2)))

    ani = FuncAnimation(fig, animate, fargs=(xs, ys, ax), interval=500)  # change to 1000

    # build and place a simple spacer between the graph and the purchase/sell amount entry box
    Label(text="", fg="black").pack()

    # entry field for amount of stocks to buy or sell
    input_amount_frm = Frame(root)
    input_amount_frm.pack()

    inputAmount = Entry(input_amount_frm, bg="white", fg="black", width=100)
    inputAmount.pack(side=LEFT)
    inputAmount.insert(0, "Amount")

    def clickInput(*args):
        amountStr = str(inputAmount.get())
        if amountStr == "Amount":
            inputAmount.delete(0, 'end')
            return 0
        return int(amountStr)

    inputAmount.bind("<Button-1>", clickInput)

    # Build and place the no funds label when the user doesn't have enough money to buy a stock
    no_funds = Label(text="", fg="black")
    no_funds.pack()

    # Build and place the buy/sell buttons frame
    btn_frm = Frame(root)
    btn_frm.pack()

    def checkFunds(total_money, stocks_data, entry_val, stocks_owned, button_type):
        global wallet_amount
        global stocks_held
        fundsOrNoFunds, updatedWallet, updatedStocks = buy(wallet_amount, stocks_data, entry_val, stocks_owned)
        if button_type == 1:
            if fundsOrNoFunds == 1:
                no_funds.config(text="Insufficent Funds")
            else:
                no_funds.config(text="")
                wallet_amount = updatedWallet
                stocks_held = stocks_owned + entry_val
                labelValUpdater(str(round(wallet_amount, 2)), str(stocks_held))

        elif button_type == 2:
            print("You clicked the sell button")

        else:
            print("There was a problem please try again")

    b1 = Button(master=btn_frm, text="Buy", padx=50, pady=10, command=lambda: checkFunds(wallet_amount,
                                                                                         stock_data.stock_price,
                                                                                         clickInput(), stocks_held, 1))
    b1.pack(side=LEFT, padx=50)
    b2 = Button(master=btn_frm, text="Sell", padx=50, pady=10, command=command(sell, stock_data))
    b2.pack(side=RIGHT, padx=50)

    # build and place a simple spacer between the buy and sell buttons and the score label
    Label(text="", fg="black").pack()

    # build and place the total score frame
    score_frm = Frame(root)
    Label(score_frm, text="SCORE: 0", fg="black", anchor="w", font=("Arial", 12)).pack(side=LEFT)

    score_frm.pack()

    # build and place a simple spacer between the score label and the bottom of the page
    Label(text="", fg="black").pack()

    root.mainloop()


wallet_amount = 3000
stocks_held = 0

if __name__ == "__main__":
    main()
