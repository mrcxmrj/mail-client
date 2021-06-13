from tkinter import *
import tkinter.filedialog as fd
from PIL import Image, ImageTk


class ClientWindow:
    def __init__(self, email_address):
        self.email_address = email_address
        self.frame = Tk()
        self.frame.attributes('-zoomed', True)
        self.frame.resizable(0, 0)
        self.frame.title("Client window")
        self.icon = ImageTk.PhotoImage(Image.open("icons/icon.ico"))
        self.frame.iconphoto(False, self.icon)
        self.width = self.frame.winfo_screenwidth()
        self.height = self.frame.winfo_screenheight()
        self.create_widgets()
        self.frame.mainloop()

    def create_widgets(self):
        # write
        self.write_button = Button(self.frame, text="Write", width=20, command=lambda: self.write())
        self.write_button.place(x=30, y=30)
        # send
        self.send_button = Button(self.frame, text="Send", width=20, command=lambda: self.send())
        # send
        self.save_button = Button(self.frame, text="Save", width=20, command=lambda: self.save())
        # cancle
        self.cancle_button = Button(self.frame, text="Cancle", width=20, command=lambda: self.cancle())
        # from
        self.from_label = Label(self.frame, text="From:")
        self.from_label2 = Label(self.frame, text=self.email_address)
        # to
        self.to_label = Label(self.frame, text="To:")
        self.to_entry = Entry(self.frame, bd=2)
        # topic
        self.topic_label = Label(self.frame, text="Topic:")
        self.topic_entry = Entry(self.frame, bd=2)
        # attach
        self.attach_label = Label(self.frame, text="Attach:")
        self.attach_button = Button(self.frame, text="Add", width=20, command=lambda: self.attach())
        # text
        self.text = Text(self.frame, bd=2)

        # inbox
        self.inbox_button = Button(self.frame, text="Inbox", width=20, command=lambda: self.inbox())
        self.inbox_button.place(x=30, y=70)

        # trash
        self.trash_button = Button(self.frame, text="Trash", width=20, command=lambda: self.trash())
        self.trash_button.place(x=30, y=110)

    def set_write_widgets_visibiltiy(self, visible):
        if visible:
            self.send_button.place(x=250, y=30)
            self.save_button.place(x=470, y=30)
            self.cancle_button.place(x=690, y=30)
            self.from_label.place(x=258, y=80)
            self.from_label2.place(x=300, y=80)
            self.to_label.place(x=276, y=110)
            self.to_entry.place(x=300, y=110, width=self.width - 400)
            self.topic_label.place(x=257, y=140)
            self.topic_entry.place(x=300, y=140, width=self.width - 400)
            self.attach_label.place(x=250, y=170)
            self.attach_button.place(x=300, y=170, height=20)
            self.text.place(x=250, y=200, width=self.width - 350, height=self.height - 300)
        else:
            self.send_button.place_forget()
            self.save_button.place_forget()
            self.cancle_button.place_forget()
            self.from_label.place_forget()
            self.from_label2.place_forget()
            self.to_label.place_forget()
            self.to_entry.place_forget()
            self.topic_label.place_forget()
            self.topic_entry.place_forget()
            self.attach_label.place_forget()
            self.attach_button.place_forget()
            self.text.place_forget()
    
    def write(self):
        self.set_write_widgets_visibiltiy(True)
    
    def send(self):
        pass
    
    def save(self):
        pass

    def cancle(self):
        self.set_write_widgets_visibiltiy(False)

    def attach(self):
        path = fd.askopenfile(mode="r")

    def inbox(self):
        self.set_write_widgets_visibiltiy(False)

    def trash(self):
        self.set_write_widgets_visibiltiy(False)
