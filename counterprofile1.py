from tkinter import *

class CounterProfile:
    def __init__(self, master, profile_title, counter = 0):


        self.master = master
        self.profile_title = profile_title
        self.counter = counter
        self.toplevel = None

    def __repr__(self):
        return ("Counter:" + self.profile_title)

    def __call__(self, master, profile_title):

        self.toplevel = Toplevel(master.root)

        self.button_up = Button(self.toplevel, text=self.counter, width = 10, command=self.count, font="none 50 bold")
        self.button_up.place(relx=0.5, rely=0.5, anchor=CENTER)

        button_minus = Button(self.toplevel, text="-", width = 4, command=self.minus, font="none 12 bold")
        button_minus.place(relx=1.0, rely=1.0, anchor=SE)

        self.toplevel.title(profile_title)
        self.toplevel.geometry('500x300')
        self.toplevel.configure(background="black")


    def change_button(self):
        self.button_up["text"] = self.counter

    def count(self):
        self.counter += 1
        self.change_button()
        self.master.update_profile_count(self.profile_title)

    def minus(self):
        self.counter -= 1
        self.change_button()
        self.master.update_profile_count(self.profile_title)





#window = Tk()

#window=Toplevel()
#profile = CounterProfile("First Profile", window)

#window.mainloop()
