from tkinter import *
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from game_data import Player, StockData


def command(f, *args, **kwargs):
    """allows passing of arguments when binding functions to tkinter buttons"""
    return lambda: f(*args, **kwargs)


def main():
    """main execution"""

    stock_data = StockData()
    player = Player(stock=stock_data)

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
    currentStockLabel = Label(cash_shares_frm, text="", fg="black", anchor="w")
    currentStockLabel.pack(side=LEFT)
    totalCash = Label(cash_shares_frm, text="", fg="black", anchor="w")
    totalCash.pack(side=LEFT, padx=50)
    totalStocks = Label(cash_shares_frm, text="", fg="black", anchor="e")
    totalStocks.pack(side=RIGHT, padx=50)
    cash_shares_frm.pack()

    # updater functions for cash, shares held, and current stock price
    def stockLabelUpdater(stock_price):
        currentStockLabel.config(text=f"Current Stock Price: {round(stock_price, 2)}")

    def numStocksLabelUpdater(amount_stocks):
        totalStocks.config(text=f"Number of Stocks Held: {round(int(amount_stocks), 2)}")

    def totalCashLabelUpdater(curr_cash_amount):
        totalCash.config(text=f"Total Cash: {round(float(curr_cash_amount), 2)}")


    # Build and place the stock graph frame
    graph_frm = Frame(root)
    graph_frm.pack()

    fig = Figure(figsize=(5, 5), dpi=100)

    xs = []  # x axis data, should be dates/times eventually. left empty for now.
    ys = []  # y axis data - will contain stock price values

    fig, ax = plt.subplots()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    numStocksLabelUpdater(str(player.stocks_held))
    totalCashLabelUpdater(str(player.wallet))

    def animate(i, x_axis, y_axis, axis): # i don't know why 'i' has to be supplied. ???
        """animate function to be called repeatedly to update the graph"""
        stock_data.update_price()
        # print(stock_data.stock_price)  # DEBUG. prints stock price every time it updates
        y_axis.append(stock_data.stock_price)

        axis.clear()
        y_axis = y_axis[-25:]  # only show the last 25 values
        # ax.set_ylim(700,1300) # configuration of the graph goes here
        axis.plot(y_axis)

        stockLabelUpdater(stock_data.stock_price)
        numStocksLabelUpdater(str(player.stocks_held))
        totalCashLabelUpdater(str(player.wallet))

    ani = FuncAnimation(fig, animate, fargs=(xs, ys, ax), interval=500)  # change to 1000

    # build and place a simple spacer between the graph and the purchase/sell amount entry box
    Label(text="", fg="black").pack()

    # entry field for amount of stocks to buy or sell
    input_amount_frm = Frame(root)
    input_amount_frm.pack()

    inputAmount = Entry(input_amount_frm, bg="white", fg="black", width=100)
    inputAmount.pack(side=LEFT)
    inputAmount.insert(0, "Amount")

    # function to grab number of stocks to buy/sell from user
    def getInput():
        amountStr = str(inputAmount.get())
        if amountStr == "Amount":
            inputAmount.delete(0, 'end')
            amountStr = 0
        return int(amountStr)

    # Build and place the no funds label when the user doesn't have enough money to buy a stock
    # TODO THIS ISNT WORKING RIGHT NOW. PLS FIX
    no_funds = Label(text="", fg="black")
    no_funds.pack()

    # Build and place the buy/sell buttons frame
    btn_frm = Frame(root)
    btn_frm.pack()

    b1 = Button(master=btn_frm, text="Buy", padx=50, pady=10, command=command(player.buy, getInput))
    b1.pack(side=LEFT, padx=50)

    b2 = Button(master=btn_frm, text="Sell", padx=50, pady=10, command=command(player.sell, getInput))
    b2.pack(side=RIGHT, padx=50)

    # TODO DO THIS THE RIGHT WAY, DONT USE FRAME AS SPACER
    # build and place a simple spacer between the buy and sell buttons and the score label
    Label(text="", fg="black").pack()

    # build and place the total score frame
    score_frm = Frame(root)
    Label(score_frm, text="SCORE: 0", fg="black", anchor="w", font=("Arial", 12)).pack(side=LEFT)

    score_frm.pack()

    # TODO DO THIS THE RIGHT WAY, DONT USE FRAME AS SPACER
    # build and place a simple spacer between the score label and the bottom of the page
    Label(text="", fg="black").pack()

    root.mainloop()


if __name__ == "__main__":
    main()
