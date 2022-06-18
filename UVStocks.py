from tkinter import *
# from tkinter import ttk
from PIL import ImageTk, Image


def command(f, *args, **kwargs):
    """allows passing of arguments when binding functions to tkinter buttons"""
    return lambda: f(*args, **kwargs)


class SplashScreen:
    def __init__(self, master):

        self.splash_screen_frame = Frame(master) # this solution sucks
        self.splash_screen_frame.pack()

        # logo (didn't use frame, just packed it into master)
        path = "images/uvstocksSplashLogo.png"
        pil_img = Image.open(path).resize((600, 675))
        tk_img = ImageTk.PhotoImage(pil_img)
        logo_label = Label(self.splash_screen_frame, image=tk_img)
        logo_label.pack()
        logo_label.photo = tk_img

        # frame for buttons to start game and display leaderboard
        btn_title_frame = Frame(self.splash_screen_frame)
        btn_title_frame.pack()

        titleB1 = Button(master=btn_title_frame, text="play", padx=50, pady=20, command=self.name_prompt)
        titleB1.pack(side=LEFT) #, padx=50)

        titleB2 = Button(master=btn_title_frame, text="leaderboard", padx=25, pady=20, command=self.show_high_scores)
        titleB2.pack(side=RIGHT) #, padx=50)

    def name_prompt(self):
        prompt = NamePromptWindow()

    def show_high_scores(self):
        # THIS FUNCTION JUST TESTS DESTROYING THE FRAME FOR NOW
        self.splash_screen_frame.destroy()
        pass

class NamePromptWindow(Toplevel):
    def __init__(self, master = None):

        super().__init__(master = master)

        # main name prompt frame, acts as master for this separate window
        name_prompt_frame = Frame(self)
        name_prompt_frame.pack()

        np_label = Label(name_prompt_frame, text="input name", fg="black", font="Arial 15").pack()
        np_entry = Entry(name_prompt_frame, bg="white", fg="black", width=25, font="Arial 15")
        np_entry.pack() # have to do this unfortunately

        np_button = Button(name_prompt_frame, text="submit", fg="black", font="Arial 15", 
                            command=lambda: print(np_entry.get())).pack()


class GameWindow:
    def __init__(self, master):
        pass

class LeaderBoard:
    def __init__(self, master):
        pass

master = Tk()

def quit_me():  # define quit behavior
    print('quit')
    master.quit()
    master.destroy()

master.protocol("WM_DELETE_WINDOW", quit_me)
master.title("UVStocks")
master.geometry("770x750")

window1 = SplashScreen(master)
master.mainloop()