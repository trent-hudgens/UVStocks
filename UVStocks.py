from tkinter import *
from PIL import ImageTk, Image  
import stock_generator as sg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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



    cash_shares_frm = Frame(root)
    Label(cash_shares_frm, text="Total Cash: xxx", fg="black", anchor="w").pack(side=LEFT, padx=50)
    Label(cash_shares_frm, text="Total Shares Held: xxx", fg="black", anchor="e").pack(side=RIGHT, padx=50)
    cash_shares_frm.pack()

    # Build and place the stock graph frame #####################
    graph_frm = Frame(root)
    graph_frm.pack()

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5), dpi = 100)
    
    # subplot
    plot = fig.add_subplot(111)

    # test function for matplotlib
    y = list(sg.stock_history(100)) #[i**2 for i in range(101)] ### TESTING

    # plot the function
    plot.plot(y)

    canvas = FigureCanvasTkAgg(fig, master=root)

    canvas.draw()

    canvas.get_tk_widget().pack()

    # dummy img
    # img = Image.open("dummy_graph.png")
    # dummy_graph = ImageTk.PhotoImage(img)
    # Label(graph_frm, image=dummy_graph).pack()


########################################################################

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
