from tkinter import *
from PIL import Image, ImageTk
import getpass
import re


def is_valid_email(email):
    return re.match(r"\S+@\w+\.\w{2,}", email)


class LoginWindow:
    def __init__(self):
        self.frame = Tk()
        self.frame.title("Logging window")
        self.icon = ImageTk.PhotoImage(Image.open("icons/icon.ico"))
        self.frame.iconphoto(False, self.icon)
        self.frame.geometry("647x661")
        self.frame.resizable(0, 0)
        self.create_widgets()
        self.frame.mainloop()

    def create_widgets(self):
        # continue
        self.continue_button = Button(self.frame, text="Continue", state=DISABLED, command=lambda: self.go_on())
        self.continue_button.place(x=517, y=600)
        # name
        self.name_label = Label(self.frame, text="Your name:")
        self.name_label.place(x=30, y=110)
        name_sv = StringVar()
        name_sv.trace("w", lambda name, index, mode, sv=name_sv: self.check())
        self.name_entry = Entry(self.frame, width=50, bd=2)
        # email
        self.email_label = Label(self.frame, text="Email address:")
        self.email_label.place(x=30, y=155)
        email_sv = StringVar()
        email_sv.trace("w", lambda name, index, mode, sv=email_sv: self.check())
        self.email_entry = Entry(self.frame, width=50, bd=2, textvariable=email_sv,
                                 highlightthickness=0, highlightbackground="red", highlightcolor="red")
        self.email_entry.bind("<FocusOut>", lambda entry: self.email_entry_on_focus_out())
        self.email_entry.place(x=195, y=155)
        self.name_entry.config(textvariable=name_sv)
        self.name_entry.insert(0, getpass.getuser())
        self.name_entry.place(x=195, y=110)
        # password
        self.password_label = Label(self.frame, text="Password:")
        self.password_label.place(x=30, y=200)
        self.password_entry = Entry(self.frame, width=50, bd=2, show="*")
        self.password_entry.place(x=195, y=200)
        self.password_check_box_label = Label(self.frame, text="Remember password")
        self.password_check_box_label.place(x=220, y=245)
        self.remember_password_var = IntVar()
        self.remember_password_check_box = Checkbutton(self.frame, bd=2,
                                                       variable=self.remember_password_var, onvalue=1, offvalue=0)
        self.remember_password_check_box.place(x=187, y=244)
        self.show_password_image = ImageTk.PhotoImage(Image.open("icons/show_password_icon.bmp"))
        self.hide_password_image = ImageTk.PhotoImage(Image.open("icons/hide_password_icon.bmp"))
        self.show_password_var = IntVar()
        self.show_password_check_box = Checkbutton(self.frame, bd=0, image=self.hide_password_image,
                                                   selectimage=self.show_password_image, indicatoron=False,
                                                   variable=self.show_password_var, onvalue=1, offvalue=0,
                                                   command=lambda: self.show_password_change())
        self.show_password_check_box.place(x=610, y=200)
        # cancle
        self.cancle_button = Button(self.frame, text="Cancel", command=self.frame.destroy)
        self.cancle_button.place(x=30, y=600)

    def check(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        if name and email and is_valid_email(email):
            self.continue_button.config(state=NORMAL)
        else:
            self.continue_button.config(state=DISABLED)

    def email_entry_on_focus_out(self):
        self.check_email()

    def check_email(self):
        email = self.email_entry.get()
        if not email or is_valid_email(email):
            self.email_entry.config(highlightthickness=0)
        else:
            self.email_entry.config(highlightthickness=2)

    def show_password_change(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def go_on(self):
        "TODO"
        pass