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


    root.mainloop()


if __name__ == "__main__":
    main()
