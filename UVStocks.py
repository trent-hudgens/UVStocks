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

def show_frame(frame):
    """raises the inputted frame to the top so it's visible"""
    frame.tkraise()


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
    root.geometry("700x750")

    #root.state("zoomed")#currently zoomed in to full screen because i dont have it working with a scalable window yet

    #page frames 
    title_frame = Frame(root)
    stock_frame = Frame(root)
    highscores_frame = Frame(root)

    #stacking page frames on top of each other
    for frame in (title_frame, stock_frame, highscores_frame):
        frame.place(x=0, y=0, width=700, height=750)

    show_frame(title_frame)

    title_logo_frm = Frame(title_frame)
    title_logo_frm.pack()

    title_logo_img = Image.open("images/uvstocksSplashLogo.png")
    title_logo_img = title_logo_img.resize((600, 675))  # Resize image
    title_UVlogo = ImageTk.PhotoImage(title_logo_img)
    Label(title_logo_frm, image=title_UVlogo).pack()


    #buttons to go to the game or the leaderboard
    btn_title_frame = Frame(title_frame)

    titleB1 = Button(master=btn_title_frame, text="play", padx=50, pady=20, command=command(show_frame, stock_frame))
    titleB1.pack(side=LEFT, padx=50)

    titleB2 = Button(master=btn_title_frame, text="leaderboard", padx=25, pady=20, command=command(show_frame, highscores_frame))
    titleB2.pack(side=RIGHT, padx=50)

    btn_title_frame.pack()


    # Build and place the logo frame
    logo_frm = Frame(stock_frame)
    logo_frm.pack()

    img = Image.open("images/UVStocks-logo.png")
    img = img.resize((200, 50))  # Resize image
    UVlogo = ImageTk.PhotoImage(img)
    Label(logo_frm, image=UVlogo).pack()

    # build and place the labels for cash, shares held, and current stock price
    cash_shares_frm = Frame(stock_frame)
    currentStockLabel = Label(cash_shares_frm, text="", fg="black", anchor="w", font="Arial 10 bold")
    currentStockLabel.pack(side=LEFT, padx=50, ipady=10)
    totalCash = Label(cash_shares_frm, text="", fg="black", anchor="w", font="Arial 10 bold")
    totalCash.pack(side=LEFT, padx=50)
    totalStocks = Label(cash_shares_frm, text="", fg="black", anchor="e", font="Arial 10 bold")
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
    graph_frm = Frame(stock_frame)
    graph_frm.pack()

    fig = Figure(figsize=(5, 5), dpi=100)

    xs = []  # x axis data, should be dates/times eventually. left empty for now.
    ys = []  # y axis data - will contain stock price values

    fig, ax = plt.subplots()

    canvas = FigureCanvasTkAgg(fig, master=stock_frame)
    canvas.get_tk_widget().pack()

    numStocksLabelUpdater(str(player.stocks_held))
    totalCashLabelUpdater(str(player.wallet))

    def animate(i, x_axis, y_axis, axis):  # i don't know why 'i' has to be supplied. ???
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
    input_amount_frm = Frame(stock_frame)
    input_amount_frm.pack()

    inputAmount = Entry(input_amount_frm, bg="white", fg="black", width=58, font="Arial 15")
    inputAmount.pack(side=LEFT)
    inputAmount.insert(0, "Amount")

    # function to grab number of stocks to buy/sell from user
    def getInput(*args):
        amountStr = str(inputAmount.get())
        if amountStr == "Amount":
            inputAmount.delete(0, 'end')
            amountStr = 0
        return int(amountStr)

    inputAmount.bind("<Button-1>", getInput)

    # Build and place the no funds label when the user doesn't have enough money to buy a stock
    no_funds = Label(text="", fg="black")
    no_funds.pack()

    # Build and place the buy/sell buttons frame
    btn_frm = Frame(stock_frame)
    btn_frm.pack()

    b1 = Button(master=btn_frm, text="Buy", padx=40, pady=10, fg="white", bg="#2e8bc0", font="Arial 14 bold",
                command=command(player.buy, getInput, no_funds))
    b1.pack(side=LEFT, padx=50, pady=10)

    b2 = Button(master=btn_frm, text="Sell", padx=40, pady=10, fg="white", bg="#2e8bc0", font="Arial 14 bold",
                command=command(player.sell, getInput, no_funds))
    b2.pack(side=RIGHT, padx=50, pady=10)

    # build and place the total score frame
    score_frm = Frame(stock_frame)
    Label(score_frm, text="SCORE: 0", fg="black", anchor="w", pady=10, font="Arial 14 bold").pack(side=LEFT)
    score_frm.pack()

    #title_frame.place(x=0, y=0, width=stock_frame.winfo_width(), height=stock_frame.winfo_height())
    #highscores_frame.place(x=0, y=0, width=stock_frame.winfo_width(), height=stock_frame.winfo_height())

    root.mainloop()


if __name__ == "__main__":
    main()
