from tkinter import *
from PIL import ImageTk, Image
import csv
import os
import tkinter.ttk as ttk
import fnmatch

import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

from stockdata import StockData
from player import Player


def command(f, *args, **kwargs):
    """allows passing of arguments when binding functions to tkinter buttons"""
    return lambda: f(*args, **kwargs)


class GUI(Tk):
    """wrapper for the entire Tkinter game"""

    def __init__(self):
        Tk.__init__(self)  # the main GUI window is a Tk object

        self.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.title("UVStocks")
        # self.configure(bg="#282828") # ugly but it saves the eyes and also helps you see what your frames are
        self.geometry("800x800")

        self.create_leaderboard()

        # initialize stock data and player for the session
        # i don;t know if this is the best way
        self.stock_data = StockData()
        self.player = Player(stock=self.stock_data)

        # game switches to it's first frame, splashscreen
        self._frame = None
        self.switch_frame(SplashScreen)

    def quit_me(self):
        self.quit()
        self.destroy()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

        return self._frame
    
    def create_leaderboard(self):
        """create leaderboard csv if it doesn't already exist"""
        header = ['Name', 'Score']
        if not os.path.exists('leaderboards.csv'):
            with open('leaderboards.csv', 'w', newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(header)
                for i in reversed(range(0, 10)):
                    csvwriter.writerow(("BLANK", int(0)))


class SplashScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # logo
        path = "images/uvstocks-splash-logo.png"
        pil_img = Image.open(path).resize((600, 675))
        tk_img = ImageTk.PhotoImage(pil_img)
        self.logo_label = Label(self, image=tk_img)
        self.logo_label.pack()
        self.logo_label.photo = tk_img  # don't know why i have to do this

        # frame for buttons to start game and display leaderboard
        self.btn_title_frame = Frame(self)
        self.btn_title_frame.pack()

        self.titleB1 = Button(master=self.btn_title_frame, text="Play", font="Arial 14", padx=50, pady=20, 
                              command=self.open_name_prompt)
        self.titleB1.pack(side=LEFT, padx=50)

        self.titleB2 = Button(master=self.btn_title_frame, text="Leaderboard", font="Arial 14", padx=25, pady=20,
                              command=command(master.switch_frame, Leaderboard))
        self.titleB2.pack(side=RIGHT, padx=50)


    def open_name_prompt(self):
        # NamePromptWindow is an attribute of SplashScreen for now ???
        self.prompt = NamePromptWindow(self.master)


class NamePromptWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        # Place the popup window based on the width and height of the splash screen
        self.geometry(f'+{self.winfo_width()+ 399}+{self.winfo_height() + 374}') # TODO FINISH POPUP Window Calculations

        # Call function when we click on entry box
        def click(*args):
            self.np_entry.delete(0, 'end')

        # main name prompt frame, acts as master for this separate window
        self.name_prompt_frame = Frame(self)
        self.name_prompt_frame.pack(pady=3, padx=10)

        self.np_entry = Entry(self.name_prompt_frame, bg="white", fg="black", width=25, font="Arial 15",
                              justify='center')
        self.np_entry.pack(pady=6)
        self.np_entry.insert(0, "Input Name")
        self.np_entry.bind("<Button-1>", click)

        self.np_button = Button(self.name_prompt_frame, text="submit", fg="black", font="Arial 15",
                                command=command(self.submit, master))  # TODO ????? switch instead?
        self.np_button.pack(pady=7)

        self.grab_set()  # focuses onto this window, prevents interaction with the SplashScreen

    def submit(self, master):
        """
        creates a csv file with the player's name and switches to the game when the 
        'submit' button is pressed
        """
        player_name = self.np_entry.get()  # collect the user's name

        # create csv file
        headers = ['Action', 'Score', 'Wallet', 'Current Stock Price', 'Stocks bought']

        if not os.path.exists('Records'):
            os.mkdir('Records')

        with open(f'Records/records_of_{player_name}.csv', 'w', newline='')as file:
            write_in_file = csv.writer(file)
            write_in_file.writerow(headers)

        # switch frame to the Game and set the Game's Player name
        _frame = GUI.switch_frame(master, Game)
        _frame.player.name = player_name

        self.destroy()


class Game(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # initialize the game's stock data and player data
        # GUI houses both of these
        # TODO discuss and decide the best way to do this
        self.stock_data = master.stock_data
        self.player = master.player

        # back button
        self.np_button = Button(self, text="Leaderboard", font="Arial 14", command=command(master.switch_frame, Leaderboard))
        self.np_button.pack(side="top", padx=50, pady=20)

        # build and place the logo
        img = Image.open("images/uvstocks-logo.png")
        img = img.resize((200, 50))  # Resize image
        UVlogo = ImageTk.PhotoImage(img)
        logo_label = Label(self, image=UVlogo)
        logo_label.photo = UVlogo
        logo_label.pack()

        # build and place the labels for cash, shares held, and current stock price
        cash_shares_frm = Frame(self)
        cash_shares_frm.pack()

        self.currentStockLabel = Label(cash_shares_frm, text="", fg="black", anchor="w", font="Arial 10 bold")
        self.currentStockLabel.pack(side=LEFT, padx=50)  # , ipady=10)

        self.totalCashLabel = Label(cash_shares_frm, text="", fg="black", anchor="w", font="Arial 10 bold")
        self.totalCashLabel.pack(side=LEFT, padx=50)

        self.totalStocksLabel = Label(cash_shares_frm, text="", fg="black", anchor="e", font="Arial 10 bold")
        self.totalStocksLabel.pack(side=RIGHT, padx=50)

        # build and place the stock graph
        x_axis = []  # x axis data, should be dates/times eventually. left empty for now.
        y_axis = []  # y axis data - will contain stock price values

        fig, ax = plt.subplots()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack()

        # Call function when we click on entry box
        def click(*args):
            self.inputAmount.delete(0, 'end')

        def animate(i, x_axis, y_axis, axis):  # i don't know why 'i' has to be supplied. ???
            """animate function to be called repeatedly to update the graph"""
            self.stock_data.update_price()
            print(self.stock_data.stock_price)  ### DEBUG. prints stock price every time it updates
            y_axis.append(self.stock_data.stock_price)

            axis.clear()
            y_axis = y_axis[-25:]  # only show the last 25 values
            # ax.set_ylim(700,1300) # configuration of the graph goes here
            axis.plot(y_axis)

            self.update_all_labels()

        self.ani = FuncAnimation(fig, animate, fargs=(x_axis, y_axis, ax), interval=500)  # change to 1000

        # build and place the no funds label when the user doesn't have enough money to buy a stock
        no_funds = Label(self, text="", fg="black")
        no_funds.pack()

        # build and place the entry field for amount of stocks to buy or sell
        self.inputAmount = Entry(self, bg="white", fg="black", width=58, font="Arial 15")
        self.inputAmount.pack()
        self.inputAmount.insert(0, "Amount")
        self.inputAmount.bind("<Button-1>", click)

        # build and place the buy/sell buttons
        btn_frm = Frame(self)
        btn_frm.pack(side=BOTTOM)

        b1 = Button(master=btn_frm, text="Buy", padx=40, pady=10, fg="white", bg="#2e8bc0", font="Arial 14 bold",
                    command=command(self.player.buy, self.getInput, no_funds))
        b1.pack(side=LEFT, padx=50, pady=10)

        b2 = Button(master=btn_frm, text="Sell", padx=40, pady=10, fg="white", bg="#2e8bc0", font="Arial 14 bold",
                    command=command(self.player.sell, self.getInput, no_funds))
        b2.pack(side=RIGHT, padx=50, pady=10)

        # total score
        self.scoreLabel = Label(self, text="SCORE: ", fg="black", anchor="w", pady=10, font="Arial 14 bold")
        self.scoreLabel.pack()

    def update_all_labels(self):
        self.currentStockLabel.config(text=f"Current Stock Price: {round(self.stock_data.stock_price, 2)}")
        self.totalStocksLabel.config(text=f"Number of Stocks Held: {round(int(self.player.stocks_held), 2)}")
        self.totalCashLabel.config(text=f"Total Cash: {round(float(self.player.wallet), 2)}")
        self.scoreLabel.config(text=f"Net worth: {self.player.calc_score()}")

    def getInput(self):
        amountVal = self.inputAmount.get()
        return amountVal


class Leaderboard(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # logic that changes the command whether or not the game has been loaded yet
        # TODO rigorous testing of this bit of logic. 
        if True in [fnmatch.fnmatch(child, '!game*') for child in master.__dict__['children']]:
            cmd = command(master.switch_frame, Game)
            # print("WENT BACK TO GAME") ### DEBUG
        else:
            cmd = command(master.switch_frame, SplashScreen)
            # print("WENT BACK TO SPLASHCREEN") ### DEBUG

        # back button
        self.np_button = Button(self, text="Back", font="Arial 14", command=cmd)
        self.np_button.pack(side="top", padx=50, pady=20)

        header = ['Name', 'Score']
        Frame.configure(self) #, bg='black')
        Label(self, text="Leaderboard", font="Helvetica 20 bold").pack(side="top", fill="x", pady=3, padx=3)

        # Create a leaderboards file if player decides to check leaderboards before starting game
        header = ['Name', 'Score']
        if not os.path.exists('leaderboards.csv'):
            with open('leaderboards.csv', 'w', newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                for i in reversed(range(0, 10)):
                    csv_writer.writerow(("BLANK", int(0)))

        style = ttk.Style()
        style.configure("mystyle.Treeview.Heading", font="Arial 15 bold", rowheight=40)
        # TableMargin = Frame(self, width=1000)
        # TableMargin.pack(pady=3)
        tree = ttk.Treeview(self, columns=("Name", "Score"), height=15, style="mystyle.Treeview")
        tree.heading('Name', text="Name", anchor=CENTER)
        tree.heading('Score', text="Score", anchor=CENTER)
        tree.column('#0', stretch=NO, minwidth=0, width=0, anchor=CENTER)
        # tree.column('#1', stretch=NO, minwidth=0, width=300, anchor=CENTER)
        # tree.column('#2', stretch=NO, minwidth=0, width=300, anchor=CENTER)
        tree.pack(side="bottom", expand=True, fill='y')
        
        # TODO This bit of code needs to be ran every time you switch to the frame.
        # it might already be running this every time since the switch_frame() destroys the old one...... ??? 
        with open('leaderboards.csv', mode='r', newline='') as f:
            reader = csv.DictReader(f, delimiter=',')

            i=0
            for row in reader:
                name = row['Name']
                score = row['Score']
                tree.insert("", index=i, values=(name, score))
                i+=1


def main():
    gui = GUI()
    gui.mainloop()


if __name__ == "__main__":
    main()
