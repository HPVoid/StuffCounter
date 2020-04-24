from tkinter import *
from counterprofile1 import CounterProfile
from profile_frame import ProfileFrame
import win32api
import datetime

class App:
    def __init__(self):

        file1 = open("profile_dict.txt","r")
        self.profile_dict = eval(file1.read())
        self.profiles = {}
        for key, value in self.profile_dict.items():
            self.create_profile(key, value)

        file2 = open("click_count.txt","r")
        click_count_list = file2.read().split(" ")
        self.click_count_l = int(click_count_list[0])
        self.click_count_r = int(click_count_list[1])

        self.root = Tk()
        self.root.title("Counter")

        label_1 = Label(self.root, text="         Count Things:         ", font="none 30 bold")
        label_1.pack(padx=5)

        self.frame_just_count = Frame(self.root, bd=3, relief=RIDGE)
        self.frame_just_count.pack(fill=X)
        Label(self.frame_just_count, text="Just count stuff:", font="none 11 bold").pack(anchor = "w", padx=5)

        frame_sub = Frame(self.frame_just_count)
        frame_sub.pack(side=BOTTOM)

        self.entry = Entry(frame_sub, width = 30)
        self.entry.pack(side=LEFT, pady=5, padx=5, anchor="w")

        self.root.bind('<Return>', lambda e: self.add_profile_wrap())

        add = Button(frame_sub, text="Add something to count", width= 23, command=self.add_profile_wrap)
        add.pack(side=RIGHT, pady=5, padx=5, anchor="w")

        self.frame_dict = {}
        for key in self.profile_dict.keys():
            self.add_frame(key)

        self.error_window = None

        self.frame_special = Frame(self.root, bd=3, relief=RIDGE)
        self.frame_special.pack(fill=X)
        label_2 = Label(self.frame_special, text="Some other stuff regarding counting:", font="none 11 bold").pack(anchor = "w", padx=5)
        self.click = Button(self.frame_special, text="Activate click counter", command = self.click_counter, bg="white", width=17)
        self.click.pack(anchor="w", pady=5, padx=5, side=LEFT)
        self.reset = Button(self.frame_special, text="Reset", command = self.sure)
        self.reset.pack(pady=5, padx=5, side=LEFT)
        self.export_click = Button(self.frame_special, text="Export", command = self.click_export)
        self.export_click.pack(side=LEFT)

        self.label_4 = Label(self.frame_special, text="RMB: " + str(self.click_count_r), font="none 11 bold")
        self.label_4.pack(side=RIGHT, padx=5)
        self.label_3 = Label(self.frame_special, text="LMB: " + str(self.click_count_l), font="none 11 bold")
        self.label_3.pack(side=RIGHT, padx=5)

    def click_counter(self):

        self.stop_loop = False
        def stop_click_counter():
            self.stop_loop
            self.stop_loop = True
            self.click.configure(text="Activate click count", comman = self.click_counter, bg="white")

        self.click.configure(text="Deactivate click count", command = stop_click_counter, bg="red")
        self.state_left = win32api.GetKeyState(0x01)
        self.state_right = win32api.GetKeyState(0x02)

        def loop():
            left = win32api.GetKeyState(0x01)
            right = win32api.GetKeyState(0x02)
            if left != self.state_left:
                self.state_left = left
                print (self.state_left)

                if left < 0:
                    pass
                else:
                    self.click_count_l += 1
                    self.label_3.configure(text="LMB: " + str(self.click_count_l))
                    self.store_click_count()

                if self.stop_loop:

                    self.click_count_l -= 1
                    self.label_3.configure(text="LMB: " + str(self.click_count_l))
                    self.store_click_count()
                    return

            if right != self.state_right:
                self.state_right = right
                print (self.state_right)

                if right < 0:
                    pass
                else:
                    self.click_count_r += 1
                    self.label_4.configure(text="RMB: " + str(self.click_count_r))
                    self.store_click_count()

                if self.stop_loop:

                    self.click_count_r -= 1
                    self.label_4.configure(text="RMB: " + str(self.click_count_r))
                    self.store_click_count()
                    return

            self.root.after(50, loop)

        self.root.after(50, loop)

    def reset_click_counter(self):
        self.click_count_l = 0
        self.label_3.configure(text="LMB: " + str(self.click_count_l))
        self.click_count_r = 0
        self.label_4.configure(text="RMB: " + str(self.click_count_r))
        self.store_click_count()
        self.sure.destroy()

    def store_click_count(self):
        file2 = open("click_count.txt","w")
        file2.write(str(self.click_count_l) + " " + str(self.click_count_r))
        file2.close()

    def click_export(self):

        def write_exp_file():
            exp_file = open((filename_entry.get()+".txt"),"w")
            exp_file.write("LMB: "+str(self.click_count_l)+" RMB: "+str(self.click_count_r))
            exp_file.close()
            filename_entry.delete(0, 'end')
            export.destroy()

        export = Toplevel(self.root)
        export.title("Export click counts!")
        #export.geometry('400x120')
        Label(export, text="Filename:").pack(pady=5, padx=5,side=LEFT)
        filename_entry = Entry(export, width=30)
        filename_entry.pack(pady=5, padx=5,side=LEFT)
        export_button = Button(export, text="Export .txt-file", command = write_exp_file)
        export_button.pack(pady=5, padx=5,side=RIGHT)

    def add_profile_wrap(self):
        self.add_profile(self.entry.get())
        self.entry.delete(0, 'end')

    def add_frame(self, title):
        self.frame_dict[title] = ProfileFrame(self, title)

    def del_frame(self, title):
        self.frame_dict[title].frame.pack_forget()
        self.frame_dict[title].frame.destroy()
        self.frame_dict.pop(title)

    def add_profile(self, title):
        if title in self.profile_dict:
            self.error_2()
            return

        self.create_profile(title, 0)

        self.profile_dict[title] = self.profiles[title].counter
        #print(self.profile_dict)

        self.add_frame(title)
        self.update_profile_count(title)

    def call_profile(self, title):
        call_profile = self.profiles[title](self, title)

    def del_profile(self, title):
        self.profile_dict.pop(title)
        try:
            self.profiles[title].toplevel.destroy()
        except AttributeError:
            pass
        self.profiles.pop(title)
        self.del_frame(title)

        self.file = open("profile_dict.txt","w")
        self.file.write(str(self.profile_dict))
        self.file.close()

    def create_profile(self, title, counter):
        self.profiles[title] = CounterProfile(self, title, counter)

    def update_profile_count(self, title):
        self.profile_dict[title] = self.profiles[title].counter
        print(self.profile_dict)

        self.frame_dict[title].change_frame()

        self.file = open("profile_dict.txt","w")
        self.file.write(str(self.profile_dict))
        self.file.close()

    def error_2(self):

        if self.error_window == None or not self.error_window.winfo_exists():
            self.error_window = Toplevel(self.root)
            self.error_window.title("Error")
            Label(self.error_window, text="Can't add! The Profile name already exists.\nChoose another name.", font="none 14").pack()
            ok = Button(self.error_window, text="Ok", width=10,command=self.error_window.destroy)
            ok.pack()

    def sure(self):
        self.sure = Toplevel(self.root)
        self.sure.title("Reset counter?")
        self.sure.geometry('400x120')
        Label(self.sure, text="Are you sure you want to reset the counter?", font="none 11 bold").pack(pady=5, padx=5)
        yes_button = Button(self.sure, text="Yes", width= 10, command=self.reset_click_counter)
        yes_button.pack(side = LEFT, pady=5, padx=30)
        no_button = Button(self.sure, text="No", width= 10, command=self.sure.destroy)
        no_button.pack(side = RIGHT, pady=5, padx=30)

app = App()

app.root.mainloop()
