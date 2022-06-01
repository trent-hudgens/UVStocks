from tkinter import *
from PIL import ImageTk, Image  
import stock_generator as stgen
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def dummy():
    '''placeholder for button commands.'''

    #the following code is used to clear and then restore the default value, "amount", to the inputAmount entry
    #it should be run when buy or sell is clicked
    #note: inputAmount is defined after this which may cause issues
    #amountStr = str(inputAmount.get())
    #if amountStr == "":
        #inputAmount.insert(0, "Amount")
        #root.focus()

    pass


def main():

    # Initialize + configure the main window
    root = Tk()
    root.title("UVStocks")
    # root.configure(bg="green",)


    # Build and place the logo frame
    logo_frm = Frame(root)
    logo_frm.pack()

    img = Image.open("UVStocks_logo.png")
    img = img.resize((200, 50)) # Resize image
    UVlogo = ImageTk.PhotoImage(img)
    Label(logo_frm, image=UVlogo).pack()


    # build and place the labels for cash and shares held
    cash_shares_frm = Frame(root)
    Label(cash_shares_frm, text="Total Cash: xxx", fg="black", anchor="w").pack(side=LEFT, padx=50)
    Label(cash_shares_frm, text="Total Shares Held: xxx", fg="black", anchor="e").pack(side=RIGHT, padx=50)
    cash_shares_frm.pack()


    # Build and place the stock graph frame
    graph_frm = Frame(root)
    graph_frm.pack()

    fig = Figure(figsize = (5, 5), dpi = 100)

    xs = []
    ys = []
    data = stgen.stock_history(100)

    fig, ax = plt.subplots()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    def animate(i, xs, ys, data, ax):
        '''animate function to be called repeatedly to update the graph'''
        CURR_STOCK_PRICE = round(next(data), 2)
        ys.append(CURR_STOCK_PRICE)
        print(CURR_STOCK_PRICE)
        ys = ys[-25:] # only show the last 25 values

        ax.clear()
        # ax.set_ylim(700,1300) # configuration of the graph goes here
        ax.plot(ys)

    ani = FuncAnimation(fig, animate, fargs=(xs, ys, data, ax), interval=500) # change to 1000


    # Build and place the buy/sell buttons frame
    btn_frm = Frame(root)
    btn_frm.pack()

    b1 = Button(master=btn_frm, text="Buy", padx=50, pady=10, command=dummy)
    b1.pack(side=LEFT, padx=50)
    b2 = Button(master=btn_frm, text="Sell", padx=50, pady=10, command=dummy)
    b2.pack(side=RIGHT, padx=50)


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
