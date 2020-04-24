from tkinter import *

class ProfileFrame:

    def __init__(self, master, title):

        self.master = master
        self.title = title

        self.frame = Frame(master.frame_just_count, bd=3, relief=RAISED)
        self.frame.pack(side=TOP, fill=X)

        self.label = Label(self.frame, text=(self.title + "    " + str(master.profile_dict[self.title])), font="none 11 bold")
        self.label.pack(side=LEFT)

        open = Button(self.frame, text="Open", width= 10, command=self.call_profile_wrap)
        open.pack(side=RIGHT, pady=5, padx=5)

        delete = Button(self.frame, text="Delete", width= 10, command=self.sure)
        delete.pack(side=RIGHT, pady=5, padx=5)

    def change_frame(self):
        self.label.configure(text = self.title + "    " + str(self.master.profile_dict[self.title]))

    def call_profile_wrap(self):
        try:
            self.master.profiles[self.title].toplevel.destroy()
        except AttributeError:
            pass

        self.master.call_profile(self.title)

    def sure(self):
        self.sure = Toplevel(self.master.root)
        self.sure.title("Delete?")
        self.sure.geometry('400x120')
        Label(self.sure, text="Are you sure you want to delete this profile?", font="none 11 bold").pack(pady=5, padx=5)
        yes_button = Button(self.sure, text="Yes", width= 10, command=self.del_profile_wrap)
        yes_button.pack(side = LEFT, pady=5, padx=30)
        no_button = Button(self.sure, text="No", width= 10, command=self.sure.destroy)
        no_button.pack(side = RIGHT, pady=5, padx=30)


    def del_profile_wrap(self):
        self.master.del_profile(self.title)
        self.sure.destroy()
