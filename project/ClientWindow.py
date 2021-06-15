import re, os, email, tkinter.ttk as ttk, tkinter.filedialog as fd
from tkinter import *
from tkhtmlview import HTMLScrolledText
from PIL import Image, ImageTk
from tkinter import scrolledtext
from Sender import send_email
from Downloader import download_emails
from Attachments import Attachemnts
from MailHeaders import MailHeaders


def is_valid_email(email_address):
    return re.match(r'\S+@\w+\.\w{2,}', email_address)


def get_body(mail):
    msg = email.message_from_string(mail)
    payload = msg.get_payload()[-1]
    return payload.get_payload()


class ClientWindow:
    def __init__(self, name, email_address, imap_server, smtp_server):
        self.name = name
        self.email_address = email_address
        self.imap_server = imap_server
        self.smtp_server = smtp_server

        self.inbox_mails = self.load_mails('Inbox')

        self.frame = Tk()
        self.frame.attributes('-zoomed', True)
        self.frame.resizable(0, 0)
        self.frame.title('Client window')
        self.icon = ImageTk.PhotoImage(Image.open('icons/icon.ico'))
        self.frame.iconphoto(False, self.icon)
        self.width = self.frame.winfo_screenwidth()
        self.height = self.frame.winfo_screenheight()
        self.create_widgets()
        self.inbox()
        self.frame.mainloop()

    def create_widgets(self):
        # write
        self.write_button = Button(self.frame, text='Write', width=20, command=lambda: self.write())
        self.write_button.place(x=30, y=30)
        # send
        self.send_button = Button(self.frame, text='Send', width=20, command=lambda: self.send(), state=DISABLED)
        # cancle
        self.cancle_button = Button(self.frame, text='Cancle', width=20, command=lambda: self.cancle())
        # from
        self.from_label = Label(self.frame, text='From:')
        self.from_label2 = Label(self.frame, text=self.email_address)
        # to
        self.to_label = Label(self.frame, text='To:')
        to_sv = StringVar()
        to_sv.trace('w', lambda name, index, mode, sv=to_sv: self.check())
        self.to_entry = Entry(self.frame, bd=2, textvariable=to_sv,
                                 highlightthickness=0, highlightbackground='red', highlightcolor='red')
        self.to_entry.bind('<FocusOut>', lambda entry: self.to_entry_on_focus_out())
        # topic
        self.topic_label = Label(self.frame, text='Topic:')
        self.topic_entry = Entry(self.frame, bd=2)
        # attach
        self.attach_label = Label(self.frame, text='Attach:')
        self.attach_button = Button(self.frame, text='Add', width=20, command=lambda: self.attach())
        # attachment_list
        self.attachments = Attachemnts(self.frame, self.width - 350, 50)
        # text
        self.text = scrolledtext.ScrolledText()

        # inbox
        self.inbox_button = Button(self.frame, text='Inbox', width=20, command=lambda: self.inbox())
        self.inbox_button.place(x=30, y=70)
        # open
        self.open_button = Button(self.frame, text='Open', width=20, command=lambda: self.open())
        # back
        self.back_button = Button(self.frame, text='Back', width=20, command=lambda: self.back())
        # page
        self.page_label = Label(self.frame, text='Page:')
        self.page_combobox = ttk.Combobox(state='readonly')
        self.page_combobox.bind('<<ComboboxSelected>>', lambda event: self.page_change())
        # mails headers
        self.mail_headers = MailHeaders(self, (self.height-140)//20-1)
        self.mail_headers.add_headers(self.inbox_mails[0], self.email_address)
        self.message_content = HTMLScrolledText(self.frame)

    def set_write_widgets_visibiltiy(self, visible):
        if visible:
            self.send_button.place(x=250, y=30)
            self.cancle_button.place(x=470, y=30)
            self.from_label.place(x=258, y=80)
            self.from_label2.place(x=300, y=80)
            self.to_label.place(x=276, y=110)
            self.to_entry.place(x=300, y=110, width=self.width - 400)
            self.topic_label.place(x=257, y=140)
            self.topic_entry.place(x=300, y=140, width=self.width - 400)
            self.attach_label.place(x=250, y=170)
            self.attach_button.place(x=300, y=170, width=40, height=20)
            self.attachments.place(x=250, y=200, width=self.width - 350, height=50)
            self.text.place(x=250, y=260, width=self.width - 350, height=self.height - 330)
        else:
            self.send_button.place_forget()
            self.cancle_button.place_forget()
            self.from_label.place_forget()
            self.from_label2.place_forget()
            self.to_label.place_forget()
            self.to_entry.place_forget()
            self.topic_label.place_forget()
            self.topic_entry.place_forget()
            self.attach_label.place_forget()
            self.attach_button.place_forget()
            self.attachments.place_forget()
            self.text.place_forget()

    def set_inbox_widgets_visibiltiy(self, visible):
        if visible:
            self.open_button.place(x=250, y=30)
            self.open_button.config(state=DISABLED)
            self.page_label.place(x=self.width-190, y=32)
            self.page_combobox.place(x=self.width-150, y=32, width=50)
            self.mail_headers.place(x=250, y=70, width=self.width-350, height=(self.height-140)-7)
        else:
            self.open_button.place_forget()
            self.page_label.place_forget()
            self.page_combobox.place_forget()
            self.mail_headers.place_forget()

    def set_open_widgets_visibiltiy(self, visible):
        if visible:
            self.back_button.place(x=250, y=30)
            self.back_button.config(state=NORMAL)
            self.message_content.place(x=250, y=70, width=self.width-350, height=(self.height-140)-7)
        else:
            self.back_button.place_forget()
            self.message_content.place_forget()

    def write(self):
        self.set_inbox_widgets_visibiltiy(False)
        self.set_open_widgets_visibiltiy(False)
        self.set_write_widgets_visibiltiy(True)
    
    def send(self):
        send_email(self.smtp_server, self.email_address, self.to_entry.get(), self.topic_entry.get(),
                   self.text.get('1.0', 'end-1c'), self.attachments.get())
        self.inbox()

    def cancle(self):
        self.to_entry.config(highlightthickness=0)
        self.to_entry.delete(0, 'end')
        self.topic_entry.delete(0, 'end')
        self.text.delete('1.0','end')
        self.attachments.clear()
        self.send_button.config(state=DISABLED)
        self.set_write_widgets_visibiltiy(False)
        self.set_inbox_widgets_visibiltiy(True)

    def attach(self):
        path = fd.askopenfile(mode='r').name
        self.attachments.add(path)

    def inbox(self):
        self.cancle()
        self.set_open_widgets_visibiltiy(False)
        status, messages = self.imap_server.select('INBOX')
        messages = int(messages[0])
        if self.inbox_mails[1] < messages:
            new_mails, count = download_emails(self.imap_server, self.inbox_mails[1])
            self.inbox_mails[0] = new_mails+self.inbox_mails[0]
            self.inbox_mails[1] += count
            self.save_mails(self.inbox_mails[0], 'Inbox')
            self.mail_headers.add_headers(new_mails, self.email_address)

        self.fill_page_combobox(self.mail_headers.get_page_count())
        self.mail_headers.clear_selction()
        self.set_inbox_widgets_visibiltiy(True)

    def open(self):
        ind = self.mail_headers.get_selected()
        self.mail_headers.clear_selction()
        mail = self.get_mail(ind)
        mail_body = get_body(mail)
        self.message_content.set_html(mail_body, False)
        self.set_inbox_widgets_visibiltiy(False)
        self.set_open_widgets_visibiltiy(True)

    def back(self):
        self.inbox()

    def page_change(self):
        n = int(self.page_combobox.get())
        self.mail_headers.set_page(n)

    def trash(self):
        self.set_write_widgets_visibiltiy(False)

    def check(self):
        if is_valid_email(self.to_entry.get()):
            self.send_button.config(state=NORMAL)
            self.to_entry.config(highlightthickness=0)
        else:
            self.send_button.config(state=DISABLED)

    def to_entry_on_focus_out(self):
        to = self.to_entry.get()
        if not to or is_valid_email(to):
            self.to_entry.config(highlightthickness=0)
        else:
            self.to_entry.config(highlightthickness=2)

    def load_mails(self, mailbox):
        home = home = os.path.expanduser('~')
        if mailbox == 'Inbox':
            path = home + '/.mailclient/Mails/Inbox'
            if not os.path.exists(path):
                return ['', 0]
            else:
                with open(path, 'r') as infile:
                    mails = infile.read()
                return [mails, len(re.findall(r'#####<EMAIL>#####', mails))]

    def save_mails(self, mails, mailbox):
        home = home = os.path.expanduser('~')
        path = home + '/.mailclient/Mails'
        if not os.path.exists(path):
            os.mkdir(path)
        if mailbox == 'Inbox':
            path += '/Inbox'
            with open(path, 'w') as outfile:
                outfile.writelines(mails)

    def fill_page_combobox(self, n):
        self.page_combobox.set('')
        self.page_combobox.config(values=[str(i) for i in range(1, n+1)])
        n = self.mail_headers.get_page()
        self.page_combobox.current(n-1)
        self.mail_headers.set_page(n)

    def get_mail(self, id):
        regex = r'#####<EMAIL>##### '+str(id)+'\n'
        start = re.search(regex, self.inbox_mails[0]).regs[0][1]
        end = self.inbox_mails[0].find('#####<EMAIL>#####', start)
        if end == -1:
            return self.inbox_mails[0][start:]
        else:
            return self.inbox_mails[0][start:end]