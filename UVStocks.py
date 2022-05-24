from tkinter import *
from PIL import ImageTk, Image  


def dummy():
    '''placeholder for button commands.'''
    pass


def main():

    # Initialize + configure the main window
    root = Tk()
    root.title("UVStocks")
    # root.configure(bg="green",)


    # Build and place the logo frame
    logo_frm = Frame(root)

    img = Image.open("UVStocks_logo.png")
    img = img.resize((200, 50)) # Resize image
    UVlogo = ImageTk.PhotoImage(img)
    Label(logo_frm, image=UVlogo).pack()

    logo_frm.pack()

    cash_shares_frm = Frame(root)
    Label(cash_shares_frm, text="Total Cash: xxx", fg="black", anchor="w").pack(side=LEFT, padx=50)
    Label(cash_shares_frm, text="Total Shares Held: xxx", fg="black", anchor="e").pack(side=RIGHT, padx=50)
    cash_shares_frm.pack()

    # Build and place the stock graph frame (dummy for now)
    graph_frm = Frame(root)

    img = Image.open("dummy_graph.png")
    dummy_graph = ImageTk.PhotoImage(img)
    Label(graph_frm, image=dummy_graph).pack()

    graph_frm.pack()


    # Build and place the buy/sell buttons frame
    btn_frm = Frame(root)

    b1 = Button(master=btn_frm, text="Buy", padx=50, pady=10, command=dummy)
    b1.pack(side=LEFT, padx=50)
    b2 = Button(master=btn_frm, text="Sell", padx=50, pady=10, command=dummy)
    b2.pack(side=RIGHT, padx=50)

    btn_frm.pack()

    #entry field for amount of stocks to buy or sell
    input_amount_frm = Frame(root)
    inputAmount = Entry(input_amount_frm, bg="white", fg="black", width=100)
    inputAmount.pack(side=LEFT)
    inputAmount.insert(0, "Amount")
    def clickInput(*args):
        amountStr = str(inputAmount.get())
        if amountStr == "Amount":
            inputAmount.delete(0, 'end')
    def focusOutInput(*args):
        amountStr = str(inputAmount.get())
        if amountStr == "":
            inputAmount.insert(0, "Amount")
            root.focus()
    inputAmount.bind("<Button-1>", clickInput)
    inputAmount.bind("<FocusOut>", focusOutInput)
    input_amount_frm.pack()

    score_frm = Frame(root)
    Label(score_frm, text="SCORE: XXXXX.XX", fg="black", anchor="w").pack(side=LEFT)
    score_frm.pack()


    root.mainloop()


if __name__ == "__main__":
    main()
