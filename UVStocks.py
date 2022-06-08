from tkinter import *
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from game_data import StockData
from buy_sell import buy, sell


def command(f, *args, **kwargs):
    '''allows passing of arguments when binding functions to tkinter buttons'''
    return lambda: f(*args, **kwargs)


def main():
    '''main execution'''

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
    Label(cash_shares_frm, text="Total Cash: xxx", fg="black", anchor="w").pack(side=LEFT, padx=50)
    Label(cash_shares_frm, text="Total Shares Held: xxx", fg="black", anchor="e").pack(side=RIGHT, padx=50)
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

    def animate(i, xs, ys, ax):
        '''animate function to be called repeatedly to update the graph'''
        # global stock_data
        stock_data.update_price()  # UPDATES THE GLOBAL STOCK PRICE
        print(stock_data.stock_price)  ### DEBUG. prints stock price every time it updates

        ys.append(stock_data.stock_price)

        ax.clear()
        ys = ys[-25:]  # only show the last 25 values
        # ax.set_ylim(700,1300) # configuration of the graph goes here
        ax.plot(ys)

    ani = FuncAnimation(fig, animate, fargs=(xs, ys, ax), interval=500)  # change to 1000

    # Build and place the buy/sell buttons frame
    btn_frm = Frame(root)
    btn_frm.pack()

    b1 = Button(master=btn_frm, text="Buy", padx=50, pady=10, command=command(buy, stock_data))
    b1.pack(side=LEFT, padx=50)
    b2 = Button(master=btn_frm, text="Sell", padx=50, pady=10, command=command(sell, stock_data))
    b2.pack(side=RIGHT, padx=50)

    ani = FuncAnimation(fig, animate, fargs=(xs, ys, ax), interval=500)  # change to 1000

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

    inputAmount.bind("<Button-1>", clickInput)

    # build and place the total score frame
    score_frm = Frame(root)
    Label(score_frm, text="SCORE: XXXXX.XX", fg="black", anchor="w").pack(side=LEFT)
    score_frm.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
