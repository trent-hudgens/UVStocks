from tkinter import *
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from game_data import Player, StockData



# TODO DIAGNOSE

# Exception in Tkinter callback
# Traceback (most recent call last):
#   File "C:\Users\Trent Hudgens\AppData\Local\Programs\Python\Python310\lib\tkinter\__init__.py", line 1921, in __call__
#     return self.func(*args)
# TypeError: command.<locals>.<lambda>() takes 0 positional arguments but 1 was given

def command(f, *args, **kwargs):
    """allows passing of arguments when binding functions to tkinter buttons"""
    return lambda: f(*args, **kwargs)

class GUI(Tk):
    '''wrapper for the entire Tkinter game'''
    def __init__(self):

        Tk.__init__(self) # the main GUI window is a Tk object
        self.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.title("UVStocks")
        self.geometry("770x750")

        # game switches to it's first frame, splashscreen
        self._frame = None
        self.switch_frame = self.switch_frame(SplashScreen)


    def quit_me(self):  # define quit behavior
        self.quit()
        self.destroy()
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class SplashScreen(Frame):
    def __init__(self, master):

        Frame.__init__(self, master)

        # logo
        path = "images/uvstocksSplashLogo.png"
        pil_img = Image.open(path).resize((600, 675))
        tk_img = ImageTk.PhotoImage(pil_img)
        self.logo_label = Label(self, image=tk_img)
        self.logo_label.pack()
        self.logo_label.photo = tk_img # don't know why i have to do this

        # frame for buttons to start game and display leaderboard
        self.btn_title_frame = Frame(self)
        self.btn_title_frame.pack()

        self.titleB1 = Button(master=self.btn_title_frame, text="Play", padx=50, pady=20, command=self.open_name_prompt)
        self.titleB1.pack(side=LEFT, padx=50)

        self.titleB2 = Button(master=self.btn_title_frame, text="Leaderboard", padx=25, pady=20, 
                              command=command(master.switch_frame, Leaderboard))
        self.titleB2.pack(side=RIGHT, padx=50)

    def open_name_prompt(self):
        # NamePromptWindow is an attribute of SplashScreen for now ???
        self.prompt = NamePromptWindow(self.master)


class NamePromptWindow(Toplevel):
    def __init__(self, master):

        Toplevel.__init__(self, master)

        # TODO MAKE THE WINDOW SPAWN NEAR THE SPLASH SCREEN WHEN IT'S CREATED

        # main name prompt frame, acts as master for this separate window
        self.name_prompt_frame = Frame(self)
        self.name_prompt_frame.pack()

        self.np_label = Label(self.name_prompt_frame, text="input name", fg="black", font="Arial 15")
        self.np_label.pack()

        self.np_entry = Entry(self.name_prompt_frame, bg="white", fg="black", width=25, font="Arial 15")
        self.np_entry.pack()

        self.np_button = Button(self.name_prompt_frame, text="submit", fg="black", font="Arial 15", 
                                command=command(self.submit, master)) # TODO ????? switch isnteaD?
        self.np_button.pack()

        self.grab_set() # focuses onto this window, prevents interaction with the SplashScreen

    def submit(self, master):
        self.entry_text = self.np_entry.get() # don't know if this is the best solution
        GUI.switch_frame(master, Game) # idk why but I have to use the GUI method explicitly instead of just doing master.switch_frame
        self.destroy()


class Game(Frame):
    def __init__(self, master):

        Frame.__init__(self, master)

        # initialize the game's stock data and player data. the way this works
        # is subject to change, not sure if this is the best thing
        self.stock_data = StockData()
        self.player = Player(stock=self.stock_data) # TODO PASS IN PLAYER NAME FROM NAMEPROMPTWINDOW

        # build and place the logo
        img = Image.open("images/UVStocks-logo.png")
        img = img.resize((200, 50))  # Resize image
        UVlogo = ImageTk.PhotoImage(img)
        logo_label = Label(self, image=UVlogo)
        logo_label.photo = UVlogo
        logo_label.pack()

        # build and place the labels for cash, shares held, and current stock price
        cash_shares_frm = Frame(self)
        cash_shares_frm.pack()

        self.currentStockLabel = Label(cash_shares_frm, text="", fg="black", anchor="w", font="Arial 10 bold")
        self.currentStockLabel.pack(side=LEFT, padx=50) #, ipady=10)

        self.totalCash = Label(cash_shares_frm, text="", fg="black", anchor="w", font="Arial 10 bold")
        self.totalCash.pack(side=LEFT, padx=50)

        self.totalStocks = Label(cash_shares_frm, text="", fg="black", anchor="e", font="Arial 10 bold")
        self.totalStocks.pack(side=RIGHT, padx=50)

        # build and place the stock graph
        x_axis = []  # x axis data, should be dates/times eventually. left empty for now.
        y_axis = []  # y axis data - will contain stock price values

        fig, ax = plt.subplots()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack()

        def animate(i, x_axis, y_axis, axis):  # i don't know why 'i' has to be supplied. ???
            """animate function to be called repeatedly to update the graph"""
            self.stock_data.update_price()
            # print(self.stock_data.stock_price)  # DEBUG. prints stock price every time it updates
            y_axis.append(self.stock_data.stock_price)

            axis.clear()
            y_axis = y_axis[-25:]  # only show the last 25 values
            # ax.set_ylim(700,1300) # configuration of the graph goes here
            axis.plot(y_axis)

            self.stockLabelUpdater(self.stock_data.stock_price)
            self.numStocksLabelUpdater(str(self.player.stocks_held))
            self.totalCashLabelUpdater(str(self.player.wallet))
            self.scoreLabelUpdater(self.player.score)

        self.ani = FuncAnimation(fig, animate, fargs=(x_axis, y_axis, ax), interval=500)  # change to 1000

        # build and place the no funds label when the user doesn't have enough money to buy a stock
        no_funds = Label(self, text="", fg="black")
        no_funds.pack()

        # build and place the entry field for amount of stocks to buy or sell
        self.inputAmount = Entry(self, bg="white", fg="black", width=58, font="Arial 15")
        self.inputAmount.pack()
        self.inputAmount.insert(0, "Amount")
        self.inputAmount.bind("<Button-1>", command(self.getInput))

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

    # TODO seems like there is a better solution to having four separate updaters...
    def stockLabelUpdater(self, stock_price):
        self.currentStockLabel.config(text=f"Current Stock Price: {round(stock_price, 2)}")

    def numStocksLabelUpdater(self, stocks):
        self.totalStocks.config(text=f"Number of Stocks Held: {round(int(stocks), 2)}")

    def totalCashLabelUpdater(self, curr_cash_amount):
        self.totalCash.config(text=f"Total Cash: {round(float(curr_cash_amount), 2)}")

    def scoreLabelUpdater(self, score):
        score = self.player.update_score(self.player, self.stock_data.stock_price)
        self.scoreLabel.config(text=f"Net worth: {round(float(score))}") # TODO figure out naming. Net worth makes the most sense to me

    def getInput(self):
        # function to grab number of stocks to buy/sell from user
        # TODO this should be generic, and should just return the text inside the box when called,
        # not just for the num stocks sell/buy feature.
        amountStr = str(self.inputAmount.get())
        if amountStr == "Amount":
            self.inputAmount.delete(0, 'end')
            amountStr = 0
        return int(amountStr)


class Leaderboard(Frame):
    def __init__(self, master):

        Frame.__init__(self, master)

        # TODO TODO TODO COMPLETE LEADERBOARD
        # currently is just a label with some placeholder text
        Frame.configure(self,bg='blue')
        Label(self, text="Leaderboard", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)


def main():

    gui = GUI()
    gui.mainloop()

if __name__ == "__main__":
    main()
